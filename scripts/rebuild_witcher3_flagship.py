#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/rebuild_witcher3_flagship.py
Content for The Witcher 3 (console guide, command categories, curated mods,
metadata).

Writes only the fields in OWNED_FIELDS of witcher-3, through gamedata_guard: the master
data must exist, radar and trainer fields are never written (trainer data comes from
fling_trainer_sync.py), and in public/data.js only the GAMES_DATA segment changes
(TRANSLATIONS_DATA is left alone). No player reviews are written.

Usage: python3 scripts/rebuild_witcher3_flagship.py [--dry-run]
"""

from gamedata_guard import write_owned_fields

GAME_ID = "witcher-3"

witcher_categories = [
    {
        "category": "👑 核心上帝模式与主角机体掌控 (God Mode & Invincibility)",
        "commands": [
            {
                "id": "w3_god",
                "name": {
                    "zh-CN": "上帝模式",
                    "en": "God Mode"
                },
                "syntax_type": "redengine_cmd",
                "code": "god",
                "desc": "开启后杰洛特免疫伤害：生命值和昆恩法印护盾锁定，不会被怪物攻击、挥砍、中毒、摔落或狂猎霜冻击破；再次输入指令可关闭。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/god"
            },
            {
                "id": "w3_likeaboss",
                "name": {
                    "zh-CN": "像大Boss一样战斗 (每次攻击造成敌方最大生命值40%伤害)",
                    "en": "Like a Boss Mode"
                },
                "syntax_type": "redengine_cmd",
                "code": "likeaboss",
                "desc": "开启后(可再次输入关闭)，杰洛特对敌人造成的每次攻击伤害变为该敌人最大生命值的40%；该效果不会降低杰洛特自身受到的伤害。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/likeaboss"
            },
            {
                "id": "w3_healme",
                "name": {
                    "zh-CN": "瞬间全状态恢复满血",
                    "en": "Heal to Full"
                },
                "syntax_type": "redengine_cmd",
                "code": "healme",
                "desc": "立即将杰洛特的生命值回满。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/healme"
            },
            {
                "id": "w3_killall",
                "name": {
                    "zh-CN": "清除视野内敌人",
                    "en": "Kill All Enemies"
                },
                "syntax_type": "redengine_cmd",
                "code": "killall",
                "desc": "清除当前战斗视野范围内的敌人，包括妖灵、狂猎士兵、孽鬼与部分 Boss。",
                "framework_required": "None (Native Console)",
                "source": "https://web.archive.org/web/20260518032436/https://primagames.com/tips/witcher-3-next-gen-console-commands-full-list-of-cheats"
            },
            {
                "id": "w3_witchcraft",
                "name": {
                    "zh-CN": "添加全部道具各 1 份",
                    "en": "Witchcraft All Items"
                },
                "syntax_type": "redengine_cmd",
                "code": "witchcraft",
                "desc": "将游戏中武器、防具、原料、图纸等物品各添加 1 份到背包（执行时可能有短暂卡顿，背包负重会明显增加）。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/witchcraft"
            },

        ]
    },
    {
        "category": "🎯 角色等级、经验值与全技能洗点 (Levels, XP & Skill Tree)",
        "commands": [
            {
                "id": "w3_setlevel_100",
                "name": {
                    "zh-CN": "角色等级直接设为 100 级",
                    "en": "Set Level 100"
                },
                "syntax_type": "redengine_cmd",
                "code": "setlevel(100)",
                "desc": "将杰洛特的等级直接设为 100 级（游戏等级上限），满足陶森特与石之心部分装备的等级需求。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/setlevel"
            },
            {
                "id": "w3_levelup",
                "name": {
                    "zh-CN": "角色等级提升 1 级",
                    "en": "Level Up"
                },
                "syntax_type": "redengine_cmd",
                "code": "levelup",
                "desc": "让杰洛特立即升 1 级并获得相应的属性与能力点。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/levelup"
            },
            {
                "id": "w3_addexp_10000",
                "name": {
                    "zh-CN": "增加 10,000 点人物经验值",
                    "en": "Add 10,000 XP"
                },
                "syntax_type": "redengine_cmd",
                "code": "addexp(10000)",
                "desc": "注入 10000 点战斗与任务经验值，按游戏原本曲线稳定升级。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/addexp"
            },
            {
                "id": "w3_addskillpoints_50",
                "name": {
                    "zh-CN": "获得 50 点技能点",
                    "en": "Add 50 Skill Points"
                },
                "syntax_type": "redengine_cmd",
                "code": "addskillpoints(50)",
                "desc": "直接增加 50 点未分配的技能点，可用于点出战斗、法印、炼金与突变分支中的更多技能。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/addskillpoints"
            },
            {
                "id": "w3_addskillpoints_10",
                "name": {
                    "zh-CN": "获得 10 点技能点数",
                    "en": "Add 10 Skill Points"
                },
                "syntax_type": "redengine_cmd",
                "code": "addskillpoints(10)",
                "desc": "小幅增加 10 点能力点数，满足某个专精支线的快速加点需求。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/addskillpoints"
            },
            {
                "id": "w3_cleardevelop",
                "name": {
                    "zh-CN": "完全重置角色 (清空等级、背包与装备，重置为1级)",
                    "en": "Reset Character Completely"
                },
                "syntax_type": "redengine_cmd",
                "code": "cleardevelop",
                "desc": "将杰洛特的等级重置为1级，并清空背包物品与已装备的所有装备，重新给予新手初始装备；这不是单纯的洗点。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/cleardevelop"
            },
            {
                "id": "w3_learnskill_swordsmanship",
                "name": {
                    "zh-CN": "直接解锁剑术大师技能",
                    "en": "Learn Sword Mastery"
                },
                "syntax_type": "redengine_cmd",
                "code": "learnskill('sword_s1')",
                "desc": "直接学会并解锁剑术第一阶核心被动技能。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/skills"
            }
        ]
    },
    {
        "category": "💰 金币、负重上限与大突变诱发物 (Crowns, Weight & Greater Mutagens)",
        "commands": [
            {
                "id": "w3_addmoney_100k",
                "name": {
                    "zh-CN": "增加 100,000 克朗金币",
                    "en": "Add 100,000 Crowns"
                },
                "syntax_type": "redengine_cmd",
                "code": "addmoney(100000)",
                "desc": "增加 100,000 克朗，可用于购买宗师级装备材料或陶森特庄园升级等花费较高的内容。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/addmoney"
            },
            {
                "id": "w3_addmoney_10k",
                "name": {
                    "zh-CN": "增加 10,000 克朗金币",
                    "en": "Add 10,000 Crowns"
                },
                "syntax_type": "redengine_cmd",
                "code": "addmoney(10000)",
                "desc": "增加 10000 克朗，用于日常补给魔药与修理装备。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/addmoney"
            },
            {
                "id": "w3_removemoney_50k",
                "name": {
                    "zh-CN": "扣除 50,000 克朗金币 (还清债务/降低难度)",
                    "en": "Remove 50,000 Crowns"
                },
                "syntax_type": "redengine_cmd",
                "code": "removemoney(50000)",
                "desc": "清减多余资产，体验身无分文的底层猎魔人真实流浪生活。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/removemoney"
            },
            {
                "id": "w3_mutagen_red_greater",
                "name": {
                    "zh-CN": "大红突变诱发物 x10",
                    "en": "Greater Red Mutagen x10"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Greater mutagen red', 10)",
                "desc": "可镶嵌到红色技能格中，每镶嵌一个使相关攻击力提升 10%（最多叠加到 +40%）；也可用于合成对应的突变煎药。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/greater-mutagen-red"
            },
            {
                "id": "w3_mutagen_blue_greater",
                "name": {
                    "zh-CN": "大蓝突变诱发物 x10",
                    "en": "Greater Blue Mutagen x10"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Greater mutagen blue', 10)",
                "desc": "可镶嵌到蓝色技能格中，每镶嵌一个使法印强度提升 10%（最多叠加到 +40%）；也可用于合成对应的突变煎药。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/greater-mutagen-blue"
            },
            {
                "id": "w3_mutagen_green_greater",
                "name": {
                    "zh-CN": "大绿突变诱发物 x10",
                    "en": "Greater Green Mutagen x10"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Greater mutagen green', 10)",
                "desc": "可镶嵌到绿色技能格中，每镶嵌一个使最大生命值提升 150 点（最多叠加到 +600）；也可用于合成对应的突变煎药。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/greater-mutagen-green"
            },
            {
                "id": "w3_horse_bag_3",
                "name": {
                    "zh-CN": "陶森特马鞍袋 (最高等级)",
                    "en": "Beauclair Saddlebags (Max Capacity)"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Horse Bag 3')",
                "desc": "获得陶森特马鞍袋，提升杰洛特的背包负重上限；是该类马鞍袋中的最高等级。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/horse-bag-3"
            }
        ]
    },
    {
        "category": "🌟 次世代版 / 完全版专属装备与网飞联动 (Next-Gen Remaster Exclusives & Netflix Rewards)",
        "commands": [
            {
                "id": "w3_white_tiger_armor",
                "name": {
                    "zh-CN": "西境白虎盔甲 (次世代中文配音特供中国风战甲)",
                    "en": "White Tiger Armor"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('White Tiger Armor')",
                "desc": "CDPR 为次世代版 / 完全版中文语音实装专属打造的提尔格里希白虎甲胄，绣有金丝盘龙与猛虎纹样，防御力与抗性出众。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/White_Tiger_of_the_West_armor"
            },
            {
                "id": "w3_white_tiger_boots",
                "name": {
                    "zh-CN": "西境白虎靴子",
                    "en": "White Tiger Boots"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('White Tiger Boots')",
                "desc": "西境白虎套装护足，提供优秀的穿刺伤害抵抗与移动稳定性。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/White_Tiger_of_the_West_boots"
            },
            {
                "id": "w3_white_tiger_gloves",
                "name": {
                    "zh-CN": "西境白虎手套",
                    "en": "White Tiger Gloves"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('White Tiger Gloves')",
                "desc": "西境白虎套装护手，提升攻击速度与法印强度加成。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/White_Tiger_of_the_West_vambraces"
            },
            {
                "id": "w3_white_tiger_pants",
                "name": {
                    "zh-CN": "西境白虎下装",
                    "en": "White Tiger Pants"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('White Tiger Pants')",
                "desc": "西境白虎战袍长裤，提供高额斩击抗性与活力恢复速度。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/White_Tiger_of_the_West_trousers"
            },
            {
                "id": "w3_white_tiger_steel_sword",
                "name": {
                    "zh-CN": "九尾狐女钢剑 (西境白虎配套名刀)",
                    "en": "Vixen Steel Sword"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Steel Vixen')",
                "desc": "刀身刻有青丘灵狐符文的东亚风格优雅佩剑，大幅提高暴击率与暴击伤害加成。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Nine-Tailed_Vixen_steel_sword"
            },
            {
                "id": "w3_white_tiger_silver_sword",
                "name": {
                    "zh-CN": "九尾狐女银剑 (西境白虎配套银刃)",
                    "en": "Vixen Silver Sword"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Silver Vixen')",
                "desc": "针对怪物魔兽的灵狐银剑，击中敌人时有极高概率附加流血与失衡效果。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Nine-Tailed_Vixen_silver_sword"
            },
            {
                "id": "w3_dol_blathanna_armor",
                "name": {
                    "zh-CN": "多尔·布雷坦纳千花盔甲 (次世代特典精灵华服)",
                    "en": "Dol Blathanna Armor"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Dol Blathanna Armor')",
                "desc": "来自百花谷精灵工匠精心编织的轻型锁子甲战袍，提供强大的毒素与魔法元素抗性。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Armor_of_a_Thousand_Flowers"
            },
            {
                "id": "w3_dol_blathanna_boots",
                "name": {
                    "zh-CN": "多尔·布雷坦纳千花靴子",
                    "en": "Dol Blathanna Boots"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Dol Blathanna Boots')",
                "desc": "百花谷轻便皮靴，无声潜行与翻滚体力消耗减少。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Boots_of_a_Thousand_Flowers"
            },
            {
                "id": "w3_dol_blathanna_gloves",
                "name": {
                    "zh-CN": "多尔·布雷坦纳千花手套",
                    "en": "Dol Blathanna Gloves"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Dol Blathanna Gloves')",
                "desc": "百花谷刺客手套，赋予杰洛特更强劲的弓弩瞄准与挥剑精准度。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Gauntlets_of_a_Thousand_Flowers"
            },
            {
                "id": "w3_dol_blathanna_pants",
                "name": {
                    "zh-CN": "多尔·布雷坦纳千花长裤",
                    "en": "Dol Blathanna Pants"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Dol Blathanna Pants')",
                "desc": "多尔·布雷坦纳战裙下装，兼具高透气性与卓越的抗打击韧度。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Trousers_of_a_Thousand_Flowers"
            },
            {
                "id": "w3_dol_blathanna_steel_sword",
                "name": {
                    "zh-CN": "千花钢剑 (百花之谷上古钢刃)",
                    "en": "Thousand Flowers Steel Sword"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('NGP Dol Blathanna longsword')",
                "desc": "剑柄镶嵌花藤蓝宝石的精灵宝剑，极高概率削弱敌人士气并触发深度割伤。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Sword_of_a_Thousand_Flowers"
            },
            {
                "id": "w3_dol_blathanna_silver_sword",
                "name": {
                    "zh-CN": "白女妖银剑 (百花之谷纯银之锋)",
                    "en": "White Widow Silver Sword"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('NGP White Widow of Dol Blathanna')",
                "desc": "散发淡淡幽光的多尔·布雷坦纳银剑，对幽灵鬼魂生物有高额真实克制伤害。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/White_Widow_of_the_Valley_of_Flowers"
            },
            {
                "id": "w3_netflix_armor_base",
                "name": {
                    "zh-CN": "初阶遗忘狼学派胸甲 (网飞第一季同款)",
                    "en": "Forgotten Wolven Armor (Base)"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Netflix Armor')",
                "desc": "亨利·卡维尔主演《巫师》第一季经典的圆领黑皮猎魔人战甲外观，带有粗犷的铆钉绑带。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Forgotten_Wolven_armor"
            },
            {
                "id": "w3_netflix_steel_base",
                "name": {
                    "zh-CN": "初阶遗忘狼学派钢剑",
                    "en": "Forgotten Wolven Steel Sword (Base)"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Netflix steel sword')",
                "desc": "网飞剧版同款单手阔剑，剑首带有十字形狼头浮雕，兼顾斩击与刺击。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Forgotten_Wolven_steel_sword"
            },
            {
                "id": "w3_netflix_silver_base",
                "name": {
                    "zh-CN": "初阶遗忘狼学派银剑",
                    "en": "Forgotten Wolven Silver Sword (Base)"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Netflix silver sword')",
                "desc": "网飞剧版同款银剑，对恶魔之坑释放的赤红疫病怪物有特殊驱散伤害。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Forgotten_Wolven_silver_sword"
            },
            {
                "id": "w3_netflix_armor_1",
                "name": {
                    "zh-CN": "精制遗忘狼学派胸甲 (网飞进阶版)",
                    "en": "Mastercrafted Forgotten Wolven Armor"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Netflix Armor 1')",
                "desc": "经过陶森特级工匠强化的遗忘狼胸甲，肩部增加硬化钢片衬底与更密集的护心皮甲。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Mastercrafted_legendary_forgotten_Wolven_armor"
            },
            {
                "id": "w3_netflix_steel_1",
                "name": {
                    "zh-CN": "精制遗忘狼学派钢剑",
                    "en": "Mastercrafted Forgotten Wolven Steel Sword"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Netflix steel sword 1')",
                "desc": "精制遗忘狼钢剑：+6% 法印强度、+9% 肾上腺素点获取、+15% 暴击伤害加成、+6% 暴击率、+5% 流血几率、+5% 人形与非人类敌人经验加成。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Forgotten_Wolven_steel_sword_-_mastercrafted"
            },
            {
                "id": "w3_netflix_silver_1",
                "name": {
                    "zh-CN": "精制遗忘狼学派银剑",
                    "en": "Mastercrafted Forgotten Wolven Silver Sword"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Netflix silver sword 1')",
                "desc": "精制遗忘狼银剑：+9% 法印强度、+4% 肾上腺素点获取、+30% 暴击伤害加成、+13% 暴击率、+8% 流血几率、+6% 怪物经验加成。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Legendary_forgotten_Wolven_silver_sword_-_mastercrafted"
            },
            {
                "id": "w3_gwint_card_roach",
                "name": {
                    "zh-CN": "次世代专属联动昆特牌：萝卜 (Roach)",
                    "en": "Gwent Card: Roach (Next-Gen Exclusive)"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('gwint_card_roach')",
                "desc": "次世代版 / 完全版新增的中立昆特牌，战力 3 点，为普通单位卡（非英雄卡），本身没有特殊技能。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Roach_(gwent_card)"
            }
        ]
    },
    {
        "category": "🐺 宗师级狼学派与宗师级遗弃狼套装 (Grandmaster & Forgotten Wolven Sets)",
        "commands": [
            {
                "id": "w3_gm_wolf_silver",
                "name": {
                    "zh-CN": "宗师级狼学派银剑",
                    "en": "Grandmaster Wolven Silver Sword"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Wolf School silver sword 4')",
                "desc": "狼学派最高阶银剑，法印强度与暴击率全方位均衡提升。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/wolf-school-silver-sword-4"
            },
            {
                "id": "w3_gm_wolf_steel",
                "name": {
                    "zh-CN": "宗师级狼学派钢剑",
                    "en": "Grandmaster Wolven Steel Sword"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Wolf School steel sword 4')",
                "desc": "狼学派宗师级钢剑：+11% 法印强度、+11% 肾上腺素点获取、+11% 暴击率、+11% 流血几率、+5% 人形与非人类敌人经验加成。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/wolf-school-steel-sword-4"
            },
            {
                "id": "w3_gm_wolf_armor",
                "name": {
                    "zh-CN": "宗师级狼学派防具胸甲",
                    "en": "Grandmaster Wolven Armor"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Wolf Armor 4')",
                "desc": "宗师级狼学派胸甲。次世代版套装特效：对流血目标造成的长剑伤害提升（按已穿戴套装件数叠加）；穿满 6 件后，肾上腺素点数会提升单个敌人可叠加的流血层数上限。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/wolf-armor-4"
            },
            {
                "id": "w3_gm_wolf_gloves",
                "name": {
                    "zh-CN": "宗师级狼学派手套",
                    "en": "Grandmaster Wolven Gloves"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Wolf Gloves 4')",
                "desc": "宗师级狼学派手甲，提升攻击力与法印强度。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/wolf-gloves-4"
            },
            {
                "id": "w3_gm_wolf_pants",
                "name": {
                    "zh-CN": "宗师级狼学派裤子",
                    "en": "Grandmaster Wolven Pants"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Wolf Pants 4')",
                "desc": "宗师级狼学派下装，提供斩击、穿刺与怪物全方位防御。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/wolf-pants-4"
            },
            {
                "id": "w3_gm_wolf_boots",
                "name": {
                    "zh-CN": "宗师级狼学派靴子",
                    "en": "Grandmaster Wolven Boots"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Wolf Boots 4')",
                "desc": "宗师级狼学派长靴，增强突进抗性与奔跑稳定性。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/wolf-boots-4"
            },
            {
                "id": "w3_netflix_silver_2",
                "name": {
                    "zh-CN": "宗师级遗弃狼银剑 (网飞剧版同款外观)",
                    "en": "Grandmaster Forgotten Wolven Silver Sword"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Netflix silver sword 2')",
                "desc": "宗师级遗弃狼银剑：+10% 法印强度、+7% 肾上腺素点获取、+35% 暴击伤害加成、+15% 暴击率、+10% 流血几率、+10% 怪物经验加成。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Grandmaster_forgotten_Wolven_silver_sword"
            },
            {
                "id": "w3_netflix_steel_2",
                "name": {
                    "zh-CN": "宗师级遗弃狼钢剑",
                    "en": "Grandmaster Forgotten Wolven Steel Sword"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Netflix steel sword 2')",
                "desc": "宗师级遗弃狼钢剑：+7% 法印强度、+10% 肾上腺素点获取、+20% 暴击伤害加成、+7% 暴击率、+5% 流血几率、+10% 人形与非人类敌人经验加成。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Grandmaster_forgotten_Wolven_steel_sword"
            },
            {
                "id": "w3_netflix_armor_2",
                "name": {
                    "zh-CN": "宗师级遗弃狼防具胸甲 (网飞剧版同款外观)",
                    "en": "Grandmaster Forgotten Wolven Armor"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Netflix Armor 2')",
                "desc": "宗师级遗弃狼胸甲：+20% 攻击力、+20% 肾上腺素点获取，以及穿刺、斩击、怪物与元素伤害抗性加成。次世代套装特效：3 件时提升药水持续时间（每件 +7%）；6 件时，受亚登影响的敌人被阿尔德法印击中会额外受到 10% 伤害。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Grandmaster_forgotten_Wolven_armor"
            },
            {
                "id": "w3_netflix_gloves_2",
                "name": {
                    "zh-CN": "宗师级遗弃狼手套",
                    "en": "Grandmaster Forgotten Wolven Gauntlets"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Netflix Gloves 2')",
                "desc": "宗师级遗弃狼护手：+12% 阿尔德法印强度，以及穿刺、斩击、怪物与元素伤害抗性加成。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Grandmaster_forgotten_Wolven_gauntlets"
            },
            {
                "id": "w3_netflix_pants_2",
                "name": {
                    "zh-CN": "宗师级遗弃狼下装",
                    "en": "Grandmaster Forgotten Wolven Trousers"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Netflix Pants 2')",
                "desc": "宗师级遗弃狼战裙：+12% 法印强度，以及斩击、怪物与元素伤害抗性加成。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Grandmaster_forgotten_Wolven_trousers"
            },
            {
                "id": "w3_netflix_boots_2",
                "name": {
                    "zh-CN": "宗师级遗弃狼靴子",
                    "en": "Grandmaster Forgotten Wolven Boots"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Netflix Boots 2')",
                "desc": "宗师级遗弃狼靴子：+12% 亚登法印强度，以及穿刺、钝击、斩击与怪物伤害抗性加成。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Grandmaster_forgotten_Wolven_boots"
            }
        ]
    },
    {
        "category": "🐻 宗师级熊学派全套重甲 (Grandmaster Ursine School Set)",
        "commands": [
            {
                "id": "w3_gm_bear_silver",
                "name": {
                    "zh-CN": "宗师级熊学派银剑",
                    "en": "Grandmaster Ursine Silver Sword"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Bear School silver sword 4')",
                "desc": "拜年剑法核心重剑，肾上腺素生成速度与暴击伤害极高。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/bear-school-silver-sword-4"
            },
            {
                "id": "w3_gm_bear_steel",
                "name": {
                    "zh-CN": "宗师级熊学派钢剑",
                    "en": "Grandmaster Ursine Steel Sword"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Bear School steel sword 4')",
                "desc": "宗师级熊学派钢剑：+22% 肾上腺素点获取、+75% 暴击伤害加成、+5% 暴击率、+14% 肢解几率、+5% 人形与非人类敌人经验加成。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/bear-school-steel-sword-4"
            },
            {
                "id": "w3_gm_bear_armor",
                "name": {
                    "zh-CN": "宗师级熊学派重防具胸甲",
                    "en": "Grandmaster Ursine Armor"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Bear Armor 4')",
                "desc": "宗师级熊学派重甲胸甲：+22% 肾上腺素点获取，以及穿刺、钝击、斩击与怪物伤害抗性加成。套装特效：昆恩护盾破碎时有几率免耗蓝重新生成（每件 +5%，六件时上限 30%）；穿满 6 件后，与昆恩法印相关技能造成的伤害 +200%。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/bear-armor-4"
            },
            {
                "id": "w3_gm_bear_gloves",
                "name": {
                    "zh-CN": "宗师级熊学派手套",
                    "en": "Grandmaster Ursine Gloves"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Bear Gloves 4')",
                "desc": "极具防护力的重甲铁手套，增加暴击伤害与劈砍抗性。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/bear-gloves-4"
            },
            {
                "id": "w3_gm_bear_pants",
                "name": {
                    "zh-CN": "宗师级熊学派裤子",
                    "en": "Grandmaster Ursine Pants"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Bear Pants 4')",
                "desc": "宗师级熊学派裤子：+11% 肾上腺素点获取，以及穿刺、斩击、怪物与元素伤害抗性加成。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/bear-pants-4"
            },
            {
                "id": "w3_gm_bear_boots",
                "name": {
                    "zh-CN": "宗师级熊学派靴子",
                    "en": "Grandmaster Ursine Boots"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Bear Boots 4')",
                "desc": "宗师级熊学派靴子：+11% 肾上腺素点获取，以及穿刺、钝击、斩击与怪物伤害抗性加成。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/bear-boots-4"
            }
        ]
    },
    {
        "category": "🐱 宗师级猫学派轻甲套装 (Grandmaster Feline School Set)",
        "commands": [
            {
                "id": "w3_gm_cat_silver",
                "name": {
                    "zh-CN": "宗师级猫学派银剑",
                    "en": "Grandmaster Feline Silver Sword"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Lynx School silver sword 4')",
                "desc": "宗师级猫学派银剑：+15% 阿尔德法印强度、+10% 暴击率、+15% 流血几率、+10% 肢解几率、+20% 怪物经验加成。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/lynx-school-silver-sword-4"
            },
            {
                "id": "w3_gm_cat_steel",
                "name": {
                    "zh-CN": "宗师级猫学派钢剑",
                    "en": "Grandmaster Feline Steel Sword"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Lynx School steel sword 4')",
                "desc": "宗师级猫学派钢剑：+15% 阿尔德法印强度、+10% 暴击率、+15% 流血几率、+10% 肢解几率、+5% 人形与非人类敌人经验加成。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/lynx-school-steel-sword-4"
            },
            {
                "id": "w3_gm_cat_armor",
                "name": {
                    "zh-CN": "宗师级猫学派轻型防具",
                    "en": "Grandmaster Feline Armor"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Lynx Armor 4')",
                "desc": "宗师级猫学派轻甲（带兜帽的刺客皮甲）：+22% 攻击力，以及穿刺、斩击、怪物与元素伤害抗性加成。套装特效：重击命中后 3 秒内快速攻击伤害提升（按已穿戴件数叠加）；穿满 6 件后，背后攻击伤害 +50% 并有几率眩晕目标（消耗 1 点肾上腺素）。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/lynx-armor-4"
            },
            {
                "id": "w3_gm_cat_gloves",
                "name": {
                    "zh-CN": "宗师级猫学派手套",
                    "en": "Grandmaster Feline Gloves"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Lynx Gloves 4')",
                "desc": "宗师级猫学派手套：+11% 攻击力，以及穿刺、斩击、怪物与元素伤害抗性加成。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/lynx-gloves-4"
            },
            {
                "id": "w3_gm_cat_pants",
                "name": {
                    "zh-CN": "宗师级猫学派裤子",
                    "en": "Grandmaster Feline Pants"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Lynx Pants 4')",
                "desc": "刺客紧身长裤，大幅提升闪避灵活性与暴击几率加成。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/lynx-pants-4"
            },
            {
                "id": "w3_gm_cat_boots",
                "name": {
                    "zh-CN": "宗师级猫学派靴子",
                    "en": "Grandmaster Feline Boots"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Lynx Boots 4')",
                "desc": "轻型潜行靴，奔跑速度极快且降低脚步惊扰范围。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/lynx-boots-4"
            }
        ]
    },
    {
        "category": "🦅 宗师级狮鹫学派法印套装 (Grandmaster Griffin School Set)",
        "commands": [
            {
                "id": "w3_gm_griffin_silver",
                "name": {
                    "zh-CN": "宗师级狮鹫学派银剑",
                    "en": "Grandmaster Griffin Silver Sword"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Gryphon School silver sword 4')",
                "desc": "法印流核心银剑，直接提升全部 5 种猎魔人法印的法术强度。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/gryphon-school-silver-sword-4"
            },
            {
                "id": "w3_gm_griffin_steel",
                "name": {
                    "zh-CN": "宗师级狮鹫学派钢剑",
                    "en": "Grandmaster Griffin Steel Sword"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Gryphon School steel sword 4')",
                "desc": "法印增幅钢剑，加快法印释放后的活力恢复速度。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/gryphon-school-steel-sword-4"
            },
            {
                "id": "w3_gm_griffin_armor",
                "name": {
                    "zh-CN": "宗师级狮鹫学派防具胸甲",
                    "en": "Grandmaster Griffin Armor"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Gryphon Armor 4')",
                "desc": "宗师级狮鹫学派胸甲：+22% 法印强度，以及穿刺、钝击、斩击与怪物伤害抗性加成。套装特效：用耐力施放一次法印后，3 秒内下一个法印施放不消耗耐力；穿满 6 件后亚登陷阱范围 +40%，站在亚登陷阱内时耐力回复与法印强度大幅提升，受到的伤害降低。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/gryphon-armor-4"
            },
            {
                "id": "w3_gm_griffin_gloves",
                "name": {
                    "zh-CN": "宗师级狮鹫学派手套",
                    "en": "Grandmaster Griffin Gloves"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Gryphon Gloves 4')",
                "desc": "宗师级狮鹫学派手套：+11% 法印强度，以及穿刺、斩击、怪物与元素伤害抗性加成。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/gryphon-gloves-4"
            },
            {
                "id": "w3_gm_griffin_pants",
                "name": {
                    "zh-CN": "宗师级狮鹫学派裤子",
                    "en": "Grandmaster Griffin Pants"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Gryphon Pants 4')",
                "desc": "宗师级狮鹫下装，提供卓越的元素抗性与伤害减免。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/gryphon-pants-4"
            },
            {
                "id": "w3_gm_griffin_boots",
                "name": {
                    "zh-CN": "宗师级狮鹫学派靴子",
                    "en": "Grandmaster Griffin Boots"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Gryphon Boots 4')",
                "desc": "宗师级狮鹫长靴，稳定站桩连续法印施法不被打断。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/gryphon-boots-4"
            }
        ]
    },
    {
        "category": "🐍 飞狮怪与毒蛇学派套装 (Manticore & Viper School Sets)",
        "commands": [
            {
                "id": "w3_gm_manticore_silver",
                "name": {
                    "zh-CN": "师匠级飞狮怪银剑",
                    "en": "Manticore Silver Sword"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Red Wolf School silver sword 1')",
                "desc": "陶森特炼金大师银剑，提升暴击伤害与毒性容忍阈值。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Manticore_silver_sword"
            },
            {
                "id": "w3_gm_manticore_steel",
                "name": {
                    "zh-CN": "师匠级飞狮怪钢剑",
                    "en": "Manticore Steel Sword"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Red Wolf School steel sword 1')",
                "desc": "飞狮怪钢剑：+250 护甲穿透、+50% 暴击伤害加成、+5% 暴击率、+10% 流血几率、+5% 人形与非人类敌人经验加成。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Manticore_steel_sword"
            },
            {
                "id": "w3_gm_manticore_armor",
                "name": {
                    "zh-CN": "师匠级飞狮怪防具胸甲",
                    "en": "Manticore Armor"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Red Wolf Armor 1')",
                "desc": "飞狮怪防具胸甲：+5 最大毒性上限，以及穿刺、斩击与怪物伤害抗性加成、+25% 暴击伤害加成。套装特效：暴击率与暴击伤害加成同样作用于炸弹，且炸弹投掷无延迟；穿满 6 件后炼金道具最大携带充能数 +1。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/red-wolf-armor-1"
            },
            {
                "id": "w3_gm_manticore_gloves",
                "name": {
                    "zh-CN": "师匠级飞狮怪手套",
                    "en": "Manticore Gloves"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Red Wolf Gloves 1')",
                "desc": "增加药水毒性抗性与暴击几率加成。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/red-wolf-gloves-1"
            },
            {
                "id": "w3_gm_manticore_pants",
                "name": {
                    "zh-CN": "师匠级飞狮怪裤子",
                    "en": "Manticore Pants"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Red Wolf Pants 1')",
                "desc": "提升炼金炸弹携带数量与毒素伤害抵抗。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/red-wolf-pants-1"
            },
            {
                "id": "w3_gm_manticore_boots",
                "name": {
                    "zh-CN": "师匠级飞狮怪靴子",
                    "en": "Manticore Boots"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Red Wolf Boots 1')",
                "desc": "提供高额毒抗与穿刺劈砍抗性。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/red-wolf-boots-1"
            },
            {
                "id": "w3_viper_silver",
                "name": {
                    "zh-CN": "毒蛇剧毒银剑",
                    "en": "Viper Venomous Silver Sword"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('EP1 Viper School silver sword')",
                "desc": "毒蛇学派银剑：+25% 阿尔德法印强度、+75% 暴击伤害加成、+10% 暴击率、15% 中毒几率、+20% 怪物经验加成。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/ep1-viper-school-silver-sword"
            },
            {
                "id": "w3_viper_steel",
                "name": {
                    "zh-CN": "毒蛇剧毒钢剑",
                    "en": "Viper Venomous Steel Sword"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('EP1 Viper School steel sword')",
                "desc": "毒蛇学派钢剑：+25% 阿尔德法印强度、+75% 暴击伤害加成、+10% 暴击率、15% 中毒几率、+5% 人形与非人类敌人经验加成。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/ep1-viper-school-steel-sword"
            },
            {
                "id": "w3_viper_armor",
                "name": {
                    "zh-CN": "毒蛇学派护甲 (开场 CG 同款黑皮甲)",
                    "en": "Viper Armor"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('EP1 Witcher Armor')",
                "desc": "与白果园开场动画同款的黑色鳞甲：+50% 中毒抗性，以及穿刺、斩击、怪物与元素伤害抗性加成。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Legendary_Viper_armor"
            },
            {
                "id": "w3_viper_gloves",
                "name": {
                    "zh-CN": "毒蛇学派手套",
                    "en": "Viper Gloves"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('EP1 Witcher Gloves')",
                "desc": "毒蛇战甲皮手套，提升物理攻击与流血中毒施加几率。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Viper_gauntlets"
            },
            {
                "id": "w3_viper_pants",
                "name": {
                    "zh-CN": "毒蛇学派裤子",
                    "en": "Viper Pants"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('EP1 Witcher Pants')",
                "desc": "毒蛇鳞纹战术裤，提供极高的钝击与元素防御。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Viper_trousers"
            },
            {
                "id": "w3_viper_boots",
                "name": {
                    "zh-CN": "毒蛇学派靴子",
                    "en": "Viper Boots"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('EP1 Witcher Boots')",
                "desc": "毒蛇防水战靴，提升移动稳定性与毒素抗性。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Viper_boots"
            }
        ]
    },
    {
        "category": "🗡️ 传奇武器与资料片专属装备 (Legendary Relics & Iconic Blades)",
        "commands": [
            {
                "id": "w3_aerondight",
                "name": {
                    "zh-CN": "湖中之剑 (血与酒成长型银剑)",
                    "en": "Aerondight (Endless Growth)"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Aerondight EP2')",
                "desc": "每次命中为该剑叠加一层能量（最多 10 层），每层增伤 10%；满层时攻击必定暴击，若在满层状态下击杀敌人，会永久提升该剑的基础伤害（上限随角色等级提高）。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Aerondight"
            },
            {
                "id": "w3_iris_olgierd_sabre",
                "name": {
                    "zh-CN": "爱丽丝 (欧吉尔德的血弯刀)",
                    "en": "Iris (Olgierd Sabre)"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Olgierd Sabre')",
                "desc": "战斗中会随攻击积蓄能量，剑身变红后使用重击可打出一次威力更强的攻击，但会消耗杰洛特自身部分生命值。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/olgierd-sabre"
            },
            {
                "id": "w3_caretaker_shovel",
                "name": {
                    "zh-CN": "看门人的铲子",
                    "en": "Caretaker Shovel"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Caretaker Shovel')",
                "desc": "欧吉尔德庄园中的铲子，攻击造成的伤害有 10% 转化为生命值回复给杰洛特。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/caretaker-shovel"
            },
            {
                "id": "w3_winters_blade",
                "name": {
                    "zh-CN": "冬之刃 (克拉奇家传剑)",
                    "en": "Winter's Blade"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('q402 Skellige sword 3')",
                "desc": "史凯利格克拉奇家族传剑：+40 护甲穿透、+55% 暴击伤害加成、+10% 冻结几率；次世代版本下伤害会随角色等级自动调整。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Winter%27s_Blade"
            },
            {
                "id": "w3_fate_sword",
                "name": {
                    "zh-CN": "命运 (经典遗物银剑)",
                    "en": "Fate Silver Sword"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Fate')",
                "desc": "拥有 3 个符文镶嵌孔的银剑：+2%～10% 伊格尼法印强度、+2%～10% 亚克西法印强度（两者数值相同、随机生成）、+10% 击晕几率。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/fate"
            },
            {
                "id": "w3_toussaint_steel_3",
                "name": {
                    "zh-CN": "陶森特骑士钢剑",
                    "en": "Toussaint Knight's Steel Sword"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Toussaint steel sword 3')",
                "desc": "陶森特骑士钢剑：+300 护甲穿透、+30% 昆恩法印强度、+100% 暴击伤害加成、+20% 暴击率、+15% 点燃几率。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/toussaint-steel-sword-3"
            },
            {
                "id": "w3_vampire_mask_q704",
                "name": {
                    "zh-CN": "亨盖得吸血鬼面具",
                    "en": "Hen Gaidth Vampire Mask"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('q704_vampire_mask')",
                "desc": "暗影长者之穴中找到的吸血鬼面具；与亨盖得全套装备搭配时，击杀敌人可回复生命值，回复量为已穿戴套装件数 × 最大生命值的 1%。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/q704-vampire-mask"
            },
            {
                "id": "w3_vampire_armor_q704",
                "name": {
                    "zh-CN": "亨盖得吸血鬼全身血甲",
                    "en": "Hen Gaidth Vampire Armor"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('q704_vampire_armor')",
                "desc": "赤红色的高阶吸血鬼铠甲，提供极高劈砍与穿刺防御，穿戴套装击败敌人可不断回复生命。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/q704-vampire-armor"
            },
            {
                "id": "w3_vampire_steel_sword_q704",
                "name": {
                    "zh-CN": "亨盖得吸血鬼钢剑",
                    "en": "Hen Gaidth Steel Sword"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('q704 vampire steel sword')",
                "desc": "亨盖得套装钢剑：+150 护甲穿透、+75% 暴击伤害加成、+15% 暴击率、+15% 流血几率、+15% 眩晕几率。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/q704-vampire-steel-sword"
            },
            {
                "id": "w3_tesham_mutna_armor",
                "name": {
                    "zh-CN": "特斯汉穆那吸血鬼黑甲 (黑金铠甲)",
                    "en": "Tesham Mutna Armor"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('q702_vampire_armor')",
                "desc": "血与酒特斯汉穆那废墟古老吸血鬼套装，纯黑金属重装，击杀敌人吸收生命活力。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Tesham_Mutna_armor"
            },
            {
                "id": "w3_tesham_mutna_mask",
                "name": {
                    "zh-CN": "特斯汉穆那吸血鬼面具",
                    "en": "Tesham Mutna Mask"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('q702_vampire_mask')",
                "desc": "特斯汉穆那遗迹假面，搭配特斯汉穆那全套防具激活吸血鬼套装击杀吸血特效。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Tesham_Mutna_mask"
            }
        ]
    },
    {
        "category": "🧪 高等魔药与炼金药 (Superior Potions & Decoctions)",
        "commands": [
            {
                "id": "w3_potion_swallow_sup",
                "name": {
                    "zh-CN": "高等燕子魔药",
                    "en": "Superior Swallow"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Swallow 3')",
                "desc": "加速生命值回复，且受到伤害不会打断回复效果；战斗中同样持续回血。",
                "framework_required": "None (Native Console)",
                "source": "https://segmentnext.com/witcher-3-item-codes"
            },
            {
                "id": "w3_potion_thunderbolt_sup",
                "name": {
                    "zh-CN": "高等雷霆魔药",
                    "en": "Superior Thunderbolt"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Thunderbolt 3')",
                "desc": "延长药效持续时间，并提升攻击力（约 +35%）；暴风雨天气下攻击必定暴击。",
                "framework_required": "None (Native Console)",
                "source": "https://segmentnext.com/witcher-3-item-codes"
            },
            {
                "id": "w3_potion_white_honey_sup",
                "name": {
                    "zh-CN": "高等白蜂蜜 (瞬间清空全部毒性与异常)",
                    "en": "Superior White Honey"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('White Honey 3')",
                "desc": "立刻清除当前体内累积的所有药水毒性与负面状态，重置药效。",
                "framework_required": "None (Native Console)",
                "source": "https://segmentnext.com/witcher-3-item-codes"
            },
            {
                "id": "w3_potion_tawny_owl_sup",
                "name": {
                    "zh-CN": "高等黄褐色猫头鹰",
                    "en": "Superior Tawny Owl"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Tawny Owl 3')",
                "desc": "加速活力（耐力）回复速度并延长药效持续时间；夜晚期间药效不会过期。",
                "framework_required": "None (Native Console)",
                "source": "https://segmentnext.com/witcher-3-item-codes"
            },
            {
                "id": "w3_dec_ekhidna",
                "name": {
                    "zh-CN": "海克娜煎药",
                    "en": "Ekhidna Decoction"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Mutagen 21')",
                "desc": "做出消耗活力的动作（如施放法印、翻滚）时回复一定生命值。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Ekhidna_decoction"
            },
            {
                "id": "w3_dec_ekimmara",
                "name": {
                    "zh-CN": "艾基马拉煎药",
                    "en": "Ekimmara Decoction"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Mutagen 7')",
                "desc": "原条目名称与代码张冠李戴(把艾基马拉 Ekimmara 与海克娜 Ekhidna 的名字/代码对调了)，现已按效果对应修正：造成伤害的一部分转化为生命值回复。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Ekimmara_decoction"
            },
            {
                "id": "w3_dec_troll",
                "name": {
                    "zh-CN": "巨魔煎药 (战斗内外持续回血)",
                    "en": "Troll Decoction"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Mutagen 12')",
                "desc": "战斗内外持续回复生命值；次世代版本下，战斗中每击杀一名敌人额外回复 20 点生命，药效持续 30 分钟。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Troll_decoction"
            },
            {
                "id": "w3_dec_katakan",
                "name": {
                    "zh-CN": "卡塔卡恩煎药 (常驻暴击率提升)",
                    "en": "Katakan Decoction"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Mutagen 1')",
                "desc": "次世代版本下恒定提升 10% 暴击几率（此前版本为 5%）。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Katakan_decoction"
            },
            {
                "id": "w3_dec_succubus",
                "name": {
                    "zh-CN": "女夜魔煎药 (战斗时间越长攻击力越猛)",
                    "en": "Succubus Decoction"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Mutagen 14')",
                "desc": "战斗中攻击力随时间持续递增，直至达到最高峰值。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Succubus_decoction"
            },
            {
                "id": "w3_dec_griffin",
                "name": {
                    "zh-CN": "大狮鹫煎药",
                    "en": "Archgriffin Decoction"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Mutagen 4')",
                "desc": "若还有剩余活力，重击会消耗全部活力，并在造成普通伤害后额外扣除目标最大生命值 5% 的生命值。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Archgriffin_decoction"
            }
        ]
    },
    {
        "category": "💣 高级剑油、炸弹与特级符文石 (Superior Oils, Bombs & Greater Runes)",
        "commands": [
            {
                "id": "w3_oil_specter_sup",
                "name": {
                    "zh-CN": "高等残灵生物油 (克制妖灵类)",
                    "en": "Superior Specter Oil"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Specter Oil 3')",
                "desc": "对妖灵等灵体类怪物（Specter）造成的攻击力提升 50%。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/specter-oil-3"
            },
            {
                "id": "w3_oil_necrophage_sup",
                "name": {
                    "zh-CN": "高等食尸生物油 (克制水鬼/食尸鬼类)",
                    "en": "Superior Necrophage Oil"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Necrophage Oil 3')",
                "desc": "对食尸生物（如水鬼、食尸鬼、孽鬼等 Necrophage）造成的攻击力提升 50%。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/necrophage-oil-3"
            },
            {
                "id": "w3_oil_vampire_sup",
                "name": {
                    "zh-CN": "高等吸血鬼油 (克制吸血鬼类)",
                    "en": "Superior Vampire Oil"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Vampire Oil 3')",
                "desc": "对吸血鬼类怪物（如卡塔卡恩、蝠翼魔、吸血女妖等 Vampire）造成的攻击力提升 50%。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/vampire-oil-3"
            },
            {
                "id": "w3_oil_cursed_sup",
                "name": {
                    "zh-CN": "高等诅咒生物油 (克制狼人/尸婴类)",
                    "en": "Superior Cursed Oil"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Cursed Oil 3')",
                "desc": "对诅咒类生物（如狼人、尸婴等 Cursed One）造成的攻击力提升 50%。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/cursed-oil-3"
            },
            {
                "id": "w3_oil_relict_sup",
                "name": {
                    "zh-CN": "高等类魔油 (克制鹿首精/林中夫人类)",
                    "en": "Superior Relict Oil"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Relic Oil 3')",
                "desc": "对远古魔法类生物（Relict，如鹿首精、林中夫人等）造成的攻击力提升 50%。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/relic-oil-3"
            },
            {
                "id": "w3_bomb_grapeshot_sup",
                "name": {
                    "zh-CN": "高等蜂窝炸弹",
                    "en": "Superior Grapeshot"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Grapeshot 3', 10)",
                "desc": "对爆炸范围内的敌人造成破片与火焰伤害，伤害无视护甲，可摧毁怪物巢穴。",
                "framework_required": "None (Native Console)",
                "source": "https://segmentnext.com/witcher-3-item-codes"
            },
            {
                "id": "w3_bomb_dancing_star_sup",
                "name": {
                    "zh-CN": "高等舞动之星炸弹 (大范围烈焰燃烧地毯)",
                    "en": "Superior Dancing Star"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Dancing Star 3', 10)",
                "desc": "制造大面积持续燃烧火海，点燃敌人并使其陷入长时间抱头惨叫瘫痪。",
                "framework_required": "None (Native Console)",
                "source": "https://segmentnext.com/witcher-3-item-codes"
            },
            {
                "id": "w3_bomb_northern_wind_sup",
                "name": {
                    "zh-CN": "高等北风炸弹",
                    "en": "Superior Northern Wind"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('White Frost 3', 10)",
                "desc": "使爆炸范围内的敌人陷入冰冻（持续约 10 秒），命中冻结目标会造成额外伤害，并有几率直接即死。",
                "framework_required": "None (Native Console)",
                "source": "https://segmentnext.com/witcher-3-item-codes"
            },
            {
                "id": "w3_bomb_dimeritium_sup",
                "name": {
                    "zh-CN": "高等阻魔金炸弹",
                    "en": "Superior Dimeritium Bomb"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Dwimeritium Bomb 3', 10)",
                "desc": "释放阻魔金粉尘，短时间内阻断范围内怪物使用魔法类能力，云雾消散后效果还会再持续一段时间，总持续约 30 秒。",
                "framework_required": "None (Native Console)",
                "source": "https://segmentnext.com/witcher-3-item-codes"
            },
            {
                "id": "w3_rune_chernobog_sup",
                "name": {
                    "zh-CN": "特级元素符文石 x10",
                    "en": "Greater Elemental Rune x10"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Rune elemental greater', 10)",
                "desc": "附魔武器符文，三孔全部镶嵌可提升近战武器的元素伤害加成（具体数值未在可核实来源中给出，原描述的「切尔诺伯格」为该符文的传说别名而非内部代码/固定加成数字）。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Greater_Chernobog_runestone"
            },
            {
                "id": "w3_glyph_quen_sup",
                "name": {
                    "zh-CN": "特级昆恩字印 x10 (+10% 昆恩护盾强度)",
                    "en": "Greater Glyph of Quen x10"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Glyph quen greater', 10)",
                "desc": "镶嵌在护甲符文卡槽中的字印，提供 +10% 昆恩法印强度；装备在多件护甲上时效果可叠加。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/glyph-quen-greater"
            }
        ]
    },
    {
        "category": "🃏 昆特牌牌组与对局指令 (Gwent Decks & Match Commands)",
        "commands": [
            {
                "id": "w3_secretgwint",
                "name": {
                    "zh-CN": "开始一局昆特牌对局 (对战AI)",
                    "en": "Start a Gwent Match"
                },
                "syntax_type": "redengine_cmd",
                "code": "secretgwint",
                "desc": "立即开始一局与AI对战的昆特牌比赛；并不会直接把全部卡牌加入牌库（集卡需用 addgwintcards 或逐张 additem）。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/secretgwint"
            },
            {
                "id": "w3_wingwint",
                "name": {
                    "zh-CN": "直接判定当前昆特牌对局获胜",
                    "en": "Instant Win Current Gwent Match"
                },
                "syntax_type": "redengine_cmd",
                "code": "winGwint(true)",
                "desc": "在对局进行中的任意时刻输入，直接判定当前昆特牌对局获胜（对方直接认输结算）。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/wingwint"
            },
            {
                "id": "w3_addgwintcards",
                "name": {
                    "zh-CN": "注入全套基础昆特牌组",
                    "en": "Add Basic Gwent Cards"
                },
                "syntax_type": "redengine_cmd",
                "code": "addgwintcards",
                "desc": "将游戏开局缺失的基础势力作战单位牌各补充一份入库。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/addgwintcards"
            },
            {
                "id": "w3_card_geralt",
                "name": {
                    "zh-CN": "利维亚的杰洛特 (15点中立近战英雄金卡)",
                    "en": "Gwent Card: Geralt of Rivia (15 Pts)"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('gwint_card_geralt')",
                "desc": "中立近战英雄卡，战力 15 点；作为英雄牌免疫特殊卡牌效果，登场时会额外从牌库中找出并打出萝卜卡。",
                "framework_required": "None (Native Console)",
                "source": "https://segmentnext.com/witcher-3-item-codes"
            },
            {
                "id": "w3_card_ciri",
                "name": {
                    "zh-CN": "希里 (15点中立近战英雄金卡)",
                    "en": "Gwent Card: Ciri (15 Pts)"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('gwint_card_ciri')",
                "desc": "中立近战英雄卡，战力 15 点；作为英雄牌免疫特殊卡牌效果，登场时会额外从牌库中找出并打出萝卜卡。",
                "framework_required": "None (Native Console)",
                "source": "https://segmentnext.com/witcher-3-item-codes"
            },
            {
                "id": "w3_card_yennefer",
                "name": {
                    "zh-CN": "叶奈法 (7点医生复活英雄金卡)",
                    "en": "Gwent Card: Yennefer of Vengerberg"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('gwint_card_yennefer')",
                "desc": "中立远程英雄卡，战力 7 点；登场时可从己方墓地选择一张普通单位卡（不含英雄与特殊卡）直接复活打出。",
                "framework_required": "None (Native Console)",
                "source": "https://segmentnext.com/witcher-3-item-codes"
            },
            {
                "id": "w3_card_mysterious_elf",
                "name": {
                    "zh-CN": "神秘精灵阿瓦拉克 (0点间谍金卡)",
                    "en": "Gwent Card: Avallac'h (0 Pt Spy)"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('gwint_card_avallach')",
                "desc": "0 点点数的间谍卡：登场后置于对方场上（计入对方总分），同时可从自己牌库抽 2 张牌；作为英雄牌免疫特殊卡牌效果。",
                "framework_required": "None (Native Console)",
                "source": "https://segmentnext.com/witcher-3-item-codes"
            },
            {
                "id": "w3_card_roach",
                "name": {
                    "zh-CN": "萝卜 (次世代新版中立牌)",
                    "en": "Gwent Card: Roach (Next-Gen)"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('gwint_card_roach')",
                "desc": "次世代版 / 完全版新增的中立昆特牌，战力 3 点，为普通单位卡（非英雄卡），本身没有特殊技能。",
                "framework_required": "None (Native Console)",
                "source": "https://witcher.fandom.com/wiki/Roach_(gwent_card)"
            }
        ]
    },
    {
        "category": "🗺️ 全大陆路标瞬移、迷雾全开与城市传送 (World Exploration & Fast Travel)",
        "commands": [
            {
                "id": "w3_showallft",
                "name": {
                    "zh-CN": "解锁全部快速旅行路标",
                    "en": "Show All Fast Travel Signposts"
                },
                "syntax_type": "redengine_cmd",
                "code": "ShowAllFT(1)",
                "desc": "解锁大地图上白果园、威伦、诺维格瑞、史凯利格与陶森特的全部快速旅行路标。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/showallft"
            },
            {
                "id": "w3_allowft",
                "name": {
                    "zh-CN": "允许在地图任意位置快速旅行",
                    "en": "Allow Fast Travel Anywhere"
                },
                "syntax_type": "redengine_cmd",
                "code": "AllowFT(1)",
                "desc": "允许在地图上任意已探索位置直接打开地图进行快速旅行，无需先跑到路标旁。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/allowft"
            },
            {
                "id": "w3_showpins",
                "name": {
                    "zh-CN": "点亮全大陆所有未探索的 '?' 问号标记",
                    "en": "Show All Question Mark Pins"
                },
                "syntax_type": "redengine_cmd",
                "code": "ShowPins(1)",
                "desc": "强迫症玩家清图福音，将大地图上所有隐藏的问号宝藏与魔力之所全息标注。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/showpins"
            },
            {
                "id": "w3_showknownpins",
                "name": {
                    "zh-CN": "显示所有已知地标图标",
                    "en": "Show All Known Pins"
                },
                "syntax_type": "redengine_cmd",
                "code": "ShowKnownPins(1)",
                "desc": "将地图上已知商贩、铁匠与理发师图标常驻显示。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/showknownpins"
            },
            {
                "id": "w3_goto_novigrad",
                "name": {
                    "zh-CN": "瞬间传送到诺维格瑞自由城 (Novigrad)",
                    "en": "Fast Travel to Novigrad"
                },
                "syntax_type": "redengine_cmd",
                "code": "gotoNovigrad",
                "desc": "立即跨地图传送到北方最大繁华都市诺维格瑞教皇广场中心。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/gotonovigrad"
            },
            {
                "id": "w3_goto_skellige",
                "name": {
                    "zh-CN": "瞬间传送到史凯利格群岛 (Skellige)",
                    "en": "Fast Travel to Skellige"
                },
                "syntax_type": "redengine_cmd",
                "code": "gotoSkellige",
                "desc": "免去乘船海难剧情，直接传送至史凯利格大史凯利格岛主城堡大门前。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/gotoskellige"
            },
            {
                "id": "w3_goto_kaermorhen",
                "name": {
                    "zh-CN": "瞬间传送到狼学派老巢凯尔莫罕 (Kaer Morhen)",
                    "en": "Fast Travel to Kaer Morhen"
                },
                "syntax_type": "redengine_cmd",
                "code": "gotoKaerMohren",
                "desc": "瞬间回到巍峨的群山堡垒凯尔莫罕主庭院。",
                "framework_required": "None (Native Console)",
                "source": "https://web.archive.org/web/20260518032436/https://primagames.com/tips/witcher-3-next-gen-console-commands-full-list-of-cheats"
            },
            {
                "id": "w3_goto_prolog",
                "name": {
                    "zh-CN": "瞬间传送回新手村白果园 (White Orchard)",
                    "en": "Fast Travel to White Orchard"
                },
                "syntax_type": "redengine_cmd",
                "code": "gotoProlog",
                "desc": "快速传送回新手村白果园酒馆旅店前，补齐错过的早期支线。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/gotoprolog"
            },
            {
                "id": "w3_goto_wyzima",
                "name": {
                    "zh-CN": "瞬间传送到维吉玛皇家城堡 (Wyzima)",
                    "en": "Fast Travel to Wyzima Palace"
                },
                "syntax_type": "redengine_cmd",
                "code": "gotoWyzima",
                "desc": "传送到泰莫利亚皇宫城堡，与尼弗迦德大帝恩希尔当面对质。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/gotowyzima"
            }
        ]
    },
    {
        "category": "⏱️ 昼夜时间流速、天气调控与坐骑马匹掌控 (Time, Weather & Roach Horse Tuning)",
        "commands": [
            {
                "id": "w3_settime_12",
                "name": {
                    "zh-CN": "将游戏内时间设为正午 12:00",
                    "en": "Set Time to Noon (12:00)"
                },
                "syntax_type": "redengine_cmd",
                "code": "settime(1, 12, 0, 0)",
                "desc": "将游戏内时间设置为正午 12 点。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/settime"
            },
            {
                "id": "w3_settime_0",
                "name": {
                    "zh-CN": "将世界时间跳转至午夜 00:00 (狂猎降临时刻)",
                    "en": "Set Time to Midnight (00:00)"
                },
                "syntax_type": "redengine_cmd",
                "code": "settime(1, 0, 0, 0)",
                "desc": "定格午夜，让日间女妖转化为夜间妖灵，营造极佳的魔幻恐怖氛围。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/settime"
            },
            {
                "id": "w3_makeitrain",
                "name": {
                    "zh-CN": "召唤降雨天气",
                    "en": "Make It Rain"
                },
                "syntax_type": "redengine_cmd",
                "code": "makeitrain",
                "desc": "将当前天气切换为下雨。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/makeitrain"
            },
            {
                "id": "w3_stoprain",
                "name": {
                    "zh-CN": "停止降雨",
                    "en": "Stop Rain"
                },
                "syntax_type": "redengine_cmd",
                "code": "stoprain",
                "desc": "停止当前的降雨天气。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/stoprain"
            },
            {
                "id": "w3_weather_storm",
                "name": {
                    "zh-CN": "切换为暴风雨天气",
                    "en": "Set Storm Weather"
                },
                "syntax_type": "redengine_cmd",
                "code": "changeweather('WT_Rain_Storm')",
                "desc": "将天气切换为暴风雨。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/weather"
            },
            {
                "id": "w3_weather_clear",
                "name": {
                    "zh-CN": "切换为晴朗天气",
                    "en": "Set Clear Weather"
                },
                "syntax_type": "redengine_cmd",
                "code": "changeweather('WT_Clear')",
                "desc": "将天气切换为晴朗无云。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/weather"
            },
            {
                "id": "w3_horse_saddle_4",
                "name": {
                    "zh-CN": "鲍克兰骑兵马鞍 (提升马匹体力上限)",
                    "en": "Beauclair Cavalry Saddle (Max Stamina)"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Horse Saddle 4')",
                "desc": "为萝卜装备陶森特骑兵马鞍，提升其体力（耐力）上限。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/items/horse-saddle-4"
            },
            {
                "id": "w3_horse_blinders_3",
                "name": {
                    "zh-CN": "鲍克兰马盲目镜 (+60 惊慌度上限)",
                    "en": "Beauclair Blinders (Anti-Panic)"
                },
                "syntax_type": "redengine_cmd",
                "code": "additem('Horse Blinder 3')",
                "desc": "为萝卜装备陶森特马用眼罩，使其惊慌度上限 +60，更不容易因怪物惊吓而将杰洛特甩下马。",
                "framework_required": "None (Native Console)",
                "source": "https://segmentnext.com/witcher-3-item-codes"
            }
        ]
    },
    {
        "category": "🎭 角色外观造型、希里切换与视觉特写 (Appearance, Ciri Switch & Visual FX)",
        "commands": [
            {
                "id": "w3_ciri_switch",
                "name": {
                    "zh-CN": "切换操控角色为希里",
                    "en": "Switch Player to Ciri"
                },
                "syntax_type": "redengine_cmd",
                "code": "Ciri",
                "desc": "将当前操控角色切换为希里，可使用她的瞬移突进能力。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/ciri"
            },
            {
                "id": "w3_geralt_switch",
                "name": {
                    "zh-CN": "恢复操控利维亚的杰洛特 (Geralt)",
                    "en": "Switch Back to Geralt"
                },
                "syntax_type": "redengine_cmd",
                "code": "Geralt",
                "desc": "从希里或其他状态平滑切回利维亚的杰洛特主角视角，恢复全部猎魔人法印与背包物品栏系统。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/geralt"
            },
            {
                "id": "w3_shave",
                "name": {
                    "zh-CN": "剃除杰洛特胡须",
                    "en": "Shave Geralt Beard"
                },
                "syntax_type": "redengine_cmd",
                "code": "shave",
                "desc": "立即剃除杰洛特的胡须。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/shave"
            },
            {
                "id": "w3_setbeard_1",
                "name": {
                    "zh-CN": "瞬间长出威严茂密的络腮胡",
                    "en": "Set Full Bushy Beard"
                },
                "syntax_type": "redengine_cmd",
                "code": "setbeard(1)",
                "desc": "将杰洛特的胡须状态瞬间锁定为生长完全的沧桑大络腮胡须。",
                "framework_required": "None (Native Console)",
                "source": "https://web.archive.org/web/20260518032436/https://primagames.com/tips/witcher-3-next-gen-console-commands-full-list-of-cheats"
            },
            {
                "id": "w3_dismember",
                "name": {
                    "zh-CN": "开启击杀必定触发断肢效果",
                    "en": "Always Dismember on Kill"
                },
                "syntax_type": "redengine_cmd",
                "code": "dismember",
                "desc": "开启后，终结敌人的最后一击会触发慢动作断肢效果。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/dismember"
            },
            {
                "id": "w3_cat_1",
                "name": {
                    "zh-CN": "开启猫之视野夜视夜瞳 (地牢无需火把亮如白昼)",
                    "en": "Enable Cat Night Vision"
                },
                "syntax_type": "redengine_cmd",
                "code": "Cat(1)",
                "desc": "直接开启黑白高对比度夜视热感视野，深入古墓洞穴无需右手举火把即可看清每一个角落。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/cat"
            },
            {
                "id": "w3_cat_0",
                "name": {
                    "zh-CN": "关闭猫之视野夜视",
                    "en": "Disable Cat Night Vision"
                },
                "syntax_type": "redengine_cmd",
                "code": "Cat(0)",
                "desc": "关闭夜视视野，恢复自然光影色彩呈现。",
                "framework_required": "None (Native Console)",
                "source": "https://commands.gg/witcher3/cat"
            },
            {
                "id": "w3_drunk_1",
                "name": {
                    "zh-CN": "开启醉酒晃动与重影模糊视觉特效",
                    "en": "Enable Drunk FX"
                },
                "syntax_type": "redengine_cmd",
                "code": "drunk(1)",
                "desc": "模拟杰洛特在酒馆痛饮伏特加后的醉态，视线产生晃动拉伸镜头特效。",
                "framework_required": "None (Native Console)",
                "source": "https://web.archive.org/web/20260518032436/https://primagames.com/tips/witcher-3-next-gen-console-commands-full-list-of-cheats"
            },
            {
                "id": "w3_drunk_0",
                "name": {
                    "zh-CN": "解除醉酒状态并恢复正常视觉",
                    "en": "Disable Drunk FX"
                },
                "syntax_type": "redengine_cmd",
                "code": "drunk(0)",
                "desc": "瞬间醒酒，消除一切头晕晃动滤镜。",
                "framework_required": "None (Native Console)",
                "source": "https://web.archive.org/web/20260518032436/https://primagames.com/tips/witcher-3-next-gen-console-commands-full-list-of-cheats"
            },

        ]
    }
]

witcher_popular = [
    {
        "name": {"zh-CN": "上帝模式 (God Mode)", "en": "God Mode"},
        "command": "god",
        "desc": "开启后杰洛特免疫伤害，生命值与昆恩法印锁定，不会受到物理与法术伤害。",
        "source": "https://commands.gg/witcher3/god"
    },
    {
        "name": {"zh-CN": "增加金币 (100,000 克朗)", "en": "Add 100,000 Crowns"},
        "command": "addmoney(100000)",
        "desc": "增加 100,000 克朗，可用于购买宗师级装备材料或陶森特庄园升级等花费较高的内容。",
        "source": "https://commands.gg/witcher3/addmoney"
    },
    {
        "name": {"zh-CN": "开始一局昆特牌对局", "en": "Add All Gwent Cards"},
        "command": "secretgwint",
        "desc": "立即开始一局与 AI 对战的昆特牌比赛；不会直接把全部卡牌加入牌库。",
        "source": "https://commands.gg/witcher3/secretgwint"
    },
    {
        "name": {"zh-CN": "直接获得湖中之剑 (血与酒成长型银剑)", "en": "Add Aerondight Sword"},
        "command": "additem('Aerondight EP2')",
        "desc": "获得会随战斗表现持续强化基础伤害的银剑（Aerondight）。",
        "source": "https://witcher.fandom.com/wiki/Aerondight"
    },
    {
        "name": {"zh-CN": "大地图点亮全部快速旅行路标", "en": "Show All Fast Travel"},
        "command": "ShowAllFT(1)",
        "desc": "瞬间解锁白果园、威伦、诺维格瑞、群岛与陶森特的全部快速旅行路标。",
        "source": "https://commands.gg/witcher3/showallft"
    },
    {
        "name": {"zh-CN": "获取大超同款宗师级遗忘狼防具 (次世代版 / 完全版特供)", "en": "Add Netflix Wolven Armor"},
        "command": "additem('Netflix Armor 2')",
        "desc": "直接注入亨利·卡维尔网飞剧版同款纯黑宗师级遗弃狼战甲。",
        "source": "https://witcher.fandom.com/wiki/Grandmaster_forgotten_Wolven_armor"
    }
]

witcher_mods = [
    {
        "id": "hd-reworked-project-nextgen",
        "title": "The Witcher 3 HD Reworked Project NextGen Edition",
        "author": "Halk Hogan PL",
        "category": "画面材质 (Visuals / Textures)",
        "desc": "次世代版 / 完全版的材质重制 Mod，重绘岩石、植被、砖墙、木纹等大量场景材质，面向次世代 DX12 版本。",
        "dependencies": [
            "None"
        ],
        "installPath": "The Witcher 3\\Mods\\",
        "installSteps": [
            "1. 确认游戏已升级至次世代版本 (v4.04+)；",
            "2. 下载后直接运行安装程序，指定《巫师3》安装根目录；",
            "3. 进入游戏视频选项，将材质品质调至最高 'HDReworked' 即可生效。"
        ],
        "isDirect": False,
        "nexusUrl": "https://www.nexusmods.com/witcher3/mods/9963",
        "version": "20.0-fixed",
        "downloads": "749.2K",
        "endorsements": "8.1K",
        "checkedAt": "2026-11-20"
    },
    {
        "id": "witcher-3-script-merger",
        "title": "Script Merger (CLASSIC)",
        "author": "AnotherSymbiote",
        "category": "核心排错工具 (Utility / Conflict Resolver)",
        "desc": "用于检测并合并多个 Mod 之间的 WitcherScript 冲突代码，解决因脚本冲突导致的 Script Compilation Error 报错。",
        "dependencies": [
            "None"
        ],
        "installPath": "任意独立文件夹 (如 D:\\Tools\\ScriptMerger)",
        "installSteps": [
            "1. 解压后运行 ScriptMerger.exe，在设置中指定《巫师3》安装根目录；",
            "2. 点击 'Refresh' 扫描，勾选检测到的有冲突的脚本点击 'Create Merged Script' 即可。"
        ],
        "isDirect": False,
        "nexusUrl": "https://www.nexusmods.com/witcher3/mods/484",
        "version": "0.6.4",
        "downloads": "3.1M",
        "endorsements": "105.6K",
        "checkedAt": "2026-11-20"
    },
    {
        "id": "brothers-in-arms-nextgen",
        "title": "Brothers in Arms - TW3 Bug Fix and Restored Content Collection - Next-Gen",
        "author": "PaulR0013 - MerseyRockoff - konyme",
        "category": "剧情与修复 (Gameplay / Bug Fixes / Cut Content)",
        "desc": "修复《巫师3》本体与两个资料片中的多个遗留 Bug、未使用的 NPC 对话、被截断的过场动画片段与部分任务物品缺失问题。",
        "dependencies": [
            "Script Merger (若有其他脚本Mod)"
        ],
        "installPath": "The Witcher 3\\Mods\\modBrothersInArms\\",
        "installSteps": [
            "1. 下载解压后将 modBrothersInArms 放入 The Witcher 3\\Mods\\ 目录；",
            "2. 若安装了其他剧本或交互 Mod，务必运行 Script Merger 合并冲突脚本。"
        ],
        "isDirect": False,
        "nexusUrl": "https://www.nexusmods.com/witcher3/mods/7329",
        "version": "2.81",
        "downloads": "837.6K",
        "endorsements": "8.1K",
        "checkedAt": "2026-11-20"
    },
    {
        "id": "all-quest-objectives-on-map",
        "title": "All Quest Objectives On Map",
        "author": "Wolfmark",
        "category": "界面导航 (UI / Map)",
        "desc": "在大地图上同时显示所有未完成的主线、支线、猎魔委托与寻宝任务的目标点。",
        "dependencies": [
            "None"
        ],
        "installPath": "The Witcher 3\\Mods\\modAllQuestObjectivesOnMap\\",
        "installSteps": [
            "1. 将下载的 modAllQuestObjectivesOnMap 放入 The Witcher 3\\Mods 目录；",
            "2. 启动游戏在大地图左侧勾选全部任务筛选。"
        ],
        "isDirect": False,
        "nexusUrl": "https://www.nexusmods.com/witcher3/mods/943",
        "version": "4.03.13",
        "downloads": "3.5M",
        "endorsements": "81.6K",
        "checkedAt": "2026-11-20"
    },
    {
        "id": "friendly-hud-nextgen",
        "title": "(Next Gen Edition) Friendly HUD",
        "author": "wghost81 aka Wasteland Ghost",
        "category": "界面交互 (UI / Immersion)",
        "desc": "非战斗状态下自动隐藏小地图与血条，猎魔人感官开启时在 3D 场景中显示任务标记与罗盘。",
        "dependencies": [
            "None"
        ],
        "installPath": "The Witcher 3\\Mods\\modFriendlyHUD\\",
        "installSteps": [
            "1. 将 modFriendlyHUD 解压放入 The Witcher 3\\Mods\\ 文件夹；",
            "2. 将 bin 文件夹覆盖到游戏安装目录以整合配置菜单。"
        ],
        "isDirect": False,
        "nexusUrl": "https://www.nexusmods.com/witcher3/mods/7290",
        "version": "0.9.9.1NGE",
        "downloads": "261.7K",
        "endorsements": "3.9K",
        "checkedAt": "2026-11-20"
    }
]


OWNED_FIELDS = (
    "title",
    "titles",
    "consoleCategories",
    "popularCommands",
    "curatedMods",
    "latestPatch",
    "modInstallPath",
    "nexusStats",
    "consoleShortcut",
    "consoleEnableGuide",
)


def witcher3_fields():
    return {
        "title": "The Witcher 3: Wild Hunt - Complete Edition (Next-Gen)",
        "titles": {
            "en": "The Witcher 3: Wild Hunt - Complete Edition (Next-Gen)",
            "zh-CN": "巫师 3：狂猎 (次世代版 / 完全版 / 完全版)",
            "zh-TW": "巫師 3：狂獵 (次世代重製版 / 完全版)",
            "ja": "ウィッチャー3 ワイルドハント コンプリートエディション (次世代機版)",
            "ko": "더 위쳐 3: 와일드 헌트 - 컴플리트 에디션 (차세대 리마스터)",
            "ru": "Ведьмак 3: Дикая Охота — Полное издание (Next-Gen)",
            "de": "The Witcher 3: Wild Hunt - Complete Edition (Next-Gen)",
            "es": "The Witcher 3: Wild Hunt - Edición Completa (Next-Gen)"
        },
        "consoleCategories": witcher_categories,
        "popularCommands": witcher_popular,
        "curatedMods": witcher_mods,
        "latestPatch": "v4.04 (次世代版 / 完全版 - 官方 REDkit & 工坊支持)",
        "modInstallPath": "The Witcher 3\\Mods\\ (次世代 DX12 主程序位于 bin\\x64_dx12\\witcher3.exe)",
        "nexusStats": {
            "totalDownloads": "224.4M",
            "totalMods": "10,991",
            "checkedAt": "2026-11-20",
            "nexusDomain": "witcher3"
        },
        "consoleShortcut": "~ (波浪键) 或 @ 键 (次世代原生 ini 开启，免 DLL 注入)",
        "consoleEnableGuide": {
            "zh-CN": "1. 【原生免 Mod 开启控制台】在《巫师3 次世代版 / 完全版》安装根目录进入 bin\\config\\base\\ 文件夹，用记事本打开 general.ini；\n2. 【追加调试参数】在文件末尾 [General] 区块最下方另起一行，添加 DBGConsoleOn=true 并保存退出；\n3. 【呼出与执行】启动游戏（次世代默认 DX12 版本路径为 bin\\x64_dx12\\witcher3.exe），在任何战役关卡按下键盘 ~ (波浪键) 或 @ 键即可弹出顶部控制台，输入下方代码回车直接生效！\n4. 【次世代版 / 完全版原生特色提示】本版本已内置原生「拍照模式」(在游戏中随时按 U 键呼出，支持景深、自由机位与滤镜)、「法印快捷施法」(游戏设置-游戏性中开启，无需呼出法印轮盘)、「自动涂抹剑油」(游戏设置中开启，无需额外Mod)，并全面支持官方 REDkit 编辑器与 Steam 创意工坊！",
            "en": "1. Navigate to 'The Witcher 3\\bin\\config\\base\\', open general.ini in Notepad.\n2. Add 'DBGConsoleOn=true' under [General] and save.\n3. Launch game (DX12 executable is in bin\\x64_dx12\\witcher3.exe), press ~ or @ in-game to open console.\n4. Next-Gen features: Built-in Photo Mode (press U), Quick Sign Casting (in Gameplay settings), Auto-apply Oils, and official REDkit mod editor / Steam Workshop support."
        }
    }


if __name__ == "__main__":
    write_owned_fields("rebuild_witcher3_flagship.py", OWNED_FIELDS, {GAME_ID: witcher3_fields()})
