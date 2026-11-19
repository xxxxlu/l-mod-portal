#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/steam_patch_monitor.py · 补丁雷达 v2 巡检脚本

判定规则以 docs/RADAR_V2_CONTRACT.md 第 2 节为准，用法见 docs/STEAM_PATCH_MONITOR_GUIDE.md。

每款带 steamAppId 的游戏读四样东西：
  1. Steam 公共分支当前 build 和它的发布时间 timeupdated（api.steamcmd.net）
  2. 最新一条官方公告（ISteamNews，只用来展示，不参与判定）
  3. Mod 框架资料（scripts/radar_frameworks/part-*.json，可能缺文件或缺条目）
  4. 风灵月影修改器最后更新时间（public/trainers.json → games.<id>.modified）

判定（RECENT_DAYS = 14）：
  build ≤ 14 天，且框架资料 hooksExe == true  → red    / recent-update-hooks
  build ≤ 14 天                              → yellow / recent-update
  修改器更新时间早于 build 超过 1 天          → yellow / trainer-behind
  其余                                       → green  / quiet

任何一个 Steam 请求失败（超时、HTTP 错误、返回格式不对），这款游戏的雷达字段一律保持原值，
报告里列为「本次未取到」。非 Steam 游戏（steamAppId 为 0 或缺失）不巡检、不写字段。

报告里写一行 `<!-- radar-new-red: N -->`，工作流读它决定要不要开预警单。
纯标准库，零第三方依赖。
"""

import argparse
import datetime
import glob
import http.client
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

# ==============================================================================
# 路径与常量
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAMES_JSON_PATH = os.path.join(BASE_DIR, 'src/data/games_top100.json')
DATA_JS_PATH = os.path.join(BASE_DIR, 'public/data.js')
TRANS_JSON_PATH = os.path.join(BASE_DIR, 'src/i18n/translations.json')
TRAINERS_PATH = os.path.join(BASE_DIR, 'public/trainers.json')
FRAMEWORKS_DIR = os.path.join(BASE_DIR, 'scripts/radar_frameworks')
REPORT_PATH_DEFAULT = os.path.join(BASE_DIR, 'docs/PATCH_MONITOR_LATEST.md')

RECENT_DAYS = 14
TRAINER_TOLERANCE_DAYS = 1
MIN_REQUEST_INTERVAL = 0.5
DEFAULT_REQUEST_INTERVAL = 0.6
DEFAULT_TIMEOUT = 10
RETRY_BACKOFF_SECONDS = 3

UTC = datetime.timezone.utc

# 原因码 → 状态（契约 2.2 节）
REASON_STATUS = {
    'recent-update-hooks': 'red',
    'recent-update': 'yellow',
    'trainer-behind': 'yellow',
    'quiet': 'green',
}

# radarStatusText 固定四句（契约 2.3 节）
STATUS_TEXT = {
    'quiet': '🟢 近 14 天无更新',
    'recent-update': '🟡 刚更新 · Mod/修改器可能要等适配',
    'trainer-behind': '🟡 修改器早于当前游戏版本',
    'recent-update-hooks': '🔴 刚更新 · {framework} 待适配，先别更新',
}

# 写进数据和报告的文案里不许出现的说法（没人做过的事）
BANNED_PHRASES = ('实测', '完美兼容', '老L团队')

# 脚本会写的全部字段；verifiedPatch 不碰
RADAR_FIELDS = (
    'compatibilityStatus', 'radarReason', 'radarStatusText', 'latestSteamPatch', 'latestSteamPatchUrl',
    'steamBuildId', 'steamBuildUpdatedAt', 'steamLastChecked', 'radarFramework',
    'radarSummary', 'radarRiskTitle', 'radarRiskDesc', 'emergencyAlert',
)

GENERIC_RISK_DESC = {
    'default': '游戏更新后，依赖框架的 Mod 和修改器可能要等作者适配；想稳妥可在 Steam 属性里把自动更新改成「仅在启动时更新」，并先备份存档。',
    'trainer-behind': '修改器早于当前游戏版本时，部分功能可能失效；用之前先备份存档，等修改器更新后再用更稳妥。',
}

SIMULATED_FRAMEWORK_NAME = 'Mod 框架（演练）'

HTTP_HEADERS = {
    'User-Agent': 'L-MOD-Patch-Radar/2.0 (+steam_patch_monitor.py)',
    'Accept': 'application/json',
}

# public/data.js 的布局：window.GAMES_DATA = [...];\n\nwindow.GAMES_DATABASE = ...;
# 主数据 src/data/games_top100.json 不进 git，所以 CI 和新克隆里 public/data.js 是唯一一份游戏库。
GAMES_DATA_HEAD = "window.GAMES_DATA = "
GAMES_DATA_TAIL = ";\n\nwindow.GAMES_DATABASE"


# ==============================================================================
# 时间工具
# ==============================================================================
def utc_now():
    return datetime.datetime.now(UTC)


def parse_iso_utc(value):
    """ISO 8601 字符串 → 带时区的 UTC datetime。没有时区的按 UTC 看；解析不了返回 None。"""
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    if text.endswith('Z') or text.endswith('z'):
        text = text[:-1] + '+00:00'
    try:
        dt = datetime.datetime.fromisoformat(text)
    except ValueError:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


def iso_z(dt):
    return dt.astimezone(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')


def fmt_date(dt):
    return dt.astimezone(UTC).strftime('%Y-%m-%d') if dt else '—'


def _is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def _is_url(value):
    return isinstance(value, str) and re.match(r'^https?://\S+$', value) is not None


def _dig(obj, *keys):
    for key in keys:
        if not isinstance(obj, dict):
            return None
        obj = obj.get(key)
    return obj


# ==============================================================================
# 游戏库读写（public/data.js 的 GAMES_DATA 段）
# ==============================================================================
def _games_data_span(js_text, path=DATA_JS_PATH):
    """返回 data.js 文本里 GAMES_DATA 数组的 (start, end) 偏移。"""
    a = js_text.find(GAMES_DATA_HEAD)
    if a < 0:
        raise ValueError(f"{path}: 找不到 '{GAMES_DATA_HEAD.strip()}'")
    a += len(GAMES_DATA_HEAD)
    b = js_text.find(GAMES_DATA_TAIL, a)
    if b < 0:
        raise ValueError(f"{path}: 找不到 GAMES_DATA 的结尾（'{GAMES_DATA_TAIL.strip()}'）")
    return a, b


def load_games(data_js_path=DATA_JS_PATH, use_master=None):
    """读游戏库：本地有主数据 JSON 时读它，否则读 public/data.js 的 GAMES_DATA 段。"""
    if use_master is None:
        use_master = os.path.abspath(data_js_path) == DATA_JS_PATH and os.path.exists(GAMES_JSON_PATH)
    if use_master:
        with open(GAMES_JSON_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    with open(data_js_path, 'r', encoding='utf-8') as f:
        js_text = f.read()
    a, b = _games_data_span(js_text, data_js_path)
    return json.loads(js_text[a:b])


def save_games(games, data_js_path=DATA_JS_PATH, use_master=False):
    """写回游戏库。

    - 有主数据（本地开发）：写 games_top100.json，再整份重新生成 public/data.js（沿用旧行为）。
    - 没有主数据（GitHub Actions / 新克隆）：只替换 data.js 里 GAMES_DATA 段，
      TRANSLATIONS_DATA 等其它部分一个字节都不动。
    修改器字段（hasTrainer / trainerInfo …）归 fling_trainer_sync.py 管，这里原样保留。
    """
    if use_master:
        with open(GAMES_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(games, f, ensure_ascii=False, indent=2)
        translations = {}
        if os.path.exists(TRANS_JSON_PATH):
            with open(TRANS_JSON_PATH, 'r', encoding='utf-8') as f:
                translations = json.load(f)
        with open(data_js_path, 'w', encoding='utf-8') as f:
            f.write("// L-MOD Vault Offline Database (Auto-bundled by Steam Patch Sentinel)\n")
            f.write(GAMES_DATA_HEAD + json.dumps(games, ensure_ascii=False, indent=2) + ";\n\n")
            f.write("window.GAMES_DATABASE = window.GAMES_DATA;\n\n")
            if translations:
                f.write("window.TRANSLATIONS_DATA = " + json.dumps(translations, ensure_ascii=False, indent=2) + ";\n")
        return
    with open(data_js_path, 'r', encoding='utf-8') as f:
        js_text = f.read()
    a, b = _games_data_span(js_text, data_js_path)
    js_text = js_text[:a] + json.dumps(games, ensure_ascii=False, indent=2) + js_text[b:]
    with open(data_js_path, 'w', encoding='utf-8') as f:
        f.write(js_text)


# ==============================================================================
# 框架资料（scripts/radar_frameworks/part-*.json）
# ==============================================================================
FRAMEWORK_REQUIRED_KEYS = (
    'id', 'rank', 'steamAppId', 'framework', 'hooksExe', 'modSupport', 'afterUpdate', 'sources', 'checkedAt',
)
MOD_SUPPORT_VALUES = ('official', 'workshop', 'community', 'none', None)
AFTER_UPDATE_LIMITS = {'zh-CN': 60, 'en': 120}
JUDGMENT_KEYS = ('framework', 'hooksExe', 'modSupport', 'afterUpdate')


class FrameworkData:
    """合并后的框架资料。errors = 被跳过的条目/文件，warnings = 照用但要提醒的地方。"""

    def __init__(self, directory):
        self.directory = directory
        self.entries = {}
        self.origin = {}
        self.files = []        # [(文件名, 数组长度)]
        self.errors = []
        self.warnings = []
        self.missing_dir = False

    def get(self, game_id):
        return self.entries.get(game_id)


def validate_framework_entry(entry):
    """校验一条框架资料。返回 (errors, warnings)：有 errors 就整条跳过。"""
    if not isinstance(entry, dict):
        return ['不是 JSON 对象'], []
    errors, warnings = [], []

    missing = [k for k in FRAMEWORK_REQUIRED_KEYS if k not in entry]
    if missing:
        errors.append('缺字段 ' + '、'.join(missing))

    gid = entry.get('id')
    if not (isinstance(gid, str) and gid.strip()):
        errors.append('id 必须是非空字符串')
    if 'rank' in entry and not _is_int(entry['rank']):
        errors.append('rank 必须是整数')
    if 'steamAppId' in entry:
        appid = entry['steamAppId']
        if not (appid is None or (_is_int(appid) and appid >= 0)):
            errors.append('steamAppId 必须是非负整数或 null')

    fw = entry.get('framework')
    if fw is not None:
        if not isinstance(fw, dict):
            errors.append('framework 必须是 {name, url} 或 null')
        else:
            if not (isinstance(fw.get('name'), str) and fw['name'].strip()):
                errors.append('framework.name 必须是非空字符串')
            if not _is_url(fw.get('url')):
                errors.append('framework.url 必须是 http(s) 链接')

    hooks = entry.get('hooksExe')
    if not (hooks is None or isinstance(hooks, bool)):
        errors.append('hooksExe 只能是 true / false / null')
    elif hooks is True and fw is None:
        errors.append('hooksExe 为 true 但 framework 为 null（红灯文案需要框架名）')

    if 'modSupport' in entry and entry['modSupport'] not in MOD_SUPPORT_VALUES:
        errors.append('modSupport 只能是 official / workshop / community / none / null')

    after = entry.get('afterUpdate')
    if after is not None:
        if not isinstance(after, dict):
            errors.append('afterUpdate 必须是 {"zh-CN", "en"} 或 null')
        else:
            for lang, limit in AFTER_UPDATE_LIMITS.items():
                text = after.get(lang)
                if not (isinstance(text, str) and text.strip()):
                    errors.append(f'afterUpdate.{lang} 必须是非空字符串')
                elif len(text.strip()) > limit:
                    warnings.append(f'afterUpdate.{lang} 超长（{len(text.strip())} > {limit}）')

    if 'sources' in entry:
        sources = entry['sources']
        if not isinstance(sources, list) or not all(_is_url(s) for s in sources):
            errors.append('sources 必须是 http(s) 链接数组')
        elif not sources and any(entry.get(k) is not None for k in JUDGMENT_KEYS):
            errors.append('有非 null 的判断，但 sources 为空')

    checked = entry.get('checkedAt')
    if 'checkedAt' in entry and not (isinstance(checked, str) and re.match(r'^\d{4}-\d{2}-\d{2}$', checked)):
        warnings.append('checkedAt 不是 YYYY-MM-DD')

    return errors, warnings


def _part_sort_key(path):
    m = re.search(r'part-(\d+)\.json$', path)
    return (int(m.group(1)) if m else 10 ** 9, path)


def load_frameworks(directory=FRAMEWORKS_DIR, games=None):
    """把所有 part-*.json 合起来。缺目录、缺文件、缺条目都照常返回；坏文件/坏条目跳过并记下来。"""
    data = FrameworkData(directory)
    if not os.path.isdir(directory):
        data.missing_dir = True
        return data
    by_id = {g.get('id'): g for g in games} if games is not None else None

    for path in sorted(glob.glob(os.path.join(directory, 'part-*.json')), key=_part_sort_key):
        name = os.path.basename(path)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                raw = json.load(f)
        except (OSError, ValueError) as exc:
            data.errors.append(f'{name}: 读不了或不是合法 JSON（{exc}），整份跳过')
            continue
        if not isinstance(raw, list):
            data.errors.append(f'{name}: 顶层必须是数组，整份跳过')
            continue
        data.files.append((name, len(raw)))

        for idx, entry in enumerate(raw):
            label = f'{name}[{idx}]'
            if isinstance(entry, dict) and isinstance(entry.get('id'), str):
                label += f' {entry["id"]}'
            errors, warnings = validate_framework_entry(entry)
            if not errors and by_id is not None:
                game = by_id.get(entry['id'])
                if game is None:
                    errors.append('GAMES_DATA 里没有这个 id')
                else:
                    if entry['rank'] != game.get('rank'):
                        warnings.append(f'rank 与 GAMES_DATA 不一致（{entry["rank"]} ≠ {game.get("rank")}）')
                    if (entry.get('steamAppId') or 0) != (game.get('steamAppId') or 0):
                        warnings.append(f'steamAppId 与 GAMES_DATA 不一致（{entry.get("steamAppId")} ≠ {game.get("steamAppId")}）')
            if errors:
                data.errors.append(f'{label}: ' + '；'.join(errors))
                continue
            gid = entry['id']
            if gid in data.entries:
                data.errors.append(f'{label}: id 重复（已在 {data.origin[gid]} 出现），这一条忽略')
                continue
            for w in warnings:
                data.warnings.append(f'{label}: {w}')
            data.entries[gid] = entry
            data.origin[gid] = name
    return data


# ==============================================================================
# 修改器时间（public/trainers.json）
# ==============================================================================
def load_trainer_times(path=TRAINERS_PATH):
    """返回 ({game_id: UTC datetime}, 说明或 None)。modified 是站点本地时间、无时区，按 UTC 看。"""
    if not os.path.exists(path):
        return {}, f'{os.path.relpath(path, BASE_DIR)} 不存在，本次不判 trainer-behind'
    try:
        with open(path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
    except (OSError, ValueError) as exc:
        return {}, f'{os.path.relpath(path, BASE_DIR)} 读不了（{exc}），本次不判 trainer-behind'
    out = {}
    games = manifest.get('games') if isinstance(manifest, dict) else None
    if not isinstance(games, dict):
        return {}, 'trainers.json 里没有 games 对象，本次不判 trainer-behind'
    for gid, info in games.items():
        dt = parse_iso_utc(info.get('modified')) if isinstance(info, dict) else None
        if dt:
            out[gid] = dt
    return out, None


# ==============================================================================
# Steam 数据
# ==============================================================================
class FetchError(Exception):
    """这一款这次没取到 Steam 数据。"""


def store_news_url(appid):
    return f'https://store.steampowered.com/news/app/{appid}'


def parse_steamcmd_payload(payload, appid):
    """api.steamcmd.net/v1/info/<appid> → {'buildid': str, 'updated_at': datetime}；格式不对抛 FetchError。"""
    if not isinstance(payload, dict) or payload.get('status') != 'success':
        raise FetchError('steamcmd 返回的 status 不是 success')
    public = _dig(payload, 'data', str(appid), 'depots', 'branches', 'public')
    if not isinstance(public, dict):
        raise FetchError('steamcmd 返回里没有 depots.branches.public')
    buildid = public.get('buildid')
    stamp = public.get('timeupdated') or public.get('timebuildupdated')
    if buildid is None or not str(buildid).strip().isdigit():
        raise FetchError(f'public 分支 buildid 不对：{buildid!r}')
    try:
        stamp = int(stamp)
    except (TypeError, ValueError):
        raise FetchError(f'public 分支 timeupdated 不对：{stamp!r}')
    if stamp <= 0:
        raise FetchError(f'public 分支 timeupdated 不对：{stamp!r}')
    return {'buildid': str(buildid).strip(), 'updated_at': datetime.datetime.fromtimestamp(stamp, UTC)}


def parse_news_payload(payload):
    """ISteamNews/GetNewsForApp → 最新一条 {'title', 'url', 'date'}；没有公告返回 None；格式不对抛 FetchError。"""
    items = _dig(payload, 'appnews', 'newsitems')
    if not isinstance(items, list):
        raise FetchError('ISteamNews 返回里没有 appnews.newsitems')
    if not items:
        return None
    item = items[0] if isinstance(items[0], dict) else {}
    title = ' '.join(str(item.get('title') or '').split())
    url = item.get('url') if _is_url(item.get('url')) else None
    try:
        stamp = int(item.get('date') or 0)
    except (TypeError, ValueError):
        stamp = 0
    date = datetime.datetime.fromtimestamp(stamp, UTC) if stamp > 0 else None
    if not title and not url:
        return None
    return {'title': title, 'url': url, 'date': date}


class SteamClient:
    """联网取数：每个请求之间至少隔 interval 秒；超时/429/5xx 重试一次；最后还失败就抛 FetchError。"""

    STEAMCMD_URL = 'https://api.steamcmd.net/v1/info/{appid}'
    NEWS_URL = ('https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/'
                '?appid={appid}&count=1&maxlength=1&feeds=steam_community_announcements&format=json')

    def __init__(self, timeout=DEFAULT_TIMEOUT, interval=DEFAULT_REQUEST_INTERVAL, retries=1,
                 sleep=time.sleep, clock=time.monotonic, opener=urllib.request.urlopen):
        self.timeout = timeout
        self.interval = max(interval, MIN_REQUEST_INTERVAL)
        self.retries = retries
        self._sleep = sleep
        self._clock = clock
        self._open = opener
        self._last_request = None
        self.request_count = 0

    def _throttle(self):
        if self._last_request is not None:
            wait = self.interval - (self._clock() - self._last_request)
            if wait > 0:
                self._sleep(wait)
        self._last_request = self._clock()

    def _get_json(self, url):
        last_error = '未知错误'
        for attempt in range(self.retries + 1):
            self._throttle()
            self.request_count += 1
            retryable = True
            try:
                req = urllib.request.Request(url, headers=HTTP_HEADERS)
                with self._open(req, timeout=self.timeout) as resp:
                    return json.loads(resp.read().decode('utf-8'))
            except urllib.error.HTTPError as exc:
                last_error = f'HTTP {exc.code}'
                retryable = exc.code == 429 or exc.code >= 500
            except ValueError as exc:  # JSON 解析失败 / 解码失败
                last_error = f'返回不是合法 JSON（{exc.__class__.__name__}）'
                retryable = False
            except (urllib.error.URLError, OSError, http.client.HTTPException) as exc:  # 含超时、断连
                reason = getattr(exc, 'reason', None) or exc
                last_error = f'网络错误（{reason}）'
            if not retryable or attempt >= self.retries:
                break
            self._sleep(RETRY_BACKOFF_SECONDS)
        raise FetchError(last_error)

    def fetch_build(self, appid):
        try:
            payload = self._get_json(self.STEAMCMD_URL.format(appid=appid))
        except FetchError as exc:
            raise FetchError(f'steamcmd：{exc}')
        return parse_steamcmd_payload(payload, appid)

    def fetch_latest_news(self, appid):
        try:
            payload = self._get_json(self.NEWS_URL.format(appid=appid))
        except FetchError as exc:
            raise FetchError(f'ISteamNews：{exc}')
        return parse_news_payload(payload)


class SnapshotClient:
    """--offline：不联网，从 JSON 快照取数。快照里没有的游戏一律算「没取到」。

    快照格式（键是 appid 字符串）：
      {"1086940": {"buildid": "123", "timeupdated": "2026-11-17T08:00:00Z",   # 或 "daysAgo": 2
                   "news": {"title": "...", "url": "https://...", "date": "2026-11-17T08:00:00Z"}},
       "1245620": {"error": "模拟超时"}}
    """

    def __init__(self, snapshot=None, now=None):
        self.snapshot = snapshot or {}
        self.now = now or utc_now()
        self.request_count = 0

    def _entry(self, appid):
        entry = self.snapshot.get(str(appid))
        if entry is None:
            raise FetchError('离线模式：快照里没有这款')
        if entry.get('error'):
            raise FetchError(f'离线快照：{entry["error"]}')
        return entry

    def fetch_build(self, appid):
        entry = self._entry(appid)
        if 'daysAgo' in entry:
            updated = self.now - datetime.timedelta(days=float(entry['daysAgo']))
        else:
            updated = parse_iso_utc(entry.get('timeupdated'))
        if updated is None or not str(entry.get('buildid', '')).isdigit():
            raise FetchError('离线快照：buildid / timeupdated 不对')
        return {'buildid': str(entry['buildid']), 'updated_at': updated}

    def fetch_latest_news(self, appid):
        entry = self._entry(appid)
        if entry.get('newsError'):
            raise FetchError(f'离线快照：{entry["newsError"]}')
        news = entry.get('news')
        if not news:
            return None
        return {'title': news.get('title') or '', 'url': news.get('url') if _is_url(news.get('url')) else None,
                'date': parse_iso_utc(news.get('date'))}


# ==============================================================================
# 判定
# ==============================================================================
def classify(now, build_updated_at, framework_entry=None, trainer_modified=None):
    """契约 2.2 节。返回原因码。"""
    build_age = now - build_updated_at
    if build_age <= datetime.timedelta(days=RECENT_DAYS):
        hooks = bool(framework_entry) and framework_entry.get('hooksExe') is True
        return 'recent-update-hooks' if hooks else 'recent-update'
    if trainer_modified is not None and \
            trainer_modified < build_updated_at - datetime.timedelta(days=TRAINER_TOLERANCE_DAYS):
        return 'trainer-behind'
    return 'quiet'


def status_text(reason, framework_name=None):
    text = STATUS_TEXT[reason]
    if reason == 'recent-update-hooks':
        text = text.format(framework=framework_name or 'Mod 框架')
    return text


def is_new_red(status, buildid, prev_status, prev_buildid):
    """契约 2.4 节：这次 red，且上次不是 red 或上次 build 不一样。"""
    if status != 'red':
        return False
    return prev_status != 'red' or str(prev_buildid or '') != str(buildid)


def _titles(game):
    titles = game.get('titles') if isinstance(game.get('titles'), dict) else {}
    zh = titles.get('zh-CN') or game.get('title') or game.get('id')
    en = titles.get('en') or game.get('title') or game.get('id')
    return zh, en


def build_radar_fields(game, reason, build, news, framework_entry, trainer_modified, now, framework_name=None):
    """算出要写回的字段（不改 game）。返回 (fields, emergency_alert 或 None)。

    fields 里值为 None 的 latestSteamPatch 表示「删掉这个字段」；radarFramework 为 None 就写 null。
    """
    status = REASON_STATUS[reason]
    fw = framework_entry.get('framework') if framework_entry else None
    fw_name = framework_name or (fw['name'] if fw else None)
    appid = game.get('steamAppId')
    zh_title, en_title = _titles(game)
    build_date = fmt_date(build['updated_at'])
    buildid = build['buildid']

    if reason == 'quiet':
        summary = f'Steam 公共分支最近一次更新在 {build_date}（build {buildid}），近 {RECENT_DAYS} 天没有新版本。'
        risk_title = f'💡 近 {RECENT_DAYS} 天无更新'
    elif reason == 'recent-update':
        summary = f'Steam 在 {build_date} 推送了新版本（build {buildid}）。依赖框架的 Mod 和修改器可能要等作者适配。'
        risk_title = '⚠️ 刚更新 · Mod/修改器可能要等适配'
    elif reason == 'trainer-behind':
        summary = (f'风灵月影修改器最后更新于 {fmt_date(trainer_modified)}，早于 Steam 当前版本'
                   f'（{build_date}，build {buildid}），可能和当前版本对不上。')
        risk_title = '⚠️ 修改器早于当前游戏版本'
    else:  # recent-update-hooks
        summary = (f'Steam 在 {build_date} 推送了新版本（build {buildid}）。{fw_name} 按游戏 exe 的具体版本挂钩，'
                   f'游戏一更新通常要等作者发新版才能用。')
        risk_title = f'🚨 刚更新 · {fw_name} 待适配'

    after = framework_entry.get('afterUpdate') if framework_entry else None
    risk_desc = (after or {}).get('zh-CN') or GENERIC_RISK_DESC.get(reason, GENERIC_RISK_DESC['default'])

    fields = {
        'compatibilityStatus': status,
        'radarReason': reason,
        'radarStatusText': status_text(reason, fw_name),
        'latestSteamPatch': news['title'] if news and news.get('title') else None,
        'latestSteamPatchUrl': (news or {}).get('url') or store_news_url(appid),
        'steamBuildId': buildid,
        'steamBuildUpdatedAt': iso_z(build['updated_at']),
        'steamLastChecked': iso_z(now),
        'radarFramework': {'name': fw['name'], 'url': fw['url']} if fw else None,
        'radarSummary': summary,
        'radarRiskTitle': risk_title,
        'radarRiskDesc': risk_desc,
    }

    alert = None
    if status == 'red':
        alert = {
            'zh-CN': f'《{zh_title}》Steam 于 {build_date} 更新，{fw_name} 通常要等作者发新版，先别更新',
            'en': (f'{en_title} was updated on Steam on {build_date}. {fw_name} usually needs a new release '
                   f'after each game update, so hold off on updating.'),
        }
    elif reason == 'recent-update':
        alert = {
            'zh-CN': f'《{zh_title}》Steam 于 {build_date} 更新，Mod/修改器可能要等适配',
            'en': f'{en_title} was updated on Steam on {build_date}. Mods and trainers may need time to catch up.',
        }
    return fields, alert


def inspect_game(game, client, framework_entry, trainer_modified, now, simulate=None):
    """巡检一款。返回结果 dict；fetched=False 时不带 fields（字段保持原值）。"""
    appid = game.get('steamAppId')
    zh_title, en_title = _titles(game)
    result = {
        'id': game.get('id'), 'rank': game.get('rank'), 'title': zh_title, 'title_en': en_title, 'appid': appid,
        'prev_status': game.get('compatibilityStatus'), 'prev_buildid': game.get('steamBuildId'),
        'framework_entry': framework_entry, 'trainer_modified': trainer_modified,
        'fetched': False, 'error': None, 'simulated': False, 'new_red': False,
        'build': None, 'news': None, 'reason': None, 'status': None, 'fields': None, 'alert': None,
        'framework_name': None,
    }

    framework_name = None
    if simulate and simulate.get('game_id') == game.get('id'):
        result['simulated'] = True
        build = {'buildid': str(simulate.get('build_id') or now.strftime('%Y%m%d%H%M')), 'updated_at': now}
        news = {'title': f'【演练】{simulate.get("version") or "模拟更新"}', 'url': store_news_url(appid), 'date': now}
        if simulate.get('risk', 'red') == 'red':
            fw = (framework_entry or {}).get('framework')
            framework_entry = dict(framework_entry or {}, hooksExe=True, framework=fw)
            framework_name = None if fw else SIMULATED_FRAMEWORK_NAME
        else:
            framework_entry = dict(framework_entry or {}, hooksExe=False) if framework_entry else None
    else:
        try:
            build = client.fetch_build(appid)
            news = client.fetch_latest_news(appid)
        except FetchError as exc:
            result['error'] = str(exc)
            return result

    reason = classify(now, build['updated_at'], framework_entry, trainer_modified)
    fields, alert = build_radar_fields(game, reason, build, news, framework_entry, trainer_modified, now,
                                       framework_name=framework_name)
    status = REASON_STATUS[reason]
    fw = (framework_entry or {}).get('framework')
    result.update({
        'fetched': True, 'build': build, 'news': news, 'reason': reason, 'status': status,
        'fields': fields, 'alert': alert, 'framework_name': framework_name or (fw['name'] if fw else None),
        'new_red': is_new_red(status, build['buildid'], result['prev_status'], result['prev_buildid']),
    })
    return result


def select_targets(games, game_id=None, appid=None):
    """默认全部带 steamAppId 的游戏；--game / --appid 只挑一款。"""
    steam_games = [g for g in games if g.get('steamAppId')]
    if game_id:
        return [g for g in steam_games if g.get('id') == game_id]
    if appid:
        return [g for g in steam_games if g.get('steamAppId') == appid]
    return steam_games


def inspect_games(targets, client, frameworks, trainer_times, now, simulate=None, log=print):
    results = []
    total = len(targets)
    for i, game in enumerate(targets, 1):
        res = inspect_game(game, client, frameworks.get(game.get('id')), trainer_times.get(game.get('id')),
                           now, simulate=simulate)
        results.append(res)
        if log:
            if res['fetched']:
                icon = {'red': '🔴', 'yellow': '🟡', 'green': '🟢'}[res['status']]
                extra = f"{res['reason']:<20} build {res['build']['buildid']} @ {fmt_date(res['build']['updated_at'])}"
                if res['new_red']:
                    extra += '  ← 新变红'
                if res['simulated']:
                    extra += '  (演练)'
            else:
                icon, extra = '⚪', f"未取到：{res['error']}"
            log(f"[{i:>3}/{total}] {icon} #{res['rank']:<3} {str(res['title_en'])[:30]:<31} {extra}")
    return results


def results_to_snapshot(results):
    """把这次取到的 Steam 数据存成 --steam-snapshot 能读的格式（演练的那款不存）。"""
    snap = {}
    for r in results:
        if r['simulated']:
            continue
        if not r['fetched']:
            snap[str(r['appid'])] = {'error': r['error']}
            continue
        news = r['news']
        snap[str(r['appid'])] = {
            'buildid': r['build']['buildid'],
            'timeupdated': iso_z(r['build']['updated_at']),
            'news': None if not news else {
                'title': news.get('title') or '', 'url': news.get('url'),
                'date': iso_z(news['date']) if news.get('date') else None,
            },
        }
    return snap


def apply_results(games, results):
    """把取到数据的结果写进 games（原地改）。没取到的一个字段都不动。返回改了几款。"""
    by_id = {g.get('id'): g for g in games}
    updated = 0
    for res in results:
        if not res['fetched']:
            continue
        game = by_id.get(res['id'])
        if game is None:
            continue
        for key, value in res['fields'].items():
            if key == 'latestSteamPatch' and value is None:
                game.pop(key, None)
            else:
                game[key] = value
        if res['alert']:
            game['emergencyAlert'] = res['alert']
        else:
            game.pop('emergencyAlert', None)
        updated += 1
    return updated


# ==============================================================================
# 报告（docs/PATCH_MONITOR_LATEST.md，也是预警单正文）
# ==============================================================================
def _md(text, limit=None):
    s = ' '.join(str(text if text is not None else '').split())
    if limit and len(s) > limit:
        s = s[:limit - 1] + '…'
    return s.replace('|', '\\|')


def _age_days(now, dt):
    return (now - dt).total_seconds() / 86400.0 if dt else None


def _fw_label(res):
    fw = (res.get('fields') or {}).get('radarFramework')
    if fw:
        return f"[{_md(fw['name'], 40)}]({fw['url']})"
    if res.get('framework_name'):
        return _md(res['framework_name'], 40)
    return '—' if res.get('framework_entry') else '（无资料）'


def _hooks_label(entry):
    if not entry:
        return '—'
    return {True: 'true', False: 'false', None: 'null'}.get(entry.get('hooksExe'), '?')


def summarize(results):
    fetched = [r for r in results if r['fetched']]
    return {
        'total': len(results),
        'red': sum(1 for r in fetched if r['status'] == 'red'),
        'yellow': sum(1 for r in fetched if r['status'] == 'yellow'),
        'green': sum(1 for r in fetched if r['status'] == 'green'),
        'missing': sum(1 for r in results if not r['fetched']),
        'new_red': sum(1 for r in results if r['new_red']),
    }


def render_report(results, now, frameworks, trainer_note=None, mode_notes=(), simulate=None):
    counts = summarize(results)
    fetched = [r for r in results if r['fetched']]
    reds = [r for r in fetched if r['status'] == 'red']
    yellows = [r for r in fetched if r['status'] == 'yellow']
    greens = [r for r in fetched if r['status'] == 'green']
    missing = [r for r in results if not r['fetched']]
    new_reds = [r for r in results if r['new_red']]

    lines = [
        '# 📡 补丁雷达巡检报告',
        '',
        f'<!-- radar-new-red: {counts["new_red"]} -->',
        '',
        f'- 巡检时间：`{iso_z(now)}`（UTC）',
        f'- 范围：{counts["total"]} 款带 Steam AppID 的游戏（非 Steam 游戏不巡检）',
        f'- 规则：Steam 公共分支 build 发布时间 ≤ {RECENT_DAYS} 天算「刚更新」；框架资料 `hooksExe` 为 true 才亮红；'
        f'修改器早于当前 build 超过 {TRAINER_TOLERANCE_DAYS} 天亮黄。公告只展示，不参与判定。',
        '- 没取到 Steam 数据的游戏，雷达字段保持上次的值不动。',
    ]
    if simulate:
        lines.append(f'- 🧪 **本次是演练**：`{simulate["game_id"]}` 被模拟成刚更新（风险 `{simulate.get("risk", "red")}`），'
                     f'不是真的 Steam 更新。')
    for note in mode_notes:
        lines.append(f'- {note}')

    lines += [
        '',
        '## 概览',
        '',
        '| 🔴 红 | 🟡 黄 | 🟢 绿 | ⚪ 本次未取到 | 🚨 新变红 |',
        '|:---:|:---:|:---:|:---:|:---:|',
        f'| {counts["red"]} | {counts["yellow"]} | {counts["green"]} | {counts["missing"]} | {counts["new_red"]} |',
        '',
        f'原因码：`recent-update-hooks` {counts["red"]} · '
        f'`recent-update` {sum(1 for r in yellows if r["reason"] == "recent-update")} · '
        f'`trainer-behind` {sum(1 for r in yellows if r["reason"] == "trainer-behind")} · '
        f'`quiet` {counts["green"]}',
        '',
        f'## 🚨 新变红（{len(new_reds)}）',
        '',
    ]
    if not new_reds:
        lines.append('本次没有新变红的游戏。')
    else:
        lines.append('这次是红灯，并且上次不是红灯、或者上次的 build 和这次不一样：')
        lines.append('')
        for r in new_reds:
            prev = r['prev_status'] or '无'
            prev_build = r['prev_buildid'] or '无'
            tag = '（演练）' if r['simulated'] else ''
            lines.append(f"- **#{r['rank']} {_md(r['title'])}**{tag} · AppID `{r['appid']}` · build `{r['build']['buildid']}`"
                         f"（{fmt_date(r['build']['updated_at'])}）· 框架 {_fw_label(r)} · 上次 `{prev}` / build `{prev_build}`")
        lines += ['', '可直接转发的提醒（只写事实）：', '', '```text']
        for r in new_reds:
            fw_name = r['framework_name'] or 'Mod 框架'
            drill = '【演练，不是真的更新】' if r['simulated'] else ''
            lines.append(f"{drill}《{r['title']}》Steam 于 {fmt_date(r['build']['updated_at'])} 更新。{fw_name} 通常要等作者发新版"
                         f"才能用，带 Mod 玩的先别更新：Steam 库里右键游戏 → 属性 → 更新 → 改成「仅在启动时更新」。")
        lines.append('```')

    def table(rows, header, sep, render):
        out = [header, sep]
        out += [render(r) for r in rows]
        return out

    lines += ['', f'## 🔴 红灯（{len(reds)}）', '']
    if reds:
        lines += table(
            reds, '| # | 游戏 | 原因 | Steam build | 发布时间 (UTC) | 框架 | 新变红 |', '|:---:|:---|:---|:---|:---|:---|:---:|',
            lambda r: (f"| {r['rank']} | {_md(r['title'], 40)} | `{r['reason']}` | `{r['build']['buildid']}` | "
                       f"{iso_z(r['build']['updated_at'])} | {_fw_label(r)} | {'是' if r['new_red'] else ''} |"))
    else:
        lines.append('无。')

    lines += ['', f'## 🟡 黄灯（{len(yellows)}）', '']
    if yellows:
        lines += table(
            yellows, '| # | 游戏 | 原因 | Steam build | 发布时间 (UTC) | 修改器更新 | 框架 / hooksExe |',
            '|:---:|:---|:---|:---|:---|:---|:---|',
            lambda r: (f"| {r['rank']} | {_md(r['title'], 40)} | `{r['reason']}` | `{r['build']['buildid']}` | "
                       f"{iso_z(r['build']['updated_at'])} | {fmt_date(r['trainer_modified'])} | "
                       f"{_fw_label(r)} / `{_hooks_label(r['framework_entry'])}` |"))
    else:
        lines.append('无。')

    lines += ['', f'## ⚪ 本次未取到（{len(missing)}，字段保持上次的值）', '']
    if missing:
        lines += table(
            missing, '| # | 游戏 | AppID | 原因 | 上次状态 |', '|:---:|:---|:---:|:---|:---:|',
            lambda r: f"| {r['rank']} | {_md(r['title'], 40)} | `{r['appid']}` | {_md(r['error'], 80)} | {r['prev_status'] or '—'} |")
    else:
        lines.append('无。')

    lines += ['', f'## 🟢 绿灯（{len(greens)}）', '']
    if greens:
        lines.append('、'.join(f"#{r['rank']} {_md(r['title'], 30)}" for r in greens))
    else:
        lines.append('无。')

    # 框架资料体检
    covered = sum(1 for r in results if r['framework_entry'])
    hooks = {'true': 0, 'false': 0, 'null': 0}
    for r in results:
        if r['framework_entry']:
            hooks[_hooks_label(r['framework_entry'])] += 1
    lines += ['', '## 🧩 框架资料', '']
    rel_dir = os.path.relpath(frameworks.directory, BASE_DIR)
    if frameworks.missing_dir:
        lines.append(f'- `{rel_dir}/` 目录不存在：全部游戏按「没有框架资料」处理（最多亮黄，不亮红）。')
    elif not frameworks.files and not frameworks.errors:
        lines.append(f'- `{rel_dir}/` 里还没有 part-*.json：全部游戏按「没有框架资料」处理（最多亮黄，不亮红）。')
    else:
        files = '、'.join(f'`{name}`（{n} 条）' for name, n in frameworks.files) or '无'
        lines.append(f'- 读到的文件：{files}')
    lines.append(f'- 覆盖：{covered} / {len(results)} 款巡检目标有可用条目；hooksExe true {hooks["true"]} · '
                 f'false {hooks["false"]} · null {hooks["null"]}')
    if frameworks.errors:
        lines.append(f'- ❌ 跳过（格式不对，{len(frameworks.errors)} 处）：')
        lines += [f'  - {_md(e, 200)}' for e in frameworks.errors]
    if frameworks.warnings:
        lines.append(f'- ⚠️ 提醒（条目照用，{len(frameworks.warnings)} 处）：')
        lines += [f'  - {_md(w, 200)}' for w in frameworks.warnings]
    uncovered = [r for r in results if not r['framework_entry']]
    if uncovered and len(uncovered) < len(results):
        lines.append('- 没有条目的游戏：' + '、'.join(f"`{r['id']}`" for r in uncovered))
    if trainer_note:
        lines += ['', f'- 修改器：{trainer_note}']

    # 全量明细
    lines += ['', '<details>', f'<summary>全部 {len(results)} 款明细</summary>', '',
              '| # | 游戏 | 状态 | 原因 | Steam build | 发布时间 (UTC) | 修改器更新 | 最新公告 |',
              '|:---:|:---|:---:|:---|:---|:---|:---|:---|']
    for r in sorted(results, key=lambda x: (x['rank'] if _is_int(x['rank']) else 10 ** 6)):
        if r['fetched']:
            news = r['news'] or {}
            title = _md(news.get('title') or '（无公告）', 40)
            link = (r['fields'] or {}).get('latestSteamPatchUrl')
            news_cell = f'[{title}]({link})' if link else title
            icon = {'red': '🔴', 'yellow': '🟡', 'green': '🟢'}[r['status']]
            lines.append(f"| {r['rank']} | {_md(r['title'], 30)} | {icon} | `{r['reason']}` | `{r['build']['buildid']}` | "
                         f"{iso_z(r['build']['updated_at'])} | {fmt_date(r['trainer_modified'])} | {news_cell} |")
        else:
            lines.append(f"| {r['rank']} | {_md(r['title'], 30)} | ⚪ | 未取到 | — | — | {fmt_date(r['trainer_modified'])} | — |")
    lines += ['', '</details>', '', '---',
              '*由 `scripts/steam_patch_monitor.py` 生成 · 规则见 `docs/RADAR_V2_CONTRACT.md` 第 2 节*', '']
    return '\n'.join(lines)


# ==============================================================================
# 命令行
# ==============================================================================
def parse_args(argv=None):
    p = argparse.ArgumentParser(description='补丁雷达 v2：巡检 Steam build、写报告，可选写回 public/data.js')
    p.add_argument('--game', help='只巡检这一款（游戏 id，如 baldurs-gate-3）')
    p.add_argument('--appid', type=int, help='只巡检这个 Steam AppID')
    p.add_argument('--all', action='store_true', help='兼容旧参数；现在默认就是全部带 steamAppId 的游戏')
    p.add_argument('--update-radar', action='store_true', help='把结果写回 public/data.js 的 GAMES_DATA 段')
    p.add_argument('--output-report', default=REPORT_PATH_DEFAULT, help='Markdown 报告输出路径')
    p.add_argument('--offline', action='store_true', help='不联网；配 --steam-snapshot 用假数据，否则全部算「本次未取到」')
    p.add_argument('--steam-snapshot', help='--offline 用的 Steam 数据快照 JSON（格式见 SnapshotClient）')
    p.add_argument('--save-snapshot', help='把这次取到的 Steam 数据存成快照 JSON，之后可 --offline --steam-snapshot 复跑')
    p.add_argument('--simulate-patch', metavar='GAME_ID', help='演练：把这款游戏模拟成「刚更新」，用来走一遍新变红流程')
    p.add_argument('--simulate-version', default='模拟更新', help='演练时公告标题里显示的版本名')
    p.add_argument('--simulate-risk', choices=['red', 'yellow'], default='red',
                   help='演练风险：red = 当作框架挂钩 exe（会产生新变红），yellow = recent-update')
    p.add_argument('--simulate-build-id', help='演练用的 build 号（默认按当前时间生成）')
    p.add_argument('--data-js', default=DATA_JS_PATH, help='游戏库 data.js 路径（默认 public/data.js）')
    p.add_argument('--frameworks-dir', default=FRAMEWORKS_DIR, help='框架资料目录（默认 scripts/radar_frameworks）')
    p.add_argument('--trainers', default=TRAINERS_PATH, help='修改器清单（默认 public/trainers.json）')
    p.add_argument('--now', help='把「现在」固定成这个 ISO 时间（离线复现用）')
    p.add_argument('--timeout', type=float, default=DEFAULT_TIMEOUT, help='单个请求超时秒数')
    p.add_argument('--interval', type=float, default=DEFAULT_REQUEST_INTERVAL,
                   help=f'请求间隔秒数（不小于 {MIN_REQUEST_INTERVAL}）')
    return p.parse_args(argv)


def run_monitor(argv=None, log=print):
    args = parse_args(argv)
    now = utc_now()
    if args.now:
        now = parse_iso_utc(args.now)
        if now is None:
            log(f'❌ --now 不是合法的 ISO 时间：{args.now}')
            return 2

    data_js = os.path.abspath(args.data_js)
    use_master = data_js == DATA_JS_PATH and os.path.exists(GAMES_JSON_PATH)
    games = load_games(data_js, use_master)
    targets = select_targets(games, game_id=args.game, appid=args.appid)
    if (args.game or args.appid) and not targets:
        log(f'❌ 找不到要巡检的游戏（--game {args.game} / --appid {args.appid}）；非 Steam 游戏不巡检。')
        return 1

    simulate = None
    if args.simulate_patch:
        if not any(g.get('id') == args.simulate_patch for g in targets):
            log(f'❌ 演练的游戏 {args.simulate_patch} 不在本次巡检范围里（不存在、没有 steamAppId，或被 --game/--appid 过滤掉）。')
            return 1
        simulate = {'game_id': args.simulate_patch, 'version': args.simulate_version,
                    'risk': args.simulate_risk, 'build_id': args.simulate_build_id}

    frameworks = load_frameworks(os.path.abspath(args.frameworks_dir), games)
    trainer_times, trainer_note = load_trainer_times(os.path.abspath(args.trainers))

    mode_notes = []
    if args.offline:
        snapshot = {}
        if args.steam_snapshot:
            with open(args.steam_snapshot, 'r', encoding='utf-8') as f:
                snapshot = json.load(f)
            mode_notes.append(f'离线模式：Steam 数据来自快照 `{os.path.basename(args.steam_snapshot)}`，不是实时数据。')
        else:
            mode_notes.append('离线模式：没有 Steam 数据，全部算「本次未取到」。')
        client = SnapshotClient(snapshot, now=now)
    else:
        client = SteamClient(timeout=args.timeout, interval=args.interval)

    log('=' * 80)
    log('📡 补丁雷达 v2 巡检')
    log(f'⏰ {iso_z(now)}  ·  {"离线" if args.offline else "联网"}  ·  目标 {len(targets)} 款')
    log(f'🧩 框架资料：{len(frameworks.entries)} 条可用，{len(frameworks.errors)} 处跳过，{len(frameworks.warnings)} 处提醒')
    if simulate:
        log(f'🧪 演练：{simulate["game_id"]}（风险 {simulate["risk"]}）')
    log('-' * 80)

    results = inspect_games(targets, client, frameworks, trainer_times, now, simulate=simulate, log=log)
    counts = summarize(results)

    report = render_report(results, now, frameworks, trainer_note=trainer_note, mode_notes=mode_notes, simulate=simulate)
    report_path = os.path.abspath(args.output_report)
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    if args.save_snapshot:
        with open(args.save_snapshot, 'w', encoding='utf-8') as f:
            json.dump(results_to_snapshot(results), f, ensure_ascii=False, indent=2)
        log(f'💾 Steam 数据快照：{os.path.abspath(args.save_snapshot)}')

    log('-' * 80)
    log(f"🔴 {counts['red']}  🟡 {counts['yellow']}  🟢 {counts['green']}  ⚪ 未取到 {counts['missing']}  "
        f"🚨 新变红 {counts['new_red']}  （请求 {client.request_count} 次）")
    log(f'📝 报告：{report_path}')

    if args.update_radar:
        updated = apply_results(games, results)
        save_games(games, data_js, use_master)
        log(f'💾 已写回 {updated} 款到 {data_js}（未取到的 {counts["missing"]} 款不动）')
        if simulate:
            log('⚠️ 演练数据已写进 data.js，别提交。')
    log('=' * 80)
    return 0


if __name__ == '__main__':
    sys.exit(run_monitor())
