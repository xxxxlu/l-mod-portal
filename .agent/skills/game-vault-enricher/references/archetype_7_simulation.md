# 原型 7：拟真驾驶、飞行与物理模拟 (Driving & Physics Simulation)

## 📌 代表游戏与引擎映射
| 游戏名称 | Steam AppID | 引擎方案 | 核心控制台 / 注入工具 |
|---|---|---|---|
| 《欧洲卡车模拟 2》(Euro Truck Simulator 2) | 227300 | Prism3D Engine | `config.cfg` 启用开发者控制台 |
| 《美洲卡车模拟》(American Truck Simulator) | 270880 | Prism3D Engine | `config.cfg` 启用开发者控制台 |
| 《极限竞速：地平线 5》(Forza Horizon 5) | 1551360 | ForzaTech 专有引擎 | AIO Cheat Tool / FLiNG Trainer |
| 《车祸模拟器》(BeamNG.drive) | 284160 | Torque3D + Lua | `F11` 原生世界编辑器 (World Editor) |
| 《微软模拟飞行》(Microsoft Flight Simulator) | 1250410 | Asobo 专有引擎 | 开发者模式 (Dev Mode) |
| 《神力科莎》(Assetto Corsa) | 244210 | 专有物理引擎 | Content Manager + Custom Shaders Patch |

---

## 🔍 四级精准技术检索 SOP (4-Tier Retrieval Queries)

### Tier 1: 官方开发者控制台规范与配置手册
- `site:truckersmp.com "Developer console commands" "config.cfg"`
- `site:beamng.com "World Editor" "Lua console commands"`
- `"Euro Truck Simulator 2" "console commands" site:scssoft.com`

### Tier 2: 专有底层运行时与开源代码仓
- `site:github.com "BeamNG" "Lua"`
- `site:github.com "x4fab/acc-extension-config"` (Assetto Corsa CSP)

### Tier 3: Nexus Mods / RaceDepartment 权威专区
- 重点定位：Physics Engine Overhauls (真实悬挂与抓地力修正)、Sound Engine Fixes (真实发动机引擎轰鸣)、All Garages Unlocked (全欧洲车库买断)、No Police Fines (消除违章罚单)。

### Tier 4: 社群高频痛点与卡车货物防损
- `site:reddit.com/r/trucksim "ets2 freecam teleport not working"`
- `site:reddit.com/r/BeamNG "reset car deformation hotkey"`
- `"ets2" "turn off speed limiter console command"`

---

## 🎯 八大系统维度全息核对清单 (Mandatory 8-Dimension Checklist)

1. **👑 自由漫游飞行视角与平稳着陆传送 (FreeCam & Teleportation)**：
   - 欧卡 2：按键盘数字 `0` 键切换至漫游飞行摄像机，按小键盘 `8/4/5/6` 自由穿云低空飞行；
   - 移动到目标地表上方，按下键盘 **`F9`** 键，卡车瞬间平稳安全投送至地面（告别漫长 2000 公里疲劳驾驶！）。
2. **📍 城市坐标直达瞬间跳跃 (`goto`)**：
   - 输入 `goto <city_name>` (如 `goto berlin`, `goto paris`, `goto london`)，瞬间将摄像机与运货车辆传送至目标枢纽货运站。
3. **🔧 车辆瞬间全损修复与无限燃油 (Instant Repair & Infinite Fuel)**：
   - 发生严重车祸导致发动机红字熄火、车架全损时，一键完全消除 100% 车损，恢复崭新出厂状态；
   - 油箱燃料锁定为 100%，长途跨境无需中途寻找加油站停靠。
4. **🏎️ 发动机动力调校与扭矩/马力突破**：
   - 解除 90 km/h 强制限速安全锁器（`g_speed_limiter 0`）；
   - 将卡车马力改装至 1000+ 匹马力，轻松拖曳百吨重装特种变压器货物爬坡飞驰。
5. **👮 违章罚单、疲劳驾驶与交通处罚彻底豁免**：
   - `g_police 0`：彻底关闭雷达测速拍照、闯红灯罚款、压线逆行与未开大灯的惩罚金扣除；
   - `g_fatigue 0`：彻底关闭疲劳驾驶打瞌睡哈欠与屏幕变黑机制，无需寻找旅馆强制睡觉。
6. **💰 物流帝国财富与等级直升满级**：
   - 瞬间注入数亿欧元流动资金；
   - 等级直升至传奇运输大亨，一键全自动买断全欧洲所有主要物流枢纽的大型豪华车库与满配拖车。
7. **⏱️ 世界时间流速、昼夜跳跃与天气环境切换**：
   - `g_set_time <HH:MM>` (如 `g_set_time 14:00` 瞬间变为万里无云正午时光，打光截图极为通透)；
   - `g_set_weather 0` (消除暴雨大雾天，保持路面最高抓地力)。
8. **🚗 交通流密度自由调控 (`g_traffic`)**：
   - `g_traffic 0`：瞬间清空全高速公路与市区所有 AI 堵车车辆，享受畅通无阻的个人包场驾驶；
   - `g_traffic 5`：调高车流密度，体验极致真实的晚高峰长龙车阵挑战。

---

## ⚠️ 欧卡 2 与拟真模拟器控制台启用 SOP
1. **必须在 `config.cfg` 中开启双参数**（位于 `%UserProfile%\Documents\Euro Truck Simulator 2\config.cfg`）：
   ```text
   uset g_developer "1"
   uset g_console "1"
   ```
2. **F9 投送高度防翻车**：使用 `0` 键自由视角传送卡车时，**摄像机距离地面必须保持 1-2 米低空**！若在数百米高空按 `F9`，卡车自由落体砸地会导致底盘瞬间 100% 报废全损！
