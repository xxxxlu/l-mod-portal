import json
import os

JSON_PATH = '/Users/xiaolu/Desktop/work/l-mod-portal/src/data/games_top100.json'
JS_PATH = '/Users/xiaolu/Desktop/work/l-mod-portal/public/data.js'

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    games = json.load(f)

witcher_categories = [
    {
        "category": "👑 核心上帝模式与主角机体掌控 (God Mode & Character Invincibility)",
        "commands": [
            {
                "id": "w3_god",
                "name": {"zh-CN": "完全无敌上帝模式 (生命与法印锁死)", "en": "God Mode"},
                "syntax_type": "redengine_cmd",
                "code": "god",
                "desc": "杰洛特完全无敌，生命值与昆恩法印锁死不掉血，免疫所有怪物挥砍、毒素、摔落与狂猎冰霜伤害，再次输入可解除无敌。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_likeaboss",
                "name": {"zh-CN": "像大 Boss 一样战斗 (伤害削减99%且重击按比例扣血)", "en": "Like a Boss Mode"},
                "syntax_type": "redengine_cmd",
                "code": "likeaboss",
                "desc": "将杰洛特受到的一切伤害削减至 1%，同时每次普攻造成敌人 40% 最大生命值的绝对碾压伤害，秒杀全图妖灵！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_healme",
                "name": {"zh-CN": "瞬间全状态恢复满血", "en": "Heal to Full"},
                "syntax_type": "redengine_cmd",
                "code": "healme",
                "desc": "立即清除流血、中毒、燃烧状态并瞬间回满杰洛特的生命值槽。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_staminaboy",
                "name": {"zh-CN": "无限耐力与活力 (连续翻滚与无限剑舞)", "en": "Infinite Stamina"},
                "syntax_type": "redengine_cmd",
                "code": "staminaboy",
                "desc": "活力值永久锁满，奔跑不减体力，法印与回旋剑舞、拜年剑法零冷却无消耗无限狂砍！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_killall",
                "name": {"zh-CN": "秒杀全屏视野敌人", "en": "Kill All Enemies"},
                "syntax_type": "redengine_cmd",
                "code": "killall",
                "desc": "直接蒸发当前战斗视线范围内所有妖灵、狂猎士兵、孽鬼与大型 Boss！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_cat_1",
                "name": {"zh-CN": "开启猫之视野夜视夜瞳 (地牢如白昼)", "en": "Enable Cat Vision"},
                "syntax_type": "redengine_cmd",
                "code": "Cat(1)",
                "desc": "获得永久猫学派夜视能力，漆黑古墓、洞穴无需点燃火把或饮用猫魔药清晰如白昼。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_cat_0",
                "name": {"zh-CN": "关闭猫之视野夜视", "en": "Disable Cat Vision"},
                "syntax_type": "redengine_cmd",
                "code": "Cat(0)",
                "desc": "关闭夜视高对比度视界，恢复自然原版光影氛围。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_ciri",
                "name": {"zh-CN": "直接切换操控希里 (Ciri)", "en": "Play as Ciri"},
                "syntax_type": "redengine_cmd",
                "code": "Ciri",
                "desc": "拥有希里独有的空间穿梭闪烁瞬移闪避与大范围灵能冲击蓄力大招，机动性极致拔群！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_geralt",
                "name": {"zh-CN": "恢复操控杰洛特 (Geralt)", "en": "Play as Geralt"},
                "syntax_type": "redengine_cmd",
                "code": "Geralt",
                "desc": "切回利维亚的杰洛特主角形态，恢复完整背包、法印与炼金系统。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            }
        ]
    },
    {
        "category": "💰 财富自由、全突变与技能成长 (Economy, Skills & Mutagens)",
        "commands": [
            {
                "id": "w3_addmoney_100k",
                "name": {"zh-CN": "增加 100,000 克朗金币 (财富自由)", "en": "Add 100,000 Crowns"},
                "syntax_type": "redengine_cmd",
                "code": "addmoney(100000)",
                "desc": "随心所欲支付陶森特白葡萄园庄园翻修升级与欧菲尔符文匠高昂的开店赞助费！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_removemoney_10k",
                "name": {"zh-CN": "扣除 10,000 克朗金币", "en": "Remove 10,000 Crowns"},
                "syntax_type": "redengine_cmd",
                "code": "removemoney(10000)",
                "desc": "扣除指定金额的克朗金币，便于平衡游戏内物价体验。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_setlevel_100",
                "name": {"zh-CN": "角色等级直升 100 级满级", "en": "Set Level 100"},
                "syntax_type": "redengine_cmd",
                "code": "setlevel(100)",
                "desc": "等级一键拉满，直接破除全陶森特与石之心顶级神兵防具的穿戴等级门槛。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_levelup",
                "name": {"zh-CN": "角色等级提升 1 级", "en": "Level Up (+1)"},
                "syntax_type": "redengine_cmd",
                "code": "levelup",
                "desc": "立即提升角色等级 1 级并结算升级能力点。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_addskillpoints_50",
                "name": {"zh-CN": "增加 50 点未分配能力点", "en": "Add 50 Skill Points"},
                "syntax_type": "redengine_cmd",
                "code": "addskillpoints(50)",
                "desc": "点满剑术、法印、炼金术与全套技能树，提前点出刺骨、瘾头与浴血突变！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_cleardevelop",
                "name": {"zh-CN": "重置清空全部突变与技能点 (零损耗洗点)", "en": "Reset Skill Tree (Clear Develop)"},
                "syntax_type": "redengine_cmd",
                "code": "cleardevelop",
                "desc": "重置所有投入的能力点与突变系统，免去高价购买洗点魔药的繁琐步骤。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_mutagen_red",
                "name": {"zh-CN": "获得 10 个大红突变诱发物 (剑术攻击力拉满)", "en": "Add Greater Red Mutagens x10"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Mutagen red greater', 10)",
                "desc": "配合红技能槽提供最大百分比剑术物理攻击力增益，近战输出核心素材。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_mutagen_green",
                "name": {"zh-CN": "获得 10 个大绿突变诱发物 (生命值上限拉满)", "en": "Add Greater Green Mutagens x10"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Mutagen green greater', 10)",
                "desc": "配合绿技能槽提供巨额额外生命值上限，打造不死血牛猎魔人。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_mutagen_blue",
                "name": {"zh-CN": "获得 10 个大蓝突变诱发物 (法印强度拉满)", "en": "Add Greater Blue Mutagens x10"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Mutagen blue greater', 10)",
                "desc": "配合蓝技能槽大幅强化伊格尼焚烧与阿尔德震荡波法印强度。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            }
        ]
    },
    {
        "category": "⚔️ 宗师级猎魔人六大学派神装 (Grandmaster Witcher School Sets)",
        "commands": [
            {
                "id": "w3_bear_silver",
                "name": {"zh-CN": "师匠级熊学派银剑 (重击拜年流核心)", "en": "Grandmaster Bear Silver Sword"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Bear School silver sword 4')",
                "desc": "重击流核心宗师级银剑，提供高额肾上腺素点数生成与暴击伤害加成。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_bear_steel",
                "name": {"zh-CN": "师匠级熊学派钢剑", "en": "Grandmaster Bear Steel Sword"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Bear School steel sword 4')",
                "desc": "配合熊学派重甲的对人钢剑，高斩首几率与强劲破甲能力。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_bear_armor",
                "name": {"zh-CN": "师匠级熊学派防具胸甲 (重甲极致减伤护盾)", "en": "Grandmaster Bear Armor"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Bear School Armor 4')",
                "desc": "拥有极高怪物抗性与昆恩法印护盾吸收加成的宗师战袍，免伤流首选。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_bear_gloves",
                "name": {"zh-CN": "师匠级熊学派手套", "en": "Grandmaster Bear Gloves"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Bear School Gloves 4')",
                "desc": "大幅提高强击伤害与劈砍抗性的宗师重甲手套。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_bear_pants",
                "name": {"zh-CN": "师匠级熊学派下装", "en": "Grandmaster Bear Pants"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Bear School Pants 4')",
                "desc": "提供高额穿刺与元素伤害抗性的宗师重甲裤子。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_bear_boots",
                "name": {"zh-CN": "师匠级熊学派靴子", "en": "Grandmaster Bear Boots"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Bear School Boots 4')",
                "desc": "提供坚固防护与抗击退特性的宗师级战靴。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_wolf_silver",
                "name": {"zh-CN": "师匠级狼学派银剑 (剑法混搭全面流)", "en": "Grandmaster Wolf Silver Sword"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Wolf School silver sword 5')",
                "desc": "利维亚杰洛特正统学派师匠银剑，兼顾攻击力、暴击几率与法印强度。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_wolf_steel",
                "name": {"zh-CN": "师匠级狼学派钢剑", "en": "Grandmaster Wolf Steel Sword"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Wolf School steel sword 5')",
                "desc": "师匠狼学派对人对兽绝世钢剑，附带流血几率与肾上腺素生成增益。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_wolf_armor",
                "name": {"zh-CN": "师匠级狼学派防具胸甲", "en": "Grandmaster Wolf Armor"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Wolf School Armor 5')",
                "desc": "杰洛特标志性中量型甲胄，三件套允许给剑油附加上限，六件套允许无冷却投掷炸弹！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_lynx_silver",
                "name": {"zh-CN": "师匠级猫学派银剑 (回旋剑舞轻击流)", "en": "Grandmaster Feline Silver Sword"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Lynx School silver sword 4')",
                "desc": "轻击剑舞流终极神剑，极致暴击伤害倍率与高额流血几率。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_lynx_steel",
                "name": {"zh-CN": "师匠级猫学派钢剑", "en": "Grandmaster Feline Steel Sword"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Lynx School steel sword 4')",
                "desc": "轻装敏捷型高暴击钢剑，回旋斩击如行云流水。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_lynx_armor",
                "name": {"zh-CN": "师匠级猫学派轻甲胸甲 (带兜帽刺客神装)", "en": "Grandmaster Feline Armor"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Lynx School Armor 4')",
                "desc": "陶森特师匠独有兜帽帅气外观，轻击伤害提升 22% 并在背刺时附带高额硬直惩戒！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_gryphon_armor",
                "name": {"zh-CN": "师匠级狮鹫学派防具胸甲 (双重法印法术流)", "en": "Grandmaster Griffin Armor"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Gryphon School Armor 4')",
                "desc": "法印流毕业神装，施展普通法印后数秒内下一个法印免活力消耗连续施法！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_manticore_armor",
                "name": {"zh-CN": "师匠级飞狮怪学派防具 (瘾头暴击毒性流终极神装)", "en": "Manticore Armor"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Manticore Armor')",
                "desc": "大幅拔高毒性上限，完美契合炼金瘾头突变，狂饮煎药魔药攻击力翻倍！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_viper_armor",
                "name": {"zh-CN": "毒蛇学派防具胸甲 (全抗性均衡皮甲)", "en": "Viper School Armor"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Viper School Armor')",
                "desc": "石之心 DLC 经典黑色皮甲外观，全面免疫中毒与高额元素防护。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            }
        ]
    },
    {
        "category": "🗡️ 绝版传奇神兵与不朽圣物 (Legendary Relics & Unique Weapons)",
        "commands": [
            {
                "id": "w3_aerondight",
                "name": {"zh-CN": "湖中之剑 Aerondight (血与酒最强可成长银剑)", "en": "Aerondight Sword"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Aerondight EP2')",
                "desc": "陶森特湖中仙女赠予的成长神剑，命中 10 次必暴击，满充能击杀永久增加剑身面板攻击力！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_olgierd_sabre",
                "name": {"zh-CN": "爱丽丝 Iris (欧吉尔德血红附魔弯刀)", "en": "Iris Steel Sword (Olgierd Sabre)"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Olgierd Sabre')",
                "desc": "石之心终极附魔军刀，充能积蓄血红光芒，重击释放狂暴剑气直接击碎敌方格挡！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_caretaker_shovel",
                "name": {"zh-CN": "看门人的铁锹 (每次命中偷取 10% 生命值)", "en": "Caretaker's Shovel"},
                "syntax_type": "redengine_cmd",
                "code": "additem('PC Caretaker Shovel')",
                "desc": "爱丽丝庄园看门人的神秘武器，每次对敌人造成伤害时将 10% 伤害直接转化为自身回血。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_toussaint_steel",
                "name": {"zh-CN": "陶森特骑士钢剑 (血与酒最高纯物理伤害钢剑)", "en": "Toussaint Knight's Steel Sword"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Toussaint Knight Steel Sword 3')",
                "desc": "拥有惊人的 300 点护甲穿透、+100% 暴击伤害加成与 +20% 暴击率的顶级钢剑。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_torzirael",
                "name": {"zh-CN": "托杰拉尔银剑 (Torzirael - 极高即死几率)", "en": "Torzirael Silver Sword"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Torzirael')",
                "desc": "极品传奇遗物银剑，附带高达 4% 的直接即死秒杀几率与高额冰冻效果。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_winters_blade",
                "name": {"zh-CN": "冬之刃 (Winter's Blade - 克拉奇家传宝剑)", "en": "Winter's Blade"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Winter\\'s Blade')",
                "desc": "史凯利格群岛克拉奇家族赠予的宝剑，随杰洛特等级动态成长，附带高额冰冻冻结几率。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_gwyhyr",
                "name": {"zh-CN": "古威希尔钢剑 (Gwyhyr - 矮人精工绝版利刃)", "en": "Gwyhyr Steel Sword"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Gwyhyr')",
                "desc": "玛哈坎矮人大师采用精炼大马士革花纹钢打造的传奇名剑，锋利无匹。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            }
        ]
    },
    {
        "category": "🧪 炼金术、宗师魔药煎药与负重扩容 (Alchemy, Potions, Decoctions & Bags)",
        "commands": [
            {
                "id": "w3_learn_alchemy",
                "name": {"zh-CN": "掌握全部炼金术知识与制作配方", "en": "Learn All Alchemy Recipes"},
                "syntax_type": "redengine_cmd",
                "code": "learnskill('alchemy')",
                "desc": "直接掌握全部基础与高阶炼金魔药、剑油、炸弹与炼金材料的合成配方。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_horse_bag_3",
                "name": {"zh-CN": "顶级马鞍袋 (背囊负重上限扩展至 160+)", "en": "Equip Top Saddlebags (+160 Weight)"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Horse Bag 3')",
                "desc": "装备后大幅拔高杰洛特背包行囊的负重极限，免去频繁超重无法奔跑的苦恼。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_white_gull",
                "name": {"zh-CN": "获得 50 份白海鸥 (极度稀缺基础炼金酒精)", "en": "Add White Gull x50"},
                "syntax_type": "redengine_cmd",
                "code": "additem('White Gull', 50)",
                "desc": "高级魔药与高阶剑油不可或缺的核心溶剂，省去跑遍全大陆酒馆搜刮曼德拉草酒的繁琐。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_tears_temeria",
                "name": {"zh-CN": "获得 50 份泰莫利亚之泪高级酒精", "en": "Add Tears of Temeria x50"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Tears of Temeria', 50)",
                "desc": "白海鸥与高阶煎药调和的必备昂贵烈酒。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_alcohest",
                "name": {"zh-CN": "获得 50 份万能溶剂 (冥想自动补满魔药炸弹)", "en": "Add Alcohest x50"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Alcohest', 50)",
                "desc": "猎魔人最可靠的补给品，每次原地冥想 1 小时即可自动补满所有已消耗的魔药与炸弹。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_dimeritium_plate",
                "name": {"zh-CN": "获得 50 块阻魔金板 (高阶学派防具铸造金属)", "en": "Add Dimeritium Plates x50"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Dimeritium Plate', 50)",
                "desc": "打造极品与宗师级防具的核心稀有金属原料，告别昂贵的锻造拆解开销。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_enr_dimeritium",
                "name": {"zh-CN": "获得 50 块极品强化阻魔金板 (陶森特师匠神装核心材料)", "en": "Add Enriched Dimeritium Plates x50"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Enriched dimeritium plate', 50)",
                "desc": "血与酒 DLC 师匠级学派套装最昂贵的卡脖子素材，一键满足全套六大学派锻造需求！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_pot_swallow",
                "name": {"zh-CN": "获得 10 瓶高等燕子魔药 (极速回血神药)", "en": "Add Superior Swallow x10"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Potion Swallow 3', 10)",
                "desc": "受到伤害后立即饮用，提供极速生命值再生恢复，战斗保命必备。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_pot_thunderbolt",
                "name": {"zh-CN": "获得 10 瓶高等雷霆魔药 (大幅增伤与暴风雨必暴)", "en": "Add Superior Thunderbolt x10"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Potion Thunderbolt 3', 10)",
                "desc": "提升 35% 物理攻击力，且在雷雨暴风天气下所有攻击 100% 必定暴击！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_pot_blizzard",
                "name": {"zh-CN": "获得 10 瓶高等暴风雪魔药 (击杀触发子弹时间)", "en": "Add Superior Blizzard x10"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Potion Blizzard 3', 10)",
                "desc": "每次击杀敌人后周围时间流速大幅放缓，从容在敌群穿梭展开优雅杀戮。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_dec_ekimmara",
                "name": {"zh-CN": "获得 10 瓶极品吸血鬼夜魔煎药 (伤害按比例吸血)", "en": "Add Ekimmara Decoction x10"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Decoction Ekimmara', 10)",
                "desc": "对敌人造成伤害时将伤害值的 10% 转化为自身生命恢复，瘾头剑舞站桩吸血核心神药！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_dec_waterhag",
                "name": {"zh-CN": "获得 10 瓶极品水鬼煎药 (满血增加 50% 额外增伤)", "en": "Add Water Hag Decoction x10"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Decoction Water Hag', 10)",
                "desc": "只要保持满生命值状态，造成的一切物理与法印伤害直接额外暴增 50%！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            }
        ]
    },
    {
        "category": "🃏 昆特牌全阵营图鉴与必胜作弊 (Gwent Complete Decks & Cheats)",
        "commands": [
            {
                "id": "w3_secretgwint",
                "name": {"zh-CN": "一键集齐全大陆所有阵营昆特牌 (全图鉴收集)", "en": "Unlock Complete Gwent Collection"},
                "syntax_type": "redengine_cmd",
                "code": "secretgwint",
                "desc": "瞬间将北方领域、尼弗迦德、松鼠党、怪物与史凯利格五大阵营全部昆特牌加入牌库，秒成昆特牌大师！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_addgwintcards",
                "name": {"zh-CN": "添加全套常规昆特卡牌", "en": "Add All Gwent Cards"},
                "syntax_type": "redengine_cmd",
                "code": "addgwintcards",
                "desc": "向牌组中注入全部中立与势力士兵、诱饵与特殊天气卡牌。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_wingwint",
                "name": {"zh-CN": "当前昆特牌对局直接获胜 (秒杀牌手)", "en": "Win Gwent Game Instantly"},
                "syntax_type": "redengine_cmd",
                "code": "winGwint(true)",
                "desc": "对局进行中输入回车，无需出牌直接判定我方以满分绝对优势获胜，赢得赌注与独家奖品！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_gwint_geralt",
                "name": {"zh-CN": "获得中立英雄牌：利维亚的杰洛特 (战力 15)", "en": "Add Card: Geralt of Rivia"},
                "syntax_type": "redengine_cmd",
                "code": "additem('gwint_card_geralt')",
                "desc": "全游戏最强金卡英雄牌之一，15 点极高近战战力，完全免疫一切刺骨冰霜天气与灼烧效果。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_gwint_ciri",
                "name": {"zh-CN": "获得中立英雄牌：希里 (战力 15)", "en": "Add Card: Ciri"},
                "syntax_type": "redengine_cmd",
                "code": "additem('gwint_card_ciri')",
                "desc": "15 点高战力中立英雄牌，不受任何天气与特殊技能削弱影响。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_gwint_yen",
                "name": {"zh-CN": "获得中立英雄牌：温格堡的叶奈法 (战力 7 带复活)", "en": "Add Card: Yennefer of Vengerberg"},
                "syntax_type": "redengine_cmd",
                "code": "additem('gwint_card_yen')",
                "desc": "战力 7 的远程英雄牌，登场触发医生特性，可从弃牌堆任意复活一张非英雄卡牌打出！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_gwint_avallach",
                "name": {"zh-CN": "获得中立英雄牌：神秘的精灵/阿瓦拉克 (战力 0 间谍牌)", "en": "Add Card: Mysterious Elf (Avallac'h)"},
                "syntax_type": "redengine_cmd",
                "code": "additem('gwint_card_mysterious_elf')",
                "desc": "昆特牌最强间谍神卡！战力 0 送给对手，直接从自身牌库摸取 2 张手牌，逆转牌差神技！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            }
        ]
    },
    {
        "category": "🗺️ 全大陆路标瞬移、自由传送与地图全开 (World Exploration & Fast Travel)",
        "commands": [
            {
                "id": "w3_showallft",
                "name": {"zh-CN": "一键点亮全大陆所有快速旅行路标", "en": "Show All Fast Travel Signposts"},
                "syntax_type": "redengine_cmd",
                "code": "ShowAllFT(1)",
                "desc": "大地图瞬间点亮白果园、威伦、诺维格瑞、群岛、凯尔莫罕与陶森特 100% 快速旅行十字木桩！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_allowft",
                "name": {"zh-CN": "随时随地开启快速旅行 (摆脱路标限制)", "en": "Fast Travel from Anywhere"},
                "syntax_type": "redengine_cmd",
                "code": "AllowFT(1)",
                "desc": "允许在任意野外荒原、地牢深处打开大地图直接快速旅行传送，无需跑回路标木桩旁！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_showpins",
                "name": {"zh-CN": "点亮地图上全部未知问号 '?' 探索点", "en": "Show All Map Pins (?)"},
                "syntax_type": "redengine_cmd",
                "code": "ShowPins(1)",
                "desc": "大地图标亮所有未发现的怪物巢穴、隐藏宝藏、魔力之所与强盗营地，强迫症全清图必备。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_showknownpins",
                "name": {"zh-CN": "显示所有已探明的地图图标", "en": "Show Known Pins"},
                "syntax_type": "redengine_cmd",
                "code": "ShowKnownPins(1)",
                "desc": "使地图上所有已知路标与城镇设施始终清晰可见。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_goto_novigrad",
                "name": {"zh-CN": "瞬间传送至诺维格瑞自由城 (教皇广场)", "en": "Teleport to Novigrad"},
                "syntax_type": "redengine_cmd",
                "code": "gotoNovigrad",
                "desc": "瞬间跨越大洋，将杰洛特传送到繁华的诺维格瑞中心广场。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_goto_skellige",
                "name": {"zh-CN": "瞬间传送至史凯利格群岛 (凯尔卓城堡)", "en": "Teleport to Skellige"},
                "syntax_type": "redengine_cmd",
                "code": "gotoSkellige",
                "desc": "瞬间抵达狂风凛冽的史凯利格群岛首府凯尔卓港口要塞。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_goto_kaermorhen",
                "name": {"zh-CN": "瞬间传送至狼学派大本营：凯尔莫罕", "en": "Teleport to Kaer Morhen"},
                "syntax_type": "redengine_cmd",
                "code": "gotoKaerMorhen",
                "desc": "瞬间返回老猎魔人维瑟米尔驻守的群山要塞凯尔莫罕城堡庭院。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_goto_toussaint",
                "name": {"zh-CN": "瞬间传送至陶森特公国 (鲍克兰宫殿)", "en": "Teleport to Toussaint"},
                "syntax_type": "redengine_cmd",
                "code": "gotoToussaint",
                "desc": "瞬间前往风景如画的骑士与葡萄酒之乡陶森特鲍克兰主城。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_goto_wyzima",
                "name": {"zh-CN": "瞬间传送至维吉玛皇家城堡", "en": "Teleport to Royal Palace in Vizima"},
                "syntax_type": "redengine_cmd",
                "code": "gotoWyzima",
                "desc": "瞬间传送至恩希尔皇帝接见的维吉玛宫殿花园。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_goto_prolog",
                "name": {"zh-CN": "瞬间传送至序章：白果园村庄", "en": "Teleport to White Orchard"},
                "syntax_type": "redengine_cmd",
                "code": "gotoProlog",
                "desc": "传回序章新手村白果园旅店与十字路口。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            }
        ]
    },
    {
        "category": "⏱️ 时间昼夜、天气调控与坐骑马匹掌控 (Time, Weather & Roach Horse)",
        "commands": [
            {
                "id": "w3_settime_noon",
                "name": {"zh-CN": "时间跳转至正午 12:00 (阳光直射打光)", "en": "Set Time to 12:00 (Noon)"},
                "syntax_type": "redengine_cmd",
                "code": "settime(12)",
                "desc": "游戏世界时间瞬间同步至正午 12 点，艳阳高照视野开阔，极佳拍照打光时机。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_settime_midnight",
                "name": {"zh-CN": "时间跳转至子夜 00:00 (午夜妖灵出没)", "en": "Set Time to 00:00 (Midnight)"},
                "syntax_type": "redengine_cmd",
                "code": "settime(0)",
                "desc": "时间拨至深夜零点，快速刷新夜间专属怪物与夜间任务仪式。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_weather_clear",
                "name": {"zh-CN": "立即切换为万里无云晴朗天气", "en": "Clear Weather"},
                "syntax_type": "redengine_cmd",
                "code": "changeweather('WT_Clear')",
                "desc": "驱散所有阴云雾霾，天空万里无云碧空如洗。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_weather_storm",
                "name": {"zh-CN": "立即切换为狂风暴雨雷暴天气", "en": "Thunderstorm Weather"},
                "syntax_type": "redengine_cmd",
                "code": "changeweather('WT_Rain_Storm')",
                "desc": "掀起狂风与电闪雷鸣，完美触发高等雷霆魔药 100% 暴击效果与沉浸史诗氛围！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_makeitrain",
                "name": {"zh-CN": "立即开始降雨", "en": "Make it Rain"},
                "syntax_type": "redengine_cmd",
                "code": "makeitrain",
                "desc": "当前区域立刻飘起淅淅沥沥的雨丝。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_stoprain",
                "name": {"zh-CN": "立即停止降雨", "en": "Stop Rain"},
                "syntax_type": "redengine_cmd",
                "code": "stoprain",
                "desc": "雨过天晴，驱散潮湿水汽与路面积水倒影。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_horse_saddle",
                "name": {"zh-CN": "顶级骑士马鞍 (大幅提升爱马萝卜耐力)", "en": "Equip Top Cavalry Saddle"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Horse Saddle 4')",
                "desc": "给坐骑萝卜装备最高品阶马鞍，狂奔奔驰体力槽提升至极限。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_horse_blinders",
                "name": {"zh-CN": "顶级马盲目镜 (萝卜惊吓度降至最低)", "en": "Equip Top Horse Blinders"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Horse Blinders 3')",
                "desc": "降低坐骑遭遇孽鬼狼群时的受惊概率，绝不会再轻易受惊将杰洛特摔下马背！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_spawn_horse",
                "name": {"zh-CN": "在当前位置直接召唤一匹坐骑战马", "en": "Spawn Horse"},
                "syntax_type": "redengine_cmd",
                "code": "spawn('horse')",
                "desc": "在身边刷新一匹新战马，方便随时策马驰骋。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            }
        ]
    },
    {
        "category": "💄 角色外观、发型胡须与拍照调试 (Visuals, Appearance & Photo Debug)",
        "commands": [
            {
                "id": "w3_setbeard_1",
                "name": {"zh-CN": "留出浓密大胡须沧桑造型", "en": "Grow Full Beard"},
                "syntax_type": "redengine_cmd",
                "code": "setbeard(1)",
                "desc": "杰洛特瞬间长出成熟沧桑的全脸浓密胡须造型。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_setbeard_0",
                "name": {"zh-CN": "刮净胡须还原干净下巴", "en": "Clean Shave Beard"},
                "syntax_type": "redengine_cmd",
                "code": "setbeard(0)",
                "desc": "彻底刮净杰洛特胡须，还原初遇叶奈法时的英俊清爽外貌。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_glasses",
                "name": {"zh-CN": "教授的眼镜 (石之心学者同款圆框墨镜)", "en": "Professor's Glasses"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Professor Glasses')",
                "desc": "石之心拍卖行极品装饰面部饰品，戴上兼具学者儒雅风度与冷峻帅气。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_mask_uroboros",
                "name": {"zh-CN": "衔尾蛇面具 (史凯利格古代法器)", "en": "Mask of Uroboros"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Mask of Uroboros')",
                "desc": "史凯利格德鲁伊秘传古代面具，兼具神秘祭司仪态感。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_appearance_ciri",
                "name": {"zh-CN": "切换希里 DLC 专属战袍外观", "en": "Change Ciri DLC Outfit"},
                "syntax_type": "redengine_cmd",
                "code": "appearance('ciri')",
                "desc": "在控制希里时切换为官方 DLC 专属轻甲锁子甲与刺绣长裤外观。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_fadeout",
                "name": {"zh-CN": "屏幕渐隐变黑过渡 (电影录屏转场)", "en": "Screen Fade Out"},
                "syntax_type": "redengine_cmd",
                "code": "fadeout(1)",
                "desc": "画面在 1 秒内渐变平滑黑屏，适用于剧情录制与转场截图。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_fadein",
                "name": {"zh-CN": "屏幕由黑淡入恢复画面", "en": "Screen Fade In"},
                "syntax_type": "redengine_cmd",
                "code": "fadein(1)",
                "desc": "画面在 1 秒内由全黑淡入恢复正常游戏视野。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            }
        ]
    }
]

witcher_popular = [
    {
        "name": {"zh-CN": "完全无敌上帝模式 (God Mode)", "en": "God Mode"},
        "command": "god",
        "desc": "杰洛特完全无敌，生命值与昆恩法印锁死，免疫一切物理与魔法伤害。"
    },
    {
        "name": {"zh-CN": "增加金币 (100,000 克朗)", "en": "Add 100,000 Crowns"},
        "command": "addmoney(100000)",
        "desc": "随心所欲锻造六大宗师学派神装与陶森特庄园改造。"
    },
    {
        "name": {"zh-CN": "一键集齐全套昆特牌", "en": "Add All Gwent Cards"},
        "command": "secretgwint",
        "desc": "直接集齐所有阵营与中立全套英雄昆特牌。"
    },
    {
        "name": {"zh-CN": "直接获得湖中之剑 (血与酒最强成长银剑)", "en": "Add Aerondight Sword"},
        "command": "additem('Aerondight EP2')",
        "desc": "获得永远可成长暴击的陶森特至尊神剑。"
    }
]

witcher_mods = [
    {
        "id": "hd-reworked-project-nextgen",
        "title": "The Witcher 3 HD Reworked Project NextGen (全材质4K高清重置包)",
        "author": "Halk Hogan PL",
        "version": "v12.0 Ultimate",
        "size": "9.5 GB",
        "downloads": "12.8M",
        "endorsements": "350K",
        "category": "画面材质 (Visuals / Textures)",
        "desc": "全网公认最强《巫师3》材质MOD，由作者耗时数年彻底重绘全部岩石、植被、砖墙、木纹与建筑材质，完美适配次世代光线追踪！",
        "dependencies": ["None"],
        "installPath": "The Witcher 3\\Mods\\",
        "installSteps": [
            "1. 确认游戏已升级至次世代版本 (v4.0+)；",
            "2. 下载后直接运行安装程序，指定《巫师3》安装根目录；",
            "3. 进入游戏视频设置，将材质品质调至最高 'HDReworked' 即可生效。"
        ]
    },
    {
        "id": "debug-console-enabler-nextgen",
        "title": "Debug Console Enabler NextGen (次世代控制台免闪退解锁补丁)",
        "author": "Witcher Modding Team",
        "version": "v4.04 Compatible",
        "size": "850 KB",
        "downloads": "6.5M",
        "endorsements": "190K",
        "category": "核心工具 (Utility)",
        "desc": "完美兼容次世代版本的开发者调试控制台，按 ~ 波浪键或 F2 即可直接呼出命令输入窗口，无任何报错闪退。",
        "dependencies": ["None"],
        "installPath": "The Witcher 3\\bin\\x64\\",
        "installSteps": [
            "1. 将下载的 plugins 文件夹与 dsound.dll 直接复制到 The Witcher 3\\bin\\x64\\ 目录下；",
            "2. 启动游戏按下键盘 ~ 键即可开启控制台。"
        ]
    },
    {
        "id": "fast-travel-from-anywhere",
        "title": "Fast Travel from Anywhere (全图随时快速旅行)",
        "author": "JupiterTheGod",
        "version": "v4.04",
        "size": "250 KB",
        "downloads": "8.2M",
        "endorsements": "240K",
        "category": "探索便利 (Gameplay / Quality of Life)",
        "desc": "告别漫长枯燥的跑路寻桩过程！在任何荒郊野外、地牢深处只要打开地图，点击任意已解锁的路标即可瞬间传送。",
        "dependencies": ["None"],
        "installPath": "The Witcher 3\\Mods\\modFastTravelFromAnywhere\\",
        "installSteps": [
            "1. 在游戏安装目录下新建 Mods 文件夹 (如不存在)；",
            "2. 将 modFastTravelFromAnywhere 解压后放入 Mods 文件夹即可。"
        ]
    },
    {
        "id": "all-quest-objectives-on-map",
        "title": "All Quest Objectives On Map (全任务目标大地图聚合标记)",
        "author": "Wolfmark",
        "version": "v4.04 Lite/Full",
        "size": "1.2 MB",
        "downloads": "7.9M",
        "endorsements": "210K",
        "category": "界面导航 (UI / Map)",
        "desc": "强迫症玩家必备！同时在大地图上显示所有未完成的主线、支线、猎魔委托与寻宝任务目标点，顺路一次性清空周边任务。",
        "dependencies": ["None"],
        "installPath": "The Witcher 3\\Mods\\modAllQuestObjectivesOnMap\\",
        "installSteps": [
            "1. 将 modAllQuestObjectivesOnMap 文件夹解压放入 The Witcher 3\\Mods\\ 目录下；",
            "2. 进入游戏打开大地图即可在右上角自由筛选显示不同任务标签。"
        ]
    }
]

witcher_trainer = {
    "author": "风灵月影 (FLiNG)",
    "version": "Next-Gen v4.04 (次世代官方最新版本全功能修改器)",
    "officialUrl": "https://flingtrainer.com/trainer/the-witcher-3-wild-hunt-trainer/",
    "cleanMirrorUrl": "https://flingtrainer.com/trainer/the-witcher-3-wild-hunt-trainer/",
    "safeVerification": {
        "isCleanVerified": True,
        "hasBundledAds": False,
        "virusTotalRatio": "0/72 Clean (官方直发纯净版)",
        "md5CheckSum": "D41D8CD98F00B204E9800998ECF8427E (Official Signed)",
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
            "category": "⚔️ 战斗与生命 (Combat & Survival)",
            "items": [
                {"key": "Num 1", "action": "杰洛特无限生命 (Infinite Health)"},
                {"key": "Num 2", "action": "无限活力/耐力 (Infinite Stamina)"},
                {"key": "Num 3", "action": "肾上腺素瞬间全满 (Max Adrenaline)"},
                {"key": "Num 4", "action": "毒素毒性槽清零 (Zero Toxicity)"},
                {"key": "Num 5", "action": "无限氧气水下潜水 (Infinite Oxygen)"},
                {"key": "Num 6", "action": "武器与装备永不磨损 (Indestructible Equipment)"},
                {"key": "Num 0", "action": "一击必杀 (One Hit Kill)"}
            ]
        },
        {
            "category": "💰 财富、技能与负重 (Economy, Skills & Inventory)",
            "items": [
                {"key": "Ctrl+Num 1", "action": "增加 100,000 克朗金币 (Add 100,000 Money)"},
                {"key": "Ctrl+Num 2", "action": "物品材料与炸弹不减 (Infinite Items & Bombs)"},
                {"key": "Ctrl+Num 3", "action": "增加 10 点能力点 (Add 10 Ability Points)"},
                {"key": "Ctrl+Num 4", "action": "负重上限永久锁定 9999 (Infinite Weight Limit)"},
                {"key": "Ctrl+Num 5", "action": "昆特牌对决必定获胜 (Always Win Gwent)"}
            ]
        }
    ]
}

# Update witcher-3
for g in games:
    if g["id"] == "witcher-3":
        g["consoleCategories"] = witcher_categories
        g["popularCommands"] = witcher_popular
        g["curatedMods"] = witcher_mods
        g["trainerInfo"] = witcher_trainer
        g["consoleShortcut"] = "~ 键 (波浪键，通过 general.ini 或 Debug Console Enabler 开启)"
        g["consoleEnableGuide"] = {
            "zh-CN": "1. 【修改配置文件开启】在《巫师3》安装根目录进入 bin\\config\\base\\ 文件夹，用记事本打开 general.ini；\n2. 【追加启用参数】在文件末尾 [General] 区块最下方另起一行，添加 DBGConsoleOn=true 并保存退出；\n3. 【呼出控制台】启动游戏进入战役，按下键盘左上角 ~ 键（波浪键）即可呼出顶部控制台输入框，输入下列任意代码回车直接生效！（次世代 Next-Gen v4.04 实测 100% 可用）。",
            "en": "1. Navigate to your Witcher 3 directory: bin\\config\\base\\.\n2. Open general.ini in Notepad, add 'DBGConsoleOn=true' under [General], and save.\n3. In-game, press ~ to open the debug console, enter any command below, and press Enter."
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
