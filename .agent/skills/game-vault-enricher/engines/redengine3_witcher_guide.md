# CDPR REDengine 3 (巫师 3 次世代版 / 完全版) 调试控制台与引擎规范

## 🎯 适用品类与官方版本说明
- **游戏官方全称**：《巫师 3：狂猎 完全版 / 次世代版》(The Witcher 3: Wild Hunt - Complete Edition / Next-Gen Edition)
- **Steam AppID**：`292030` | **REDkit 官方编辑器 AppID**：`2684660`
- **适配最新版本**：**Next-Gen v4.04+ (次世代完全版)** 及后续维护补丁
- **底层架构分流**：
  - **DirectX 12 核心主程序**：`The Witcher 3\bin\x64_dx12\witcher3.exe`（支持光线追踪全局光照、DLSS 3 帧生成、FSR 2.1、XeSS）
  - **DirectX 11 兼容主程序**：`The Witcher 3\bin\x64\witcher3.exe`（老旧显卡回退模式）
  - **配置文件路径**：`Documents\The Witcher 3\dx12user.settings` (DX12) 与 `user.settings` (DX11)

> [!IMPORTANT]
> **版本术语对齐**：《巫师 3》当前最新主力版本为 **次世代版 / 完全版 (Next-Gen Edition / Complete Edition, v4.00 - v4.04+)**；CDPR 官方另行宣布由 Fool's Theory 采用虚幻5引擎（UE5）从零重新制作的《巫师：重制版》(The Witcher Remake - 代号 Canis Majoris) 为全新下一代独立作品，两者不可混淆。

---

## 🛠️ 控制台激活与快捷键配置

### 1. 原生免 Mod 配置文件开启法 (官方推荐，100% 杜绝崩溃)
次世代版 v4.00 - v4.04+ 已原生内置调试控制台开关，无需安装任何可能导致游戏闪退的第三方 DLL 补丁：
1. 用记事本打开游戏安装目录下的基础配置文件：
   `The Witcher 3\bin\config\base\general.ini`
2. 在 `[General]` 区块下方另起一行，填入：
   ```ini
   [General]
   DBGConsoleOn=true
   ```
3. 保存文件并启动游戏。在任何关卡、对话或大地图中随时按下键盘左上角 **`~` (波浪键)** 或 **`@` 键**，屏幕顶部即可弹出透明调试输入窗口。

> [!WARNING]
> 严禁向次世代版的 `bin\x64\` 或 `bin\x64_dx12\` 目录随意复制老旧 1.32 时代的 `dsound.dll` 补丁，此类遗留插件会导致 DX12 主程序启动静默闪退或报 Script Compilation Error！

---

## 📸 次世代重制版内置特色系统 (无需 Mod)
1. **原生拍照模式 (Native Photo Mode)**：游戏中随时按下键盘 **`U` 键** 即可进入照片模式，支持自由移动摄像机、调整 FOV、景深光圈、胶片颗粒及多款预设调色滤镜；
2. **法印快捷施法 (Quick Sign Casting)**：在「选项 -> 游戏设定」中开启，无需呼出法印轮盘，按住施法组合键即可瞬发 5 大法印；
3. **自动涂抹剑油 (Auto-Apply Oils)**：在「选项 -> 游戏设定」中开启，战斗时杰洛特会自动涂抹克制当前怪物种族的最高阶剑油；
4. **全中文普通话配音**：次世代版全量实装高质量普通话配音，可在音频设置中自由切换；
5. **官方 REDkit 编辑器支持**：2024 年 5 月 CDPR 正式发布官方 REDkit 模组套件与 Steam 创意工坊支持。

---

## 💻 语法范式与函数调用规范 (WitcherScript)

WitcherScript 是 CDPR 自研的面向对象脚本语言，控制台直接暴露了引擎内部的原生 Global Functions：

### 1. 核心无敌与主角掌控 (Direct Commands)
```text
god              # 完全无敌 (锁死生命与昆恩法印护盾，免疫一切抓击与坠落伤害)
likeaboss        # Boss 战神模式 (免伤 99% 且每次重击按 40% 百分比秒削敌方血量)
healme           # 立即瞬回满血并清除流血、中毒、燃烧异常状态
staminaboy       # 无限耐力与活力 (连续翻滚、回旋剑舞与拜年剑法零冷却)
killall          # 秒杀视野内全部敌对实体
secretgwint      # 一键将全大陆所有阵营全套昆特牌直接加入牌库
winGwint(true)   # 当前昆特牌对局立即判定以绝对优势秒胜
Ciri             # 切换操控主角为希里 (独享瞬移穿梭绝招)
Geralt           # 切换回利维亚的杰洛特
shave            # 刮净杰洛特胡须
setbeard(1)      # 瞬间长出茂密络腮胡
dismember        # 攻击必定触发慢动作断肢处决特写
cat(1)           # 开启全图夜视猫眼视觉 (cat(0) 关闭)
```

### 2. 带参函数调用 (Function Call Syntax)
注意：字符串参数**必须使用单引号 `'...'` 包裹**，数值参数直接传参：
```text
addmoney(100000)                       # 增加 100,000 克朗金币
setlevel(100)                          # 设定角色等级为 100 级满级
addskillpoints(50)                     # 增加 50 点未分配能力点
cleardevelop                           # 重置并清空全部技能与突变点 (洗点)
ShowAllFT(1)                           # 点亮全大陆 100% 快速旅行路标
AllowFT(1)                             # 允许在全图任意位置直接快速旅行 (摆脱木桩限制)
ShowPins(1)                            # 标亮全地图所有未探索的问号 '?' 标记
settime(12)                            # 将世界时间跳转至正午 12:00
changeweather('WT_Rain_Storm')         # 切换为暴风暴雨雷电天气
```

### 3. 次世代重制版专属神装与特典物品代码
次世代版重制新增了诸多专属装备，代码严格区分大小写：
```text
# 西境白虎套装 (White Tiger of the West - 次世代中国风特典 6 件套)
additem('White Tiger Armor')           # 西境白虎盔甲 (提尔格里希护甲)
additem('White Tiger Boots')           # 西境白虎靴子
additem('White Tiger Gloves')          # 西境白虎手套
additem('White Tiger Pants')           # 西境白虎下装
additem('White Tiger Steel Sword 1')   # 九尾狐女钢剑
additem('White Tiger Silver Sword 1')  # 九尾狐女银剑

# 多尔·布雷坦纳百花套装 (Dol Blathanna Set - 次世代特典千花精灵套 6 件套)
additem('Dol Blathanna Armor')         # 多尔·布雷坦纳千花盔甲
additem('Dol Blathanna Boots')         # 多尔·布雷坦纳千花靴子
additem('Dol Blathanna Gloves')        # 多尔·布雷坦纳千花手套
additem('Dol Blathanna Pants')         # 多尔·布雷坦纳千花长裤
additem('Dol Blathanna Steel Sword 1') # 千花钢剑
additem('Dol Blathanna Silver Sword 1')# 白女妖银剑

# 遗忘狼学派全套进阶 (Netflix 剧版亨利卡维尔同款)
additem('Netflix Armor')               # 初阶遗忘狼护甲 (第1季外观)
additem('Netflix Steel Sword')         # 初阶遗忘狼钢剑
additem('Netflix Silver Sword')        # 初阶遗忘狼银剑
additem('Netflix Armor 1')             # 极品遗忘狼护甲
additem('Netflix Steel Sword 1')       # 极品遗忘狼钢剑
additem('Netflix Silver Sword 1')      # 极品遗忘狼银剑
additem('Netflix Armor 2')             # 宗师级遗忘狼护甲 (第2季全黑紧身战甲)
additem('Netflix Boots 2')             # 宗师级遗忘狼靴子
additem('Netflix Gloves 2')            # 宗师级遗忘狼手套
additem('Netflix Pants 2')             # 宗师级遗忘狼下装
additem('Netflix Steel Sword 2')       # 宗师级遗忘狼钢剑
additem('Netflix Silver Sword 2')      # 宗师级遗忘狼银剑

# 次世代联动昆特牌
additem('gwint_card_roach')            # 萝卜昆特牌 (次世代联动中立英雄牌，战力 3 带集结特效)
```

---

## 🛠️ 次世代 Mod 管理与排错红线
1. **次世代模组路径**：模组文件夹统一放置在 `The Witcher 3\Mods\` 目录下；
2. **多模组冲突合并 (Script Merger)**：安装超过两个修改脚本的 Mod 时，必须使用次世代版适配的 `Witcher 3 Script Merger` 解决代码冲突，否则启动游戏会报 `Script Compilation Error`；
3. **DX12 材质优化**：次世代虽然官方集成了部分高清材质，但追求极致画质推荐安装 `The Witcher 3 HD Reworked Project NextGen Edition` (Halk Hogan PL)，在视频设置中勾选 HDReworked 选项即可。
