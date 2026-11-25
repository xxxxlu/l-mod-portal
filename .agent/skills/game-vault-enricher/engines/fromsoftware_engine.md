# FromSoftware 专有引擎与魂系模组架构规范

## 🎯 适用品类与代表游戏
- 《艾尔登法环》(Elden Ring - Steam AppID: 1245620)
- 《只狼：影逝二度》(Sekiro: Shadows Die Twice - Steam AppID: 814380)
- 《黑暗之魂 3》(Dark Souls III - Steam AppID: 374320)
- 《装甲核心 6：境界天火》(Armored Core VI - Steam AppID: 1888160)

---

## 🛡️ 核心痛点：Easy Anti-Cheat (EAC) 离线绕过机制

FromSoftware 自《艾尔登法环》起引入了 Easy Anti-Cheat (EAC)。若不彻底解除反作弊，任何内存修改器、Cheat Engine 或 Mod 注入均会导致游戏无法启动或面临 Steam 账号联机封禁惩罚。

### 标准离线绕过工作流 (100% 安全免封)
1. **替换引导文件法**：
   - 进入游戏主程序目录 `<GameRoot>\Game\`；
   - 将原版 `start_protected_game.exe` 重命名为 `start_protected_game.exe.bak`；
   - 将主程序 `eldenring.exe` 复制一份，并重命名为 `start_protected_game.exe`；
   - 在同级目录新建文本文件 `steam_appid.txt`，内容填入 `1245620`；
   - 此时通过 Steam 或直接双击启动游戏，右下角将提示“检测到作弊行为，已进入离线模式”，此时可 100% 安全进行单机作弊与模组挂载！
2. **ModEngine2 一键离线引导**：
   - 解压 ModEngine2 包含的 `launchmod_eldenring.bat`，其内置了针对 EAC 的启动管道重定向，无需修改原版文件即可实现一键离线加载。

---

## 🛠️ 底层注入框架：ModEngine2 与 Cheat Engine (TGA/Hexinton)

### 1. ModEngine2 架构规范
- **安装路径**：独立解压至任意纯英文目录（推荐 `<GameRoot>\ModEngine2\`）；
- **核心文件**：
  - `modengine2_launcher.exe`
  - `config_eldenring.toml`
  - `mod/` 文件夹（放置解压后的 `.dcx`, `.param`, `regulation.bin` 等资源）
- **配置文件配置 (`config_eldenring.toml`)**：
  ```toml
  [modengine]
  debug = false
  
  [extension.mod_loader]
  enabled = true
  mods = [
      { enabled = true, name = "default", path = "mod" }
  ]
  ```

### 2. The Grand Archives (TGA) & Hexinton 顶级 CT 表
FromSoftware 游戏原生并不提供打字控制台，全功能作弊的核心依赖是社区经过反编译与逆向维护的 **The Grand Archives Cheat Engine Table**：
- **核心功能矩阵**：
  - **Item Gib (物品瞬间注入器)**：直接通过内部 8 位 ID 向背囊派发全套武器（含满级强化 +10/+25 变种）、防具、护符、骨灰与法术；
  - **Unlock All Graces (点亮全地图赐福点)**：一键点亮交界地与黄金树幽影 DLC 全图赐福与传送门；
  - **FreeCam & Time Freeze**：脱离角色控制 360° 自由运镜截图；
  - **Stat & Runes Injection**：自由指定 8 大属性点数（生命/耐力/力气/灵巧/智力/信仰/感应）与注入数千万卢恩。

---

## 📦 核心物品 ID 结构与数据解析
魂系物品 ID 按类型分类分段存储：
- **近战武器**：`1000000` - `1999999`（末尾数字代表强化等级与质变代码，如 `1000000` 为普通 +0，`1000025` 为 +25）
- **防具护甲**：`2000000` - `2999999`
- **护符饰品**：`3000000` - `3999999`
- **魔法与祷告**：`4000000` - `4999999`
- **骨灰召唤物**：`5000000` - `5999999`
- **消耗品与关键素材**：`100` - `9999`（如古龙岩锻造石、失色古龙岩锻造石、追忆）

---

## ⚠️ 常见踩坑与存档防损规范
1. **绝版切回线上规范**：如需切回正版线上联机，必须**彻底删除由作弊生成的非法绝版道具**（如带越级强化数值的武器、未实装的测试道具、超过持有上限的关键物品），否则登录线上服务器将被 FromSoftware 检测到非法存档并处以 180 天小黑屋隔离惩罚；
2. **存档路径备份**：
   - 艾尔登法环存档位置：`%AppData%\EldenRing\<SteamID64>\ER0000.sl2`
   - 作弊或大改模组前必须手动复制备份存档！
