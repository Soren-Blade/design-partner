# 设计系统文档写作：组件文档页 / 信息架构 / 版本化 / 治理

> 快照 2026-11-05 · 每日升级 #17（v20 → v21）
> 取源全部为官方原文、上游仓库源码或 GitHub REST API 实测：GOV.UK Design System 组件页源文件 `alphagov/govuk-design-system/src/components/button/index.md` 与 Contribution criteria、USWDS `uswds-site/_data/lifecycle-phases.yml` + `lifecycle-status.yml`、Carbon `docs/guides/versioning.md`、Diátaxis 四象限原文、Docusaurus 3.10.2 Versioning、Keep a Changelog 1.1.0、SemVer 2.0.0 全 11 条、Storybook Autodocs / MDX / Doc Blocks 官方文档、DTCG Design Tokens Format Module 2025.10（含 drafts 与 published 两条路径辨析）、Google developer documentation style guide（About / Highlights）、Figma Code Connect 帮助中心、NN/g Design Systems 101（2026-08-27 复审）。
> 使用时机：① 要建/重写一个设计系统站点或组件文档页；② 现有文档"只有截图和 API 表，没人看"；③ 组件库发版、废弃、迁移，要把变更写清楚；④ 文档数值与代码对不上、文档长期不更新；⑤ 要写设计系统的贡献规范与治理规则。

## 0. 与既有资产的分层（先判读哪一份，别读错）

| 文件 | 回答的问题 | 本文件不重复什么 |
|---|---|---|
| `design-md-format.md` | **一份 DESIGN.md 该写哪九章**（给 AI / 给单个项目的约束清单） | 不重列九章骨架与 54 品牌 DNA |
| `handoff-collaboration.md` | **设计稿怎么交给开发**（spec sheet 9 字段、标注、走查、SemVer 11 条、DTCG 管线） | 不重讲设计走查与标注；SemVer 表格只在本文做「文档侧」引用 |
| `knowledge-map.md` | **一个人该按什么顺序学**（L0→L4） | 不做学习路径 |
| **本文件 `design-system-docs.md`** | **设计系统站点本身怎么写、怎么组织、怎么保持不腐**（信息架构 / 组件页 / 文档版本化 / changelog / 治理 / 新鲜度） | — |

一句话分层：**DESIGN.md 是给机器读的约束，`design-system-docs.md` 是给人读的系统**。`handoff-collaboration.md` 的终点是"开发能做出第二个页面"，本文件的终点是"半年后第三个团队也能自己查到、自己改对、自己升级"。

---

## 1. 判层：先分清你要写的是哪一种设计系统文档（Diátaxis 四象限）

最常见的失败不是写得不好，是**把四种文档混在一页里**：一个组件页里既塞入门教程、又塞 props 表、又夹一段"我们为什么这样设计"，结果谁都找不到自己要的东西。

**Diátaxis**（官方文档原话：*"A systematic approach to technical documentation authoring"*）把文档按两根轴切成四象限，识别出四种不同需求与四种对应形式：**tutorials / how-to guides / technical reference / explanation**。

| 象限 | 读者状态 | 义务（原文口径） | 在设计系统里对应 | 绝对不能写进去的东西 |
|---|---|---|---|---|
| **Tutorials 教程** | at study（在学习） | *"to provide a successful learning experience"*；**learning-oriented** | 快速上手、第一个页面、从零搭一套主题 | 分支、可选方案、API 全表；教程**不给选择**（*"It doesn't offer choices or alternatives"*） |
| **How-to guides 操作指南** | at work（在干活） | *"to help the user accomplish a task"*；**task-oriented** | 「如何给表格加批量操作」「如何把 v2 升到 v3」「如何接入暗色」 | 教学铺垫、概念解释；可假设读者已熟悉工具，但**必须准备意外**（*"a how-to guide will typically fork and branch"*） |
| **Reference 参考** | at work（在查） | 工作时应用知识；*"If it's boring and unmemorable it's probably reference"* | props / token / 断点 / 色板 / API 全表 | 大段"为什么"；Diátaxis 明确警告：参考里把示例展开成解释，会**同时毁掉参考和解释** |
| **Explanation 解释** | at study（在理解） | 离开工作后想弄清楚；*"if you can imagine reading something in the bath"* | 设计原则、为什么禁用 disabled 按钮、暗色的证据链、ADR 决策记录 | 步骤、指令、可复制的操作序列 |

**两根轴的判据（Diátaxis 原文）**：一根是 **study ↔ work**（技能获取 vs 技能应用），一根是 **practical ↔ theoretical**（做 vs 知道）。分不清时问一句：*"is this something someone would turn to while working… or once they have stepped away from the work?"*

**三条硬纪律（原文可验证）**：
1. **教程 ≠ 入门版操作指南**。Diátaxis 说这是"*the single most common conflation made in software product documentation*"。教程在**受控环境**里消除意外（*"eliminates the unexpected"*）、责任在老师、路径只有一条、必须安全可重来；操作指南在真实世界、必须预告分支、责任在用户、常常只有一次机会。
2. **基础 ≠ 教程，进阶 ≠ 操作指南**。原文专门用"资深麻醉师参加困难新生儿插管课程"反驳：区分只看**读者当时是在学还是在干**，不看难度。
3. **参考和解释不要在一段里共生**。参考里加解释会让表格被岔开，解释里塞表格又展开不充分。

**落到设计系统目录**（推荐，四象限各一根，不要合并）：

```
/get-started/         教程   → 5 分钟装好并跑出第一个按钮（只有一条路）
/guides/              操作   → 「接入暗色」「升级到 v3」「多品牌注入」（可分支、可失败处理）
/components/          组件页 → 混合页，但内部按 §2 九段式固定分区（见下）
/tokens/ /api/        参考   → 纯表：名称·值·类型·@deprecated·版本
/principles/ /adr/    解释   → 为什么、证据、备选与否决理由
```

**判断规则**：`组件页` 是唯一允许混合的文件，因为它是"任务入口"；但混合必须靠**固定分区**约束，不能靠作者自觉。

---

## 2. 组件文档页九段式：GOV.UK 逐节拆解（最经得起检验的模板）

GOV.UK Design System 的 Button 页是全球被抄最多的组件文档结构。直接读其源文件 `src/components/button/index.md`，可逐字核对，**不是二手总结**。

### 2.1 源文件 frontmatter（7 个字段，一个都不能少）

```yaml
---
title: Button
description: Use the button component to help users carry out an action
section: Components
aliases:
discussionId: 6094
layout: layout-pane.njk
---
```

| 字段 | 作用 | 为什么必须有 |
|---|---|---|
| `title` | 组件唯一名 | NN/g：*"Component name: a specific and unique UI component name, to avoid miscommunication between designers and developers"* |
| `description` | 一句话说明「帮用户完成什么」 | 不是"一个可点击的按钮"，是**用途**；搜索引擎与列表页直接用 |
| `section` | 归档层级（Components / Patterns） | 组件与模式必须分开（见 §4） |
| `aliases` | 旧名/俗称重定向 | 改名不制造 404 |
| `discussionId` | 关联公开讨论串 | **把「Help improve」变成可点击的真实入口**，不是摆设 |
| `layout` | 渲染模板 | 内容与呈现分离 |

### 2.2 正文九段（按源文件与渲染页逐节对照）

| # | 段落 | 必须回答 | GOV.UK 原文里的做法 |
|---|---|---|---|
| 1 | **首个可交互实例**（在 H1 之后、任何文字之前） | 「长什么样、能点吗」 | 用 `example()` 宏同时给出 **HTML + Nunjucks** 两个 tab，并支持 "Open this example in a new tab" |
| 2 | **When to use this component** | 什么场景该用 | 只一句：`Use the button component to help users carry out an action like starting an application or saving their information.` |
| 3 | **How it works**（含 N 个 H3 变体/状态） | 怎么用、有哪些变体 | Button 页有 **8 个 H3**：Default / Start / Secondary / Warning / Buttons on dark backgrounds / Disabled / Grouping / 防止重复提交 |
| 4 | **每个变体的「为什么」与禁令** | 什么时候不该用 | 如 `Avoid using multiple default buttons on a single page`、`Only use warning buttons for actions with serious destructive consequences that cannot be easily undone` |
| 5 | **可访问性硬数值写进正文** | 边界条件 | `the white button and background colour must have a contrast ratio of at least 4.5:1 to meet WCAG 2.2 success criterion 1.4.3`；且"不只靠红色传达危险" |
| 6 | **代码 tab 成对给出** | 复制就能跑 | 每个例子 `HTML` / `Nunjucks` 双 tab，`data-prevent-double-click` 这类开关必须给具体属性名与值 `true` |
| 7 | **Research on this component** | 有什么证据 | `Testing on GOV.UK has shown that using green as the colour of start buttons improved click-through rates`（并链到 discussion 具体评论） |
| 8 | **Recent changes**（渲染层追加） | 最近改了什么 | 表格三列 **Date / Changed / Description**；逐条带版本与链接：`Jul 2026 GOV.UK Frontend v6.4.0`…`Apr 2023 v4.6.0` |
| 9 | **Help improve this component / Need help?** | 谁负责、怎么反馈 | 两条：参加 GitHub 讨论分享研究、直接在 GitHub **propose a change**；再给联系团队的兜底 |

### 2.3 九段里最常被漏掉的是 7/8/9 —— 而它们才是"活文档"的原因

多数设计系统只有 1–6（实例 + 用法 + 变体 + props），于是半年后没人敢信它：

- 没有 **Research**：所有"最佳实践"都是无来源的主张，评审时谁嗓门大听谁的。
- 没有 **Recent changes**：用户不知道自己的版本对应哪一版文档，发版即失配。
- 没有 **Help improve**：文档没有 owner，也没有反馈回路，错误会永久留存。

**结论（给立场）**：一个组件页如果只能保留五段，保留 **When to use / When not to use / How it works / Research / Recent changes**，而不是保留 props 表。props 表可以由代码自动生成（见 §14），判断与证据不能。

---

## 3. 五问验收 + 组件页字段清单（能打分才算规范）

### 3.1 五问（缺一即判该组件文档「未完工」）

| 问 | 对应段落 | 不合格的典型表现 |
|---|---|---|
| **用不用？** | When to use | 只有一句"这是一个 X 组件"的同义反复 |
| **什么时候不用？** | When not to use / 变体禁令 | 全篇没有 "avoid / only / do not"；用户把 warning button 当普通按钮用 |
| **怎么用？** | How it works + 代码 | 只有截图没有可复制代码；或代码缺 import / 缺依赖版本 |
| **边界态与例外？** | 变体 H3 + a11y 数值 | 没写禁用态、错误态、空数据、暗底、超长文案、键盘与读屏 |
| **凭什么这么说？** | Research + Recent changes | 没有研究、没有版本、没有负责人 |

**可量化的最低门槛**：一个组件页至少 **1 个可交互实例 + 2 段判断（use / not use）+ 3 个状态或变体 + 1 条带出处的证据 + 1 条带日期的变更记录**。低于此不要标 `stable`（见 §9）。

### 3.2 NN/g 的六字段（与九段式的映射）

NN/g *Design Systems 101*（2021-04-11 发布，2026-08-27 复审）列出组件库除视觉示例外**必须包含**：

| NN/g 字段 | 原文要点 | 落在本模板 |
|---|---|---|
| Component name | specific and unique，避免设计/开发误沟通 | frontmatter `title` + `aliases` |
| Description | 是什么 & 通常怎么用，附 do's and don'ts | §2.2 段 2/3/4 |
| Attributes | 可自定义的变量：color / size / shape / copy | §2.2 段 3 的变体 + §14 Controls |
| State | recommended defaults 及后续外观变化 | §2.2 段 3/5 的 9 态 |
| Code snippets | 实际代码；"some design systems go as far as sharing multiple examples and offering a sandbox" | §2.2 段 6 + §14 Storybook |
| Front-end & backend frameworks | 避免不必要的调试 | 代码 tab 按框架分，不混写 |

**NN/g 还给了两条治理级判断**（本轮重点引用）：
- 不建设计系统的理由第 2 条：*"It takes time to teach others how to use the design system… needs instructions for use — otherwise there is a risk that it may be applied inconsistently or incorrectly"* → **文档不是附属品，是采纳的前提**。
- 团队最小编制：*"at a minimum, the team should include 1 interaction designer, 1 visual designer, and 1 developer"*，理想再配 part-time researcher / architect / **content writer**，并建议争取 executive sponsor。→ 没有内容写手，组件页通常止步于第 6 段。
- 警告：*"When poorly implemented and maintained, design systems can become unwieldly collections of components and code"*。文档腐化的终点就是"没人敢删的组件坟场"。

---

## 4. 信息架构：目录、命名、链接、检索（文档写作的四条地基）

| 规则 | 具体做法 | 依据 / 反例 |
|---|---|---|
| **组件与模式分目录** | `/components/` 放单个元素，`/patterns/` 放元素组合与页面流程（如 Check answers / Start using a service） | NN/g 明确区分 *component libraries*（单个 UI 元素）与 *pattern libraries*（ groupings or layouts），"often used synonymously; however, there is a distinction" |
| **四象限各一根目录** | `/get-started`（教程）`/guides`（操作）`/components`+`/tokens`+`/api`（参考+入口）`/principles`+`/adr`（解释） | §1 Diátaxis；混在一页是最高频失败 |
| **标题用 sentence case** | `When to use this component`，不是 `When To Use This Component` | Google style guide Highlights：*"Use sentence case for document titles and section headings"*；GOV.UK 组件页逐字遵守 |
| **链接文字要可独立理解** | 写 `see the Button component`，不写 `click here` | Google Highlights：*"Use descriptive link text"*；也是 WCAG 2.4.4 的要求（见 `accessibility.md`） |
| **文档间链接写文件路径，不写死 URL** | `[Tutorial](../getting-started/tutorial.mdx)`、带 `.md/.mdx` 后缀 | Docusaurus 原文：构建时按当前版本重写为正确 URL；写死 URL 会在切版本后指向错版本 |
| **绝对路径 import 用 `@site` 别名** | `import Foo from '@site/src/components/Foo'`，不写 `../src/components/Foo` | Docusaurus 原文：*"Don't use relative paths import within the docs. Because when we cut a version the paths no longer work"* |
| **图片按是否随版本变化分放** | 随版本：放 doc 目录用相对路径 `./myImage.png`；全局：放 `/static` 用 `/myImage.png` | Docusaurus Versioning 原文规则 |
| **每个页面可链接、可锚定** | 版本与小节都要能链接（Keep a Changelog 指导原则第 4 条） | `## [Unreleased]`、版本号带 tag 比较链接 |

**中文场景补充**：中文组件页常见「一句英文术语 + 三种中文译法」。`ux-writing.md` 的术语表规则在此同样适用——**建一张文档术语表**，同概念同词（variant ≠ 变体 ≠ 样式 ≠ 状态），并在 frontmatter 的 `aliases` 里收口语别名（"气泡""轻提示"→ toast）。别名只影响检索，不改路由（与本技能 `memory/aliases.json` 同构）。

---

## 5. 文档写作规范：Google 三条参考层级 + 可直接执行的清单

Google developer documentation style guide（About 页）给出的**参考优先级**是设计系统文档最该照抄的治理结构：

1. **Project-specific style**（项目自己的规范，含术语与例外）
2. **This style guide**（通用技术文档规范）
3. **Third-party references**：拼写 → Merriam-Webster；非技术文体 → *Chicago Manual of Style* 17th；技术文体 → **Microsoft Writing Style Guide**

并附一句 Orwell 的破例授权：*"Break any of these rules sooner than say anything outright barbarous"* —— 但要求**偏离时全文一致**。

**可执行清单（Highlights 页逐条）**：

| 类别 | 规则 |
|---|---|
| 语气 | conversational and friendly 但不轻浮；**不预告未来**（"Don't pre-announce anything"）；为无障碍与全球受众写 |
| 人称 / 语态 | **第二人称 "you" 而非 "we"**；**主动语态**；条件写在指令前（*"Put conditions before instructions, not after"*） |
| 标题 | **sentence case**；文档标题与章节标题一律 |
| 列表 | 有顺序用**编号**，其余用**项目符号**，成对数据用**描述列表**；用 serial comma（牛津逗号） |
| 格式 | 代码相关文字用等宽；**UI 元素加粗**；日期用无歧义格式 |
| 图片 | 必须有 alt text；尽量高分辨率或矢量 |
| 链接 | descriptive link text，禁 "click here" |

**中文适配（本技能给出的落地口径，非 Google 原文）**：
- 第二人称用「你」，不用「我们/本系统」；主动语态 =「点击保存后，页面显示成功提示」而非「成功提示将被显示」。
- 条件前置 =「**如果**表单里有未保存内容，先弹出确认框，再离开页面」，不写成「离开页面前弹出确认框（当有未保存内容时）」。
- sentence case 对中文不适用，但**中英混排的章节标题**里英文部分仍用 sentence case（`When to use 组件`），且不加句号（见 `ux-writing.md`）。
- 术语表中英对照写一次，正文不再反复括号注释；UI 元素名用 `code` 或加粗，与 Google 的 bold 口径对齐。
- 句长沿用 `ux-writing.md`：中文 ≤30 字、英文 ≤20 词；长句拆成「条件 + 动作 + 结果」三行。

---

## 6. 示例代码的可抄性：五条硬规则（写错就没人用）

GOV.UK 每个例子都给 **HTML + Nunjucks 双 tab + 新窗口打开**；NN/g 更进一步要求 code snippets 与框架说明。合成本技能的验收口径：

1. **可直接复制运行**：包含完整 import、必需包裹元素、必需属性；不出现 `...`、`// 省略`、`your-token-here` 之外的占位。
2. **一个例子只演示一件事**：GOV.UK 把「默认」「start」「secondary」「warning」「dark background」「disabled」「grouping」「prevent double click」拆成 8 个独立例子，每例配一段"何时用/何时不用"。
3. **多实现形态并列**：设计侧标记语言与代码侧实现分 tab，不混在同一个代码块里；多框架时按框架切 tab（Figma Code Connect UI 支持一个设计组件映射多个框架实现，见 §15）。
4. **例子与代码库同源**：最好由 story / 示例文件渲染（§14），而不是人在 Markdown 里手抄一份 —— 手抄必然漂移。
5. **例子里的数值要能追溯到规范**：如 `4.5:1` 要写清来自 WCAG 2.2 SC 1.4.3；`data-prevent-double-click="true"` 要说明「仅前端防重复，服务端仍需防重放」（GOV.UK 原文明确补了这句）。

**反例判据**：复制示例到新项目报错 → 该组件文档的"代码"部分判 0 分，哪怕设计说明写得再漂亮。

---

## 7. 完整填充范例：一个可直接复制的组件文档页（Button 精简版）

> 下面是**模板骨架**，不是给某个具体组件库的规范值。方括号处必须替换；带 ⚠️ 的是最常被漏掉的字段。把这一段存成 `components/button.md` 即可作为新组件页的起点。

```markdown
---
title: Button 按钮
description: 让用户执行一个明确的动作，例如提交表单或开始一项服务
section: Components
aliases: [btn, 按钮组件]          # ⚠️ 改名不制造 404
status: stable                    # ⚠️ 见 §9，experimental 不得对外宣称为可用
owner: design-system-team         # ⚠️ 没有 owner 的页面必然腐化
discussionId: 6094                # ⚠️ 关联公开讨论串
lastReviewed: 2026-11-05          # ⚠️ 新鲜度见 §17
since: 1.0.0
---

> 可交互示例（H1 之后第一屏，不要先写三段介绍）
<!-- 同时给出 HTML / 框架组件 两个 tab；支持「在新标签页打开」 -->

## When to use this component 什么时候用
用 Button 让用户执行一个动作，例如「保存」「继续」「开始申请」。
一句话写**用途**，不要写「这是一个可点击的按钮」。

## When not to use 什么时候不用
- 跳转到另一个页面且不需要提交数据 → 用链接（GOV.UK：start button 通常用 `<a>` 而非 `<button>`）
- 一页出现多个主按钮 → 先简化页面或拆分步骤
- 危险且不可撤销的操作 → 用 warning 变体，并在最终确认步才使用；**不能只靠红色传达危险**

## How it works 怎么用
- 文案用 sentence case、动词开头、描述动作结果（见 `ux-writing.md`）
- 主按钮左对齐到表单左边缘
- 全篇最多两种字重、两种圆角；尺寸只用 token

### Default 默认
<!-- 示例 + 代码 tab -->
一页只放一个主按钮。

### Secondary 次要
<!-- 示例 + 代码 tab -->
次要动作过多时，先简化页面再考虑加按钮。

### Warning 危险
<!-- 示例 + 代码 tab -->
只用于「永久删除账号」这类**不可轻易撤销**的操作。

### Disabled 禁用 ⚠️
禁用态对比度差且易造成困惑 —— **仅当研究证明它让界面更好懂时才用**
（GOV.UK 原文立场；本技能 `form-table.md` 有主按钮禁用 <3 / >5 规则）。

### 暗色背景 ⚠️
白按钮与背景必须 ≥ 4.5:1（WCAG 2.2 SC 1.4.3 AA）。

### 状态矩阵 ⚠️
| 状态 | 视觉 | 键盘 | 读屏 |
|---|---|---|---|
| default / hover / focus-visible / active / disabled / loading |
（9 态矩阵见 `handoff-collaboration.md`；焦点三层标准见 `accessibility.md`）

## Props / API 参考
<!-- 纯表，禁止在此写「为什么」；由代码生成，见 §14 -->
| 名称 | 类型 | 默认值 | 说明 | 版本 |
|---|---|---|---|---|

## Accessibility 可访问性
- 焦点环对比度 ≥ 3:1（SC 1.4.11）；目标尺寸 ≥ 24×24（SC 2.5.8）
- 图标按钮必须有 aria-label 且与可见文案一致
- 加载态用 `aria-live` 播报，不新增焦点

## Research on this component 研究证据 ⚠️
| 日期 | 结论 | 出处 |
|---|---|---|
| 2026-07 | 绿色 start button 提高点击率 | GOV.UK discussion #6094（链接） |
（没有研究就写「暂无研究，欢迎在讨论串补充」，**不要编**）

## Recent changes 近期变更 ⚠️
| Date | Changed | Description |
|---|---|---|
| 2026-07 | v6.4.0 | 修复 start button 内嵌 HTML 的文字间距 |
| 2026-02 | v6.0.0 | **BREAKING** 移除 `element` 参数；按钮默认 `<button>` |

## Help improve this component 帮助改进 ⚠️
- 在讨论串分享你的研究：#6094
- 直接对本页提修改：编辑 `components/button.md`
- 找不到答案：联系 design-system-team
```

**填表纪律**：`⚠️` 的字段全部是"文档会腐化"的护栏。一个团队如果只肯填一半，宁可把 `status` 标成 `experimental`（§9），也不要用 `stable` 制造虚假承诺。

---

## 8. 活文档四件套：研究 / 已知问题 / 近期变更 / 帮助改进（证据与反馈闭环）

| 段 | 内容 | 失败模式 | Minimum Viable 写法 |
|---|---|---|---|
| **Research on this component** | 可用性测试、A/B、真实数据、讨论串结论 | 写「遵循最佳实践」却无出处 | 一条带日期 + 结论 + 可点链接；没有就明说「暂无」 |
| **Known issues / Use with caution** | 已知限制、浏览器/读屏器缺陷、未覆盖场景 | 只报喜不报忧，用户踩坑后不再信任 | 列 1–3 条，注明影响范围与 workaround |
| **Recent changes** | Date / Changed / Description 三列表格 | 只在 CHANGELOG 里写，组件页不写 → 用户看的是旧页 | 每个影响该组件的版本写一行，BREAKING 加粗 |
| **Help improve / Need help** | 讨论串、编辑入口、联系人 | 只有一个 `feedback@example.com` 死邮箱 | 三个入口：讨论 / 直接改文件 / 找团队 |

**GOV.UK 把它做成了产品机制而不是文案**：`discussionId` 是 frontmatter 字段，`Help improve` 直接给 GitHub 讨论串与 `propose a content change using GitHub` 指南，`Recent changes` 由版本数据渲染。也就是说**反馈路径是结构化数据，不是一段礼貌用语**。

**三条可验证结论**：
1. **证据可以很短**。GOV.UK 的 Research 只有一句 `Testing on GOV.UK has shown that using green as the colour of start buttons improved click-through rates` + 讨论串链接。写不出长报告不是不写的理由。
2. **变更记录要精确到版本与破坏性**。GOV.UK `Recent changes` 里 `v6.0.0 Removed element Nunjucks parameter` 这行，同时给出了"哪个版本 / 什么被删 / 影响什么"；用户升级时不需要去翻 CHANGELOG。
3. **状态是可回退的**。USWDS 的 `Use with caution` 明确定义为「组件未能满足 accessibility / usability / development requirements」时的中间态，可回到 stable 或走向 deprecation（§9）——文档必须允许自己说"这个组件现在别用"。

---

## 9. 组件文档状态与成熟度（USWDS 生命周期 + Carbon semver 对照）

### 9.1 USWDS 三阶段 / 十二子状态（读 `_data/lifecycle-phases.yml` 源码所得）

USWDS 把组件状态存在 `_data/lifecycle-status.yml`（`status_major` + `status_minor` 两个字段），阶段定义存在 `_data/lifecycle-phases.yml`。这是**状态数据化**的范例：文档页不手写徽章，从数据渲染。

| 阶段 Phase | 子状态 Subphase | `starts_when` → `ends_when`（原文要点） |
|---|---|---|
| **Proposal 提案** | Discussion started | 任何人发起讨论 → 核心团队开始起草提案 |
| | Proposal in progress | 团队起草 → 完整提案公开征求最终反馈 |
| | **Proposal open for comment** | **社区有最少 45 天评论期**（原文：*"The community has a minimum of 45 days to comment on the complete proposal."*）→ 评论期关闭、团队评估 |
| | Proposal evaluation | 团队开始评估 → 公布决定 |
| | Approved / Conditionally approved | 批准 → 分配开发 / 依赖工作完成 |
| | Returned for revision / Will not pursue | 退回修改 / 不做 |
| **Development 开发** | Assigned | 分配给团队 → 开发开始 |
| | In development | 开发已启动 → 组件可发布 |
| **Released 已发布** | **Experimental** | 组件可发布 → *"fully tested, documented, and has an established history in production"* |
| | **Stable** | *"passes all tests and is fully documented"* → 转为 use with caution 或 deprecation |
| | **Use with caution** | 未满足 accessibility / usability / development 要求 → 回 stable 或转 deprecated |
| | **Deprecated** | 核心团队停止维护 → 从代码库移除 |
| | **Retired** | 终态 |

**最值得抄的一条**：`Stable` 的准入门槛原文是 **"passes all tests and is fully documented"**——**文档完整是 stable 的硬条件，不是加分项**。本技能 §3.1 的五问验收就是把它变成可打分的检查表。

补充：45 天评论期是**下限**，不是建议值；`status_major/status_minor` 双字段让列表页能按阶段筛选，比一个自由文本 badge 可靠。

### 9.2 Carbon 把"什么改动算什么版本"做成了可查表（源码 `docs/guides/versioning.md`）

Carbon 直接引用 SemVer 三段定义，并给出 `@carbon/react` 的**逐改动类型版本表**：

| 改动类型 | semver bump |
|---|---|
| 组件 typings / definitions 变更 | `patch`（表中）※ |
| 新增 prop | `minor` |
| 标记某 prop 为 deprecated | `minor` |
| 移除已有 prop | **`major`** |
| prop 类型变得更具体（收窄） | **`major`** |
| prop 类型变得更宽泛（放宽） | `minor` |
| `PropTypes.func` 参数**改变** | **`major`** |
| `PropTypes.func` 参数**增加** | `minor` |
| `PropTypes.func` 参数**减少** | **`major`** |
| `id` / `aria-label` 对应的 DOM 节点改变 | 文档目录列入专节说明 |

※ **Carbon 自身存在一处口径不一致**（原文照录，供评审时引用）：Overview 表格把 "component typings/definitions" 标为 `patch`，但紧随其后的 Examples 小节写 `semver bump: **minor**`，并解释 *"Typescript definitions … are provided on an as-is basis and are not bound to semver… Breaking changes may happen across patch or minor versions"*。**裁决：不要把 TS 类型变更当成有版本保证的 API；文档里应显式写出这条免责。** 这也是"文档必须敢写自己的例外"的例证。

**状态 → 文档的映射规则**：`experimental` 页必须在页首写「API 可能变更、不建议生产使用」；`deprecated` 页必须写「替代组件 + 迁移步骤 + 移除版本」；`use with caution` 页必须写「具体哪一条要求未满足」。状态变了，页面必须跟着变，否则状态字段就是谎言。

---

## 10. 文档版本化（Docusaurus 3.10.2 官方规则 + SemVer 对接）

### 10.1 先问"要不要版本化" —— 官方立场是否定的

Docusaurus Versioning 原文三条警告（逐字）：

> *"Think about it before starting to version your documentation - it can become difficult for contributors to help improve it!"*
> *"Most of the time, you don't need versioning as it will just increase your build time, and introduce complexity to your codebase."*
> *"Versioning is best suited for websites with high-traffic and rapid changes to documentation between versions. If your documentation rarely changes, don't add versioning to your documentation."*

**结论**：只有当「流量高 + 版本间文档差异大 + 用户确实停在旧版本」三条同时成立才版本化。多数设计系统（一个组件库一条主线）**不需要**多版本文档，一个 `Recent changes` 表 + 一份 CHANGELOG 就够（GOV.UK 正是这么做的）。

### 10.2 需要版本化时的精确规则

| 项 | 精确值 / 配置 | 说明 |
|---|---|---|
| Current version | `./docs` 目录 | 由**文件系统位置**定义，默认标签 `Next`、URL `/docs/next/*` |
| Latest / last version | 默认 `/docs` | 由**导航行为**定义，与 current 可以不同 |
| 冻结快照 | `versioned_docs/version-[versionName]/` | `npm run docusaurus docs:version 1.1.0` 时自动复制 `docs/` |
| 冻结侧栏 | `versioned_sidebars/version-[versionName]-sidebars.json` | 自动生成 |
| 版本清单 | `versions.json`，**newest → oldest** | 手工删除版本从这里开始 |
| 建议保留版本数 | **< 10**（*"try to keep the number of your versions below 10"*） | 超过就是「nobody even reads anymore」的陈旧文档 |
| dev / deploy preview | `onlyIncludeVersions` 限制为 **2 或 3** 个版本 | 改善 startup / build time |
| 单 major 长期维护 | `lastVersion: 'current'` + `versions.current: {label, path}` | 避免同时维护 `./docs` 和 `./versioned_docs/version-1.0.0` 两份 |
| banner | `'none' / 'unreleased' / 'unmaintained'` | 高于 latest 视为 unreleased，低于视为 unmaintained |
| 关闭版本化 | `disableVersioning: true` | 有版本数据也只显示 current |
| 隐藏未完成 current | `includeCurrentVersion: false` | current 是 WIP 时 |

**PATCH 不要切文档版本**（官方原文）：包从 `1.0.0` 修到 `1.0.1`，*"Should you cut a new documentation version 1.0.1? **You probably shouldn't**"*，理由是 *"1.0.1 and 1.0.0 docs shouldn't differ according to semver because there are no new features!"* → 只制造重复文件。**规则：按 MINOR/MAJOR 切文档版本，PATCH 只更新 CHANGELOG 与 `Recent changes`。**

**版本化与 SemVer 的对接**（`handoff-collaboration.md` §12 已给 11 条全文，这里只列文档侧动作）：

| 变更 | SemVer | 文档动作 |
|---|---|---|
| 修文档错字、修对比度、修视觉 bug | PATCH | 更新 `Recent changes` + CHANGELOG `Fixed`；**不切文档版本** |
| 新增组件 / 新增 prop / 新增变体 | MINOR | 新组件页 + CHANGELOG `Added`；可切文档版本 |
| 标记废弃 | MINOR | **必须先有至少一个含废弃声明的 MINOR**（SemVer FAQ），组件页加 `deprecated` + 替代方案 + 移除版本 |
| 移除 prop / 收窄类型 / 改默认值 | **MAJOR** | 切文档版本 + **迁移文档**（§12）+ CHANGELOG `Removed` + `[BREAKING]` 标记 |
| 撤回的发行 | — | CHANGELOG 标 `[YANKED]`（§11） |

**归档老版本**：Docusaurus 建议把 archived versions 作为外链指向 Jamstack 提供商的 immutable URL（Jest / Docusaurus 官网自用），这些版本永不再 rebuild。

---

## 11. Changelog：Keep a Changelog 1.1.0 的七条指导原则与六类变更

> "All notable changes to this project will be documented in this file."
> "Don't let your friends dump git logs into changelogs."

**定义**（原文）：*"A changelog is a file which contains a curated, chronologically ordered list of notable changes for each version of a project."* —— **curated（经过策展）**是关键词，不是自动生成的 commit 流。

**七条指导原则（逐字）**：
1. `Changelogs are for humans, not machines.`
2. `There should be an entry for every single version.`
3. `The same types of changes should be grouped.`
4. `Versions and sections should be linkable.`
5. `The latest version comes first.`
6. `The release date of each version is displayed.`
7. `Mention whether you follow Semantic Versioning.`

**六类变更分组**：`Added` / `Changed` / `Deprecated` / `Removed` / `Fixed` / `Security`。空小节**删掉**（原文：占空间、制造噪声；用户应理解成"该版本没有这类显著变更"）。

**其余硬规则**：
- 顶部保留 `## [Unreleased]`：两个用途 —— 让人看见即将发布什么、发版时把条目搬进新版本小节。
- **日期用 ISO 8601** `2017-07-17`：原文理由是单位从大到小、不与地区格式歧义重叠，且是 ISO 标准。→ 中文团队不要写 `2026/11/5`，与 `i18n-localization.md` 的日期口径一致。
- **`[YANKED]`**：因严重 bug/安全撤回的版本**也要写进 changelog**，格式 `## [0.0.5] - 2014-12-13 [YANKED]`；方括号既醒目又便于程序解析。
- 文件固定命名 **`CHANGELOG.md`**：不要叫 `HISTORY`/`NEWS`/`RELEASES`，也不要只用 GitHub Releases（不可移植、不易发现）。
- **绝不能漏**：deprecations / removals / breaking changes。原文：*"If you do nothing else, list deprecations, removals, and any breaking changes in your changelog."*
- 别拿 commit log diff 当 changelog：commit 记源码演进步骤，changelog 记**跨多个 commit 的、对最终用户值得注意的差异**。
- **一致性即可信度**：*"A changelog which only mentions some of the changes can be as dangerous as not having a changelog"* —— 它应当是 *the single source of truth*。发现漏了 breaking change 要回去补。

**设计系统专用模板**：

```markdown
# Changelog
All notable changes to this design system will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- `Table` 新增 `stickyHeader` prop（#1234）

## [3.0.0] - 2026-11-05
### Changed
- **BREAKING** `Button` 默认 `type` 由 `submit` 改为 `button`。迁移见 `migrations/v2-to-v3.md`
### Removed
- **BREAKING** 移除 `Button` 的 `element` 参数，改用 `href` 决定是否渲染 `<a>`
### Deprecated
- `Toast` 标记废弃，请用 `Notification`；将在 4.0.0 移除
### Fixed
- 修复 start button 内嵌 HTML 的文字间距

[Unreleased]: https://github.com/org/ds/compare/v3.0.0...HEAD
[3.0.0]: https://github.com/org/ds/compare/v2.4.0...v3.0.0
```

**三个版本号要同时写清**（`handoff-collaboration.md` §12.1 的事故高发点）：设计稿版本 / 组件库 SemVer / 产品版本。文档页脚给出三者，避免「稿子写 v3、库是 2.4.0、产品是 5.1.2」。

---

## 12. 迁移文档：MAJOR 必带，且必须能被机器校验

SemVer FAQ 关于废弃的原文要求：*"When you deprecate part of your public API, you should do two things: (1) update your documentation to let users know about the change, (2) issue a new minor release with the deprecation in place. Before you completely remove the functionality in a new major release there should be at least one minor release that contains the deprecation"*。

**一份合格迁移文档的六段**：

| 段 | 内容 | 判据 |
|---|---|---|
| 适用范围 | `from v2.x → v3.0.0`，列出受影响包与版本 | 能一句话判断"我要不要读" |
| 破坏性变更清单 | 每条：旧 API / 新 API / 为什么 / 自动可改吗 | 与 CHANGELOG 的 `Removed`/`Changed` 一一对应 |
| before / after 代码 | 成对可编译代码，不是伪代码 | 复制即可运行 |
| codemod | 命令 + 覆盖哪些改动 + 哪些必须手工 | 有自动脚本时给 `npx` 命令与 dry-run 选项 |
| 逐组件映射表 | 组件名 / prop / token 的新旧对照 | 能 `grep` 到旧名 |
| 验收清单 | 迁移后跑什么（VRT / AVT / 视觉走查 / 三个版本号对齐） | 与 `handoff-collaboration.md` 回归四层衔接 |

**反模式**：只在 CHANGELOG 写一行 `Removed element prop`，把迁移成本转嫁给每个使用方；或者把迁移指南写在 Slack 置顶 / 会议纪要里（原文路径不可检索、不可版本化）。

---

## 13. Token 文档自动生成：DTCG 2025.10 把 `$description` 明确定位成文档源

### 13.1 ⚠️ 先裁决一个本技能自己引用过的 URL 口径

`handoff-collaboration.md` §13.2 与来源清单写的是 `https://tr.designtokens.org/format/`，标注「预览草稿」。本轮打开该页核对，页首状态为：

> **This is a preview.** *"Do not attempt to implement this version of the specification. Do not reference this version as authoritative in any way."*
> Draft Community Group Report, 08 September 2026
> **Latest published version: `https://www.designtokens.org/TR/2025.10/format/`**

**裁决**：`tr.designtokens.org/format/` 是**进行中的 preview draft**，不可作为权威依据引用；设计系统文档应引用 **published 2025.10**（`https://www.designtokens.org/TR/2025.10/format/`）。本文件以下条款以规范正文与 `design-tokens/community-group` 仓库为准，并明确标注 draft 带来的不确定性。这与 `handoff-collaboration.md` 的「预览草稿，不可当标准」立场一致，只是把**该引用哪条 URL**说清楚了。

### 13.2 规范里原生就有「文档工具」这一类

DTCG §3.5 原文定义 **Documentation tool**：*"A tool for documenting design tokens usage"*，并列举 **Storybook / Zeroheight / Backlight / Supernova / Knapsack**。§2 引言更直接点名文档工具的作用：*"Documentation tools can display design token names rather than the raw values in design specs and style guides."*

**这是本节最重要的一句**：规范制定者早就假定**文档展示的是 token 名而不是裸值**。所以设计系统文档里手抄 `#1677FF`、`16px` 是**架构性错误**——一旦 token 值变了，所有手写页面同时说谎。

### 13.3 能直接喂给文档生成器的字段（全部来自规范正文）

| 字段 | 规范措辞 | 文档侧用途 |
|---|---|---|
| `$description` | *"A plain text description explaining the token's purpose"*；*`MUST` be a plain JSON string* | 规范原文列出四种消费方式：**style guide generators 在视觉预览旁显示描述**、**IDE 自动补全 tooltip**、**设计工具 tooltip**、**翻译工具把描述渲染成源码注释** → 一次编写，四处复用 |
| `$type` | 未设时按「引用目标类型 → 最近父组 `$type` → 否则 invalid」解析；**`MUST NOT` attempt to guess the type** | 文档生成器据此选预览控件（色块 / 尺寸条 / 时长轴 / 贝塞尔曲线） |
| `$deprecated` | `true` / **说明字符串** / `false`（可覆盖组默认）；示例 `"Please use the border style for active buttons instead."`；规范还给出渲染成 `@deprecated {@link …}` 的示例 | 自动生成「废弃 + 替代 token + 文档链接」区块，与 §11 CHANGELOG `Deprecated` 对齐 |
| `$extensions` | *`MUST` preserve any extension data they do not themselves understand*；建议反域名键 | 放 `org.example.docs/owner`、`lastReviewed`、可视化参数等**不影响值理解的元数据** |
| Group / `$description`(组级) | 组是任意分组，工具 **`SHOULD NOT` 用组推断类型或用途** | 文档目录结构可以照组生成，但不要从组名猜语义 |
| Alias `{token}` / `$ref` | 花括号只指向**完整 token**；`$ref` 用 JSON Pointer 可指到属性；**引用环 `MUST NOT`** | 文档展示「语义 token → 原始 token → 实际值」的解析链，而不是只给一个 hex |
| dimension / duration / cubicBezier / fontWeight | `px`\|`rem`；`ms`\|`s`；四数数组且 x∈[0,1]；数值 [1,1000] 或预定义别名 | 表格渲染时按类型带单位、带校验，避免 `16` 这种无单位数值 |

**可抄的 token → 文档最小范例**（`$description` 与 `$deprecated` 均按规范正文写法）：

```json
{
  "button": {
    "$description": "Button component tokens",
    "background": {
      "$type": "color",
      "$description": "The background color for buttons in their normal state.",
      "$value": { "colorSpace": "srgb", "components": [0.09, 0.46, 1], "hex": "#1677ff" }
    },
    "background-legacy": {
      "$type": "color",
      "$value": "{button.background}",
      "$deprecated": "Please use {button.background} instead. Removed in 4.0.0."
    }
  }
}
```

### 13.4 三条落地纪律

1. **单一真源**：token 值是 `.tokens.json`，文档页由生成器渲染（Style Dictionary / Storybook doc block），**禁止在 Markdown 里复制粘贴数值**。本技能自己就是这么做的：`scripts/build_readme.py` 从 SKILL.md 与 `references/` 实时解析版本号、路由数、自检数、别名组数，避免 README 数字过期（§17）。
2. **`$description` 写用途不写值**：反例 `"蓝色 #1677FF"`（值会变）；正例 `"The background color for buttons in their normal state"`（规范原文示例）。
3. **文档与代码同一次提交**：token 变更 PR 若不带文档产物更新，CI 判失败。这是让"自动生成"真正生效的唯一办法，否则生成器会被人绕过。

---

## 14. 代码即文档：Storybook Autodocs / MDX / Doc Blocks 精确配置

NN/g 要求 code snippets 与 sandbox，DTCG 把 Storybook 列为文档工具，Storybook 官方则把 story 直接定义为文档的基础：*"When you write component stories during development, you also create basic documentation to revisit later."*

### 14.1 Autodocs：`tags: ['autodocs']`（版本相关，逐字配置）

| 作用范围 | 位置 | 代码 |
|---|---|---|
| 全项目 | `.storybook/preview.ts` 的 `preview` 对象 | `const preview: Preview = { tags: ['autodocs'] };` |
| 单组件 | `*.stories.ts` 默认导出 `meta`，与 `component` **同级** | `const meta = { component: Button, tags: ['autodocs'] } satisfies Meta<typeof Button>;` |
| 禁用组件 | `meta` | `tags: ['!autodocs']` |
| 排除单个 story | story 对象 | `tags: ['!autodocs']` |

原文规则：*"If a CSF file contains at least one story tagged with `autodocs`, then a documentation page will be generated for that component."* —— 注意触发条件是 **至少一个 story 带 tag**，不是只看 meta。

`.storybook/main.ts` 的附加选项：`docs: { defaultName: 'Documentation', docsMode: true }`（默认 `defaultName: 'Docs'`、`docsMode: false`；`docsMode` 只让侧栏显示文档页）。

**Autodocs 默认页 = 六个 Doc Block**（官方内部模板）：`Title` → `Subtitle` → `Description` → `Primary`（文件里第一个 story，带缩放控件）→ `Controls`（`args` / `argTypes`）→ `Stories`（其余 story）。元数据来自推断的 `args` / `argTypes` / `parameters`。

### 14.2 MDX：结构文档 + 可交互 JSX

官方分工原话：**CSF** *"is great for succinctly defining stories… If you use TypeScript, it also provides type safety and auto-completion"*；**MDX** *"is great for writing structured documentation and composing it with interactive JSX elements"*。

逐字示例（`Checkbox.mdx`）：

```mdx
import { Canvas, Meta } from '@storybook/addon-docs/blocks';
import * as CheckboxStories from './Checkbox.stories';

<Meta of={CheckboxStories} />

# Checkbox

A checkbox is a square box that can be activated or deactivated when ticked.

<Canvas of={CheckboxStories.Unchecked} />
```

**四个必须记住的坑（官方文档明确写出）**：
1. **`<Meta of={...} />` 必须引用 story 文件的 `full set of exports`**（`import * as XStories`），**不是组件本身**，否则生成的文档会渲染出错。
2. MDX 各 block 之间**必须留空行**：*"Failing to separate blocks by whitespace can cause (sometimes cryptic) parse errors."*
3. 省略 `<Meta>` 时，Storybook 用文件物理位置推断标题与侧栏位置，并**覆盖**已有的自动生成文档页；若你已开 `autodocs`，官方建议先移除以免报错。
4. `<Controls>` 与 `<Story>` 的已知限制：Canvas 里 anchors 会被忽略（Storybook 用 URL 追踪 args）；关掉 `inline` 渲染后，controls 不会更新文档页里的 story。

其余 Doc Blocks（官方 MDX 页确认）：`Canvas`（展示 story）、`Story`（引用单个 story，多组件页可带 `meta={...}`）、`Controls`（属性交互表）、`Markdown`（`import Readme from '../../Changelog.md?raw'` → `<Markdown>{Readme}</Markdown>`，把 CHANGELOG 直接嵌进文档站）、`Meta`（`name` 改默认 "Docs" 节点名、`title` 放到任意导航层级）。`<Guidelines>` / `<Dos>` / `<Donts>` 是任意 React 组件，**不是** Doc Block。

### 14.3 与九段式的对接表

| §2 段落 | Storybook 承载方式 |
|---|---|
| 首个可交互实例 | `<Primary />` 或 `<Canvas of={...} />` |
| How it works 变体 | 每个变体一个 named story（CSF），由 `<Stories />` 汇总 |
| Props 参考 | `<Controls />` / `argTypes`（**自动生成，别手写**） |
| 状态矩阵 | 每个状态一个 story + `play` 函数做交互断言 |
| Recent changes | `<Markdown>{Changelog}</Markdown>` 或独立 docs page |
| Research / 判断 / 禁令 | **MDX 手写**（机器生成不了判断与证据） |

**结论（给立场）**：**机器负责"值"，人负责"判断"**。props、token 值、状态截图、代码 tab 全部自动生成；`When not to use`、`Research`、`Recent changes`、禁令与取舍理由必须人写。把两者混在同一份手写 Markdown 里，就是文档漂移的起点。

---

## 15. 设计稿 ↔ 文档 ↔ 代码：Figma Code Connect 与命名一致性

`handoff-collaboration.md` 讲「标注只标例外」「Dev resources 传播到所有实例」；本节补上**设计组件与真实代码组件之间的连接层**。

Figma 官方定义：*"Code Connect is a bridge between your codebase and Figma's Dev Mode, connecting components in your repositories directly to components in your design files."* 它还把连接喂给 **Figma MCP server**，让 AI agent 拿到「实际代码引用」而不是猜组件名。

| | **Code Connect UI** | **Code Connect CLI** |
|---|---|---|
| 运行位置 | 完全在 Figma 内 | 本地仓库终端，`figma connect` 发布 |
| 适合 | 设计+工程协作、快速可视化、语言无关 | 需要精确 property mapping 与动态代码示例 |
| 能力 | 连 GitHub 仓库 **或**手工填组件路径与名称；支持**一个设计组件映射多个框架**（React / SwiftUI / Jetpack Compose / Vue 各一条） | template files（framework-agnostic）把 Figma properties 映射到生产组件 API，Dev Mode 显示**真实代码片段**而非自动生成代码 |
| 关键限制 | **UI 连接的组件不在 Inspect 面板显示代码片段**，只给文件路径/组件名与 AI 预览片段；要代码片段必须用 CLI | 官方：*"Template files are now the recommended format… Framework-specific parsers are no longer actively maintained"* |
| 权限 | Professional / Organization / Government / Enterprise 计划 + Full 或 Dev seat；连 GitHub 需文件 owner 或组织管理员，**不支持 GitHub Enterprise Server** | Professional 计划**只能有 1 个 active library + 1 个 active framework**，其余连接保留但标记 Deactivated |

**四步接入**（官方给出的组织流程）：① 规划支持的语言/框架与代码呈现方式 → ② 安装 CLI 并加配置文件 → ③ 写 template files 做 property mapping → ④ 与设计师一起在 Dev Mode 复核示例。

**对文档写作的三条硬要求**：
1. **命名必须三处一致**：Figma 主组件名 = 代码组件名 = 文档 `title`。任一处不同，Code Connect 连上也没用（NN/g 的 "specific and unique UI component name" 就是为此）。
2. **文档页脚要给出组件的代码路径**（Code Connect UI 的手动映射输入的就是这个），否则 Dev Mode 与文档站是两套信息。
3. **CLI 输出与文档示例同源**。Dev Mode 显示真实片段、文档站显示手抄片段，是最典型的"两份真相"；用同一份 story/template 渲染两边。

---

## 16. 贡献与治理：GOV.UK 的准入标准（含可量化阈值）

### 16.1 组件准入：提案 2 条 + 发布前 3 条（Contribution criteria 原文）

| 阶段 | 标准 | 要求的证据 |
|---|---|---|
| **Proposing 提案** | **Useful** | *"evidence that this component or pattern would be useful for many teams or services"*；证据可以是**不同服务里正在使用的截图或链接** |
| | **Unique** | 不重复系统里已有的东西；若要替换现有组件，须有证据证明更好 |
| **Developing 发布前** | **Usable** | *"tested in user research and shown to work with a representative sample of users, **including those with disabilities**"*；还须在**一系列浏览器、辅助技术与设备**上测过 |
| | **Consistent** | 复用已有样式/组件；**指南与示例里的文案都要遵守 GOV.UK style guide**；代码遵守 GOV.UK Frontend coding standards 且可合并 |
| | **Versatile** | 能用于多种服务（例：日期输入可只问年、问年月、问精确日期…） |

**可复制的治理动作**：提案阶段先要「多团队复用证据 + 不重复」，避免系统变成个人组件收藏夹；发布前要「含残障用户的研究样本 + 跨浏览器/读屏/设备 + 文案与代码规范 + 多场景通用性」。这五条比"PR 里附张截图"严格一个数量级，也正是 §3 五问验收的组织版本。

### 16.2 社区资源/工具准入的**七条带数值**要求（原文）

链接到设计系统的第三方资源须满足：有明确 owner；不会被误认为官方；**有文档说明如何使用、如何贡献、如何获得支持**；**support tickets 1 个月内答复**；写明支持哪个 GOV.UK Frontend 版本；**落后最新版本不超过 3 个月**；设计与开发资源与官方一致（输出相同 markup）、不收费不推广私人生意、符合 Service Standard 与 Technology code of practice。

→ 本技能给出的**文档新鲜度阈值**就取这两个官方数值：**issue 响应 ≤ 1 个月、依赖版本落后 ≤ 3 个月**（§17）。这是全仓第一次把"文档多久算过期"写成可检查的数。

### 16.3 USWDS 的公开决策节奏

`Proposal open for comment` 阶段**最少 45 天**公开评论期，状态数据存在仓库里（`lifecycle-status.yml`），而不是会议纪要。结合 NN/g 的最小团队编制（1 交互 + 1 视觉 + 1 开发，理想配 part-time 研究员/架构师/**内容写手**，并争取 executive sponsor），得到本技能的治理底线：

> **没有 owner、没有内容写手、没有公开反馈入口的设计系统文档，不要标 `stable`。**

---

## 17. 文档新鲜度与漂移：可测指标 + 本技能自身的防漂移机制（自举）

### 17.1 六项可自动检查的指标

| 指标 | 阈值 / 检查 | 来源 |
|---|---|---|
| `lastReviewed` 距今 | **> 90 天标 stale**（建议值）；上游依赖变更时立即复核 | 由 GOV.UK「落后 ≤3 个月」推导 |
| `owner` 缺失 | 直接 FAIL | GOV.UK 社区资源第 1 条 |
| issue / 反馈响应 | **≤ 1 个月** | GOV.UK 社区资源原文 |
| 依赖版本落后 | **≤ 3 个月** | GOV.UK 社区资源原文 |
| 手写数值与 token 源不一致 | CI diff，任一处 FAIL | DTCG §2「展示 token 名而非裸值」 |
| 链接失联 / 章节接线 | 全站巡检，失联 0 容忍 | 本技能 `mindmap.py` 接线体检 |

### 17.2 本技能自己就是这套机制的活样本（可直接抄架构）

`design-partner` 为了对抗自身 26+ 份参考的漂移，已经跑通四层，正好对应本文的四个论点：

| 层 | 脚本 | 防的是什么谎 | 对应本文 |
|---|---|---|---|
| **统计自动生成** | `scripts/build_readme.py` | 早期把「11 份参考 / 12 类路由 / 9 项自检 / 25 组别名」硬编码在 README 里，每轮升级都会过期 → 改为从 `SKILL.md` 与 `references/` **实时解析**版本号、路由行数、自检项数、字数、别名组数 | §13 单一真源、§11 一致性 |
| **记忆树 + 接线体检** | `scripts/mindmap.py` → `memory/tree.md` + `memory/index.json` | 新增知识「写了但没路由」，等于没写 → 逐文件报「未接线 / 失联」 | §1 信息架构、§4 链接 |
| **章节级检索** | `scripts/dp_search.py` + `memory/aliases.json` | 标题写得像散文，用户查不到 → 强制「新知识必须命中关键词前 3 条，命中不了改标题不改检索器」 | §4 检索、§5 标题 sentence case |
| **版本与发布闭环** | `memory/design-log.md` → `build_readme.py` → `publish_github.py` → 双份全局安装 → 远端逐字比对 | README changelog 漏记一轮、本地/远端/安装副本三者不一致 | §10 版本化、§11 changelog 单一可信源 |

**两条踩过的坑，值得写进任何文档团队的规约**：
- **历史基线只加标注、不改原文；但活规则必须改源头**。#16 轮发现 `ux-writing.md` 的「按钮容纳 +40%」对短串是错的，处理方式不是只在新文件里写「以我为准」，而是把 `ux-writing.md` §13.1 与 §18 自检第 16 项**一并改写**，历史段落只加「v20 已裁决」标注。→ 对应本文 §11「changelog 应当是 single source of truth」。
- **远端比对先归一化行尾**：远端存 LF、本地存 CRLF，直接比 sha256 会假报 DIFF。文档产物也常有同类问题（不同 OS 生成），比对前统一换行、统一编码。

### 17.3 一条反直觉但重要的结论

**文档越"自动生成"越要写判断**。能自动生成的（props、token 值、故事截图、变更列表）不写反而更准；不能自动生成的（何时别用、证据、取舍、已知问题）不写就永远没人补。所以文档工作量不会因自动化减少，只是**从抄数值转向写立场**。

---

## 18. 十二场景速查（设计系统文档写作）

| # | 场景 | 先读 | 第一动作 |
|---|---|---|---|
| 1 | 从零建设计系统站 | §1 §4 §7 | 先切四象限目录，再写第一个组件页 |
| 2 | 重写一个没人看的组件页 | §2 §3 §8 | 补 When not to use / Research / Recent changes / Help improve |
| 3 | 「文档和代码对不上」 | §13 §14 | 把数值与 props 改为生成，Markdown 只留判断 |
| 4 | 组件库发版 | §10 §11 | 按 MINOR/MAJOR 决定是否切文档版本；必写 `Unreleased` → 版本 |
| 5 | 有 breaking change | §12 | 迁移文档六段 + codemod + `[BREAKING]` |
| 6 | 要废弃一个组件 | §9 §11 | 至少一个带废弃声明的 MINOR，再在 MAJOR 移除 |
| 7 | 组件被投诉难用 | §8 §9 §16 | 转 `use with caution`，写清哪条要求未满足 |
| 8 | 用户说"照 XX 感觉做" | `design-md-format.md` | 那是 DESIGN.md，不是设计系统站点（§0） |
| 9 | 多版本并存 | §10 | 先回答"真的需要吗"；要则版本数 <10、dev 限 2–3 |
| 10 | 中文团队写文档 | §5 | 术语表 + sentence case 英文标题 + 条件前置 + ≤30 字 |
| 11 | 接入 AI 编码 / MCP | §15 | 命名三处一致 + Code Connect 连真实代码路径 |
| 12 | 文档长期没人维护 | §16 §17 | 补 owner、lastReviewed、反馈入口；CI 巡检 |

---

## 19. 二十条反模式（写了等于没写）

1. **只有截图和 props 表**，没有「什么时候不用」。
2. 把教程、操作指南、参考、解释**混在一页**不分区（Diátaxis 最常见的 conflation）。
3. 教程里给分支与可选项 —— *"It doesn't offer choices or alternatives"*。
4. 操作指南不写异常处理，遇到真实世界就断。
5. props 参考表里夹三段「我们为什么这样设计」。
6. `description` 写同义反复（"这是一个按钮"）而不是用途。
7. **手抄 token 值**到 Markdown（`#1677FF` / `16px`），改 token 时全站说谎。
8. 示例缺 import / 用 `...` 省略 / 不能复制运行。
9. 只有一种实现形态，框架用户自己猜。
10. **不写禁用态、错误态、空态、暗底、超长文案、键盘与读屏**。
11. 用"遵循业界最佳实践"代替可点的研究出处。
12. 组件页没有 `Recent changes`，用户不知道看的是哪一版。
13. 没有 `Help improve` / owner / 讨论串，错误永久留存。
14. `stable` 徽章随手贴，但没测过、没写完整文档（USWDS：stable 要求 *fully documented*）。
15. **PATCH 也切一份文档版本**，制造重复文件（Docusaurus 明确反对）。
16. 用 commit log diff 当 CHANGELOG；或漏写 deprecations / removals / breaking changes。
17. 日期写 `2026/11/5`，地区歧义；或 changelog 只存在于 GitHub Releases。
18. 迁移说明写在会议纪要 / 群置顶，不可检索、不可版本化。
19. Figma 组件名、代码组件名、文档 `title` 三者不一致，Code Connect 形同虚设。
20. 文档里留着旧口径还标「 authoritative」——包括引用 **preview draft** 的规范 URL（`tr.designtokens.org/format/`），而不引用 published 2025.10。

---

## 20. 二十项自检（组件文档上线前逐条打勾）

1. 页面属于四象限中的哪一类？混合页是否有固定分区（§1）？
2. frontmatter 的 `title / description / section / aliases / status / owner / lastReviewed / discussionId` 齐了吗（§2.1 / §7）？
3. 五问全答得出来：用不用 / 何时不用 / 怎么用 / 边界态 / 凭什么（§3.1）？
4. 达到最低门槛：1 可交互实例 + 2 段判断 + 3 状态 + 1 证据 + 1 变更记录？
5. NN/g 六字段齐了吗（name / description / attributes / state / code snippets / frameworks）？
6. 标题是 sentence case？链接文字可独立理解？文档间链接写的是文件路径带 `.md`（§4/§5）？
7. 绝对路径 import 用 `@site`？图片按随版本/全局分放（§4）？
8. 第二人称 + 主动语态 + 条件前置 + 无未来预告（§5）？
9. 中文有术语表？同概念同词？英文标题 sentence case、标题不加句号？
10. 每个示例可直接复制运行，且一例只演示一件事（§6）？
11. 代码与示例是否与 story / template 同源，而非手抄（§14/§15）？
12. 可访问性数值写进正文了吗（对比度、焦点、目标尺寸、aria-label、aria-live）？
13. `Research` 有日期 + 结论 + 可点出处？没有则明确写「暂无」？
14. `Known issues` / `Recent changes`（Date/Changed/Description）在吗？BREAKING 加粗了吗？
15. `Help improve` 三个入口齐了吗（讨论 / 改文件 / 找团队）？
16. `status` 是否与实际成熟度一致？改状态是否同步改了页首警示与替代方案（§9）？
17. 这次变更是 PATCH 吗？是则**没有**切文档版本（§10）？
18. CHANGELOG 顶部有 `Unreleased`？六类分组、ISO 8601 日期、版本可链接、废移除破坏项齐全（§11）？
19. 有 MAJOR 吗？迁移文档六段 + codemod + before/after 齐了吗（§12）？
20. token 值全部由 `.tokens.json` 生成？`$description` 写用途不写值？CI 会在 token 变更未更新文档时失败（§13/§17）？

---

## 21. 六段可抄代码（文档团队直接拿去用）

### 21.1 组件页 frontmatter 校验（Python，CI 里跑）

```python
import re, sys, datetime, pathlib
REQ = ["title","description","section","status","owner","lastReviewed","discussionId"]
VALID_STATUS = {"experimental","stable","use with caution","deprecated","retired"}
def check(p: pathlib.Path):
    t = p.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", t, re.S)
    if not m: return [f"{p.name}: 缺 frontmatter"]
    fm = dict(re.findall(r"^([A-Za-z]+):\s*(.+)$", m.group(1), re.M))
    errs = [f"{p.name}: 缺 {k}" for k in REQ if k not in fm]
    if fm.get("status") not in VALID_STATUS: errs.append(f"{p.name}: status 非法")
    try:
        age = (datetime.date.today() - datetime.date.fromisoformat(fm["lastReviewed"])).days
        if age > 90: errs.append(f"{p.name}: stale {age}d (>90)")
    except Exception: errs.append(f"{p.name}: lastReviewed 非 ISO 日期")
    body = t[m.end():]
    for h in ["When to use","When not to use","How it works","Research","Recent changes","Help improve"]:
        if h.lower() not in body.lower(): errs.append(f"{p.name}: 缺段 {h}")
    return errs
errs = [e for p in pathlib.Path("components").glob("*.md") for e in check(p)]
print("\n".join(errs) or "OK: 全部组件页通过")
sys.exit(1 if errs else 0)
```

### 21.2 Docusaurus 版本化配置（单 major 长期维护，避免维护两份）

```js
// docusaurus.config.js
export default {
  presets: [['classic', {
    docs: {
      lastVersion: 'current',            // /docs 指向 ./docs，不再指向冻结快照
      includeCurrentVersion: true,
      onlyIncludeVersions: process.env.NODE_ENV === 'production'
        ? undefined : ['current', '3.0', '2.0'],   // dev 只构建 2–3 个版本
      versions: { current: { label: '3.0', path: '3.0', banner: 'none', badge: true } },
    },
  }]],
  themeConfig: { navbar: { items: [{ type: 'docsVersionDropdown',
    versions: ['current', '3.0', '2.0'] }] } },
};
```

### 21.3 CHANGELOG 格式校验（六类 / ISO 日期 / Unreleased / breaking）

```python
import re, sys, pathlib
t = pathlib.Path("CHANGELOG.md").read_text(encoding="utf-8")
HEAD = re.compile(r"^## \[(.+?)\](?: - (\d{4}-\d{2}-\d{2}))?(?: \[YANKED\])?$", re.M)
ALLOWED = {"Added","Changed","Deprecated","Removed","Fixed","Security"}
errs = []
if not t.startswith("# Changelog"): errs.append("文件名/首行应为 '# Changelog'")
if "## [Unreleased]" not in t: errs.append("缺 Unreleased")
heads = HEAD.findall(t)
if any(v != "Unreleased" and not d for v, d in heads): errs.append("有版本缺 ISO 8601 日期")
for sec in re.findall(r"^### (.+)$", t, re.M):
    if sec not in ALLOWED: errs.append(f"非法分组 {sec}")
if re.search(r"BREAKING|Removed", t) and "migrations/" not in t:
    errs.append("有破坏性变更但 CHANGELOG 未指向迁移文档")
print("\n".join(errs) or "OK: CHANGELOG 通过")
sys.exit(1 if errs else 0)
```

### 21.4 token 文件 → 文档表格生成器（用 `$description` / `$deprecated`）

```python
import json, pathlib
def rows(node, prefix=""):
    for name, obj in node.items():
        if name.startswith("$") or not isinstance(obj, dict): continue
        path = f"{prefix}.{name}" if prefix else name
        if "$value" in obj:
            v = obj["$value"]
            val = v.get("hex") if isinstance(v, dict) else v
            dep = obj.get("$deprecated")
            status = "⚠️ 废弃" if dep and dep is not False else "✅"
            note = dep if isinstance(dep, str) else obj.get("$description", "")
            yield f"| `{path}` | `{obj.get('$type','—')}` | `{val}` | {status} | {note} |"
        else:
            yield from rows(obj, path)
data = json.loads(pathlib.Path("tokens/tokens.tokens.json").read_text(encoding="utf-8"))
body = "\n".join(rows(data))
print("| Token | 类型 | 值 | 状态 | 说明 |\n|---|---|---|---|---|\n" + body)
# 注意：只展示 token 名与解析值；$description 写用途不写值（DTCG §5.2.1）
```

### 21.5 Storybook MDX 组件页（人写判断 + 机器给值）

```mdx
import { Meta, Canvas, Controls, Stories, Markdown } from '@storybook/addon-docs/blocks';
import * as ButtonStories from './Button.stories';
import Changelog from '../../CHANGELOG.md?raw';

<Meta of={ButtonStories} name="用法与规范" />

# Button 按钮

让用户执行一个明确的动作，例如提交表单或开始一项服务。

## When not to use 什么时候不用

- 只是跳转页面 → 用链接；一页多个主按钮 → 先简化页面。
- 危险且不可撤销 → 用 warning 变体，且不能只靠红色传达。

<Canvas of={ButtonStories.Default} />
<Controls of={ButtonStories.Default} />

## 状态与变体

<Stories />

## Research on this component

| 日期 | 结论 | 出处 |
|---|---|---|
| 2026-07 | 绿色 start button 提高点击率 | GOV.UK discussion #6094 |

## Recent changes

<Markdown>{Changelog}</Markdown>
```

### 21.6 文档新鲜度巡检（owner / stale / 失联链接）

```python
import re, pathlib, datetime
root = pathlib.Path(".")
docs = list(root.glob("components/*.md")) + list(root.glob("guides/*.md"))
ids = {p.stem for p in docs}
for p in docs:
    t = p.read_text(encoding="utf-8")
    fm = dict(re.findall(r"^([A-Za-z]+):\s*(.+)$", t.split("---")[1], re.M)) if t.startswith("---") else {}
    if not fm.get("owner"): print(f"FAIL {p}: 无 owner")
    d = fm.get("lastReviewed")
    if d and (datetime.date.today()-datetime.date.fromisoformat(d)).days > 90:
        print(f"STALE {p}: {d}")
    for link in re.findall(r"\]\(\.?\.?/?([\w-]+)\.md", t):
        if link not in ids: print(f"BROKEN {p} -> {link}.md")
```

---

## 22. 来源（2026-11-05 取源，全部官方原文 / 上游源码 / API 实测）

**组件页结构与准入**：
- GOV.UK Design System · Button（渲染页九段 + Recent changes + Help improve）：https://design-system.service.gov.uk/components/button/
- GOV.UK Design System · `src/components/button/index.md`（frontmatter 与全部 H2/H3 源文件）：https://github.com/alphagov/govuk-design-system/blob/main/src/components/button/index.md
- GOV.UK Design System · Contribution criteria（Useful/Unique/Usable/Consistent/Versatile + 社区资源 1 个月 / 3 个月阈值）：https://design-system.service.gov.uk/community/contribution-criteria/
- NN/g · Design Systems 101（2021-04-11，2026-08-27 复审；组件库六字段、最小团队、维护警告）：https://www.nngroup.com/articles/design-systems-101/

**信息架构与写作**：
- Diátaxis 首页与四象限：https://diataxis.fr/ 、https://diataxis.fr/tutorials-how-to/ 、https://diataxis.fr/reference-explanation/
- Google developer documentation style guide · About（三层参考层级 / Orwell 破例）：https://developers.google.com/style
- Google style guide · Highlights（第二人称、主动语态、sentence case、列表、alt、descriptive link）：https://developers.google.com/style/highlights

**状态、版本与变更**：
- USWDS 站点数据 `lifecycle-phases.yml`（三阶段 / 十二子状态 / 45 天评论期 / fully documented）：https://github.com/uswds/uswds-site/blob/main/_data/lifecycle-phases.yml
- USWDS 组件状态数据 `lifecycle-status.yml`（`status_major` / `status_minor`）：https://github.com/uswds/uswds-site/blob/main/_data/lifecycle-status.yml
- Carbon · `docs/guides/versioning.md`（逐改动类型 semver 表 + TS 类型免责）：https://github.com/carbon-design-system/carbon/blob/main/docs/guides/versioning.md
- Docusaurus 3.10.2 · Versioning（目录结构 / `lastVersion` / `onlyIncludeVersions` / <10 / patch 不切版本 / `@site`）：https://docusaurus.io/docs/versioning
- Keep a Changelog 1.1.0（七原则 / 六类 / Unreleased / ISO 8601 / YANKED）：https://keepachangelog.com/en/1.1.0/
- SemVer 2.0.0（11 条规范 + FAQ 废弃流程）：https://semver.org/

**token 文档与代码即文档**：
- DTCG · Design Tokens Format Module **published 2025.10**（应引用的权威 URL）：https://www.designtokens.org/TR/2025.10/format/
- DTCG · preview drafts（**不可引用为权威**，页首明确 "Do not reference this version as authoritative"）：https://tr.designtokens.org/format/
- DTCG 规范仓库（术语 §3.5 Documentation tool / `$description` / `$deprecated` / `$extensions` / 引用环）：https://github.com/design-tokens/community-group
- Storybook · How to document components：https://storybook.js.org/docs/writing-docs
- Storybook · Autodocs（`tags: ['autodocs']` / `!autodocs` / 默认六 Doc Block）：https://storybook.js.org/docs/writing-docs/autodocs
- Storybook · MDX（`Meta of` full set of exports / 空行规则 / Canvas / Story / Markdown）：https://storybook.js.org/docs/writing-docs/mdx
- Figma · Code Connect（UI vs CLI / template files / MCP / 计划与 active library 限制）：https://help.figma.com/hc/en-us/articles/23992898986135-code-connect 、https://www.figma.com/developers/code-connect

**GitHub REST API 实测（2026-11-05，star / 许可 / 最近推送 / 归档状态）**：

| 仓库 | star | 许可 | pushed | 状态 |
|---|---|---|---|---|
| storybookjs/storybook | 91461 | MIT | 2026-11-05 | 活跃 |
| facebook/docusaurus | 66657 | MIT | 2026-11-05 | 活跃 |
| mdx-js/mdx | 19850 | MIT | 2026-11-04 | 活跃 |
| vuejs/vitepress | 18463 | MIT | 2026-11-05 | 活跃 |
| carbon-design-system/carbon | 9604 | Apache-2.0 | 2026-11-05 | 活跃 |
| uswds/uswds | 7238 | NOASSERTION | 2026-11-04 | 活跃 |
| olivierlacan/keep-a-changelog | 6750 | MIT | 2026-09-07 | 活跃 |
| Shopify/polaris | 6148 | NOASSERTION | 2026-09-11 | **已归档（archived=true）** |
| amzn/style-dictionary | 4877 | Apache-2.0 | 2026-11-03 | 活跃 |
| histoire-dev/histoire | 3589 | MIT | 2026-11-03 | 活跃 |
| tajo/ladle | 2998 | MIT | 2026-06-28 | 活跃（推送趋缓） |
| design-tokens/community-group | 2163 | NOASSERTION | 2026-11-01 | 活跃 |
| adobe/spectrum-css | 1293 | Apache-2.0 | 2026-10-13 | **已归档（archived=true）** |
| storybookjs/addon-designs | 952 | MIT | 2026-10-22 | 活跃 |
| alphagov/govuk-design-system | 685 | MIT | 2026-11-05 | 活跃（文档站仓库） |

> ⚠️ **本轮实测发现**：`Shopify/polaris` 与 `adobe/spectrum-css` 均已 `archived=true`。引用它们的设计规范内容仍有效，但**不要把它们当作会持续更新的活源**；`handoff-collaboration.md` 的 Star 快照是 2026-11-01 的历史值，本表是 2026-11-05 新快照，两者不冲突。
