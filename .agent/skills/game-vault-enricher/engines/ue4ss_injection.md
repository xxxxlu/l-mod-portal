# 虚幻引擎 4 / 5 (UE4 / UE5) 注入与控制台规范

## 🎯 核心方案：RE-UE4SS
对于现代虚幻 4 / 5 商业大作（如《黑神话：悟空》、《幻兽帕鲁》、《霍格沃茨之遗》），发行版通常在编译阶段剥离了原生控制台（Shipping Build Strip）。
最通用且稳定的工业级解法是装载 **RE-UE4SS (Unreal Engine 4/5 Scripting System)**。

---

## 🛠️ 安装与配置路径
1. **安装目录**：必须解压至游戏可执行文件同级的 Win64 目录：
   - 黑神话：`<GameRoot>\b1\Binaries\Win64\`
   - 帕鲁：`<GameRoot>\Pal\Binaries\Win64\`
2. **核心引导文件**：
   - `UE4SS.dll`
   - `dxgi.dll` (或 Windows 11/Overlay 冲突时改名为 `dwmapi.dll`)
   - `UE4SS-settings.ini`
3. **关键参数配置 (`UE4SS-settings.ini`)**：
   ```ini
   [Engine]
   GuiConsoleVisible = 1
   EnableHotkeys = 1
   GuiConsoleShortcutKey = F10
   
   [Overrides]
   OverrideConsoleEnabler = 1
   ```

---

## 🎮 控制台呼出与常见指令
- **控制台快捷键**：进入战役关卡后，按 `F10` 或 `~` 呼出 UE4SS 调试面板 / 原生命令栏。
- **高频通用指令**：
  - `slomo <rate>`：全场景时间流速缩放（如 `slomo 0.3` 识破防反、`slomo 1.0` 还原、`slomo 2.0` 狂奔）
  - `teleport`：沿准星方向向前瞬移（穿透空气墙）
  - `toggledebugcamera`：360° 自由飞行观察摄像机
  - `ShowHUD 0` / `ShowHUD 1`：隐藏/显示游戏 UI
  - `r.Tonemapper.Sharpen 1.5`：抗锯齿细节锐化
  - `r.MotionBlurQuality 0`：关闭动态模糊
  - `stat fps`：显示帧率

---

## ⚡ 黑神话专属：BGUFunctionLibraryManaged:RunScriptGM
针对黑神话等特定大作，原生导出了 GM 调试接口。无需在控制台手工寻找偏移，可通过 UE4SS Lua 脚本直接调用游戏原生函数库：
```lua
local lib = StaticFindObject("/Script/b1-Managed.Default__BGUFunctionLibraryManaged")
local ctx = FindFirstOf("BGPPlayerController")
lib:RunScriptGM("additem 1002 100000", ctx)  -- 获得 100,000 灵蕴
lib:RunScriptGM("allweapon", ctx)            -- 解锁全部神兵
lib:RunScriptGM("allsoulskill", ctx)         -- 解锁全部 54 种精魄变身
```
由社区工具（如 `WukongGM`）封装为热键一键执行（默认 `F7`），具备跨补丁免维护特性。
