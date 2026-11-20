#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/rebuild_bg3_flagship.py
Content for Baldur's Gate 3 (console guide, command categories, curated mods,
metadata).

Writes only the fields in OWNED_FIELDS of baldurs-gate-3, through gamedata_guard: the
master data must exist, radar and trainer fields are never written (trainer data
comes from fling_trainer_sync.py), and in public/data.js only the GAMES_DATA segment
changes (TRANSLATIONS_DATA is left alone).

Usage: python3 scripts/rebuild_bg3_flagship.py [--dry-run]
"""

from gamedata_guard import write_owned_fields

GAME_ID = "baldurs-gate-3"

bg3_categories = [
    {
        "category": "👑 核心生存、豁免锁死与全法术位无限长休 (God Mode, Spell Slots & Long Rest)",
        "commands": [
            {
                "id": "bg3_apply_sanctuary",
                "name": {
                    "zh-CN": "赋予常驻庇护术状态 (绝对免受单体攻击)",
                    "en": "Permanent Sanctuary Buff"
                },
                "syntax_type": "lua_function",
                "code": "Osi.ApplyStatus(GetHostCharacter(), \"SANCTUARY\", -1)",
                "desc": "为主角施加永久生效的庇护术护盾，敌方无法将角色选为单体伤害目标，直至角色主动做出攻击。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://docs.baldursgate3.game/index.php?title=ApplyStatus"
            },
            {
                "id": "bg3_resurrect",
                "name": {
                    "zh-CN": "原地满血复生重生",
                    "en": "Resurrect Character to Full HP"
                },
                "syntax_type": "lua_function",
                "code": "Osi.Resurrect(GetHostCharacter())",
                "desc": "当队伍角色不慎被推落悬崖或重伤暴毙时，立即在原地满血复活并重置全部生理状态。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://docs.baldursgate3.game/index.php?title=Resurrect"
            },
            {
                "id": "bg3_remove_downed",
                "name": {
                    "zh-CN": "立即清除倒地重伤濒死异常状态",
                    "en": "Remove Downed & Bleeding Status"
                },
                "syntax_type": "lua_function",
                "code": "Osi.RemoveStatus(GetHostCharacter(), \"DOWNED\")",
                "desc": "立即清除倒地、残废、流血等负面残疾 Debuff，使角色瞬间站立投入战斗。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://docs.baldursgate3.game/index.php?title=RemoveStatus"
            }
        ]
    },
    {
        "category": "🎯 角色等级直升、经验值与职业兼修洗点 (Level, XP & Respec)",
        "commands": [
            {
                "id": "bg3_spawn_revivify_scroll",
                "name": {
                    "zh-CN": "获得复活卷轴 x10 (野外救急与守墓人洗点备用)",
                    "en": "Scroll of Revivify x10"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"c1c3e4fb-d68c-4e10-afdc-d4550238d50e\", GetHostCharacter(), 10)",
                "desc": "向背包添加 10 张神圣复活卷轴，无需长休即可随时拉起倒下的战友。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Scroll_of_Revivify"
            }
        ]
    },
    {
        "category": "💰 财富自由、负重解限与全营地补给物资 (Gold, Weight & Camp Supplies)",
        "commands": [
            {
                "id": "bg3_add_gold_100k",
                "name": {
                    "zh-CN": "增加 100,000 金币 (博德之门首富)",
                    "en": "Add 100,000 Gold"
                },
                "syntax_type": "lua_function",
                "code": "Osi.AddGold(GetHostCharacter(), 100000)",
                "desc": "向背包注入 10 万金币，随心所欲搬空第三章巫术杂货铺与各大商贩所有稀世魔法装备！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://docs.baldursgate3.game/index.php?title=AddGold"
            },
            {
                "id": "bg3_add_gold_template",
                "name": {
                    "zh-CN": "直接注入纯金币道具 (Gold Template x50,000)",
                    "en": "Add 50,000 Gold Template"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"1c3c9c74-34a1-4685-989e-410dc080be6f\", GetHostCharacter(), 50000)",
                "desc": "通过模板 GUID 直接将 50000 金币装填入背包底层。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Gold"
            },
            {
                "id": "bg3_camp_supplies_pack",
                "name": {
                    "zh-CN": "营地补给补给包 x50 (永久告别搜刮食物长休)",
                    "en": "Camp Supply Pack x50 (Full Rest Supply)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"398e7328-ce90-4c02-94a2-93341fac499a\", GetHostCharacter(), 50)",
                "desc": "每个补给包提供整整 40 点补给点，50 包足够连续进行 50 次完全长休，无限次触发营地剧情与法术位重置！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Supply_Pack"
            },
            {
                "id": "bg3_thieves_tools",
                "name": {
                    "zh-CN": "高级盗贼工具 x30 (秒撬全大陆所有宝箱大门)",
                    "en": "Thieves' Tools x30"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"e32a200c-5b63-414d-ae57-00e7b38f125b\", GetHostCharacter(), 30)",
                "desc": "阿斯代伦撬锁专用高阶工具，轻松开遍地城密室与银行金库。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Thieves%27_Tools"
            },
            {
                "id": "bg3_trap_disarm_tools",
                "name": {
                    "zh-CN": "陷阱解除工具包 x30 (安全拆除全地城陷阱)",
                    "en": "Trap Disarm Toolkit x30"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"22c74b5e-bef2-41b1-b9ed-f4acc766d4ee\", GetHostCharacter(), 30)",
                "desc": "安全拆除火球、落石与爆炸毒雾陷阱，探险零伤亡。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Trap_Disarm_Toolkit"
            }
        ]
    },
    {
        "category": "🧠 夺心魔蝌蚪寄生虫与至尊灵能潜能 (Illithid Parasites & Powers)",
        "commands": [
            {
                "id": "bg3_illithid_parasites_30",
                "name": {
                    "zh-CN": "夺心魔寄生虫标本 x30 (点满全员脑池灵能潜能)",
                    "en": "Mind Flayer Parasite Specimen x30"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"1ec327be-3b7f-4502-9586-860e057e09ae\", GetHostCharacter(), 30)",
                "desc": "一次性获得 30 只夺心魔蝌蚪，直接将主角与全队所有伙伴的脑部异能树（灵能过载、强运不利、灵能反冲等）全部点满！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Mind_Flayer_Parasite_Specimen"
            },
            {
                "id": "bg3_astral_tadpole",
                "name": {
                    "zh-CN": "受星界灌注的蝌蚪 (解锁半夺心魔至尊灵能与自由飞行)",
                    "en": "Astral-Touched Tadpole (Half-Illithid)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"4a82e6f2-839f-434e-addf-b07dd1578194\", GetHostCharacter(), 1)",
                "desc": "君主赠予的至尊星界蝌蚪，食用后立刻晋升为半夺心魔形态，解锁三层终极外圈技能与永久无消耗全图无障碍自由飞行！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Astral-Touched_Tadpole"
            }
        ]
    },
    {
        "category": "🗡️ 绝世金色传奇近战神兵 (Legendary Melee Weapons)",
        "commands": [
            {
                "id": "bg3_balduran_giantslayer",
                "name": {
                    "zh-CN": "博德安的巨人杀手巨剑 (传奇双手巨剑 - 力量加倍与巨化)",
                    "en": "Balduran's Giantslayer (Legendary Greatsword)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"7219fca3-5f41-43a0-8253-f4c09d8b6308\", GetHostCharacter(), 1)",
                "desc": "安苏巨龙巢穴最强神兵！力量调整值双倍附加伤害，自带「巨人体型」技能，体型暴增且攻击造成额外巨额武器力场打击！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Balduran%27s_Giantslayer"
            },
            {
                "id": "bg3_nyrulna_trident",
                "name": {
                    "zh-CN": "尼鲁纳三叉戟 (投掷流至尊神器 - 自动回手与雷鸣爆破)",
                    "en": "Nyrulna (Legendary Returning Trident)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"daf0be7f-87d9-448a-b94e-471ffec40ac5\", GetHostCharacter(), 1)",
                "desc": "末日马戏团头奖神器！投掷后无论飞出多远都会自动飞回手中，落地伴随大范围 3d4 雷鸣爆炸，全游戏投掷蛮子与战士的毕业神武！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Nyrulna"
            },
            {
                "id": "bg3_markoheshkir_staff",
                "name": {
                    "zh-CN": "玛科赫什基传奇法杖 (全法系毕业终极神杖 - 免费免消耗施法)",
                    "en": "Markoheshkir (Legendary Staff)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"7e39ad11-f8c3-421a-940c-05348c420c7d\", GetHostCharacter(), 1)",
                "desc": "拉玛吉斯高塔顶层至尊法杖！法术豁免难度与攻击掷骰 +1，自带「凯瑟里克之宠」多重元素附魔，每场战斗可免费免消耗释放一次 6 环终极法术！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Markoheshkir"
            },
            {
                "id": "bg3_blood_of_lathander",
                "name": {
                    "zh-CN": "洛山达之血钉头锤 (第一章传奇神锤 - 盲目不死生物与自动免死重生)",
                    "en": "The Blood of Lathander (Legendary Mace)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"7b961f08-46c1-46b1-99bc-c59283831a0b\", GetHostCharacter(), 1)",
                "desc": "晨曦之神洛山达的圣物，常驻 6 米范围内所有不死生物与邪魔致盲，生命归零时立即原地回血复苏并为全队回血！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/The_Blood_of_Lathander"
            },
            {
                "id": "bg3_silver_sword_astral",
                "name": {
                    "zh-CN": "星界银剑 (吉斯洋基人至尊巨剑 - 灵能伤害与心灵伤害免疫)",
                    "en": "Silver Sword of the Astral Plane"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"f01c3f5d-c542-420f-86c5-bdddf7819e29\", GetHostCharacter(), 1)",
                "desc": "洋基妹莱埃泽尔专属神器，由沃斯百夫长所赐，附带额外 1d6 心灵伤害，持有者完全免疫魅惑与心灵震慑伤害！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Silver_Sword_of_the_Astral_Plane"
            },
            {
                "id": "bg3_crimson_mischief",
                "name": {
                    "zh-CN": "猩红恶意短剑 (奥林巴尔神选近战短剑)",
                    "en": "Crimson Mischief (Legendary Shortsword)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"5961d027-75fd-4ad7-964c-8b786b5839fb\", GetHostCharacter(), 1)",
                "desc": "击杀血腥奥林获取的刺杀神器，对处于优势的敌人额外追加 7 点纯穿刺伤害加成！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Crimson_Mischief"
            },
            {
                "id": "bg3_bloodthirst_dagger",
                "name": {
                    "zh-CN": "嗜血狂怒匕首 (增加暴击率与反弹借机攻击)",
                    "en": "Bloodthirst (Legendary Dagger)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"d90abf24-3c4e-4bbf-84aa-def05ca9962a\", GetHostCharacter(), 1)",
                "desc": "暴击所需点数降低 1 点，击中敌人施加穿刺易伤 Debuff，主手装备时近战攻击落空会自动反击！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Bloodthirst"
            },
            {
                "id": "bg3_duelist_prerogative",
                "name": {
                    "zh-CN": "决斗者的特权细剑 (双重附赠动作与额外借机攻击)",
                    "en": "Duelist's Prerogative (Legendary Rapier)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"d49bf05e-4f94-4860-bd8c-ae63dae811be\", GetHostCharacter(), 1)",
                "desc": "单手持握时每回合额外获得一次附赠动作与反应机会，暴击阈值大幅下降，自带坏死伤害挑战决斗技能！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Duellist%27s_Prerogative"
            },
            {
                "id": "bg3_selune_spear_night",
                "name": {
                    "zh-CN": "塞伦涅的黑夜之矛 (月之圣矛 - 黑暗视觉与全豁免优势)",
                    "en": "Selûne's Spear of Night"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"2eeabe97-8f29-4f4f-827e-6cfcd8fd1779\", GetHostCharacter(), 1)",
                "desc": "影心救赎线专属圣矛，赋予持有者黑暗视觉与感知豁免优势，附带「月之微光」与「月之护盾」神圣技能！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Selûne%27s_Spear_of_Night"
            },
            {
                "id": "bg3_shar_spear_evening",
                "name": {
                    "zh-CN": "莎尔的暮色之矛 (黑夜法官专属神器 - 黑暗视觉与隐形)",
                    "en": "Shar's Spear of Evening"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"61f31bf6-47ec-41e1-9385-2f6c26facc87\", GetHostCharacter(), 1)",
                "desc": "影心堕落成为暗夜法官之刃，在魔法黑暗中视物无阻且造成额外 1d6 伤害，自带「莎尔之拥」自由隐形！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Shar%27s_Spear_of_Evening"
            }
        ]
    },
    {
        "category": "🏹 绝世传奇远程武器与高阶箭矢 (Legendary Ranged Weapons & Ammo)",
        "commands": [
            {
                "id": "bg3_gontr_mael",
                "name": {
                    "zh-CN": "冈特·耶尔传奇长弓 (钢铁卫士铸造厂泰坦神弓 - 恒定加速与神圣引导)",
                    "en": "Gontr Mael (Legendary Longbow)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"7e81bb6a-f465-4fe9-b1db-7ce6198246ba\", GetHostCharacter(), 1)",
                "desc": "击败钢铁卫士泰坦获取的神弓！bg3.wiki 标注其武器类型为长弓（Longbow），并非原目录所写的“重弩”；攻击命中敌人概率施加「发光光辉」，自带「天界加速术」。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Gontr_Mael"
            },
            {
                "id": "bg3_the_dead_shot",
                "name": {
                    "zh-CN": "致命一击长弓 (暴击掷骰减少1点与熟练项双倍附加)",
                    "en": "The Dead Shot (Legendary Longbow)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"269b2b03-aaaf-4635-98e2-e9b32dab5ffa\", GetHostCharacter(), 1)",
                "desc": "神射手流派核心远程武器，将致命一击需求降低 1 点，并使攻击掷骰的熟练加值直接翻倍！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/The_Dead_Shot"
            },
            {
                "id": "bg3_titanstring_bow",
                "name": {
                    "zh-CN": "泰坦弦弓 (将力量调整值附加于远程伤害)",
                    "en": "Titanstring Bow"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"13236988-83df-4bf2-8005-b4ac31f21ff4\", GetHostCharacter(), 1)",
                "desc": "配合巨人药水实现伤害最大化的变态长弓，在敏捷加成之外将全额力量加成叠加在每一箭上！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Titanstring_Bow"
            },
            {
                "id": "bg3_arrows_many_targets",
                "name": {
                    "zh-CN": "多重目标箭 x30 (一箭串联散射全屏小怪)",
                    "en": "Arrow of Many Targets x30"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"b11b3f7f-d8ec-41db-93b9-24474aea31e3\", GetHostCharacter(), 30)",
                "desc": "射出后自动弹射至目标周围最多 3 名额外敌人，清图效率最狂暴的高阶箭矢！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Arrow_of_Many_Targets"
            },
            {
                "id": "bg3_arrows_slaying_dragon",
                "name": {
                    "zh-CN": "屠龙箭 x10 (对巨龙双倍伤害)",
                    "en": "Arrow of Dragon Slaying x10"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"437835b4-0d13-47b7-8aca-5da4f948783b\", GetHostCharacter(), 10)",
                "desc": "决战安苏巨龙与耐色瑞尔红龙必备，命中造成两倍绝对暴击伤害！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Arrow_of_Dragon_Slaying"
            }
        ]
    },
    {
        "category": "🛡️ 绝世传奇护甲与地狱火重装 (Legendary Armour & Helldusk Set)",
        "commands": [
            {
                "id": "bg3_helldusk_armor",
                "name": {
                    "zh-CN": "地狱火胸甲 (21点高AC重甲 - 全职业免熟练项穿戴与绝对免火伤)",
                    "en": "Helldusk Armour (AC 21 Legendary)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"7ae705fd-1cfd-4482-a584-d2e68f9c1262\", GetHostCharacter(), 1)",
                "desc": "希望之邸拉斐尔掉落的终极重铠！高达 21 护甲等级，任何职业穿戴自动获得熟练项且不会阻碍施法，完全免疫燃烧并削减 3 点所有受到的伤害！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Helldusk_Armour"
            },
            {
                "id": "bg3_helldusk_helmet",
                "name": {
                    "zh-CN": "地狱火头盔 (免疫暴击、震慑与附加劣势)",
                    "en": "Helldusk Helmet"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"1c198060-6b6a-41c5-82ce-a3d3c3d76404\", GetHostCharacter(), 1)",
                "desc": "绝对免疫暴击打击，自带魔法抗性豁免优势与地狱火视界黑暗视觉，附带「灼热射线」法术！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Helldusk_Helmet"
            },
            {
                "id": "bg3_helldusk_gloves",
                "name": {
                    "zh-CN": "地狱火手套 (附加火焰坏死法术与近战双重伤害)",
                    "en": "Helldusk Gloves"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"ad219a90-ab3d-4821-8206-011293f5837b\", GetHostCharacter(), 1)",
                "desc": "武器攻击附带额外 1d6 火焰伤害，空手打击附加 1d6 坏死伤害并施加流血！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Helldusk_Gloves"
            },
            {
                "id": "bg3_helldusk_boots",
                "name": {
                    "zh-CN": "地狱火靴子 (免疫强风与地面位移摔倒)",
                    "en": "Helldusk Boots"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"bc82f909-ade5-4ada-9b94-cec7ca1d4a68\", GetHostCharacter(), 1)",
                "desc": "绝对不会被法术击退或强制移动，免疫光滑冰面与油脂打滑，附带「地狱步」瞬移传送技能！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Helldusk_Boots"
            },
            {
                "id": "bg3_helm_of_balduran",
                "name": {
                    "zh-CN": "博德安的头盔 (每回合自愈2点生命与绝对免疫暴击)",
                    "en": "Helm of Balduran"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"0a64283a-1fc4-45cd-9e5e-f463f6b762ea\", GetHostCharacter(), 1)",
                "desc": "博德之门传奇创始人头盔，AC +1，每回合开始自动恢复 2 点生命值，免疫一切致晕与暴击伤害！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Helm_of_Balduran"
            },
            {
                "id": "bg3_viconia_shield",
                "name": {
                    "zh-CN": "维康尼亚的行走要塞 (传奇重盾 - +3AC与法术反弹结界)",
                    "en": "Viconia's Walking Fortress (Legendary Shield)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"4f313dde-14bb-43a2-abdd-07b2eb38b33a\", GetHostCharacter(), 1)",
                "desc": "哀伤之邸击败维康尼亚获得的至尊盾牌！高达 +3 护甲等级，对抗法术获得优势，被攻击时可使用反应力场直接将敌人击退震翻！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Viconia%27s_Walking_Fortress"
            },
            {
                "id": "bg3_bhaalist_armour",
                "name": {
                    "zh-CN": "巴尔信徒护甲 (赋予周围敌人穿刺易伤光环 - 物理伤害直接翻倍)",
                    "en": "Bhaalist Armour (Aura of Murder)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"443b2caf-8d36-42cf-b389-d774229ed18c\", GetHostCharacter(), 1)",
                "desc": "刺客与弓手流派的核心神装，周围 2 米内所有非穿刺抗性敌人自动获得穿刺伤害翻倍易伤 Debuff！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Bhaalist_Armour"
            },
            {
                "id": "bg3_vest_soul_rejuvenation",
                "name": {
                    "zh-CN": "灵魂复苏胸甲 (武僧毕业神甲 - 反弹近战反击与法术自愈)",
                    "en": "Vest of Soul Rejuvenation"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"1c69a87e-9136-4e13-90af-c0f02d0fc81f\", GetHostCharacter(), 1)",
                "desc": "散打宗武僧终极毕业防具，敌人近战攻击落空时可立即使用反应施展徒手攻击痛击对手！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Vest_of_Soul_Rejuvenation"
            }
        ]
    },
    {
        "category": "💍 传奇首饰、属性锁死护符与关键戒指 (Legendary Rings & Amulets)",
        "commands": [
            {
                "id": "bg3_amulet_greater_health",
                "name": {
                    "zh-CN": "高等健康护符 (体质属性直接锁死 23 点与体质豁免优势)",
                    "en": "Amulet of Greater Health (Con 23)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"5ed63342-30c9-456d-9a57-a88c8596c0c9\", GetHostCharacter(), 1)",
                "desc": "佩戴后将佩戴者的体质属性直接拉满并强制锁死为 23 点，生命值暴涨上百点，法术专注检定获得常驻优势！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Amulet_of_Greater_Health"
            },
            {
                "id": "bg3_gauntlets_hill_giant",
                "name": {
                    "zh-CN": "山丘巨人力量手套 (力量属性直接锁死 23 点)",
                    "en": "Gauntlets of Hill Giant Strength (Str 23)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"9481aa27-ce9c-414c-84ff-5e974fd64d89\", GetHostCharacter(), 1)",
                "desc": "将佩戴者的力量属性直接恒定锁死为 23 点，无论法师或游荡者佩戴都能拥有撼动山丘的物理爆发与跳跃距离！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Gauntlets_of_Hill_Giant_Strength"
            },
            {
                "id": "bg3_ring_regeneration",
                "name": {
                    "zh-CN": "再生之戒 (每回合开始自动回复 1d4 生命值)",
                    "en": "Ring of Regeneration"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"d6ee2594-7373-4fed-a167-f9d95cb4ecfd\", GetHostCharacter(), 1)",
                "desc": "巫术杂货铺洛若坎售卖的传说戒指，战斗中与非战斗状态持续自愈回血。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Ring_of_Regeneration"
            },
            {
                "id": "bg3_risky_ring",
                "name": {
                    "zh-CN": "风险之戒 (所有攻击掷骰常驻获得优势)",
                    "en": "Risky Ring (All Attack Rolls Advantage)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"6fa51fb6-0c99-4e2e-bf3c-f4fe18fd64a7\", GetHostCharacter(), 1)",
                "desc": "战术家与硬核玩家必备神戒，所有近战与远程攻击必定拥有双骰优势，触发暴击概率翻倍！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Risky_Ring"
            },
            {
                "id": "bg3_ring_free_action",
                "name": {
                    "zh-CN": "自由行动之戒 (免疫麻痹、禁锢与困难地形)",
                    "en": "Ring of Free Action"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"50379f58-7892-44cb-be6e-146a60070055\", GetHostCharacter(), 1)",
                "desc": "彻底无视藤蔓缠绕、冰面减速与一切麻痹眩晕控制技能，在战场中穿梭自如。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Ring_of_Free_Action"
            },
            {
                "id": "bg3_killer_sweetheart",
                "name": {
                    "zh-CN": "杀手的甜心戒指 (击杀目标后下一次攻击必定触发暴击)",
                    "en": "Killer's Sweetheart"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"2f2d4bf3-6a14-43f5-81fe-e14aa9871215\", GetHostCharacter(), 1)",
                "desc": "击杀任意敌人后激活，下一次无论使用什么武器攻击都必定判定为致命一击（Natural 20）！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Killer%27s_Sweetheart"
            }
        ]
    },
    {
        "category": "📜 全职业 6 环终极魔法卷轴 (Level 6 Master Scrolls)",
        "commands": [
            {
                "id": "bg3_scroll_globe_invulnerability",
                "name": {
                    "zh-CN": "无敌护罩卷轴 x10 (范围内全员绝对无敌免疫一切伤害)",
                    "en": "Scroll of Globe of Invulnerability x10"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"8d4c06d1-e504-49b0-a4fa-5179ab717f1e\", GetHostCharacter(), 10)",
                "desc": "战役通关神器！释放半径 3 米的绝对屏障金钟罩，圆圈内所有友方免疫包括龙炎、神圣与力场在内的一切伤害！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Scroll_of_Globe_of_Invulnerability"
            },
            {
                "id": "bg3_scroll_disintegrate",
                "name": {
                    "zh-CN": "解离术卷轴 x10 (10d6+40 点毁灭力场伤害直接化为灰烬)",
                    "en": "Scroll of Disintegrate x10"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"3f737706-57ca-45e6-b0d1-45238da76329\", GetHostCharacter(), 10)",
                "desc": "超高单体爆发射线，目标生命降为 0 时直接瓦解为一堆灰烬，彻底阻止复活机制。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Scroll_of_Disintegrate"
            },
            {
                "id": "bg3_scroll_chain_lightning",
                "name": {
                    "zh-CN": "链状闪电卷轴 x10 (10d8 点连锁闪电轰炸多名强敌)",
                    "en": "Scroll of Chain Lightning x10"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"13105f7d-55fa-4292-abfe-b9d80054b48e\", GetHostCharacter(), 10)",
                "desc": "召唤极速电光在目标及周围 3 名敌对实体之间疯狂弹射，水面潮湿状态下伤害暴涨 200%！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Scroll_of_Chain_Lightning"
            },
            {
                "id": "bg3_scroll_sunbeam",
                "name": {
                    "zh-CN": "阳光术卷轴 x10 (每回合持续释放耀光并致盲敌人)",
                    "en": "Scroll of Sunbeam x10"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"049d70c4-7ea3-4b6c-af6f-44dab7813a89\", GetHostCharacter(), 10)",
                "desc": "召唤炽热日光射线，对不死生物造成高额克制光耀伤害，每回合无需额外消耗法术位即可重新发射。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Scroll_of_Sunbeam"
            },
            {
                "id": "bg3_scroll_freezing_sphere",
                "name": {
                    "zh-CN": "奥提路克冰封球卷轴 x10 (10d6 点大范围严寒冰冻)",
                    "en": "Scroll of Otiluke's Freezing Sphere x10"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"74d0e4f0-de97-4097-a7e7-f5759a375c81\", GetHostCharacter(), 10)",
                "desc": "在目标区域引爆超大范围冰霜风暴，冻结一切液体并将敌人双足冻结在地面上。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Scroll_of_Otiluke%27s_Freezing_Sphere"
            }
        ]
    },
    {
        "category": "🧪 传奇灵药与飞行隐形药剂 (Legendary Elixirs & Potions)",
        "commands": [
            {
                "id": "bg3_elixir_cloud_giant",
                "name": {
                    "zh-CN": "云巨人力量灵药 x20 (力量属性拉满至 27 点极限神力)",
                    "en": "Elixir of Cloud Giant Strength x20 (Str 27)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"e6490cc8-7f81-4aac-95e8-a58ce5e88a31\", GetHostCharacter(), 20)",
                "desc": "全游戏最强力量药水！药效持续直至下一次长休，将力量直接飙升至游戏设定的绝对上限 27 点（+8 攻击与伤害修正加成）！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Elixir_of_Cloud_Giant_Strength"
            },
            {
                "id": "bg3_elixir_bloodlust",
                "name": {
                    "zh-CN": "嗜血灵药 x20 (每击杀一人立即额外获得一个完整动作)",
                    "en": "Bloodlust Elixir x20 (Extra Action on Kill)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"45a775f8-2cf9-440d-b9eb-4ee5f17efca8\", GetHostCharacter(), 20)",
                "desc": "持续至长休，每回合首次击杀敌人后立即恢复一个完整的战斗动作并获得 5 点临时生命，砍倒全场！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Elixir_of_Bloodlust"
            },
            {
                "id": "bg3_potion_angelic_slumber",
                "name": {
                    "zh-CN": "天使轻眠药水 x10 (就地陷入浅睡等效一次完整长休)",
                    "en": "Potion of Angelic Slumber x10 (Instant Long Rest)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"4d801c1a-691e-47c8-88e7-78367b4e2c8e\", GetHostCharacter(), 10)",
                "desc": "在红名禁止长休的决战副本中就地进入 2 回合浅睡，醒来完全恢复所有 1~6 环法术位与全部生命值！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Potion_of_Angelic_Slumber"
            },
            {
                "id": "bg3_potion_speed",
                "name": {
                    "zh-CN": "极速药水 x20 (获得加速术 - 额外动作与AC+2)",
                    "en": "Potion of Speed x20 (Haste)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"ad9f3f24-d755-48b6-aa7b-c34da068209f\", GetHostCharacter(), 20)",
                "desc": "快速进入 3 回合加速状态，每回合多一次施法或普攻机会，移动速度翻倍。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Potion_of_Speed"
            }
        ]
    },
    {
        "category": "⏱️ 动作掌控、常驻全图飞行与急速爆发 (Actions, Flight & Movement)",
        "commands": [
            {
                "id": "bg3_apply_haste",
                "name": {
                    "zh-CN": "常驻绝对急速术 (动作翻倍且永不疲劳瘫痪)",
                    "en": "Permanent Haste Buff"
                },
                "syntax_type": "lua_function",
                "code": "Osi.ApplyStatus(GetHostCharacter(), \"HASTE\", -1)",
                "desc": "为主角施加永久生效的急速术，每回合直接额外获取一个完整的法术或武器攻击动作，移动速度翻倍，且绝对不会因为被打断而陷入 1 回合虚脱！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://docs.baldursgate3.game/index.php?title=ApplyStatus"
            },
            {
                "id": "bg3_apply_fly",
                "name": {
                    "zh-CN": "赋予常驻全图自由飞行能力 (无视地形跨越断崖)",
                    "en": "Permanent Fly Buff"
                },
                "syntax_type": "lua_function",
                "code": "Osi.ApplyStatus(GetHostCharacter(), \"FLY\", -1)",
                "desc": "直接赋予主角飞天遁地能力，免去攀爬楼梯与跳跃落脚点限制，直飞高台抢占先攻优势！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://docs.baldursgate3.game/index.php?title=ApplyStatus"
            },
            {
                "id": "bg3_apply_see_invis",
                "name": {
                    "zh-CN": "赋予常驻识破隐形破除虚妄视界",
                    "en": "Permanent See Invisibility"
                },
                "syntax_type": "lua_function",
                "code": "Osi.ApplyStatus(GetHostCharacter(), \"SEE_INVISIBILITY\", -1)",
                "desc": "9 米范围内任何试图隐形的幽灵、鬼婆或盗贼直接被识破真身显形暴露无遗！",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://docs.baldursgate3.game/index.php?title=ApplyStatus"
            },
            {
                "id": "bg3_apply_longstrider",
                "name": {
                    "zh-CN": "赋予常驻大步奔行 (移动距离大幅提升)",
                    "en": "Permanent Longstrider"
                },
                "syntax_type": "lua_function",
                "code": "Osi.ApplyStatus(GetHostCharacter(), \"LONGSTRIDER\", -1)",
                "desc": "每回合移动力增加 3 米，战术位移与跑图探路更加迅捷敏锐。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://docs.baldursgate3.game/index.php?title=ApplyStatus"
            }
        ]
    }
]

bg3_popular = [
    {
        "name": {"zh-CN": "增加金币 (100,000 金币)", "en": "Add 100,000 Gold"},
        "command": "Osi.AddGold(GetHostCharacter(), 100000)",
        "desc": "瞬间化身博德之门巨富，搬空全大陆所有商贩的绝世装备。",
        "source": "https://docs.baldursgate3.game/index.php?title=AddGold"
    },
    {
        "name": {"zh-CN": "获得夺心魔寄生虫标本 x30", "en": "Add 30 Illithid Parasites"},
        "command": "Osi.TemplateAddTo(\"1ec327be-3b7f-4502-9586-860e057e09ae\", GetHostCharacter(), 30)",
        "desc": "一次性点满主角与全队所有伙伴的脑池异能潜能。",
        "source": "https://bg3.wiki/wiki/Mind_Flayer_Parasite_Specimen"
    },
    {
        "name": {"zh-CN": "获得博德安的巨人杀手巨剑 (传奇双手巨剑)", "en": "Add Balduran's Giantslayer"},
        "command": "Osi.TemplateAddTo(\"7219fca3-5f41-43a0-8253-f4c09d8b6308\", GetHostCharacter(), 1)",
        "desc": "获取力量加倍并自带巨人体型的最强近战巨剑。",
        "source": "https://bg3.wiki/wiki/Balduran%27s_Giantslayer"
    },
    {
        "name": {"zh-CN": "获得地狱火全套胸甲 (21AC全职业免熟练)", "en": "Add Helldusk Armour"},
        "command": "Osi.TemplateAddTo(\"7ae705fd-1cfd-4482-a584-d2e68f9c1262\", GetHostCharacter(), 1)",
        "desc": "拉斐尔终极重铠，全职业穿戴免熟练项且免疫火伤。",
        "source": "https://bg3.wiki/wiki/Helldusk_Armour"
    },
    {
        "name": {"zh-CN": "赋予常驻急速术 (动作翻倍且永不疲劳)", "en": "Permanent Haste Buff"},
        "command": "Osi.ApplyStatus(GetHostCharacter(), \"HASTE\", -1)",
        "desc": "战斗动作常驻翻倍，移动速度翻倍且断专注不虚脱。",
        "source": "https://docs.baldursgate3.game/index.php?title=ApplyStatus"
    }
]

bg3_mods = [
    {
        "id": "bg3-script-extender",
        "title": "BG3 Script Extender (bg3se)",
        "author": "Norbyte",
        "category": "核心底层工具 (Core Utility / Framework)",
        "desc": "全网公认最核心的博德之门3底层框架！劫持 DWrite.dll 开启游戏底层 Osiris 引擎控制台黑窗，提供极速内存注入与所有高级 Mod 的前置运行支持。",
        "dependencies": [
            "None"
        ],
        "installPath": "Baldur's Gate 3\\bin\\",
        "installSteps": [
            "1. 下载解压得到 DWrite.dll 文件；",
            "2. 直接复制放入 Baldur's Gate 3\\bin\\ 目录（与 bg3.exe 同级）；",
            "3. 在 bin 目录新建 ScriptExtenderSettings.json，写入 {\"CreateConsole\": true} 即可开机自动弹窗呼出命令控制台。"
        ],
        "isDirect": False,
        "nexusUrl": "https://github.com/Norbyte/bg3se"
    },
    {
        "id": "improved-ui",
        "title": "ImpUI (ImprovedUI)",
        "author": "AlanaSP ShinyHobo Djmr Zee and bibsan",
        "category": "界面增强 (UI / QoL)",
        "desc": "彻底解除捏脸、背包与战斗界面的布局限制，支持宽屏 21:9 / 32:9 分辨率，杜绝 Mod 导致的剧情对话黑框与捏脸滑条重叠问题。",
        "dependencies": [
            "None"
        ],
        "installPath": "%LocalAppData%\\Larian Studios\\Baldur's Gate 3\\Mods\\",
        "installSteps": [
            "1. 下载 ImprovedUI.pak 并放入 LocalAppData 模组目录；",
            "2. 使用官方 Patch 7 模组管理器或 BG3 Mod Manager 激活并置于加载顺序顶端。"
        ],
        "isDirect": False,
        "nexusUrl": "https://www.nexusmods.com/baldursgate3/mods/366",
        "version": "2.1.0.82",
        "downloads": "8.3M",
        "endorsements": "89.9K",
        "checkedAt": "2026-11-20"
    },
    {
        "id": "party-limit-begone",
        "title": "Party Limit Begone",
        "author": "Sildur",
        "category": "玩法规则 (Gameplay / Party)",
        "desc": "强迫症玩家必装！将联机上限提升至 8 人，单人战役队伍上限直接提升至 16 人！全员伙伴（影心、阿斯代伦、卡菈克、盖尔、莱埃泽尔等）全员随队，再也不会错过任何旷世野外拌嘴对话！",
        "dependencies": [
            "None"
        ],
        "installPath": "Baldur's Gate 3\\bin\\ 与 Mods 目录",
        "installSteps": [
            "1. 将压缩包中的 Mods 文件夹与 bin 文件夹直接解压覆盖到《博德之门3》安装根目录；",
            "2. 进入游戏即可直接在营地招募所有伙伴入队。"
        ],
        "isDirect": False,
        "nexusUrl": "https://www.nexusmods.com/baldursgate3/mods/327",
        "version": "3.5",
        "downloads": "2.9M",
        "endorsements": "43.5K",
        "checkedAt": "2026-11-20"
    },
    {
        "id": "5e-spells",
        "title": "5e Spells",
        "author": "Celes",
        "category": "法术与战斗 (Spells / Combat)",
        "desc": "将龙与地下城第五版规则书中拉瑞安未采用的 100+ 个经典法术（如绿色火焰之刃、寒冰之触、闪电箭、心灵尖刺等）全部按官方平衡性无缝实装到全职业法术树中！",
        "dependencies": [
            "ImprovedUI"
        ],
        "installPath": "%LocalAppData%\\Larian Studios\\Baldur's Gate 3\\Mods\\",
        "installSteps": [
            "1. 将 5eSpells.pak 放入 Mods 目录；",
            "2. 使用模组管理器导出活动加载顺序。"
        ],
        "isDirect": False,
        "nexusUrl": "https://www.nexusmods.com/baldursgate3/mods/125",
        "version": "2.4.3.0",
        "downloads": "4.2M",
        "endorsements": "44.4K",
        "checkedAt": "2026-11-20"
    },
    {
        "id": "native-camera-tweaks",
        "title": "Native Camera Tweaks",
        "author": "Ershin",
        "category": "镜头视角 (Camera / Immersion)",
        "desc": "彻底解除原版俯视角镜头俯仰角被锁死在 45 度的限制！允许将镜头下压至水平视线，以完全沉浸式的越肩第三人称动作 RPG 视角仰望巍峨的博德之门大都市！",
        "dependencies": [
            "BG3 Script Extender"
        ],
        "installPath": "Baldur's Gate 3\\bin\\NativeMods\\",
        "installSteps": [
            "1. 确保已安装 BG3 Script Extender；",
            "2. 将 NativeCameraTweaks.dll 与 .ini 放入 bin\\NativeMods\\ 目录；",
            "3. 在游戏中按下滚轮即可自由无限制仰望。"
        ],
        "isDirect": False,
        "nexusUrl": "https://www.nexusmods.com/baldursgate3/mods/945",
        "version": "2.4.5",
        "downloads": "2.4M",
        "endorsements": "31.4K",
        "checkedAt": "2026-11-20"
    },
    {
        "id": "wasd-character-movement",
        "title": "WASD Character Movement",
        "author": "Ch4nKyy",
        "category": "操控手感 (Controls / Movement)",
        "desc": "告别鼠标点地寻路！直接使用键盘 WASD 键平滑操控角色向前后左右自由奔跑奔行，配合 Native Camera Tweaks 瞬间将博德之门3变身为巫师3级别的第三人称动作大作！",
        "dependencies": [
            "Native Camera Tweaks"
        ],
        "installPath": "Baldur's Gate 3\\bin\\NativeMods\\",
        "installSteps": [
            "1. 将 wasd.dll 与 wasd.ini 放入 bin\\NativeMods 目录；",
            "2. 游戏中直接按 CapsLock 键可在鼠标点击模式与键盘直控模式间一键切换。"
        ],
        "isDirect": False,
        "nexusUrl": "https://www.nexusmods.com/baldursgate3/mods/781",
        "version": "1.9.9",
        "downloads": "2.2M",
        "endorsements": "26.7K",
        "checkedAt": "2026-11-20"
    },
    {
        "id": "tavs-hair-salon",
        "title": "Tav's Hair Salon",
        "author": "Toarie",
        "category": "外观美化 (Visuals / Character Creation)",
        "desc": "全网热度最高的发型模组！为所有人类、精灵、半精灵、卓尔、提夫林男女角色增加数十款极致飘逸唯美的现代与奇幻长发、辫发与发饰，捏脸党必备！",
        "dependencies": [
            "ImprovedUI"
        ],
        "installPath": "%LocalAppData%\\Larian Studios\\Baldur's Gate 3\\Mods\\",
        "installSteps": [
            "1. 将 Tavs_Hair_Salon.pak 放入 Mods 目录；",
            "2. 在创建角色或魔镜捏脸时直接选择全新发型序号。"
        ],
        "isDirect": False,
        "nexusUrl": "https://www.nexusmods.com/baldursgate3/mods/213",
        "version": "2.0.0.0",
        "downloads": "4.0M",
        "endorsements": "62.8K",
        "checkedAt": "2026-11-20"
    }
]

OWNED_FIELDS = (
    "title",
    "titles",
    "developer",
    "releaseYear",
    "genre",
    "steamRating",
    "steamAppId",
    "latestPatch",
    "hasConsole",
    "consoleShortcut",
    "consoleEnableGuide",
    "consoleCategories",
    "popularCommands",
    "curatedMods",
    "modInstallPath",
    "nexusStats",
)


def bg3_fields():
    return {
        "title": "Baldur's Gate 3",
        "titles": {
            "en": "Baldur's Gate 3",
            "zh-CN": "博德之门 3",
            "zh-TW": "柏德之門 3",
            "ja": "バルダーズ・ゲート3",
            "ko": "발더스 게이트 3",
            "ru": "Baldur's Gate 3",
            "de": "Baldur's Gate 3",
            "es": "Baldur's Gate 3"
        },
        "developer": "Larian Studios",
        "releaseYear": 2023,
        "genre": "CRPG / Turn-Based Tactics",
        "steamRating": "96% Overwhelmingly Positive",
        "steamAppId": 1086940,
        "latestPatch": "Patch 7 (官方内置模组管理器与全新邪恶结局更新)",
        "hasConsole": False,
        "consoleShortcut": "Norbyte Script Extender 控制台黑窗 (回车即时执行)",
        "consoleEnableGuide": {
            "zh-CN": "1. 【下载与部署前置】下载最新版 Norbyte's BG3 Script Extender，解压得到 DWrite.dll 文件；\n2. 【放置主程序目录】将 DWrite.dll 复制放入《博德之门3》安装根目录的 bin\\ 文件夹下（与 bg3.exe 和 bg3_dx11.exe 位于同一级目录）；\n3. 【启用控制台黑窗】在 bin\\ 目录下新建一个文本文件并重命名为 ScriptExtenderSettings.json，用记事本打开填入 {\"CreateConsole\": true} 并保存；\n4. 【呼出与代码执行】启动游戏，屏幕旁会自动伴随弹出一个透明的 Windows 控制台黑色终端窗口；在控制台窗口内直接按下回车键激活输入光标，将下列任意 Osi 函数指令复制粘贴进去并回车，游戏内道具即刻秒级刷入当前操控角色背包中！\n5. 【Patch 7 官方模组工坊说明】拉瑞安官方在 Patch 7 中内置了官方模组浏览器，本站整理的指令和精选 Mod 没有针对 Patch 7 及之后的版本逐一实测，装 Mod 前先看 Mod 页面写的支持版本。",
            "en": "1. Download Norbyte's BG3 Script Extender and extract DWrite.dll.\n2. Place DWrite.dll into 'Baldur's Gate 3\\bin\\' (same folder as bg3.exe).\n3. In bin\\, create ScriptExtenderSettings.json containing '{\"CreateConsole\": true}'.\n4. Launch the game; an interactive console terminal window will open alongside it. Press Enter in the terminal, paste any Osi command below, and press Enter to execute.\n5. The commands and mods listed here were not individually tested on Patch 7 or later; check each mod page for the game versions it supports."
        },
        "consoleCategories": bg3_categories,
        "popularCommands": bg3_popular,
        "curatedMods": bg3_mods,
        "modInstallPath": "%LocalAppData%\\Larian Studios\\Baldur's Gate 3\\Mods\\",
        "nexusStats": {
            "totalDownloads": "567.9M",
            "totalMods": "20,399",
            "checkedAt": "2026-11-20",
            "nexusDomain": "baldursgate3"
        }
    }


if __name__ == "__main__":
    write_owned_fields("rebuild_bg3_flagship.py", OWNED_FIELDS, {GAME_ID: bg3_fields()})
