# 组件库与设计 GitHub 地图 — Component Libraries

> 元素级需求的**代码落地层**：当需求从「设计参考」推进到「实现」时按此匹配。2026-10-29 经 GitHub API 逐库验证（star 数与最近推送），网站分发的库以预览地址为准。选择顺序：技术栈匹配 → 元素覆盖 → 许可。

## 元素覆盖矩阵

| 库 | 预览/文档 | 技术栈 | 导航 | Hero | 页脚 | CTA/定价 | 动效 | 许可 |
|---|---|---|---|---|---|---|---|---|
| [shadcn/ui](https://ui.shadcn.com) | ui.shadcn.com | React+Tailwind+Radix | ✅ blocks | ✅ | ✅ | ✅ | 基础 | MIT |
| [HeroUI](https://www.heroui.com) | heroui.com | React/Next.js | ✅ | ✅ | ✅ | ✅ | 基础 | Apache-2.0 |
| [daisyUI](https://daisyui.com) | daisyui.com | 纯 CSS（框架无关） | ✅ | ✅ | ✅ | ✅ | 基础 | MIT |
| [HyperUI](https://www.hyperui.dev) | hyperui.dev | 纯 Tailwind 类（复制即用） | ✅ | ✅ | ✅ | ✅ | — | MIT |
| [Flowbite](https://flowbite.com) | flowbite.com | Tailwind+任意 JS | ✅ | ✅ | ✅ | ✅ | 基础 | MIT（组件） |
| [Preline UI](https://preline.co) | preline.co | Tailwind+Headless | ✅ | ✅ | ✅ | ✅ | 基础 | 组件 MIT |
| [TailGrids](https://tailgrids.com) | tailgrids.com | HTML/React/Vue+Tailwind | ✅ | ✅ | ✅ | ✅ | — | MIT（60+ 免费区块） |
| [Park UI](https://park-ui.com) | park-ui.com | Ark UI+Panda（多框架） | ✅ | — | — | 部分 | 基础 | MIT |
| [Magic UI](https://magicui.design) | magicui.design | React+Tailwind+Motion | — | ✅ | — | ✅ | ✅ 专精 | MIT |
| [Motion Primitives](https://motion-primitives.com) | motion-primitives.com | React 动效原语 | — | — | — | — | ✅ 专精 | MIT |
| [Meraki UI](https://merakiui.com) | merakiui.com | HTML/React/Vue，支持 RTL | ✅ | ✅ | 部分 | 部分 | — | MIT |
| [Aceternity UI](https://ui.aceternity.com) | ui.aceternity.com | React+Tailwind | — | ✅ | — | — | ✅ 专精 | MIT |
| [uiverse](https://uiverse.io) | uiverse.io | 社区组件（HTML/CSS） | 部分 | — | — | 按钮✅ | ✅ | 逐组件署名 |
| [Tailwind UI](https://tailwindui.com) | tailwindui.com | React/HTML 官方出品 | ✅ | ✅ | ✅ | ✅ | ✅ | **付费** |

## 选型规则

- **要"复制类名就用"**（无 JS 依赖）：HyperUI > TailGrids > daisyUI > Meraki UI
- **React 项目要设计系统级完整性**：shadcn/ui（生态最大 ★126k）> HeroUI > Park UI
- **动效/高级感**：Magic UI、Aceternity UI、Motion Primitives（三者常组合使用；克制原则下每页选 1–2 处）
- **后台/仪表盘**：shadcn/ui blocks（sidebar/dashboard 模板）+ Preline
- **RTL/多语言**：Meraki UI
- **商业项目预算内**：Tailwind UI（官方维护，块最全）
- 许可红线：uiverse 组件保留原作者署名要求；Tailwind UI 付费不可转售。

## 维护协议

- 快照：2026-10-29。任何条目链接失效或用户报告质量下降时：先 GitHub API 复核该库（star/推送/许可），再决定降级或替换，并在本文件更新快照日期。
- 深度调研入口：GitHub Topics `ui-components` / `component-library` / `tailwindcss` 按最近更新+star 筛选；新库入选标准与 designeer 一致——craft、utility、clarity、relevance。
