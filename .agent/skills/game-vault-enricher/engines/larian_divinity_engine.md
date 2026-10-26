# Larian Divinity 4.0 引擎与博德之门 3 模组架构规范

## 🎯 适用品类与代表游戏
- 《博德之门 3》(Baldur's Gate 3 - Steam AppID: 1086940)
- 《神界：原罪 2》(Divinity: Original Sin 2 - Steam AppID: 435150)

---

## 🛠️ 底层注入核心：Norbyte's BG3 Script Extender

拉瑞安自研的 Divinity 4.0 引擎采用复杂的 Osiris 故事脚本系统。目前最为强大的工业级底层挂载器是 Norbyte 维护的 **BG3 Script Extender**。

### 1. 架构与安装路径
- **安装路径**：解压至 `Baldur's Gate 3\bin\` 目录（与 `bg3.exe` 和 `bg3_dx11.exe` 同级）；
- **核心文件**：
  - `DWrite.dll` (DirectWrite API 挂钩劫持引导)
  - `ScriptExtenderSettings.json`
- **配置文件配置 (`ScriptExtenderSettings.json`)**：
  ```json
  {
    "CreateConsole": true,
    "EnableLuaDebugger": false,
    "EnableDebugger": false
  }
  ```
  设置为 `CreateConsole: true` 后，启动游戏会自动弹出一个独立的 Windows 控制台终端黑窗，支持直接执行 Lua 代码与 Osiris 查询。

---

## 💻 控制台指令与 Osiris 函数语法

在 Script Extender 控制台终端中，可直接调用全局 `Osi` 命名空间下的所有内部故事引擎函数：

### 1. 物品与金币直接注入 (`Osi.TemplateAddTo`)
语法格式：`Osi.TemplateAddTo("模板GUID", "目标角色GUID", 数量)`
```lua
-- 向主角背包注入 100,000 金币
Osi.TemplateAddTo("f791555d-355b-4029-9e36-fb38e7898d9e", GetHostCharacter(), 100000)

-- 注入传奇武器：博德安的巨人杀手巨剑 (Balduran's Giantslayer)
Osi.TemplateAddTo("3b6b2512-cf49-411a-8260-cb56220b0805", GetHostCharacter(), 1)

-- 注入传奇武器：猩红恶意 (Crimson Mischief)
Osi.TemplateAddTo("77f3e827-fc19-4876-805c-35804ee9be76", GetHostCharacter(), 1)

-- 注入传奇防具：地狱火护甲 (Helldusk Armour)
Osi.TemplateAddTo("026fe827-ce47-49f3-855c-e587e91eb3c8", GetHostCharacter(), 1)
```

### 2. 角色属性、法术位与豁免掌控
```lua
-- 立即为当前角色回复全部法术位与动作点
Osi.RestoreSpellSlots(GetHostCharacter())

-- 增加未分配经验值 (Exp)
Osi.AddExperience(GetHostCharacter(), 50000)

-- 强制锁定好感度 / 关系破除
Osi.SetAttitude(GetHostCharacter(), "影心/阿斯代伦GUID", 100)
```

---

## 📦 现代模组管理标准：BG3 Mod Manager (BG3MM)
- **Mod 物理存放路径**：
  `%LocalAppData%\Larian Studios\Baldur's Gate 3\Mods\`
- **配置与加载顺序 (`modsettings.lsx`)**：
  `%LocalAppData%\Larian Studios\Baldur's Gate 3\PlayerProfiles\Public\modsettings.lsx`
- 模组打包格式均为 `.pak`，必须通过 BG3MM 导出至活动加载顺序 (Active Load Order)，避免手工修改 XML 导致存档损坏。
