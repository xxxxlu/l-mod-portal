# 安全问题报告 / Security Policy

发现安全问题（例如后台鉴权绕过、接口越权、数据泄露）时，请**不要**开公开 Issue。

请在本仓库的 **Security → Report a vulnerability** 私密提交。写清楚：

- 受影响的地址或接口；
- 复现步骤；
- 可能的影响。

我们会尽快确认和修复，修好之前请不要公开细节。

---

Please do **not** open a public issue for security problems (auth bypass, broken access control, data exposure, etc.).
Report them privately via **Security → Report a vulnerability** in this repository, with the affected URL or endpoint, steps to reproduce and the impact.
Please keep the details private until a fix is released.

## 范围 / Scope

- 线上站点 `lmod-vault.pages.dev` 和 GitHub Pages 镜像；
- `functions/` 下的接口、站长后台（`/admin`）。

站点上链接到的第三方修改器、Mod、工具不在范围内，请直接联系对应作者。
Third-party trainers, mods and tools linked from the site are out of scope; please contact their authors.
