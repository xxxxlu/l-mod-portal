# Paradox Clausewitz 引擎控制台与 Grand Strategy 规范

## 🎯 适用品类与代表游戏
- 《钢铁雄心 4》(Hearts of Iron IV - Steam AppID: 394360)
- 《群星》(Stellaris - Steam AppID: 281990)
- 《十字军之王 3》(Crusader Kings III - Steam AppID: 1158310)
- 《维多利亚 3》(Victoria 3 - Steam AppID: 529340)
- 《欧陆风云 4》(Europa Universalis IV - Steam AppID: 236850)

---

## 🛠️ 控制台激活与快捷键配置

### 1. 激活调试模式 (Debug Mode)
P社游戏在非铁人模式 (Non-Ironman) 下默认原生开放控制台。但在 CK3 与 Victoria 3 中，必须通过 Steam 启动项加入参数：
- 打开 Steam 游戏属性 -> 通用 -> 启动选项 -> 输入 `-debug_mode`；
- 进入游戏后，键盘按下 **`~` (波浪键)** 或 **`Shift + 2`** 或 **`§` 键** 即可展开全屏/顶部控制台终端。

---

## 💻 核心语法范式与国家 Tag 体系

Clausewitz 引擎所有指令由英文字符构成，支持直接传参与国家代码 (3位英文字母 TAG) 目标指向：

### 1. 国家切换与政治意志 (`tag`)
```text
tag <TAG>          # 切换操控国家 (如 tag GER 德国, tag SOV 苏联, tag USA 美国, tag CHI 中国)
pp <amount>        # 增加政治点数 (Political Power)
cp <amount>        # 增加指挥点数 (Command Power)
st <amount>        # 增加国家稳定度 (Stability)
ws <amount>        # 增加战争支持度 (War Support)
nu <amount>        # 修改中立度
```

### 2. 瞬间建造与瞬间科研 (Instant Economy & Tech)
```text
ic                 # 切换瞬间建造模式 (Instant Construction: 工厂、要塞、造船厂秒落成)
research all       # 瞬间研究全部科技树 (包含核武器与喷气战机)
research_on_icon_click # 鼠标点击任意科技图标瞬间研发完成
fuel <amount>      # 增加战略石油燃油储备
manpower <amount>  # 增加行省适役人口兵源
```

### 3. 外交与国策瞬间突破 (Diplomatic & Focus Cheats)
```text
yesman             # 强制外交同意 (AI 无条件接受一切宣战、同盟、租借法案与和平谈判)
focus.autocomplete # 瞬间完成国策树焦点任务 (无需等待70天周期)
focus.nochecks     # 忽略一切先决国策前提限制自由点选
decision.nochecks  # 忽略一切决议条件瞬间激活决策
fow                # 完全消除战争迷雾 (查看全球敌军部署动态)
allowdiplo         # 允许使用所有外交选项无视世界紧张度限制
```

### 4. 军队与装备瞬间列装
```text
ale <amount>       # 获得所有陆军装备 (Add Latest Equipment: 步枪、火炮、坦克、防空炮全满)
gain_xp <amount>   # 增加陆军、海军、空军经验点数
xp <amount>        # 增加全军种三军经验
annex <TAG>        # 瞬间吞并指定国家领土
whitepeace <TAG>   # 与指定国家立即达成白和平停战
```

---

## ⚠️ 常见排错与注意事项
1. **铁人模式限制**：铁人模式 (Ironman) 会在存档底层彻底禁用控制台以防止成就作弊。如果需要全成就，建议使用 `Achievement Watcher` 或在本地修改器中开启免封锁补丁；
2. **AI 同时享受 ic 陷阱**：在《钢铁雄心4》中输入 `ic` 后，**全球所有 AI 国家也会同时获得瞬间建造加成**！正确做法：在游戏暂停状态下输入 `ic`，排满建造队列，随后立即再次输入 `ic` 关闭，然后再恢复游戏时间流逝。
