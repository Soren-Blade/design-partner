# design-partner · 设计伙伴

**把模糊的想法，变成有品味、可执行的设计决策。** 它不是一本规范手册，而是一条判断流程：
先问清约束，再并置三个方向，然后带着代价选一个，最后用证据自检。

`当前版本 v70` · 本页由 `scripts/build_readme.py` 生成于 2026-11-23 · 生成器与 `CHANGELOG.md` 同源

---

## 它做什么，不做什么

| 做 | 不做 |
|---|---|
| 从一句模糊需求里问出真正约束（最多 3 个问题，给选项） | 一上来给 8 套配色让你挑 |
| 对同一 brief 给**保守 / 主流 / 进取**三案，并说明各自代价 | 只给「最佳实践」一句话 |
| 按比例、节奏、层级、材料、克制、一致性六维给审美判断 | 用「高级感」「大气」当结论 |
| 用 5 秒测试、盲评、大众锚检验是否只是自我感觉良好 | 用合规清单代替好看 |
| 把每次真实反馈记进 `memory/journal.jsonl`，够了才升级为规则 | 把「待观察」写成「已完成」 |

## 30 秒开始

```bash
python scripts/dp_search.py "续费弹窗怎么写得不像骗人"   # 关键词 → 命中文件 §章节 + 行号
python scripts/dp_search.py --topic                    # 看全部主题
python scripts/mindmap.py                              # 资产变了才需要：重建索引与记忆树
python scripts/memory.py stats                         # 记忆里到底有多少条真实反馈
```

在 DeepSeek Harness 里直接说需求即可（如「做一个 SaaS 定价页」「这张海报不好看，改」），
技能会被自动载入；`SKILL.md` 是判断流程，`references/` 是按需读的 1–3 份资产。

## 一次完整的判断长什么样

```
你：做个面向独立开发者的 API 监控落地页
它：问 3 个问题（谁在什么场景打开？最怕什么？要极简还是浓烈？）→ 缺省：极简、浅色、专业
    给三案：A 保守（文档站气质，信任优先）/ B 主流（Linear 式暗色+渐变，转化优先）/ C 进取（监控墙即首屏，证据优先）
    裁决：选 B；代价＝更贵的前端动效与更弱的「朴素可信」；证据＝同类产品首屏 5 秒测试通过率
    改选 A 的条件：客户是金融/政企，采购先看合规与稳定
    自检：5 秒内能否说出「这是监控」？缩小到 320px 后主按钮还在首屏？暗色下状态色对比度过 4.5:1？
```

## 资产一览（62 份，按需读）

| 组 | 资产 | 行 | 节 |
|---|---|---:|---:|
| 判断与品味 | [`taste-criteria.md`](references/taste-criteria.md) · 品味判据 · Taste Criteria | 304 | 11 |
| 判断与品味 | [`comparison-protocol.md`](references/comparison-protocol.md) · 比较协议 · Comparison Protocol | 190 | 9 |
| 判断与品味 | [`before-after.md`](references/before-after.md) · 改稿案例（Before / After） | 976 | 13 |
| 判断与品味 | [`user-modeling.md`](references/user-modeling.md) · 用户建模（User Modeling） | 276 | 9 |
| 判断与品味 | [`numeric-truth.md`](references/numeric-truth.md) · 数值口径单点（Numeric Truth） | 202 | 6 |
| 判断与品味 | [`design-critique.md`](references/design-critique.md) · 设计评审与反馈 · Design Critique & Feedback | 261 | 23 |
| 视觉基础 | [`typography-system.md`](references/typography-system.md) · 字体排印系统（Typography System） | 590 | 24 |
| 视觉基础 | [`color-science.md`](references/color-science.md) · 色彩科学（Color Science for Designers） | 400 | 16 |
| 视觉基础 | [`visual-hierarchy-gestalt.md`](references/visual-hierarchy-gestalt.md) · 视觉层级与格式塔组织律（Visual Hierarchy & Gestalt / Attention & Cognitive Load） | 672 | 24 |
| 视觉基础 | [`shape-elevation.md`](references/shape-elevation.md) · 形状与深度系统（Shape & Elevation） | 820 | 24 |
| 视觉基础 | [`iconography.md`](references/iconography.md) · 图标设计系统 · Iconography | 339 | 20 |
| 视觉基础 | [`visual-style-taxonomy.md`](references/visual-style-taxonomy.md) · 视觉风格谱系与设计运动（Visual Style Taxonomy） | 318 | 14 |
| 视觉基础 | [`chinese-design.md`](references/chinese-design.md) · 中文设计场景 — Chinese Design（排版规范 + 生态地图） | 181 | 4 |
| 视觉基础 | [`design-tokens.md`](references/design-tokens.md) · 设计 Token 体系 — Design Tokens（深度蒸馏） | 229 | 6 |
| 视觉基础 | [`brand-identity.md`](references/brand-identity.md) · 品牌视觉与 Logo 逻辑（Brand Identity） | 695 | 21 |
| 版式与系统 | [`editorial-layout.md`](references/editorial-layout.md) · 版式与网格（Editorial Layout） | 759 | 21 |
| 版式与系统 | [`responsive-layout.md`](references/responsive-layout.md) · 响应式与断点体系 · Responsive Layout | 717 | 20 |
| 版式与系统 | [`dark-mode.md`](references/dark-mode.md) · 暗色模式体系（Dark Mode System） | 559 | 15 |
| 版式与系统 | [`motion-system.md`](references/motion-system.md) · 动效与微交互系统 — Motion System（深度蒸馏） | 325 | 12 |
| 版式与系统 | [`dataviz.md`](references/dataviz.md) · 数据可视化规范 · Data Visualization | 361 | 14 |
| 版式与系统 | [`performance-design.md`](references/performance-design.md) · 性能与设计的关系（Performance × Design） | 844 | 19 |
| 版式与系统 | [`multi-brand-theming.md`](references/multi-brand-theming.md) · 多品牌与多主题 Token 架构 — Multi-brand & Multi-theme | 865 | 21 |
| 界面与交互 | [`component-api-design.md`](references/component-api-design.md) · 组件 API 设计与组合模式：状态所有权、渲染所有权、契约可演进 | 918 | 23 |
| 界面与交互 | [`form-table.md`](references/form-table.md) · 表单与表格 — Forms & Tables（深度蒸馏） | 503 | 19 |
| 界面与交互 | [`feedback-states.md`](references/feedback-states.md) · 反馈与状态设计 — Feedback & States（深度蒸馏） | 551 | 15 |
| 界面与交互 | [`empty-states.md`](references/empty-states.md) · 空状态与零数据位（Empty States & Zero-Data） | 254 | 16 |
| 界面与交互 | [`navigation-ia.md`](references/navigation-ia.md) · 导航与信息架构 · Navigation & Information Architecture | 279 | 15 |
| 界面与交互 | [`overlays-modality.md`](references/overlays-modality.md) · 叠加层与模态性：判型、焦点契约、顶层栈与非模态消隐 | 927 | 25 |
| 界面与交互 | [`content-findability.md`](references/content-findability.md) · 内容可发现性与可扫读性（Content Findability / Search UX / Scannability） | 957 | 27 |
| 界面与交互 | [`direct-manipulation.md`](references/direct-manipulation.md) · 直接操纵与指针交互（Direct Manipulation / Pointer, Gesture & Drag-and-Drop） | 894 | 26 |
| 界面与交互 | [`keyboard-shortcuts-command-palette.md`](references/keyboard-shortcuts-command-palette.md) · 键盘快捷键与命令面板（Keyboard Shortcuts & Command Palette）：把「记不住的按键」做成可发现、可关闭、可重 | 919 | 17 |
| 界面与交互 | [`onboarding-first-run.md`](references/onboarding-first-run.md) · 首次体验与用户引导：从启动到 Aha Moment 的判型、时机与可访问性契约 | 901 | 25 |
| 界面与交互 | [`sound-haptics-feedback.md`](references/sound-haptics-feedback.md) · 声音与触觉反馈：把「要不要响一下 / 震一下」判成通道、时长与强度 | 788 | 16 |
| 界面与交互 | [`conversational-generative-ui.md`](references/conversational-generative-ui.md) · 对话式与生成式界面：流式输出、混合界面与可纠错契约 | 748 | 26 |
| 界面与交互 | [`realtime-collaboration.md`](references/realtime-collaboration.md) · 实时协作与多人编辑（Real-time Collaboration & Presence） | 770 | 22 |
| 界面与交互 | [`video-player-captions.md`](references/video-player-captions.md) · 视频播放器与字幕（Video Player UX & Captions / Subtitles / WebVTT） | 586 | 14 |
| 领域与商业 | [`presentation-design.md`](references/presentation-design.md) · 演示文稿与幻灯片版式（Presentation Design） | 1129 | 19 |
| 领域与商业 | [`email-design.md`](references/email-design.md) · 邮件设计与 EDM 排版（HTML Email Design / EDM Layout） | 835 | 22 |
| 领域与商业 | [`pricing-checkout.md`](references/pricing-checkout.md) · 定价页与结账流程（Pricing & Checkout） | 445 | 19 |
| 领域与商业 | [`pricing-localization.md`](references/pricing-localization.md) · 定价本地化（Pricing Localization）：币种、含税口径、地区价差与法定原价 | 689 | 14 |
| 领域与商业 | [`quote-invoice-documents.md`](references/quote-invoice-documents.md) · 报价与发票单据（Quote, Invoice & Order Documents）：报价单、发票、订单确认与对账的单据语法 | 1004 | 15 |
| 领域与商业 | [`auth-account-ux.md`](references/auth-account-ux.md) · 认证与账户体验（Authentication & Account UX） | 827 | 19 |
| 领域与商业 | [`notifications-messaging.md`](references/notifications-messaging.md) · 通知与消息触达（Notifications & Messaging） | 989 | 26 |
| 领域与商业 | [`file-upload-media-input.md`](references/file-upload-media-input.md) · 文件上传与媒体输入（File Upload & Media Input）：把「选个文件传上去」做成可失败、可恢复、可验收的五段链路 | 713 | 15 |
| 领域与商业 | [`handoff-collaboration.md`](references/handoff-collaboration.md) · 设计交付与协作 / Design Handoff & Collaboration | 852 | 24 |
| 领域与商业 | [`design-measurement-research.md`](references/design-measurement-research.md) · 设计度量与用户研究：可用性指标、研究方法与统计验收 | 510 | 24 |
| 领域与商业 | [`ux-writing.md`](references/ux-writing.md) · 内容设计与 UX 文案 — UX Writing & Content Design（深度蒸馏） | 821 | 19 |
| 合规与工具链 | [`accessibility.md`](references/accessibility.md) · 可访问性实操 / 无障碍（Accessibility in Practice） | 691 | 20 |
| 合规与工具链 | [`i18n-localization.md`](references/i18n-localization.md) · 国际化与本地化设计（i18n / L10n / RTL / 多语言） | 1059 | 22 |
| 合规与工具链 | [`design-ethics-inclusion.md`](references/design-ethics-inclusion.md) · 设计伦理与包容性：欺骗性设计、隐私同意 UI、成瘾机制与认知无障碍 | 800 | 24 |
| 合规与工具链 | [`ai-design-toolchain.md`](references/ai-design-toolchain.md) · AI / 生成式设计工具链：工作流、提示词、质量验收与合规边界 | 791 | 32 |
| 合规与工具链 | [`design-system-docs.md`](references/design-system-docs.md) · 设计系统文档写作：组件文档页 / 信息架构 / 版本化 / 治理 | 950 | 37 |
| 合规与工具链 | [`component-libraries.md`](references/component-libraries.md) · 组件库与设计 GitHub 地图 — Component Libraries | 38 | 3 |
| 索引与资源 | [`knowledge-map.md`](references/knowledge-map.md) · 设计能力知识路线图 — Knowledge Map（L0→L4） | 820 | 9 |
| 索引与资源 | [`patterns.md`](references/patterns.md) · 元素设计模式图鉴 — Patterns（深度蒸馏） | 134 | 14 |
| 索引与资源 | [`portfolios.md`](references/portfolios.md) · 作品集 — Portfolios | 23 | 4 |
| 索引与资源 | [`resources.md`](references/resources.md) · 设计资源 — Resources | 40 | 6 |
| 索引与资源 | [`tools.md`](references/tools.md) · 制作工具 — Tools | 31 | 5 |
| 索引与资源 | [`inspiration.md`](references/inspiration.md) · 灵感与阅读 — Inspiration | 21 | 3 |
| 索引与资源 | [`design-md-format.md`](references/design-md-format.md) · DESIGN.md 规范与品牌 DNA — Design Spec | 191 | 7 |
| 未归组（请补 GROUPS） | [`motion-orchestration.md`](references/motion-orchestration.md) · 动效进阶 — 编排、状态机与共享元素转场（深度蒸馏） | 1046 | 20 |
| 未归组（请补 GROUPS） | [`print-export.md`](references/print-export.md) · 打印与导出（Print & PDF Export）：纸张、分页、去色可读、页眉页脚 | 195 | 10 |

## 记忆与成长

- 反馈日志：`memory/journal.jsonl`，67 条记录，其中 0 条带真实用户反馈
- 用户画像：`memory/profile.md`（51 行）；规则只在同一偏好出现 ≥2 次后晋升
- 历史：`CHANGELOG.md`（每轮一行摘要）；取源口径：`SOURCES.md`
- 成长协议：一进一出（新增 N 字符必须删掉 N 字符）、`SKILL.md` ≤ 500 行、单份资产 ≤ 1,200 行、
  每轮必须写下「被推翻的旧判断」；`scripts/audit.py` 是发布门禁

## 目录

```
SKILL.md           判断流程（≤500 行）：总纲 → 五问 → 判层 → 三案裁决 → 路由 → 自检 → 记忆 → 成长
references/        资产库：判断品味 / 视觉基础 / 版式系统 / 界面交互 / 领域商业 / 合规与索引
memory/            profile.md + journal.jsonl（长期记忆）；索引与树是本地生成物，不入库
scripts/           dp_search / mindmap / memory / audit / build_readme / regression
tests/golden/      10 条基准 brief + 评分 rubric（防回退）
CHANGELOG.md       逐版变更（只追加一行摘要）
SOURCES.md         每轮取源与「未验证」标记的纪律
```

## 视觉与内容边界

- 不臆造资源、库、数值：引用不给 URL 视为未验证，写进 `SOURCES.md` 的「未验证」区
- 不把法条当设计值、不把设计值当法条：口径冲突先查 `references/numeric-truth.md`
- 中文优先；中英混排、行高、标点按 `typography-system.md` + `chinese-design.md` 的同一套口径

## License

代码（`scripts/`、`tests/`）MIT；文本与资产（`SKILL.md`、`references/`、`memory/` 模板）CC BY 4.0，
转载注明来源。商用前请自行核对所引第三方规范的授权。

## 反馈

发现说错、过时、自相矛盾：直接开 issue，附「哪一句 / 哪份文件 / 反例」。
每一条带反例的反馈都会进 `journal.jsonl`，而不是只改一句话。
