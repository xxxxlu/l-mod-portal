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
        "category": "👑 核心生存与状态恢复 (Survival & Status Recovery)",
        "commands": [
            {
                "id": "bg3_apply_sanctuary",
                "name": {
                    "zh-CN": "赋予常驻庇护术状态（免疫单体锁定攻击）",
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
        "category": "🎯 复活与急救道具 (Revival Items)",
        "commands": [
            {
                "id": "bg3_spawn_revivify_scroll",
                "name": {
                    "zh-CN": "复活卷轴 x10（无需长休即可复活队友）",
                    "en": "Scroll of Revivify x10"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"c1c3e4fb-d68c-4e10-afdc-d4550238d50e\", GetHostCharacter(), 10)",
                "desc": "向背包添加 10 张复活卷轴，无需长休即可随时拉起倒下的战友。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Scroll_of_Revivify"
            }
        ]
    },
    {
        "category": "💰 金币、营地补给与工具道具 (Gold, Camp Supplies & Tools)",
        "commands": [
            {
                "id": "bg3_add_gold_100k",
                "name": {
                    "zh-CN": "增加 100,000 金币",
                    "en": "Add 100,000 Gold"
                },
                "syntax_type": "lua_function",
                "code": "Osi.AddGold(GetHostCharacter(), 100000)",
                "desc": "向背包注入 10 万金币，可用于购买商店中的装备和物资。",
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
                    "zh-CN": "营地补给包 x50",
                    "en": "Camp Supply Pack x50 (Full Rest Supply)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"398e7328-ce90-4c02-94a2-93341fac499a\", GetHostCharacter(), 50)",
                "desc": "每个补给包提供 40 点补给，50 个补给包足够进行 50 次完全长休，用于触发营地剧情与恢复法术位。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Supply_Pack"
            },
            {
                "id": "bg3_thieves_tools",
                "name": {
                    "zh-CN": "高级盗贼工具 x30",
                    "en": "Thieves' Tools x30"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"e32a200c-5b63-414d-ae57-00e7b38f125b\", GetHostCharacter(), 30)",
                "desc": "阿斯塔利昂撬锁专用的高阶工具，可用于打开上锁的箱子与房门。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Thieves%27_Tools"
            },
            {
                "id": "bg3_trap_disarm_tools",
                "name": {
                    "zh-CN": "陷阱拆除工具包 x30",
                    "en": "Trap Disarm Toolkit x30"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"22c74b5e-bef2-41b1-b9ed-f4acc766d4ee\", GetHostCharacter(), 30)",
                "desc": "用于拆除火球、落石、毒雾等陷阱，避免触发陷阱造成的伤害。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Trap_Disarm_Toolkit"
            }
        ]
    },
    {
        "category": "🧠 夺心魔寄生虫与灵能 (Illithid Parasites & Powers)",
        "commands": [
            {
                "id": "bg3_illithid_parasites_30",
                "name": {
                    "zh-CN": "夺心魔寄生虫标本 x30（用于解锁灵能异能）",
                    "en": "Mind Flayer Parasite Specimen x30"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"1ec327be-3b7f-4502-9586-860e057e09ae\", GetHostCharacter(), 30)",
                "desc": "一次性获得 30 个夺心魔寄生虫标本，可用于解锁主角与队友的灵能异能（如灵能过载、强运不利、灵能反冲等）。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Mind_Flayer_Parasite_Specimen"
            },
            {
                "id": "bg3_astral_tadpole",
                "name": {
                    "zh-CN": "受星界感染的蝌蚪（解锁半夺心魔形态与飞行）",
                    "en": "Astral-Touched Tadpole (Half-Illithid)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"4a82e6f2-839f-434e-addf-b07dd1578194\", GetHostCharacter(), 1)",
                "desc": "君主赠予的特殊蝌蚪，食用后角色变为半夺心魔形态，解锁三层外圈异能，并获得无消耗的自由飞行能力。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Astral-Touched_Tadpole"
            }
        ]
    },
    {
        "category": "🗡️ 传奇近战武器 (Legendary Melee Weapons)",
        "commands": [
            {
                "id": "bg3_balduran_giantslayer",
                "name": {
                    "zh-CN": "博德安的巨人杀手巨剑 (传奇双手巨剑 - 力量加倍与巨化)",
                    "en": "Balduran's Giantslayer (Legendary Greatsword)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"7219fca3-5f41-43a0-8253-f4c09d8b6308\", GetHostCharacter(), 1)",
                "desc": "安苏巨龙巢穴掉落的双手巨剑，攻击伤害额外增加等同于两倍力量调整值的加成，并自带「巨人体型」技能，使角色体型变大。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Balduran%27s_Giantslayer"
            },
            {
                "id": "bg3_nyrulna_trident",
                "name": {
                    "zh-CN": "尼鲁纳三叉戟 (投掷武器 - 自动回手与雷鸣爆炸)",
                    "en": "Nyrulna (Legendary Returning Trident)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"daf0be7f-87d9-448a-b94e-471ffec40ac5\", GetHostCharacter(), 1)",
                "desc": "马戏团剧情获得的三叉戟，投掷出去后会自动飞回手中，落地时造成范围 3d4 雷鸣伤害。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Nyrulna"
            },
            {
                "id": "bg3_markoheshkir_staff",
                "name": {
                    "zh-CN": "玛科赫什基法杖 (传奇法杖 - 免消耗施放法术)",
                    "en": "Markoheshkir (Legendary Staff)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"7e39ad11-f8c3-421a-940c-05348c420c7d\", GetHostCharacter(), 1)",
                "desc": "拉玛吉斯高塔获得的法杖，使法术豁免难度和攻击掷骰 +1，并带有多重元素附魔，每场战斗可免费施放一次 6 环法术。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Markoheshkir"
            },
            {
                "id": "bg3_blood_of_lathander",
                "name": {
                    "zh-CN": "洛山达之血钉头锤 (传奇钉头锤 - 致盲不死生物与自动复苏)",
                    "en": "The Blood of Lathander (Legendary Mace)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"7b961f08-46c1-46b1-99bc-c59283831a0b\", GetHostCharacter(), 1)",
                "desc": "晨曦之神洛山达的圣物，范围 6 米内的不死生物与邪魔会被致盲；生命归零时自动回复生命而非倒地，并为附近队友回血。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/The_Blood_of_Lathander"
            },
            {
                "id": "bg3_silver_sword_astral",
                "name": {
                    "zh-CN": "星界银剑 (传奇大剑 - 吉斯洋基人持有者专属加成)",
                    "en": "Silver Sword of the Astral Plane"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"f01c3f5d-c542-420f-86c5-bdddf7819e29\", GetHostCharacter(), 1)",
                "desc": "传奇+3巨剑，基础伤害为 2d6+3 加力量调整值；若由吉斯洋基人（如莱埃泽尔）持有，则额外获得心灵伤害加成、魅惑免疫与多项豁免优势。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Silver_Sword_of_the_Astral_Plane"
            },
            {
                "id": "bg3_crimson_mischief",
                "name": {
                    "zh-CN": "猩红恶意短剑 (传奇短剑)",
                    "en": "Crimson Mischief (Legendary Shortsword)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"5961d027-75fd-4ad7-964c-8b786b5839fb\", GetHostCharacter(), 1)",
                "desc": "击败血腥奥林获得的短剑；主手攻击对生命值低于一半的目标追加 1d4 穿刺伤害，副手持握且攻击带有优势时追加 7 点穿刺伤害。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Crimson_Mischief"
            },
            {
                "id": "bg3_bloodthirst_dagger",
                "name": {
                    "zh-CN": "嗜血狂怒匕首 (传奇匕首 - 暴击率提升与反击)",
                    "en": "Bloodthirst (Legendary Dagger)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"d90abf24-3c4e-4bbf-84aa-def05ca9962a\", GetHostCharacter(), 1)",
                "desc": "传奇+2匕首；主手持握时暴击所需点数降低 1 点，副手持握时近战命中会使目标易受穿刺伤害，且敌人攻击落空时可用反应发动反击。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Bloodthirst"
            },
            {
                "id": "bg3_duelist_prerogative",
                "name": {
                    "zh-CN": "决斗者的特权细剑 (传奇细剑 - 额外反应与暴击加成)",
                    "en": "Duelist's Prerogative (Legendary Rapier)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"d49bf05e-4f94-4860-bd8c-ae63dae811be\", GetHostCharacter(), 1)",
                "desc": "传奇细剑，副手空闲时额外获得一次反应机会，且掷骰 19 或 20 即视为暴击；命中敌人时可用反应追加等同熟练加值的坏死伤害。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Duellist%27s_Prerogative"
            },
            {
                "id": "bg3_selune_spear_night",
                "name": {
                    "zh-CN": "塞伦涅的黑夜之矛 (传奇长枪 - 黑暗视觉与感知优势)",
                    "en": "Selûne's Spear of Night"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"2eeabe97-8f29-4f4f-827e-6cfcd8fd1779\", GetHostCharacter(), 1)",
                "desc": "影心救赎结局专属武器，攻击与伤害 +3，赋予黑暗视觉、感知检定与感知豁免优势，并可每次长休施放一次「月光束」和「月斑」。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Selûne%27s_Spear_of_Night"
            },
            {
                "id": "bg3_shar_spear_evening",
                "name": {
                    "zh-CN": "莎尔的暮色之矛 (传奇长枪 - 黑暗免疫与遮蔽加成)",
                    "en": "Shar's Spear of Evening"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"61f31bf6-47ec-41e1-9385-2f6c26facc87\", GetHostCharacter(), 1)",
                "desc": "黑夜法官专属武器，佩戴者免疫致盲并可在魔法黑暗中视物，对处于隐蔽状态的目标攻击额外造成 1d6 伤害；可每回合施放一次「莎尔的黑暗」法术。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Shar%27s_Spear_of_Evening"
            }
        ]
    },
    {
        "category": "🏹 传奇远程武器与特殊箭矢 (Legendary Ranged Weapons & Ammo)",
        "commands": [
            {
                "id": "bg3_gontr_mael",
                "name": {
                    "zh-CN": "冈特·耶尔长弓 (传奇长弓 - 命中附加效果与急速术)",
                    "en": "Gontr Mael (Legendary Longbow)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"7e81bb6a-f465-4fe9-b1db-7ce6198246ba\", GetHostCharacter(), 1)",
                "desc": "击败钢铁巨人获得的传奇+3长弓；bg3.wiki 标注其武器类型为长弓（而非原目录所写的重弩）。命中有概率对目标施加「发光光辉」，并可每次长休使用一次「天界急速术」获得急速状态。",
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
                "desc": "将暴击所需骰值降低 1 点（可叠加，影响全部攻击），并使用该弓进行远程攻击时熟练加值翻倍。",
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
                "desc": "长弓在敏捷加成之外，额外将力量调整值加入每次远程攻击伤害，可配合力量增益药水提升输出。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Titanstring_Bow"
            },
            {
                "id": "bg3_arrows_many_targets",
                "name": {
                    "zh-CN": "弹射箭 x30 (命中后弹射至最多 3 个额外目标)",
                    "en": "Arrow of Many Targets x30"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"b11b3f7f-d8ec-41db-93b9-24474aea31e3\", GetHostCharacter(), 30)",
                "desc": "射中目标后会弹射，额外命中附近最多 3 个目标（弹射伤害为武器伤害的一半）。",
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
                "desc": "只能用于攻击巨龙，命中巨龙时造成两倍武器伤害。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Arrow_of_Dragon_Slaying"
            }
        ]
    },
    {
        "category": "🛡️ 传奇护甲与地狱火套装 (Legendary Armour & Helldusk Set)",
        "commands": [
            {
                "id": "bg3_helldusk_armor",
                "name": {
                    "zh-CN": "地狱火胸甲 (传奇重甲 - AC 21，全职业免熟练要求)",
                    "en": "Helldusk Armour (AC 21 Legendary)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"7ae705fd-1cfd-4482-a584-d2e68f9c1262\", GetHostCharacter(), 1)",
                "desc": "希望之邸拉斐尔处获得的重甲，护甲等级 21，任何职业穿戴都视为熟练；对火焰伤害有抗性且不会被点燃，并减少所受到的一切伤害 3 点。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Helldusk_Armour"
            },
            {
                "id": "bg3_helldusk_helmet",
                "name": {
                    "zh-CN": "地狱火头盔 (免疫暴击、黑暗视觉与法术豁免加值)",
                    "en": "Helldusk Helmet"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"1c198060-6b6a-41c5-82ce-a3d3c3d76404\", GetHostCharacter(), 1)",
                "desc": "佩戴后攻击者无法对佩戴者造成暴击，对法术豁免检定 +2，并获得不受黑暗影响的黑暗视觉，同时附带「灼热凝视」法术。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Helldusk_Helmet"
            },
            {
                "id": "bg3_helldusk_gloves",
                "name": {
                    "zh-CN": "地狱火手套 (武器附加火焰伤害，空手附加坏死伤害)",
                    "en": "Helldusk Gloves"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"ad219a90-ab3d-4821-8206-011293f5837b\", GetHostCharacter(), 1)",
                "desc": "武器攻击附带额外 1d6 火焰伤害，空手攻击附加 1d6 坏死伤害并可能施加流血。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Helldusk_Gloves"
            },
            {
                "id": "bg3_helldusk_boots",
                "name": {
                    "zh-CN": "地狱火靴子 (免疫强制位移与部分困难地形)",
                    "en": "Helldusk Boots"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"bc82f909-ade5-4ada-9b94-cec7ca1d4a68\", GetHostCharacter(), 1)",
                "desc": "佩戴后不会被敌方效果强制击退或移动，并免疫熔岩、泥浆、藤蔓、蛛网等困难地形的减速效果；另附带「地狱爬行」瞬移技能，落地造成范围火焰伤害。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Helldusk_Boots"
            },
            {
                "id": "bg3_helm_of_balduran",
                "name": {
                    "zh-CN": "博德安的头盔 (每回合回复生命与免疫暴击)",
                    "en": "Helm of Balduran"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"0a64283a-1fc4-45cd-9e5e-f463f6b762ea\", GetHostCharacter(), 1)",
                "desc": "博德之门创始人留下的头盔，提供 AC 和豁免 +1，战斗中每回合开始恢复 2 点生命，并使佩戴者免疫暴击和大部分致晕效果（部分特殊致晕来源除外）。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Helm_of_Balduran"
            },
            {
                "id": "bg3_viconia_shield",
                "name": {
                    "zh-CN": "维康尼亚的行走要塞 (传奇盾牌 - +3AC 与反击效果)",
                    "en": "Viconia's Walking Fortress (Legendary Shield)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"4f313dde-14bb-43a2-abdd-07b2eb38b33a\", GetHostCharacter(), 1)",
                "desc": "击败维康尼亚获得的盾牌，提供 +3 护甲等级与对抗法术的豁免优势；被近战攻击命中时可用反应造成力场伤害并尝试将敌人击倒在地。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Viconia%27s_Walking_Fortress"
            },
            {
                "id": "bg3_bhaalist_armour",
                "name": {
                    "zh-CN": "巴尔信徒护甲 (周围敌人穿刺伤害易伤光环)",
                    "en": "Bhaalist Armour (Aura of Murder)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"443b2caf-8d36-42cf-b389-d774229ed18c\", GetHostCharacter(), 1)",
                "desc": "刺客/弓手向流派防具，使周围 3 米内非穿刺免疫的敌人穿刺伤害翻倍，并获得 +2 先攻加值。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Bhaalist_Armour"
            },
            {
                "id": "bg3_vest_soul_rejuvenation",
                "name": {
                    "zh-CN": "灵魂复苏胸甲 (AC+2，法术豁免回血与反击)",
                    "en": "Vest of Soul Rejuvenation"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"1c69a87e-9136-4e13-90af-c0f02d0fc81f\", GetHostCharacter(), 1)",
                "desc": "防具提供 AC+2，法术豁免成功时回复 1d4 生命值；敌人近战攻击落空时可用反应发动一次徒手反击。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Vest_of_Soul_Rejuvenation"
            }
        ]
    },
    {
        "category": "💍 传奇首饰与戒指 (Legendary Rings & Amulets)",
        "commands": [
            {
                "id": "bg3_amulet_greater_health",
                "name": {
                    "zh-CN": "高等健康护符 (体质设为 23 点)",
                    "en": "Amulet of Greater Health (Con 23)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"5ed63342-30c9-456d-9a57-a88c8596c0c9\", GetHostCharacter(), 1)",
                "desc": "若佩戴者当前体质低于 23，会将其体质属性设为 23 点（体质已达到或超过 23 时无效），从而提高生命值上限。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Amulet_of_Greater_Health"
            },
            {
                "id": "bg3_gauntlets_hill_giant",
                "name": {
                    "zh-CN": "山丘巨人力量手套 (力量设为 23 点)",
                    "en": "Gauntlets of Hill Giant Strength (Str 23)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"9481aa27-ce9c-414c-84ff-5e974fd64d89\", GetHostCharacter(), 1)",
                "desc": "若佩戴者当前力量低于 23，会将其力量属性设为 23 点（力量已达到或超过 23 时无效）。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Gauntlets_of_Hill_Giant_Strength"
            },
            {
                "id": "bg3_ring_regeneration",
                "name": {
                    "zh-CN": "再生之戒 (战斗中每回合回复 1d4 生命值)",
                    "en": "Ring of Regeneration"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"d6ee2594-7373-4fed-a167-f9d95cb4ecfd\", GetHostCharacter(), 1)",
                "desc": "洛若坎出售的戒指，战斗中每回合开始时恢复 1d4 生命值（非战斗状态下无效，角色倒地时也不会触发）。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Ring_of_Regeneration"
            },
            {
                "id": "bg3_risky_ring",
                "name": {
                    "zh-CN": "风险之戒 (攻击掷骰优势，但豁免检定劣势)",
                    "en": "Risky Ring (All Attack Rolls Advantage)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"6fa51fb6-0c99-4e2e-bf3c-f4fe18fd64a7\", GetHostCharacter(), 1)",
                "desc": "佩戴后所有攻击掷骰获得优势，但豁免检定会因此获得劣势，是有取舍的戒指。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Risky_Ring"
            },
            {
                "id": "bg3_ring_free_action",
                "name": {
                    "zh-CN": "自由行动之戒 (免疫麻痹、束缚与困难地形)",
                    "en": "Ring of Free Action"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"50379f58-7892-44cb-be6e-146a60070055\", GetHostCharacter(), 1)",
                "desc": "佩戴后免疫麻痹、束缚（Restrained）以及困难地形的减速效果，但不能免疫冰面、油脂等打滑效果。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Ring_of_Free_Action"
            },
            {
                "id": "bg3_killer_sweetheart",
                "name": {
                    "zh-CN": "杀手的甜心戒指 (击杀后下一次攻击必定暴击)",
                    "en": "Killer's Sweetheart"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"2f2d4bf3-6a14-43f5-81fe-e14aa9871215\", GetHostCharacter(), 1)",
                "desc": "击杀敌人后触发，下一次武器攻击必定暴击，每次长休只能触发一次。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Killer%27s_Sweetheart"
            }
        ]
    },
    {
        "category": "📜 全职业 6 环魔法卷轴 (Level 6 Scrolls)",
        "commands": [
            {
                "id": "bg3_scroll_globe_invulnerability",
                "name": {
                    "zh-CN": "Globe of Invulnerability 卷轴 x10（法术无效结界）",
                    "en": "Scroll of Globe of Invulnerability x10"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"8d4c06d1-e504-49b0-a4fa-5179ab717f1e\", GetHostCharacter(), 10)",
                "desc": "释放后在范围内形成结界，范围内生物免疫 5 环及以下的法术效果（不阻挡武器攻击等非法术伤害）。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Scroll_of_Globe_of_Invulnerability"
            },
            {
                "id": "bg3_scroll_disintegrate",
                "name": {
                    "zh-CN": "解离术卷轴 x10 (10d6+40 点力场伤害)",
                    "en": "Scroll of Disintegrate x10"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"3f737706-57ca-45e6-b0d1-45238da76329\", GetHostCharacter(), 10)",
                "desc": "对单个目标造成 10d6+40 点力场伤害，若目标生命降至 0，会化为灰烬，无法用常规方式复活。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Scroll_of_Disintegrate"
            },
            {
                "id": "bg3_scroll_chain_lightning",
                "name": {
                    "zh-CN": "链状闪电卷轴 x10 (10d8 点闪电伤害，可连锁 3 个目标)",
                    "en": "Scroll of Chain Lightning x10"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"13105f7d-55fa-4292-abfe-b9d80054b48e\", GetHostCharacter(), 10)",
                "desc": "对目标及最多 3 个额外目标造成 10d8 点闪电伤害（豁免成功减半），若目标处于潮湿状态伤害会进一步提高。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Scroll_of_Chain_Lightning"
            },
            {
                "id": "bg3_scroll_sunbeam",
                "name": {
                    "zh-CN": "阳光术卷轴 x10 (范围光耀伤害，可连续发射)",
                    "en": "Scroll of Sunbeam x10"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"049d70c4-7ea3-4b6c-af6f-44dab7813a89\", GetHostCharacter(), 10)",
                "desc": "召唤光耀射线对范围内生物造成伤害并可能致盲，不死生物与软泥怪的豁免判定处于劣势；发动后可在后续回合免费重新发射，无需消耗额外法术位。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Scroll_of_Sunbeam"
            },
            {
                "id": "bg3_scroll_freezing_sphere",
                "name": {
                    "zh-CN": "奥提路克冰封球卷轴 x10 (10d6 点范围冰冷伤害)",
                    "en": "Scroll of Otiluke's Freezing Sphere x10"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"74d0e4f0-de97-4097-a7e7-f5759a375c81\", GetHostCharacter(), 10)",
                "desc": "在目标点引发范围冰爆，造成 10d6 点冰冷伤害，并会将接触到的水面冻结成冰面。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Scroll_of_Otiluke%27s_Freezing_Sphere"
            }
        ]
    },
    {
        "category": "🧪 灵药与药剂 (Elixirs & Potions)",
        "commands": [
            {
                "id": "bg3_elixir_cloud_giant",
                "name": {
                    "zh-CN": "云巨人力量灵药 x20 (力量设为 27 点，直至长休)",
                    "en": "Elixir of Cloud Giant Strength x20 (Str 27)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"e6490cc8-7f81-4aac-95e8-a58ce5e88a31\", GetHostCharacter(), 20)",
                "desc": "饮用后将力量属性设为 27 点，效果持续至下次长休（投掷命中时效果持续 10 回合）。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Elixir_of_Cloud_Giant_Strength"
            },
            {
                "id": "bg3_elixir_bloodlust",
                "name": {
                    "zh-CN": "嗜血灵药 x20 (每回合首次击杀获得额外动作与临时生命)",
                    "en": "Bloodlust Elixir x20 (Extra Action on Kill)"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"45a775f8-2cf9-440d-b9eb-4ee5f17efca8\", GetHostCharacter(), 20)",
                "desc": "效果持续至下次长休；每回合首次击杀敌人后，获得一个额外动作和 5 点临时生命值（击晕不触发）。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Elixir_of_Bloodlust"
            },
            {
                "id": "bg3_potion_angelic_slumber",
                "name": {
                    "zh-CN": "天使轻眠药水 x10（睡 2 回合后获得长休效果）",
                    "en": "Potion of Angelic Slumber x10"
                },
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"4d801c1a-691e-47c8-88e7-78367b4e2c8e\", GetHostCharacter(), 10)",
                "desc": "饮用后睡眠 2 回合，醒来时获得长休效果；睡眠被打断则不生效。据 bg3.wiki，部分需要长休恢复的能力不会被它恢复。",
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
                "desc": "饮用后进入 3 回合急速状态：每回合多一次动作、移动速度 +9 米、AC+2，并对敏捷豁免有优势；效果结束后会陷入疲乏状态，下回合无法行动。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://bg3.wiki/wiki/Potion_of_Speed"
            }
        ]
    },
    {
        "category": "⏱️ 状态增益：急速、飞行与移动 (Status Buffs: Haste, Flight & Movement)",
        "commands": [
            {
                "id": "bg3_apply_haste",
                "name": {
                    "zh-CN": "赋予常驻急速术（HASTE）",
                    "en": "Permanent Haste Buff"
                },
                "syntax_type": "lua_function",
                "code": "Osi.ApplyStatus(GetHostCharacter(), \"HASTE\", -1)",
                "desc": "为主角施加持续生效的急速状态：每回合可额外执行一次动作，移动速度与敏捷豁免获得提升，且因手动施加不会到期触发急速结束后的疲乏状态。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://docs.baldursgate3.game/index.php?title=ApplyStatus"
            },
            {
                "id": "bg3_apply_fly",
                "name": {
                    "zh-CN": "赋予常驻飞行状态 (FLY)",
                    "en": "Permanent Fly Buff"
                },
                "syntax_type": "lua_function",
                "code": "Osi.ApplyStatus(GetHostCharacter(), \"FLY\", -1)",
                "desc": "为主角施加飞行状态，可自由飞越地形与高低差，无需走楼梯或跳跃。",
                "framework_required": "BG3 Script Extender (Norbyte)",
                "source": "https://docs.baldursgate3.game/index.php?title=ApplyStatus"
            },
            {
                "id": "bg3_apply_see_invis",
                "name": {
                    "zh-CN": "赋予常驻识破隐形状态",
                    "en": "Permanent See Invisibility"
                },
                "syntax_type": "lua_function",
                "code": "Osi.ApplyStatus(GetHostCharacter(), \"SEE_INVISIBILITY\", -1)",
                "desc": "为主角施加识破隐形状态，使其能看见附近范围内隐形的敌人。",
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
        "desc": "向背包增加 10 万金币，可用于购买装备和物资。",
        "source": "https://docs.baldursgate3.game/index.php?title=AddGold"
    },
    {
        "name": {"zh-CN": "获得夺心魔寄生虫标本 x30", "en": "Add 30 Illithid Parasites"},
        "command": "Osi.TemplateAddTo(\"1ec327be-3b7f-4502-9586-860e057e09ae\", GetHostCharacter(), 30)",
        "desc": "一次性获得 30 个夺心魔寄生虫标本，可用于解锁主角与队友的灵能异能。",
        "source": "https://bg3.wiki/wiki/Mind_Flayer_Parasite_Specimen"
    },
    {
        "name": {"zh-CN": "获得博德安的巨人杀手巨剑 (传奇双手巨剑)", "en": "Add Balduran's Giantslayer"},
        "command": "Osi.TemplateAddTo(\"7219fca3-5f41-43a0-8253-f4c09d8b6308\", GetHostCharacter(), 1)",
        "desc": "获得攻击伤害额外附加两倍力量调整值、并带有「巨人体型」技能的双手巨剑。",
        "source": "https://bg3.wiki/wiki/Balduran%27s_Giantslayer"
    },
    {
        "name": {"zh-CN": "获得地狱火全套胸甲 (21AC全职业免熟练)", "en": "Add Helldusk Armour"},
        "command": "Osi.TemplateAddTo(\"7ae705fd-1cfd-4482-a584-d2e68f9c1262\", GetHostCharacter(), 1)",
        "desc": "获得拉斐尔掉落的重甲，AC 21，任何职业穿戴都视为熟练，并对火焰伤害有抗性。",
        "source": "https://bg3.wiki/wiki/Helldusk_Armour"
    },
    {
        "name": {"zh-CN": "赋予常驻急速术 (HASTE)", "en": "Permanent Haste Buff"},
        "command": "Osi.ApplyStatus(GetHostCharacter(), \"HASTE\", -1)",
        "desc": "持续施加急速状态：每回合多一次动作、移动速度提升，且因手动施加不会到期陷入疲乏状态。",
        "source": "https://docs.baldursgate3.game/index.php?title=ApplyStatus"
    }
]

bg3_mods = [
    {
        "id": "bg3-script-extender",
        "title": "BG3 Script Extender (bg3se)",
        "author": "Norbyte",
        "category": "核心底层工具 (Core Utility / Framework)",
        "desc": "博德之门3的底层模组框架，通过劫持 DWrite.dll 开启游戏内置的 Osiris 控制台，是许多高级 Mod 运行所需的前置库。",
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
        "desc": "解除捏脸、背包与战斗界面的布局限制，支持 21:9 / 32:9 宽屏分辨率，并修复部分 Mod 导致的对话黑框与捏脸滑条重叠问题。",
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
        "desc": "将联机人数上限提升至 8 人，单人战役的队伍人数上限提升至 16 人，可让所有同伴（影心、阿斯代伦、卡菈克、盖尔、莱埃泽尔等）同时随队。",
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
        "desc": "将龙与地下城第五版规则书中拉瑞安未采用的 100 余个法术（如绿色火焰之刃、寒冰之触、闪电箭、心灵尖刺等）添加到全部职业的法术列表中，并参考官方数值进行平衡。",
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
        "desc": "解除原版镜头俯仰角被限制在 45 度以内的限制，可将镜头下压至接近水平视角，实现越肩第三人称视角。",
        "dependencies": [
            "BG3 Script Extender"
        ],
        "installPath": "Baldur's Gate 3\\bin\\NativeMods\\",
        "installSteps": [
            "1. 确保已安装 BG3 Script Extender；",
            "2. 将 NativeCameraTweaks.dll 与 .ini 放入 bin\\NativeMods\\ 目录；",
            "3. 游戏中滚动鼠标滚轮即可调整镜头俯仰角度。"
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
        "desc": "使用键盘 WASD 键直接控制角色移动，替代鼠标点地寻路；配合 Native Camera Tweaks 可实现越肩第三人称视角的操控方式。",
        "dependencies": [
            "Native Camera Tweaks"
        ],
        "installPath": "Baldur's Gate 3\\bin\\NativeMods\\",
        "installSteps": [
            "1. 将 wasd.dll 与 wasd.ini 放入 bin\\NativeMods 目录；",
            "2. 游戏中按 CapsLock 键可在鼠标点击模式与键盘直控模式间切换。"
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
        "desc": "为人类、精灵、半精灵、卓尔、提夫林等种族的男女角色新增数十款长发、辫发与发饰造型，可在捏脸界面中选择。",
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
            "zh-CN": "1. 【下载与部署前置】下载最新版 Norbyte's BG3 Script Extender，解压得到 DWrite.dll 文件；\n2. 【放置主程序目录】将 DWrite.dll 复制放入《博德之门3》安装根目录的 bin\\ 文件夹下（与 bg3.exe 和 bg3_dx11.exe 位于同一级目录）；\n3. 【启用控制台黑窗】在 bin\\ 目录下新建一个文本文件并重命名为 ScriptExtenderSettings.json，用记事本打开填入 {\"CreateConsole\": true} 并保存；\n4. 【呼出与代码执行】启动游戏，屏幕旁会弹出一个 Script Extender 的控制台终端窗口；在控制台窗口内按一下回车键进入输入模式，把下列任意 Osi 函数指令粘贴进去再按回车执行，效果会直接作用在当前操控的角色身上。\n5. 【Patch 7 官方模组工坊说明】拉瑞安官方在 Patch 7 中内置了官方模组浏览器，本站整理的指令和精选 Mod 没有针对 Patch 7 及之后的版本逐一实测，装 Mod 前先看 Mod 页面写的支持版本。",
            "en": "1. Download Norbyte's BG3 Script Extender and extract DWrite.dll.\n2. Place DWrite.dll into 'Baldur's Gate 3\\bin\\' (same folder as bg3.exe).\n3. In bin\\, create ScriptExtenderSettings.json containing '{\"CreateConsole\": true}'.\n4. Launch the game; a Script Extender console terminal window will open alongside it. Press Enter in that window to enter input mode, then paste any Osi command below and press Enter — it runs against your currently controlled character.\n5. The commands and mods listed here were not individually tested on Patch 7 or later; check each mod page for the game versions it supports."
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
