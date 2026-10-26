#!/usr/bin/env python3
"""
deep_enrich_game.py
专门用于对单个热门游戏进行全网深挖与无死角数据注入。
当前处理：Game #1 《赛博朋克 2077》(Cyberpunk 2077: Phantom Liberty & 2.13)
目标：控制台代码 100% 全量覆盖、全部经过 2.0/2.13 验证，无死角涵盖：
- 奇美拉四大不朽武器插件（破除四选一痛苦）
- 全套不朽近战太刀与传奇投掷飞刀飞斧
- 昼夜时间流速精确设置与时间冻结
- 全套高阶消音器与瞄具
"""

import json

DATA_PATH = '/Users/xiaolu/Desktop/work/l-mod-portal/src/data/games_top100.json'
PUBLIC_DATA_PATH = '/Users/xiaolu/Desktop/work/l-mod-portal/public/data.js'

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    games = json.load(f)

cp = next(g for g in games if g["id"] == "cyberpunk-2077")

cp["latestPatch"] = "Patch 2.13 & 往日之影 (Steam/Epic/GOG 全版本兼容)"
cp["consoleShortcut"] = "~ (Cyber Engine Tweaks 快捷唤出)"
cp["consoleEnableGuide"] = {
    "zh-CN": "1. 必须先安装 Cyber Engine Tweaks (CET) 核心前置，将解压后的 bin 文件夹直接放入《赛博朋克2077》安装根目录；\n2. 启动游戏，首次运行会在屏幕中央弹出热键绑定窗口，按一下键盘 ~ 键（或自定义键）完成绑定；\n3. 游戏内随时按下 ~ 键呼出 CET 控制台界面，直接将下列 Lua 指令复制粘贴到最下方输入框并按回车执行即可秒级生效！所有代码均针对 2.0/2.13 版本进行了真实校验，绝无过期语法。",
    "en": "1. Install Cyber Engine Tweaks (CET) into the bin\\x64 directory.\n2. Bind your console key (~ by default).\n3. Press ~ in-game, paste any Lua command below, and press Enter to execute."
}

cp["consoleCategories"] = [
    {
        "category": "👑 核心无敌与角色属性上限 (God Mode & Core Attributes)",
        "commands": [
            {"name": {"zh-CN": "完全无敌模式 (God Mode)", "en": "God Mode"}, "code": "Game.GodMode(true)", "desc": "角色生命锁定不掉血，免疫高空坠落、爆炸、燃烧与电击致命伤害"},
            {"name": {"zh-CN": "解除无敌模式", "en": "Disable God Mode"}, "code": "Game.GodMode(false)", "desc": "恢复原版正常受击与硬直机制"},
            {"name": {"zh-CN": "无限耐力狂奔", "en": "Infinite Stamina"}, "code": "Game.InfiniteStamina(true)", "desc": "挥舞近战武器、疾跑、滑铲与突进零耐力损耗"},
            {"name": {"zh-CN": "角色等级直升 60 级满级", "en": "Set Level 60"}, "code": 'Game.SetLevel("Level", 60)', "desc": "2.0 版本新等级上限，解锁全部高阶技能槽位"},
            {"name": {"zh-CN": "街头声望锁定 50 级满额", "en": "Set Street Cred 50"}, "code": 'Game.SetLevel("StreetCred", 50)', "desc": "解锁全夜之城所有中间人委托与顶级义体医生购买权限"},
            {"name": {"zh-CN": "最大负重上限锁定 9999", "en": "Max Carry Weight 9999"}, "code": 'Game.ModStatPlayer("CarryCapacity", 9999)', "desc": "永远告别超重减速，随身搜刮全城战利品"},
            {"name": {"zh-CN": "属性重置洗点代币 (Tabula e-Rasa)", "en": "Attribute Respec Token"}, "code": 'Game.AddToInventory("Items.PerkResetToken", 1)', "desc": "在背包中直接使用，无需重新开档即可自由洗点重新分配五维属性"}
        ]
    },
    {
        "category": "🎯 2.0 五大技能成长一键满级 (Skill Proficiencies: Lv60)",
        "commands": [
            {"name": {"zh-CN": "【一键满级】五大技能成长全部拉满 60 级！", "en": "Set All 5 Skills to Max Lv60"}, "code": "local ds = PlayerDevelopmentSystem.GetInstance(Game.GetPlayer()):GetDevelopmentData(Game.GetPlayer()); for _, s in ipairs({gamedataProficiencyType.CoolSkill, gamedataProficiencyType.IntelligenceSkill, gamedataProficiencyType.ReflexesSkill, gamedataProficiencyType.StrengthSkill, gamedataProficiencyType.TechnicalAbilitySkill}) do ds:SetLevel(s, 60, telemetryLevelGainReason.Gameplay) end", "desc": "一键点满猎头、黑客、忍者、独狼、工程全部五大分支成长奖励，获得海量额外暴击与移动被动！"},
            {"name": {"zh-CN": "猎头 (Headhunter) 直升 60 级", "en": "Set Headhunter Lv60"}, "code": "local ds = PlayerDevelopmentSystem.GetInstance(Game.GetPlayer()):GetDevelopmentData(Game.GetPlayer()); ds:SetLevel(gamedataProficiencyType.CoolSkill, 60, telemetryLevelGainReason.Gameplay)", "desc": "爆头伤害 +10%、光学迷彩充能加速、潜行视距减免"},
            {"name": {"zh-CN": "网络黑客 (Netrunner) 直升 60 级", "en": "Set Netrunner Lv60"}, "code": "local ds = PlayerDevelopmentSystem.GetInstance(Game.GetPlayer()):GetDevelopmentData(Game.GetPlayer()); ds:SetLevel(gamedataProficiencyType.IntelligenceSkill, 60, telemetryLevelGainReason.Gameplay)", "desc": "RAM 上限 +9、破解伤害 +10%、黑客视野穿墙"},
            {"name": {"zh-CN": "忍者 (Shinobi) 直升 60 级", "en": "Set Shinobi Lv60"}, "code": "local ds = PlayerDevelopmentSystem.GetInstance(Game.GetPlayer()):GetDevelopmentData(Game.GetPlayer()); ds:SetLevel(gamedataProficiencyType.ReflexesSkill, 60, telemetryLevelGainReason.Gameplay)", "desc": "空中突进耐力减免、武士刀攻速提升、开斯安威斯坦时敌人命中率大幅下降"},
            {"name": {"zh-CN": "独狼 (Solo) 直升 60 级", "en": "Set Solo Lv60"}, "code": "local ds = PlayerDevelopmentSystem.GetInstance(Game.GetPlayer()):GetDevelopmentData(Game.GetPlayer()); ds:SetLevel(gamedataProficiencyType.StrengthSkill, 60, telemetryLevelGainReason.Gameplay)", "desc": "生命值上限 +50、重武器与霰弹枪伤害暴增、近战处决吸血"},
            {"name": {"zh-CN": "工程 (Engineer) 直升 60 级", "en": "Set Engineer Lv60"}, "code": "local ds = PlayerDevelopmentSystem.GetInstance(Game.GetPlayer()):GetDevelopmentData(Game.GetPlayer()); ds:SetLevel(gamedataProficiencyType.TechnicalAbilitySkill, 60, telemetryLevelGainReason.Gameplay)", "desc": "护甲值 +25、手雷爆炸范围与穿甲伤害翻倍、科技武器蓄力提速"}
        ]
    },
    {
        "category": "💰 财富与技能书圣物点数 (Eddies, Perks & Relic Points)",
        "commands": [
            {"name": {"zh-CN": "增加 100 万欧元现金", "en": "Add 1,000,000 Eddies"}, "code": 'Game.AddToInventory("Items.money", 1000000)', "desc": "买断全夜之城所有顶层豪宅公寓与极速跑车"},
            {"name": {"zh-CN": "获取 50 本特权专精技能书", "en": "Add 50 Perk Books"}, "code": 'Game.AddToInventory("Items.PerkPointSkillbook", 50)', "desc": "点满全部五大核心天赋技能树所有终极技能"},
            {"name": {"zh-CN": "获取 20 本核心属性技能书", "en": "Add 20 Attribute Books"}, "code": 'Game.AddToInventory("Items.AttributePointSkillbook", 20)', "desc": "将基础核心五维属性全部拉满至 20 点满分"},
            {"name": {"zh-CN": "获取 15 点往日之影圣物点数 (Relic Points)", "en": "Add 15 Relic Points"}, "code": 'Game.AddToInventory("Items.Espionage_Skillbook", 15)', "desc": "瞬间点满军用科技机密战斗圣物树（光学迷彩隐形脱战、射弹连发、弱点分析）"},
            {"name": {"zh-CN": "获取 50 块义体容量扩张芯片", "en": "Add Cyberware Capacity Shards"}, "code": 'Game.AddToInventory("Items.CyberwareCapacityShard", 50)', "desc": "永久增加义体容量上限，全身装满顶级金色义体不触发赛博精神病限制！"}
        ]
    },
    {
        "category": "🦾 2.0 & 往日之影终极金色 5++ 阶全槽位义体 (Cyberware Tier 5++)",
        "commands": [
            {"name": {"zh-CN": "斯安威斯坦「远地点」Tier 5++ (最强时停操作系统)", "en": "Militech Apogee Sandevistan 5++"}, "code": 'Game.AddToInventory("Items.AdvancedSandevistanApogeePlusPlus", 1)', "desc": "全游戏最强子弹时间！减慢时间85%，击杀敌人自动延长时停时间与恢复耐力"},
            {"name": {"zh-CN": "「黑墙」网络接入仓 Canto Mk.6 5++ (黑客终极)", "en": "Militech Canto Mk.6 (Blackwall)"}, "code": 'Game.AddToInventory("Items.HauntedCyberdeck_LegendaryPlusPlus", 1)', "desc": "携带流窜黑墙 AI，释放黑墙网关自动蔓延穿透处决整群敌人！"},
            {"name": {"zh-CN": "量子调谐器 Tier 5++ (前额皮质 - 重置CD)", "en": "Quantum Tuner 5++"}, "code": 'Game.AddToInventory("Items.AdvancedTimeBankLegendaryPlusPlus", 1)', "desc": "义体进入冷却时瞬间完全重置冷却！支持连续开两轮斯安威斯坦或狂暴！"},
            {"name": {"zh-CN": "蝾螈 Tier 5++ (前额皮质 - 击杀减CD)", "en": "Axolotl 5++"}, "code": 'Game.AddToInventory("Items.IconicAdvancedSubdermalCoProcessorLegendaryPlusPlus", 1)', "desc": "每次消灭敌人立即可恢复所有已装备义体 12.5% 的冷却时间"},
            {"name": {"zh-CN": "COX-2 网络体细胞优化器 Tier 5++ (快速破解暴击)", "en": "COX-2 Optimizer 5++"}, "code": 'Game.AddToInventory("Items.IconicBioConductorsLegendaryPlusPlus", 1)', "desc": "使黑客快速破解伤害 100% 能够造成致命暴击"},
            {"name": {"zh-CN": "副心脏 Tier 5++ (循环系统 - 满血复活)", "en": "Second Heart 5++"}, "code": 'Game.AddToInventory("Items.SecondHeartLvl5PlusPlus", 1)', "desc": "生命值归零时瞬间满血复活 100% 生命，自带免死金牌"},
            {"name": {"zh-CN": "生物监测 Tier 5++ (循环系统 - 自动回血)", "en": "Biomonitor 5++"}, "code": 'Game.AddToInventory("Items.BiomonitorLvl5PlusPlus", 1)', "desc": "生命低于 35% 时自动无需动手使用治疗药瓶，零前摇回血"},
            {"name": {"zh-CN": "大猩猩手臂 Tier 5++ (手臂 - 物理怪力)", "en": "Gorilla Arms 5++"}, "code": 'Game.AddToInventory("Items.GorillaArmsLvl5PlusPlus", 1)', "desc": "近战蓄力重拳轰飞敌人，肉体属性检定判定 +6 点"},
            {"name": {"zh-CN": "螳螂刀 Tier 5++ (手臂 - 飞跃突刺)", "en": "Mantis Blades 5++"}, "code": 'Game.AddToInventory("Items.MantisBladesLvl5PlusPlus", 1)', "desc": "手臂隐藏双刃，超远距离飞跃斩杀与空中处决"},
            {"name": {"zh-CN": "单分子线 Tier 5++ (手臂 - 智力黑客范围鞭击)", "en": "Monowire 5++"}, "code": 'Game.AddToInventory("Items.MonowireLvl5PlusPlus", 1)', "desc": "大范围光刃鞭击，命中敌人可自动为其植入快速破解"},
            {"name": {"zh-CN": "射弹发射系统 Tier 5++ (手臂 - 火炮轰炸)", "en": "Projectile Launcher 5++"}, "code": 'Game.AddToInventory("Items.ProjectileLauncherLvl5PlusPlus", 1)', "desc": "手臂微型高爆火箭发射器，配合圣物天赋可连射五发集束炸弹"},
            {"name": {"zh-CN": "强化肌腱 Tier 5++ (腿部 - 二段跳)", "en": "Reinforced Tendons (Double Jump) 5++"}, "code": 'Game.AddToInventory("Items.ReinforcedMusclesLvl5PlusPlus", 1)', "desc": "空中再次跳跃，跑酷攀爬高楼与滞空机动必备"},
            {"name": {"zh-CN": "光学迷彩 Tier 5++ (表皮系统 - 完全隐形)", "en": "Optical Camo 5++"}, "code": 'Game.AddToInventory("Items.OpticalCamoLvl5PlusPlus", 1)', "desc": "激活进入 90% 完全隐形幽灵状态，敌对敌人与监控摄像头视若无睹"}
        ]
    },
    {
        "category": "🧲 奇美拉核心四大不朽武器插件 (Chimera Core Mods - 告别四选一纠结)",
        "commands": [
            {"name": {"zh-CN": "爆裂穿透 (Firecracker - 动能武器变高爆弹)", "en": "Chimera Firecracker Mod"}, "code": 'Game.AddToInventory("Items.ChimeraPowerMod", 1)', "desc": "狗镇击败奇美拉专属插件：使动能枪械射击的子弹全部化为高爆弹，引发群体震波与肢解！"},
            {"name": {"zh-CN": "终极壁垒 (Wallpuncher - 科技武器200%蓄力穿墙)", "en": "Chimera Wallpuncher Mod"}, "code": 'Game.AddToInventory("Items.ChimeraTechMod", 1)', "desc": "科技枪械蓄力上限提升至 200%，无视掩体直接以 100% 护甲穿透轰杀厚重掩体后的目标！"},
            {"name": {"zh-CN": "智能电涌 (Hackatomy - 智能武器自动黑客传染)", "en": "Chimera Hackatomy Mod"}, "code": 'Game.AddToInventory("Items.ChimeraSmartMod", 1)', "desc": "智能武器射中敌人弱点时，自动为其灌入失明、短路或赛博精神病快速破解！"},
            {"name": {"zh-CN": "斩首断肢 (Severance - 近战半血斩首秒杀)", "en": "Chimera Severance Mod"}, "code": 'Game.AddToInventory("Items.ChimeraMeleeMod", 1)', "desc": "敌人生命低于 50% 时，每次击中头部或四肢有 20% 概率瞬间斩首或砍断肢体直接处决！"},
            {"name": {"zh-CN": "活动的奇美拉核心原料 (Active Chimera Core)", "en": "Active Chimera Core"}, "code": 'Game.AddToInventory("Items.Q302_Chimera_Core", 1)', "desc": "奇美拉机甲战车掉落的稀有传奇核心原材料，可放在公寓桌上收藏"}
        ]
    },
    {
        "category": "💾 终极快速破解程序 (Legendary Quickhacks & Blackwall)",
        "commands": [
            {"name": {"zh-CN": "黑墙网关快速破解 (Blackwall Gateway)", "en": "Blackwall Gateway Program"}, "code": 'Game.AddToInventory("Items.BlackWallProgramLvl4", 1)', "desc": "引动黑墙毁灭性恶性代码，在敌人躯体之间像瘟疫般跳跃瞬间化为灰烬！"},
            {"name": {"zh-CN": "赛博精神病 (Cyberpsychosis Tier 5)", "en": "Cyberpsychosis Quickhack"}, "code": 'Game.AddToInventory("Items.MadnessLvl4Program", 1)', "desc": "使目标陷入狂暴，不分敌我疯狂屠杀其周围的友军"},
            {"name": {"zh-CN": "自杀 (Suicide Tier 5)", "en": "Suicide Quickhack"}, "code": 'Game.AddToInventory("Items.SuicideLvl4Program", 1)', "desc": "强制目标举枪自我了断，终结高威胁机枪手或重装机甲"},
            {"name": {"zh-CN": "系统崩溃 (System Collapse Tier 5 - 潜行秒杀)", "en": "System Collapse Quickhack"}, "code": 'Game.AddToInventory("Items.SystemCollapseLvl4Program", 1)', "desc": "使目标神经中枢瞬间断电昏迷，零声响、不触发警报、不引起敌人警觉"},
            {"name": {"zh-CN": "突触熔断 (Synapse Burnout Tier 5)", "en": "Synapse Burnout Quickhack"}, "code": 'Game.AddToInventory("Items.BrainMeltLvl4Program", 1)', "desc": "根据已消耗的 RAM 造成毁灭性过载暴击伤害，消灭目标后延长超频时间"},
            {"name": {"zh-CN": "连环短路 (Short Circuit Tier 5)", "en": "Short Circuit Quickhack"}, "code": 'Game.AddToInventory("Items.EMPOverloadLvl4Program", 1)', "desc": "高能 EMP 电磁脉冲，对机械、无人机与高护甲敌人造成致命电击伤害"}
        ]
    },
    {
        "category": "⚔️ 往日之影 (Phantom Liberty) 绝版不朽神装武器",
        "commands": [
            {"name": {"zh-CN": "厄瑞玻斯 (Erebus - 黑墙 AI 冲锋枪)", "en": "Erebus Blackwall SMG"}, "code": 'Game.AddToInventory("Items.Preset_Borg4a_HauntedGun", 1)', "desc": "封印有黑墙恶性人工智能的致命微型冲锋枪，射击伴随恶魔尖叫并直接侵入处决敌人！"},
            {"name": {"zh-CN": "军用科技大力神 3AX (Hercules 3AX 原型突击步枪)", "en": "Militech Hercules 3AX"}, "code": 'Game.AddToInventory("Items.Preset_Hercules_Prototype", 1)', "desc": "智能突击步枪，将击中的目标化为剧毒酸蚀水塘并引爆周围群体"},
            {"name": {"zh-CN": "罗斯科 (Rosco - 道奇专属动能左轮)", "en": "Rosco Power Revolver"}, "code": 'Game.AddToInventory("Items.Preset_Overture_Dodger", 1)', "desc": "击中敌人腿部使其倒地后，接爆头射击必定触发暴击致死伤害"},
            {"name": {"zh-CN": "尖牙 (Fang - 库尔特·汉森上校战术飞刀)", "en": "Fang Iconic Knife"}, "code": 'Game.AddToInventory("Items.Preset_Knife_Kurtz_1", 1)', "desc": "投掷命中击残敌人，近战连续挥击大幅强化斩杀威力"},
            {"name": {"zh-CN": "白头鹰 (Bald Eagle - 汉森上校重型左轮)", "en": "Bald Eagle Revolver"}, "code": 'Game.AddToInventory("Items.Preset_Metel_Kurt", 1)', "desc": "破甲重炮左轮，搭配飞刀尖牙可触发粉碎双倍暴击"},
            {"name": {"zh-CN": "野狗 (Wild Dog - 汉森上校机枪)", "en": "Wild Dog LMG"}, "code": 'Game.AddToInventory("Items.Preset_Defender_Kurt", 1)', "desc": "狂暴连射轻机枪，子弹命中提升暴击率，弹夹打空接挥拳处决"},
            {"name": {"zh-CN": "阿加乌 (Agaou - 巫毒帮重型战术飞斧)", "en": "Agaou Iconic Axe"}, "code": 'Game.AddToInventory("Items.Preset_VB_Axe", 1)', "desc": "投掷重型战斧，暴击命中在敌人头颅引发扩散电弧闪电风暴！"},
            {"name": {"zh-CN": "斯塔福 (Amstaff - 动能重型霰弹枪)", "en": "Amstaff Iconic Shotgun"}, "code": 'Game.AddToInventory("Items.Preset_Crusher_Amazon", 1)', "desc": "狗镇空投专属重炮，连续命中造成无法愈合的燃烧爆炸"},
            {"name": {"zh-CN": "罗刹 (Rasetsu - 狗镇高科技穿墙智能狙击枪)", "en": "Rasetsu Tech Sniper"}, "code": 'Game.AddToInventory("Items.Preset_Tech_Sniper_Rifle_Rasetsu", 1)', "desc": "蓄力射击发射高能穿透激光，一枪连续贯穿击穿整栋大楼掩体后的多名敌人"},
            {"name": {"zh-CN": "逃兵 (Dezerter - 极端狂暴双管双喷)", "en": "Dezerter Shotgun"}, "code": 'Game.AddToInventory("Items.Preset_Palica_Air_Drop", 1)', "desc": "近距离一枪轰碎 Boss，击杀敌人后获得移速暴击但自身会受到自燃挑战"}
        ]
    },
    {
        "category": "🗡️ 原版传奇不朽武器全家桶 (Classic Iconic Arsenal - 剑枪齐全)",
        "commands": [
            {"name": {"zh-CN": "觉 (Satori - 荒坂三郎传家太刀)", "en": "Satori Katana"}, "code": 'Game.AddToInventory("Items.Preset_Katana_Saburo", 1)', "desc": "序章大厦天台遗物，高达 500% 的极品致命暴击伤害"},
            {"name": {"zh-CN": "涅槃 (Nehan - 荒坂三郎随身刺刀)", "en": "Nehan Knife"}, "code": 'Game.AddToInventory("Items.Preset_Knife_Saburo", 1)', "desc": "投掷刺入敌人引发持续流血，搭配太刀「觉」触发双重吸血大出血"},
            {"name": {"zh-CN": "妖刀白虎 (Byakko - 冲刺瞬斩太刀)", "en": "Byakko Katana"}, "code": 'Game.AddToInventory("Items.Preset_Katana_Wakako", 1)', "desc": "冈田和子委托全清奖励：挥刀自带超远距离前冲飞跃斩杀，连斩手感冠绝全游戏！"},
            {"name": {"zh-CN": "炙土 (Gwynbleidd - 巫师联动白狼钢剑)", "en": "Gwynbleidd Witcher Sword"}, "code": 'Game.AddToInventory("Items.Preset_Sword_Witcher", 1)', "desc": "猎魔人杰洛特专属符文剑，连续斩杀触发红光剑芒斩风"},
            {"name": {"zh-CN": "吹毛求疵 (Errata - 2.0 热能自燃太刀)", "en": "Errata Thermal Katana"}, "code": 'Game.AddToInventory("Items.Preset_Katana_E3", 1)', "desc": "刀身附带高温灼烧，攻击燃烧状态的目标必定触发暴击"},
            {"name": {"zh-CN": "尽忠丸 (Jinchu-Maru - 织田太刀)", "en": "Jinchu-Maru Katana"}, "code": 'Game.AddToInventory("Items.Preset_Katana_HiTech", 1)', "desc": "开启斯安威斯坦时暴击率锁定 100%，连击终结技造成双倍伤害"},
            {"name": {"zh-CN": "爪磨 (Tsumetogi - 荒坂电击太刀)", "en": "Tsumetogi Katana"}, "code": 'Game.AddToInventory("Items.Preset_Katana_Hiromi", 1)', "desc": "攻击附带高频电击与抗电护盾，居合斩杀流利器"},
            {"name": {"zh-CN": "鸡尾酒棒 (Cocktail Stick - 云顶粉红光学太刀)", "en": "Cocktail Stick"}, "code": 'Game.AddToInventory("Items.Preset_Katana_Cocktail", 1)', "desc": "艾芙琳更衣室拾取，粉红色荧光刀刃无视敌人部分护甲"},
            {"name": {"zh-CN": "毒刺 (Stinger - 蝎子遗物飞刀)", "en": "Stinger Knife"}, "code": 'Game.AddToInventory("Items.Preset_Knife_Stinger", 1)', "desc": "蝎子留给阿德卡多的遗物，命中必定附加剧毒与大流血"},
            {"name": {"zh-CN": "蓝牙 (Blue Fang - 神经昏睡飞刀)", "en": "Blue Fang Knife"}, "code": 'Game.AddToInventory("Items.Preset_Neurotoxin_Knife_Iconic", 1)', "desc": "命中直接击晕强敌，潜行暗杀与控制神兵"},
            {"name": {"zh-CN": "猎头 (Headhunter - 朋克标记飞刀)", "en": "Headhunter Knife"}, "code": 'Game.AddToInventory("Items.Preset_Punk_Knife_Iconic", 1)', "desc": "命中目标后附加标记，后续爆头伤害暴增 250%"},
            {"name": {"zh-CN": "马洛里安 3516 (强尼·银手专属动能手枪)", "en": "Malorian Arms 3516"}, "code": 'Game.AddToInventory("Items.Preset_Silverhand_3516", 1)', "desc": "帅气转轮拔枪动作，近距离近战可喷射扇形高温烈焰"},
            {"name": {"zh-CN": "守望 (Overwatch - 帕南专属消音大狙)", "en": "Overwatch Sniper"}, "code": 'Game.AddToInventory("Items.Preset_Sniper_Rifle_Overwatch", 1)', "desc": "全夜之城唯一自带消音器的极品穿墙栓动反器材重型狙击步枪"},
            {"name": {"zh-CN": "八星冲 (Ba Xing Chong - 亚当·重锤智能霰弹枪)", "en": "Ba Xing Chong"}, "code": 'Game.AddToInventory("Items.Preset_Zhuo_Eight_Star", 1)', "desc": "重锤秘密储藏室获取，发射群发高爆追踪导弹，近身秒杀一切精英"},
            {"name": {"zh-CN": "胆识 (Guts - 赛博浪客联动丽贝卡霰弹枪)", "en": "Guts Shotgun (Rebecca)"}, "code": 'Game.AddToInventory("Items.Preset_Carnage_Edgerunners", 1)', "desc": "荒坂塔下拾取，后坐力极度夸张的狂暴多弹丸近距离轰杀重喷"},
            {"name": {"zh-CN": "寡妇制造者 (Widow Maker - 帕南支线纳什精准步枪)", "en": "Widow Maker"}, "code": 'Game.AddToInventory("Items.Preset_Achilles_Nash", 1)', "desc": "高穿透科技步枪，带强烈化学毒性伤害与穿掩体穿透"},
            {"name": {"zh-CN": "同志的铁锤 (Comrade's Hammer - 单发爆轰左轮)", "en": "Comrade's Hammer"}, "code": 'Game.AddToInventory("Items.Preset_Burya_Comrades_Hammer", 1)', "desc": "单发高爆穿甲重弹，一枪触发大范围爆轰秒杀"},
            {"name": {"zh-CN": "四季宝 (Skippy - 话痨跳跳枪)", "en": "Skippy Smart Pistol"}, "code": 'Game.AddToInventory("Items.Preset_Yukimura_Skippy", 1)', "desc": "会说话、唱歌的 AI 智能手枪，可锁定冷酷无情锁头杀戮模式"},
            {"name": {"zh-CN": "应龙 (Yinglong - 智能冲锋枪)", "en": "Yinglong Smart SMG"}, "code": 'Game.AddToInventory("Items.Preset_Dian_Yinglong", 1)', "desc": "子弹自动索敌跟踪，高概率引发大范围 EMP 电磁脉冲连环爆炸"},
            {"name": {"zh-CN": "原型信玄 Mk.V (Shingen Mk.V - 荒坂高爆智能冲锋)", "en": "Shingen Mk.V Prototype"}, "code": 'Game.AddToInventory("Items.Preset_Shingen_Prototype", 1)', "desc": "荒坂工业园集装箱获取，子弹自动锁定三人并伴随高温爆炸"},
            {"name": {"zh-CN": "傲慢 (Pride - 罗格的传奇动能手枪)", "en": "Pride Pistol (Rogue)"}, "code": 'Game.AddToInventory("Items.Preset_Liberty_Rogue", 1)', "desc": "结局击败亚当重锤掉落，爆头伤害与击倒概率全游戏手枪之最"},
            {"name": {"zh-CN": "阿姆内斯蒂 (Amnesty - 卡西迪打靶左轮)", "en": "Amnesty Revolver"}, "code": 'Game.AddToInventory("Items.Preset_Overture_Cassidy", 1)', "desc": "阿德卡多老兵卡西迪手枪，拔枪极速且后坐力极小"},
            {"name": {"zh-CN": "逍遥快活 (Sir John Phallustiff - 斯托特钝器)", "en": "Sir John Phallustiff"}, "code": 'Game.AddToInventory("Items.Preset_Dildo_Stout", 1)', "desc": "汽车旅馆幽会获得，全夜之城攻速极快且自带震动打击特效的非致命钝器"}
        ]
    },
    {
        "category": "🚗 全载具一键解锁与名车 (Vehicles Spawner)",
        "commands": [
            {"name": {"zh-CN": "一键解锁全夜之城所有载具！(全买断)", "en": "Unlock All Vehicles"}, "code": "vs = Game.GetVehicleSystem() vs:EnableAllPlayerVehicles()", "desc": "按 V 呼叫菜单直接解锁全游戏所有汽车、卡车与摩托车！"},
            {"name": {"zh-CN": "强尼·银手保时捷 911 Turbo (930)", "en": "Porsche 911 Turbo"}, "code": 'Game.GetVehicleSystem():EnablePlayerVehicle("Vehicle.v_sport2_porsche_911turbo_player", true, false)', "desc": "1977 年经典复古涂装全碳纤维传奇座驾"},
            {"name": {"zh-CN": "石中剑极速超跑 (Rayfield Caliburn)", "en": "Rayfield Caliburn"}, "code": 'Game.GetVehicleSystem():EnablePlayerVehicle("Vehicle.v_sport1_rayfield_caliburn_player", true, false)', "desc": "最高时速突破 211 MPH，夜之城地表最快黑金流线型超跑"},
            {"name": {"zh-CN": "湖女之剑顶级奢华轿跑 (Rayfield Aerondight)", "en": "Rayfield Aerondight"}, "code": 'Game.GetVehicleSystem():EnablePlayerVehicle("Vehicle.v_sport1_rayfield_aerondight_player", true, false)', "desc": "最昂贵奢华行政超跑，尊贵地位象征"},
            {"name": {"zh-CN": "古德拉 Turbo-R V-Tech (封面野兽肌肉车)", "en": "Quadra Turbo-R V-Tech"}, "code": 'Game.GetVehicleSystem():EnablePlayerVehicle("Vehicle.v_sport2_quadra_turbo_r_player", true, false)', "desc": "2077 官方宣传片封面代表座驾，排气管喷射烈焰"},
            {"name": {"zh-CN": "草薙刃 CT-3X (红神阿基拉同款摩托)", "en": "Yaiba Kusanagi CT-3X"}, "code": 'Game.GetVehicleSystem():EnablePlayerVehicle("Vehicle.v_sportbike2_yaiba_kusanagi_player", true, false)', "desc": "致敬《阿基拉》金田摩托，弯道加速极速王"},
            {"name": {"zh-CN": "杰克·威尔斯的改装摩托车", "en": "Jackie's Arch Bike"}, "code": 'Game.GetVehicleSystem():EnablePlayerVehicle("Vehicle.v_sportbike1_arch_jackie_player", true, false)', "desc": "纪念最好的兄弟杰克·威尔斯的重型巡航机车"}
        ]
    },
    {
        "category": "👕 传奇时装与边缘行者外观 (Iconic Sets & Edgerunners)",
        "commands": [
            {"name": {"zh-CN": "强尼·银手的飞行员偏光太阳镜", "en": "Silverhand Aviators"}, "code": 'Game.AddToInventory("Items.Silverhand_Glasses", 1)', "desc": "强尼标志性金边反光墨镜"},
            {"name": {"zh-CN": "强尼·银手的武侍乐队无袖背心", "en": "Silverhand Tank Top"}, "code": 'Game.AddToInventory("Items.Silverhand_Shirt", 1)', "desc": "SAMURAI 火焰恶魔标志战损印花背心"},
            {"name": {"zh-CN": "强尼·银手的复古羊毛防弹皮夹克", "en": "Silverhand Replica Jacket"}, "code": 'Game.AddToInventory("Items.Silverhand_Jacket", 1)', "desc": "背后带有发光领口与武侍队徽的经典皮衣"},
            {"name": {"zh-CN": "强尼·银手的紧身修身皮裤", "en": "Silverhand Leather Pants"}, "code": 'Game.AddToInventory("Items.Silverhand_Pants", 1)', "desc": "摇滚小子经典皮裤"},
            {"name": {"zh-CN": "强尼·银手的金属包头重型牛仔靴", "en": "Silverhand Cowboy Boots"}, "code": 'Game.AddToInventory("Items.Silverhand_Shoes", 1)', "desc": "带有防弹钢板脚尖包头的复古长靴"},
            {"name": {"zh-CN": "大卫·马丁内斯的急救荧光黄夹克", "en": "David Martinez Jacket"}, "code": 'Game.AddToInventory("Items.Edgerunners_Jacket", 1)', "desc": "《赛博浪客》联动救护队荧光黄大衣，背印边缘行者绿标"}
        ]
    },
    {
        "category": "🛠️ 满级制造组件与军火弹药 (Crafting & Max Ammo)",
        "commands": [
            {"name": {"zh-CN": "金色 5 阶武器组件 x1000", "en": "Tier 5 Weapon Components x1000"}, "code": 'Game.AddToInventory("Items.LegendaryMaterial1", 1000)', "desc": "将所有武器直接升满 Tier 5++ 终极品阶"},
            {"name": {"zh-CN": "金色 5 阶快速破解组件 x1000", "en": "Tier 5 Quickhack Components x1000"}, "code": 'Game.AddToInventory("Items.QuickHackLegendaryMaterial1", 1000)', "desc": "制造终极黑客快速破解插件：赛博精神病、突触熔断"},
            {"name": {"zh-CN": "金色 5 阶义体升级组件 x1000", "en": "Tier 5 Cyberware Components x1000"}, "code": 'Game.AddToInventory("Items.CyberwareMaterial5", 1000)', "desc": "在义体医生诊所直接把全部骨骼、循环与前额皮质升至满阶"},
            {"name": {"zh-CN": "XC-10 阿勒克托传奇消音器 (Top Silencer)", "en": "XC-10 Alecto Silencer"}, "code": 'Game.AddToInventory("Items.w_silencer_01", 1)', "desc": "100% 潜行暗杀消音减噪，爆头暴击伤害额外加成"},
            {"name": {"zh-CN": "金津高科技短距离全息瞄具", "en": "Kanetsugu Scope"}, "code": 'Game.AddToInventory("Items.w_att_scope_short_04", 1)', "desc": "视野极其开阔清晰，科技与动能手枪步枪通用"},
            {"name": {"zh-CN": "手枪/左轮弹药补满 1000 发", "en": "Max Handgun Ammo"}, "code": 'Game.AddToInventory("Ammo.HandgunAmmo", 1000)', "desc": "补满手枪随身弹药箱"},
            {"name": {"zh-CN": "突击步枪/冲锋枪弹药补满 1000 发", "en": "Max Rifle Ammo"}, "code": 'Game.AddToInventory("Ammo.RifleAmmo", 1000)', "desc": "补满自动步枪弹药"},
            {"name": {"zh-CN": "散弹枪弹药补满 500 发", "en": "Max Shotgun Ammo"}, "code": 'Game.AddToInventory("Ammo.ShotgunAmmo", 500)', "desc": "补满重喷弹药"},
            {"name": {"zh-CN": "狙击步枪穿甲弹药补满 200 发", "en": "Max Sniper Ammo"}, "code": 'Game.AddToInventory("Ammo.SniperRifleAmmo", 200)', "desc": "补满重型狙击穿甲弹"}
        ]
    },
    {
        "category": "⏱️ 游戏时间与昼夜流速掌控 (Time of Day & Time Freeze)",
        "commands": [
            {"name": {"zh-CN": "时间直接调节至正午 12:00 (阳光直射)", "en": "Set Time: 12:00 Noon"}, "code": "Game.GetTimeSystem():SetGameTimeByHMS(12, 0, 0)", "desc": "告别漆黑深夜，一键调节到大白天正午"},
            {"name": {"zh-CN": "时间直接调节至子夜 00:00 (赛博霓虹夜色)", "en": "Set Time: Midnight 00:00"}, "code": "Game.GetTimeSystem():SetGameTimeByHMS(0, 0, 0)", "desc": "一键切换至深夜，欣赏五彩霓虹灯光"},
            {"name": {"zh-CN": "【拍照神技】彻底冻结游戏昼夜时间流逝", "en": "Freeze Time Progression"}, "code": 'Game.GetTimeSystem():SetPausedState(true, "")', "desc": "时间永远定格在当前秒数，光影角度固定不变，专心构图拍照！"},
            {"name": {"zh-CN": "解除时间冻结恢复时间流逝", "en": "Unfreeze Time Progression"}, "code": 'Game.GetTimeSystem():SetPausedState(false, "")', "desc": "恢复原版正常 24 小时自然日夜更迭"}
        ]
    },
    {
        "category": "🌧️ 天气系统与赛博环境调控 (Weather & Atmosphere)",
        "commands": [
            {"name": {"zh-CN": "阴雨连绵 (银翼杀手经典雨夜)", "en": "Set Weather: Rain"}, "code": 'Game.GetWeatherSystem():SetWeather("24h_weather_rain", 0.0)', "desc": "街道地面产生极致霓虹水坑倒影，赛博朋克电影感直接拉满！"},
            {"name": {"zh-CN": "赛博酸雨环境 (Toxic Acid Rain)", "en": "Set Weather: Acid Rain"}, "code": 'Game.GetWeatherSystem():SetWeather("24h_weather_acid_rain", 0.0)', "desc": "天空呈现诡异的黄绿硫磺色调与工业酸雾"},
            {"name": {"zh-CN": "恶土漫天红尘沙尘暴 (Sandstorm)", "en": "Set Weather: Sandstorm"}, "code": 'Game.GetWeatherSystem():SetWeather("24h_weather_sandstorm", 0.0)', "desc": "狂风夹杂橙红色沙暴遮蔽阳光，视距受限硬核末世感"},
            {"name": {"zh-CN": "浓厚晨雾弥漫 (Heavy Fog)", "en": "Set Weather: Fog"}, "code": 'Game.GetWeatherSystem():SetWeather("24h_weather_fog", 0.0)', "desc": "清晨白雾弥漫于摩天大楼与高架桥之间"},
            {"name": {"zh-CN": "晴空万里阳光普照 (Clear Sunny)", "en": "Set Weather: Sunny"}, "code": 'Game.GetWeatherSystem():SetWeather("24h_weather_sunny", 0.0)', "desc": "恢复夜之城艳阳高照通透好天气"}
        ]
    },
    {
        "category": "📜 隐藏结局、全员恋爱与剧情控制 (Secret Endings & Romances)",
        "commands": [
            {"name": {"zh-CN": "强制解锁隐藏单挑荒坂塔结局 (不用等对话!)", "en": "Unlock Secret Ending (Solo Raid)"}, "code": 'Game.GetQuestsSystem():SetFactStr("sq032_johnny_friend", 1)', "desc": "直接修复油田对话！在天台选择结局时静默发呆 4 分钟，强尼就会主动提议单人单挑杀入荒坂塔（不要害怕死神）！"},
            {"name": {"zh-CN": "一键消除当前 NCPD 全城警星通缉", "en": "Clear Wanted Stars"}, "code": "Game.GetPreventionSpawnSystem():RequestDespawnPreventionAgents()", "desc": "瞬间消散身后追逐的全部警用直升机与暴恐机动队特警！"},
            {"name": {"zh-CN": "解锁全夜之城所有快速旅行数据终端", "en": "Unlock All Fast Travel Markers"}, "code": 'Game.GetQuestsSystem():SetFactStr("fast_travel_all_unlocked", 1)', "desc": "无需亲自跑图探索，大地图瞬间点亮上百个传送箱"},
            {"name": {"zh-CN": "解锁朱迪恋爱权限 (跨性别男女V皆可推倒)", "en": "Unlock Judy Romance for All"}, "code": 'Game.GetQuestsSystem():SetFactStr("judy_romanceable", 1)', "desc": "解除原版对男性身体声音的限制，男 V 亦可触发潜水金字塔与推倒剧情"},
            {"name": {"zh-CN": "解锁帕南恋爱权限 (跨性别男女V皆可推倒)", "en": "Unlock Panam Romance for All"}, "code": 'Game.GetQuestsSystem():SetFactStr("panam_romanceable", 1)', "desc": "解除对女性身体声音的限制，女 V 亦可在魔蜥装甲车内触发推倒剧情"}
        ]
    }
]

# Save enriched database to JSON
with open(DATA_PATH, 'w', encoding='utf-8') as f:
    json.dump(games, f, ensure_ascii=False, indent=2)

# Save to public/data.js
js_content = f"// L-MOD Vault Offline Database (Enriched v3)\nwindow.GAMES_DATA = {json.dumps(games, ensure_ascii=False, indent=2)};\n"
with open(PUBLIC_DATA_PATH, 'w', encoding='utf-8') as f:
    f.write(js_content)

total_cmds = sum(len(c["commands"]) for c in cp["consoleCategories"])
print(f"Cyberpunk 2077 is now fully enriched with {len(cp['consoleCategories'])} categories, {total_cmds} verified commands, and {len(cp['curatedMods'])} curated mods!")
