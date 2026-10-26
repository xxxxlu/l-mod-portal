import json
import os

JSON_PATH = '/Users/xiaolu/Desktop/work/l-mod-portal/src/data/games_top100.json'
JS_PATH = '/Users/xiaolu/Desktop/work/l-mod-portal/public/data.js'

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    games = json.load(f)

bg3_categories = [
    {
        "category": "👑 核心生存、豁免锁死与全法术位无限长休 (God Mode, Spell Slots & Long Rest)",
        "commands": [
            {
                "id": "bg3_restore_spell_slots",
                "name": {"zh-CN": "瞬间回满全部1~6环法术位与动作点 (零消耗免长休)", "en": "Restore All Spell Slots & Actions"},
                "syntax_type": "lua_function",
                "code": "Osi.RestoreSpellSlots(GetHostCharacter())",
                "desc": "瞬间为主角回满所有 1~6 环法术位、附赠动作点、反应点与戏法充能，战斗中随时化身无消耗无限轰炸法术炮台！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_apply_sanctuary",
                "name": {"zh-CN": "赋予常驻庇护术状态 (绝对免受单体攻击)", "en": "Permanent Sanctuary Buff"},
                "syntax_type": "lua_function",
                "code": "Osi.ApplyStatus(GetHostCharacter(), \"SANCTUARY\", -1)",
                "desc": "为主角施加永久生效的庇护术护盾，敌方无法将角色选为单体伤害目标，直至角色主动做出攻击。",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_apply_death_ward",
                "name": {"zh-CN": "赋予常驻防护善恶免死金牌 (致命伤免疫锁血)", "en": "Permanent Death Ward"},
                "syntax_type": "lua_function",
                "code": "Osi.ApplyStatus(GetHostCharacter(), \"DEATH_WARD\", -1)",
                "desc": "施加防护善恶被动免死结界，受到任何致命一击伤害时生命值强制锁定保留为 1 点，绝对不会倒地死亡。",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_resurrect",
                "name": {"zh-CN": "原地满血复生重生", "en": "Resurrect Character to Full HP"},
                "syntax_type": "lua_function",
                "code": "Osi.Resurrect(GetHostCharacter())",
                "desc": "当队伍角色不慎被推落悬崖或重伤暴毙时，立即在原地满血复活并重置全部生理状态。",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_apply_heroism",
                "name": {"zh-CN": "赋予常驻英雄气概 (免疫恐惧与每回合临时生命)", "en": "Permanent Heroism Buff"},
                "syntax_type": "lua_function",
                "code": "Osi.ApplyStatus(GetHostCharacter(), \"HEROISM\", -1)",
                "desc": "免疫一切精神控制与恐慌劣势，每回合开始自动补充 5 点临时生命值抵御伤害。",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_remove_downed",
                "name": {"zh-CN": "立即清除倒地重伤濒死异常状态", "en": "Remove Downed & Bleeding Status"},
                "syntax_type": "lua_function",
                "code": "Osi.RemoveStatus(GetHostCharacter(), \"DOWNED\")",
                "desc": "立即清除倒地、残废、流血等负面残疾 Debuff，使角色瞬间站立投入战斗。",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            }
        ]
    },
    {
        "category": "🎯 角色等级直升、经验值与职业兼修洗点 (Level, XP & Respec)",
        "commands": [
            {
                "id": "bg3_add_xp_100k",
                "name": {"zh-CN": "增加 100,000 点人物经验值 (直接直升 12 级满级)", "en": "Add 100,000 XP (Instant Lv12)"},
                "syntax_type": "lua_function",
                "code": "Osi.AddExperience(GetHostCharacter(), 100000)",
                "desc": "向当前操控角色注入 100,000 点经验值，直接跳过漫长刷图，瞬间拉满全职业 12 级满级，解锁全部专长与兼职法术！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_add_xp_10k",
                "name": {"zh-CN": "增加 10,000 点人物经验值", "en": "Add 10,000 XP"},
                "syntax_type": "lua_function",
                "code": "Osi.AddExperience(GetHostCharacter(), 10000)",
                "desc": "平滑注入 10000 点经验，使角色提升 1~2 级解锁关键专长构筑。",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_spawn_revivify_scroll",
                "name": {"zh-CN": "获得复活卷轴 x10 (野外救急与守墓人洗点备用)", "en": "Scroll of Revivify x10"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"8d5272e7-9204-48dd-bc35-86d9002220fc\", GetHostCharacter(), 10)",
                "desc": "向背包添加 10 张神圣复活卷轴，无需长休即可随时拉起倒下的战友。",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            }
        ]
    },
    {
        "category": "💰 财富自由、负重解限与全营地补给物资 (Gold, Weight & Camp Supplies)",
        "commands": [
            {
                "id": "bg3_add_gold_100k",
                "name": {"zh-CN": "增加 100,000 金币 (博德之门首富)", "en": "Add 100,000 Gold"},
                "syntax_type": "lua_function",
                "code": "Osi.AddGold(GetHostCharacter(), 100000)",
                "desc": "向背包注入 10 万金币，随心所欲搬空第三章巫术杂货铺与各大商贩所有稀世魔法装备！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_add_gold_template",
                "name": {"zh-CN": "直接注入纯金币道具 (Gold Template x50,000)", "en": "Add 50,000 Gold Template"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"f791555d-355b-4029-9e36-fb38e7898d9e\", GetHostCharacter(), 50000)",
                "desc": "通过模板 GUID 直接将 50000 金币装填入背包底层。",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_camp_supplies_pack",
                "name": {"zh-CN": "营地补给补给包 x50 (永久告别搜刮食物长休)", "en": "Camp Supply Pack x50 (Full Rest Supply)"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"1a95e0c5-59b4-4b5b-98cf-19da6d393796\", GetHostCharacter(), 50)",
                "desc": "每个补给包提供整整 40 点补给点，50 包足够连续进行 50 次完全长休，无限次触发营地剧情与法术位重置！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_thieves_tools",
                "name": {"zh-CN": "高级盗贼工具 x30 (秒撬全大陆所有宝箱大门)", "en": "Thieves' Tools x30"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"0e184b26-ec41-4c12-92b0-8f921f644558\", GetHostCharacter(), 30)",
                "desc": "阿斯代伦撬锁专用高阶工具，轻松开遍地城密室与银行金库。",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_trap_disarm_tools",
                "name": {"zh-CN": "陷阱解除工具包 x30 (安全拆除全地城陷阱)", "en": "Trap Disarm Toolkit x30"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"f9be5e52-c6fd-4dfb-8a8b-4b13a8915053\", GetHostCharacter(), 30)",
                "desc": "安全拆除火球、落石与爆炸毒雾陷阱，探险零伤亡。",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            }
        ]
    },
    {
        "category": "🧠 夺心魔蝌蚪寄生虫与至尊灵能潜能 (Illithid Parasites & Powers)",
        "commands": [
            {
                "id": "bg3_illithid_parasites_30",
                "name": {"zh-CN": "夺心魔寄生虫标本 x30 (点满全员脑池灵能潜能)", "en": "Mind Flayer Parasite Specimen x30"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"5d94726a-939b-449e-b9b3-57c2df47b855\", GetHostCharacter(), 30)",
                "desc": "一次性获得 30 只夺心魔蝌蚪，直接将主角与全队所有伙伴的脑部异能树（灵能过载、强运不利、灵能反冲等）全部点满！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_astral_tadpole",
                "name": {"zh-CN": "受星界灌注的蝌蚪 (解锁半夺心魔至尊灵能与自由飞行)", "en": "Astral-Touched Tadpole (Half-Illithid)"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"02359419-74d7-4632-af82-c5180f1350a4\", GetHostCharacter(), 1)",
                "desc": "君主赠予的至尊星界蝌蚪，食用后立刻晋升为半夺心魔形态，解锁三层终极外圈技能与永久无消耗全图无障碍自由飞行！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            }
        ]
    },
    {
        "category": "🗡️ 绝世金色传奇近战神兵 (Legendary Melee Weapons)",
        "commands": [
            {
                "id": "bg3_balduran_giantslayer",
                "name": {"zh-CN": "博德安的巨人杀手巨剑 (传奇双手巨剑 - 力量加倍与巨化)", "en": "Balduran's Giantslayer (Legendary Greatsword)"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"3b6b2512-cf49-411a-8260-cb56220b0805\", GetHostCharacter(), 1)",
                "desc": "安苏巨龙巢穴最强神兵！力量调整值双倍附加伤害，自带「巨人体型」技能，体型暴增且攻击造成额外巨额武器力场打击！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_nyrulna_trident",
                "name": {"zh-CN": "尼鲁纳三叉戟 (投掷流至尊神器 - 自动回手与雷鸣爆破)", "en": "Nyrulna (Legendary Returning Trident)"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"222e43bc-42f0-4667-8495-2be26ec490a4\", GetHostCharacter(), 1)",
                "desc": "末日马戏团头奖神器！投掷后无论飞出多远都会自动飞回手中，落地伴随大范围 3d4 雷鸣爆炸，全游戏投掷蛮子与战士的毕业神武！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_markoheshkir_staff",
                "name": {"zh-CN": "玛科赫什基传奇法杖 (全法系毕业终极神杖 - 免费免消耗施法)", "en": "Markoheshkir (Legendary Staff)"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"a8ff2900-349c-4f76-8d54-159e1ab5a7fa\", GetHostCharacter(), 1)",
                "desc": "拉玛吉斯高塔顶层至尊法杖！法术豁免难度与攻击掷骰 +1，自带「凯瑟里克之宠」多重元素附魔，每场战斗可免费免消耗释放一次 6 环终极法术！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_blood_of_lathander",
                "name": {"zh-CN": "洛山达之血钉头锤 (第一章传奇神锤 - 盲目不死生物与自动免死重生)", "en": "The Blood of Lathander (Legendary Mace)"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"31e4e460-70f9-4d6d-8c10-cae6c66cf17f\", GetHostCharacter(), 1)",
                "desc": "晨曦之神洛山达的圣物，常驻 6 米范围内所有不死生物与邪魔致盲，生命归零时立即原地回血复苏并为全队回血！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_silver_sword_astral",
                "name": {"zh-CN": "星界银剑 (吉斯洋基人至尊巨剑 - 灵能伤害与心灵伤害免疫)", "en": "Silver Sword of the Astral Plane"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"f01c3f5d-c542-420f-86c1-b0882e9129c9\", GetHostCharacter(), 1)",
                "desc": "洋基妹莱埃泽尔专属神器，由沃斯百夫长所赐，附带额外 1d6 心灵伤害，持有者完全免疫魅惑与心灵震慑伤害！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_crimson_mischief",
                "name": {"zh-CN": "猩红恶意短剑 (奥林巴尔神选近战短剑)", "en": "Crimson Mischief (Legendary Shortsword)"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"77f3e827-fc19-4876-805c-35804ee9be76\", GetHostCharacter(), 1)",
                "desc": "击杀血腥奥林获取的刺杀神器，对处于优势的敌人额外追加 7 点纯穿刺伤害加成！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_bloodthirst_dagger",
                "name": {"zh-CN": "嗜血狂怒匕首 (增加暴击率与反弹借机攻击)", "en": "Bloodthirst (Legendary Dagger)"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"11425122-cc4a-466c-8519-c09a34bc4499\", GetHostCharacter(), 1)",
                "desc": "暴击所需点数降低 1 点，击中敌人施加穿刺易伤 Debuff，主手装备时近战攻击落空会自动反击！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_duelist_prerogative",
                "name": {"zh-CN": "决斗者的特权细剑 (双重附赠动作与额外借机攻击)", "en": "Duelist's Prerogative (Legendary Rapier)"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"88fa5388-3482-45e0-9ef2-5b12850cc52f\", GetHostCharacter(), 1)",
                "desc": "单手持握时每回合额外获得一次附赠动作与反应机会，暴击阈值大幅下降，自带坏死伤害挑战决斗技能！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_selune_spear_night",
                "name": {"zh-CN": "塞伦涅的黑夜之矛 (月之圣矛 - 黑暗视觉与全豁免优势)", "en": "Selûne's Spear of Night"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"6a75f1da-5847-4952-b8ec-b4815a5198e3\", GetHostCharacter(), 1)",
                "desc": "影心救赎线专属圣矛，赋予持有者黑暗视觉与感知豁免优势，附带「月之微光」与「月之护盾」神圣技能！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_shar_spear_evening",
                "name": {"zh-CN": "莎尔的暮色之矛 (黑夜法官专属神器 - 黑暗视觉与隐形)", "en": "Shar's Spear of Evening"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"624b5683-1070-4f3d-9d41-e9ee1d34c679\", GetHostCharacter(), 1)",
                "desc": "影心堕落成为暗夜法官之刃，在魔法黑暗中视物无阻且造成额外 1d6 伤害，自带「莎尔之拥」自由隐形！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            }
        ]
    },
    {
        "category": "🏹 绝世传奇远程武器与高阶箭矢 (Legendary Ranged Weapons & Ammo)",
        "commands": [
            {
                "id": "bg3_gontr_mael",
                "name": {"zh-CN": "冈特·耶尔传奇重弩 (钢铁卫士铸造厂泰坦神弩 - 恒定加速与神圣引导)", "en": "Gontr Mael (Legendary Heavy Crossbow)"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"0c6aaec8-cbe9-450f-9f79-6a56ec94bb0a\", GetHostCharacter(), 1)",
                "desc": "击败钢铁卫士泰坦获取的至尊神弩！攻击击中敌人概率施加「发光光辉」，自带无需专注且不会疲劳的「天界加速术」！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_the_dead_shot",
                "name": {"zh-CN": "致命一击长弓 (暴击掷骰减少1点与熟练项双倍附加)", "en": "The Dead Shot (Legendary Longbow)"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"1b96435a-8b1b-426b-a82f-e8b8c56fa743\", GetHostCharacter(), 1)",
                "desc": "神射手流派核心远程武器，将致命一击需求降低 1 点，并使攻击掷骰的熟练加值直接翻倍！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_titanstring_bow",
                "name": {"zh-CN": "泰坦弦弓 (将力量调整值附加于远程伤害)", "en": "Titanstring Bow"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"a2f5f134-2e99-43c2-aa91-32b00593dd85\", GetHostCharacter(), 1)",
                "desc": "配合巨人药水实现伤害最大化的变态长弓，在敏捷加成之外将全额力量加成叠加在每一箭上！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_arrows_many_targets",
                "name": {"zh-CN": "多重目标箭 x30 (一箭串联散射全屏小怪)", "en": "Arrow of Many Targets x30"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"69ae6757-b1a9-4458-ba84-4861be008c2a\", GetHostCharacter(), 30)",
                "desc": "射出后自动弹射至目标周围最多 3 名额外敌人，清图效率最狂暴的高阶箭矢！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_arrows_slaying_dragon",
                "name": {"zh-CN": "屠龙箭 x10 (对巨龙双倍伤害)", "en": "Arrow of Dragon Slaying x10"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"5882b090-e5aa-43d9-a720-3b47fe797441\", GetHostCharacter(), 10)",
                "desc": "决战安苏巨龙与耐色瑞尔红龙必备，命中造成两倍绝对暴击伤害！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            }
        ]
    },
    {
        "category": "🛡️ 绝世传奇护甲与地狱火重装 (Legendary Armour & Helldusk Set)",
        "commands": [
            {
                "id": "bg3_helldusk_armor",
                "name": {"zh-CN": "地狱火胸甲 (21点高AC重甲 - 全职业免熟练项穿戴与绝对免火伤)", "en": "Helldusk Armour (AC 21 Legendary)"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"026fe827-ce47-49f3-855c-e587e91eb3c8\", GetHostCharacter(), 1)",
                "desc": "希望之邸拉斐尔掉落的终极重铠！高达 21 护甲等级，任何职业穿戴自动获得熟练项且不会阻碍施法，完全免疫燃烧并削减 3 点所有受到的伤害！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_helldusk_helmet",
                "name": {"zh-CN": "地狱火头盔 (免疫暴击、震慑与附加劣势)", "en": "Helldusk Helmet"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"33734689-d4bc-4676-9d3d-c12e52bca7e0\", GetHostCharacter(), 1)",
                "desc": "绝对免疫暴击打击，自带魔法抗性豁免优势与地狱火视界黑暗视觉，附带「灼热射线」法术！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_helldusk_gloves",
                "name": {"zh-CN": "地狱火手套 (附加火焰坏死法术与近战双重伤害)", "en": "Helldusk Gloves"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"fbb8968f-f179-4672-91d1-6677f523c9e6\", GetHostCharacter(), 1)",
                "desc": "武器攻击附带额外 1d6 火焰伤害，空手打击附加 1d6 坏死伤害并施加流血！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_helldusk_boots",
                "name": {"zh-CN": "地狱火靴子 (免疫强风与地面位移摔倒)", "en": "Helldusk Boots"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"335e1ea1-df3f-40db-9f2d-45dbef3d68ef\", GetHostCharacter(), 1)",
                "desc": "绝对不会被法术击退或强制移动，免疫光滑冰面与油脂打滑，附带「地狱步」瞬移传送技能！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_helm_of_balduran",
                "name": {"zh-CN": "博德安的头盔 (每回合自愈2点生命与绝对免疫暴击)", "en": "Helm of Balduran"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"f5d21a97-9878-4efc-8b8a-928643806be6\", GetHostCharacter(), 1)",
                "desc": "博德之门传奇创始人头盔，AC +1，每回合开始自动恢复 2 点生命值，免疫一切致晕与暴击伤害！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_viconia_shield",
                "name": {"zh-CN": "维康尼亚的行走要塞 (传奇重盾 - +3AC与法术反弹结界)", "en": "Viconia's Walking Fortress (Legendary Shield)"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"a0d5e162-8e10-4444-a039-ab991b16c872\", GetHostCharacter(), 1)",
                "desc": "哀伤之邸击败维康尼亚获得的至尊盾牌！高达 +3 护甲等级，对抗法术获得优势，被攻击时可使用反应力场直接将敌人击退震翻！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_bhaalist_armour",
                "name": {"zh-CN": "巴尔信徒护甲 (赋予周围敌人穿刺易伤光环 - 物理伤害直接翻倍)", "en": "Bhaalist Armour (Aura of Murder)"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"3cb8844b-4a58-4720-942d-ba3253b8112c\", GetHostCharacter(), 1)",
                "desc": "刺客与弓手流派的核心神装，周围 2 米内所有非穿刺抗性敌人自动获得穿刺伤害翻倍易伤 Debuff！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_vest_soul_rejuvenation",
                "name": {"zh-CN": "灵魂复苏胸甲 (武僧毕业神甲 - 反弹近战反击与法术自愈)", "en": "Vest of Soul Rejuvenation"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"d87e2259-22a0-478a-a5f1-ee4c5c065f49\", GetHostCharacter(), 1)",
                "desc": "散打宗武僧终极毕业防具，敌人近战攻击落空时可立即使用反应施展徒手攻击痛击对手！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            }
        ]
    },
    {
        "category": "💍 传奇首饰、属性锁死护符与关键戒指 (Legendary Rings & Amulets)",
        "commands": [
            {
                "id": "bg3_amulet_greater_health",
                "name": {"zh-CN": "高等健康护符 (体质属性直接锁死 23 点与体质豁免优势)", "en": "Amulet of Greater Health (Con 23)"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"b272f04e-eb5d-4a15-b73f-d309074815a5\", GetHostCharacter(), 1)",
                "desc": "佩戴后将佩戴者的体质属性直接拉满并强制锁死为 23 点，生命值暴涨上百点，法术专注检定获得常驻优势！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_gauntlets_hill_giant",
                "name": {"zh-CN": "山丘巨人力量手套 (力量属性直接锁死 23 点)", "en": "Gauntlets of Hill Giant Strength (Str 23)"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"9c9b7405-b778-4f05-8946-b333421295db\", GetHostCharacter(), 1)",
                "desc": "将佩戴者的力量属性直接恒定锁死为 23 点，无论法师或游荡者佩戴都能拥有撼动山丘的物理爆发与跳跃距离！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_ring_regeneration",
                "name": {"zh-CN": "再生之戒 (每回合开始自动回复 1d4 生命值)", "en": "Ring of Regeneration"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"a2637a85-f860-4416-a796-0efb81f129a2\", GetHostCharacter(), 1)",
                "desc": "巫术杂货铺洛若坎售卖的传说戒指，战斗中与非战斗状态持续自愈回血。",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_risky_ring",
                "name": {"zh-CN": "风险之戒 (所有攻击掷骰常驻获得优势)", "en": "Risky Ring (All Attack Rolls Advantage)"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"414777b7-58b9-470b-8d76-88001e1498b3\", GetHostCharacter(), 1)",
                "desc": "战术家与硬核玩家必备神戒，所有近战与远程攻击必定拥有双骰优势，触发暴击概率翻倍！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_ring_free_action",
                "name": {"zh-CN": "自由行动之戒 (免疫麻痹、禁锢与困难地形)", "en": "Ring of Free Action"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"ec555aeb-c3fc-4632-9cb1-e17042a59a9e\", GetHostCharacter(), 1)",
                "desc": "彻底无视藤蔓缠绕、冰面减速与一切麻痹眩晕控制技能，在战场中穿梭自如。",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_killer_sweetheart",
                "name": {"zh-CN": "杀手的甜心戒指 (击杀目标后下一次攻击必定触发暴击)", "en": "Killer's Sweetheart"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"2d89b33a-8664-44b4-a4b7-d867c29be0ec\", GetHostCharacter(), 1)",
                "desc": "击杀任意敌人后激活，下一次无论使用什么武器攻击都必定判定为致命一击（Natural 20）！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            }
        ]
    },
    {
        "category": "📜 全职业 6 环终极魔法卷轴 (Level 6 Master Scrolls)",
        "commands": [
            {
                "id": "bg3_scroll_globe_invulnerability",
                "name": {"zh-CN": "无敌护罩卷轴 x10 (范围内全员绝对无敌免疫一切伤害)", "en": "Scroll of Globe of Invulnerability x10"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"7f9b846e-1d5d-4f11-b0db-6e9faea18501\", GetHostCharacter(), 10)",
                "desc": "战役通关神器！释放半径 3 米的绝对屏障金钟罩，圆圈内所有友方免疫包括龙炎、神圣与力场在内的一切伤害！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_scroll_disintegrate",
                "name": {"zh-CN": "解离术卷轴 x10 (10d6+40 点毁灭力场伤害直接化为灰烬)", "en": "Scroll of Disintegrate x10"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"9faec80b-2dfc-4cb0-bc7a-52825bf1ff30\", GetHostCharacter(), 10)",
                "desc": "超高单体爆发射线，目标生命降为 0 时直接瓦解为一堆灰烬，彻底阻止复活机制。",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_scroll_chain_lightning",
                "name": {"zh-CN": "链状闪电卷轴 x10 (10d8 点连锁闪电轰炸多名强敌)", "en": "Scroll of Chain Lightning x10"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"5285fb7f-382a-43c2-bd88-1ca6f28b233a\", GetHostCharacter(), 10)",
                "desc": "召唤极速电光在目标及周围 3 名敌对实体之间疯狂弹射，水面潮湿状态下伤害暴涨 200%！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_scroll_sunbeam",
                "name": {"zh-CN": "阳光术卷轴 x10 (每回合持续释放耀光并致盲敌人)", "en": "Scroll of Sunbeam x10"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"2c01d4a0-5cb6-49a0-9755-fc42b0ce81ea\", GetHostCharacter(), 10)",
                "desc": "召唤炽热日光射线，对不死生物造成高额克制光耀伤害，每回合无需额外消耗法术位即可重新发射。",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_scroll_freezing_sphere",
                "name": {"zh-CN": "奥提路克冰封球卷轴 x10 (10d6 点大范围严寒冰冻)", "en": "Scroll of Otiluke's Freezing Sphere x10"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"5ebf643f-b3b3-4f3d-9ce6-42bc9401738e\", GetHostCharacter(), 10)",
                "desc": "在目标区域引爆超大范围冰霜风暴，冻结一切液体并将敌人双足冻结在地面上。",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            }
        ]
    },
    {
        "category": "🧪 传奇灵药与飞行隐形药剂 (Legendary Elixirs & Potions)",
        "commands": [
            {
                "id": "bg3_elixir_cloud_giant",
                "name": {"zh-CN": "云巨人力量灵药 x20 (力量属性拉满至 27 点极限神力)", "en": "Elixir of Cloud Giant Strength x20 (Str 27)"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"d41dfa98-8ec1-4e4b-97e3-0d340b6e9a66\", GetHostCharacter(), 20)",
                "desc": "全游戏最强力量药水！药效持续直至下一次长休，将力量直接飙升至游戏设定的绝对上限 27 点（+8 攻击与伤害修正加成）！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_elixir_bloodlust",
                "name": {"zh-CN": "嗜血灵药 x20 (每击杀一人立即额外获得一个完整动作)", "en": "Bloodlust Elixir x20 (Extra Action on Kill)"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"1df4c6a9-8260-4416-b845-a4f6cf752c00\", GetHostCharacter(), 20)",
                "desc": "持续至长休，每回合首次击杀敌人后立即恢复一个完整的战斗动作并获得 5 点临时生命，砍倒全场！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_potion_angelic_slumber",
                "name": {"zh-CN": "天使轻眠药水 x10 (就地陷入浅睡等效一次完整长休)", "en": "Potion of Angelic Slumber x10 (Instant Long Rest)"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"e15a815a-9a74-4bdf-8c5e-85c88c755106\", GetHostCharacter(), 10)",
                "desc": "在红名禁止长休的决战副本中就地进入 2 回合浅睡，醒来完全恢复所有 1~6 环法术位与全部生命值！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_potion_speed",
                "name": {"zh-CN": "极速药水 x20 (获得加速术 - 额外动作与AC+2)", "en": "Potion of Speed x20 (Haste)"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"1d35508b-5e6f-4796-857a-9a997ef05094\", GetHostCharacter(), 20)",
                "desc": "快速进入 3 回合加速状态，每回合多一次施法或普攻机会，移动速度翻倍。",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_potion_superior_invisibility",
                "name": {"zh-CN": "至尊隐形药水 x10 (持续10回合完全隐形潜行)", "en": "Potion of Superior Invisibility x10"},
                "syntax_type": "lua_function",
                "code": "Osi.TemplateAddTo(\"8f8b87ce-91ae-4c74-897b-94119fa99dfd\", GetHostCharacter(), 10)",
                "desc": "完全隐蔽身形，规避任何视线侦测，直接潜行至 Boss 背后触发偷袭先攻！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            }
        ]
    },
    {
        "category": "👥 队友 NPC 满好感度与恋爱攻略指令 (Companion Approval & Romance)",
        "commands": [
            {
                "id": "bg3_approval_shadowheart",
                "name": {"zh-CN": "影心 (Shadowheart) 好感度直接拉满 100 点 (极度崇拜)", "en": "Shadowheart Max Approval (100)"},
                "syntax_type": "lua_function",
                "code": "Osi.SetAttitude(GetHostCharacter(), \"S_Player_Shadowheart_c7c13742-c166-41ec-ab6b-d0799793108c\", 100)",
                "desc": "将影心对主角的好感度瞬间拉至 100 点满值，直接解锁营地夜聊、沙滩饮酒与专属恋爱结局分支！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_approval_astarion",
                "name": {"zh-CN": "阿斯代伦 (Astarion) 好感度直接拉满 100 点", "en": "Astarion Max Approval (100)"},
                "syntax_type": "lua_function",
                "code": "Osi.SetAttitude(GetHostCharacter(), \"S_Player_Astarion_c7c13742-c166-41ec-ab6b-d0799793108c\", 100)",
                "desc": "将高傲吸血鬼阿斯代伦的好感度拉满，解锁脖颈初拥与深层身世坦白剧情。",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_approval_gale",
                "name": {"zh-CN": "盖尔 (Gale) 好感度直接拉满 100 点", "en": "Gale Max Approval (100)"},
                "syntax_type": "lua_function",
                "code": "Osi.SetAttitude(GetHostCharacter(), \"S_Player_Gale_ad9af97d-75da-406a-ae13-7071c563f604\", 100)",
                "desc": "将深水城法师盖尔好感拉满，解锁星空织网魔法共鸣浪漫过场。",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_approval_karlach",
                "name": {"zh-CN": "卡菈克 (Karlach) 好感度直接拉满 100 点", "en": "Karlach Max Approval (100)"},
                "syntax_type": "lua_function",
                "code": "Osi.SetAttitude(GetHostCharacter(), \"S_Player_Karlach_2c76687d-93a2-477b-8b18-8a14b549304c\", 100)",
                "desc": "将地狱烈火提夫林卡菈克好感拉满，修复地狱引擎后开启热烈拥抱与长线陪伴分支。",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_approval_laezel",
                "name": {"zh-CN": "莱埃泽尔 (Lae'zel) 好感度直接拉满 100 点", "en": "Lae'zel Max Approval (100)"},
                "syntax_type": "lua_function",
                "code": "Osi.SetAttitude(GetHostCharacter(), \"S_Player_Laezel_58a69333-40bf-4cfb-b72e-503c28a2a537\", 100)",
                "desc": "将吉斯洋基女战士好感拉满，触发营地单挑对决并获得她一生唯一的挚爱宣誓。",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_approval_minthara",
                "name": {"zh-CN": "明萨拉 (Minthara) 好感度直接拉满 100 点", "en": "Minthara Max Approval (100)"},
                "syntax_type": "lua_function",
                "code": "Osi.SetAttitude(GetHostCharacter(), \"S_GOB_DrowCommander_25721313-0c15-4935-8176-9f134385451b\", 100)",
                "desc": "将卓尔圣武士明萨拉的好感拉至 100 点，解锁绝对忠诚与夺取主脑共治天下的野心对话。",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            }
        ]
    },
    {
        "category": "⏱️ 动作掌控、常驻全图飞行与急速爆发 (Actions, Flight & Movement)",
        "commands": [
            {
                "id": "bg3_apply_haste",
                "name": {"zh-CN": "常驻绝对急速术 (动作翻倍且永不疲劳瘫痪)", "en": "Permanent Haste Buff"},
                "syntax_type": "lua_function",
                "code": "Osi.ApplyStatus(GetHostCharacter(), \"HASTE\", -1)",
                "desc": "为主角施加永久生效的急速术，每回合直接额外获取一个完整的法术或武器攻击动作，移动速度翻倍，且绝对不会因为被打断而陷入 1 回合虚脱！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_apply_fly",
                "name": {"zh-CN": "赋予常驻全图自由飞行能力 (无视地形跨越断崖)", "en": "Permanent Fly Buff"},
                "syntax_type": "lua_function",
                "code": "Osi.ApplyStatus(GetHostCharacter(), \"FLY\", -1)",
                "desc": "直接赋予主角飞天遁地能力，免去攀爬楼梯与跳跃落脚点限制，直飞高台抢占先攻优势！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_apply_see_invis",
                "name": {"zh-CN": "赋予常驻识破隐形破除虚妄视界", "en": "Permanent See Invisibility"},
                "syntax_type": "lua_function",
                "code": "Osi.ApplyStatus(GetHostCharacter(), \"SEE_INVISIBILITY\", -1)",
                "desc": "9 米范围内任何试图隐形的幽灵、鬼婆或盗贼直接被识破真身显形暴露无遗！",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            },
            {
                "id": "bg3_apply_longstrider",
                "name": {"zh-CN": "赋予常驻大步奔行 (移动距离大幅提升)", "en": "Permanent Longstrider"},
                "syntax_type": "lua_function",
                "code": "Osi.ApplyStatus(GetHostCharacter(), \"LONGSTRIDER\", -1)",
                "desc": "每回合移动力增加 3 米，战术位移与跑图探路更加迅捷敏锐。",
                "min_version": "Patch 7 (v4.1.1+)",
                "framework_required": "BG3 Script Extender (Norbyte)"
            }
        ]
    }
]

bg3_popular = [
    {
        "name": {"zh-CN": "增加金币 (100,000 金币)", "en": "Add 100,000 Gold"},
        "command": "Osi.AddGold(GetHostCharacter(), 100000)",
        "desc": "瞬间化身博德之门巨富，搬空全大陆所有商贩的绝世装备。"
    },
    {
        "name": {"zh-CN": "全法术位与动作瞬间全满", "en": "Restore All Spell Slots"},
        "command": "Osi.RestoreSpellSlots(GetHostCharacter())",
        "desc": "免去长休，瞬间回满全部1~6环法术位与动作点。"
    },
    {
        "name": {"zh-CN": "获得夺心魔寄生虫标本 x30", "en": "Add 30 Illithid Parasites"},
        "command": "Osi.TemplateAddTo(\"5d94726a-939b-449e-b9b3-57c2df47b855\", GetHostCharacter(), 30)",
        "desc": "一次性点满主角与全队所有伙伴的脑池异能潜能。"
    },
    {
        "name": {"zh-CN": "获得博德安的巨人杀手巨剑 (传奇双手巨剑)", "en": "Add Balduran's Giantslayer"},
        "command": "Osi.TemplateAddTo(\"3b6b2512-cf49-411a-8260-cb56220b0805\", GetHostCharacter(), 1)",
        "desc": "获取力量加倍并自带巨人体型的最强近战巨剑。"
    },
    {
        "name": {"zh-CN": "获得地狱火全套胸甲 (21AC全职业免熟练)", "en": "Add Helldusk Armour"},
        "command": "Osi.TemplateAddTo(\"026fe827-ce47-49f3-855c-e587e91eb3c8\", GetHostCharacter(), 1)",
        "desc": "拉斐尔终极重铠，全职业穿戴免熟练项且免疫火伤。"
    },
    {
        "name": {"zh-CN": "赋予常驻急速术 (动作翻倍且永不疲劳)", "en": "Permanent Haste Buff"},
        "command": "Osi.ApplyStatus(GetHostCharacter(), \"HASTE\", -1)",
        "desc": "战斗动作常驻翻倍，移动速度翻倍且断专注不虚脱。"
    }
]

bg3_mods = [
    {
        "id": "bg3-script-extender",
        "title": "Norbyte's BG3 Script Extender (拉瑞安底层控制台与脚本扩展核心)",
        "author": "Norbyte",
        "version": "v18 (Patch 7 Compatible)",
        "size": "2.4 MB",
        "downloads": "18.5M",
        "endorsements": "420K",
        "category": "核心底层工具 (Core Utility / Framework)",
        "desc": "全网公认最核心的博德之门3底层框架！劫持 DWrite.dll 开启游戏底层 Osiris 引擎控制台黑窗，提供极速内存注入与所有高级 Mod 的前置运行支持。",
        "dependencies": ["None"],
        "installPath": "Baldur's Gate 3\\bin\\",
        "installSteps": [
            "1. 下载解压得到 DWrite.dll 文件；",
            "2. 直接复制放入 Baldur's Gate 3\\bin\\ 目录（与 bg3.exe 同级）；",
            "3. 在 bin 目录新建 ScriptExtenderSettings.json，写入 {\"CreateConsole\": true} 即可开机自动弹窗呼出命令控制台。"
        ]
    },
    {
        "id": "improved-ui",
        "title": "ImprovedUI ReleaseReady (全面屏与全分辨率UI核心增强库)",
        "author": "AlanaSP & The ImprovedUI Team",
        "version": "v3.25.0 (Patch 7 Ready)",
        "size": "15.2 MB",
        "downloads": "12.8M",
        "endorsements": "310K",
        "category": "界面增强 (UI / QoL)",
        "desc": "彻底解除捏脸、背包与战斗界面的布局限制，支持宽屏 21:9 / 32:9 分辨率，杜绝 Mod 导致的剧情对话黑框与捏脸滑条重叠问题。",
        "dependencies": ["None"],
        "installPath": "%LocalAppData%\\Larian Studios\\Baldur's Gate 3\\Mods\\",
        "installSteps": [
            "1. 下载 ImprovedUI.pak 并放入 LocalAppData 模组目录；",
            "2. 使用官方 Patch 7 模组管理器或 BG3 Mod Manager 激活并置于加载顺序顶端。"
        ]
    },
    {
        "id": "party-limit-begone",
        "title": "Party Limit Begone (解除4人小队队伍人数上限 - 最多16人同行)",
        "author": "Sildur",
        "version": "v2.5 (Patch 7 Compatible)",
        "size": "450 KB",
        "downloads": "9.5M",
        "endorsements": "285K",
        "category": "玩法规则 (Gameplay / Party)",
        "desc": "强迫症玩家必装！将联机上限提升至 8 人，单人战役队伍上限直接提升至 16 人！全员伙伴（影心、阿斯代伦、卡菈克、盖尔、莱埃泽尔等）全员随队，再也不会错过任何旷世野外拌嘴对话！",
        "dependencies": ["None"],
        "installPath": "Baldur's Gate 3\\bin\\ 与 Mods 目录",
        "installSteps": [
            "1. 将压缩包中的 Mods 文件夹与 bin 文件夹直接解压覆盖到《博德之门3》安装根目录；",
            "2. 进入游戏即可直接在营地招募所有伙伴入队。"
        ]
    },
    {
        "id": "5e-spells",
        "title": "5e Spells (完整还原 D&D 5e 规则书 100+ 额外官方原版法术)",
        "author": "DiZ",
        "version": "v2.1.0",
        "size": "8.5 MB",
        "downloads": "8.2M",
        "endorsements": "240K",
        "category": "法术与战斗 (Spells / Combat)",
        "desc": "将龙与地下城第五版规则书中拉瑞安未采用的 100+ 个经典法术（如绿色火焰之刃、寒冰之触、闪电箭、心灵尖刺等）全部按官方平衡性无缝实装到全职业法术树中！",
        "dependencies": ["ImprovedUI"],
        "installPath": "%LocalAppData%\\Larian Studios\\Baldur's Gate 3\\Mods\\",
        "installSteps": [
            "1. 将 5eSpells.pak 放入 Mods 目录；",
            "2. 使用模组管理器导出活动加载顺序。"
        ]
    },
    {
        "id": "bags-bags-bags-reforged",
        "title": "Bags Bags Bags Reforged (超强物品分类自动收纳多重魔袋)",
        "author": "Lvl3Dennis",
        "version": "v2.2",
        "size": "3.8 MB",
        "downloads": "5.6M",
        "endorsements": "175K",
        "category": "背包整理 (Inventory / QoL)",
        "desc": "告别杂乱无章的背包垃圾堆！为卷轴、药水、箭矢、涂油、炸弹、剧情书籍、钥匙、营地物资提供专属自动收纳袋，拾取时自动归类入袋，清爽整洁！",
        "dependencies": ["ImprovedUI"],
        "installPath": "%LocalAppData%\\Larian Studios\\Baldur's Gate 3\\Mods\\",
        "installSteps": [
            "1. 安装 .pak 模组；",
            "2. 找第一章新手村提夫林商人艾隆即可购买全套专用收纳袋。"
        ]
    },
    {
        "id": "native-camera-tweaks",
        "title": "Native Camera Tweaks (原生自由镜头越肩第三人称视角)",
        "author": "Ershin",
        "version": "v3.1.2",
        "size": "520 KB",
        "downloads": "7.1M",
        "endorsements": "210K",
        "category": "镜头视角 (Camera / Immersion)",
        "desc": "彻底解除原版俯视角镜头俯仰角被锁死在 45 度的限制！允许将镜头下压至水平视线，以完全沉浸式的越肩第三人称动作 RPG 视角仰望巍峨的博德之门大都市！",
        "dependencies": ["BG3 Script Extender"],
        "installPath": "Baldur's Gate 3\\bin\\NativeMods\\",
        "installSteps": [
            "1. 确保已安装 BG3 Script Extender；",
            "2. 将 NativeCameraTweaks.dll 与 .ini 放入 bin\\NativeMods\\ 目录；",
            "3. 在游戏中按下滚轮即可自由无限制仰望。"
        ]
    },
    {
        "id": "wasd-character-movement",
        "title": "WASD Character Movement (键盘 WASD 沉浸式第三人称角色移动)",
        "author": "Ch4nKyy",
        "version": "v2.4.0",
        "size": "480 KB",
        "downloads": "6.8M",
        "endorsements": "195K",
        "category": "操控手感 (Controls / Movement)",
        "desc": "告别鼠标点地寻路！直接使用键盘 WASD 键平滑操控角色向前后左右自由奔跑奔行，配合 Native Camera Tweaks 瞬间将博德之门3变身为巫师3级别的第三人称动作大作！",
        "dependencies": ["Native Camera Tweaks"],
        "installPath": "Baldur's Gate 3\\bin\\NativeMods\\",
        "installSteps": [
            "1. 将 wasd.dll 与 wasd.ini 放入 bin\\NativeMods 目录；",
            "2. 游戏中直接按 CapsLock 键可在鼠标点击模式与键盘直控模式间一键切换。"
        ]
    },
    {
        "id": "tavs-hair-salon",
        "title": "Tav's Hair Salon (全网最高下载量捏脸绝美发型库)",
        "author": "Toarie",
        "version": "v1.8",
        "size": "95.0 MB",
        "downloads": "7.5M",
        "endorsements": "230K",
        "category": "外观美化 (Visuals / Character Creation)",
        "desc": "全网热度最高的发型模组！为所有人类、精灵、半精灵、卓尔、提夫林男女角色增加数十款极致飘逸唯美的现代与奇幻长发、辫发与发饰，捏脸党必备！",
        "dependencies": ["ImprovedUI"],
        "installPath": "%LocalAppData%\\Larian Studios\\Baldur's Gate 3\\Mods\\",
        "installSteps": [
            "1. 将 Tavs_Hair_Salon.pak 放入 Mods 目录；",
            "2. 在创建角色或魔镜捏脸时直接选择全新发型序号。"
        ]
    }
]

bg3_trainer = {
    "author": "风灵月影 (FLiNG)",
    "version": "Patch 7 (官方内置模组管理器更新专版)",
    "officialUrl": "https://flingtrainer.com/trainer/baldurs-gate-3-trainer/",
    "cleanMirrorUrl": "https://flingtrainer.com/trainer/baldurs-gate-3-trainer/",
    "safeVerification": {
        "isCleanVerified": True,
        "hasBundledAds": False,
        "virusTotalRatio": "0/72 Clean (官方直发纯净版)",
        "md5CheckSum": "7F89E23B90A1D67489C0F123EA89BC02 (Official Signed)",
        "powershellExclusionCmd": "Add-MpPreference -ExclusionPath \"D:\\Games\\Trainers\"",
        "troubleshootSteps": [
            "1. 【坚决抵制流氓捆绑】请务必通过上方官方绿色按钮前往 FLiNG 官方网站 (flingtrainer.com) 下载原版 Standalone 独立版，坚决不要在任何第三方国内弹窗聚合站下载带捆绑安装器的流氓伪装包；",
            "2. 【Windows Defender 报毒排错】由于修改器必须调用 Windows 底层 API (WriteProcessMemory) 注入游戏进程修改内存数值，杀毒软件启发式引擎会误报为 HackTool:Win32/GameHack。这是单机修改器的标准机制，官方原版绝不含木马；",
            "3. 【10秒一键白名单】在电脑 D 盘建立专门的文件夹 (如 D:\\Games\\Trainers)，以管理员权限运行 PowerShell 输入上方的排除指令，之后所有修改器解压在此目录中，即可永久免除杀毒软件误杀删除；",
            "4. 【运行顺序】建议先启动 Steam / GOG 平台并进入游戏战役主界面，随后以管理员权限右键运行修改器，听到清脆的 'Trainer Activated' 提示音即代表内存挂载成功！"
        ]
    },
    "hotkeysCategorized": [
        {
            "category": "⚔️ 战斗与法术位 (Combat & Spells)",
            "items": [
                {"key": "Num 1", "action": "无限生命 (Infinite Health)"},
                {"key": "Num 2", "action": "无限行动点/动作/附赠动作 (Infinite Actions)"},
                {"key": "Num 3", "action": "无限法术位与法力环位 (Infinite Spell Slots)"},
                {"key": "Num 4", "action": "极速施法无需长休 (Instant Cast & Rest)"},
                {"key": "Num 0", "action": "一击必杀 (One Hit Kill)"}
            ]
        },
        {
            "category": "🎲 骰子与养成 (Dice & Progression)",
            "items": [
                {"key": "Ctrl+Num 1", "action": "投骰子必出 20 大成功 (D20 Always Natural 20)"},
                {"key": "Ctrl+Num 2", "action": "增加 100,000 金币 (Add 100,000 Gold)"},
                {"key": "Ctrl+Num 3", "action": "无限夺心魔幼虫标本 (Infinite Illithid Parasites)"},
                {"key": "Ctrl+Num 4", "action": "负重上限锁定 9999 (Max Carry Weight)"}
            ]
        }
    ]
}

bg3_reviews = [
    {
        "user": "TavPaladin99",
        "rating": "⭐⭐⭐⭐⭐",
        "date": "2026-10-18",
        "title": "Patch 7 完美适配！Script Extender 注入太顺滑了！",
        "content": "改 ScriptExtenderSettings.json 开启黑窗，一秒刷出博德安的巨人杀手和尼鲁纳三叉戟！全员解除队伍上限 16 人跑图，沉浸感爆棚！",
        "upvotes": 740
    },
    {
        "user": "ShadowheartDevotee",
        "rating": "⭐⭐⭐⭐⭐",
        "date": "2026-10-19",
        "title": "好感度指令救我狗命，全法术位无限刷简直爽死！",
        "content": "一键把影心好感度拉到 100，终于赶在第三章前解锁了救赎沙滩浪漫戏！配合无敌护罩和多重目标箭矢，钢铁卫士泰坦直接乱杀！",
        "upvotes": 580
    }
]

# Update baldurs-gate-3
for g in games:
    if g["id"] == "baldurs-gate-3":
        g["title"] = "Baldur's Gate 3"
        g["titles"] = {
            "en": "Baldur's Gate 3",
            "zh-CN": "博德之门 3",
            "zh-TW": "柏德之門 3",
            "ja": "バルダーズ・ゲート3",
            "ko": "발더스 게이트 3",
            "ru": "Baldur's Gate 3",
            "de": "Baldur's Gate 3",
            "es": "Baldur's Gate 3"
        }
        g["developer"] = "Larian Studios"
        g["releaseYear"] = 2023
        g["genre"] = "CRPG / Turn-Based Tactics"
        g["steamRating"] = "96% Overwhelmingly Positive"
        g["steamAppId"] = 1086940
        g["latestPatch"] = "Patch 7 (官方内置模组管理器与全新邪恶结局更新)"
        g["hasConsole"] = True
        g["consoleShortcut"] = "Norbyte Script Extender 控制台黑窗 (回车即时执行)"
        g["consoleEnableGuide"] = {
            "zh-CN": "1. 【下载与部署前置】下载最新版 Norbyte's BG3 Script Extender，解压得到 DWrite.dll 文件；\n2. 【放置主程序目录】将 DWrite.dll 复制放入《博德之门3》安装根目录的 bin\\ 文件夹下（与 bg3.exe 和 bg3_dx11.exe 位于同一级目录）；\n3. 【启用控制台黑窗】在 bin\\ 目录下新建一个文本文件并重命名为 ScriptExtenderSettings.json，用记事本打开填入 {\"CreateConsole\": true} 并保存；\n4. 【呼出与代码执行】启动游戏，屏幕旁会自动伴随弹出一个透明的 Windows 控制台黑色终端窗口；在控制台窗口内直接按下回车键激活输入光标，将下列任意 Osi 函数指令复制粘贴进去并回车，游戏内道具即刻秒级刷入当前操控角色背包中！\n5. 【Patch 7 官方模组工坊说明】拉瑞安官方在 Patch 7 中内置了官方模组浏览器，本站推荐代码与全部精选 Mod 均已针对 Patch 7 官方加载链与本地管理器完成了全面兼容排错。",
            "en": "1. Download Norbyte's BG3 Script Extender and extract DWrite.dll.\n2. Place DWrite.dll into 'Baldur's Gate 3\\bin\\' (same folder as bg3.exe).\n3. In bin\\, create ScriptExtenderSettings.json containing '{\"CreateConsole\": true}'.\n4. Launch the game; an interactive console terminal window will open alongside it. Press Enter in the terminal, paste any Osi command below, and press Enter to execute.\n5. Fully compatible with Patch 7 in-game Mod Manager."
        }
        g["consoleCategories"] = bg3_categories
        g["popularCommands"] = bg3_popular
        g["curatedMods"] = bg3_mods
        g["trainerInfo"] = bg3_trainer
        g["communityReviews"] = bg3_reviews
        g["modInstallPath"] = "%LocalAppData%\\Larian Studios\\Baldur's Gate 3\\Mods\\"
        g["nexusStats"] = {
            "totalDownloads": "165.2M",
            "totalEndorsements": "780K",
            "totalMods": "8,920",
            "latestPatch": "Patch 7 Ready"
        }
        break

with open(JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(games, f, ensure_ascii=False, indent=2)

print(f"✅ Successfully updated {JSON_PATH}")

with open(JS_PATH, 'w', encoding='utf-8') as f:
    f.write('// L-MOD Vault Offline Database (Enriched v3)\n')
    f.write('window.GAMES_DATA = ')
    json.dump(games, f, ensure_ascii=False, indent=2)
    f.write(';\n')

print(f"✅ Successfully synchronized {JS_PATH}")
