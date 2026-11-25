# Unity 引擎与 BepInEx / 独立游戏调试架构规范

## 🎯 适用品类与代表游戏
- 《英灵神殿》(Valheim - Steam AppID: 892970)
- 《深海迷航》(Subnautica - Steam AppID: 264710)
- 《边缘世界》(RimWorld - Steam AppID: 294100)
- 《雨中冒险 2》(Risk of Rain 2 - Steam AppID: 632360)
- 《森林之子》(Sons of the Forest - Steam AppID: 1326470)
- 《杀戮尖塔》(Slay the Spire - ModTheSpire / Unity)

---

## 🛠️ Unity 底层模组标准：BepInEx (5.x / 6.x)

BepInEx 是 Unity (Mono / IL2CPP) 游戏事实上的工业级底层注入器与插件装载器。

### 1. 架构与安装路径
- **根目录注入文件**：
  - `winhttp.dll` (Windows 原生 API 劫持引导)
  - `doorstop_config.ini`
  - `BepInEx/`
    - `core/` (核心运行时程序集)
    - `config/` (各插件自动生成的 `.cfg` 配置文件)
    - `plugins/` (所有第三方 `.dll` 模组的存放目录)
- **IL2CPP 游戏特化**：针对 IL2CPP 编译游戏（如特定现代商业 Unity 作品），需使用 BepInEx 6.x Bleeding Edge 构建，并自动生成 Interop 程序集。

---

## 💻 原生开发者控制台唤出与作弊参数

许多 Unity 独立作品内置了未禁用的开发者控制台，但需要特定启动参数或按键序列激活：

### 1. 英灵神殿 (Valheim)
- **启动项设置**：Steam 游戏属性 -> 通用 -> 启动选项中输入 `-console`；
- **控制台激活**：游戏中按 `F5` 呼出控制台输入框；
- **核心提权指令**：
  ```text
  devcommands                # 激活开发者超级权限模式 (必须先输入此指令)
  debugmode                  # 开启创造模式 (按 Z 自由飞行，按 K 秒杀周边敌怪，按 B 自由建造零材料消耗)
  god                        # 无敌模式
  ghost                      # 幽灵隐形模式 (怪物完全无视玩家)
  raiseskill <skill> <level> # 技能等级提升 (如 raiseskill run 100)
  spawn <item> <amount>      # 生成物品与生物
  heal                       # 恢复满血
  puke                       # 清空胃部饱食度以重新食用顶级食物
  ```

### 2. 深海迷航 (Subnautica)
- **控制台激活按键**：按 `F3` 打开调试面板，按 `F8` 调出鼠标，取消勾选左上角的 `Disable Console`，之后随时按 `~` 或 `Enter` 呼出控制台；
- **核心指令**：
  ```text
  nodamage                   # 上帝模式 (生命、饥饿、口渴、氧气完全锁死)
  oxygen                     # 无限氧气供应
  item <id> <count>          # 直接获取物品
  spawn <id> <count>         # 在准星处生成载具、生物或矿石 (如 spawn seamoth 1)
  fastbuild                  # 瞬间完成水下建造
  nocost                     # 零材料自由建造
  day / night                # 昼夜切换
  ```

### 3. 边缘世界 (RimWorld)
- **内置开发者模式 (Dev Mode)**：
  - 游戏内打开“选项 (Options)” -> 勾选“开发人员模式 (Development Mode)”；
  - 屏幕顶部中央将浮现一排调试图标：
    - `God Mode` (上帝模式)：全建筑一键瞬间落成，无视科技、材料与施工等待；
    - `Debug Actions Menu` (第四个齿轮图标)：全地图生成袭击、清除机械族、治疗所有殖民者疾病成瘾、瞬加科技研究。

---

## 📦 Unity Mod 与存档防错指南
1. **依赖项管理**：绝大多数高级 Unity 模组强依赖于 `ConfigurationManager`（游戏中按 `F1` 呼出统一图形化配置面板）与 `HookGenPatcher`；
2. **存档路径统一归档**：
   - Unity 独立游戏存档通常位于 `%AppData%\..\LocalLow\<DeveloperName>\<GameName>\`；
   - 在进行大规模控制台测试前，务必打包备份当前文件夹。
