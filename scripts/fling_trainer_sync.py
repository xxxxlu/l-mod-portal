#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/fling_trainer_sync.py
风灵月影 (FLiNG) 修改器清单同步 —— 网站和客户端共用的唯一修改器数据源。

数据来源与边界：
  - 只读 flingtrainer.com 公开的 WordPress 接口 /wp-json/wp/v2/posts（robots.txt 未禁止）。
  - 不访问 /downloads/（robots.txt 禁止），不转存任何修改器文件，下载一律跳官方页面。
  - 带反作弊的游戏只打标记，不收录任何绕过反作弊的步骤。

产出：
  public/trainers.json   修改器清单（网站 + 客户端共用）
  --apply 时额外回写游戏数据里的 hasTrainer / trainerHotkeys / trainerInfo：
      src/data/games_top100.json（本地主数据，未进 git；存在才写，写前自动备份）
      public/data.js（只替换 window.GAMES_DATA 一段，其余原样保留）

用法：
  python3 scripts/fling_trainer_sync.py                 # 抓取 → 生成 public/trainers.json → 打印匹配报告
  python3 scripts/fling_trainer_sync.py --apply         # 同上，并回写游戏数据
  python3 scripts/fling_trainer_sync.py --cache-dir D   # 抓到的原始分页存到 D；D 里已有就直接用（调试用，少打对方站点）
"""

import argparse
import datetime
import glob
import html
import json
import os
import re
import shutil
import sys
import time
import unicodedata
import urllib.request

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAMES_JSON_PATH = os.path.join(BASE_DIR, "src/data/games_top100.json")
DATA_JS_PATH = os.path.join(BASE_DIR, "public/data.js")
MANIFEST_PATH = os.path.join(BASE_DIR, "public/trainers.json")

API = "https://flingtrainer.com/wp-json/wp/v2/posts"
FIELDS = "id,slug,link,title,modified,date,content"
USER_AGENT = "L-MOD-TrainerSync/1.0"
PAGE_DELAY_SEC = 2.0

# 自动匹配不上、或会误配到同系列别作的游戏，在这里手工指定风灵月影的 slug。
# 值为 None 表示确认风灵月影没有这款游戏的修改器。
MANUAL_SLUGS = {
    # 同一 Steam 应用，风灵月影换了标题
    "elden-ring": "elden-ring-shadow-of-the-erdtree-trainer",
    "monster-hunter-world": "monster-hunter-world-iceborne-trainer",
    "dying-light": "dying-light-enhanced-edition-trainer",
    "hitman-3": "hitman-3-trainer",
    "re4-remake": "resident-evil-4-trainer",
    "ghost-of-tsushima": "ghost-of-tsushima-trainer",
    # 宽松匹配会误配到 Remastered（另一个 Steam 应用），手工指回 Complete Edition
    "horizon-zero-dawn": "horizon-zero-dawn-complete-edition-trainer",
    # 风灵月影只有续作/同系列别作，或只在 2019 年前的旧存档里 —— 当作没有
    "the-forest": None, "cities-skylines": None, "borderlands-2": None, "far-cry-5": None,
    "slay-the-spire": None, "conan-exiles": None,
    # 风灵月影的 Raft 页（2026-03-14 版）正文是另一款无双类游戏的热键（Musou / K.O. / Karma Embers），疑似贴错，先当作没有
    "raft": None,
}

# ---------------------------------------------------------------------------
# 1. 抓取
# ---------------------------------------------------------------------------

def fetch_all_posts(cache_dir=None):
    if cache_dir:
        cached = sorted(glob.glob(os.path.join(cache_dir, "p*.json")),
                        key=lambda p: int(re.sub(r"\D", "", os.path.basename(p)) or 0))
        if cached:
            posts = []
            for path in cached:
                with open(path, encoding="utf-8") as f:
                    posts += json.load(f)
            print(f"📦 使用缓存 {cache_dir}：{len(cached)} 页 / {len(posts)} 款")
            return posts
        os.makedirs(cache_dir, exist_ok=True)

    posts, page, total_pages = [], 1, 1
    while page <= total_pages:
        url = f"{API}?per_page=100&page={page}&_fields={FIELDS}"
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=60) as resp:
            total_pages = int(resp.headers.get("X-WP-TotalPages", "1"))
            body = resp.read().decode("utf-8")
        batch = json.loads(body)
        posts += batch
        if cache_dir:
            with open(os.path.join(cache_dir, f"p{page}.json"), "w", encoding="utf-8") as f:
                f.write(body)
        print(f"🌐 第 {page}/{total_pages} 页：{len(batch)} 款")
        page += 1
        if page <= total_pages:
            time.sleep(PAGE_DELAY_SEC)
    return posts

# ---------------------------------------------------------------------------
# 2. 匹配
# ---------------------------------------------------------------------------

ROMAN = {"ii": "2", "iii": "3", "iv": "4", "v": "5", "vi": "6", "vii": "7", "viii": "8", "ix": "9", "xvi": "16"}
EDITION_WORDS = {"complete", "edition", "next", "gen", "remastered", "directors", "cut", "ultimate",
                 "intergrade", "special", "definitive", "goty", "royal", "remake", "the", "trainer"}


def norm_title(s):
    s = html.unescape(s or "")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = s.lower().replace("&", " and ").replace("’", "").replace("'", "")
    s = re.sub(r"[^a-z0-9]+", " ", s)
    words = [ROMAN.get(w, w) for w in s.split()]
    return " ".join(words)


def loose_key(s):
    return " ".join(w for w in norm_title(s).split() if w not in EDITION_WORDS)


def slug_base(url_or_slug):
    s = (url_or_slug or "").rstrip("/").split("/")[-1]
    return re.sub(r"-\d{6,}$", "", s)


def match_games(games, posts):
    trainer_posts = [p for p in posts if p["slug"] != "my-trainers-archive"]
    by_slug = {}
    for p in trainer_posts:
        by_slug.setdefault(slug_base(p["slug"]), []).append(p)
    by_title, by_loose = {}, {}
    for p in trainer_posts:
        by_title.setdefault(norm_title(p["title"]["rendered"]), []).append(p)
        by_loose.setdefault(loose_key(p["title"]["rendered"]), []).append(p)

    def newest(cands):
        return max(cands, key=lambda p: p["modified"]) if cands else None

    result = {}
    for g in games:
        gid = g["id"]
        if gid in MANUAL_SLUGS:
            want = MANUAL_SLUGS[gid]
            result[gid] = (newest(by_slug.get(slug_base(want), [])) if want else None, "manual")
            continue
        old_url = (g.get("trainerInfo") or {}).get("officialUrl", "")
        hit = newest(by_slug.get(slug_base(old_url), [])) if "flingtrainer.com" in old_url else None
        if hit:
            result[gid] = (hit, "slug")
            continue
        titles = [g.get("title", "")] + [g.get("titles", {}).get("en", "")]
        hit = None
        for t in titles:
            hit = newest(by_title.get(norm_title(t + " Trainer"), []))
            if hit:
                break
        if hit:
            result[gid] = (hit, "title")
            continue
        for t in titles:
            hit = newest(by_loose.get(loose_key(t), []))
            if hit:
                break
        result[gid] = (hit, "loose") if hit else (None, "none")
    return result

# ---------------------------------------------------------------------------
# 3. 解析正文
# ---------------------------------------------------------------------------

TIP_RE = re.compile(
    r"""jQuery\("document"\)\.ready\(function\(\)\{\s*toolTips\('[^']*','((?:[^'\\]|\\.)*)'\);\s*\}\);""", re.S)
SECTION_END_RE = re.compile(r"^(notes?|special notes|important notes|updates|update log|changelog)\s*:?$", re.I)
NOTE_LINE_RE = re.compile(r"^(note|notes)\s*:", re.I)
HOTKEY_RE = re.compile(r"^(?P<key>(?:(?:Ctrl|Alt|Shift)\+)*(?:Num\s?\S|Num|F\d{1,2}(?:/F\d{1,2})*|PageUp|PageDown|Home|End|Insert|Delete|[A-Za-z0-9\-=+\[\]]))\s+–\s+(?P<act>.+)$")
ANTI_CHEAT_RE = re.compile(r"anti-?cheat|easyanticheat|battleye|start_protected_game", re.I)
OFFLINE_ONLY_RE = re.compile(r"offline mode only|single[- ]player mode only|offline mode", re.I)


def unescape_tip(s):
    s = re.sub(r"\\(.)", r"\1", s)
    return re.sub(r"\s+", " ", s).strip()


def content_lines(raw_html):
    c = re.sub(r"<script.*?</script>", "", raw_html, flags=re.S)
    tips = []

    def keep_tip(m):
        tips.append(unescape_tip(m.group(1)))
        return f" ⟦TIP{len(tips) - 1}⟧ "

    c = TIP_RE.sub(keep_tip, c)
    platforms = re.findall(r"<title>([^<]+)</title>", c.split("</p>", 1)[0])
    c = re.sub(r"<svg.*?</svg>", " ", c, flags=re.S)
    c = re.sub(r"<br\s*/?>", "\n", c)
    c = re.sub(r"</(p|div|li|h\d|tr|blockquote)>", "\n", c)
    c = re.sub(r"<[^>]+>", "", c)
    c = html.unescape(c)
    lines = [re.sub(r"\s+", " ", l).strip() for l in c.split("\n")]
    return [l for l in lines if l], tips, [html.unescape(p) for p in platforms]


def parse_trainer(post):
    raw = post["content"]["rendered"]
    lines, tips, platforms = content_lines(raw)
    plain = "\n".join(lines)
    info = {
        "optionsCount": None,
        "gameVersion": "",
        "platforms": platforms,
        "lastUpdated": "",
        "antiCheat": bool(ANTI_CHEAT_RE.search(plain)),
        "offlineOnly": bool(OFFLINE_ONLY_RE.search(plain)),
        "hotkeys": [],
        "editableStats": [],
    }
    if lines:
        head = re.sub(r"⟦TIP\d+⟧", "", lines[0])
        m = re.search(r"(\d+)\s+Options", head)
        info["optionsCount"] = int(m.group(1)) if m else None
        m = re.search(r"Last Updated:\s*([\d.]+)", head)
        if m:
            info["lastUpdated"] = m.group(1).strip(".").replace(".", "-")
        m = re.search(r"Game Version:\s*(.*?)\s*(?:·|$)", head)
        if m:
            ver = m.group(1)
            for p in sorted(platforms, key=len, reverse=True):
                ver = ver.replace(p, " ")
            info["gameVersion"] = re.sub(r"\s+", " ", ver).strip()

    section, in_options = None, False
    for line in lines[1:]:
        tip_ids = [int(x) for x in re.findall(r"⟦TIP(\d+)⟧", line)]
        text = re.sub(r"\s*⟦TIP\d+⟧\s*", " ", line).strip()
        if not in_options:
            if text.lower() == "options":
                in_options = True
            continue
        if SECTION_END_RE.match(text) or NOTE_LINE_RE.match(text):
            break
        m = HOTKEY_RE.match(text)
        if m:
            key, act = m.group("key").strip(), m.group("act").strip()
            if act.startswith("– "):  # 「Num – – 隐身」这种，键位本身是小键盘减号
                key, act = key + " –", act[2:].strip()
            item = {"key": key, "en": act}
            if tip_ids:
                item["tip"] = " ".join(tips[i] for i in tip_ids)
            if section:
                item["section"] = section
            info["hotkeys"].append(item)
        elif len(text) <= 48 and not text.endswith((".", ":", "。")) and re.search(r"(?i)options|stats|edit|settings", text):
            section = text
        elif section and len(text) <= 48 and not text.endswith((".", "。")):
            info["editableStats"].append({"en": text, "section": section})
        else:
            break
    if info["optionsCount"] is None:
        info["optionsCount"] = len(info["hotkeys"]) + len(info["editableStats"])
    return info

# ---------------------------------------------------------------------------
# 4. 中文名
# ---------------------------------------------------------------------------

PHRASES = {
    "god mode": "无敌模式", "one hit kill": "一击必杀", "one hit kills": "一击必杀",
    "damage multiplier": "伤害倍率", "defense multiplier": "防御倍率", "game speed": "游戏速度",
    "set game speed": "设置游戏速度", "stealth mode": "隐身模式", "no reload": "无需换弹", "no recoil": "无后坐力",
    "super accuracy": "超级精准", "rapid fire": "快速射击", "no spread": "无扩散", "infinite ammo": "无限弹药",
    "infinite items/ammo": "无限物品/弹药", "items won't decrease": "物品不减少", "items won’t decrease": "物品不减少",
    "ignore crafting requirements": "无视制作需求", "free crafting": "免费制作", "easy crafting": "简易制作",
    "instant crafting": "瞬间制作", "fast crafting": "快速制作", "free upgrade": "免费升级", "free upgrades": "免费升级",
    "free purchase": "免费购买", "free shopping": "免费购物", "free build": "免费建造", "easy build": "简易建造",
    "instant build": "瞬间建造", "fast build": "快速建造", "max level": "满级", "max skills": "技能满级",
    "super jump": "超级跳跃", "enable fly mode": "开启飞行模式", "fly mode": "飞行模式", "no clip": "穿墙模式",
    "noclip": "穿墙模式", "teleport to waypoint": "传送到标记点", "teleport to marker": "传送到标记点",
    "save location": "保存坐标", "teleport": "传送", "freeze daytime": "冻结时间", "freeze time": "冻结时间",
    "freeze game time": "冻结游戏时间", "daytime +1 hour": "时间 +1 小时", "unlimited time": "无限时间",
    "freeze timer": "冻结计时器", "invisible": "隐身", "invisibility": "隐身", "no fall damage": "无坠落伤害",
    "no hunger": "不会饥饿", "no thirst": "不会口渴", "no hunger & thirst": "不会饥渴",
    "no hunger and thirst": "不会饥渴", "always full": "始终饱腹", "no cooldown": "无冷却",
    "skills no cooldown": "技能无冷却", "skill no cooldown": "技能无冷却", "abilities no cooldown": "能力无冷却",
    "no durability loss": "无耐久损耗", "unbreakable weapons": "武器不损坏", "max stats": "属性满值",
    "infinite jumps": "无限跳跃", "infinite double jumps": "无限二段跳", "weak enemies": "敌人虚弱",
    "enemies can't attack": "敌人无法攻击", "freeze enemies": "冻结敌人", "slow enemies": "敌人减速",
    "max affinity": "好感度满值", "max relationship": "关系满值", "max friendship": "友好度满值",
    "unlock all": "全部解锁", "unlock all skills": "解锁全部技能", "unlock all recipes": "解锁全部配方",
    "unlock all blueprints": "解锁全部蓝图", "unlock all items": "解锁全部物品", "unlock all weapons": "解锁全部武器",
    "infinite health": "无限生命", "infinite stamina": "无限耐力", "infinite mana": "无限法力",
    "infinite energy": "无限能量", "infinite oxygen": "无限氧气", "infinite money": "无限金钱",
    "infinite xp": "无限经验", "infinite exp": "无限经验", "infinite skill points": "无限技能点",
    "infinite items": "无限物品", "infinite resources": "无限资源", "infinite durability": "无限耐久",
    "infinite grenades": "无限手雷", "infinite focus": "无限专注", "infinite fp": "无限专注值 (FP)",
    "infinite hp": "无限生命", "infinite sp": "无限技能值 (SP)", "infinite mp": "无限魔法值 (MP)",
    "infinite ap": "无限行动点 (AP)", "infinite shield": "无限护盾", "infinite armor": "无限护甲",
    "infinite fuel": "无限燃料", "infinite battery": "无限电量", "infinite runes": "无限卢恩",
    "infinite souls": "无限魂", "infinite gold": "无限金币", "infinite credits": "无限信用点",
    "infinite carry weight": "无限负重", "infinite rage": "无限怒气", "infinite adrenaline": "无限肾上腺素",
    "infinite breath": "无限呼吸", "infinite sanity": "无限理智", "infinite food": "无限食物",
    "infinite water": "无限水", "infinite power": "无限电力", "infinite research points": "无限研究点",
    "infinite influence": "无限影响力", "infinite prestige": "无限威望", "infinite gems": "无限宝石",
    "infinite crystals": "无限水晶", "infinite components": "无限零件", "infinite materials": "无限材料",
    "infinite crafting materials": "无限制作材料", "infinite ram": "无限 RAM",
    "infinite street cred": "无限街头声望", "infinite consumables": "无限消耗品",
    "infinite healing items": "无限治疗物品", "infinite throwables": "无限投掷物",
    "infinite perk points": "无限天赋点", "infinite attribute points": "无限属性点",
    "super damage": "超级伤害", "super speed": "超级速度", "ignore hits": "无视攻击", "ignore hit": "无视攻击",
    "invincible": "无敌", "100% drop rate": "100% 掉落率", "zero weight": "零重量", "slow motion": "慢动作",
    "teleport to waypoint location": "传送到标记点", "teleport to saved location": "传送到保存坐标",
    "undo teleportation": "撤销传送", "daytime -1 hour": "时间 -1 小时", "time pass speed": "时间流逝速度",
    "100% critical chance": "100% 暴击率", "100% critical rate": "100% 暴击率", "max combo": "最大连击",
    "enemies can't attack": "敌人无法攻击", "one hit stun": "一击眩晕", "weapons no overheat": "武器不过热",
    "stable body temperature": "体温稳定", "instant craft": "瞬间制作", "instant catch": "瞬间上钩",
    "one turn construction": "一回合建造", "empty enemies morale": "敌人士气清空",
    "prevent negative status": "免疫负面状态", "no overburden": "不会超重", "ignore weight": "无视负重",
    "ignore cyberware capacity": "无视义体容量", "no crafting material requirements": "无需制作材料",
    "always succeed": "必定成功", "no fog": "去除迷雾", "reveal map": "显示全地图", "unlock all": "全部解锁",
    "won't lose runes when player dies": "死亡不掉卢恩", "fly up": "向上飞", "fly down": "向下飞",
    "freeze enemies position": "冻结敌人位置", "enemies cannot move": "敌人无法移动", "lock health": "锁定生命",
    "immune to all negative status": "免疫所有负面状态", "easy lock picking": "简易开锁",
    "food won't spoil": "食物不腐坏", "fast crafting & building": "快速制作与建造",
    "perfect body temperature": "体温完美", "no building material requirements": "无需建造材料",
    "no equipment upgrade requirement": "无需装备升级材料", "100% pal capture rate": "100% 帕鲁捕获率",
    "100% rare pal spawn rate": "100% 稀有帕鲁刷新率", "one hit destroy": "一击摧毁",
}

NOUNS = {
    "health": "生命", "hp": "生命", "stamina": "耐力", "mana": "法力", "energy": "能量", "money": "金钱",
    "gold": "金币", "coins": "金币", "cash": "现金", "credits": "信用点", "xp": "经验", "exp": "经验",
    "experience": "经验", "skill points": "技能点", "skill point": "技能点", "attribute points": "属性点",
    "perk points": "天赋点", "ability points": "能力点", "talent points": "天赋点", "research points": "研究点",
    "level": "等级", "player level": "玩家等级", "character level": "角色等级", "movement speed": "移动速度",
    "move speed": "移动速度", "run speed": "奔跑速度", "jump height": "跳跃高度", "attack speed": "攻击速度",
    "damage": "伤害", "defense": "防御", "armor": "护甲", "strength": "力量", "dexterity": "敏捷",
    "intelligence": "智力", "agility": "敏捷", "luck": "幸运", "vitality": "活力", "endurance": "耐力",
    "charisma": "魅力", "perception": "感知", "constitution": "体质", "wisdom": "感知", "stats": "属性",
    "items": "物品", "item": "物品", "ammo": "弹药", "resources": "资源", "materials": "材料",
    "components": "零件", "durability": "耐久", "oxygen": "氧气", "food": "食物", "water": "水",
    "hunger": "饥饿", "thirst": "口渴", "fuel": "燃料", "reputation": "声望", "fame": "名声",
    "influence": "影响力", "prestige": "威望", "runes": "卢恩", "souls": "魂", "skill xp": "技能经验",
    "street cred": "街头声望", "max carrying weight": "最大负重", "carry weight": "负重",
    "max health": "最大生命", "max stamina": "最大耐力", "max mana": "最大法力", "score": "分数",
    "max score": "最高分", "game speed": "游戏速度", "player speed": "玩家速度", "time": "时间",
    "crafting materials": "制作材料", "inventory items": "背包物品", "selected item": "选中物品",
    "selected item amount": "选中物品数量", "item amount": "物品数量", "skill level": "技能等级",
    "relationship": "关系", "affinity": "好感度", "friendship": "友好度", "happiness": "幸福度",
    "loyalty": "忠诚度", "population": "人口", "research": "研究", "power": "电力", "gems": "宝石",
    "crystals": "水晶", "keys": "钥匙", "lockpicks": "开锁器", "potions": "药水", "grenades": "手雷",
    "skills": "技能", "skill": "技能", "abilities": "能力", "ability": "能力", "healing items": "治疗物品",
    "consumables": "消耗品", "rage": "怒气", "focus": "专注", "shield": "护盾", "sanity": "理智",
    "battery": "电量", "breath": "呼吸", "speed": "速度", "player stats": "玩家属性",
    "character stats": "角色属性", "money multiplier": "金钱倍率", "xp multiplier": "经验倍率",
    "equipment durability": "装备耐久", "weapon durability": "武器耐久", "item durability": "物品耐久",
    "vehicle health": "载具生命", "horse health": "马匹生命", "horse stamina": "马匹耐力", "arrow": "箭矢",
    "arrows": "箭矢", "relic points": "遗物点", "clicked item amount": "点选物品数量", "radiation": "辐射",
    "crafting recipes": "制作配方", "recipes": "配方", "blueprints": "蓝图", "swim speed": "游泳速度",
    "building": "建造", "crafting": "制作", "construction": "建造", "challenge timer": "挑战计时器",
    "timer": "计时器", "research": "研究", "build": "建造", "craft": "制作", "max encumbrance": "最大负重",
    "magick": "魔力", "magick defense": "魔法防御", "knockdown power": "击倒力", "consumables": "消耗品",
    "skill cards": "技能卡", "accessories": "饰品", "outfits": "服装", "weapons": "武器", "gil": "金币 (Gil)",
    "materials amount": "材料数量", "job exp": "职业经验", "bond": "羁绊", "force": "原力",
    "projectile launch system": "投射物发射系统", "breach protocol timer": "破解协议计时器",
    "quickhack components": "快速破解零件", "street cred level": "街头声望等级", "fly height": "飞行高度",
    "fly speed": "飞行速度", "gourd": "葫芦", "spell": "法术", "spells": "法术", "transform": "变身",
    "weapon": "武器", "critical hit chance": "暴击率", "critical chance": "暴击率", "critical hit damage": "暴击伤害",
    "critical damage": "暴击伤害", "poise": "韧性", "stamina consumption rate": "耐力消耗率", "attack": "攻击力",
    "stamina recovery rate": "耐力恢复速率", "damage bonus": "伤害加成", "damage reduction": "伤害减免",
    "chill": "冰冻", "burn": "灼烧", "poison": "中毒", "shock": "雷电", "fire": "火焰", "ice": "冰霜",
    "lightning": "雷电", "magic": "魔法", "toxicity": "毒性", "potions & bombs": "药水和炸弹",
    "progression": "进度", "skill xp": "技能经验", "max skill xp": "技能经验满值", "dice": "骰子",
    "morale": "士气", "vehicle fuel": "载具燃料", "nitro": "氮气", "boost": "加速", "ammo": "弹药",
    "mana/stamina": "法力/耐力", "magazine": "弹匣", "hunger & thirst": "饥渴", "temperature": "体温",
    "body temperature": "体温", "wanted level": "通缉等级", "spirit energy": "精魄能量", "vessel energy": "法宝能量",
    "health regeneration": "生命恢复", "stamina regeneration": "耐力恢复", "mana regeneration": "法力恢复",
    "max hp": "最大生命", "max fp": "最大专注值 (FP)", "vigor": "生命力", "mind": "集中力", "faith": "信仰",
    "arcane": "感应", "endurance": "耐力", "buff": "增益", "drop item": "掉落物品", "items amount": "物品数量",
    "dragon shouts": "龙吼", "power armor core power": "动力装甲核心能量", "hacking attempts": "骇入次数",
    "companions approval": "同伴好感", "horse hp": "马匹生命", "cp": "CP",
}

PATTERNS = [
    (re.compile(r"^infinite (.+) usage$"), "{}无限使用"),
    (re.compile(r"^infinite (.+) duration$"), "{}无限持续"),
    (re.compile(r"^infinite (.+)$"), "无限{}"),
    (re.compile(r"^unlimited (.+)$"), "无限{}"),
    (re.compile(r"^edit base (.+)$"), "修改基础{}"),
    (re.compile(r"^edit (.+)$"), "修改{}"),
    (re.compile(r"^set (.+)$"), "设置{}"),
    (re.compile(r"^max (.+) level$"), "{}满级"),
    (re.compile(r"^max (.+)$"), "{}满值"),
    (re.compile(r"^freeze (.+)$"), "冻结{}"),
    (re.compile(r"^increase (.+)$"), "提高{}"),
    (re.compile(r"^super (.+)$"), "超级{}"),
    (re.compile(r"^instant (.+) cooldown$"), "{}瞬间冷却"),
    (re.compile(r"^(.+) instant cooldown$"), "{}瞬间冷却"),
    (re.compile(r"^instant (.+)$"), "瞬间{}"),
    (re.compile(r"^obtain all (.+)$"), "获得全部{}"),
    (re.compile(r"^unlock all (.+)$"), "解锁全部{}"),
    (re.compile(r"^ignore (.+) requirements?$"), "无视{}需求"),
    (re.compile(r"^drain enemies (.+)$"), "清空敌人{}"),
    (re.compile(r"^teleport to (.+)$"), "传送到{}"),
    (re.compile(r"^zero (.+)$"), "零{}"),
    (re.compile(r"^(.+) multiplier$"), "{}倍率"),
    (re.compile(r"^(.+) resistance$"), "{}抗性"),
    (re.compile(r"^(.+) no cooldown$"), "{}无冷却"),
    (re.compile(r"^(.+) won't decrease$"), "{}不减少"),
    (re.compile(r"^(.+) don't decrease$"), "{}不减少"),
    (re.compile(r"^no (.+) loss$"), "无{}损耗"),
    (re.compile(r"^no (.+)$"), "无{}"),
    (re.compile(r"^add (.+)$"), "增加{}"),
]


def to_zh(en, _depth=0):
    key = re.sub(r"\s+", " ", en.strip().lower()).replace("’", "'").replace("‘", "'")
    key = re.sub(r"\s*\(.*?\)\s*", " ", key).strip()  # 「Infinite Double Jumps (Reinforced Tendons)」去掉括注再查
    key = re.sub(r"^[a-z ]+: ", "", key) if _depth == 0 and key.count(":") == 1 else key  # 「Fishing: Instant Catch」
    if key in PHRASES:
        return PHRASES[key]
    if key in NOUNS:
        return NOUNS[key]
    m = re.match(r"^add (\d[\d,]*) (.+)$", key)
    if m and m.group(2) in NOUNS:
        return f"增加 {m.group(1)} {NOUNS[m.group(2)]}"
    for pat, tpl in PATTERNS:
        m = pat.match(key)
        if m:
            noun = m.group(1).strip()
            if noun in NOUNS:
                return tpl.format(NOUNS[noun])
            if "/" in noun:  # 「Infinite Health/Stamina」「Items/Gold Won't Decrease」
                parts = [NOUNS.get(p.strip()) for p in noun.split("/")]
                if all(parts):
                    return tpl.format("/".join(parts))
    if "/" in key and _depth == 0:  # 「Super Damage/One Hit Kills」：每段都是完整短语
        parts = [to_zh(p, _depth + 1) for p in key.split("/")]
        if all(parts):
            return "/".join(parts)
    return None

# ---------------------------------------------------------------------------
# 5. 分组
# ---------------------------------------------------------------------------

CATEGORIES = [
    ("combat", "⚔️ 战斗与生存 (Combat & Survival)",
     r"health|\bhp\b|stamina|mana|\bmp\b|\bsp\b|\bfp\b|energy|god mode|damage|defen[cs]e|kill|ammo|reload|recoil|accuracy|"
     r"spread|grenade|stealth|invisib|cooldown|shield|armor|oxygen|hunger|thirst|breath|sanity|rage|focus|adrenaline|"
     r"durability|enemies|enemy|fall damage|healing|poison|bleed|status effect"),
    ("economy", "💰 资源与物品 (Resources & Items)",
     r"money|gold|coin|cash|credit|item|resource|material|component|craft|currency|souls|runes|gems?|crystal|fuel|"
     r"food|water|consumable|purchase|shop|build|upgrade|inventory|carry|weight|ram\b|lockpick|key"),
    ("progress", "📈 等级与属性 (Level & Stats)",
     r"\bxp\b|\bexp\b|experience|level|skill|point|attribute|stat|perk|talent|ability|abilities|reputation|fame|"
     r"cred|affinity|relationship|friendship|loyalty|prestige|influence|score"),
    ("world", "🌍 移动与世界 (Movement & World)",
     r"speed|jump|fly|teleport|clip|time|day|weather|gravity|height|waypoint|location|position|map"),
]
OTHER_CATEGORY = ("other", "🧩 其他功能 (Other)")


def categorize(hotkeys):
    groups = {}
    for hk in hotkeys:
        en = hk["en"].lower()
        cat = OTHER_CATEGORY
        for cid, label, pat in CATEGORIES:
            if re.search(pat, en):
                cat = (cid, label)
                break
        groups.setdefault(cat, []).append(hk)
    order = [c[:2] for c in CATEGORIES] + [OTHER_CATEGORY]
    out = []
    for cid, label in order:
        items = groups.get((cid, label))
        if items:
            out.append({"category": label, "items": [
                {"key": h["key"], "action": f'{h["zh"]} ({h["en"]})' if h.get("zh") else h["en"],
                 **({"tip": h["tip"]} if h.get("tip") else {})}
                for h in items]})
    return out

# ---------------------------------------------------------------------------
# 6. 产出
# ---------------------------------------------------------------------------

def build_manifest(games, matches):
    entries, unmatched, untranslated = {}, [], {}
    for g in games:
        post, how = matches[g["id"]]
        if not post:
            unmatched.append(g["id"])
            continue
        info = parse_trainer(post)
        for hk in info["hotkeys"]:
            zh = to_zh(hk["en"])
            if zh:
                hk["zh"] = zh
            else:
                untranslated[hk["en"]] = untranslated.get(hk["en"], 0) + 1
        entries[g["id"]] = {
            "flingId": post["id"],
            "title": html.unescape(post["title"]["rendered"]),
            "url": post["link"],
            "matchedBy": how,
            "modified": post["modified"],
            **info,
        }
    manifest = {
        "schema": 1,
        "generatedAt": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
        "source": "flingtrainer.com 公开 WordPress 接口（只读元数据，不转存文件）",
        "author": "风灵月影 (FLiNG)",
        "games": entries,
        "unmatched": unmatched,
    }
    return manifest, untranslated


def apply_to_game(g, entry):
    if not entry:
        g["hasTrainer"] = False
        g["trainerHotkeys"] = []
        g["trainerInfo"] = {}  # 保持 dict：老脚本普遍写 g.get("trainerInfo", {}).get(...)
        return
    hk = entry["hotkeys"]
    g["hasTrainer"] = True
    g["trainerHotkeys"] = [{"key": h["key"], "action": f'{h["en"]} ({h["zh"]})' if h.get("zh") else h["en"]}
                           for h in hk[:8]]
    g["trainerInfo"] = {
        "author": "风灵月影 (FLiNG)",
        "officialUrl": entry["url"],
        "version": entry["gameVersion"] or "见官方页面",
        "optionsCount": entry["optionsCount"],
        "lastUpdated": entry["lastUpdated"],
        "platforms": entry["platforms"],
        "antiCheat": entry["antiCheat"],
        "offlineOnly": entry["offlineOnly"],
        "hotkeysCategorized": categorize(hk),
        "source": "trainers.json",
    }


def write_games(games):
    if os.path.exists(GAMES_JSON_PATH):
        # 本地有主数据：经 gamedata_guard（owner="trainer"）只写 hasTrainer / trainerHotkeys / trainerInfo
        # 里确实变了的部分，主数据和 data.js 的 GAMES_DATA 段同步改，其它字段和 TRANSLATIONS_DATA 不动
        from gamedata_guard import TRAINER_FIELDS, write_changed_fields
        stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = GAMES_JSON_PATH.replace(".json", f".before-trainer-sync-{stamp}.backup.json")
        shutil.copy2(GAMES_JSON_PATH, backup)
        write_changed_fields("fling_trainer_sync.py", TRAINER_FIELDS, games, dry_run=False, owner="trainer")
        print(f"✅ 已回写（备份：{os.path.relpath(backup, BASE_DIR)}）")
        return

    # 没有主数据（GitHub Actions / 新克隆）：只替换 data.js 里 GAMES_DATA 一段
    with open(DATA_JS_PATH, encoding="utf-8") as f:
        s = f.read()
    head = "window.GAMES_DATA = "
    a = s.index(head) + len(head)
    b = s.index(";\n\nwindow.GAMES_DATABASE", a)
    s = s[:a] + json.dumps(games, ensure_ascii=False, indent=2) + s[b:]
    with open(DATA_JS_PATH, "w", encoding="utf-8") as f:
        f.write(s)
    print(f"✅ 已回写 {os.path.relpath(DATA_JS_PATH, BASE_DIR)}（只替换 GAMES_DATA 一段）")


def load_games():
    if os.path.exists(GAMES_JSON_PATH):
        with open(GAMES_JSON_PATH, encoding="utf-8") as f:
            return json.load(f)
    with open(DATA_JS_PATH, encoding="utf-8") as f:
        s = f.read()
    head = "window.GAMES_DATA = "
    a = s.index(head) + len(head)
    b = s.index(";\n\nwindow.GAMES_DATABASE", a)
    return json.loads(s[a:b])


def main():
    ap = argparse.ArgumentParser(description="风灵月影修改器清单同步")
    ap.add_argument("--apply", action="store_true", help="回写游戏数据（games_top100.json + public/data.js）")
    ap.add_argument("--cache-dir", help="原始分页缓存目录（调试用）")
    args = ap.parse_args()

    games = load_games()
    posts = fetch_all_posts(args.cache_dir)
    matches = match_games(games, posts)
    manifest, untranslated = build_manifest(games, matches)

    old = None
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH, encoding="utf-8") as f:
            old = json.load(f)
    if old and {k: v for k, v in old.items() if k != "generatedAt"} == \
            {k: v for k, v in manifest.items() if k != "generatedAt"}:
        manifest["generatedAt"] = old.get("generatedAt", manifest["generatedAt"])  # 内容没变就不动时间戳，免得每天空提交
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
        f.write("\n")

    entries = manifest["games"]
    hk_total = sum(len(e["hotkeys"]) for e in entries.values())
    hk_zh = sum(1 for e in entries.values() for h in e["hotkeys"] if h.get("zh"))
    by_how = {}
    for e in entries.values():
        by_how[e["matchedBy"]] = by_how.get(e["matchedBy"], 0) + 1
    print(f"\n📋 匹配：{len(entries)}/{len(games)} 款（{by_how}）")
    print(f"   未匹配：{manifest['unmatched']}")
    print(f"   热键：{hk_total} 条，有中文名 {hk_zh} 条（{hk_zh * 100 // max(hk_total, 1)}%）")
    print(f"   带反作弊：{[k for k, e in entries.items() if e['antiCheat']]}")
    no_hk = [k for k, e in entries.items() if not e["hotkeys"]]
    if no_hk:
        print(f"   ⚠️ 没解析出热键：{no_hk}")
    loose = {k: e["title"] for k, e in entries.items() if e["matchedBy"] == "loose"}
    if loose:
        print(f"   ⚠️ 宽松匹配（请人工确认）：{loose}")
    print(f"✅ 已生成 {os.path.relpath(MANIFEST_PATH, BASE_DIR)}")

    if untranslated and os.environ.get("SHOW_UNTRANSLATED"):
        for en, n in sorted(untranslated.items(), key=lambda x: -x[1])[:120]:
            print(f"   {n:3d}  {en}")

    if args.apply:
        for g in games:
            apply_to_game(g, entries.get(g["id"]))
        write_games(games)
    return 0


if __name__ == "__main__":
    sys.exit(main())
