# Rockstar RAGE 引擎与 Script Hook 架构规范

## 🎯 适用品类与代表游戏
- 《侠盗猎车手 5》(Grand Theft Auto V - Steam AppID: 271590)
- 《荒野大镖客：救赎 2》(Red Dead Redemption 2 - Steam AppID: 1174180)

---

## 🛠️ 底层注入核心：Script Hook 系列

Rockstar 专有的 RAGE (Rockstar Advanced Game Engine) 采用强混淆与原生脚本虚拟机。单机环境下所有高级功能、载具生成与物理调校均基于 Alexander Blade 开发的 **Script Hook**。

### 1. GTA V 核心安装路径
- **文件清单**：解压至 `GTA V` 安装根目录（与 `GTA5.exe` 同级）：
  - `ScriptHookV.dll` (核心原生函数运行时)
  - `dinput8.dll` (DirectInput API 挂钩引导器)
  - `NativeTrainer.asi` (官方原版内置基础菜单) 或第三方全能菜单 `Menyoo.asi` + `menyooStuff/`
- **菜单呼出快捷键**：进入单人线下故事模式后，按键盘 **`F4`** 呼出 Native Trainer（小键盘 `8/2/4/6` 控制上下翻页，`5` 确认，`0` 返回）；按 **`F8`** 呼出 Menyoo 终极修改菜单。

### 2. RDR2 (荒野大镖客 2) 核心安装路径
- **文件清单**：解压至 `Red Dead Redemption 2` 根目录：
  - `ScriptHookRDR2.dll`
  - `dinput8.dll`
  - 推荐第三方顶级菜单：`Rampage Trainer` (`Rampage.asi` + `RampageFiles/`)
- **呼出快捷键**：按 **`F5`** 呼出 Rampage 界面。

---

## 💻 线下原生秘籍与控制台机制

除了 Script Hook 菜单外，RAGE 引擎故事模式内置了经典的电话号码与控制台秘籍：

### 1. GTA V 控制台秘籍 (~ 键输入 或 手机拨号)
- 按键盘 **`~` (波浪键)** 开启全屏命令框：
  ```text
  PAINKILLER         # 上帝模式 (5分钟无敌，过期需重新输入)
  TURTLE             # 生命值与护甲值瞬间全满，修复当前载具
  FUGITIVE           # 通缉星级 +1 星
  LAWYERUP           # 通缉星级降低为 0 (消星)
  POWERUP            # 瞬间回满角色专属特殊技能槽
  CATCHME            # 极速狂奔移动
  HOPTOIT            # 超级大跳 (跳跃高度翻倍)
  SKYDIVE            # 瞬间获得一把降落伞
  SKYFALL            # 高空天降自由落体跳伞
  COMET              # 瞬间召唤彗星跑车 (Pfister Comet)
  RAPIDGT            # 瞬间召唤疾速 GT 跑车 (Dewbauchee Rapid GT)
  BUZZOFF            # 瞬间召唤秃鹰武装直升机 (Buzzard Attack Chopper)
  ```

### 2. RDR 2 内置秘籍 (设置 -> 秘籍列表)
需在设置菜单中输入指定密语解锁（部分秘籍需要先在报社购买特定报纸方可激活）：
- `A simple life, a beautiful death`：获得全套基础武器
- `You want punishment`：通缉等级上升
- `You want freedom`：清除全郡通缉赏金
- `You flourish before you die`：生命、体力、死神之眼核心与外圈全满
- `Better than my dog`：无论距离多远随时吹哨唤来马匹

---

## 🚨 安全防封与线上隔离红线 (CRITICAL)
1. **绝对禁止带 Mod 登入线上联机 (GTA Online / Red Dead Online)**：
   - 只要主目录下存在 `dinput8.dll` 或任何 `.asi` 插件，在点击进入线上模式前必须将其重命名或移出；
   - 否则 Rockstar 反作弊监测系统将立即触发永久硬件封号惩罚；
2. **BattlEye 反作弊隔离**：GTA V 引入 BattlEye 后，若仅游玩单人故事模式，可在启动器设置中关闭 BattlEye 启动参数。
