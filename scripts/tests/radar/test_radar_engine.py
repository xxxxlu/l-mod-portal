# -*- coding: utf-8 -*-
"""补丁雷达 v2 巡检脚本的测试（标准库 unittest）。

跑法（仓库根目录）：
    python3 -m unittest discover -s scripts/tests/radar -v

只用 fixtures/ 下的假数据和临时目录，不联网，不改 public/data.js、docs/PATCH_MONITOR_LATEST.md。
"""

import copy
import datetime
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
FIXTURES = os.path.join(HERE, 'fixtures')
sys.path.insert(0, os.path.join(REPO, 'scripts'))

import steam_patch_monitor as spm  # noqa: E402

UTC = datetime.timezone.utc
NOW = datetime.datetime(2026, 11, 19, 0, 0, 0, tzinfo=UTC)
DAY = datetime.timedelta(days=1)


def days_ago(n):
    return NOW - datetime.timedelta(days=n)


def make_game(gid='game-a', rank=1, appid=100, **extra):
    game = {'id': gid, 'rank': rank, 'title': gid.title(), 'titles': {'en': gid.title(), 'zh-CN': f'游戏{gid}'},
            'steamAppId': appid, 'verifiedPatch': 'v1.0'}
    game.update(extra)
    return game


def fw_entry(gid='game-a', rank=1, appid=100, hooks=True, name='Script Extender', after=None):
    return {
        'id': gid, 'rank': rank, 'steamAppId': appid,
        'framework': {'name': name, 'url': 'https://example.com/fw'} if name else None,
        'hooksExe': hooks, 'modSupport': 'community', 'afterUpdate': after,
        'sources': ['https://example.com/fw'], 'checkedAt': '2026-11-19',
    }


class FakeClient:
    """按 appid 返回假 build / 公告；值是 Exception 就抛 FetchError。"""

    def __init__(self, builds=None, news=None):
        self.builds = builds or {}
        self.news = news or {}
        self.request_count = 0

    def fetch_build(self, appid):
        self.request_count += 1
        value = self.builds.get(appid)
        if value is None or isinstance(value, Exception):
            raise spm.FetchError(f'fake build failure {appid}')
        return value

    def fetch_latest_news(self, appid):
        self.request_count += 1
        value = self.news.get(appid)
        if isinstance(value, Exception):
            raise spm.FetchError(f'fake news failure {appid}')
        return value


def build(buildid='200', when=None):
    return {'buildid': buildid, 'updated_at': when or days_ago(3)}


# ==============================================================================
# 2.2 节：四种状态
# ==============================================================================
class ClassifyTest(unittest.TestCase):
    def test_recent_update_with_hooks_is_red(self):
        reason = spm.classify(NOW, days_ago(3), fw_entry(hooks=True))
        self.assertEqual(reason, 'recent-update-hooks')
        self.assertEqual(spm.REASON_STATUS[reason], 'red')

    def test_recent_update_without_framework_data_is_yellow(self):
        self.assertEqual(spm.classify(NOW, days_ago(3), None), 'recent-update')

    def test_recent_update_hooks_false_or_null_is_yellow(self):
        self.assertEqual(spm.classify(NOW, days_ago(3), fw_entry(hooks=False)), 'recent-update')
        self.assertEqual(spm.classify(NOW, days_ago(3), fw_entry(hooks=None)), 'recent-update')
        self.assertEqual(spm.REASON_STATUS['recent-update'], 'yellow')

    def test_recent_window_is_inclusive_14_days(self):
        self.assertEqual(spm.classify(NOW, days_ago(14), None), 'recent-update')
        just_over = NOW - datetime.timedelta(days=14, seconds=1)
        self.assertEqual(spm.classify(NOW, just_over, None), 'quiet')

    def test_trainer_behind(self):
        build_time = days_ago(30)
        reason = spm.classify(NOW, build_time, None, trainer_modified=build_time - 2 * DAY)
        self.assertEqual(reason, 'trainer-behind')
        self.assertEqual(spm.REASON_STATUS[reason], 'yellow')

    def test_trainer_within_one_day_tolerance_is_quiet(self):
        build_time = days_ago(30)
        self.assertEqual(spm.classify(NOW, build_time, None, trainer_modified=build_time - DAY), 'quiet')
        self.assertEqual(spm.classify(NOW, build_time, None, trainer_modified=build_time + DAY), 'quiet')
        over = build_time - DAY - datetime.timedelta(seconds=1)
        self.assertEqual(spm.classify(NOW, build_time, None, trainer_modified=over), 'trainer-behind')

    def test_no_trainer_and_old_build_is_green(self):
        reason = spm.classify(NOW, days_ago(200), fw_entry(hooks=True))
        self.assertEqual(reason, 'quiet')
        self.assertEqual(spm.REASON_STATUS[reason], 'green')

    def test_recent_update_takes_priority_over_trainer_behind(self):
        build_time = days_ago(2)
        reason = spm.classify(NOW, build_time, fw_entry(hooks=True), trainer_modified=days_ago(400))
        self.assertEqual(reason, 'recent-update-hooks')


class StatusTextTest(unittest.TestCase):
    def test_four_fixed_sentences(self):
        self.assertEqual(spm.status_text('quiet'), '🟢 近 14 天无更新')
        self.assertEqual(spm.status_text('recent-update'), '🟡 刚更新 · Mod/修改器可能要等适配')
        self.assertEqual(spm.status_text('trainer-behind'), '🟡 修改器早于当前游戏版本')
        self.assertEqual(spm.status_text('recent-update-hooks', 'SKSE64'), '🔴 刚更新 · SKSE64 待适配，先别更新')

    def test_no_banned_phrases_in_any_generated_text(self):
        game = make_game()
        cases = [
            ('quiet', fw_entry(hooks=True), None),
            ('recent-update', None, None),
            ('trainer-behind', None, days_ago(400)),
            ('recent-update-hooks', fw_entry(hooks=True), None),
        ]
        for reason, entry, trainer in cases:
            fields, alert = spm.build_radar_fields(game, reason, build(), {'title': 't', 'url': None},
                                                   entry, trainer, NOW)
            blob = json.dumps([fields, alert], ensure_ascii=False)
            for phrase in spm.BANNED_PHRASES:
                self.assertNotIn(phrase, blob, f'{reason} 里出现了「{phrase}」')
        for text in list(spm.STATUS_TEXT.values()) + list(spm.GENERIC_RISK_DESC.values()):
            for phrase in spm.BANNED_PHRASES:
                self.assertNotIn(phrase, text)


# ==============================================================================
# 2.4 节：新变红
# ==============================================================================
class NewRedTest(unittest.TestCase):
    def test_rules(self):
        self.assertTrue(spm.is_new_red('red', '200', 'green', '100'))
        self.assertTrue(spm.is_new_red('red', '200', None, None))
        self.assertTrue(spm.is_new_red('red', '200', 'yellow', '200'))
        self.assertTrue(spm.is_new_red('red', '200', 'red', '100'), '上次红、build 变了 → 算新变红')
        self.assertFalse(spm.is_new_red('red', '200', 'red', '200'), '已经红着、build 没变 → 不再报')
        self.assertFalse(spm.is_new_red('red', '200', 'red', 200), 'build 号类型不同也按字符串比')
        self.assertFalse(spm.is_new_red('yellow', '200', 'green', '100'))
        self.assertFalse(spm.is_new_red('green', '200', 'red', '100'))

    def test_inspect_game_marks_new_red(self):
        client = FakeClient({100: build('201')}, {100: None})
        res = spm.inspect_game(make_game(compatibilityStatus='red', steamBuildId='200'), client,
                               fw_entry(hooks=True), None, NOW)
        self.assertTrue(res['new_red'])
        res = spm.inspect_game(make_game(compatibilityStatus='red', steamBuildId='201'), client,
                               fw_entry(hooks=True), None, NOW)
        self.assertEqual(res['status'], 'red')
        self.assertFalse(res['new_red'])


# ==============================================================================
# 2.2 / 2.3 节：没取到保持原值、字段写回、emergencyAlert 清理
# ==============================================================================
class ApplyResultsTest(unittest.TestCase):
    def run_one(self, game, client, entry=None, trainer=None):
        games = [game]
        res = spm.inspect_game(game, client, entry, trainer, NOW)
        spm.apply_results(games, [res])
        return games[0], res

    def test_build_fetch_failure_keeps_every_field(self):
        game = make_game(compatibilityStatus='red', radarStatusText='旧', steamBuildId='1', steamLastChecked='x',
                         emergencyAlert={'zh-CN': 'a', 'en': 'b'}, radarSummary='旧')
        before = copy.deepcopy(game)
        after, res = self.run_one(game, FakeClient({100: RuntimeError()}))
        self.assertFalse(res['fetched'])
        self.assertIn('fake build failure', res['error'])
        self.assertEqual(after, before)

    def test_news_fetch_failure_also_keeps_every_field(self):
        game = make_game(compatibilityStatus='green', steamBuildId='1')
        before = copy.deepcopy(game)
        after, res = self.run_one(game, FakeClient({100: build()}, {100: RuntimeError()}))
        self.assertFalse(res['fetched'])
        self.assertEqual(after, before)

    def test_red_writes_all_fields_and_alert(self):
        entry = fw_entry(hooks=True, name='SKSE64', after={'zh-CN': '等 SKSE64 更新再玩。', 'en': 'Wait for SKSE64.'})
        news = {'title': 'Patch 1.2', 'url': 'https://store.steampowered.com/news/app/100/view/9', 'date': days_ago(3)}
        game = make_game(verifiedPatch='保持不动')
        after, res = self.run_one(game, FakeClient({100: build('555', days_ago(3))}, {100: news}), entry)
        self.assertEqual(after['compatibilityStatus'], 'red')
        self.assertEqual(after['radarReason'], 'recent-update-hooks')
        self.assertEqual(after['radarStatusText'], '🔴 刚更新 · SKSE64 待适配，先别更新')
        self.assertEqual(after['steamBuildId'], '555')
        self.assertEqual(after['steamBuildUpdatedAt'], '2026-11-16T00:00:00Z')
        self.assertEqual(after['steamLastChecked'], '2026-11-19T00:00:00Z')
        self.assertEqual(after['radarFramework'], {'name': 'SKSE64', 'url': 'https://example.com/fw'})
        self.assertEqual(after['latestSteamPatch'], 'Patch 1.2')
        self.assertEqual(after['latestSteamPatchUrl'], news['url'])
        self.assertEqual(after['radarRiskDesc'], '等 SKSE64 更新再玩。')
        self.assertEqual(set(after['emergencyAlert']), {'zh-CN', 'en'})
        self.assertIn('SKSE64', after['emergencyAlert']['zh-CN'])
        self.assertEqual(after['verifiedPatch'], '保持不动')
        for key in ('radarSummary', 'radarRiskTitle'):
            self.assertTrue(after[key])

    def test_recent_update_writes_alert(self):
        after, _ = self.run_one(make_game(), FakeClient({100: build()}, {100: None}))
        self.assertEqual(after['radarReason'], 'recent-update')
        self.assertIn('emergencyAlert', after)
        self.assertIsNone(after['radarFramework'])

    def test_alert_removed_for_quiet_and_trainer_behind(self):
        old_alert = {'zh-CN': '旧预警', 'en': 'old'}
        after, _ = self.run_one(make_game(emergencyAlert=old_alert), FakeClient({100: build(when=days_ago(60))}))
        self.assertEqual(after['radarReason'], 'quiet')
        self.assertNotIn('emergencyAlert', after)

        after, _ = self.run_one(make_game(emergencyAlert=old_alert), FakeClient({100: build(when=days_ago(60))}),
                                trainer=days_ago(300))
        self.assertEqual(after['radarReason'], 'trainer-behind')
        self.assertNotIn('emergencyAlert', after)

    def test_no_announcement_falls_back_to_store_news_page(self):
        game = make_game(latestSteamPatch='很旧的公告')
        after, _ = self.run_one(game, FakeClient({100: build(when=days_ago(60))}, {100: None}))
        self.assertNotIn('latestSteamPatch', after)
        self.assertEqual(after['latestSteamPatchUrl'], 'https://store.steampowered.com/news/app/100')

    def test_generic_risk_desc_when_no_after_update(self):
        after, _ = self.run_one(make_game(), FakeClient({100: build()}), fw_entry(hooks=False))
        self.assertEqual(after['radarRiskDesc'], spm.GENERIC_RISK_DESC['default'])

    def test_non_steam_games_are_not_targets(self):
        games = [make_game('a', appid=100), make_game('b', appid=0), make_game('c', appid=None)]
        self.assertEqual([g['id'] for g in spm.select_targets(games)], ['a'])
        self.assertEqual(spm.select_targets(games, game_id='b'), [])
        self.assertEqual([g['id'] for g in spm.select_targets(games, appid=100)], ['a'])

    def test_simulation_produces_new_red_even_if_already_red(self):
        game = make_game(compatibilityStatus='red', steamBuildId='900')
        sim = {'game_id': 'game-a', 'version': 'Update 9', 'risk': 'red', 'build_id': None}
        res = spm.inspect_game(game, FakeClient(), None, None, NOW, simulate=sim)
        self.assertTrue(res['simulated'])
        self.assertEqual(res['status'], 'red')
        self.assertTrue(res['new_red'])
        self.assertIn(spm.SIMULATED_FRAMEWORK_NAME, res['fields']['radarStatusText'])

        sim['risk'] = 'yellow'
        res = spm.inspect_game(make_game(), FakeClient(), fw_entry(hooks=True), None, NOW, simulate=sim)
        self.assertEqual(res['reason'], 'recent-update')
        self.assertFalse(res['new_red'])


# ==============================================================================
# 框架资料加载器
# ==============================================================================
class FrameworkLoaderTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.games = [make_game('game-a', 1, 100), make_game('game-b', 2, 200), make_game('game-c', 3, 300)]

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def write(self, name, payload):
        with open(os.path.join(self.tmp, name), 'w', encoding='utf-8') as f:
            f.write(payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False))

    def test_missing_directory_is_fine(self):
        data = spm.load_frameworks(os.path.join(self.tmp, 'nope'), self.games)
        self.assertTrue(data.missing_dir)
        self.assertEqual(data.entries, {})
        self.assertEqual(data.errors, [])

    def test_empty_directory(self):
        data = spm.load_frameworks(self.tmp, self.games)
        self.assertFalse(data.missing_dir)
        self.assertEqual(data.files, [])

    def test_only_some_part_files_present(self):
        self.write('part-2.json', [fw_entry('game-b', 2, 200)])
        data = spm.load_frameworks(self.tmp, self.games)
        self.assertEqual(list(data.entries), ['game-b'])
        self.assertIsNone(data.get('game-a'))
        self.assertEqual(data.errors, [])

    def test_broken_file_is_skipped_others_load(self):
        self.write('part-1.json', '[{"id": "game-a",')
        self.write('part-2.json', {'not': 'a list'})
        self.write('part-3.json', [fw_entry('game-c', 3, 300)])
        data = spm.load_frameworks(self.tmp, self.games)
        self.assertEqual(list(data.entries), ['game-c'])
        self.assertEqual(len(data.errors), 2)
        self.assertTrue(data.errors[0].startswith('part-1.json'))
        self.assertIn('顶层必须是数组', data.errors[1])

    def test_invalid_entries_are_skipped_and_listed(self):
        bad_hooks = fw_entry('game-a', 1, 100)
        bad_hooks['hooksExe'] = 'yes'
        missing = fw_entry('game-b', 2, 200)
        del missing['sources']
        hooks_without_fw = fw_entry('game-c', 3, 300, hooks=True, name=None)
        self.write('part-1.json', [bad_hooks, missing, hooks_without_fw, 'not-an-object'])
        data = spm.load_frameworks(self.tmp, self.games)
        self.assertEqual(data.entries, {})
        self.assertEqual(len(data.errors), 4)
        joined = '\n'.join(data.errors)
        self.assertIn('hooksExe 只能是', joined)
        self.assertIn('缺字段 sources', joined)
        self.assertIn('framework 为 null', joined)
        self.assertIn('不是 JSON 对象', joined)

    def test_field_format_rules(self):
        cases = {
            'framework.url': dict(framework={'name': 'X', 'url': 'not-a-url'}),
            'modSupport': dict(modSupport='maybe'),
            'sources 为空': dict(sources=[]),
            'sources 必须是': dict(sources=['ftp://x']),
            'afterUpdate.en': dict(afterUpdate={'zh-CN': '好'}),
            'rank 必须是整数': dict(rank='1'),
            'steamAppId': dict(steamAppId=-5),
        }
        for expect, patch in cases.items():
            entry = fw_entry()
            entry.update(patch)
            errors, _ = spm.validate_framework_entry(entry)
            self.assertTrue(any(expect in e for e in errors), f'{expect}: {errors}')

    def test_all_null_entry_with_no_sources_is_valid(self):
        entry = fw_entry(hooks=None, name=None)
        entry.update(modSupport=None, afterUpdate=None, sources=[])
        self.assertEqual(spm.validate_framework_entry(entry), ([], []))

    def test_warnings_keep_the_entry(self):
        long_after = {'zh-CN': '长' * 61, 'en': 'x' * 121}
        entry = fw_entry('game-a', 7, 100, after=long_after)
        entry['checkedAt'] = '19/11/2026'
        self.write('part-1.json', [entry])
        data = spm.load_frameworks(self.tmp, self.games)
        self.assertIn('game-a', data.entries)
        joined = '\n'.join(data.warnings)
        self.assertIn('afterUpdate.zh-CN 超长', joined)
        self.assertIn('afterUpdate.en 超长', joined)
        self.assertIn('checkedAt', joined)
        self.assertIn('rank 与 GAMES_DATA 不一致', joined)

    def test_unknown_id_and_duplicates(self):
        self.write('part-1.json', [fw_entry('game-a', 1, 100), fw_entry('ghost', 9, 900)])
        self.write('part-2.json', [fw_entry('game-a', 1, 100, name='Other')])
        data = spm.load_frameworks(self.tmp, self.games)
        self.assertEqual(data.entries['game-a']['framework']['name'], 'Script Extender')
        joined = '\n'.join(data.errors)
        self.assertIn('ghost', joined)
        self.assertIn('id 重复', joined)

    def test_part_files_sorted_numerically(self):
        self.write('part-10.json', [fw_entry('game-a', 1, 100, name='Later')])
        self.write('part-2.json', [fw_entry('game-a', 1, 100, name='Earlier')])
        data = spm.load_frameworks(self.tmp, self.games)
        self.assertEqual([n for n, _ in data.files], ['part-2.json', 'part-10.json'])
        self.assertEqual(data.entries['game-a']['framework']['name'], 'Earlier')


# ==============================================================================
# Steam 接口解析与请求节流
# ==============================================================================
class ParserTest(unittest.TestCase):
    def test_steamcmd_payload(self):
        payload = {'status': 'success', 'data': {'42': {'depots': {'branches': {'public': {
            'buildid': '25605617', 'timebuildupdated': '1', 'timeupdated': '1790693718'}}}}}}
        got = spm.parse_steamcmd_payload(payload, 42)
        self.assertEqual(got['buildid'], '25605617')
        self.assertEqual(spm.iso_z(got['updated_at']), '2026-09-29T14:55:18Z')

    def test_steamcmd_payload_errors(self):
        bad = [
            {'status': 'failed'},
            {'status': 'success', 'data': {}},
            {'status': 'success', 'data': {'42': {'depots': {'branches': {'public': {'buildid': 'abc', 'timeupdated': '1'}}}}}},
            {'status': 'success', 'data': {'42': {'depots': {'branches': {'public': {'buildid': '1', 'timeupdated': 'x'}}}}}},
            [],
        ]
        for payload in bad:
            with self.assertRaises(spm.FetchError, msg=payload):
                spm.parse_steamcmd_payload(payload, 42)

    def test_news_payload(self):
        payload = {'appnews': {'newsitems': [{'title': ' Hotfix  #36 ', 'url': 'https://x/1', 'date': 1774536005}]}}
        got = spm.parse_news_payload(payload)
        self.assertEqual(got['title'], 'Hotfix #36')
        self.assertEqual(got['url'], 'https://x/1')
        self.assertIsNone(spm.parse_news_payload({'appnews': {'newsitems': []}}))
        with self.assertRaises(spm.FetchError):
            spm.parse_news_payload({'error': 'nope'})


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class SteamClientTest(unittest.TestCase):
    def make_client(self, responses, interval=0.5):
        self.sleeps = []
        self.clock_value = [0.0]
        self.urls = []

        def fake_sleep(sec):
            self.sleeps.append(sec)
            self.clock_value[0] += sec

        def fake_open(req, timeout):
            self.urls.append(req.full_url)
            item = responses.pop(0)
            if isinstance(item, Exception):
                raise item
            return FakeResponse(json.dumps(item).encode('utf-8'))

        return spm.SteamClient(timeout=1, interval=interval, sleep=fake_sleep,
                               clock=lambda: self.clock_value[0], opener=fake_open)

    def test_requests_are_spaced_at_least_half_a_second(self):
        news = {'appnews': {'newsitems': []}}
        client = self.make_client([news, news, news], interval=0.1)
        self.assertEqual(client.interval, spm.MIN_REQUEST_INTERVAL)
        for _ in range(3):
            client.fetch_latest_news(1)
        self.assertEqual(len(self.sleeps), 2)
        self.assertTrue(all(s >= 0.5 for s in self.sleeps))

    def test_retry_once_on_5xx_then_succeed(self):
        err = urllib.error.HTTPError('u', 503, 'busy', {}, None)
        client = self.make_client([err, {'appnews': {'newsitems': []}}])
        self.assertIsNone(client.fetch_latest_news(1))
        self.assertEqual(client.request_count, 2)

    def test_no_retry_on_404(self):
        err = urllib.error.HTTPError('u', 404, 'nf', {}, None)
        client = self.make_client([err])
        with self.assertRaises(spm.FetchError) as ctx:
            client.fetch_build(1)
        self.assertIn('HTTP 404', str(ctx.exception))
        self.assertEqual(client.request_count, 1)

    def test_timeout_twice_raises(self):
        client = self.make_client([TimeoutError('timed out'), urllib.error.URLError('timed out')])
        with self.assertRaises(spm.FetchError) as ctx:
            client.fetch_build(1)
        self.assertIn('steamcmd', str(ctx.exception))

    def test_news_url_only_reads_official_announcements(self):
        client = self.make_client([{'appnews': {'newsitems': []}}])
        client.fetch_latest_news(1086940)
        self.assertIn('feeds=steam_community_announcements', self.urls[0])
        self.assertIn('appid=1086940', self.urls[0])


class TrainerTimesTest(unittest.TestCase):
    def test_naive_times_read_as_utc(self):
        times, note = spm.load_trainer_times(os.path.join(FIXTURES, 'trainers.json'))
        self.assertIsNone(note)
        self.assertEqual(spm.iso_z(times['baldurs-gate-3']), '2025-04-16T05:20:55Z')

    def test_missing_file(self):
        times, note = spm.load_trainer_times(os.path.join(FIXTURES, 'nope.json'))
        self.assertEqual(times, {})
        self.assertIn('不判 trainer-behind', note)

    def test_parse_iso_utc(self):
        self.assertEqual(spm.iso_z(spm.parse_iso_utc('2026-11-19T08:00:00+08:00')), '2026-11-19T00:00:00Z')
        self.assertEqual(spm.iso_z(spm.parse_iso_utc('2026-11-19T00:00:00Z')), '2026-11-19T00:00:00Z')
        self.assertIsNone(spm.parse_iso_utc('not a date'))
        self.assertIsNone(spm.parse_iso_utc(None))


# ==============================================================================
# 离线端到端：假数据跑一遍完整命令
# ==============================================================================
class OfflineEndToEndTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.data_js = os.path.join(self.tmp, 'data.js')
        shutil.copy(os.path.join(FIXTURES, 'data_min.js'), self.data_js)
        self.report = os.path.join(self.tmp, 'report.md')
        self.logs = []

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def run_monitor(self, *extra, frameworks=os.path.join(FIXTURES, 'frameworks')):
        argv = ['--offline', '--steam-snapshot', os.path.join(FIXTURES, 'steam_snapshot.json'),
                '--frameworks-dir', frameworks, '--trainers', os.path.join(FIXTURES, 'trainers.json'),
                '--data-js', self.data_js, '--output-report', self.report, '--now', '2026-11-19T00:00:00Z'] + list(extra)
        code = spm.run_monitor(argv, log=self.logs.append)
        with open(self.report, encoding='utf-8') as f:
            report = f.read()
        return code, report

    def games(self):
        return {g['id']: g for g in spm.load_games(self.data_js, use_master=False)}

    def raw(self):
        with open(self.data_js, encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def new_red_count(report):
        m = re.search(r'<!-- radar-new-red: (\d+) -->', report)
        return int(m.group(1)) if m else None

    def test_full_offline_run_with_update(self):
        before_games = self.games()
        before_raw = self.raw()
        code, report = self.run_monitor('--update-radar')
        self.assertEqual(code, 0)
        after = self.games()

        expect = {
            'cyberpunk-2077': ('red', 'recent-update-hooks'),
            'witcher-3': ('green', 'quiet'),
            'baldurs-gate-3': ('yellow', 'trainer-behind'),
            'skyrim-se': ('red', 'recent-update-hooks'),
            'palworld': ('yellow', 'recent-update'),
        }
        for gid, (status, reason) in expect.items():
            self.assertEqual((after[gid]['compatibilityStatus'], after[gid]['radarReason']), (status, reason), gid)

        # 没取到 / 非 Steam：一个字段都不动
        self.assertEqual(after['elden-ring'], before_games['elden-ring'])
        self.assertEqual(after['alan-wake-2'], before_games['alan-wake-2'])

        # emergencyAlert：红和 recent-update 写，其余删
        self.assertIn('emergencyAlert', after['cyberpunk-2077'])
        self.assertIn('emergencyAlert', after['palworld'])
        self.assertNotIn('emergencyAlert', after['witcher-3'])
        self.assertNotIn('emergencyAlert', after['baldurs-gate-3'])

        # 新变红：赛博朋克（绿→红）算；天际（红、build 没变）不算
        self.assertEqual(self.new_red_count(report), 1)
        self.assertIn('赛博朋克 2077', report.split('## 🔴')[0])

        # GAMES_DATA 之外一个字节都不动
        a, b = spm._games_data_span(before_raw)
        a2, b2 = spm._games_data_span(self.raw())
        self.assertEqual(before_raw[:a], self.raw()[:a2])
        self.assertEqual(before_raw[b:], self.raw()[b2:])

        # 报告：未取到、框架资料问题都列出来
        self.assertIn('模拟 steamcmd 超时', report)
        self.assertIn('palworld', report)
        self.assertIn('not-a-game', report)
        self.assertIn('rank 与 GAMES_DATA 不一致', report)
        for phrase in spm.BANNED_PHRASES:
            self.assertNotIn(phrase, report)

    def test_without_update_flag_data_js_is_untouched(self):
        before = self.raw()
        code, report = self.run_monitor()
        self.assertEqual(code, 0)
        self.assertEqual(self.raw(), before)
        self.assertEqual(self.new_red_count(report), 1)

    def test_second_run_reports_no_new_red(self):
        self.run_monitor('--update-radar')
        _, report = self.run_monitor('--update-radar')
        self.assertEqual(self.new_red_count(report), 0)

    def test_missing_framework_dir_still_runs_and_never_red(self):
        code, report = self.run_monitor('--update-radar', frameworks=os.path.join(self.tmp, 'radar_frameworks'))
        self.assertEqual(code, 0)
        after = self.games()
        self.assertEqual(after['cyberpunk-2077']['compatibilityStatus'], 'yellow')
        self.assertEqual(after['skyrim-se']['compatibilityStatus'], 'yellow')
        self.assertEqual(self.new_red_count(report), 0)
        self.assertIn('目录不存在', report)

    def test_simulation_creates_a_new_red(self):
        code, report = self.run_monitor('--simulate-patch', 'palworld', '--simulate-version', 'Update 2.5')
        self.assertEqual(code, 0)
        self.assertEqual(self.new_red_count(report), 2)
        self.assertIn('本次是演练', report)
        self.assertIn('【演练】Update 2.5', report)

    def test_simulation_of_unknown_or_non_steam_game_fails(self):
        self.assertEqual(spm.run_monitor(['--offline', '--data-js', self.data_js, '--output-report', self.report,
                                          '--simulate-patch', 'alan-wake-2'], log=self.logs.append), 1)
        self.assertEqual(spm.run_monitor(['--offline', '--data-js', self.data_js, '--output-report', self.report,
                                          '--game', 'nope'], log=self.logs.append), 1)

    def test_single_game_mode(self):
        code, report = self.run_monitor('--game', 'baldurs-gate-3')
        self.assertEqual(code, 0)
        self.assertIn('范围：1 款', report)

    def test_offline_without_snapshot_marks_everything_missing(self):
        before = self.raw()
        code = spm.run_monitor(['--offline', '--data-js', self.data_js, '--output-report', self.report,
                                '--frameworks-dir', os.path.join(FIXTURES, 'frameworks'), '--update-radar'],
                               log=self.logs.append)
        self.assertEqual(code, 0)
        games_before = {g['id']: g for g in json.loads(before[slice(*spm._games_data_span(before))])}
        self.assertEqual(self.games(), games_before)

    def test_snapshot_round_trip(self):
        snap_path = os.path.join(self.tmp, 'snap.json')
        self.run_monitor('--save-snapshot', snap_path)
        with open(snap_path, encoding='utf-8') as f:
            snap = json.load(f)
        self.assertEqual(snap['1086940']['buildid'], '25605617')
        self.assertIn('error', snap['1245620'])


class RealDataTest(unittest.TestCase):
    """只读真实 public/data.js，确认默认巡检范围 = 全部带 steamAppId 的游戏。"""

    def test_default_targets_cover_every_steam_game(self):
        games = spm.load_games(spm.DATA_JS_PATH, use_master=False)
        targets = spm.select_targets(games)
        self.assertEqual(len(targets), sum(1 for g in games if g.get('steamAppId')))
        self.assertNotIn('alan-wake-2', [g['id'] for g in targets])
        self.assertGreaterEqual(len(targets), 99)


# ==============================================================================
# 工作流 check_risk：只认 radar-new-red 那一行
# ==============================================================================
def extract_step_script(workflow_text, step_id):
    lines = workflow_text.splitlines()
    start = next(i for i, line in enumerate(lines) if line.strip() == f'id: {step_id}')
    run_idx = next(i for i in range(start, len(lines)) if lines[i].strip().startswith('run: |'))
    indent = len(lines[run_idx + 1]) - len(lines[run_idx + 1].lstrip())
    body = []
    for line in lines[run_idx + 1:]:
        if line.strip() and len(line) - len(line.lstrip()) < indent:
            break
        body.append(line[indent:])
    return '\n'.join(body) + '\n'


@unittest.skipUnless(shutil.which('bash'), 'needs bash')
class WorkflowCheckRiskTest(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(REPO, '.github/workflows/patch_radar_cron.yml'), encoding='utf-8') as f:
            self.script = extract_step_script(f.read(), 'check_risk')
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def run_check(self, report_text):
        report = os.path.join(self.tmp, 'report.md')
        out = os.path.join(self.tmp, 'out.txt')
        with open(report, 'w', encoding='utf-8') as f:
            f.write(report_text)
        open(out, 'w').close()
        env = dict(os.environ, RADAR_REPORT=report, GITHUB_OUTPUT=out)
        subprocess.run(['bash', '-e', '-c', self.script], env=env, check=True, capture_output=True)
        with open(out, encoding='utf-8') as f:
            return dict(line.split('=', 1) for line in f.read().split())

    def test_new_red_opens_issue(self):
        got = self.run_check('# r\n\n<!-- radar-new-red: 3 -->\n')
        self.assertEqual(got['high_risk_detected'], 'true')
        self.assertEqual(got['new_red'], '3')

    def test_zero_new_red_does_not_open_issue_even_with_red_words(self):
        got = self.run_check('# r\n\n<!-- radar-new-red: 0 -->\n🔴 坏档预警·暂缓更新\n🔴【坏档高危·暂停更新】\n')
        self.assertEqual(got['high_risk_detected'], 'false')

    def test_missing_marker_counts_as_zero(self):
        got = self.run_check('# old report without marker\n')
        self.assertEqual(got['high_risk_detected'], 'false')
        self.assertEqual(got['new_red'], '0')


if __name__ == '__main__':
    unittest.main()
