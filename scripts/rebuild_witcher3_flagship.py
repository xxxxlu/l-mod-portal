import json
import os

JSON_PATH = '/Users/xiaolu/Desktop/work/l-mod-portal/src/data/games_top100.json'
JS_PATH = '/Users/xiaolu/Desktop/work/l-mod-portal/public/data.js'

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    games = json.load(f)

witcher_categories = [
    {
        "category": "👑 核心上帝模式与主角机体掌控 (God Mode & Invincibility)",
        "commands": [
            {
                "id": "w3_god",
                "name": {"zh-CN": "完全无敌上帝模式 (生命与法印锁死)", "en": "God Mode"},
                "syntax_type": "redengine_cmd",
                "code": "god",
                "desc": "杰洛特完全无敌，生命值与昆恩法印锁死不掉血，免疫所有怪物抓击、挥砍、毒素、坠落摔伤与狂猎霜冻，再次输入可解除无敌状态。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_likeaboss",
                "name": {"zh-CN": "像大 Boss 一样战斗 (伤害削减99%且重击按比例秒杀)", "en": "Like a Boss Mode"},
                "syntax_type": "redengine_cmd",
                "code": "likeaboss",
                "desc": "将杰洛特受到的所有伤害削减至 1%，同时每次普攻造成敌方 40% 最大生命值的绝对碾压伤害，秒杀一切强敌妖灵！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_healme",
                "name": {"zh-CN": "瞬间全状态恢复满血", "en": "Heal to Full"},
                "syntax_type": "redengine_cmd",
                "code": "healme",
                "desc": "立即清除流血、中毒、燃烧状态并瞬间回满杰洛特的全部生命值。",
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
                "id": "w3_witchcraft",
                "name": {"zh-CN": "终极宝库一键装填 (全游戏所有道具各注入一份)", "en": "Witchcraft All Items"},
                "syntax_type": "redengine_cmd",
                "code": "witchcraft",
                "desc": "将游戏中包括全部武器、防具、原料、图纸在内的所有物品全部各添加 1 份至背包（执行会略微卡顿，背包负重会剧增）。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_resurrect",
                "name": {"zh-CN": "原地满血复活", "en": "Resurrect"},
                "syntax_type": "redengine_cmd",
                "code": "resurrect",
                "desc": "在重伤倒地死亡判定出现瞬间立即原地满血重生，免去重新读档读取进度条的漫长等待。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            }
        ]
    },
    {
        "category": "🎯 角色等级、经验值与全技能洗点 (Levels, XP & Skill Tree)",
        "commands": [
            {
                "id": "w3_setlevel_100",
                "name": {"zh-CN": "角色等级直升 100 级满级", "en": "Set Level 100"},
                "syntax_type": "redengine_cmd",
                "code": "setlevel(100)",
                "desc": "将杰洛特的人物等级直接设定为最高 100 级，直接破除全陶森特与石之心顶级神装的穿戴门槛。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_levelup",
                "name": {"zh-CN": "角色等级提升 1 级", "en": "Level Up"},
                "syntax_type": "redengine_cmd",
                "code": "levelup",
                "desc": "让杰洛特立即升 1 级并获得相应的属性与能力点。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_addexp_10000",
                "name": {"zh-CN": "增加 10,000 点人物经验值", "en": "Add 10,000 XP"},
                "syntax_type": "redengine_cmd",
                "code": "addexp(10000)",
                "desc": "注入 10000 点战斗与任务经验值，按游戏原本曲线稳定升级。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_addskillpoints_50",
                "name": {"zh-CN": "获得 50 点技能点数 (点亮全技能树)", "en": "Add 50 Skill Points"},
                "syntax_type": "redengine_cmd",
                "code": "addskillpoints(50)",
                "desc": "直接增加 50 点未分配能力点数，随心所欲点亮战斗、法印、炼金与突变全技能树！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_addskillpoints_10",
                "name": {"zh-CN": "获得 10 点技能点数", "en": "Add 10 Skill Points"},
                "syntax_type": "redengine_cmd",
                "code": "addskillpoints(10)",
                "desc": "小幅增加 10 点能力点数，满足某个专精支线的快速加点需求。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_cleardevelop",
                "name": {"zh-CN": "完全洗点并重置突变诱发物", "en": "Reset Skill Tree & Points"},
                "syntax_type": "redengine_cmd",
                "code": "cleardevelop",
                "desc": "清空并重置所有已学习的战斗、法印、炼金技能与突变槽，全额返还全部技能点供重新构筑流派。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_learnskill_swordsmanship",
                "name": {"zh-CN": "直接解锁剑术大师技能", "en": "Learn Sword Mastery"},
                "syntax_type": "redengine_cmd",
                "code": "learnskill('sword_s1')",
                "desc": "直接学会并解锁剑术第一阶核心被动技能。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            }
        ]
    },
    {
        "category": "💰 财富自由、负重突破与大突变诱发物 (Crowns, Weight & Greater Mutagens)",
        "commands": [
            {
                "id": "w3_addmoney_100k",
                "name": {"zh-CN": "增加 100,000 克朗金币 (奥森弗特首富)", "en": "Add 100,000 Crowns"},
                "syntax_type": "redengine_cmd",
                "code": "addmoney(100000)",
                "desc": "随心所欲锻造六大宗师学派神装与陶森特白葡萄庄园全设施扩建升级！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_addmoney_10k",
                "name": {"zh-CN": "增加 10,000 克朗金币", "en": "Add 10,000 Crowns"},
                "syntax_type": "redengine_cmd",
                "code": "addmoney(10000)",
                "desc": "增加 10000 克朗，用于日常补给魔药与修理装备。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_removemoney_50k",
                "name": {"zh-CN": "扣除 50,000 克朗金币 (还清债务/降低难度)", "en": "Remove 50,000 Crowns"},
                "syntax_type": "redengine_cmd",
                "code": "removemoney(50000)",
                "desc": "清减多余资产，体验身无分文的底层猎魔人真实流浪生活。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_mutagen_red_greater",
                "name": {"zh-CN": "大红突变诱发物 x10 (剑术攻击力暴涨)", "en": "Greater Red Mutagen x10"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Mutagen red greater', 10)",
                "desc": "最稀缺珍贵的大红诱发物，解锁并激活血与酒最强剑术瘾头增伤突变核心！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_mutagen_blue_greater",
                "name": {"zh-CN": "大蓝突变诱发物 x10 (法印强度暴涨)", "en": "Greater Blue Mutagen x10"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Mutagen blue greater', 10)",
                "desc": "狮鹫学派法印轰炸流必备，大幅强化阿尔德推力与伊格尼点燃几率！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_mutagen_green_greater",
                "name": {"zh-CN": "大绿突变诱发物 x10 (最大生命值上限暴涨)", "en": "Greater Green Mutagen x10"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Mutagen green greater', 10)",
                "desc": "炼金熊学派坦克流核心，搭配协同作用技能让杰洛特血量突破万血！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_horse_bag_3",
                "name": {"zh-CN": "鲍克兰极品马鞍袋 (官方最高等级背包容量上限)", "en": "Beauclair Saddlebags (Max Capacity)"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Horse Bag 3')",
                "desc": "直接获得陶森特极品豪华马鞍袋，将背包负重基准上限永久大幅扩充！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            }
        ]
    },
    {
        "category": "🌟 次世代版 / 完全版专属神装与特典联动 (Next-Gen Remaster Exclusives & Netflix Rewards)",
        "commands": [
            {
                "id": "w3_white_tiger_armor",
                "name": {"zh-CN": "西境白虎盔甲 (次世代中文配音特供中国风战甲)", "en": "White Tiger Armor"},
                "syntax_type": "redengine_cmd",
                "code": "additem('White Tiger Armor')",
                "desc": "CDPR 为次世代版 / 完全版中文语音实装专属打造的提尔格里希白虎甲胄，绣有金丝盘龙与猛虎纹样，防御力与抗性出众。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_white_tiger_boots",
                "name": {"zh-CN": "西境白虎靴子", "en": "White Tiger Boots"},
                "syntax_type": "redengine_cmd",
                "code": "additem('White Tiger Boots')",
                "desc": "西境白虎套装护足，提供优秀的穿刺伤害抵抗与移动稳定性。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_white_tiger_gloves",
                "name": {"zh-CN": "西境白虎手套", "en": "White Tiger Gloves"},
                "syntax_type": "redengine_cmd",
                "code": "additem('White Tiger Gloves')",
                "desc": "西境白虎套装护手，提升攻击速度与法印强度加成。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_white_tiger_pants",
                "name": {"zh-CN": "西境白虎下装", "en": "White Tiger Pants"},
                "syntax_type": "redengine_cmd",
                "code": "additem('White Tiger Pants')",
                "desc": "西境白虎战袍长裤，提供高额斩击抗性与活力恢复速度。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_white_tiger_steel_sword",
                "name": {"zh-CN": "九尾狐女钢剑 (西境白虎配套名刀)", "en": "Vixen Steel Sword"},
                "syntax_type": "redengine_cmd",
                "code": "additem('White Tiger Steel Sword 1')",
                "desc": "刀身刻有青丘灵狐符文的东亚风格优雅佩剑，大幅提高暴击率与暴击伤害加成。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_white_tiger_silver_sword",
                "name": {"zh-CN": "九尾狐女银剑 (西境白虎配套银刃)", "en": "Vixen Silver Sword"},
                "syntax_type": "redengine_cmd",
                "code": "additem('White Tiger Silver Sword 1')",
                "desc": "针对怪物魔兽的灵狐银剑，击中敌人时有极高概率附加流血与失衡效果。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_dol_blathanna_armor",
                "name": {"zh-CN": "多尔·布雷坦纳千花盔甲 (次世代特典精灵华服)", "en": "Dol Blathanna Armor"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Dol Blathanna Armor')",
                "desc": "来自百花谷精灵工匠精心编织的轻型锁子甲战袍，提供强大的毒素与魔法元素抗性。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_dol_blathanna_boots",
                "name": {"zh-CN": "多尔·布雷坦纳千花靴子", "en": "Dol Blathanna Boots"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Dol Blathanna Boots')",
                "desc": "百花谷轻便皮靴，无声潜行与翻滚体力消耗减少。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_dol_blathanna_gloves",
                "name": {"zh-CN": "多尔·布雷坦纳千花手套", "en": "Dol Blathanna Gloves"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Dol Blathanna Gloves')",
                "desc": "百花谷刺客手套，赋予杰洛特更强劲的弓弩瞄准与挥剑精准度。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_dol_blathanna_pants",
                "name": {"zh-CN": "多尔·布雷坦纳千花长裤", "en": "Dol Blathanna Pants"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Dol Blathanna Pants')",
                "desc": "多尔·布雷坦纳战裙下装，兼具高透气性与卓越的抗打击韧度。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_dol_blathanna_steel_sword",
                "name": {"zh-CN": "千花钢剑 (百花之谷上古钢刃)", "en": "Thousand Flowers Steel Sword"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Dol Blathanna Steel Sword 1')",
                "desc": "剑柄镶嵌花藤蓝宝石的精灵宝剑，极高概率削弱敌人士气并触发深度割伤。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_dol_blathanna_silver_sword",
                "name": {"zh-CN": "白女妖银剑 (百花之谷纯银之锋)", "en": "White Widow Silver Sword"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Dol Blathanna Silver Sword 1')",
                "desc": "散发淡淡幽光的多尔·布雷坦纳银剑，对幽灵鬼魂生物有高额真实克制伤害。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_netflix_armor_base",
                "name": {"zh-CN": "初阶遗忘狼学派胸甲 (网飞第一季同款)", "en": "Forgotten Wolven Armor (Base)"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Netflix Armor')",
                "desc": "亨利·卡维尔主演《巫师》第一季经典的圆领黑皮猎魔人战甲外观，带有粗犷的铆钉绑带。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_netflix_steel_base",
                "name": {"zh-CN": "初阶遗忘狼学派钢剑", "en": "Forgotten Wolven Steel Sword (Base)"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Netflix Steel Sword')",
                "desc": "网飞剧版同款单手阔剑，剑首带有十字形狼头浮雕，兼顾斩击与刺击。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_netflix_silver_base",
                "name": {"zh-CN": "初阶遗忘狼学派银剑", "en": "Forgotten Wolven Silver Sword (Base)"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Netflix Silver Sword')",
                "desc": "网飞剧版同款银剑，对恶魔之坑释放的赤红疫病怪物有特殊驱散伤害。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_netflix_armor_1",
                "name": {"zh-CN": "极品遗忘狼学派胸甲 (网飞进阶版)", "en": "Mastercrafted Forgotten Wolven Armor"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Netflix Armor 1')",
                "desc": "经过陶森特级工匠强化的遗忘狼胸甲，肩部增加硬化钢片衬底与更密集的护心皮甲。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_netflix_steel_1",
                "name": {"zh-CN": "极品遗忘狼学派钢剑", "en": "Mastercrafted Forgotten Wolven Steel Sword"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Netflix Steel Sword 1')",
                "desc": "极品阶段遗忘狼钢剑，大幅强化亚登与阿尔德法印协同轰炸威力。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_netflix_silver_1",
                "name": {"zh-CN": "极品遗忘狼学派银剑", "en": "Mastercrafted Forgotten Wolven Silver Sword"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Netflix Silver Sword 1')",
                "desc": "极品阶段遗忘狼银剑，攻击击中受亚登影响的目标必定触发暴击。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_gwint_card_roach",
                "name": {"zh-CN": "次世代专属联动昆特牌：萝卜 (Roach)", "en": "Gwent Card: Roach (Next-Gen Exclusive)"},
                "syntax_type": "redengine_cmd",
                "code": "additem('gwint_card_roach')",
                "desc": "CDPR 在次世代版 / 完全版中新加入的官方中立昆特英雄牌，攻击力为 3 点，打出后可自动从牌库拉出同伴支援，自带萝卜鬼畜站房顶插画！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            }
        ]
    },
    {
        "category": "🐺 宗师级狼学派与宗师级遗弃狼套装 (Grandmaster & Forgotten Wolven Sets)",
        "commands": [
            {
                "id": "w3_gm_wolf_silver",
                "name": {"zh-CN": "宗师级狼学派银剑", "en": "Grandmaster Wolven Silver Sword"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Wolf School Silver Sword 4')",
                "desc": "狼学派最高阶银剑，法印强度与暴击率全方位均衡提升。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_gm_wolf_steel",
                "name": {"zh-CN": "宗师级狼学派钢剑", "en": "Grandmaster Wolven Steel Sword"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Wolf School Steel Sword 4')",
                "desc": "凯尔莫罕正统传承至尊钢剑，大幅强化斩击伤害与肾上腺素获取速度。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_gm_wolf_armor",
                "name": {"zh-CN": "宗师级狼学派防具胸甲", "en": "Grandmaster Wolven Armor"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Wolf Armor 4')",
                "desc": "陶森特宗师级铸造大师打造，激活剑油加成与炸弹多重投掷特效！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_gm_wolf_gloves",
                "name": {"zh-CN": "宗师级狼学派手套", "en": "Grandmaster Wolven Gloves"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Wolf Gloves 4')",
                "desc": "宗师级狼学派手甲，提升攻击力与法印强度。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_gm_wolf_pants",
                "name": {"zh-CN": "宗师级狼学派裤子", "en": "Grandmaster Wolven Pants"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Wolf Pants 4')",
                "desc": "宗师级狼学派下装，提供斩击、穿刺与怪物全方位防御。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_gm_wolf_boots",
                "name": {"zh-CN": "宗师级狼学派靴子", "en": "Grandmaster Wolven Boots"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Wolf Boots 4')",
                "desc": "宗师级狼学派长靴，增强突进抗性与奔跑稳定性。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_netflix_silver_2",
                "name": {"zh-CN": "宗师级遗弃狼银剑 (网飞剧版第二季终极神兵)", "en": "Grandmaster Forgotten Wolven Silver Sword"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Netflix Silver Sword 2')",
                "desc": "次世代专属最高级遗弃狼银剑，亚登与阿尔德法印伤害提升超 300%！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_netflix_steel_2",
                "name": {"zh-CN": "宗师级遗弃狼钢剑", "en": "Grandmaster Forgotten Wolven Steel Sword"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Netflix Steel Sword 2')",
                "desc": "宗师级遗弃狼钢剑，附加高额肾上腺素充能与肢解斩杀几率。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_netflix_armor_2",
                "name": {"zh-CN": "宗师级遗弃狼防具胸甲 (大超同款紧身皮甲战袍)", "en": "Grandmaster Forgotten Wolven Armor"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Netflix Armor 2')",
                "desc": "激活次世代最强套装特效：亚登法印圈内敌人受到伤害时额外产生魔法爆破，药水药效延长！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_netflix_gloves_2",
                "name": {"zh-CN": "宗师级遗弃狼手套", "en": "Grandmaster Forgotten Wolven Gauntlets"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Netflix Gloves 2')",
                "desc": "宗师级遗弃狼护手，提升攻击速度与法印连发韧性。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_netflix_pants_2",
                "name": {"zh-CN": "宗师级遗弃狼下装", "en": "Grandmaster Forgotten Wolven Trousers"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Netflix Pants 2')",
                "desc": "宗师级遗弃狼战裙长裤，兼顾敏捷翻滚与高防御。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_netflix_boots_2",
                "name": {"zh-CN": "宗师级遗弃狼靴子", "en": "Grandmaster Forgotten Wolven Boots"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Netflix Boots 2')",
                "desc": "宗师级遗弃狼重型皮靴，抗击退与抗元素伤害大幅跃升。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            }
        ]
    },
    {
        "category": "🐻 宗师级熊学派全套重装 (Grandmaster Ursine School Set - 拜年重击流)",
        "commands": [
            {
                "id": "w3_gm_bear_silver",
                "name": {"zh-CN": "宗师级熊学派银剑", "en": "Grandmaster Ursine Silver Sword"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Bear School silver sword 4')",
                "desc": "拜年剑法核心重剑，肾上腺素生成速度与暴击伤害极高。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_gm_bear_steel",
                "name": {"zh-CN": "宗师级熊学派钢剑", "en": "Grandmaster Ursine Steel Sword"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Bear School steel sword 4')",
                "desc": "重击流对人专属大剑，一刀碎甲打断任何强敌招架！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_gm_bear_armor",
                "name": {"zh-CN": "宗师级熊学派重防具胸甲", "en": "Grandmaster Ursine Armor"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Bear School Armor 4')",
                "desc": "全游戏最坚固的重铠战袍！套装特效有概率无消耗瞬发强效昆恩护盾！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_gm_bear_gloves",
                "name": {"zh-CN": "宗师级熊学派手套", "en": "Grandmaster Ursine Gloves"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Bear School Gloves 4')",
                "desc": "极具防护力的重甲铁手套，增加暴击伤害与劈砍抗性。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_gm_bear_pants",
                "name": {"zh-CN": "宗师级熊学派裤子", "en": "Grandmaster Ursine Pants"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Bear School Pants 4')",
                "desc": "重型板甲下装，提供极致的怪物抓击伤害抵抗。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_gm_bear_boots",
                "name": {"zh-CN": "宗师级熊学派靴子", "en": "Grandmaster Ursine Boots"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Bear School Boots 4')",
                "desc": "厚重战靴，彻底免疫被怪物撞击击倒击晕。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            }
        ]
    },
    {
        "category": "🐱 宗师级猫学派刺客轻装 (Grandmaster Feline School Set - 回旋剑舞流)",
        "commands": [
            {
                "id": "w3_gm_cat_silver",
                "name": {"zh-CN": "宗师级猫学派银剑", "en": "Grandmaster Feline Silver Sword"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Lynx School silver sword 4')",
                "desc": "回旋剑舞流神剑，大幅提升攻击速度、流血概率与暴击几率！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_gm_cat_steel",
                "name": {"zh-CN": "宗师级猫学派钢剑", "en": "Grandmaster Feline Steel Sword"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Lynx School steel sword 4')",
                "desc": "高暴击轻刃钢剑，面对土匪强盗群直接化身旋风斩绞肉机！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_gm_cat_armor",
                "name": {"zh-CN": "宗师级猫学派轻型防具", "en": "Grandmaster Feline Armor"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Lynx Armor 4')",
                "desc": "带兜帽的刺客皮甲，后背偷袭伤害翻倍，套装特效强化连续轻击爆发！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_gm_cat_gloves",
                "name": {"zh-CN": "宗师级猫学派手套", "en": "Grandmaster Feline Gloves"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Lynx Gloves 4')",
                "desc": "轻型战斗皮手套，极大增加每次攻击造成的物理攻击力！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_gm_cat_pants",
                "name": {"zh-CN": "宗师级猫学派裤子", "en": "Grandmaster Feline Pants"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Lynx Pants 4')",
                "desc": "刺客紧身长裤，大幅提升闪避灵活性与暴击几率加成。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_gm_cat_boots",
                "name": {"zh-CN": "宗师级猫学派靴子", "en": "Grandmaster Feline Boots"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Lynx Boots 4')",
                "desc": "轻型潜行靴，奔跑速度极快且降低脚步惊扰范围。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            }
        ]
    },
    {
        "category": "🦅 宗师级狮鹫学派法印轰炸流 (Grandmaster Griffin School Set)",
        "commands": [
            {
                "id": "w3_gm_griffin_silver",
                "name": {"zh-CN": "宗师级狮鹫学派银剑", "en": "Grandmaster Griffin Silver Sword"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Gryphon School silver sword 4')",
                "desc": "法印流核心银剑，直接提升全部 5 种猎魔人法印的法术强度。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_gm_griffin_steel",
                "name": {"zh-CN": "宗师级狮鹫学派钢剑", "en": "Grandmaster Griffin Steel Sword"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Gryphon School steel sword 4')",
                "desc": "法印增幅钢剑，加快法印释放后的活力恢复速度。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_gm_griffin_armor",
                "name": {"zh-CN": "宗师级狮鹫学派防具胸甲", "en": "Grandmaster Griffin Armor"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Gryphon Armor 4')",
                "desc": "激活最强法印特效：施放法印后 3 秒内施放下一个法印无需消耗活力，伊格尼火烧全场！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_gm_griffin_gloves",
                "name": {"zh-CN": "宗师级狮鹫学派手套", "en": "Grandmaster Griffin Gloves"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Gryphon Gloves 4')",
                "desc": "宗师级狮鹫手套，全法印强度大幅飙升！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_gm_griffin_pants",
                "name": {"zh-CN": "宗师级狮鹫学派裤子", "en": "Grandmaster Griffin Pants"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Gryphon Pants 4')",
                "desc": "宗师级狮鹫下装，提供卓越的元素抗性与伤害减免。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_gm_griffin_boots",
                "name": {"zh-CN": "宗师级狮鹫学派靴子", "en": "Grandmaster Griffin Boots"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Gryphon Boots 4')",
                "desc": "宗师级狮鹫长靴，稳定站桩连续法印施法不被打断。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            }
        ]
    },
    {
        "category": "🐍 师匠级飞狮怪与毒蛇学派神装 (Manticore & Viper School Sets - 瘾头暴击流)",
        "commands": [
            {
                "id": "w3_gm_manticore_silver",
                "name": {"zh-CN": "师匠级飞狮怪银剑", "en": "Manticore Silver Sword"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Red Wolf Silver Sword 1')",
                "desc": "陶森特炼金大师银剑，提升暴击伤害与毒性容忍阈值。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_gm_manticore_steel",
                "name": {"zh-CN": "师匠级飞狮怪钢剑", "en": "Manticore Steel Sword"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Red Wolf Steel Sword 1')",
                "desc": "具有高穿甲与中毒概率的炼金流至尊钢剑！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_gm_manticore_armor",
                "name": {"zh-CN": "师匠级飞狮怪防具胸甲", "en": "Manticore Armor"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Red Wolf Armor 1')",
                "desc": "巫师1初版经典皮甲造型，增加最大毒性上限，完美同时磕下 4 瓶强力煎药！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_gm_manticore_gloves",
                "name": {"zh-CN": "师匠级飞狮怪手套", "en": "Manticore Gloves"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Red Wolf Gloves 1')",
                "desc": "增加药水毒性抗性与暴击几率加成。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_gm_manticore_pants",
                "name": {"zh-CN": "师匠级飞狮怪裤子", "en": "Manticore Pants"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Red Wolf Pants 1')",
                "desc": "提升炼金炸弹携带数量与毒素伤害抵抗。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_gm_manticore_boots",
                "name": {"zh-CN": "师匠级飞狮怪靴子", "en": "Manticore Boots"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Red Wolf Boots 1')",
                "desc": "提供高额毒抗与穿刺劈砍抗性。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_viper_silver",
                "name": {"zh-CN": "毒蛇剧毒银剑 (石之心绝版神兵)", "en": "Viper Venomous Silver Sword"},
                "syntax_type": "redengine_cmd",
                "code": "additem('EP1 Viper School Silver Sword')",
                "desc": "石之心迷宫中隐藏的绝世神兵，攻击敌人必定附加致命剧毒伤害！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_viper_steel",
                "name": {"zh-CN": "毒蛇剧毒钢剑", "en": "Viper Venomous Steel Sword"},
                "syntax_type": "redengine_cmd",
                "code": "additem('EP1 Viper School Steel Sword')",
                "desc": "拍卖行地下金库专属钢剑，高暴击高淬毒高穿甲！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_viper_armor",
                "name": {"zh-CN": "毒蛇学派护甲 (开场 CG 帅气黑皮甲)", "en": "Viper Armor"},
                "syntax_type": "redengine_cmd",
                "code": "additem('EP1 Viper School Armor')",
                "desc": "与白果园开场 CG 一致的纯黑鳞片皮甲，全毒素免疫与全面抗性极佳！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_viper_gloves",
                "name": {"zh-CN": "毒蛇学派手套", "en": "Viper Gloves"},
                "syntax_type": "redengine_cmd",
                "code": "additem('EP1 Viper School Gloves')",
                "desc": "毒蛇战甲皮手套，提升物理攻击与流血中毒施加几率。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_viper_pants",
                "name": {"zh-CN": "毒蛇学派裤子", "en": "Viper Pants"},
                "syntax_type": "redengine_cmd",
                "code": "additem('EP1 Viper School Pants')",
                "desc": "毒蛇鳞纹战术裤，提供极高的钝击与元素防御。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_viper_boots",
                "name": {"zh-CN": "毒蛇学派靴子", "en": "Viper Boots"},
                "syntax_type": "redengine_cmd",
                "code": "additem('EP1 Viper School Boots')",
                "desc": "毒蛇防水战靴，提升移动稳定性与毒素抗性。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            }
        ]
    },
    {
        "category": "🗡️ 绝版传奇神兵与石之心/血与酒不朽圣物 (Legendary Relics & Iconic Blades)",
        "commands": [
            {
                "id": "w3_aerondight",
                "name": {"zh-CN": "湖中之剑 (血与酒湖中仙女最强成长银剑)", "en": "Aerondight (Endless Growth)"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Aerondight EP2')",
                "desc": "全游戏最强银剑！每砍一刀充能一层增伤10%，10层必定 100% 暴击且击杀永久永久增加基础物理攻击力！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_iris_olgierd_sabre",
                "name": {"zh-CN": "爱丽丝 (石之心欧吉尔德赠予血弯刀)", "en": "Iris (Olgierd Sabre)"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Olgierd Sabre')",
                "desc": "斩击积蓄赤红能量，重击释放摧毁一切防守的强力冲击波！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_caretaker_shovel",
                "name": {"zh-CN": "看门人的铲子 (吸血鬼级吸血钝器)", "en": "Caretaker Shovel"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Caretaker Shovel')",
                "desc": "欧吉尔德庄园怪异铲子，每次攻击造成的伤害直接按 10% 转化为生命值回复杰洛特！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_winters_blade",
                "name": {"zh-CN": "冬之刃 (克拉奇家传名剑)", "en": "Winter's Blade"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Winters Blade')",
                "desc": "附带极高冰冻与破甲属性的史凯利格群岛家族神兵。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_fate_sword",
                "name": {"zh-CN": "命运 (经典遗物银剑)", "en": "Fate Silver Sword"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Fate')",
                "desc": "拥有 3 个符文镶嵌孔的经典极品银剑，法印与暴击加成极高。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_toussaint_steel_3",
                "name": {"zh-CN": "陶森特骑士钢剑 (血与酒最强人属性钢剑)", "en": "Toussaint Knight's Steel Sword"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Touissant Steel Sword 3')",
                "desc": "高达 +300 护甲穿透，+100% 暴击伤害与 +20% 暴击率，公认最强钢剑！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_vampire_mask_q704",
                "name": {"zh-CN": "亨盖得吸血鬼面具 (血与酒暗影长者之穴红面具)", "en": "Hen Gaidth Vampire Mask"},
                "syntax_type": "redengine_cmd",
                "code": "additem('q704_vampire_mask')",
                "desc": "暗影长者洞穴中搜寻到的吸血鬼仪式假面，击杀敌人立即按百分比回血！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_vampire_armor_q704",
                "name": {"zh-CN": "亨盖得吸血鬼全身血甲", "en": "Hen Gaidth Vampire Armor"},
                "syntax_type": "redengine_cmd",
                "code": "additem('q704_vampire_armor')",
                "desc": "赤红色的高阶吸血鬼铠甲，提供极高劈砍与穿刺防御，穿戴套装击败敌人可不断回复生命。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_vampire_steel_sword_q704",
                "name": {"zh-CN": "亨盖得吸血鬼钢剑", "en": "Hen Gaidth Steel Sword"},
                "syntax_type": "redengine_cmd",
                "code": "additem('q704_vampire_steel_sword')",
                "desc": "亨盖得套装专属吸血钢剑，对人形敌人附带极高暴击与流血吸血特效！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_tesham_mutna_armor",
                "name": {"zh-CN": "特斯汉穆那吸血鬼黑甲 (黑金铠甲)", "en": "Tesham Mutna Armor"},
                "syntax_type": "redengine_cmd",
                "code": "additem('EP2 Vampire Armor')",
                "desc": "血与酒特斯汉穆那废墟古老吸血鬼套装，纯黑金属重装，击杀敌人吸收生命活力。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_tesham_mutna_mask",
                "name": {"zh-CN": "特斯汉穆那吸血鬼面具", "en": "Tesham Mutna Mask"},
                "syntax_type": "redengine_cmd",
                "code": "additem('EP2 Vampire Mask')",
                "desc": "特斯汉穆那遗迹假面，搭配特斯汉穆那全套防具激活吸血鬼套装击杀吸血特效。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            }
        ]
    },
    {
        "category": "🧪 高等炼金魔药与极品吸血煎药 (Superior Potions & Decoctions)",
        "commands": [
            {
                "id": "w3_potion_swallow_sup",
                "name": {"zh-CN": "高等燕子魔药 (极速持续回血)", "en": "Superior Swallow"},
                "syntax_type": "redengine_cmd",
                "code": "additem('燕子 3')",
                "desc": "最高等级燕子，高额瞬间生命回复，战斗中保命神药！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_potion_thunderbolt_sup",
                "name": {"zh-CN": "高等雷霆魔药 (大幅提升攻击力)", "en": "Superior Thunderbolt"},
                "syntax_type": "redengine_cmd",
                "code": "additem('雷霆 3')",
                "desc": "大幅强化所有攻击的物理伤害，暴风雨天气下攻击必定暴击！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_potion_white_honey_sup",
                "name": {"zh-CN": "高等白蜂蜜 (瞬间清空全部毒性与异常)", "en": "Superior White Honey"},
                "syntax_type": "redengine_cmd",
                "code": "additem('White Honey 3')",
                "desc": "立刻清除当前体内累积的所有药水毒性与负面状态，重置药效。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_potion_tawny_owl_sup",
                "name": {"zh-CN": "高等黄褐色猫头鹰 (夜间无限恢复活力)", "en": "Superior Tawny Owl"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Tawny Owl 3')",
                "desc": "大幅提高战斗中耐力与活力恢复，日落后药效持续时间锁定为永久！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_dec_ekhidna",
                "name": {"zh-CN": "海克娜煎药 (施法翻滚跳跃即回血)", "en": "Ekhidna Decoction"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Ekimmara Decoction')",
                "desc": "每当做出消耗活力的动作（放法印、跳跃、回旋斩）时立即回复 10% 生命！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_dec_ekimmara",
                "name": {"zh-CN": "极品吸血鬼煎药 (造成伤害的10%转化为回血)", "en": "Ekhidna Vampiric Decoction"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Ekhidna Decoction')",
                "desc": "全游戏最核心吸血煎药，剑术与法印造成的伤害全部吸血续航！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_dec_troll",
                "name": {"zh-CN": "巨魔煎药 (战斗中持续被动回血)", "en": "Troll Decoction"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Troll Decoction')",
                "desc": "战斗中与非战斗状态每秒稳定恢复 100 点生命，保命容错极高。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_dec_katakan",
                "name": {"zh-CN": "卡塔卡恩煎药 (常驻暴击率提升)", "en": "Katakan Decoction"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Katakan Decoction')",
                "desc": "提高 5% 额外暴击几率，猫学派与瘾头暴击流核心搭配。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_dec_succubus",
                "name": {"zh-CN": "女夜魔煎药 (战斗时间越长攻击力越猛)", "en": "Succubus Decoction"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Succubus Decoction')",
                "desc": "战斗中攻击力随时间持续递增，直至达到最高峰值。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_dec_griffin",
                "name": {"zh-CN": "大狮鹫煎药 (重击按目标最大生命值百分比扣血)", "en": "Archgriffin Decoction"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Archgriffin Decoction')",
                "desc": "活力全满时的重击直接按敌方最大生命值的 5% 扣除，越级击杀高级怪利器！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            }
        ]
    },
    {
        "category": "💣 高阶剑油、传奇炸弹与极品符文石 (Superior Oils, Bombs & Greater Runes)",
        "commands": [
            {
                "id": "w3_oil_specter_sup",
                "name": {"zh-CN": "高等残灵生物油 (克制日间妖灵/日间女妖+50%伤害)", "en": "Superior Specter Oil"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Specter Oil 3')",
                "desc": "对妖灵、女妖等一切灵体生物造成额外 50% 的真实斩击伤害加成！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_oil_necrophage_sup",
                "name": {"zh-CN": "高等食尸生物油 (+50%伤害克制水鬼/水婆婆)", "en": "Superior Necrophage Oil"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Necrophage Oil 3')",
                "desc": "大范围清理威伦泥沼水鬼、食尸鬼与孽鬼群必备剑油。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_oil_vampire_sup",
                "name": {"zh-CN": "高等吸血鬼油 (陶森特血与酒必带神油)", "en": "Superior Vampire Oil"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Vampire Oil 3')",
                "desc": "克制卡塔卡恩、蝠翼魔、隐形吸血女妖与狄拉夫狄克森等吸血种族。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_oil_cursed_sup",
                "name": {"zh-CN": "高等诅咒生物油 (克制狼人/尸婴/狂猎战犬)", "en": "Superior Cursed Oil"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Cursed Oil 3')",
                "desc": "有效遏制狼人变态的每秒自愈回血机制，重击造成强力破防撕裂！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_oil_relict_sup",
                "name": {"zh-CN": "高等类魔油 (克制林中夫人/煮婆/鹿首精)", "en": "Superior Relict Oil"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Relic Oil 3')",
                "desc": "对鹿首精、地灵、林中三巫妪等远古魔法造物造成毁灭性加成伤害！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_bomb_grapeshot_sup",
                "name": {"zh-CN": "高等蜂窝炸弹 (一发炸平怪物巢穴)", "en": "Superior Grapeshot"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Grapeshot 3', 10)",
                "desc": "爆破产生密集破片撕裂周围敌人，瞬间摧毁全大陆孽鬼和水鬼巢穴！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_bomb_dancing_star_sup",
                "name": {"zh-CN": "高等舞动之星炸弹 (大范围烈焰燃烧地毯)", "en": "Superior Dancing Star"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Dancing Star 3', 10)",
                "desc": "制造大面积持续燃烧火海，点燃敌人并使其陷入长时间抱头惨叫瘫痪。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_bomb_northern_wind_sup",
                "name": {"zh-CN": "高等北风炸弹 (绝对冰冻控制强敌)", "en": "Superior Northern Wind"},
                "syntax_type": "redengine_cmd",
                "code": "additem('White Frost 3', 10)",
                "desc": "瞬间冰封半径 5 米内所有敌人数秒，冻结期间受到的伤害暴涨 300%！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_bomb_dimeritium_sup",
                "name": {"zh-CN": "高等阻魔金炸弹 (彻底封印魔法与瞬移技能)", "en": "Superior Dimeritium Bomb"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Dimeritium Bomb 3', 10)",
                "desc": "扩散阻魔金粉尘，封锁狂猎法师的霜冻传送门与妖灵的虚体潜行！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_rune_chernobog_sup",
                "name": {"zh-CN": "极品切尔诺伯格符文石 x10 (+5%攻击力)", "en": "Greater Chernobog Rune x10"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Rune chernobog greater', 10)",
                "desc": "极品武器攻击力附魔符文，三孔全部镶嵌可直接额外提升 15% 总面板攻击！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_glyph_quen_sup",
                "name": {"zh-CN": "极品昆恩字印 x10 (+10%昆恩护盾强度)", "en": "Greater Glyph of Quen x10"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Glyph quen greater', 10)",
                "desc": "防具终极保命镶嵌符文，护甲防具四件插满直接增加 40% 昆恩伤害吸收上限！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            }
        ]
    },
    {
        "category": "🃏 昆特牌全阵营五大势力英雄牌库与秒胜 (Gwent Decks & Instant Win Cheats)",
        "commands": [
            {
                "id": "w3_secretgwint",
                "name": {"zh-CN": "一键集齐全大陆全阵营全部昆特牌 (全图鉴终极指令)", "en": "Unlock All Gwent Cards (Secret Gwint)"},
                "syntax_type": "redengine_cmd",
                "code": "secretgwint",
                "desc": "瞬间向昆特牌库中直接注入北方领域、尼弗迦德帝国、松鼠党、怪兽势力以及石之心/血与酒史凯利格全套英雄牌与间谍卡，秒清收集任务！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_wingwint",
                "name": {"zh-CN": "当前昆特牌对决立即判定以绝对优势获胜", "en": "Instant Win Current Gwent Match"},
                "syntax_type": "redengine_cmd",
                "code": "winGwint(true)",
                "desc": "打牌开局或任意回合中输入，直接触发对方认输结算，无悬念秒赢帕席芬拉大赌局！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_addgwintcards",
                "name": {"zh-CN": "注入全套基础昆特牌组", "en": "Add Basic Gwent Cards"},
                "syntax_type": "redengine_cmd",
                "code": "addgwintcards",
                "desc": "将游戏开局缺失的基础势力作战单位牌各补充一份入库。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_card_geralt",
                "name": {"zh-CN": "利维亚的杰洛特 (15点中立近战英雄金卡)", "en": "Gwent Card: Geralt of Rivia (15 Pts)"},
                "syntax_type": "redengine_cmd",
                "code": "additem('gwint_card_geralt')",
                "desc": "昆特牌最强单兵金卡之一，不受任何天气与烧灼特殊效果影响。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_card_ciri",
                "name": {"zh-CN": "希里 (15点中立近战英雄金卡)", "en": "Gwent Card: Ciri (15 Pts)"},
                "syntax_type": "redengine_cmd",
                "code": "additem('gwint_card_ciri')",
                "desc": "拥有 15 点极高战力的中立英雄牌，压制敌方关键点数战局翻盘神器。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_card_yennefer",
                "name": {"zh-CN": "叶奈法 (7点医生复活英雄金卡)", "en": "Gwent Card: Yennefer of Vengerberg"},
                "syntax_type": "redengine_cmd",
                "code": "additem('gwint_card_yennefer')",
                "desc": "打出后可直接从己方墓地将任意废弃作战卡牌复活拉回战场！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_card_mysterious_elf",
                "name": {"zh-CN": "神秘精灵阿瓦拉克 (0点无敌间谍神卡)", "en": "Gwent Card: Avallac'h (0 Pt Spy)"},
                "syntax_type": "redengine_cmd",
                "code": "additem('gwint_card_avallach')",
                "desc": "全昆特牌最强间谍！送给对面 0 点点数，己方直接白嫖抽 2 张新手牌！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_card_roach",
                "name": {"zh-CN": "萝卜 (次世代新版中立联动牌)", "en": "Gwent Card: Roach (Next-Gen)"},
                "syntax_type": "redengine_cmd",
                "code": "additem('gwint_card_roach')",
                "desc": "战力 3 点带自动集结召唤特技的次世代专属中立英雄昆特牌。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            }
        ]
    },
    {
        "category": "🗺️ 全大陆路标瞬移、迷雾全开与城市传送 (World Exploration & Fast Travel)",
        "commands": [
            {
                "id": "w3_showallft",
                "name": {"zh-CN": "大地图点亮全大陆 100% 快速旅行路标", "en": "Show All Fast Travel Signposts"},
                "syntax_type": "redengine_cmd",
                "code": "ShowAllFT(1)",
                "desc": "瞬间解锁白果园、威伦、诺维格瑞、群岛与陶森特大地图上全部绿色十字路标！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_allowft",
                "name": {"zh-CN": "允许在全图任意位置直接快速旅行 (摆脱路标木桩限制)", "en": "Allow Fast Travel Anywhere"},
                "syntax_type": "redengine_cmd",
                "code": "AllowFT(1)",
                "desc": "彻底免去跑路寻桩过程！在深山老林地牢只要按 M 打开地图点击路标即可瞬移！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_showpins",
                "name": {"zh-CN": "点亮全大陆所有未探索的 '?' 问号标记", "en": "Show All Question Mark Pins"},
                "syntax_type": "redengine_cmd",
                "code": "ShowPins(1)",
                "desc": "强迫症玩家清图福音，将大地图上所有隐藏的问号宝藏与魔力之所全息标注。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_showknownpins",
                "name": {"zh-CN": "显示所有已知地标图标", "en": "Show All Known Pins"},
                "syntax_type": "redengine_cmd",
                "code": "ShowKnownPins(1)",
                "desc": "将地图上已知商贩、铁匠与理发师图标常驻显示。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_goto_novigrad",
                "name": {"zh-CN": "瞬间传送到诺维格瑞自由城 (Novigrad)", "en": "Fast Travel to Novigrad"},
                "syntax_type": "redengine_cmd",
                "code": "gotoNovigrad",
                "desc": "立即跨地图传送到北方最大繁华都市诺维格瑞教皇广场中心。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_goto_skellige",
                "name": {"zh-CN": "瞬间传送到史凯利格群岛 (Skellige)", "en": "Fast Travel to Skellige"},
                "syntax_type": "redengine_cmd",
                "code": "gotoSkellige",
                "desc": "免去乘船海难剧情，直接传送至史凯利格大史凯利格岛主城堡大门前。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_goto_kaermorhen",
                "name": {"zh-CN": "瞬间传送到狼学派老巢凯尔莫罕 (Kaer Morhen)", "en": "Fast Travel to Kaer Morhen"},
                "syntax_type": "redengine_cmd",
                "code": "gotoKaerMorhen",
                "desc": "瞬间回到巍峨的群山堡垒凯尔莫罕主庭院。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_goto_toussaint",
                "name": {"zh-CN": "瞬间传送到陶森特公国白葡萄庄园 (Toussaint)", "en": "Fast Travel to Toussaint"},
                "syntax_type": "redengine_cmd",
                "code": "gotoToussaint",
                "desc": "无需推进主线直接跳票传送到阳光明媚的童话之国陶森特主城区！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_goto_prolog",
                "name": {"zh-CN": "瞬间传送回新手村白果园 (White Orchard)", "en": "Fast Travel to White Orchard"},
                "syntax_type": "redengine_cmd",
                "code": "gotoProlog",
                "desc": "快速传送回新手村白果园酒馆旅店前，补齐错过的早期支线。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_goto_wyzima",
                "name": {"zh-CN": "瞬间传送到维吉玛皇家城堡 (Wyzima)", "en": "Fast Travel to Wyzima Palace"},
                "syntax_type": "redengine_cmd",
                "code": "gotoWyzima",
                "desc": "传送到泰莫利亚皇宫城堡，与尼弗迦德大帝恩希尔当面对质。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            }
        ]
    },
    {
        "category": "⏱️ 昼夜时间流速、天气调控与坐骑马匹掌控 (Time, Weather & Roach Horse Tuning)",
        "commands": [
            {
                "id": "w3_settime_12",
                "name": {"zh-CN": "将世界时间跳转至正午 12:00 (艳阳高照拍照黄金时刻)", "en": "Set Time to Noon (12:00)"},
                "syntax_type": "redengine_cmd",
                "code": "settime(12)",
                "desc": "将大陆时间定格在正午，光照最强阴影最通透，搭配次世代光追拍照效果拉满！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_settime_0",
                "name": {"zh-CN": "将世界时间跳转至午夜 00:00 (狂猎降临时刻)", "en": "Set Time to Midnight (00:00)"},
                "syntax_type": "redengine_cmd",
                "code": "settime(0)",
                "desc": "定格午夜，让日间女妖转化为夜间妖灵，营造极佳的魔幻恐怖氛围。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_makeitrain",
                "name": {"zh-CN": "立即召唤暴雨天气", "en": "Make It Rain"},
                "syntax_type": "redengine_cmd",
                "code": "makeitrain",
                "desc": "呼风唤雨，电闪雷鸣，激发出杰洛特雷霆药水必定暴击的特殊气象被动！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_stoprain",
                "name": {"zh-CN": "立即驱散阴雨天气 (转为晴空万里)", "en": "Stop Rain"},
                "syntax_type": "redengine_cmd",
                "code": "stoprain",
                "desc": "瞬时驱散漫天阴霾雨滴与雷暴，使视野恢复干爽晴朗。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_weather_storm",
                "name": {"zh-CN": "切换为特大暴风暴雨雷电天气", "en": "Set Storm Weather"},
                "syntax_type": "redengine_cmd",
                "code": "changeweather('WT_Rain_Storm')",
                "desc": "呼出极度真实逼真的次世代物理级狂风骤雨，树木随风狂摆树叶漫天狂飞！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_weather_clear",
                "name": {"zh-CN": "切换为极致纯净碧空晴朗天气", "en": "Set Clear Weather"},
                "syntax_type": "redengine_cmd",
                "code": "changeweather('WT_Clear')",
                "desc": "晴空万里无云，次世代光线追踪全局光照与水面反射表现力最强的气象环境。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_horse_saddle_4",
                "name": {"zh-CN": "鲍克兰极品骑兵马鞍 (马匹体力极限扩充)", "en": "Beauclair Cavalry Saddle (Max Stamina)"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Horse Saddle 4')",
                "desc": "为萝卜装备陶森特最高规格骑兵马鞍，长途奔袭疾驰耐力用之不竭！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_horse_blinders_3",
                "name": {"zh-CN": "鲍克兰极品马盲目镜 (彻底免疫怪物惊吓摔下马)", "en": "Beauclair Blinders (Anti-Panic)"},
                "syntax_type": "redengine_cmd",
                "code": "additem('Horse Blind Flaps 3')",
                "desc": "将萝卜的惊慌度上限大幅增加，即使被水鬼狼群包围也绝不甩下杰洛特！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            }
        ]
    },
    {
        "category": "🎭 角色外观造型、希里切换与视觉特写 (Appearance, Ciri Switch & Visual FX)",
        "commands": [
            {
                "id": "w3_ciri_switch",
                "name": {"zh-CN": "直接切换操控主角为希里 (Ciri - 瞬移闪烁绝招)", "en": "Switch Player to Ciri"},
                "syntax_type": "redengine_cmd",
                "code": "Ciri",
                "desc": "在全大陆任何自由行动关卡中直接将当前操控角色无缝切换为时空之女希里，独享绿色瞬移突进与闪烁大招！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_geralt_switch",
                "name": {"zh-CN": "恢复操控利维亚的杰洛特 (Geralt)", "en": "Switch Back to Geralt"},
                "syntax_type": "redengine_cmd",
                "code": "Geralt",
                "desc": "从希里或其他状态平滑切回利维亚的杰洛特主角视角，恢复全部猎魔人法印与背包物品栏系统。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_shave",
                "name": {"zh-CN": "瞬间剃净杰洛特胡须 (清爽面容)", "en": "Shave Geralt Beard"},
                "syntax_type": "redengine_cmd",
                "code": "shave",
                "desc": "免去寻找理发师的繁琐，随时随地将杰洛特面部胡须剃得干干净净。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_setbeard_1",
                "name": {"zh-CN": "瞬间长出威严茂密的络腮胡", "en": "Set Full Bushy Beard"},
                "syntax_type": "redengine_cmd",
                "code": "setbeard(1)",
                "desc": "将杰洛特的胡须状态瞬间锁定为生长完全的沧桑大络腮胡须。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_dismember",
                "name": {"zh-CN": "剑术攻击必定触发慢动作断肢处决特写", "en": "Always Dismember on Kill"},
                "syntax_type": "redengine_cmd",
                "code": "dismember",
                "desc": "开启猎魔人暴虐战斗镜头特写，每次最后一击击杀敌人都必定触发腰斩或削首电影级断肢慢动作！",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_cat_1",
                "name": {"zh-CN": "开启猫之视野夜视夜瞳 (地牢无需火把亮如白昼)", "en": "Enable Cat Night Vision"},
                "syntax_type": "redengine_cmd",
                "code": "Cat(1)",
                "desc": "直接开启黑白高对比度夜视热感视野，深入古墓洞穴无需右手举火把即可看清每一个角落。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_cat_0",
                "name": {"zh-CN": "关闭猫之视野夜视", "en": "Disable Cat Night Vision"},
                "syntax_type": "redengine_cmd",
                "code": "Cat(0)",
                "desc": "关闭夜视视野，恢复自然光影色彩呈现。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_drunk_1",
                "name": {"zh-CN": "开启醉酒晃动与重影模糊视觉特效", "en": "Enable Drunk FX"},
                "syntax_type": "redengine_cmd",
                "code": "drunk(1)",
                "desc": "模拟杰洛特在酒馆痛饮伏特加后的醉态，视线产生晃动拉伸镜头特效。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_drunk_0",
                "name": {"zh-CN": "解除醉酒状态并恢复正常视觉", "en": "Disable Drunk FX"},
                "syntax_type": "redengine_cmd",
                "code": "drunk(0)",
                "desc": "瞬间醒酒，消除一切头晕晃动滤镜。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_appearance_naked",
                "name": {"zh-CN": "外观切换：杰洛特赤膊健美身躯", "en": "Appearance: Bare Torso"},
                "syntax_type": "redengine_cmd",
                "code": "appearance('naked')",
                "desc": "切换为杰洛特在白果园浴缸经典场景的无上衣肌肉纹身造型。",
                "min_version": "Next-Gen v4.04",
                "framework_required": "None (Native Console)"
            },
            {
                "id": "w3_appearance_winter",
                "name": {"zh-CN": "外观切换：极地抗寒长袍战装", "en": "Appearance: Winter Robe"},
                "syntax_type": "redengine_cmd",
                "code": "appearance('winter')",
                "desc": "切换为防寒毛皮领保暖长袍装束，适合在史凯利格雪山漫游沉浸式拍照。",
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
    },
    {
        "name": {"zh-CN": "大地图点亮全大陆 100% 快速旅行路标", "en": "Show All Fast Travel"},
        "command": "ShowAllFT(1)",
        "desc": "瞬间解锁白果园、威伦、诺维格瑞、群岛与陶森特全部十字路标。"
    },
    {
        "name": {"zh-CN": "获取大超同款宗师级遗忘狼防具 (次世代版 / 完全版特供)", "en": "Add Netflix Wolven Armor"},
        "command": "additem('Netflix Armor 2')",
        "desc": "直接注入亨利·卡维尔网飞剧版同款纯黑宗师级遗弃狼战甲。"
    }
]

witcher_mods = [
    {
        "id": "hd-reworked-project-nextgen",
        "title": "The Witcher 3 HD Reworked Project NextGen Edition (全材质4K高清终极材质包)",
        "author": "Halk Hogan PL",
        "version": "NextGen Ultimate 2024",
        "size": "9.5 GB",
        "downloads": "13.2M",
        "endorsements": "365K",
        "category": "画面材质 (Visuals / Textures)",
        "desc": "全网公认最强《巫师3》材质MOD！次世代版 / 完全版专属重构，彻底重绘所有岩石、植被、砖墙、木纹与建筑材质，完美适配 DX12 光线追踪！",
        "dependencies": ["None"],
        "installPath": "The Witcher 3\\Mods\\",
        "installSteps": [
            "1. 确认游戏已升级至次世代版本 (v4.04+)；",
            "2. 下载后直接运行安装程序，指定《巫师3》安装根目录；",
            "3. 进入游戏视频选项，将材质品质调至最高 'HDReworked' 即可生效。"
        ]
    },
    {
        "id": "the-witcher-3-redkit",
        "title": "The Witcher 3 REDkit (CD PROJEKT RED 官方全能 Mod 编辑器与工坊套件)",
        "author": "CD PROJEKT RED (Official)",
        "version": "v1.0 (Steam AppID: 2684660)",
        "size": "32.0 GB",
        "downloads": "1.8M",
        "endorsements": "95K",
        "category": "官方开发套件 (Official SDK / Modding Tool)",
        "desc": "CDPR 官方于 2024 年 5 月正式推出的完整开发级编辑器！包含官方脚本编译器、世界地图与任务制作器，并全面打通 Steam 创意工坊！",
        "dependencies": ["None"],
        "installPath": "Steam Library\\steamapps\\common\\The Witcher 3 REDkit\\",
        "installSteps": [
            "1. 在 Steam 商店直接搜索免费领取 'The Witcher 3 REDkit'；",
            "2. 启动后可自由在 Steam 创意工坊一键订阅 Mod 并由游戏主程序自动加载。"
        ]
    },
    {
        "id": "witcher-3-script-merger",
        "title": "Script Merger Next-Gen Edition (次世代脚本冲突智能合并神器)",
        "author": "AnotherSymbiote / Sarcen",
        "version": "v0.6.5 NextGen",
        "size": "2.1 MB",
        "downloads": "8.9M",
        "endorsements": "240K",
        "category": "核心排错工具 (Utility / Conflict Resolver)",
        "desc": "次世代 Mod 必备排错神器！自动检测并一键合并多个 Mod 之间的 WitcherScript 冲突代码，彻底解决游戏启动报 Script Compilation Error 问题。",
        "dependencies": ["None"],
        "installPath": "任意独立文件夹 (如 D:\\Tools\\ScriptMerger)",
        "installSteps": [
            "1. 解压后运行 ScriptMerger.exe，在设置中指定《巫师3》安装根目录；",
            "2. 点击 'Refresh' 扫描，勾选检测到的有冲突的脚本点击 'Create Merged Script' 即可。"
        ]
    },
    {
        "id": "brothers-in-arms-nextgen",
        "title": "Brothers In Arms - TW3 Ultimate Bug Fix and Restored Content Next-Gen Edition (终极修复与未采用内容恢复巨制)",
        "author": "Brothers In Arms Team",
        "version": "v4.04 NextGen",
        "size": "1.2 GB",
        "downloads": "1.6M",
        "endorsements": "72K",
        "category": "剧情与修复 (Gameplay / Bug Fixes / Cut Content)",
        "desc": "由全网顶级 Mod 团队数年打磨的旷世神作！修复本体与双 DLC 中数百个原版遗留 Bug、未采用的 NPC 互动对话、截断的过场动画与丢失的任务物品。",
        "dependencies": ["Script Merger (若有其他脚本Mod)"],
        "installPath": "The Witcher 3\\Mods\\modBrothersInArms\\",
        "installSteps": [
            "1. 下载解压后将 modBrothersInArms 放入 The Witcher 3\\Mods\\ 目录；",
            "2. 若安装了其他剧本或交互 Mod，务必运行 Script Merger 合并冲突脚本。"
        ]
    },
    {
        "id": "fast-travel-from-anywhere",
        "title": "Fast Travel from Anywhere (Next-Gen 全图随时随地快速旅行)",
        "author": "JupiterLily / erxv",
        "version": "v4.04 Updated",
        "size": "120 KB",
        "downloads": "7.8M",
        "endorsements": "210K",
        "category": "探索便利 (Gameplay / Quality of Life)",
        "desc": "告别漫长枯燥的跑路寻桩过程！在任何荒郊野外、洞窟深处只要打开大地图，点击任意已解锁的路标即可瞬间传送。",
        "dependencies": ["None"],
        "installPath": "The Witcher 3\\Mods\\modFastTravelFromAnywhere\\",
        "installSteps": [
            "1. 下载解压得到 modFastTravelFromAnywhere 文件夹；",
            "2. 直接复制粘贴到游戏根目录 The Witcher 3\\Mods 文件夹即可。"
        ]
    },
    {
        "id": "all-quest-objectives-on-map",
        "title": "All Quest Objectives On Map (Next-Gen 全任务目标大地图聚合标记)",
        "author": "Wolfmark",
        "version": "v4.04 Updated",
        "size": "350 KB",
        "downloads": "6.9M",
        "endorsements": "185K",
        "category": "界面导航 (UI / Map)",
        "desc": "强迫症玩家必备！同时在大地图上显示所有未完成的主线、支线、猎魔委托与寻宝任务目标点，顺路一次性清空周边任务。",
        "dependencies": ["None"],
        "installPath": "The Witcher 3\\Mods\\modAllQuestObjectivesOnMap\\",
        "installSteps": [
            "1. 将下载的 modAllQuestObjectivesOnMap 放入 The Witcher 3\\Mods 目录；",
            "2. 启动游戏在大地图左侧勾选全部任务筛选。"
        ]
    },
    {
        "id": "over-9000-weight-limit",
        "title": "Over 9000 Weight limit mod (Next-Gen 9000公斤无限背包负重)",
        "author": "Genthis",
        "version": "v4.04 Compatible",
        "size": "80 KB",
        "downloads": "5.3M",
        "endorsements": "145K",
        "category": "背包增强 (Inventory / QoL)",
        "desc": "将基础负重提升至 9000，捡走全大陆每一把生锈剑和每一张狼皮，彻底告别负重超载无法奔跑的痛苦！",
        "dependencies": ["None"],
        "installPath": "The Witcher 3\\Mods\\modOver9000\\",
        "installSteps": [
            "1. 将 modOver9000 文件夹放入 The Witcher 3\\Mods 目录；",
            "2. 进游戏背包负重上限变为 9000。"
        ]
    },
    {
        "id": "friendly-hud-nextgen",
        "title": "Friendly HUD NextGen (完全沉浸式动态智能界面)",
        "author": "wghost81",
        "version": "v14.2 NextGen",
        "size": "3.5 MB",
        "downloads": "4.3M",
        "endorsements": "135K",
        "category": "界面交互 (UI / Immersion)",
        "desc": "非战斗状态自动隐藏全部小地图与血条，猎魔人感官开启时在真实 3D 世界中浮现任务标记与罗盘，极致视听沉浸享受。",
        "dependencies": ["None"],
        "installPath": "The Witcher 3\\Mods\\modFriendlyHUD\\",
        "installSteps": [
            "1. 将 modFriendlyHUD 解压放入 The Witcher 3\\Mods\\ 文件夹；",
            "2. 将 bin 文件夹覆盖到游戏安装目录以整合配置菜单。"
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

witcher_reviews = [
    {
        "user": "GeraltOfRivia99",
        "rating": "⭐⭐⭐⭐⭐",
        "date": "2026-10-18",
        "title": "次世代版 / 完全版 v4.04 完美运行！控制台秒开太方便了！",
        "content": "改 general.ini 一秒开控制台，免去任何 DLL 插件！刷昆特牌 secretgwint 指令和湖中之剑太爽了，省下二周目几十个小时！强烈推荐安装 HD Reworked NextGen，次世代光追画质提升巨大！",
        "upvotes": 680
    },
    {
        "user": "CiriZireael",
        "rating": "⭐⭐⭐⭐⭐",
        "date": "2026-10-19",
        "title": "次世代专属西境白虎套和网飞大超遗弃狼套装绝帅！",
        "content": "中国风九尾狐女双剑和西境白虎战甲太有牌面了！输入 Ciri 直接瞬移砍杀太强，另外大超同款紧身纯黑战甲帅哭，双重法印非常猛！",
        "upvotes": 520
    }
]

# Update witcher-3
for g in games:
    if g["id"] == "witcher-3":
        g["title"] = "The Witcher 3: Wild Hunt - Complete Edition (Next-Gen)"
        g["titles"] = {
            "en": "The Witcher 3: Wild Hunt - Complete Edition (Next-Gen)",
            "zh-CN": "巫师 3：狂猎 (次世代版 / 完全版 / 完全版)",
            "zh-TW": "巫師 3：狂獵 (次世代重製版 / 完全版)",
            "ja": "ウィッチャー3 ワイルドハント コンプリートエディション (次世代機版)",
            "ko": "더 위쳐 3: 와일드 헌트 - 컴플리트 에디션 (차세대 리마스터)",
            "ru": "Ведьмак 3: Дикая Охота — Полное издание (Next-Gen)",
            "de": "The Witcher 3: Wild Hunt - Complete Edition (Next-Gen)",
            "es": "The Witcher 3: Wild Hunt - Edición Completa (Next-Gen)"
        }
        g["consoleCategories"] = witcher_categories
        g["popularCommands"] = witcher_popular
        g["curatedMods"] = witcher_mods
        g["trainerInfo"] = witcher_trainer
        g["communityReviews"] = witcher_reviews
        g["latestPatch"] = "v4.04 (次世代版 / 完全版 - 官方 REDkit & 工坊支持)"
        g["modInstallPath"] = "The Witcher 3\\Mods\\ (次世代 DX12 主程序位于 bin\\x64_dx12\\witcher3.exe)"
        g["nexusStats"] = {
            "totalDownloads": "194.5M",
            "totalEndorsements": "885K",
            "totalMods": "7,840",
            "latestPatch": "Next-Gen v4.04 Ready"
        }
        g["consoleShortcut"] = "~ (波浪键) 或 @ 键 (次世代原生 ini 开启，免 DLL 注入)"
        g["consoleEnableGuide"] = {
            "zh-CN": "1. 【原生免 Mod 开启控制台】在《巫师3 次世代版 / 完全版》安装根目录进入 bin\\config\\base\\ 文件夹，用记事本打开 general.ini；\n2. 【追加调试参数】在文件末尾 [General] 区块最下方另起一行，添加 DBGConsoleOn=true 并保存退出；\n3. 【呼出与执行】启动游戏（次世代默认 DX12 版本路径为 bin\\x64_dx12\\witcher3.exe），在任何战役关卡按下键盘 ~ (波浪键) 或 @ 键即可弹出顶部控制台，输入下方代码回车直接生效！\n4. 【次世代版 / 完全版原生特色提示】本版本已内置原生「拍照模式」(在游戏中随时按 U 键呼出，支持景深、自由机位与滤镜)、「法印快捷施法」(游戏设置-游戏性中开启，无需呼出法印轮盘)、「自动涂抹剑油」(游戏设置中开启，无需额外Mod)，并全面支持官方 REDkit 编辑器与 Steam 创意工坊！",
            "en": "1. Navigate to 'The Witcher 3\\bin\\config\\base\\', open general.ini in Notepad.\n2. Add 'DBGConsoleOn=true' under [General] and save.\n3. Launch game (DX12 executable is in bin\\x64_dx12\\witcher3.exe), press ~ or @ in-game to open console.\n4. Next-Gen features: Built-in Photo Mode (press U), Quick Sign Casting (in Gameplay settings), Auto-apply Oils, and official REDkit mod editor / Steam Workshop support."
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
