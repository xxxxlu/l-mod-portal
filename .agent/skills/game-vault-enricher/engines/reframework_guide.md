# 卡普空 RE 引擎与 REFramework 架构规范

## 🎯 适用品类与代表游戏
- 《生化危机 4：重制版》(Resident Evil 4 Remake - Steam AppID: 2050650)
- 《生化危机 8：村庄》(Resident Evil Village - Steam AppID: 1196590)
- 《生化危机 2 / 3 重制版》(Resident Evil 2 & 3 Remake)
- 《龙之信条 2》(Dragon's Dogma 2 - Steam AppID: 2054970)
- 《怪物猎人：崛起》(Monster Hunter Rise - Steam AppID: 1446780)
- 《街头霸王 6》(Street Fighter 6 - Steam AppID: 1364780)

---

## 🛠️ 底层注入核心：praydog's REFramework

卡普空 RE 引擎 (Reach for the Moon Engine) 采用模块化 C++ 与专用脚本运行时。社区公认且唯一的全能级底层框架是由 praydog 开发的 **REFramework**。

### 1. 架构与安装路径
- **安装方法**：将下载的 `dinput8.dll` 直接拷贝至游戏安装根目录（与游戏主程序 `.exe` 同级）；
- **核心文件目录结构**：
  - `dinput8.dll` (DirectInput API 劫持引导入口)
  - `reframework/`
    - `autorun/` (存放所有第三方 `.lua` 脚本与自启动插件)
    - `data/` (模组数据与配置文件)
    - `plugins/` (编译好的本地 C++ 扩展插件)
- **菜单呼出快捷键**：进入游戏战役或主菜单后，按下键盘 **`Insert`** 键（部分笔记本为 `Fn + Insert`），屏幕左上角即可展开半透明 ImGui 图形化控制面板。

---

## 🎮 REFramework 核心功能与调试接口

### 1. 镜头与沉浸式画面掌控 (Camera & Graphics)
- **FreeCam (自由飞行摄像机)**：在 REFramework 菜单中勾选 `FreeCam`，可使用鼠标与 `WASD` 键自由穿墙漫游，无死角拍摄里昂、阿什莉与怪物的特写细节；
- **First-Person Mod (第一人称视角)**：支持原生无缝切换第一人称沉浸式视角；
- **FOV Slider (视场角无级调节)**：打破原版锁死的局促第三人称越肩视角，消除 3D 晕动眩晕；
- **Vignette & Motion Blur Override**：一键彻底移除暗角遮罩、色差与动态模糊涂抹。

### 2. 运行时对象反射与 Lua 脚本生态 (`reframework.autorun`)
REFramework 提供了完整的 C# / C++ 原生 SDK 对象运行时反射机制。开发者与玩家可通过简单的 Lua 脚本在运行时挂钩游戏内存：
```lua
-- 示例：获取当前玩家生命值与无敌控制
local player_manager = sdk.get_native_singleton("via.player.PlayerManager")
local local_player = sdk.call_native_func(player_manager, sdk.find_type_definition("via.player.PlayerManager"), "getLocalPlayer")

if local_player then
    local health = local_player:get_Health()
    health:set_CurrentHealth(health:get_MaxHealth()) -- 瞬间满血锁定
end
```

### 3. 主流必备扩展模组矩阵
- **Item Spawner (全武器与道具生成器)**：直接呼出全图形化道具箱，一键生成马格南左轮、火箭发射器、急救喷雾、金色鸡蛋与无限微型手榴弹；
- **Weapon Adjuster (武器参数微调器)**：无极调整后坐力、扩散十字准星、换弹速度与最大装弹量；
- **Costume & Character Model Swapper**：角色皮肤与外观一键实时热替换。

---

## ⚠️ 常见排错与崩溃防范
1. **DirectX 12 崩溃与黑屏**：若游戏启动闪退，多因游戏内置的 HDR 或 Ray Tracing 与早期版本的 Overlay 渲染冲突。建议更新显卡驱动至最新，或在 `re2_framework.log` 中查看未捕获的空指针异常；
2. **多模组加载工具**：推荐搭配 **Fluffy Mod Manager (Modmanager.exe)** 统一管理 `.pak` 皮肤与材质包，确保解压与还原完全自动化，杜绝文件脏污。
