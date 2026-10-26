import json
import os

JSON_PATH = '/Users/xiaolu/Desktop/work/l-mod-portal/src/data/games_top100.json'
JS_PATH = '/Users/xiaolu/Desktop/work/l-mod-portal/public/data.js'

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    games = json.load(f)

# Build deep data for black-myth-wukong
wukong_categories = [
    {
        "category": "👑 核心生存与无敌机制 (God Mode & Core Survival)",
        "commands": [
            {
                "id": "bmw_slomo_03",
                "name": {"zh-CN": "开启全场景 0.3 倍速慢动作 (识破防反神技)", "en": "Slomo 0.3x (Bullet Time)"},
                "syntax_type": "ue_console",
                "code": "slomo 0.3",
                "desc": "全场景 0.3 倍速慢动作流速，轻松看清所有妖王 Boss 招式前摇，从容练习识破与定身打法！",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS"
            },
            {
                "id": "bmw_slomo_10",
                "name": {"zh-CN": "恢复正常 1.0 倍游戏流速", "en": "Normal Game Speed (1.0x)"},
                "syntax_type": "ue_console",
                "code": "slomo 1.0",
                "desc": "恢复原汁原味硬核动作打击感与标准世界流速。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS"
            },
            {
                "id": "bmw_slomo_01",
                "name": {"zh-CN": "极致 0.1 倍微距慢动作 (拆解动作帧与拍照)", "en": "Ultra Slow-Mo 0.1x"},
                "syntax_type": "ue_console",
                "code": "slomo 0.1",
                "desc": "以近乎静止的微速观察棍势挥舞轨迹、法术爆裂粒子特效与高精度特写拍照打光。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS"
            },
            {
                "id": "bmw_slomo_20",
                "name": {"zh-CN": "极速 2.0 倍流速狂奔 (跑图扫荡神器)", "en": "Fast Forward 2.0x"},
                "syntax_type": "ue_console",
                "code": "slomo 2.0",
                "desc": "2 倍速狂奔移动，大幅缩减在空旷山道与林海间来回奔波跑图的时间。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS"
            },
            {
                "id": "bmw_teleport",
                "name": {"zh-CN": "准星朝向瞬移闪现 (穿透空气墙与障碍)", "en": "Teleport Forward"},
                "syntax_type": "ue_console",
                "code": "teleport",
                "desc": "沿当前准星正前方瞬移穿透隐形空气墙或跨越深渊绝壁，探索隐藏山洞与绝壁捷径。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS"
            },
            {
                "id": "bmw_toggledebugcamera",
                "name": {"zh-CN": "虚幻5自由视角飞行摄像机 (360° 无死角摄影)", "en": "Free Fly Camera"},
                "syntax_type": "ue_console",
                "code": "toggledebugcamera",
                "desc": "脱离角色控制进入 360 度自由悬浮摄像机视角，穿墙透视妖王埋伏与拍摄史诗级战斗大片。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS"
            },
            {
                "id": "bmw_showhud_0",
                "name": {"zh-CN": "一键隐藏全场景战斗 HUD 界面 (纯净电影级沉浸)", "en": "Hide All HUD"},
                "syntax_type": "ue_console",
                "code": "ShowHUD 0",
                "desc": "隐藏血条、架势条、葫芦图标与技能栏，获得极致纯净的 4K 电影级画面录屏体验。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS"
            },
            {
                "id": "bmw_showhud_1",
                "name": {"zh-CN": "恢复显示全场景战斗 HUD 界面", "en": "Show HUD"},
                "syntax_type": "ue_console",
                "code": "ShowHUD 1",
                "desc": "恢复显示默认战斗界面、血量指示与技能冷却状态。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS"
            }
        ]
    },
    {
        "category": "⏱️ 动作慢动作子弹时间与招式防反教学 (Bullet Time & Stance Mastery)",
        "commands": [
            {
                "id": "bmw_addexp_sparks",
                "name": {"zh-CN": "增加 100,000 灵光技能点 (Sparks 技能点瞬间全满)", "en": "Add 100,000 Sparks (Skill Points)"},
                "syntax_type": "gm_command",
                "code": "addexp 100000",
                "desc": "直接注入 10 万灵光经验点数，瞬间点满劈棍、立棍、戳棍三大流派全套武艺与毫毛神通！",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_addtalentpoint_50",
                "name": {"zh-CN": "增加 50 点武艺专精修炼点 (解锁四阶蓄力棍势)", "en": "Add 50 Cultivation Points"},
                "syntax_type": "gm_command",
                "code": "addtalentpoint 50",
                "desc": "立即获得 50 点修炼点数，轻松解锁第四段棍势爆发、识破防反判定延长与奔跑蓄力等核心被动。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_alltalent",
                "name": {"zh-CN": "一键激活天命人全宗门武艺与神通天赋树", "en": "Unlock All Talents"},
                "syntax_type": "gm_command",
                "code": "alltalent",
                "desc": "直接解锁激活整张技能天赋图谱，省去数十小时繁琐刷经验过程，开局即达巅峰大圣战斗力！",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_allspell",
                "name": {"zh-CN": "一键解锁全法术绝技 (定身/散气/铁臂/分身)", "en": "Unlock All Spells"},
                "syntax_type": "gm_command",
                "code": "allspell",
                "desc": "解锁奇术·定身法、身法·聚形散气、身法·铜头铁臂、毫毛·身外身法与禁字法等全门派神技。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_setspell_ding",
                "name": {"zh-CN": "快捷装备核心奇术：定身法", "en": "Equip Immobilize Spell"},
                "syntax_type": "gm_command",
                "code": "setspell 1",
                "desc": "一键装配齐天大圣成名奇术定身法，强制凝固敌人与 Boss 动作任由输出破防。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_setspell_juxing",
                "name": {"zh-CN": "快捷装备核心身法：聚形散气", "en": "Equip Cloud Step Spell"},
                "syntax_type": "gm_command",
                "code": "setspell 2",
                "desc": "一键装配散气脱身神技，留下白雾假身迷惑对手并进入隐身破隐暴击状态。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_setspell_tongtou",
                "name": {"zh-CN": "快捷装备核心身法：铜头铁臂", "en": "Equip Rock Solid Spell"},
                "syntax_type": "gm_command",
                "code": "setspell 3",
                "desc": "一键装配金刚不坏弹反神技，完美招架敌方重击并产生强硬直震退对手。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_setspell_shenwai",
                "name": {"zh-CN": "快捷装备核心毫毛：身外身法", "en": "Equip A Pluck of Many Spell"},
                "syntax_type": "gm_command",
                "code": "setspell 4",
                "desc": "一键装配群攻分身绝技，拔出猴毛召唤数十个分身小猴协同疯狂围殴妖王！",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            }
        ]
    },
    {
        "category": "🐵 54 大精魄化身与变身神技 (Spirits Transformations & Traits)",
        "commands": [
            {
                "id": "bmw_allsoulskill",
                "name": {"zh-CN": "一键解锁全图鉴 54 种妖王妖魔精魄技能", "en": "Unlock All 54 Spirits Skills"},
                "syntax_type": "gm_command",
                "code": "allsoulskill",
                "desc": "一次性将黑神话全周期 54 种怪物精魄全部解锁入库，自由切换大头幽魂、火狼广智与不能拳法！",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_soulskill_youhun",
                "name": {"zh-CN": "获得特品精魄：幽魂 (大头头槌巨额冲击波)", "en": "Grant Spirit: Wandering Wight"},
                "syntax_type": "gm_command",
                "code": "soulskill 1001",
                "desc": "变身大头幽魂释放威力惊人的巨力头槌轰击，被动获得大量额外物理防御力加成。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_soulskill_guangzhi",
                "name": {"zh-CN": "获得特品精魄：广智 (变身火狼双头赤潮连击)", "en": "Grant Spirit: Guangzhi"},
                "syntax_type": "gm_command",
                "code": "soulskill 1002",
                "desc": "变身双头火狼手持赤潮双头枪，行云流水挥斩并附加高额火焚异常状态伤害。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_soulskill_boligelang",
                "name": {"zh-CN": "获得特品精魄：波里个浪 (变身雷蛙跳跃电击)", "en": "Grant Spirit: Baw-Li-Guhh-Lang"},
                "syntax_type": "gm_command",
                "code": "soulskill 1003",
                "desc": "化身巨蛙长舌弹射并跃起释放全屏雷属性闪电震荡波，附带麻痹感电削弱。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_soulskill_buneng",
                "name": {"zh-CN": "获得特品精魄：不能 (金刚不坏近战拳击连打)", "en": "Grant Spirit: Non-Able"},
                "syntax_type": "gm_command",
                "code": "soulskill 1004",
                "desc": "双手反绑变身苦行僧，以极速近身刚猛重拳连环轰击，大幅提升角色近战攻击与暴击率。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_soulskill_dilang",
                "name": {"zh-CN": "获得特品精魄：地狼 (潜地突袭与棍势高速充能)", "en": "Grant Spirit: Earth Wolf"},
                "syntax_type": "gm_command",
                "code": "soulskill 1005",
                "desc": "潜入地面向前极速突刺撞翻敌方防线，每次有效命中都将大幅恢复自身棍势蓄力。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_soulskill_huxianfeng",
                "name": {"zh-CN": "获得特品精魄：虎先锋 (猛虎扑食与血煞刀气)", "en": "Grant Spirit: Tiger Vanguard"},
                "syntax_type": "gm_command",
                "code": "soulskill 1006",
                "desc": "化身血池虎煞跃起怒吼扑咬，挥舞巨刃斩出血煞剑气，被动永久提高暴击伤害倍率。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_soulskill_chiyanlong",
                "name": {"zh-CN": "获得特品精魄：赤髯龙 (撼地轰雷与天雷附魔)", "en": "Grant Spirit: Red Loong"},
                "syntax_type": "gm_command",
                "code": "soulskill 1007",
                "desc": "引动九天神雷缠绕棍身，重棍砸地引爆大范围金色雷暴，对弱雷妖王造成毁灭级破韧伤害。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            }
        ]
    },
    {
        "category": "🗡️ 传奇神兵与大圣全套套装 (Legendary Weapons & Armors)",
        "commands": [
            {
                "id": "bmw_allweapon",
                "name": {"zh-CN": "一键解锁全图鉴神珍武器 (金箍棒/三尖枪/通天)", "en": "Unlock All Weapons"},
                "syntax_type": "gm_command",
                "code": "allweapon",
                "desc": "一次性解锁全部神珍级与特品级武器，无需击杀妖王或二周目苦等锻造材料即可畅享全部神兵！",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_allequip",
                "name": {"zh-CN": "一键解锁全套神珍披挂防具 (大圣套/牛魔套/行者套)", "en": "Unlock All Armors & Sets"},
                "syntax_type": "gm_command",
                "code": "allequip",
                "desc": "一键获得游戏内所有头冠、衣甲、臂甲与行履，集齐全套齐天大圣真身神装。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_allarmortotop",
                "name": {"zh-CN": "一键将已持有防具全部升至满级强化上限", "en": "Max Out All Equipped Armors"},
                "syntax_type": "gm_command",
                "code": "allarmortotop",
                "desc": "自动将角色背囊中所有披挂防具一键拉升至最高品阶（神珍），属性防御与套装词条全部拉满。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_item_jingu_staff",
                "name": {"zh-CN": "直接获得神珍武器：如意金箍棒", "en": "Add Weapon: Jingubang"},
                "syntax_type": "gm_command",
                "code": "additem 3001 1",
                "desc": "齐天大圣本命神珍神兵，攻击力 135、暴击率 6%，永久维持第四段定海神针棍势蓄力不随时间消退！",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_item_erlang_spear",
                "name": {"zh-CN": "直接获得神珍武器：三尖两刃枪", "en": "Add Weapon: Tri-Point Spear"},
                "syntax_type": "gm_command",
                "code": "additem 3002 1",
                "desc": "显圣真君二郎神绝世神兵，攻击 135，独有戳棍飞剑机制，识破后可召唤无尽神剑穿刺暴击破防！",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_item_kungun_tongtian",
                "name": {"zh-CN": "直接获得神珍武器：昆棍·通天", "en": "Add Weapon: Adept Spine Staff"},
                "syntax_type": "gm_command",
                "code": "additem 3003 1",
                "desc": "顶级神珍昆棍，蓄力劈棍重击命中可按比例吸血回复自身生命值，站桩输出续航神器。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_armor_zijin_crown",
                "name": {"zh-CN": "直接获得神珍防具：凤翅紫金冠 (大圣头部)", "en": "Add Armor: Golden Feng-Tail Crown"},
                "syntax_type": "gm_command",
                "code": "additem 3004 1",
                "desc": "齐天大圣神珍套装头部部件，大幅增加气力上限与定身法持续时间。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_armor_suozi_armor",
                "name": {"zh-CN": "直接获得神珍防具：锁子黄金甲 (大圣胸部)", "en": "Add Armor: Gold Suozi Armor"},
                "syntax_type": "gm_command",
                "code": "additem 3005 1",
                "desc": "齐天大圣神珍套装胸部部件，提供极为惊人的物理护甲与气力极速回复效果。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_armor_feilong_bracer",
                "name": {"zh-CN": "直接获得神珍防具：点翠飞龙釬 (大圣臂部)", "en": "Add Armor: Dian-Cui Loong Armlets"},
                "syntax_type": "gm_command",
                "code": "additem 3006 1",
                "desc": "齐天大圣神珍套装臂甲部件，强化重棍出招威势并大幅提高暴击率与攻击力。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_armor_buyun_boots",
                "name": {"zh-CN": "直接获得神珍防具：藕丝步云履 (大圣腿部)", "en": "Add Armor: Lotus Silk Cloud Walkers"},
                "syntax_type": "gm_command",
                "code": "additem 3007 1",
                "desc": "齐天大圣神珍套装步云履，大幅加快闪避移动速度并降低奔跑气力消耗。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            }
        ]
    },
    {
        "category": "🏺 镇宗法宝、顶级葫芦与酒食配方 (Vessels, Gourds & Drinks)",
        "commands": [
            {
                "id": "bmw_allhulu",
                "name": {"zh-CN": "一键解锁全图鉴顶级葫芦 (上清/五鬼/乾坤宝葫)", "en": "Unlock All Gourds"},
                "syntax_type": "gm_command",
                "code": "allhulu",
                "desc": "一键集齐上清宝葫芦、五鬼宝葫芦、彩玉葫芦等全套神品葫芦，尽享多重回血被动！",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_allwine",
                "name": {"zh-CN": "一键解锁全部琼浆美酒与泡酒物", "en": "Unlock All Drinks & Soaks"},
                "syntax_type": "gm_command",
                "code": "allwine",
                "desc": "解锁龙膏、千日醉、松醪酒以及铜丸、铁弹、紫纹缃核等全套顶级泡酒材料，自由定制饮酒效果。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_luojia_vine",
                "name": {"zh-CN": "获得 50 个落伽香藤 (葫芦饮用次数升至满级)", "en": "Add 50 Luojia Fragrant Vines"},
                "syntax_type": "gm_command",
                "code": "additem 1998 50",
                "desc": "极其珍贵的申猴酿造素材，直接将葫芦盛酒饮用次数强化升满至 10 次上限！",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_xingjiu_dan",
                "name": {"zh-CN": "获得 50 个醒酒胆 (品酒酿造最高阶突破素材)", "en": "Add 50 Awaken Wine Worms"},
                "syntax_type": "gm_command",
                "code": "additem 1999 50",
                "desc": "极品酿酒素材，大幅增强每一次饮酒的回血量并延长伴随的攻击/霸体增益时间。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_wine_longgao",
                "name": {"zh-CN": "获得特品药酒：龙膏 (大量回血并强化下次攻击)", "en": "Add Drink: Loong Balm"},
                "syntax_type": "gm_command",
                "code": "additem 2012 1",
                "desc": "特品药酒，饮用瞬间回复大量生命值，并赋予下一次重棍打击毁灭性的攻击力爆发加成！",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_vessel_bihuozhao",
                "name": {"zh-CN": "获得第一回法宝：辟火罩 (免疫灼烧并吸火回气)", "en": "Add Vessel: Fireproof Mantle"},
                "syntax_type": "gm_command",
                "code": "additem 4001 1",
                "desc": "第一回隐藏黑风大圣法宝，激活后免疫一切烈火灼烧环境，吸收火属性伤害并快速回复气力！",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_vessel_dingfengzhu",
                "name": {"zh-CN": "获得第二回法宝：定风珠 (克制风沙并赋予绝对霸体)", "en": "Add Vessel: Wind Tamer"},
                "syntax_type": "gm_command",
                "code": "additem 4002 1",
                "desc": "第二回黄风岭法宝，施展瞬间镇压漫天黄沙狂风，赋予天命人超级霸体与巨额物理减伤。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_vessel_xiuhuazhen",
                "name": {"zh-CN": "获得第四回法宝：绣花针 (破除金光领域与自主追踪)", "en": "Add Vessel: Weaver's Needle"},
                "syntax_type": "gm_command",
                "code": "additem 4003 1",
                "desc": "第四回紫云山法宝，专门破除百眼魔君金光二阶段毒域，飞针对准敌人弱点持续自主高速穿刺。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_vessel_bajiaoshan",
                "name": {"zh-CN": "获得第五回法宝：芭蕉扇 (召唤龙卷风瞬间打空 Boss 韧性)", "en": "Add Vessel: Plantain Fan"},
                "syntax_type": "gm_command",
                "code": "additem 4004 1",
                "desc": "第五回铁扇公主至尊法宝，一扇挥出巨大旋风将全场敌人卷至空中，瞬间彻底打空 Boss 韧性破防！",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            }
        ]
    },
    {
        "category": "💊 灵丹妙药、珍稀材料与灵蕴财富 (Elixirs, Materials & Will)",
        "commands": [
            {
                "id": "bmw_currency_will",
                "name": {"zh-CN": "增加 1,000,000 灵蕴货币 (Will 财富自由)", "en": "Add 1,000,000 Will (Currency)"},
                "syntax_type": "gm_command",
                "code": "additem 1002 1000000",
                "desc": "直接注入 100 万灵蕴金钱，全土地庙所有商品、打造图纸与稀有草药全部一键买断！",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_allitem",
                "name": {"zh-CN": "一键获得全部锻造材料、丹药与基础消耗品", "en": "Unlock All Materials & Items"},
                "syntax_type": "gm_command",
                "code": "allitem",
                "desc": "注入玲珑内丹、金树玉髓、精铁矿砂等全部强化素材，免去繁琐刷怪掉落流程！",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_allattritem",
                "name": {"zh-CN": "一键获得全部永久属性加成天上仙丹", "en": "Unlock All Attribute Boost Elixirs"},
                "syntax_type": "gm_command",
                "code": "allattritem",
                "desc": "一次性获得生命、气力、法力、攻击力、防御力与寒冻/火焚/毒瘴/雷蛰抗性的永久加成金丹！",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_allrecipe",
                "name": {"zh-CN": "一键解锁全丹方与装备锻造配方", "en": "Unlock All Crafting Recipes"},
                "syntax_type": "gm_command",
                "code": "allrecipe",
                "desc": "掌握六丁六甲全套神级丹方与隐藏武器锻造配方，在任意土地庙皆可自由炼造神品。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_allseeds",
                "name": {"zh-CN": "一键集齐全部辰龙草药种子 (开启百草园自动种植)", "en": "Unlock All Plant Seeds"},
                "syntax_type": "gm_command",
                "code": "allseeds",
                "desc": "集齐全图全部草药种子交由如意画轴辰龙打理，每隔一段时间即可收获海量珍稀炼丹药材。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_elixir_jiuzhuan",
                "name": {"zh-CN": "获得 99 颗九转金丹 (永久提升生命上限)", "en": "Add 99 Nine-Turn Pellets"},
                "syntax_type": "gm_command",
                "code": "additem 2211 99",
                "desc": "天上极品仙丹，服用一颗即可永久拔高角色生命值上限，服用 99 颗达成血牛不死之身！",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_elixir_taiyi",
                "name": {"zh-CN": "获得 99 颗太乙紫金丹 (永久提升法力上限)", "en": "Add 99 Taiyi Purple Pills"},
                "syntax_type": "gm_command",
                "code": "additem 2221 99",
                "desc": "太乙至宝仙丹，服用大幅提升法力 MP 上限，定身法与身外身法实现无限频繁施展！",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_elixir_sanqing",
                "name": {"zh-CN": "获得 99 颗三清令宝丹 (永久提升气力上限)", "en": "Add 99 Sanqing Stamina Pills"},
                "syntax_type": "gm_command",
                "code": "additem 2230 99",
                "desc": "永久提升天命人体魄气力上限，奔跑、连续闪避翻滚与重蓄力不再受制于体力枯竭。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_powder_bihuo",
                "name": {"zh-CN": "获得 99 份避火丹 (解除火焚抗性)", "en": "Add 99 Body-Warming Powders"},
                "syntax_type": "gm_command",
                "code": "additem 2204 99",
                "desc": "瞬间消解身体燃烧焦热状态，并在一定时间内大幅提高火焚耐性抗性。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_powder_bidu",
                "name": {"zh-CN": "获得 99 份避毒丹 (解除剧毒异常)", "en": "Add 99 Antimiasma Powders"},
                "syntax_type": "gm_command",
                "code": "additem 2205 99",
                "desc": "针对盘丝岭百足百眼剧毒环境神丹，瞬间清除中毒槽并提高抗毒防御力。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_powder_bilei",
                "name": {"zh-CN": "获得 99 份避雷丹 (消除雷蛰感电状态)", "en": "Add 99 Shock-Quelling Powders"},
                "syntax_type": "gm_command",
                "code": "additem 2206 99",
                "desc": "消除小西天亢金龙雷电感电减益，防止受到额外高额雷属性雷暴易伤。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            }
        ]
    },
    {
        "category": "🗺️ 全土地庙打坐点全开与全章回传送 (World Exploration & Shrines)",
        "commands": [
            {
                "id": "bmw_allmedition_1",
                "name": {"zh-CN": "一键点亮全地图所有土地庙与打坐蒲团", "en": "Unlock All Shrines & Meditation Spots"},
                "syntax_type": "gm_command",
                "code": "allmedition 1",
                "desc": "直接点亮整部游戏 100% 土地庙与野外打坐蒲团，瞬间解锁自由缩地传送与蒲团灵光加成！",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_allmap",
                "name": {"zh-CN": "一键解锁全部地图全景图卷", "en": "Unlock Full World Map"},
                "syntax_type": "gm_command",
                "code": "allmap",
                "desc": "驱散所有章回山川战争迷雾，完全点亮六大回目全部山势脉络与隐藏道观。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_refreshallshop",
                "name": {"zh-CN": "一键刷新并解锁全图所有土地庙及隐藏 NPC 货架", "en": "Unlock & Refresh All NPC Shops"},
                "syntax_type": "gm_command",
                "code": "refreshallshop",
                "desc": "重置并补满全土地庙货架库存，提前解锁寅虎打铁、申猴酿酒与石中人隐秘货架！",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_setchapter_10",
                "name": {"zh-CN": "剧情章回跳转：第一回 黑风山 (火照黑云)", "en": "Warp to Chapter 1: Black Wind Mountain"},
                "syntax_type": "gm_command",
                "code": "setchapter 10",
                "desc": "战役流程直接跳转至第一回苍狼林与黑风大王战役。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_setchapter_20",
                "name": {"zh-CN": "剧情章回跳转：第二回 黄风岭 (风起黄昏)", "en": "Warp to Chapter 2: Yellow Wind Ridge"},
                "syntax_type": "gm_command",
                "code": "setchapter 20",
                "desc": "战役流程直接跳转至第二回卧虎寺与黄风大圣沙门关隘。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_setchapter_30",
                "name": {"zh-CN": "剧情章回跳转：第三回 小西天 (夜生白露)", "en": "Warp to Chapter 3: The New West"},
                "syntax_type": "gm_command",
                "code": "setchapter 30",
                "desc": "战役流程直接跳转至第三回亢金龙、浮屠牢与黄眉雷音古刹。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_setchapter_40",
                "name": {"zh-CN": "剧情章回跳转：第四回 盘丝岭 (曲度紫鸳)", "en": "Warp to Chapter 4: The Webbed Hollow"},
                "syntax_type": "gm_command",
                "code": "setchapter 40",
                "desc": "战役流程直接跳转至第四回盘丝洞幽径、紫云山与百眼魔君巢穴。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_setchapter_50",
                "name": {"zh-CN": "剧情章回跳转：第五回 火焰山 (日落红尘)", "en": "Warp to Chapter 5: Flaming Mountains"},
                "syntax_type": "gm_command",
                "code": "setchapter 50",
                "desc": "战役流程直接跳转至第五回翠云草庐、壁画洞天与红孩儿牛魔老巢。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_setchapter_60",
                "name": {"zh-CN": "剧情章回跳转：第六回 花果山 (未竟之章与水帘洞)", "en": "Warp to Chapter 6: Mount Huaguo"},
                "syntax_type": "gm_command",
                "code": "setchapter 60",
                "desc": "战役流程直接跳转至终章花果山筋斗云腾飞天地与大圣残躯水帘洞终极对决！",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            }
        ]
    },
    {
        "category": "📜 影神图全图鉴、六根遗物与全成就解锁 (Bestiary, Relics & Achievements)",
        "commands": [
            {
                "id": "bmw_allcard",
                "name": {"zh-CN": "一键点亮影神图全部头目、妖王与小妖志异", "en": "Unlock Full Bestiary (Cards)"},
                "syntax_type": "gm_command",
                "code": "allcard",
                "desc": "直接集齐全图鉴全部头目、妖王、人物与精怪图录，阅读每一个妖怪凄美生平志异！",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_alllegacy",
                "name": {"zh-CN": "一键获得齐天大圣六根遗物 (眼耳鼻舌身意大圆满)", "en": "Unlock All Great Sage Relics"},
                "syntax_type": "gm_command",
                "code": "alllegacy",
                "desc": "直接吸收眼看喜、耳听怒、鼻嗅爱、舌尝思、身本忧、意见欲六大遗物，瞬间激活全部被动羁绊神能！",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_allsurprise",
                "name": {"zh-CN": "一键解锁全部隐藏场景交互彩蛋", "en": "Unlock All Easter Eggs"},
                "syntax_type": "gm_command",
                "code": "allsurprise",
                "desc": "触发全地图所有支线隐秘彩蛋与神像隐藏交互剧情。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_allmuseum",
                "name": {"zh-CN": "开启游戏内全景博物馆与高精模型鉴赏", "en": "Unlock 3D Character Museum"},
                "syntax_type": "gm_command",
                "code": "allmuseum",
                "desc": "在游戏内随时开启角色博物馆展厅，近距离鉴赏每一位仙魔神佛超高清材质与骨骼动画。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            },
            {
                "id": "bmw_allachievements",
                "name": {"zh-CN": "一键解锁全部 81 个 Steam / Epic 官方成就", "en": "Unlock All 81 Achievements"},
                "syntax_type": "gm_command",
                "code": "allachievements",
                "desc": "九九八十一难功德圆满，秒破全收集门槛获得 Steam 黄金全通关奖杯徽章！",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS / WukongGM"
            }
        ]
    },
    {
        "category": "🎥 虚幻5引擎镜头画质与截图打光调优 (UE5 Camera & Graphics Engine)",
        "commands": [
            {
                "id": "bmw_r_sharpen",
                "name": {"zh-CN": "开启毛发与光影锐化 (增强金箍棒金属质感)", "en": "Sharpen Details (1.5x)"},
                "syntax_type": "ue_console",
                "code": "r.Tonemapper.Sharpen 1.5",
                "desc": "显著增强角色猴毛根根分明的细节与锁子黄金甲金属纹理反射，消除抗锯齿涂抹感。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS"
            },
            {
                "id": "bmw_r_dof",
                "name": {"zh-CN": "关闭背景景深模糊 (获得超远全景清晰视野)", "en": "Disable Depth of Field"},
                "syntax_type": "ue_console",
                "code": "r.DepthOfFieldQuality 0",
                "desc": "完全关闭背景虚化景深，远景山川道观与隐匿的隐藏宝箱尽收眼底一清二楚。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS"
            },
            {
                "id": "bmw_r_motionblur",
                "name": {"zh-CN": "关闭动态模糊 (解决快速转头视角头晕)", "en": "Disable Motion Blur"},
                "syntax_type": "ue_console",
                "code": "r.MotionBlurQuality 0",
                "desc": "彻底消除转动视角或急速冲刺时的画面拖影涂抹，彻底告别 3D 眩晕不适感。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS"
            },
            {
                "id": "bmw_r_volumetricfog",
                "name": {"zh-CN": "关闭体积雾 (穿透盘丝洞与黄风浓雾障碍)", "en": "Disable Volumetric Fog"},
                "syntax_type": "ue_console",
                "code": "r.VolumetricFog 0",
                "desc": "消除盘丝洞幽深坑道与黄风大圣沙尘浓雾，大幅提升画面通透度与迷宫辨识度。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS"
            },
            {
                "id": "bmw_r_foliage_discard",
                "name": {"zh-CN": "降低高负载密林显存占用 (显著改善掉帧卡顿)", "en": "Optimize Foliage Memory"},
                "syntax_type": "ue_console",
                "code": "foliage.DiscardDataOnLoad 1",
                "desc": "释放大面积植被占用显存，针对黑风山与花果山复杂植被丛林场景提升 15-20% 帧率表现。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS"
            },
            {
                "id": "bmw_stat_fps",
                "name": {"zh-CN": "实时显示当前运行帧率 (FPS 监控)", "en": "Show FPS Overlay"},
                "syntax_type": "ue_console",
                "code": "stat fps",
                "desc": "在屏幕右上角实时显示渲染帧率与每帧毫秒延迟，随时掌控性能波动情况。",
                "min_version": "v1.0.8+",
                "framework_required": "UE4SS"
            }
        ]
    }
]

wukong_popular = [
    {
        "name": {"zh-CN": "开启电影级慢动作子弹时间 (识破神器)", "en": "Slomo 0.3x (Bullet Time)"},
        "command": "slomo 0.3",
        "desc": "全场景 0.3 倍速流速，轻松看清所有妖王 Boss 招式前摇从容识破！"
    },
    {
        "name": {"zh-CN": "一键解锁全图鉴神珍武器 (金箍棒/三尖枪)", "en": "Unlock All Weapons"},
        "command": "allweapon",
        "desc": "直接解锁游戏内全部如意金箍棒、三尖两刃枪等神珍武器。"
    },
    {
        "name": {"zh-CN": "一键解锁全图鉴 54 种妖王妖魔精魄技能", "en": "Unlock All Spirits"},
        "command": "allsoulskill",
        "desc": "全 54 种精魄变身一键入库，随心化身幽魂与火狼对决！"
    },
    {
        "name": {"zh-CN": "增加 1,000,000 灵蕴货币 (Will 财富自由)", "en": "Add 1,000,000 Will"},
        "command": "additem 1002 1000000",
        "desc": "获得百万金钱，随意购买全土地庙商品与全部打造配方。"
    }
]

wukong_mods = [
    {
        "id": "ue4ss-wukong",
        "title": "UE4SS for Black Myth Wukong (黑神话虚幻5底层调试扩展)",
        "author": "UE4SS Team",
        "version": "v3.0.1",
        "size": "4.8 MB",
        "downloads": "8.5M",
        "endorsements": "180K",
        "category": "核心框架 (Framework)",
        "desc": "黑神话悟空专属 UE5 注入器，支持实时热键控制台与 Lua 逻辑模组挂载。",
        "dependencies": ["None"],
        "installPath": "b1\\Binaries\\Win64\\",
        "installSteps": [
            "1. 将压缩包解压直接放入 b1\\Binaries\\Win64 文件夹；",
            "2. 游戏启动后按 F10 即可呼出全能控制台。"
        ]
    },
    {
        "id": "wukong-gm",
        "title": "WukongGM (黑神话悟空原生 GM 开发者指令注入器)",
        "author": "lazyassin",
        "version": "v1.2.0",
        "size": "1.2 MB",
        "downloads": "4.2M",
        "endorsements": "120K",
        "category": "实用工具 (Utility)",
        "desc": "利用游戏自身导出的 BGUFunctionLibraryManaged 函数库，热键一键派发原生指令，免疫版本更新失效！",
        "dependencies": ["UE4SS"],
        "installPath": "b1\\Binaries\\Win64\\ue4ss\\Mods\\WukongGM\\",
        "installSteps": [
            "1. 确保已安装好 RE-UE4SS 基础框架；",
            "2. 将 WukongGM 文件夹解压直接放入 b1\\Binaries\\Win64\\ue4ss\\Mods\\ 目录下；",
            "3. 进入游戏存档后，随时按下键盘 F7 键即可执行 commands.txt / items.txt 内的作弊指令。"
        ]
    },
    {
        "id": "wukong-map",
        "title": "Black Myth Wukong Realtime Map (实时全景导航地图与标记)",
        "author": "BWMap Community",
        "version": "v1.4.2",
        "size": "28 MB",
        "downloads": "9.2M",
        "endorsements": "210K",
        "category": "界面导航 (UI / Navigation)",
        "desc": "告别迷路！在屏幕右上角提供全景 3D 俯瞰小地图，标亮全土地庙、隐藏打坐蒲团、妖王 Boss 与珍玩草药位置。",
        "dependencies": ["UE4SS"],
        "installPath": "b1\\Binaries\\Win64\\ue4ss\\Mods\\BWMap\\",
        "installSteps": [
            "1. 将 BWMap 文件夹放入 ue4ss\\Mods 目录；",
            "2. 游戏中按 M 键即可在右上角自由开关小地图。"
        ]
    },
    {
        "id": "enhanced-wukong-visuals",
        "title": "Enhanced Wukong Visuals (画质增强与抗锯齿锐化优化包)",
        "author": "GamerX",
        "version": "v2.1",
        "size": "3.5 MB",
        "downloads": "3.1M",
        "endorsements": "88K",
        "category": "视觉增强 (Visuals)",
        "desc": "优化黑神话全景光线追踪反射，去除画面雾蒙蒙的涂抹感，使齐天大圣毛发与金箍棒金属质感更加逼真锋利。",
        "dependencies": ["None"],
        "installPath": "b1\\Content\\Paks\\~mods\\",
        "installSteps": [
            "1. 在游戏安装目录 b1\\Content\\Paks 下新建名为 ~mods 的文件夹；",
            "2. 将 EnhancedVisuals.pak 放入 ~mods 目录中启动游戏即可。"
        ]
    }
]

# Find Wukong and update
for g in games:
    if g["id"] == "black-myth-wukong":
        g["consoleCategories"] = wukong_categories
        g["popularCommands"] = wukong_popular
        g["curatedMods"] = wukong_mods
        g["consoleShortcut"] = "F10 键 或 ~ 键 (需装载 UE4SS 调试插件)"
        g["consoleEnableGuide"] = {
            "zh-CN": "1. 【前置依赖】将 RE-UE4SS 解压放入游戏安装目录 `b1\\Binaries\\Win64\\` 文件夹下；\n2. 【启动验证】进入游戏关卡，随时按下 F10 键即可呼出图形控制台，按 ~ 键开启虚幻5原生命令行；\n3. 【一键注入 GM 指令】针对全神兵、全精魄与无限道具，配合 WukongGM 模组（位于 `b1\\Binaries\\Win64\\ue4ss\\Mods\\WukongGM\\`），游戏内按 F7 键直接秒级调用游戏底层原生函数库 `BGUFunctionLibraryManaged:RunScriptGM` 极速生效，绝无版本失效困扰！",
            "en": "1. Extract RE-UE4SS into `b1\\Binaries\\Win64\\` directory.\n2. In-game, press F10 to toggle the UE4SS developer console or ~ for the native command bar.\n3. For GM commands and item batches, install WukongGM to `b1\\Binaries\\Win64\\ue4ss\\Mods\\WukongGM\\` and press F7 in-game to execute."
        }
        break

# Save back to games_top100.json
with open(JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(games, f, ensure_ascii=False, indent=2)

print(f"✅ Successfully updated {JSON_PATH}")

# Save to public/data.js
with open(JS_PATH, 'w', encoding='utf-8') as f:
    f.write('// L-MOD Vault Offline Database (Enriched v3)\n')
    f.write('window.GAMES_DATA = ')
    json.dump(games, f, ensure_ascii=False, indent=2)
    f.write(';\n')

print(f"✅ Successfully synchronized {JS_PATH}")
