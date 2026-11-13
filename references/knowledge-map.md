# 设计能力知识路线图 — Knowledge Map（L0→L4）

> 本文件回答「**一个设计师该按什么顺序学、每个阶段读什么、怎么验收学会了**」。它不替代其他参考文件，而是给它们排顺序、定门槛。
> 使用方式：接到任务先判断自己落在哪一级，缺什么补什么——**不要跳级**（L0 没建立视觉判断力就上 L2 做设计系统，产出必然空洞）。
> 快照 2026-11-05

---

## 全景：五级台阶与对应产出

| 级别 | 名称 | 一句话目标 | 可交付物 | 对应参考文件 |
|---|---|---|---|---|
| **L0** | 视觉感知 | 能**看出**两个设计的高低 | 一份「好在哪/差在哪」的书面判断 | `portfolios.md`、`inspiration.md` |
| **L1** | 界面语汇 | 知道每个元素**有几种做法** | 元素级设计板（4–6 变体） | `patterns.md` |
| **L2** | 系统秩序 | 用**一套 token** 统管全站 | 设计 token 表 + DESIGN.md | `design-tokens.md`、`design-md-format.md` |
| **L3** | 工程落地 | 把设计**变成可运行代码** | 组件代码 / 可交互页面 | `component-libraries.md`、`tools.md` |
| **L4** | 判断与品味 | 在**冲突约束**下做取舍 | 设计评审报告、方案对比结论 | 本文件 + `chinese-design.md` |

**级别不是资历，是任务类型。** 同一份工作里会反复上下：做落地页是 L0→L1→L2→L3 直落；被问"这版好不好"是 L4 单点。

---

## L0 · 视觉感知：先治"看不出来"

**为什么排第一**：绝大多数"设计不好"不是技法问题，是**看不出问题**。没有分辨力，学再多规范也只是套模板。

### 核心概念（4 个）
1. **层级（Hierarchy）**——一屏只有一个主角。判断法：眯眼看，还能分清主次吗？
2. **对齐（Alignment）**——一条轴贯穿到底；出现第 3 种对齐前先停。
3. **留白（Whitespace）**——留白是分组工具，不是"没填满"。
4. **一致性（Consistency）**——同义元素同款；出现"只出现一次"的样式就是漏洞。

### 必读材料
- 本技能 `portfolios.md`：选 5 个作品集，逐站回答"它的主角是谁、靠什么手法突出"
- [Refactoring UI](https://www.refactoringui.com/)：层级/间距/色彩最实用的成体系读本
- [Practical Typography](https://practicaltypography.com/)：排版判断力的地基
- [Laws of UX](https://lawsofux.com/)：把"为什么这样更舒服"讲成规律
- [Nielsen Norman Group](https://www.nngroup.com/articles/)：可用性研究的权威结论库

### 练习（必须落成文字）
取任意两个同类站点（如两个 SaaS 首页），写 300 字对比：
- 各自的主角是什么？用什么手法（字号/色/位置/留白）确立的？
- 哪个更清楚？给出**明确结论**，不许"各有千秋"。

### 验收标准
能对任何界面在 60 秒内说出：主角、视觉路径、最弱的一环。做不到就还在 L0。

---

## L1 · 界面语汇：从"感觉"到"构型"

**为什么**：设计师和普通人的差别不是审美，是**知道有几种做法**。只会一种做法的人，遇到不合适的场景就只能硬套。

### 核心概念
1. **构型谱系**——每个元素有 4–6 种主流构型，各有适用场景（见 `patterns.md`）
2. **参数区间**——高度/字号/间距不是拍脑袋，是区间（如导航栏 56–72px）
3. **构型 ≠ 装饰**——选构型解决的是"信息怎么组织"，不是"加不加渐变"
4. **变体纪律**——同页不混用两种构型语言

### 必读材料
- 本技能 `patterns.md`：12 类元素，每类「构型 → 参数 → 变体 → 速配 → 常见错误」
- [SEESAW](https://www.seesaw.website/)：按页面区块组织的参考库
- [Supahero](https://www.supahero.io/)：首屏专库
- [Mobbin](https://mobbin.com/)：真实产品流程（看真实取舍，不看概念稿）
- [Ant Design 设计模式](https://ant.design/docs/spec/overview-cn)：中后台元素的权威范式

### 练习
任选一个元素（导航栏/定价表/表单），产出 4–6 个构型变体的**真实渲染**设计板（不是截图、不是链接）。

### 验收标准
给一个元素 + 场景（"文档站导航"），能直接说出该选哪种构型、为什么、参数取多少。答"看情况"就是没学会。

---

## L2 · 系统秩序：从"页面"到"系统"

**为什么**：单个页面好看靠手艺，一整套产品好看只能靠系统。这一步是从"做图"跨到"做设计"。

### 核心概念
1. **三层 token 架构**：base（原始值）→ semantic（语义角色）→ component（组件专用）
2. **数值体系**：色阶（10 阶）、字阶（3–5 种）、间距（8 倍数）、圆角（2–3 档）、阴影（3–5 层）
3. **语义命名**：`--color-text-secondary` 而非 `--color-gray-600`——换肤/暗色才可能
4. **克制**：Ant Design 原话「完美不在于无以复加，而在于无可删减」
5. **一致性 ≠ 统一**：同义元素同款，异义元素必须拉开差距

### 必读材料
- 本技能 `design-tokens.md`：Ant Design 数值体系全量蒸馏 + 三大体系对比 + 中文设计系统矩阵
- [Ant Design 色彩](https://ant.design/docs/spec/colors-cn) / [字体](https://ant.design/docs/spec/font-cn) / [布局](https://ant.design/docs/spec/layout-cn)：中文语境最完整的规范原文
- [Material Design 3](https://m3.material.io/)：动态色彩与 token 命名的工业级参考
- [Apple HIG](https://developer.apple.com/design/human-interface-guidelines)：平台一致性思路
- [Utopia](https://utopia.fyi/)：流体字号/间距计算（生成 clamp）
- 本技能 `design-md-format.md`：把系统写成 agent 可执行的 DESIGN.md

### 练习
给一个虚构产品写出完整 token 表：12 个语义色 + 5 档字阶 + 8 档间距 + 3 档圆角 + 3 层阴影，并注明每项**使用场景**。

### 验收标准
token 表能直接翻译成 CSS 变量且无歧义；同一份表能同时生成浅色与深色两套。

---

## L3 · 工程落地：从"稿"到"跑起来"

**为什么**：设计的最终形态是运行中的界面。不懂实现的约束，就会设计出做不出来的东西（或成本高 10 倍的东西）。

### 核心概念
1. **技术栈匹配**：React/Vue/纯 HTML，选库先看栈再看元素覆盖
2. **性能预算**：LCP < 2.5s、CLS < 0.1、INP < 200ms（Core Web Vitals 阈值）；关键路径 <170KB、TTI <5s（3G）——见 `performance-design.md`
3. **渐进增强**：先保证无 JS 可用，再叠加动效
4. **可访问性不是附加项**：语义标签、焦点环、对比度、键盘可达
5. **许可合规**：MIT / Apache-2.0 可商用；逐组件署名（如 uiverse）需注意

### 必读材料
- 本技能 `component-libraries.md`：14 库元素覆盖矩阵 + 选型规则 + 维护协议
- 本技能 `performance-design.md`：性能阈值 / LCP 四分解 / 视觉手法价格表 / 预算与验收
- 本技能 `tools.md`：截图/录屏/优化/生成工具
- [web.dev Core Web Vitals](https://web.dev/articles/vitals)：性能阈值与测量
- [Inclusive Components](https://inclusive-components.design/)：可访问组件的实现范式
- [MDN CSS](https://developer.mozilla.org/zh-CN/docs/Web/CSS)：查具体属性行为

### 练习
把一个 L1 设计板里的变体，用选定组件库实现为可运行页面，并跑一次 Lighthouse。

### 验收标准
交付物能跑、能响应式、Lighthouse 可访问性 ≥ 90。

---

## L4 · 判断与品味：在冲突约束下取舍

**为什么**：真实项目里需求永远自相矛盾（"要高级又要热闹""信息多又要留白"）。L4 的能力是**给立场**，不是列选项。

### 核心概念
1. **约束识别**：分清"硬约束"（品牌色、法务文案、性能）与"软偏好"（个人喜好）
2. **代价思维**：每个选择都有代价，说得出代价才叫决策
3. **盲区发现**：用户没提但决定成败的点（首屏要不要动效？空状态谁设计？）
4. **场景优先**：同一个"好"在不同场景标准不同（后台重效率，官网重感染）
5. **文化语境**：中文场景的信息密度、审批流、表格文化（见 `chinese-design.md`）

### 必读材料
- [Ant Design 设计价值观](https://ant.design/docs/spec/values-cn)：自然/确定性/意义感/生长性——评价设计的内在标准
- 本技能 `chinese-design.md`：中文排版与中文产品形态的差异
- [Awwwards](https://www.awwwards.com/) + 本技能 `portfolios.md`：校准"上限在哪"
- [Nielsen Norman Group](https://www.nngroup.com/articles/)：用研究结论代替个人偏好

### 练习
拿一个真实需求，写一份**可行性 × 美观性预判**：3 条风险、每条给缓解方案、最后给"做什么/不做什么/先做什么"。

### 验收标准
结论有立场、有理由、有代价说明；被反驳时能说清"我为什么仍这样判断"。

---

## 三十五条专题支线（可与主线并行）

### 支线 A · 中文场景（中文项目必走）
中文不是"英文换字"。字号要 +1~2px、行高要 1.6–1.8、标点全角、避头尾、中英混排要间距。
→ 全量规范见 `chinese-design.md`。**做任何中文界面先读它。**

### 支线 B · 数据可视化
- 原则：准确 / 有效 / 清晰 / 美（AntV 四原则）；Data-ink Ratio 最大化
- **先判关系再选图形**（FT 九类）：偏差→分歧条形；相关→散点；排名→有序条形；分布→直方/箱线；随时间→折线；部分整体→堆叠柱/环形（≤5 片）；数量→柱形（**0 基线**）；空间→分级统计地图（用比率）；流向→桑基
- 硬上限：饼图 ≤5 片、折线 ≤5 条、颜色编码 ≤7 类、一屏图表 ≤5 张
- 三类色板不许混用：分类（固定顺序取）/ 顺序（浅色主题最深=最大）/ 发散（必须对称、中点=0）
- 交互三层：数据获取 → 信息加工 → 知识流转；口诀「概览第一，聚焦过滤，再按需查看详情」
- 材料：[FT Visual Vocabulary](https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary)、[Carbon 数据可视化色板](https://carbondesignsystem.com/data-visualization/color-palettes/)、[Ant Design 可视化](https://ant.design/docs/spec/visual-cn)、[Datawrapper 双轴指南](https://www.datawrapper.de/blog/dual-axis-charts-guide)
- → **精确色板 hex、坐标轴数值、中文数字单位、仪表盘布局、12 条反模式、12 项自检见 `dataviz.md`**

### 支线 C · 动效（界面"活"起来的那一层）
- 三种合法用途：反馈 / 引导（空间关系、过程）/ 个性（每页 ≤1 处）
- **语义定曲线**：入场减速、出场加速（时长 ×0.7）、双向位移标准、循环 linear
- **时长四档**：120 / 200 / 300 / 400ms（上限）；用户输入反馈 ≤120ms
- **只动 transform / opacity**；必须做 `prefers-reduced-motion` 降级
- 材料：[60fps](https://60fps.design/)、[Design Details](https://designdetails.fm/)、[Motion Primitives](https://motion-primitives.com)、[easings.net](https://easings.net/)
- → 全量数值、20 个场景速查、View Transitions/scroll-driven 代码、10 条验收见 `motion-system.md`
- → **进阶层**（多个元素编排 / 交错 stagger / FLIP / 共享元素转场 / 动画状态机 / 中断与取消 / `@starting-style`）见 `motion-orchestration.md`，对应下方支线 M

### 支线 D · 可访问性（不是"加分项"，是交付门槛）
- **四档对比度**：正文 4.5:1 / 大文本 3:1（≥24px 或 ≥18.5px 粗体）/ 非文本 3:1 / AAA 正文 7:1。**不可四舍五入**（`4.499:1` 不达标）。
- **焦点三层**：存在（2.4.7）→ 面积 ≥2px 周长、状态变化 ≥3:1（2.4.13）→ 与相邻色 ≥3:1（1.4.11）。内嵌焦点框要 ≥3px。永不用 `outline:none` 而无替代。
- **键盘**：顺序 = DOM 顺序；`tabindex` 只用 `0`/`-1`；模态锁焦点 + `Esc` + 关闭回原处 + 背景 `inert`。
- **目标尺寸三档**：24（AA 底线）/ 44（触屏）/ 60（适老版主组件）。
- **不只靠颜色**：错误、必填、状态、涨跌都要第二通道；色盲用 Okabe–Ito 8 色。
- **WCAG 2.2 新增 9 条**：焦点不遮挡、焦点外观、拖动替代、目标尺寸、帮助一致、不重复录入、可访问认证。
- 材料：[WCAG 2.2](https://www.w3.org/TR/WCAG22/)、[WAI-ARIA APG](https://www.w3.org/WAI/ARIA/apg/)、[GOV.UK 焦点样式](https://design-system.service.gov.uk/get-started/focus-states/)、[Inclusive Components](https://inclusive-components.design/)、[axe-core](https://github.com/dequelabs/axe-core)
- → **全部阈值、可抄 CSS、25 条上线自检、读屏 15 分钟脚本、GB/T 37668 与适老化硬指标见 `accessibility.md`**

### 支线 E · 反馈与状态（"有没有回应"决定可不可信）
- **五层反馈**：L0 微反馈（≤120ms）/ L1 toast（3–5s）/ L2 就地状态（常驻）/ L3 模态 / L4 结果页。**严重度决定层级，不决定颜色**。
- **时间刻度**：100ms 内必须有变化；<1s 不加加载态；1–2s 按钮 loading；2–10s 骨架/局部 spinner；>10s 进度 + 时间 + 取消。
- **toast 数值**：Ant 3s / 4.5s（384px）、Carbon 5s、M3 4–10s、微信 1.5s；≤2 行、1 个动作。
- **五种空态**：首次 / 无结果 / 无权限 / **失败（不要伪装成无数据）** / 完成。
- **五级错误**：字段 → 表单摘要 → 区块 → 页面（404/403/500）→ 全局。
- **确认框**：只给不可逆；写对象名 + 数量；按钮写动词；默认焦点不给危险项；能撤销优先撤销。
- 材料：[Carbon Notifications](https://carbondesignsystem.com/components/notification/usage/)、[M3 Snackbar](https://m3.material.io/components/snackbar/guidelines)、[Atlassian Flag](https://atlassian.design/components/flag/usage)、[NN/g 响应时间](https://www.nngroup.com/articles/response-times-3-important-limits/)、[NN/g 骨架屏](https://www.nngroup.com/articles/skeleton-screens/)、[GOV.UK 404](https://design-system.service.gov.uk/patterns/page-not-found-pages/)
- → **全部时长/尺寸、五态模型、10 场景速查、15 项自检见 `feedback-states.md`**

### 支线 F · 版式与网格（海报 / 长图 / 社媒图 / 印刷）
- **先判载体**：观看距离决定字号，停留时长决定信息量，媒介决定安全区。海报 1–5m 看 3 秒，长图 30cm 连续滑，社媒图缩略图只有 120px。
- **页边距**：Van de Graaf 内:上:外:下 = **2:3:4:6**（1/9、2/9），但那是**书页装订**系统；实用只有两条——**下边距比上边距大 6mm**、**非对称差 ≥25mm**。
- **网格**：**12 栏**（能被 2/3/4/6 整除）；gutter 固定、栏宽流体，gutter ≈ 栏宽 1/4–1/3；**基线 4/8px**，所有垂直尺寸都是它整数倍。
- **字**：一套模数比例（1.2/1.25/1.333/1.414/1.5/1.618），正文:主标题 **2–4 倍**；行长 **45–90 字符**（中文 25–40 字），行距 **120–145%**（中文 1.6–1.8），两者联动。
- **印刷五查**：300ppi / CMYK / 总墨量 ≤300% / 正文 K100 / 细线 ≥0.25pt；画布含 **3mm 出血 ×2**，文字在安全区。
- **长图换算**：`设计字号 = 目标字号 × (设计宽 ÷ 375)`；1080 宽正文 **≥44px**；一屏一个信息点。
- 材料：[Butterick's Practical Typography](https://practicaltypography.com/)、[Canons of page construction](https://en.wikipedia.org/wiki/Canons_of_page_construction)、[ISO 216](https://en.wikipedia.org/wiki/ISO_216)、[Bleed (printing)](https://en.wikipedia.org/wiki/Bleed_(printing))、[W3C clreq](https://www.w3.org/TR/clreq/)
- → **全部尺寸表、九平台规格、可抄 CSS、20 条反模式、18 项自检见 `editorial-layout.md`**

### 支线 G · 品牌视觉与 Logo（做"一个品牌"而不是"一个页面"）
- **顺序不能反**：定位（3 个形容词 + 3 个反义词）→ 语言（形/色/字/图/动/声）→ 系统（token 与网格）→ 资产（文件与手册）。从 logo 开始的项目，评审时一定被打回且说不出原因。
- **标志七型**：字标 / 字母标 / 图形标 / 抽象标 / **组合标（新品牌默认）** / 徽章 / 动态标。徽章缩到 24px 必糊；动态标必须带静态兜底。
- **构造用 24dp 网格**：内容区 20×20、padding 2、基形 **方 18 / 圆 20 / 竖矩 20×16 / 横矩 16×20**、圆角 2、描边 2（复杂处 1.5）。**一个标志只允许两档笔画。**
- **清space 必须可计算**：字高口径 0.5x–1x / 半符号口径（符号圆直径的一半）/ 高度折半。**写"留足空间"等于没写。**
- **最小尺寸**：数字 **40px**、印刷 **10mm**；40–80px / 9–18mm 换简化版；通用公式 **最细笔画 ÷ 0.75px**。
- **品牌色是种子色**：选色四问（对比度余量 / 色阶可生成性 / 印刷可复制 / 行业反差）；色阶三路线（HCT tone / Radix 12 步语义 / Leonardo 对比度优先）**选一条不许混**；**暗色不是反色，是 tone 重映射（primary 40↔80、outline 50↔60）**。
- **主色占屏 ≤10%**，不许当图表分类色，语义色不与主色同色相。
- **商标 ≠ 版权**：版权自动产生，商标必须注册；尼斯 **1–34 商品 / 35–45 服务**；互联网产品至少 9/35/42 类。
- 材料：[Material Icons 规范](https://m3.material.io/styles/icons/designing-icons)、[Carbon Icons](https://carbondesignsystem.com/elements/icons/usage/)、[Radix Colors 12 步](https://www.radix-ui.com/colors/docs/palette-composition/understanding-the-scale)、[material-color-utilities](https://github.com/material-foundation/material-color-utilities)、[Adobe Leonardo](https://github.com/adobe/leonardo)、[Apple HIG App icons](https://developer.apple.com/design/human-interface-guidelines/app-icons)、[NN/g 语气四维](https://www.nngroup.com/articles/tone-of-voice-dimensions/)
- → **决策树、tone 全表、清space CSS、交付清单、20 条反模式、18 项自检见 `brand-identity.md`**

### 支线 H · 暗色模式（"反一下色"和"设计一套暗色"是两件事）
- **先问该不该做**：正常视力用户浅色更优（**字号越小差距越大**）；暗色的正当理由是低视力/白内障、暗环境、OLED 省电、沉浸媒体、长文选项。**中后台不要默认暗色。**
- **表面层级是重排不是反相**：亮色靠阴影表达高度，暗色靠**表面变亮**。亮色跨度 1.23（98→90），暗色跨度 **1.50**（tone 6→22）——**暗色需要更大的层级差**。
- **三套可抄值**：M3 `surface 6 / cLow 10 / c 12 / cHigh 17 / cHighest 22`；Ant `lighten(0/8/12/26)`；Carbon `#161616 → #262626 → #393939`。底色默认**深灰**，纯黑只给 OLED 省电场景（有滚动拖影）。
- **文字不用纯白**：M3 tone 90 / Ant 85% 白 / Carbon `#f4f4f4` / Radix 第 12 步，四家一致。四档 **85/65/52/32**；**Ant 原生 45% 在纯黑上只有 4.43，不达标**。
- **边框要 3:1**：`#6f6f6f` 起步；Ant 的 `#424242` 只有 2.09:1，过不了 1.4.11。
- **状态方向反转**：hover 提亮、scrim 60–80%、skeleton 比底亮一档、focus 环用亮色。
- **切换三件套顺序**：`meta color-scheme` → head 内联脚本 → CSS；另设 `:root{color-scheme:light dark}` 管滚动条与原生控件。
- 材料：[M2 Dark theme](https://m2.material.io/design/color/dark-theme.html)、[M3 color-utilities 源码](https://github.com/material-foundation/material-color-utilities)、[Ant 暗色算法](https://github.com/ant-design/ant-design/blob/master/components/theme/themes/dark/colors.ts)、[Carbon g100](https://github.com/carbon-design-system/carbon/blob/main/packages/themes/src/v10/g100.ts)、[Apple HIG Dark Mode](https://developer.apple.com/design/human-interface-guidelines/dark-mode)、[NN/g Dark Mode](https://www.nngroup.com/articles/dark-mode/)、[MDN color-scheme](https://developer.mozilla.org/en-US/docs/Web/CSS/color-scheme)、[微信 DarkMode](https://developers.weixin.qq.com/miniprogram/dev/framework/ability/darkmode.html)
- → **对比度实测表、四端实现、22 项自检、20 条反模式见 `dark-mode.md`**

### 支线 I · 性能与设计（"好看"必须先"看得见"）
- **性能是设计约束，不是开发收尾**。首屏主视觉选什么、用几套字体、上不上视频，**在稿子上就已经定了 LCP 的上限**。
- **七个阈值**：LCP **2.5s** / INP **200ms** / CLS **0.1**（差：4.0 / 500 / 0.25）；辅助 TTFB 800ms、FCP 1.8s、TBT 200ms、SI 3.4s。取 **p75**，移动/桌面分段，**看现场不看本地**。
- **LCP 四分解**：TTFB ~40% / load delay <10% / load duration ~40% / render delay <10%。**单独优化一段会把时间转移到另一段**，必须四段一起看。
- **首屏视频 ≈ 2.5MB**（5s 1080p@4Mbps）：它不是 LCP 元素，但抢带宽把 LCP 推后。**想要氛围，先把氛围放到第二屏**。
- **图片 25 倍浪费**是常态：400×300 的位配 4000×3000 源图。DPR 翻倍 = 像素 **4 倍**。格式：照片 AVIF → WebP → JPEG；图标 SVG；动图 `<video>`。
- **字体是最易被低估的成本**：CJK >10000 字形，未子集化 3–8MB；不写 `font-display` 时 Safari **无限期阻塞文本**。
- **只动 `transform` / `opacity`**；`will-change` 一个全屏层就是 **7.93MB** 显存，不许常驻。
- **全屏每帧重算 = 红灯**（全屏 blur / canvas 粒子 / 多层视差）。**限定面积**是唯一便宜的解法。
- **预算**：关键路径 <170KB、TTI <5s（3G）。超了只有三选一：优化 / 删掉 / 不加。
- 材料：[web.dev Web Vitals](https://web.dev/articles/vitals)、[Optimize LCP](https://web.dev/articles/optimize-lcp)、[Performance budgets 101](https://web.dev/articles/performance-budgets-101)、[Lighthouse scoring](https://developer.chrome.com/docs/lighthouse/performance/performance-scoring)、[微信 代码包体积优化](https://developers.weixin.qq.com/miniprogram/dev/framework/performance/tips/start_optimizeA)
- → **价格表、图层内存算术、六类页面预算、三档决策分级、小程序五手段、18 项自检见 `performance-design.md`**

### 支线 J · 设计交付与协作（画完不等于交完）
- **交付的是决策，不是图**。稿子里有 intent / rule / value 三层，只给 value，开发必须反推前两层——偏差从这里开始。**检验法：拿掉设计稿，开发能做出第二个页面吗？**
- **spec 九字段**：标识（含版本与状态）/ 布局 / 间距尺寸 / 字体颜色 / 交互状态 / 行为边界 / 无障碍 / 素材链接 / 沟通字段。
- **只标例外**：例外值 + 对齐关键线 + 尺寸约束 + 断点切换。全量标注 = 没有标注。
- **9 态都要有出处**：default / hover / focus / active / selected / disabled / **read-only** / error / loading。Carbon 的 4.5:1 例外**只给 disabled**。
- **命名四套**：图层 / 组件（斜杠分级）/ 变体属性（**禁视觉名**）/ token（CTI）。**默认变体 = 左上角 = 最常用那版**。
- **AC 用 Given/When/Then 3–5 步**：只验**用户看得见**的结果，一个 When 只做一个动作。
- **评审 30 分钟/周**、round robin、quota **2 正 1 改**、**必须有决策/待定/负责人/期限**。
- **走查三遍法**：主流程 → 交互逐条 → 才看像素。**P0 = 0 才可上线**，P1 豁免要写"谁批、何时补"。
- **改默认值 = MAJOR**（SemVer 规则映射），MAJOR 必带迁移表/codemod。
- 材料：[Carbon Component checklist](https://carbondesignsystem.com/getting-started/contributing/component-checklist/)、[Figma Dev Mode](https://help.figma.com/hc/en-us/articles/15023124644247-Guide-to-Dev-Mode)、[SemVer](https://semver.org/)、[NN/g Design Critiques](https://www.nngroup.com/articles/design-critiques/)、[Cucumber Gherkin](https://cucumber.io/docs/gherkin/reference/)
- → **9 字段 spec、P0–P3 门禁、DTCG 管线、回归四层、六个指标、20 项自检、4 套模板见 `handoff-collaboration.md`**

### 支线 K · 内容设计与 UX 文案（界面上的每个字都是设计）
- **三级文案尺寸**：long ≥3 段（引导页/帮助） / short 2–3 段（对话框/结果说明） / micro <3 句（按钮/标签/toast/错误——**占界面 80%**）。先判尺寸再写。
- **五条不可商量原则**：① 动词开头 ② 说会发生什么不说当前状态 ③ 不加冠词（the/a） ④ **禁用 OK**（永远写具体动作） ⑤ 保留用户输入（校验失败不清空）。
- **扫描数据**：用户在线只读 **20%** 文字、前 **11 字符**决定是否继续读、倒金字塔是黄金法则——结论先行、细节后补。
- **按钮文案**：动词开头 **2–4 词**（英文）/ **2–4 字**（中文）；描述结果状态而非当前操作；禁 OK/Submit/Confirm/Click here/Done；需更多信息加省略号（…）；中文不加"请"。
- **错误文案三层结构**：① 发生了什么 ② 为什么 ③ 怎么修。**禁用词表 9 条**（invalid/非法/incorrect/请重新输入/Oops/We're having trouble/格式不正确/出错了/请稍后重试）。位置紧贴字段下方 4–8px、时机 = 失焦 + 提交（不一进来就红）。中文 **≤30 字**。10 类模板覆盖必填为空/格式错误/长度不足/已存在/不匹配/网络/权限/系统/操作失败/超时。
- **空态五件套**（标题 + 说明 + 按钮 + 次要链接 + 视觉）与**五种空态**区分（首次/搜索无果/筛选无果/错误/完成）。**禁俏皮话、禁纯 "No data"**——失败不要伪装成无数据。
- **语气四维**（NN/g）：正式↔随意 / 严肃↔幽默 / 尊重↔不恭 / 就事论事↔热情 + **场景矩阵**（错误禁幽默、危险确认升正式、成功可升热情）。**禁用语气 6 条**（责怪用户/道歉过多/We 指代不明/过度承诺/网络流行语/强迫语气）。
- **表单文案**：标签名词 ≤8 字不加句号、占位符写示例**禁替代标签**、帮助文案 ≤16 字与错误共用位置、设置项说"开启后做什么"而非"是否开启"。
- **对话框与 Toast**：标题说发生了什么 ≤1 行（禁"提示/警告"）、正文写后果、按钮具体动作。Toast 写具体什么成功 ≤20 字、成功 3s 消失错误不消失。
- **大小写**：默认 **sentence case**（仅首字母和专有名词大写），禁全大写——Apple + Microsoft + GOV.UK + M3 **四体系共识**。全大写降可读性 10%、读屏逐字母读。
- **数字日期**：在线用数字不用拼写（2 不用 two）、千分位（1,000）、大数用万/亿、日期不用序数词（`2 June` 不用 `2nd June`）、范围用 to 不用 `-`。
- **国际化**：文案膨胀 **+40%**（英文→德文）、禁拼接字符串用模板变量、ICU 复数规则、RTL 镜像（不能只翻转文字方向）。
- **可访问性**：图标按钮必须有 `aria-label` 且与可见文案一致、链接文字有意义（禁 "Click here"/"Learn more" 无上下文）、读屏测试、阅读等级 ≤Grade 8、句长 ≤20 词/≤30 字。
- **文案系统化**：文案 token JSON 结构（`buttons`/`errors`/`empty`/`toast` 四桶）、评审清单 8 项、链接文案检查脚本。
- 材料：[Apple HIG Writing](https://developer.apple.com/design/human-interface-guidelines/writing)、[NN/g Error-Message Guidelines](https://www.nngroup.com/articles/error-message-guidelines/)、[NN/g UI Copy](https://www.nngroup.com/articles/ui-copy/)、[NN/g Tone of Voice 4 Dimensions](https://www.nngroup.com/articles/tone-of-voice-dimensions/)、[NN/g UX Copy Sizes](https://www.nngroup.com/articles/ux-copy-sizes/)、[Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/top-10-tips-style-voice)、[GOV.UK Style Guide A–Z](https://www.gov.uk/guidance/style-guide/a-to-z-of-gov-uk-style)、[Ant Design 反馈规范](https://ant.design/docs/spec/feedback-cn)、[优设 B 端文案规范](https://www.uisdc.com/b-product-copywriting)
- → **三级尺寸 + 五原则 + 按钮规则 + 错误三层 + 禁用词 + 10 类模板 + 空态五件套 + 语气矩阵 + 表单/对话框/Toast/引导/导航文案 + 大小写 + 标点 + 数字 + 国际化 + 文案 token + 12 场景速查 + 20 反模式 + 18 自检 + 6 段可抄代码见 `ux-writing.md`**

### 支线 L · 演示文稿与幻灯片版式（不是"缩小的文档"是"放大的瞬间"）
- **3 秒法则**：每张幻灯片停留 20–60 秒，观众 3 秒内决定是否继续看。倒金字塔——结论先行。
- **尺寸**：16:9（1920×1080）为事实标准（PowerPoint/Google Slides/Keynote/reveal.js 全部默认）。4:3 仅旧投影和打印讲义。同一文件不支持混比例。
- **安全区**：标题安全区边距 ≥5%（96px/2.54cm）、动作安全区 ≥3%（58px/1.48cm）、投影过扫预留四边 0.5"。
- **字号阶梯**：封面 44–60pt / 章节标题 36–44pt / 幻灯片标题 28–36pt / 正文 24–28pt / 标注 20–22pt / 页脚 14–16pt。**最小 24pt（线上 28pt）**。阅读型讲义可降至 14pt。全篇同一层级字号一致（母版设的）。单页最多 3 种字号。
- **字体**：Sans-serif 系统字体（Helvetica/Calibri/Arial/思源黑体/微软雅黑）。全篇最多 2 种。禁 Comic Sans/ALL CAPS/全加粗/Word Art/阴影描边。
- **可读性验证**（Duarte 法）：屏幕对角线英寸数 = 后退英尺数。
- **文字密度**：Godin（≤6 词/页）/ 5×5（5 行×5 词）/ 6×6 / 1-6-6（1 观点×6 条×6 词）/ 中文 5×5 = 5 行×10 字。
- **母版与占位符**：6–8 种版式上限，每种命名。用占位符不用手动文本框（保无障碍阅读顺序）。logo 高 0.5–1"。
- **动画 vs 转场**：动画=单元素（入场/退出/强调/动作路径），转场=整张幻灯片（每页仅 1 个）。三档：细微 Fade✅ / 华丽❌。全篇统一 1 种转场，≤0.5s，禁声音。Morph 用于跨页位移非炫技。
- **投影对比度**：正文 ≥4.5:1 / 大字 ≥3:1。投影损失 20–40% 需高 50%。禁红绿/红蓝/亮色背景。
- **可访问性**：WCAG 2.1 AA。占位符/alt 文本/Accessibility Checker 0 错误/闪烁 ≤3 次/秒（2.3.1 不可豁免）/ ≤25% 面积。
- **线上演示**：字号 +4pt / 减少动画 / 高对比 / 关通知。
- **中文演示**：最小 26–28pt / 行距 1.4–1.6 / 思源黑体 / 中英加空格。
- **版式构图**：三分法则 / Z 模式 / 留白 30–50% / 视觉引导面向内部。
- **演示节奏**：主题演讲 15–30s/页 / 商务 30–60s / 教学 60–120s。切换后等 2–3s 再讲。
- 材料：[Microsoft Support - 动画与转场区别](https://support.microsoft.com/en-us/office/the-difference-between-animations-and-transitions-bae174a4-dad3-4268-bf9c-c201a70995f1)、[WCAG 2.3.1 闪烁阈值](https://www.w3.org/WAI/WCAG22/UNDERSTANDING/three-flashes-or-below-threshold)、[WebAIM 对比度检查器](https://webaim.org/resources/contrastchecker/)、[reveal.js](https://github.com/hakimel/reveal.js)、[Slidev](https://github.com/slidevjs/slidev)
- → **尺寸表 + 安全区 + 字号阶梯 + 密度规则 + 母版步骤 + 动画转场分类 + 投影对比度 + 12 场景速查 + 20 反模式 + 18 自检 + 6 段可抄代码见 `presentation-design.md`**

### 支线 M · 动效编排与状态机（动效 bug 八成不在曲线，在状态没建模）
- **三层分工**：L1 单动效（该不该动 / 多久 / 什么曲线）走 `motion-system.md`；L2 编排（≥2 元素或有先后）；L3 状态机（互斥状态 / 跨视图配对 / 会被打断）走 `motion-orchestration.md`。
- **四种时间结构**：并行 `max(d)` / 串行 `Σd` / 重叠 `d₁+(1−p)d₂` / 交错 `d+(n−1)s`。硬约束 `T ≤ 400ms`，反解 `s ≤ (400−d)/(n−1)` → 6 项×30ms=350ms ✅ / 12 项×40ms=640ms ❌，**n>6 改整组淡入**。
- **单位统一表**：CSS 秒（`0.3s`）· WAAPI 毫秒（`300`，且默认 easing 是 `linear`）· Motion 秒（`0.3`）· React Transition Group 毫秒（`timeout={300}`）。
- **FLIP 四步**：First 读 → Last 改完再读 → Invert（`invertY = first.top − last.top`）→ Play。**100ms 响应窗口**内做预计算；批量**先全读再全写**；同一时刻只允许一个 FLIP 编排。
- **列表增删四策略**：新增让位 / 删除合拢（退场项 `position:absolute` 脱离布局流）/ 重排走 FLIP 位移 / 整批替换串行。**key 禁用 index**。
- **共享元素两路线**：View Transitions（快照，UA 默认 **0.25s / ease / both**，name 必须唯一、单例、跨文档 MPA）vs Motion `layoutId`（真实 DOM transform、允许多个同名、能补滚动）。
- **状态机**：四态 `entering/entered/exiting/exited` + 状态×事件矩阵；连点时 `exiting` 收 `OPEN` 应反向 `entering` 且从当前值继续；动画轴与数据轴做并行 region。
- **中断与取消**：三策略（重启 / `composite:add` / `finish`）；保态用 `commitStyles()` 不用长期 `fill:forwards`；清理挂 `finished`+`finally`，别只挂 `transitionend`（四坑）。
- **CSS 进出场四件套**：`@starting-style` + `display` + `overlay` + `allow-discrete`；两处顺序陷阱（简写之后、原规则之后）；离散属性 50% 翻转、display 例外。
- **降级分两层**：CSS `prefers-reduced-motion` ＋ **JS 层**（WAAPI / Svelte / View Transitions 不吃 CSS media 归零）；编排要**整段跳过**而非逐项归零。WCAG **2.3.3 AAA**（motion animation 可关闭，essential 例外）。
- 材料：[MDN View Transition API](https://developer.mozilla.org/en-US/docs/Web/API/View_Transitions_API/Using)、[W3C CSS View Transitions L1](https://drafts.csswg.org/css-view-transitions-1/)、[Paul Lewis FLIP](https://aerotwist.com/blog/flip-your-animations/)、[Motion AnimatePresence](https://motion.dev/docs/react-animate-presence)、[React Transition Group](https://reactcommunity.org/react-transition-group/transition)、[W3C SC 2.3.3](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html)
- → **四种时间结构 + 总时长公式 + 两代 stagger API + FLIP 算式 + 列表四策略 + VT 伪元素树与三 promise + 四态矩阵 + WAAPI 全默认值 + 16 场景 + 20 反模式 + 20 自检 + 8 段可抄代码见 `motion-orchestration.md`**

### 支线 N · 国际化与本地化（出海不是加个语言包，是三层同时改）
- **先判三层**：① **标记层** `<html lang>` + `dir`；② **布局层** 文案膨胀弹性 / CSS logical properties / RTL 镜像；③ **数据层** 复数 / 日期 / 数字 / 姓名 / 排序。翻译只解决字符串，三层不动必然在 RTL 或复数上翻车。
- **⚠️ 修正一条自己写过的错**：`ux-writing.md` §13 的「按钮容纳 **+40%**」**对 microcopy 是错的**。W3C 转引 IBM 表：英文 **≤10 字符平均膨胀 200–300%**（Flickr `views` 实测意语 **3.0×**）、11–20 为 180–200%、21–30 为 160–180%、31–50 为 140–160%、51–70 为 151–170%（**原表非单调，照录**）、>70 为 130%。→ **microcopy 2–3× / 短文案 1.6–2.0× / 段落 1.3×**；Microsoft `+40%` 只是伪本地化测试串加长量。余量做成「能伸缩」（`min-inline-size` + 换行/省略兜底），不是「更宽的按钮」。
- **`lang` ≠ `dir`**：WCAG **3.1.1 A**（H57 在 `html` 写 lang）+ **3.1.2 AA**（H58 局部 passage）；BCP 47 / IANA；`lang` 推不出方向（`az` 可 LTR 可 RTL）。**W3C 硬禁令「Never use CSS to apply the base direction」**，RTL 必须 `<html dir="rtl">`（连带 8 项：块右对齐 / 双向流 / 标点 / 表格列 / 表单 / alt·title / CSS 自动镜像 / overflow）。方向未知用 `dir="auto"`（看首强字符、不 foolproof）+ `dirname` + `bdi` + `&rlm;`U+200F / `&lrm;`U+200E + Unicode isolates。
- **方向相关 CSS 全改逻辑属性**：`inline`/`block` 轴 + `start`/`end`；`margin-left→margin-inline-start`、`width→inline-size`、`left→inset-inline-start`、`text-align:left→start`。**镜像白名单**（布局 / 右对齐 / 导航按钮 / 方向图标 / 字段图标 / 进度条 / 时间线）与**黑名单**（数字 / 未翻译文本 / 时钟电话号 / 图表 / 媒体播放控件 / 顺时针刷新 / 物理对象 / 右手持物 / 斜线）；两条易错：**一般进度条镜像但媒体进度条不镜像**、**数字不镜像 ≠ 不本地化**（`ar-EG` 用 `arab` 字形）。
- **复数不是 `n===1`**：CLDR 六类 `zero/one/two/few/many/other`，**`one` ≠ 数字 1**（法/印地语 0→`one`，俄语 21→`one` 而 11→`many`），`other` 必需，中/日/韩/印尼/越南**仅 `other`**（中文产品本地测不出分支，最易漏），`ar` 全 6 类、`ru`/`pl` 四类、`fr` 三类。
- **ICU MessageFormat 三铁律**：禁拼接字符串 / 整句完整翻译 / `select` 外层 `plural` 内层；`offset:1`、`=0`、`=1`、`#`、ASCII 撇号转义与推荐 U+2019、skeleton `::` 优于 string pattern。
- **`Intl` 不是构造器**：10 构造器 + 2 静态方法；本机 Node v22.22.2 实测 **`Intl.DurationFormat` 抛 TypeError（MDN 已列但运行时未实现）→ 必须能力检测 + 降级**；`zh_cn` 抛 `RangeError`，BCP 47 用 `zh-CN`；`localeMatcher` lookup / best fit。数据层记忆点：`03/09/2026` 英美歧义、`hi-IN` **12,34,567.89**、`JPY` 无小数、`ListFormat` 牛津逗号、`Collator` 德/瑞 `ä` 排序相反、`weekInfo` 周起始日（zh 一 / en-US 日 / ar-EG 六）。
- **姓名单一 `Full name`**：W3C 反例——强制拆姓/名会让用户填 `.` 或 `Mr.`；别假设空格分隔、别假设单名不存在（南印/马/印尼）、别按 family name 排序（冰岛 patronymic 按 given name）。
- **没翻译也要能测**：伪本地化五变换（音标 / ①–⑨ U+2460–2468 / `^` 定界暴露截断与拼接 / 唯一 id / 分档加长），`en-XA`·`en-XB`·Windows `qps-ploc*`·RFC 4646 `qaa–qtz` 私有段（**别用 `tk-TM` 会撞真实 locale**）；译者交付包 = 上下文截图 + 字符上限 + 变量说明 + 复数样例 + 术语表。
- 材料：[W3C Text size in translation](https://www.w3.org/International/articles/article-text-size.en)、[W3C QA HTML dir](https://www.w3.org/International/questions/qa-html-dir.en.html)、[W3C Inline bidi markup](https://www.w3.org/International/articles/inline-bidi-markup/)、[MDN CSS logical properties](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_logical_properties_and_values)、[W3C WCAG 3.1.1 / 3.1.2](https://www.w3.org/WAI/WCAG22/Understanding/language-of-page.html)、[CLDR Plural Rules](https://cldr.unicode.org/index/cldr-spec/plural-rules.html)、[ICU MessageFormat](https://unicode-org.github.io/icu/userguide/format_parse/messages/)、[MDN Intl](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl)、[Material Bidirectionality](https://m2.material.io/design/usability/bidirectionality.html)、[W3C Personal names around the world](https://www.w3.org/International/questions/qa-personal-names)
- → **三层判层 + 膨胀表与四因素 + `lang`/`dir` 与 H57/H58 + logical properties 全映射 + 镜像白黑名单 + CLDR 复数类别表 + ICU 嵌套范式 + `Intl` API 实测输出 + 姓名地址与文化适配 + 伪本地化可抄代码 + 12 场景 + 20 反模式 + 20 自检 + 6 段可抄代码见 `i18n-localization.md`**

### 支线 O · 设计系统文档写作（给人读的系统，不是给机器读的约束）
- **先分层再判层**：`design-md-format.md` 的 DESIGN.md 是**给机器读的约束清单**，`handoff-collaboration.md` 的终点是"开发能做出第二个页面"，本支线的终点是"半年后第三个团队也能自己查到、自己改对、自己升级"。先用 **Diátaxis 四象限**（tutorials 不给选择 / how-to 必须能分支 / reference *"Describe and only describe"* / explanation）判清在写哪一种，别混在一页。
- **组件页九段式**：GOV.UK Button 逐节为 `When to use` / `When not to use` / `How it works` / 变体与状态 / Accessibility / Props·API / Research / Recent changes / Help improve。**最容易被砍掉的恰恰是后三段**——它们构成"活文档四件套"（研究证据 / 已知问题 / 近期变更 / 帮助改进），砍掉文档就停止生长。
- **能验收才算规范**：五问（找得到 / 看得懂 / 抄得走 / 对得上代码 / 半年后有人改）+ 字段清单逐条打分；示例代码五条硬规则（可直接复制运行、零隐式依赖、给出 import、结果与截图一致、随版本回归）；Google style highlights：sentence case、第二人称、主动语态、descriptive link text、alt 非文件名、serial comma。
- **版本化与变更**：Docusaurus 官方"多数站点不需要版本化"；真做就守住 `versioned_docs` / `versioned_sidebars` / `versions.json`、版本数 **<10**、preview **2–3** 个、patch 不切版本、旧版 `unmaintained` banner。Keep a Changelog 1.1.0 七原则 + 六类变更 + `[Unreleased]`，**反对把 git log 倒进 changelog**；MAJOR 迁移文档要能被机器校验（codemod / 脚本）。
- **规范引用与 docs-as-code**：`tr.designtokens.org/format/` 是 preview draft（*"Do not reference this version as authoritative"*），权威是 **published 2025.10**；`$description` / `$deprecated` / `$extensions` 直接当文档源。Storybook `tags: ['autodocs']` / `['!autodocs']`、MDX `of={}` 与 attached/unattached、默认六 Doc Block、`Meta` 空行规则、Figma Code Connect 命名一致性 → 文档与代码同源。
- **治理与防腐**：GOV.UK **Useful / Unique**（提案）+ **Usable / Consistent / Versatile**（发布）+ 社区资源 1 个月 / 3 个月阈值；USWDS 三阶段十二子状态与 45 天评论期；新鲜度指标（链接失效率 / props 一致性 / 最后更新 / 示例可运行率）。本技能自举：`mindmap.py` 接线体检 + `build_readme.py` 实时统计，不手抄会过期的数字。
- 材料：[Diátaxis](https://diataxis.fr/)、[GOV.UK Button](https://design-system.service.gov.uk/components/button/) 与 [Contribution criteria](https://design-system.service.gov.uk/community/contribution-criteria/)、[Docusaurus Versioning](https://docusaurus.io/docs/versioning)、[Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/)、[Storybook Autodocs](https://storybook.js.org/docs/writing-docs/autodocs)、[DTCG 2025.10](https://www.designtokens.org/TR/2025.10/format/)、[Google style highlights](https://developers.google.com/style/highlights)
- → **四象限判层 + 九段式逐节表与五问验收 + 信息架构四条地基 + 完整填充范例 + 活文档四件套 + 成熟度与 semver 对照 + 版本化目录结构 + changelog 模板 + 迁移文档 + Storybook/MDX 配置 + 治理准入 + 漂移指标 + 12 场景 + 20 反模式 + 20 自检 + 6 段可抄代码见 `design-system-docs.md`**

### 支线 P · AI / 生成式设计工具链（产能层不是判断层）
- **先判哪层交出去**：五层地图（意图与约束 / 生成 / 编辑 / 代码化 / 验收）每层都要有人工闸门；**三类活不交给 AI**——定受众与语气、判上线与否、担法定责任。AI 只出候选，不出结论。
- **合规是地基不是附录**：中国《人工智能生成合成内容标识办法》**2025-09-01 施行**，显式标识（用户可感知）+ 隐式标识（文件元数据）双轨；第 4/5/6/9/10 条 → 导出·下载·复制保留标识、元数据三类要素、传播端三档文案「属于 / 可能为 / 疑似」、无标版协议与日志 ≥6 个月、**禁止提供抹除标识的功能**；与《暂行办法》令第 15 号第 7/11 条串成授权链。出海叠加 **EU AI Act Art. 50（2026-08-02）**。GB 45438-2025 的具体尺寸/时长数值未取得原文，不臆造。
- **两条不能混的裁决**：USCO 官方解读 *"but not the mere provision of prompts"* → 提示词**不构成作者身份**，要留 brief→参考→草图→迭代→人工选择→终稿的**可举证创作链**；C2PA Content Credentials 只断言溯源清单格式良好·未篡改·签名可信·与 asset 绑定，**不证明版权归属、不判断事实真伪**。**法定内容标识 / 内容凭证 / 版权与商用授权三者互不替代**。
- **把风格写成契约**：`DESIGN.md` 九章（第 9 章 `Agent Prompt Guide` 不可省）是**给 AI 读的约束**，设计系统文档站是**给人读的系统**（接支线 O，别混写）。提示词按 `Identity → Instructions → Examples → Context` 四区块组织，结构化输出、固定模型快照、prompt 入代码库、换版跑 eval，按 SemVer 判 MAJOR/MINOR/PATCH。
- **验收要能判 PASS/FAIL**：AI Slop Test（三人盲测）+ 8 维 DO/DON'T + 12 类固有缺陷逐条回查 + **HAX G1–G18** 给 AI 功能界面落点（能力边界 / 可关闭且记住 / 可纠错 / 全局控制 / 变更通知）+ 4 段可运行脚本进 CI。**选型三问**先于 star：许可（GPL-3.0 / AGPL-3.0 / NOASSERTION 三红灯）、活源（pushed_at >12 个月不进生产依赖）、可验收。
- 材料：[CAC 标识办法](https://www.cac.gov.cn/2025-03/14/c_1743654684782215.htm)、[CAC 暂行办法令第 15 号](https://www.cac.gov.cn/2023-07/13/c_1690898327029107.htm)、[EU AI Act Article 50](https://artificialintelligenceact.eu/article/50/)、[USCO Copyright and AI](https://copyright.gov/ai/)、[C2PA Specifications](https://c2pa.org/specifications/)、[Microsoft HAX Design Library](https://www.microsoft.com/en-us/haxtoolkit/library/)、[OpenAI Prompt engineering](https://platform.openai.com/docs/guides/prompt-engineering)
- → **五层地图 + 14 条设计动作 + 中欧美三法域矩阵 + 三概念分离 + 可举证创作链 + 提示词四区块与 SemVer + HAX 18 条界面落点 + AI Slop Test 与 12 类缺陷 + 18 仓库 API 实测 + 12 场景 + 20 反模式 + 20 自检 + 6 段可抄代码见 `ai-design-toolchain.md`**

### 支线 Q · 设计伦理与包容性（对称优先，默认值即决定）
- **先立立场**：设计伦理不是道德劝告，是**可写进 CI 的路径长度、按钮构型、点击次数和默认值**。三条不可商量：① 对称优于说服；② 默认即决定（预勾选/沉默不构成同意）；③ **意图不是辩护理由**（CPPA §7004(c)：知情不修、刻意不知情同样可成立）。
- **同意 UI 有测量方法**：CPPA §7004(a)(2) 规定 opt-out 步数**从点击 `Do Not Sell or Share My Personal Information` 起算到请求完成**、opt-in **从首次表示兴趣起算到完成**，拒绝路径不得更长/更难/更耗时；`Accept All + More Information / Preferences`、`Yes + Ask me later` 均被点名为不对称，正解是 `Accept All + Decline All`、`Yes + No`。另四条：易读、禁双重否定与按钮顺序反转、不捆绑不兼容用途、端到端可执行（坏链/循环/等待都算 FAIL）。
- **中国法域五条底线**：PIPL 第 14 条（充分知情·自愿·明确，目的变更须重新同意）/ 15 条（**便捷撤回**）/ 16 条（**不得因不同意拒绝提供服务 → cookie wall 红线**）/ 17 条（显著·清晰易懂告知四项且规则便于查阅保存）/ 24 条（自动化决策须给非个性化选项或便捷拒绝、禁不合理差别待遇）。
- **两条能直接量化的红线**：《互联网广告管理办法》第 10 条「一键关闭」→ 点击 **≤1**、**无需计时**、**同页同文档不复弹**，开屏广告同样适用；《网络交易监督管理办法》第 13/16/17 条 → 授权类 `defaultChecked` 一律 false、敏感信息逐项同意、退订显著·简便·免费且拒绝后立即停止、搭售**不继承历史默认选择**。
- **⚠️ 反陈旧裁决（本支线最该记住的一条）**：第十八条经 **2025-03-18 总局令第 101 号修正、2025-05-01 施行**，旧版「自动续费日期**前五日**」已被现行「**等日期前**」取代；现行是**接受服务前 + 每次展期/续费日期前**两个时点显著提醒 + 服务期内**显著简便的随时取消或变更** + 不得收不合理费用。**别把旧稿、旧教程、AI 复述当现行法**；同理 `deceptive.design` 现行 **18 类**已不是 `Roach Motel / Privacy Zuckering` 那套。
- **未成年人是另一套产品构型**：国务院令第 766 号第 42 条防沉迷制度与年度公开、43 条**时段/时长/功能/内容**四维度 + 监护人**时间/权限/消费**三类管理、44 条**单次与单日累计**双消费限额、45 条打榜/应援集资/刷量控评**整体下线**、47 条下载·注册·登录三处适龄提示。
- **包容 ≠ 无障碍**：Microsoft 三原则（Recognize exclusion / Solve for one, extend to many / Learn from diversity）+ Persona Spectrum（永久·临时·情境）；Inclusive Design Principles 七原则；**W3C COGA 3.1–3.8 八目标**与 `Test with real users`（须包含认知与学习障碍者本人）。**无障碍审查看「能不能用」，伦理审查看「是不是被引导着用」，两张表分别签字**——情境性认知负荷正是 dark pattern 的作用面。
- 材料：[EDPB Guidelines 03/2022 v2.0 PDF](https://www.edpb.europa.eu/system/files/documents/2023-02/edpb_03-2022_guidelines_on_deceptive_design_patterns_in_social_media_platform_interfaces_v2_en_0.pdf)、[CPPA final regs PDF](https://cppa.ca.gov/regulations/pdf/20230329_final_regs_text.pdf)、[PIPL 全文](http://www.npc.gov.cn/npc/c2/c30834/202108/t20210820_313088.html)、[未成年人网络保护条例](https://www.gov.cn/zhengce/content/202310/content_6911288.htm)、[网络交易监督管理办法 2025 修正版](http://www.hunan.gov.cn/zqt/zcsd/202508/t20250804_33757595.html)、[deceptive.design types](https://www.deceptive.design/types)、[W3C COGA](https://www.w3.org/TR/coga-usable/)、[Inclusive Design Principles](https://inclusivedesignprinciples.info/)
- → **24 节 + 现行 18 类 + EDPB 六类机制 + §7004 五原则 + 三地法域决策矩阵 + 20 反模式 + 22 自检 + 4 段可抄代码（3 段 Python 已实跑）见 `design-ethics-inclusion.md`**

### 支线 R · 组件 API 设计与组合模式（三份所有权，契约先于样式）
- **先立立场**：组件 API 不是 props 清单，是**三份所有权的书面划分**——**状态所有权**（受控 / 非受控）、**渲染所有权**（组合 / 换元素）、**契约与演进所有权**（键盘无障碍 / 语义冻结 / 版本判级）。组件库"不好用"八成不是样式问题，而是状态两边都存、props 被中间层吞掉、键盘契约没人认领、改默认值却只发 PATCH。
- **受控判定只有一条**：React 官方定义 controlled 是"重要信息由 props 驱动"、uncontrolled 是 local state 驱动；Radix 上游 `useControllableState` 源码用 `const isControlled = prop !== undefined` 判定，开发态警告**组件生命周期内不得在受控与非受控之间来回切换**；React `<input>` 契约要求 `value` / `checked` 与 `onChange` 同步更新、**无 `onChange` 即只读**、`defaultValue` / `defaultChecked` 只定义初始值、`value` 不得为 `undefined` / `null`。
- **状态提升不是"把 state 挪上去"**：先确定谁是唯一数据源，再让兄弟组件共享；`v-model` 是 `modelValue` + `update:modelValue` 的语法糖而非双向绑定魔法，Vue props 仍是 **one-way-down**（Boolean absent cast `false`、`[String, Boolean]` 顺序影响 casting）→ `component-api-design.md` §3、§5。
- **组合优于继承，但"换元素"有五套互不相同的 API**：Radix `asChild` + `Slot.mergeProps`（child props override / 事件串联 / `style`·`className`·`aria-describedby` 合并）、Ariakit `render={<el/>}`（元素形态自动合并 `style`/`className`/`ref`/event，含 `null` 的显式值覆盖、`undefined` 忽略；**显式 render function 不自动合并 HTML props**）、MUI `component` / `slots` / `slotProps`（`component` 保留 root slot 样式、`slots` 可能丢样式、`slotProps` 可为 callback 收 `ownerState`）、Vue `<slot>` / named / scoped slots、原生 `children` / render prop。**别把其中一套的合并规则套到另一套上**。
- **自定义组件必须"开放扩展"**：spread 剩余 props、转发 ref、合并 `className` / `style`、事件处理器组合而非覆盖（Ariakit 官方四条规则 + "Flat is better than nested"）。中间层吞掉一个 prop，等于把用户的 `aria-*` / `data-*` / `onClick` 一次性全丢。
- **⚠️ React 19 反陈旧裁决（本支线最该记住的一条）**：官方 `forwardRef` 页已标 `### Deprecated`，原文 *"In React 19, `forwardRef` is no longer necessary. Pass `ref` as a prop instead."*，React 19 博客写明 *"In future versions we will deprecate and remove `forwardRef`."* → **写组件 API 规范必须标注目标 React 版本**。同时官方 Pitfall *"Do not overuse refs."* / *"If you can express something as a prop, you should not use a ref."* 点名 `{ open, close }` 命令式 handle 为反例，正解 `<Modal isOpen={isOpen} />`。
- **键盘契约是 API 的一部分**：WAI-ARIA APG 要求所有交互元素可键盘操作、**复合组件通常只让一个元素进 tab sequence**（roving `tabindex` 或 `aria-activedescendant` 二选一）、focus 与 selection 必须视觉区分、modal dialog 的 `Tab` / `Shift+Tab` 循环 + `Escape` 关闭 + 关闭后焦点返回触发元素；状态以 `data-*` 暴露给样式与测试，别让样式去猜 DOM 结构。
- **契约要能摆到面板上、判进版本号**：Storybook 官方 *"ArgTypes encode basic metadata for args, such as name, description, and defaultValue for an arg."*，`control: false` 保留文档不给控件、`table.disable: true` 连文档删、`sort: 'requiredFirst'` + `expanded: true` 把必填项摆前；TypeScript 用可辨识联合把互斥 props 变成类型错误。**六个冻结面**（默认值 / props 合并优先级 / 受控判定 / 键盘与 tab stop 策略 / 自动 `role`·`aria-*` / ref 形状）任一被改 → **MAJOR 且必须带可执行 codemod**；新增可选 prop·slot → MINOR；文档与类型注释 → PATCH。
- 材料：[React Composition vs Inheritance (legacy docs)](https://legacy.reactjs.org/docs/composition-vs-inheritance.html)、[React Sharing State Between Components](https://react.dev/learn/sharing-state-between-components)、[React `<input>`](https://react.dev/reference/react-dom/components/input)、[React `forwardRef`（Deprecated）](https://react.dev/reference/react/forwardRef)、[React 19 blog](https://react.dev/blog/2024/12/05/react-19)、[Radix useControllableState 源码](https://github.com/radix-ui/primitives/blob/main/packages/react/use-controllable-state/src/use-controllable-state.tsx)、[Radix Slot 源码](https://github.com/radix-ui/primitives/blob/main/packages/react/slot/src/slot.tsx)、[Ariakit Composition](https://ariakit.org/guide/composition)、[MUI Overriding component structure](https://mui.com/material-ui/customization/overriding-component-structure/)、[Vue Slots](https://vuejs.org/guide/components/slots.html)、[Vue `v-model`](https://vuejs.org/guide/components/v-model.html)、[WAI-ARIA APG Keyboard](https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/)、[Storybook Controls](https://storybook.js.org/docs/essentials/controls)
- → **23 节 + 三份所有权框架 + 五套换元素 API 对照 + 16 场景矩阵 + 20 反模式 + 22 自检 + 4 段可抄代码（3 段 Python 已实跑全 PASS）+ 15 仓库 GitHub API 实测见 `component-api-design.md`**

### 支线 S · 设计度量与用户研究（"好不好"不能只剩「我觉得」）
- **先判要度量什么**：ISO 9241-11:2018 把可用性拆成三件独立的事——Effectiveness（任务对不对）/ Efficiency（快不快）/ Satisfaction（爽不爽）；三者分别度量、分别签字，满意度高 ≠ 任务能完成。
- **样本量够检出结论就好**：定性 5 个用户约暴露 84% 的可用性问题（n=5→84% / 10→98% / 20→100%，二项暴露模型 λ≈0.31）；定量比例估计 `n ≈ Z²·p(1−p)/E²`（p=50%→97 人 / 80%→62 人 / 5%→19 人）。**不是越大越好，是够检出你要的结论**。
- **SUS 68 是行业基准不是及格线**：10 题奇偶数反向计分 ×2.5；**一致作答恒为 50 是 SUS 的已知特性（非缺陷）**；UMUX-Lite→SUS 必须用自有数据回归校准，文献系数会出荒谬值，故只给确定性重标定 `((u+e)/2−1)/6×100`。
- **A/B 的 p<0.05 只说明「不太可能纯巧合」**：必须同时报相对提升 + 95% CI（CI 跨 0 即无 winner）+ 护栏指标 + 随机单元=用户 + 序贯检验 alpha 消耗；MDE 先算再决定样本量。
- **可用性与无障碍是两件事**：「能不能用」是可用性问题，「愿不愿用 / 是不是被引导着用」是伦理与体验问题；两张表分别签字，不能拿「我们没恶意」替已知缺陷辩护。
- **研究方法按 态度/行为 × 定性/定量 2×2 选**：要 IA 结构用卡片分类/树测试，要出问题用出声思考可用性测试，要推断总体用问卷/实验，别拿问卷去发现用户说不出自己卡哪的可用性 bug。
- **HEART 五维**（Happiness/Engagement/Adoption/Retention/Task success）用 Signal→Metric→Data Source 三层落地；漏斗与行为分析看转化与流失；证据分级与三角验证决定"结论可信到哪"。
- 材料：[ISO 9241-11:2018](https://www.iso.org/standard/63500.html)、[NN/g 可用性指南](https://www.nngroup.com/articles/)、[Sauro & Lewis《Quantifying the User Experience》](https://measuringu.com/book/)、[Google HEART](https://library.gcrinc.co/ux/)、[Kohavi《Trustworthy Online Controlled Experiments》](https://experimentguide.com/)、[GOV.UK 度量实践](https://design-system.service.gov.uk/)、[USWDS Analytics](https://designsystem.digital.gov/)
- → **23 节 + 度量三步法 + 任务级指标 + SUS/UMUX/SEQ/SUPR-Q/NPS + HEART 三层 + 样本量公式 + 研究方法 2×2 + 卡片分类/树测试 + 可用性测试 + 问卷偏差 + A/B 统计 + 12 场景 + 20 反模式 + 20 自检 + 4 段可抄代码（Python 全实跑）见 `design-measurement-research.md`**

### 支线 T · 图标设计系统（Iconography，视觉速记不是装饰）
- **先判图标还是文字**：图形比文字更快被识别时才用图标；歧义或首现品牌图标配文字，正文与导航一级用文字（见 `iconography.md` §1 决策树）。
- **24×24 网格是事实标准**：viewBox 统一 `0 0 24 24`、活动区留 2px 边；同一 keyline（圆 ⌀20 / 方 18 / 矩 20×16）同形状，否则视觉重量飘——跨库碎片化的根因是网格不统一。
- **描边二选一且全库统一**：固定 `stroke-width=2`（Lucide 系）或光学缩放（Material 系，opsz 自动调权重）；圆头圆角、圆角 1–2px；混用会让视觉抖动。
- **尺寸阶梯 12/16/20/24/32/48 密度驱动**，图标-文字间距默认 8px（最小 4px）；可点图标命中区 ≥44px；用 `currentColor` 控色、暗色零改图。
- **可访问性铁律**：装饰图标 `aria-hidden="true"` **且** `focusable="false"`；有意义/icon-only 必带可访问名；非文本对比度 ≥3:1；**永不只靠颜色**；图标字体整库 `aria-hidden`（否则读屏念乱码）。
- **状态图标**：spinner `1–1.4s linear infinite`，`prefers-reduced-motion: reduce` 下停转；假加载 spinner 属欺骗性设计。
- **库选型（GitHub API 实测）**：Lucide 25.6k★ / Tabler 22.6k★ / Fluent 11k★ / Radix 2.7k★ / Material Symbols Apache-2.0（字体 295KB→1.7KB 子集）+ 选型三问（框架绑定 / 风格统一 / 体积敏感）。
- → **22 节 + 网格与 keyline + 描边 + 尺寸阶梯 + 间距 + 填充描边双色 + 光学对齐 + 状态图标 + 交付格式 + 可访问性 + 动画降级 + 命名清单 + 库选型矩阵 + 12 场景 + 20 反模式 + 20 自检 + 4 段可抄代码见 `iconography.md`**

### 支线 U · 导航与信息架构（结构先于装饰，用户只问两个问题：我在这、怎么去那）
- **先分四类职责**：全局（跨站常驻）/ 局部（区域下钻）/ 上下文（内容体内跳转）/ 辅助（页脚·帮助）；把页脚或上下文链接塞进主导航是头号错配。
- **项数有科学依据**：米勒法则 7±2，全局主导航 5–9 项一组；底部 tab ≤5（Apple + Material 共识）；侧栏无硬上限但每 7–9 项做视觉分组。
- **形态按场景选**：≤5 同级顶级 → 底部 tab / 顶部水平；6–12 → 侧栏；≥13 或层级深 → 汉堡抽屉（牺牲可发现性）；内容区切换用 tabs 而非导航。
- **深度优先于广度**：3-click 规则是迷思，用户只在乎每步「信息气味」；深度 ≤3（内容）/ ≤4（工具），分组按心智模型而非字母序。
- **当前位置 ≥2 种信号 + `aria-current`**：颜色+字重+图标+左条至少两项，永不只靠颜色；纯 CSS 高亮对读屏无效。
- **可访问性是及格线**：第一个可聚焦元素是 skip link；每个 `<nav>` 带可区分 `aria-label`；DOM 顺序=焦点顺序；WCAG 2.4.5 要求导航+搜索 ≥2 种找路方式。
- → **14 节 + 四类职责 + 形态决策矩阵 + 项数铁律 + 信息架构地基 + 面包屑三型 + ARIA Tabs + 移动端降级 + 当前位置指示 + WCAG 2.4.x 导航口径 + 搜索协同 + 20 反模式 + 20 自检 + 5 段可抄代码见 `navigation-ia.md`**

### 支线 V · 设计评审与反馈（评审是暴露盲点不是挑错，先对齐再动手）
- 评审是结构化对话对齐决策，产出「问题清单 + 决策记录」；两种形态的评审（同伴探索 / 带决策权的评审）两场会别混。
- 给反馈要可反驳（具体 / 挂目标 / 分离品味与工艺），接收反馈不辩护、每条写处置并留痕。
- 评判用权威启发式 + 严重度分级；明确唯一决策人，防集体决策平庸化与最高薪者意见压垮论证。
- → 13 节（七铁律 / 接收四步 / RACI 与远程异步 / 评判框架 / 15 反模式 / 决策记录 / 4 段模板）见 `design-critique.md`

### 支线 W · 色彩科学（配色不是审美是计算）
- **HSL 撒谎**：HSL/HSV 的 H/S/L 不是感知均匀坐标，等数值步长 ≠ 等视觉步长（蓝区 L 段比红区长 30%+），色板生成、明度梯度一律走 OKLCH/OKLab。
- **OKLCH 已可上生产**：`oklch()` 自 2023-05 跨浏览器广泛可用；L=感知亮度（0 黑 1 白）、C=色度（100%≈0.4）、H=色相；配合相对颜色语法 `oklch(from <c> l c h)` 与 `color-mix()` 做加减/混合。
- **对比度不止一套算法**：WCAG 2.x 相对亮度给正文 4.5:1 / 大文本 3:1 / 非文本 3:1，**不可四舍五入**；APCA 用 `Lc`（感知亮度对比）分 15/30/45/60/75 档，长文与暗色更准。
- **色板生成四路线**：OKLCH 色相旋转 / Radix 12 步语义档 / M3 tonal palette / Leonardo 对比度优先；选一条不许混，否则色阶错序。
- **渐变在 OKLab 插值**：sRGB 线性插值会发灰发脏，必须走 OKLab（CSS `linear-gradient(in oklab, …)` / culori / colorjs.io）。
- **色盲用 Okabe–Ito 8 色**（含 hex），且任何状态/编码**不靠颜色单通道**；非文本对比度 ≥3:1。
- **工程**：Display P3 多 ~25% 色域（`color(display-p3 …)` + sRGB 降级）；库选型 culori / colorjs.io / chroma.js；Figma 变量模式存 OKLCH。
- 材料：[OKLCH in CSS](https://evilmartians.com/chronicles/oklch-css-color-please-stop-using-rgb-hsl/) · [Björn Ottosson OKLab](https://bottosson.github.io/posts/oklab/) · [APCA](https://www.myndex.com/APCA/) · [MDN oklch()](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/oklch) · [Okabe–Ito](https://jfly.uni-koeln.de/color/) · [culori](https://culorijs.org/) · [colorjs.io](https://colorjs.io/)
- → **22 节 + 色彩空间谱系 + 感知均匀性 + OKLab 公式 + 对比度双算法 + 色盲 + 色板四路线 + 渐变插值 + 色彩无障碍 + 工程实现 + 12 场景 + 20 反模式 + 20 自检 + 6 段可抄代码见 `color-science.md`**

---

## 学习节奏（可持续，不靠意志力）

| 周期 | 动作 | 时间 |
|---|---|---|
| 每日 | 看 3 个新界面，各写 1 句"它靠什么成立" | 10 min |
| 每周 | 拆 1 个元素，产出 4–6 变体设计板 | 1 h |
| 每两周 | 读 1 篇方法论（NNG / Refactoring UI 章节）并写 200 字应用设想 | 30 min |
| 每月 | 完整走一遍 L0→L3：选题 → 系统 → 实现 → 自检 | 半天 |
| 每季 | 回看自己 3 个月前的产出，列出 5 个"现在会改的地方" | 30 min |

**最后一条最重要**：能看出自己旧作的毛病，是能力增长唯一可靠的证据。

---

### 支线 X · 视觉风格谱系与设计运动（把"感觉"翻译成信号）

- **这是什么**：用户说"做成 XX 那种感觉 / 高级感 / 科技感"时，不直接套词，而是拆成 Typography / Color / Shape&Material / Motion&Space 四维信号再落成 token。与 `design-md-format.md` §3 品牌 DNA 互补（DNA 是长期资产，本支线是竞品 / 潮流的速配）。
- **先拆再选**：任何风格需求先按四维信号表填（见 `visual-style-taxonomy.md` §2），给参考站走截三屏→逐维标注→抽交集→落 token 四步（§4.1），给形容词先确认语境分支（§4.2）。
- **材质语言与装饰密度只各一个极端**：拟物+扁平、玻璃+硬边阴影都打架；渐变/玻璃/3D/新拟态同时上 = AI slop（§5）。
- **硬红线**：新拟态只装饰/低频、禁主操作与表单、暗色禁入；玻璃拟态文字 ≥4.5:1、正文区禁用、`backdrop-filter` 低端机测成本（§3.8/§3.9）。
- **趋势分两类**：技术/平台驱动（暗色、容器查询、可变字体）值得跟；纯视觉潮流谨慎，看是否被模板化/meme 化（§6）。
- **中文/出海加一层**：中文极简留白更克制、字号 ≥14px、黑体优先；出海按目标市场文化信号、不套刻板符号（§7）。
- **落地**：风格 → token 映射表（圆角档/阴影档/色板基调/字号阶/字重对比/间距基调/动效密度），用 DTCG 固化，风格切换 = 换 semantic token（§8）。
- **判学会了**：能拆任一参考站成四维信号、能解释为什么"全站只上一种材质语言"、能指出新拟态/玻璃拟态的硬红线、能把一个潮流落成 token 组而非截图 → 见 `visual-style-taxonomy.md`。

- [ ] 面对"做成 XX 那种感觉"的需求，能先拆成 Typography/Color/Shape&Material/Motion&Space 四维信号，而不是停在"高级/科技"这种词
- [ ] 能解释为什么同一界面只能有一种主导 depth language、装饰密度只能有一个极端，并各举一例冲突组合
- [ ] 能说出新拟态与玻璃拟态各自的硬红线（可见性/对比度/暗色/正文区/性能），并解释为什么
- [ ] 能把一个参考站风格落成 token 组（圆角档/阴影档/色板基调/字号阶/字重对比/间距基调/动效密度），而不是只交截图

---

### 支线 Y · 字体排印系统（把字号行距从口诀变成可验收的契约）

- **这是什么（六层契约）**：字体排印是与色彩科学并列的基础支柱，但**不是「挑一款好看的字体」**，而是六层契约——覆盖 / 尺度 / 节奏 / 字形 / 加载 / 授权（`typography-system.md` §2）。需求里出现「字太小 / 放大就裁切 / 字号锁死 / 文本间距被改」时，先判落在哪一层；换字体修不了第 2、3 层的缺陷。
- **三条最重要裁决**：① **`font-size` 用 px 写正文不可访问**——MDN 原文 *"Defining font sizes in `px` is not accessible, because the user cannot change the font size in some browsers"*；正解 `rem`（`em` 会 compounding，MDN 实测外层 25.6px / 内层 40.96px）；WCAG 2.2 **SC 1.4.4** 要求文本无辅助技术放大到 **200%** 且不丢内容或功能。② **SC 1.4.12 Text Spacing 是用户覆盖抗压测试、不是默认样式表**（官方 Note 1：*"Content is not required to use these text spacing values"*）：四项 `line-height ≥1.5×` / 段后距 `≥2×` / `letter-spacing ≥0.12×` / `word-spacing ≥0.16×` font size，同时设置、不改其他属性，验收看是否裁切/重叠/丢功能；**SC 1.4.8（AAA）**另给行宽 ≤80 字符（CJK ≤40）、禁 `justify`、段内行距 1.5、200% 无横向滚动。③ **`font-family` 是逐字符回退**（缺 glyph 继续往下找，generic 放最后且不加引号），`unicode-range` **命中一个字符即整片下载**（MDN 原文）→ CJK 必须按高频字集分片。
- **节奏与字形**：M3 `applying-type` 给大字号（display/headline/title）行高 ≈`1.2×`、小正文/标签 ≈`1.5×`；五角色 × 三尺寸 = 15 baseline（官方 2025-05 起另有 15 emphasized 变体，共 30）；表格 / 时钟 / 金额 / 实时值用 **`tabular-nums`**（不是换 `monospace`），ID/验证码加 `slashed-zero`；大文本对比度 3:1 / 小文本 4.5:1，**超链接必须带下划线**（改字号后要重判「大文本」并重算对比度）。
- **工程链**：可变字体五注册轴 `wght/wdth/slnt/ital/opsz`（custom 轴大写，`GRAD` 不改 advance 因而 hover 不触发 reflow）→ 高层 `font-variant-*` 优先于低位 `font-feature-settings`（后者**禁用于 small caps**）→ `font-display` 三阶段（block/swap/failure）五档、初始 `auto` → `size-adjust`（初始 100%）/ `font-size-adjust`（`u=(m/m′)s`）对齐 fallback 度量压 CLS。
- **中文与授权（W3C clreq / OFL）**：汉字与西文空白「不多于 1/4 汉字宽」且行首行尾不加、汉字与标点 1:1 正方形、文本存储层避免全角 ASCII、光标/删除/计数按 **UAX #29 字素丛**（§2.1.3 / §1.2 / §4.1 / §4.2.1）；**OFL 1.1** 可随软件 use/embed/modify/redistribute/sell，但不可单独售卖字体、衍生字体必须继续 OFL、Modified Version 不得用 RFN、每份拷贝须带版权声明与 license，**文档不受字体 license 约束**。
- **取源限制**：M3 15 档精确 `size/line-height/weight/tracking` 表为动态渲染页未取得、clreq 标点挤压/避头尾/着重号本轮未证实 → **不臆造数值**，见 `typography-system.md` §24；`NOASSERTION` ≠ 无许可，逐字体目录读 `OFL.txt`。
- **判学会了**：能解释为什么正文不能用 px、能当场注入 1.4.12 四项并指出哪个容器会塌、能说清逐字符回退与整片下载的关系、能用 `tabular-nums` 修数字抖动、能判断一款字体能否自托管分发 → 见 `typography-system.md` 30 节 / 12 场景 / 20 反模式 / 20 自检 / 6 段可抄代码。
- 材料：[MDN font-size](https://developer.mozilla.org/en-US/docs/Web/CSS/font-size) · [W3C WCAG 2.2 SC 1.4.12](https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html) · [M3 Applying type](https://m3.material.io/styles/typography/applying-type) · [W3C clreq](https://www.w3.org/TR/clreq/) · [SIL OFL 1.1](https://openfontlicense.org/open-font-license-official-text/) · [MDN unicode-range](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/unicode-range) · [MDN font-display](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/font-display)

- [ ] 能解释为什么正文 `font-size` 不能用 px、`em` 为什么会 compounding，并说出 WCAG 2.2 SC 1.4.4 的 200% 门槛
- [ ] 能说清 WCAG 2.2 SC 1.4.12 四项数值，并解释它是「用户覆盖抗压测试」而非作者默认样式；能当场注入验收表单与按钮
- [ ] 能说出表格数字抖动的根因与 `tabular-nums` 解法，且不把它误答成「换成等宽字体」
- [ ] 能说清 `font-family` 逐字符回退与 `unicode-range`「命中一字即整片下载」的关系，并判断一款字体能否自托管分发

### 支线 Z · 形状与深度系统（把圆角与阴影从口诀变成几何契约）

- **这是什么（第三根基础支柱）**：与「色彩科学」「字体排印」并列，但此前 37 份参考里零独立文件，圆角/阴影/高度/材质只散落在 `dark-mode.md §2/§5`、`design-tokens.md §2.4`、`visual-style-taxonomy.md §2.3` 等边角。先按 `shape-elevation.md` §2 **五层模型**（几何 / 高度 / 表面 / 材质 / 层叠）判层，再取数值。
- **三条最重要裁决**：① **elevation 是语义 z-height 不是可抄阴影值**——M3 原文 *"Elevation has no shadow or value of its own by default."*，而 `elevation.css` 的 `box-shadow: var(--md-sys-elevation-level1)` 展开为单长度 `1px`，MDN 要求 2/3/4 `<length>`；六级 `0/1/3/6/8/12 dp` 是层级顺序不是 CSS 参数。② **阴影不算 WCAG 2.2 SC 1.4.11 的 3:1 边界**——Python 实跑白底 `5%/8%/10%/12%` 黑阴影仅 `1.119/1.192/1.248/1.320:1`，3:1 需 `alpha≈0.4176`；正解是独立边界线 / focus ring / 状态形状。③ **圆角是几何契约**——百分比水平参照 width、垂直参照 height，corner overlap 按 `f=min(L_i/S_i)` 整体缩减（`100×40` 写 30 与 50 都只生效 20px），嵌套 `r=R−p` 且 `r≤0` 时失效。
- **精确值怎么取**：七体系圆角（M3 `0/4/8/12/16/28` · TDesign `2/3/6/9/12/999` · Ant `2/4/6/8` · Arco `0/2/4/8`）与七体系阴影（Tailwind v4 八值逐字 · MUI `0.2/0.14/0.12` 三层 25 档 · Ant `boxShadow` 三层 · TDesign `--td-shadow-1~3` · Carbon 表面色阶 · Apple 材质）见 `shape-elevation.md §8 §13`；**一个项目只选一套**，别混两套光源模型。
- **深度语言三选一**：阴影（浅色消费级）/ 表面色阶（中后台·暗色·可测边界）/ 材质（仅覆盖内容的 functional layer，一个视图 ≤1 处）；暗色靠表面提亮重排而非照搬亮色阴影；`z-index` 用 `dropdown → sticky → backdrop → modal → toast → tooltip` 语义刻度，不写 `9999` → §15 §16 §18 §19。
- **判学会了**：能解释为什么 `box-shadow: 1px` 无效、能当场算出 10% 黑阴影的对比度并说明为什么不能当边界、能算出 `100×40` 写 50px 圆角的实际生效值、能判断 `R=12, p=16` 该改哪里、能说出为什么 Liquid Glass 不能用在内容层 → 见 `shape-elevation.md` §22 的 20 项自检。
- 材料：[M3 Elevation](https://m3.material.io/styles/elevation/overview) · [MDN box-shadow](https://developer.mozilla.org/en-US/docs/Web/CSS/box-shadow) · [MDN border-radius](https://developer.mozilla.org/en-US/docs/Web/CSS/border-radius) · [WCAG 1.4.11](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html) · [Apple HIG Materials](https://developer.apple.com/design/human-interface-guidelines/materials) · [Tailwind box-shadow](https://tailwindcss.com/docs/box-shadow)

- [ ] 能说出 `box-shadow` 需要几个 `<length>`，并解释为什么把 M3 `level3=6dp` 写成 `box-shadow: 0 6px 6px` 是误读
- [ ] 能算出白底 10% 黑阴影的对比度，并说明为什么它不能充当 WCAG 1.4.11 的 3:1 识别边界、正确落点是什么
- [ ] 能算出 `100×40` 盒子写 `border-radius: 50px` 的实际生效值，并说出 `r = R − p` 在 `R=12, p=16` 时该怎么处置
- [ ] 能区分阴影 / 表面色阶 / 材质三种深度语言，说出 Apple Liquid Glass 为何只属 functional layer，并写出语义 z-index 刻度

### 支线 AA · 视觉层级与格式塔组织律（把"放大加粗"翻译成注意力分配契约）

- **这是什么（第四根基础支柱）**：与「色彩科学」「字体排印」「形状与深度」并列，但此前 38 份参考里零独立文件，格式塔/眼动/认知负荷只散落在 `editorial-layout.md §8`、`navigation-ia.md`、`design-ethics-inclusion.md`、`iconography.md` 的边角。先按 `visual-hierarchy-gestalt.md` §2 **三层模型**（组织 L1 / 引导 L2 / 负荷 L3）判层，别一上来就改字号。
- **三条最重要裁决**：① **F 型不是设计目标**——NN/g（Kara Pernice, 2017）逐字 *"The F-pattern is the default pattern when there are no strong cues to attract the eyes towards meaningful information."*，用户走的是 *"path of minimum effort"*；F 之外还有 Layer-cake / Spotted / Marking / Bypassing / Commitment，RTL 语言翻转，移动端仍成立。② **视觉呈现不构成结构**——W3C SC 1.3.2（A）+ C27 / F1、SC 2.4.3（A）、SC 2.4.6（AA）、SC 2.4.10（AAA）逐字 *"visual presentation is not sufficient to identify document sections"*；DOM 阅读顺序、键盘焦点顺序、标题树必须讲同一个故事。③ **7±2 不是菜单上限**——Laws of UX 逐字 *"Don't use the 'magical number seven' to justify unnecessary design limitations."*；Sweller 1988 拆 intrinsic/extraneous/germane，Hick `log₂` 只对可逐层排除的选项成立，Fitts Shannon 形式 `ID = log₂(D/W+1)` 的 `W` 是沿运动轴宽度。
- **精确值怎么取**：IxDF 12 条格式塔原则（Emergence→Common Fate，Koffka 原话是 *"other than"* 不是 *"greater than"*）、Treisman & Gelade 1980 前注意阶段与 feature/conjunction search（18% / 23% 两个实验，**FIT 页面无视觉搜索斜率数值**）、四条 WCAG 准则原文、Hick 五条 Takeaways、Fitts 三形式、序列位置的 15–30 秒干扰抵消 recency、Von Restorff 的"相对差异"限定 → `visual-hierarchy-gestalt.md §5 §7 §9 §12 §13 §15`。**§8 的间距比 1.5× 是工程约定不是实验常数**，别写成"研究证明"。
- **判学会了**：能说出为什么 F 型不能当版式模板、能解释 `order: -1` 搬主内容为什么伤读屏用户、能用四条 SC 的级别与分工判一次顺序缺陷、能说清为什么 7±2 不能论证导航项数、能写出 Hick 与 Fitts 的公式并说出各自失效条件、能按 §6 导出三顺序并讲同一个故事 → 见 `visual-hierarchy-gestalt.md §22` 的 20 项自检与 §23.2 静态扫描器。
- 材料：[NN/g F-Shaped Pattern](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/) · [W3C SC 1.3.2](https://www.w3.org/WAI/WCAG22/Understanding/meaningful-sequence.html) · [W3C SC 2.4.3](https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html) · [W3C SC 2.4.10](https://www.w3.org/WAI/WCAG22/Understanding/section-headings.html) · [IxDF Gestalt Principles](https://www.interaction-design.org/literature/topics/gestalt-principles) · [Laws of UX](https://lawsofux.com/) · [Wikipedia: Feature integration theory](https://en.wikipedia.org/wiki/Feature_integration_theory)

- [ ] 能引用 NN/g 的 default pattern 原文，说明 F 型是诊断信号而非设计目标，并列出至少 5 种其他扫描模式
- [ ] 能逐字写出 SC 1.3.2 与 SC 2.4.3 的条文、说出 C27 / F1 各管什么，并判断一次 `order: -1` 缺陷
- [ ] 能说清 7±2 的真实含义（Miller 1956 的即时记忆广度与 bit 定义）与为什么不能用来限制导航项数
- [ ] 能写出 `RT = a + b·log₂(n+1)` 与 `ID = log₂(D/W+1)`，说出 `+1`、`W` 的含义与两条失效条件

### 支线 AB · 内容可发现性与可扫读性（把"搜得到"翻译成四层链路的线索密度）

- **这是什么（注意力链路的下游环节）**：与「视觉层级（目光先看哪）」「字体排印（字怎么排）」「导航与信息架构（结构怎么搭）」相邻但问题不同；此前 39 份参考里零独立资产，站内搜索链路、链接目的契约族、阅读等级与可发现性度量只在 `navigation-ia.md §4/§10`、`feedback-states.md §5/§6`、`ux-writing.md §14.3` 局部出现。先按 `content-findability.md` §2 **四层链路模型**（L1 有路 / L2 认得出 / L3 读得动 / L4 走得出）判层，别一上来就改文案。
- **三条最重要裁决**：① **多种找路方式是 WCAG AA 硬要求，搜索不是导航的替身**——SC 2.4.5 逐字 *"More than one way is available to locate a web page within a set of web pages except where the web page is the result of, or a step in, a process."*，In Brief *"Provide at least two options for reaching the same content."*，充分技术要求是 *"Using two or more of the following techniques"* 六项（G161 搜索只算一条）；搜索结果页是 process 例外，产品详情页不是。② **链接目的要能脱离上下文成立**——SC 2.4.4（A）/ 2.4.9（AAA）/ 3.2.4（AA）；NN/g 11 字符研究 80 人 / 20 站 / 35% 完全无法预测、Ann Taylor 85%→100%；`how-users-read-on-the-web` *"79 percent ... always scanned"* / *"only 16 percent read word-by-word"* 与 58/47/27/124% 是**单站点相对提升，不是通用 ROI**。③ **阅读等级门槛是「九年学校教育」不是 Flesch 分数**——SC 3.1.5（AAA）Intent 逐字 *"more than nine years of school"*；FRE `206.835 − 1.015×ASL − 84.6×ASW`、FKGL `0.39×ASL + 11.8×ASW − 15.59`、SMOG `1.043×√(n_poly×30/n_sent)+3.1291` 系数逐字取自 ReadabilityFormulas.com，Wikipedia 明确两者 *"not directly comparable and cannot be converted"*；音节公式不能套中文，§16 六个代理指标是**工程约定非标准**。
- **精确值怎么取**：APG combobox（`role=combobox` + `aria-expanded` / `aria-controls` / `aria-activedescendant` / `aria-autocomplete` 三档、popup 四角色、DOM focus 留在 combobox、selection follows focus、dialog 例外）、M3 Search specs（56dp / 360–720dp / 24→12dp / 16dp / 30dp）、NN/g 首次/二次/三次查询 51/32/18% 与平均 2.0 词、GOV.UK 404 四条禁令、tree testing 的 findability / directness（**定性结果不可冒充百分比**）、Plain Writing Act of 2010 → `content-findability.md §3 §6 §11 §15 §18 §20`。**§16 中文代理指标与「前 6–8 汉字」是工程约定，别写成"研究证明"**。
- **判学会了**：能说出为什么「只放一个搜索框」不达 SC 2.4.5、能解释「Learn More ×8」在读屏 links list 里为何不可辨、能判「零结果只写没有结果」落在 L4 哪一步、能说清为什么不能用 Flesch 分数当合规门槛、能写出 APG combobox 的 focus 与 aria 契约 → 见 `content-findability.md §25` 的 20 项自检与 §26 三段可抄扫描器。
- 材料：[W3C SC 2.4.5](https://www.w3.org/WAI/WCAG22/Understanding/multiple-ways.html) · [W3C SC 3.1.5](https://www.w3.org/WAI/WCAG22/Understanding/reading-level.html) · [W3C APG Combobox](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/) · [NN/g How Users Read](https://www.nngroup.com/articles/how-users-read-on-the-web/) · [NN/g First 2 Words](https://www.nngroup.com/articles/first-2-words-a-signal-for-scanning/) · [GOV.UK 404](https://design-system.service.gov.uk/patterns/page-not-found-pages/) · [M3 Search specs](https://m3.material.io/components/search/specs) · [Digital.gov Plain Language](https://digital.gov/guides/plain-language/)

- [ ] 能逐字写出 SC 2.4.5 的条文与 In Brief「至少两条路」，并列出六项充分技术里除 G161 搜索外的至少三条
- [ ] 能说清 SC 2.4.4（A）/ 2.4.9（AAA）/ 3.2.4（AA）的分工，并解释为什么「Learn More」在读屏 links list 里失效
- [ ] 能判一次「找不到内容」落在 L1–L4 哪一层，并说明为什么四层都靠「文案写短点」会越改越糟
- [ ] 能说出 SC 3.1.5 的合规门槛是「九年学校教育」而非 Flesch 分数，并解释音节公式为什么不能套中文

### 支线 AC · 直接操纵与指针交互（把"跟着指针走"翻译成四条并存的完成路径）

- **这是什么（认知链路下游的执行端）**：与「视觉层级（目光先看哪）」「内容可发现性（能不能找到）」相邻但问题不同；此前 40 份参考零独立资产，`dp_search.py "拖拽 手势 指针交互"` 首位返回 `performance-design.md` / `design-system-docs.md` / `ai-design-toolchain.md`，全域词频实测 `Drag and drop` / `Pointer Events` / `setPointerCapture` / dnd 库名几乎零命中。上游 `motion-orchestration.md` 讲列表让位动画却不给拖拽状态机、`component-api-design.md §12` 讲 APG 键盘契约却不给拖放拿起 / 移动 / 取消、`form-table.md` 讲滑块却不给 down-event / up-event 的取消要求。
- **三条最重要裁决**：① **补键盘快捷键不满足 SC 2.5.7 / 2.5.1**——逐字条文要求 *"single pointer without dragging"*，Intent 逐字 *"keyboard operability is not sufficient..."*，充分技术是 G219 四类替代；② **`pointercancel` 是规范性必达事件**——PE3 *"MUST suppress a pointer event stream"* 四步链 + `touch-action` 因果；③ **目标尺寸是三套口径**——24×24 AA 法条（含 24 CSS px 圆 spacing 例外）/ 44×44 AAA 与 iOS / 48×48 dp 平台设计值。
- **精确值怎么取**：PE3 事件与 capture 三方法、MDN `touch-action` 形式语法与祖先求交、HTML DnD 七事件与 `dragover` 的 `preventDefault()`、dnd-kit Keyboard sensor 默认 `25` pixels（自述 arbitrary）、NN/g `at least 1cm x 1cm` / `a timing delay of a few milliseconds`（未量化）/ roughly `100 ms` 让位动画、Material 2 `48 x 48 dp` / `about 9mm` / `7-10mm` / `8dp`、GitHub API 实测 10 库 star / license / pushed_at。
- **判学会了**：能说出为什么键盘快捷键不算 SC 2.5.7 的替代、能复述 `pointercancel` 的 PE3 四步抑制链、能判「按钮 24px 达标吗」落在哪套口径、能解释读屏为什么播报 position 而不是 index。
- 材料：[W3C SC 2.5.7](https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html) · [W3C G219](https://www.w3.org/WAI/WCAG22/Techniques/general/G219) · [W3C Pointer Events Level 3](https://www.w3.org/TR/pointerevents3/) · [MDN touch-action](https://developer.mozilla.org/en-US/docs/Web/CSS/touch-action) · [dnd-kit Accessibility](https://docs.dndkit.com/guides/accessibility) · [NN/g Drag-and-Drop](https://www.nngroup.com/articles/drag-drop/)

- [ ] 能逐字写出 SC 2.5.7 的条文，并解释为什么「键盘快捷键」不是 *single pointer without dragging*
- [ ] 能列出 G219 的四类无拖动替代，并说出 SC 2.5.1 与 2.5.7 的交叉约束为什么禁止「另一种拖法」
- [ ] 能复述 PE3 `MUST suppress a pointer event stream` 的四步链，并写出 `pointercancel` 回滚里必须做的五件事
- [ ] 能区分 24×24（AA，含圆 spacing 例外）/ 44×44（AAA，无例外）/ 48×48 dp（M2 设计值），并说出把 24 当推荐值的错在哪

### 支线 AD · 对话式与生成式界面（把"边生成边变化"翻译成五段链路的完成路径）

- **这是什么（认知链路下游的输出端）**：与「视觉层级（目光先看哪）」「内容可发现性（能不能找到）」「直接操纵（按下指针之后）」相邻但问题不同——前三份都假设内容是确定的，本支线处理**输出本身在流动、可能出错、可能带副作用**。此前 41 份参考零独立资产，`dp_search.py "对话式界面 聊天 UI 流式输出"` 首位落到提示词工程与加载态，判定为结构性空白。
- **三条最重要裁决**：① **流式回答正文不是 status message**——SC 4.1.3 逐字只管 *status messages*，官方明确「搜索结果列表不是 status update」，回答正文与结果同类；逐 chunk 进 `aria-live="assertive"` 属官方 Failure 族 + too "chatty" 风险；② **生成式 UI 是模型在受控组件目录里做路由**——Vercel 逐字 *"the model is akin to a dynamic router"*，组件名必须查白名单、`props` 必须过 `inputSchema`，RSC 页自述 *"currently experimental"* 并推荐 AI SDK UI 用于生产；③ **纠错是四档恢复链**——HAX G9 逐字 *"Make it easy to edit, refine, or recover when the AI system is wrong."*，停止 / 重试 / 编辑原消息 / 撤销自动化动作，不是一个「重新生成」按钮。
- **精确值怎么取**：`role=log` 隐性 `aria-live="polite"` 与 `aria-atomic="false"`（W3C ARIA23 逐字，官方示例 1 即聊天记录）；`useChat.status` 四态 `submitted` / `streaming` / `ready` / `error`（官方逐字释义）；AG-UI `RunStarted` 与 `RunFinished|RunError` 是 mandatory boundaries、`RunError` 后 no further processing；`message.parts` 支持 text / tool invocation / tool result。
- **判学会了**：能说出为什么逐 token 播报是错的、能复述 `aria-busy` 的三个必须复位出口、能判「让模型直接吐 JSX」错在哪、能列出编辑原消息时必须清空队列与截断分支的原因。
- 材料：[W3C ARIA23](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA23) · [W3C SC 4.1.3](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html) · [Microsoft HAX G9](https://www.microsoft.com/en-us/haxtoolkit/guideline/support-efficient-correction/) · [Ant Design X RICH](https://x.ant.design/docs/spec/introduce) · [Vercel AI SDK RSC](https://sdk.vercel.ai/docs/ai-sdk-rsc/streaming-react-components) · [AG-UI Events](https://docs.ag-ui.com/concepts/events)

- [ ] 能逐字写出 SC 4.1.3 条文，并解释为什么回答正文不是 status message、逐 chunk 播报为什么踩 too "chatty" 风险
- [ ] 能说出 `role=log` 的两个隐性值（polite / atomic=false），并解释为什么 `aria-busy` 不能挂在容器上且三个出口都必须复位
- [ ] 能复述 `streamUI` 的「模型当路由 + 组件白名单 + `inputSchema`」三件套，并说出 RSC 页自述 experimental 的选型后果
- [ ] 能列出四档恢复链（停止 / 重试 / 编辑原消息 / 撤销副作用），并说出编辑与重生成为什么必须清空队列
- [ ] 能列出 `useChat` 四态与 AG-UI 三模式的映射，并判出「`RunError` 之后仍收到 chunk」属于哪一层失败


### 支线 AE · 叠加层交互契约（把 inert 与顶层栈翻译成四问判型的完成路径）

- **这是什么（交互契约的边界端）**：与语义 z-index 刻度、反馈时长、props 所有权三份资产相邻但问题不同——前三份分别管层看起来多高、文案怎么写、状态归谁，本支线管 inert 是否成立、`aria-modal` 能否标、Tab 是否越界、Escape 是否闭合、以及 2.4.11 下 focused component 会不会被完全遮住。此前 42 份参考对 `Popover API` / `closedby` / `top layer` / `inert` / 2.4.11 零独立资产，判定为结构性空白。
- **三条最重要裁决**：① **模态由 inert 定义，不由遮罩定义**——W3C APG 逐字 *"Windows under a modal dialog are inert."* / *"Tab and Shift + Tab do not move focus outside the dialog."* / *"Escape: Closes the dialog."*，且 `aria-modal="true"` 只在「代码阻止一切外部交互」且「视觉遮蔽外内容」双条件齐备时才标（*"mark a dialog modal only when both"*）；② **Popover API 永远非模态**——MDN 逐字 *"Popovers created using the Popover API are always non-modal."*，`<dialog>` 只有 `showModal()` 才进 top layer 并由浏览器提供 inert，三态 `auto`/`hint`/`manual` 是三套关闭与堆叠契约而非三种动画；③ **伪模态是四条款合取的最坏形态**——SC 2.4.11 *"A properly constructed modal dialog will always pass this SC"*，而「不接管焦点、不约束交互、不失焦自关」的 dialog-like overlay *"will be at risk of failing"*；SC 1.4.13 / 2.1.2 / 3.2.1 分别管 hover 内容消隐、标准退出法与 focus 触发 change of context。
- **精确值怎么取**：APG 初始焦点四种情形与关闭后 *"focus returns to the element that invoked the dialog"*；MDN 明令**禁止**在 `<dialog>` 容器上加 `tabindex`；`closedby` 三值 `any`/`closerequest`/`none`；`popovertargetaction` 三值 `hide`/`show`/`toggle`；`beforetoggle` / `toggle` 两事件；SC 2.4.11 是 **AA**，检查对象是 focused component 而非 focus indicator；C43 `scroll-padding`、F110 sticky footer。
- **判学会了**：能用四问判出某个「弹窗」到底是模态 dialog、非模态 popover 还是伪模态；能解释为什么 `z-index: 9999` 修不好 Tab 穿透；能说出 Note 2 三条「不推进键盘焦点即可显形」的出路；能判出「字段一获焦就弹帮助框」同时踩了哪两条准则。
- 材料：[W3C APG Dialog (Modal)](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/) · [MDN `<dialog>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/dialog) · [MDN Popover API](https://developer.mozilla.org/en-US/docs/Web/API/Popover_API) · [WCAG 2.2 · SC 2.4.11](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html) · [WCAG 2.2 · SC 1.4.13](https://www.w3.org/WAI/WCAG22/Understanding/content-on-hover-or-focus.html) · [Apple HIG Modality](https://developer.apple.com/design/human-interface-guidelines/modality) · [Radix Dialog](https://www.radix-ui.com/primitives/docs/components/dialog)

- [ ] 能逐字写出 APG 的四条键盘契约（打开时焦点进层 / Tab / Shift+Tab / Escape），并说明关闭后焦点去哪
- [ ] 能说出 `aria-modal="true"` 的双条件，并解释为什么「声明」不能替代 inert 实现
- [ ] 能区分 `showModal()` / `show()` / `open` 属性 / CSS `display` 四种打开方式的模态性，并复述 `closedby` 三值
- [ ] 能列出 Popover 三态与 auto·hint 双栈的六条规则，并解释为什么 `<dialog popover>` 叠加后仍非模态
- [ ] 能列出 SC 1.4.13 三条件与 SC 2.4.11 Note 2 三条出路，并判出「持久浮层只能 Tab 回去点 X」属于 RISK 还是 FAIL

### 支线 AF · 首次体验链路（把 first-run 到 activation 翻译成六问判型的完成路径）

- **这是什么（链路的起点端）**：与叠加层契约、零数据位结构、组件条款明细三份资产相邻但问题不同——它们分别管 coach mark 作为 overlay 的 inert·Tab·Escape、空态五件套、以及 3.3.2/3.3.7 的表格侧明细；本支线管 FTUE 这条**有时间起止的路径**：`Launch → First-run → Teach → Activate → Return`，判「该不该教、教什么、什么时候教、什么时候要权限、什么时候算成功」。此前 43 份参考对 `first-run` / `progressive disclosure` / `coach mark` / `aha moment` / `Splash screen` / `SC 2.2.1` 等 25 个主题词全域零命中，`onboarding` 仅零散落在 4 份文件、无独立资产，判定为结构性空白。
- **三条最重要裁决**：① **默认不加教程**——NN/g《Mobile Tutorials》(A. Kendrick, 2020-03-08) 70 人 / 4 apps 逐字：91% vs 94%（p=0.443 不显著）、93.49s vs 85.17s（p>0.1 不显著），唯一显著项 SEQ 4.92 vs 5.49（p=0.047）且方向对教程不利；Apple HIG *"Teach through interactivity."* / *"Consider providing a collection of context-specific tips instead of a single onboarding flow."*，NN/g *"Instructional onboarding should not be used to supplement poor design."*，落成「先测无引导 → 先改界面 → 才原型化引导 → 有成功率提升才上线」四步闸门。② **权限按功能时机请求，不按会话起点批发**——Apple HIG Privacy *"Request permission only when your app clearly needs access to the data or resource."* / *"Avoid requesting permission at launch unless the data or resource is required for your app to function."*；Onboarding 页允许整合权限的硬前置条件是 *"before it can function"*；purpose string 四标准「brief / complete sentence / sentence case / avoid passive voice / 句末句号」；pre-alert 单按钮·禁 `Allow`·禁 cancel·禁 close 是**平台特定规则**，禁止外推到 Web cookie 同意层。③ **四条款合取**——SC 3.3.7（浏览器 `autocomplete` 不足够，站点须自己回填或提供可选）、SC 3.3.8（**明确不覆盖账号创建**，但注册建议照做；OTP 手动转录不合规）、SC 3.2.1（官方失败例恰是抢走 focus 的 help dialog，G107 改用 activate）、SC 2.2.1（六选项 / 20 seconds / ten times / 10x / 20 hours，且 OTP 靠 essential 豁免后仍要过 3.3.8）。
- **精确值怎么取**：NN/g 研究的限定条件必须随数值一起给（4 个简单 iOS App、仅测 deck-of-cards 教程、耗时不含阅读时间、geometric mean、剔除 13 trials = 5%）；Material 1 `m2.material.io` 是**归档版、非现行 M3**：`fewer than ten choices` / `90% of the way through the first session` / `up to three benefits` / 2–3 秒 / 24sp·32sp·15sp·16sp·56dp·24dp·48dp；Apple tips 阈值 `>3 actions` 不宜 / 1–2 句 / `once every 24 hours` / 60–75 字符；Ant Design Tour 的 `mask` / `disabledInteraction` / `keyboard` / `gap` / `zIndex` 是**实现默认值**不是规范刻度；Carbon 的 starter content 与 in-line documentation 无逐字数值，相关建议一律标「工程约定」。`push revelation` / `pull revelation` 是 Laubheimer 2023 篇的成对术语，本文件 §4 的 push/pull 是另一套工程简称，二者不等价（见该资产 §22 第 4 条勘误）。
- **判学会了**：能用六问判型（Q4「先测无引导版本」是闸门）判出该不该做、做哪一种；能说清 `launch screen ≠ splash screen ≠ onboarding` 三分界；能把 purpose string 写成句末带句号的主动具体完整句，并说出 pre-alert 为什么不能搬到 Web 同意层；能解释「注册成功」不等于 activation、跳过率下降为什么不是好转信号；能把四类可延后设置从首启移走。
- 材料：[Apple HIG · Onboarding](https://developer.apple.com/design/human-interface-guidelines/onboarding) · [Apple HIG · Launching](https://developer.apple.com/design/human-interface-guidelines/launching) · [Apple HIG · Offering help](https://developer.apple.com/design/human-interface-guidelines/offering-help) · [Apple HIG · Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy) · [NN/g · Mobile Tutorials](https://www.nngroup.com/articles/mobile-tutorials/) · [NN/g · Mobile-App Onboarding](https://www.nngroup.com/articles/mobile-app-onboarding/) · [NN/g · Onboarding Tutorials vs. Contextual Help](https://www.nngroup.com/articles/onboarding-tutorials/) · [Material 1 · Onboarding（归档）](https://m2.material.io/design/communication/onboarding.html) · [W3C · SC 3.3.7](https://www.w3.org/WAI/WCAG22/Understanding/redundant-entry.html) · [W3C · SC 3.3.8](https://www.w3.org/WAI/WCAG22/Understanding/accessible-authentication-minimum.html) · [W3C · SC 2.2.1](https://www.w3.org/WAI/WCAG22/Understanding/timing-adjustable.html) · [Ant Design · Tour](https://ant.design/components/tour) · [Carbon · Empty states](https://www.carbondesignsystem.com/building-blocks/core/patterns/empty-states)

- [ ] 能写出六问判型并解释为什么 Q4「先测无引导」是闸门而不是建议，以及 Q3 + Q1 为什么不能叠加成五屏轮播的理由
- [ ] 能完整复述 NN/g 70 人研究的四项数值与四条限制，并说明唯一显著的 SEQ 为什么方向对教程不利
- [ ] 能区分 `launch screen` / `splash screen` / onboarding 三者职责，并说出 Material 1 三模型为什么 Self-Select 与 Top User Benefits 不得组合、以及这些数值为什么不能当 M3 合规值
- [ ] 能写出 purpose string 的四条逐字标准与三行正反例，并解释 pre-alert 的「单按钮 / 禁 cancel / 禁 close」为什么只作用于受保护资源的系统权限弹窗之前
- [ ] 能列出 SC 3.3.7 / 3.3.8 / 3.2.1 / 2.2.1 的合取验收点，判出「第三步重复要邮箱」「禁粘贴验证码」「聚焦即弹帮助框」「超时清空整张表」各踩了哪一条

### 支线 AG · 空状态与零数据位（把"没有数据"翻译成五件套与可抄矩阵的完成路径）

- **这是什么（链路的内容端）**：与首次体验链路（AF）、五种空状态结构（feedback-states §5）、零结果出路（content-findability）、首次操作率（design-measurement-research）相邻但问题不同——它们分别管 first-run 的时间路径、五种空的判型与速查、搜索无结果的出路、以及空状态有没有用怎么度量；本支线管**空状态的内容设计本身**：结构五件套、中英抄写矩阵、装饰插画的取舍与无障碍、零数据位（starter content）四模式、变体承载位置。此前 44 份参考对 `empty state` / `starter content` / `blank slate` / `zero-data` / `零数据位` / `装饰插画` 等几乎零命中，判定为结构性空白（feedback-states §5 只给分类与速查，无一手解剖、无可抄矩阵）。
- **三条最重要裁决**：① **默认不道歉、不留白死路**——Atlassian *"Empty states can be a chance to celebrate, educate, and inform people of what they can do next."*、Ant Design *"User tutorial to create something in fresh new situation."*；② **装饰性插画必须 `aria-hidden` 且不让焦点滞留**——Atlassian Accessibility *"If it's only for decoration, avoid alt text or remove the image altogether."*，纯装饰图 `aria-hidden` + `alt=""` 且不进 Tab 顺序（SC 1.1.1 / 2.4.3）；③ **失败态 ≠ 缺省态，禁止伪装**——失败态必须给原因 + 重试，不得渲染成"零内容"，否则用户不再重试。
- **精确值怎么取**：Ant Design Empty 一手 token（`colorTextDescription rgba(0,0,0,0.45)`、`PRESENTED_IMAGE_SIMPLE` / `PRESENTED_IMAGE_DEFAULT`、margin 8/16/32、内置 footer 行动槽）2026-11-13 逐字核验；Atlassian 一手 anatomy（Illustration/Header/Description/Buttons、wide 464px / narrow 304px、h600 标题、CTA imperative verbs、语气分级、装饰图 alt 规则）2026-11-13 逐字核验；NN/g 四分类与 Material 3 / Apple HIG 为 JS 渲染或 404 动态页，未取得逐字正文 → 取源限制（见该资产 §16）。
- **判学会了**：能用五种空态判型器三问定类（完成/失败/无结果/无权限/首次）；能写出中英抄写矩阵并说出标题正向 ≤12 字、说明 ≤30 字、按钮 ≤6 字的公式；能判装饰插画该不该用、用了怎么过无障碍；能说出零数据位四模式适用边界（创作型 vs 交易型）；能解释失败空态伪装成无数据为什么是最高频也最贵的错误；材料见 `references/empty-states.md`。

- [ ] 能用判型器三问把任意空状态归入五种之一，并说出把失败渲染成无数据为什么会让用户不再重试
- [ ] 能写出空状态文案公式（标题≤12/说明≤30/按钮≤6）并给中英两版，且装饰插画在纯装饰时给出 `aria-hidden` + `alt=""` 的写法

### 支线 AH · 定价页与结账流程（把"敢不敢付"翻译成总价锁定与承诺闸门的完成路径）

- **这是什么（链路的内容端）**：与表单与表格（`form-table`：字段/校验/错误文案）、可访问性（`accessibility`：SC 阈值与焦点）、设计伦理（`design-ethics-inclusion`：附加费 sneaking）、反馈与状态（`feedback-states §6`：`role="status"`）相邻但问题不同——它们分别管字段怎么排、条款怎么判、附加项合不合伦理、状态怎么播报；本支线管**钱的两端**：定价页怎么让人选得明白、结账页怎么让人敢付完，核心是「总价锁定」与「承诺闸门」。此前 45 份参考对 `结账`=0 / `checkout`=2 / `运费`=0 / `税费`=0 / `PSD2`=0 近乎零命中，`定价`/`价格表` 仅落在 `patterns.md §定价表` 五行速记，判定为结构性空白。
- **三条最重要裁决**：① **总价先行且不可变**——FTC 16 CFR 464 §464.1 total price 逐字 *"the maximum total of all fees or charges a consumer must pay for any good(s) or service(s) and any mandatory ancillary good or service…"*，§464.2(b) 要求总价比任何其他价格信息更显著，§464.1(4) 要求电子媒介披露 *"must be unavoidable"*；② **结账是承诺不是表单**——SC 3.3.4（**Level AA**）三选一 Reversible / Checked / Confirmed，充分技术 G164 / G98 / G155，复核页照 GOV.UK check answers；③ **同一进程内不重复索要**——SC 3.3.7（Level A）*"The autocomplete feature of browsers is not considered sufficient…"*，且 *"if a check-out process includes a 3rd party payment provider, that would be in scope"*，配套 SC 1.3.5 要求 `autocomplete` token 暴露用途。
- **精确值怎么取**：FTC 16 CFR 464 §464.1/§464.2 经 eCFR 镜像逐字核验（2026-11-13，Daily eCFR 版 2026-10-30，Source 90 FR 2166, Jan. 10, 2025）；欧盟 (EU) 2019/2161 新增 **Article 6a** 五款与我国《明码标价和禁止价格欺诈规定》第十六/十七/十九/二十一条、消保法实施条例第十条第二款经官方页核验（前者需 headless Chrome 过 WAF，见该资产 §18 第 4 条）；WCAG 2.2 SC 3.3.4 AA（Updated 16 September 2025）/ SC 3.3.7 A / SC 1.3.5 AA W3C 官方页逐字核验；GOV.UK check answers 与 Apple Pay Marketing Guidelines 逐字核验；Baymard 正文被导航超截断、Google Pay 品牌规范 `fetch failed`、Apple HIG JS 渲染 → 取源限制（见该资产 §18）。
- **判学会了**：能三问定位"选哪个 vs 敢不敢付"；能说出四种定价页构型的适用与尺寸（卡内边距 32px / 价格 40–48px / `tabular-nums` / 货币符号 0.5em 上移 0.13em）；能判划线价有没有成交依据、折扣率能不能从两个价格算回；能写出结账三型与复核页七条；能列出 13 个字段的 `autocomplete` token（含 `shipping`/`billing` 前缀）；能验 SC 3.3.4 三选一与金额变化播报；材料见 `references/pricing-checkout.md`。

- [ ] 能说出为什么"总价"必须在用户同意付款前锁定，并指出 FTC 464 的 total price 定义里哪两类费用可以被排除，以及该规则实际只覆盖哪两类商品
- [ ] 能对一个结账页做三项验收：SC 3.3.4 三选一是否成立、复核页每个 `Change` 是否带视觉隐藏文本、返回后已填内容是否仍预填

### 支线 AI · 通知与消息触达（把「该不该发」翻译成六段链路与三平台验收的完成路径）

- **这是什么（链路的内容端）**：与反馈五层（`feedback-states`：L0–L4 时效与 `role="status"`）、文案体例（`ux-writing §7.3`：in-app 右上角通知的标题/正文/按钮）、首启权限（`onboarding-first-run §10`：**何时**问权限）相邻但问题不同——它们分别管「此刻页面内的提示怎么呈现」「站内通知卡怎么写」「权限该在哪个功能点问」；本支线管**「这个事件要不要打扰用户、走哪条通道、什么时候发、被拒之后怎么办、发了之后怎么收」**，核心是六段链路（事件 → 决策 → 通道 → 时机 → 呈现 → 回收）。此前 46 份参考对 `免打扰`=0 / `消息中心`=0 / `未读`=2 / `inbox`=1 近乎零命中，`通知`=38 / `push`=42 绝大多数是图标与提醒语境的顺带提及，判定为结构性空白。
- **三条最重要裁决**：① **同一件事只发一次**——Apple HIG *"Avoid sending multiple notifications for the same thing, even if someone hasn't responded."*；通道失败不换通道补发（短信失败改推 push 就是同一事件第二次打扰）。② **系统权限是一次性资源**——iOS *"Subsequent calls to this method don't prompt the person again."*、Web Permissions §5.2 *"If current state is not "prompt", return current state and abort these steps."*；pre-permission 的全部价值是「别浪费唯一一次」。③ **未读数与角标是状态契约，不是装饰**——iOS 角标语义 *"the number of unread notifications that are available"*、`0` 清除并清空通知中心、`nil` 保持；Android 只允许 `setNumber()` 建议（*"may or may not use this field"*），不得自绘数字。
- **精确值怎么取**：Apple `interruptionLevel` 四档逐字（passive 不亮屏不响 / active 立即亮屏可响 / timeSensitive 破系统控制 / critical 压静音且需 entitlement），且 `timeSensitive` 在 `UNAuthorizationOptions` 里是 Deprecated（引入即废弃，iOS 15.0）→ 时效性走 interruptionLevel 而非授权项；action 上限 4 个（watchOS 同 4），**title/body 无字符上限**（不可编造 40 字符）；Android 渠道五级 importance 与「创建后不可改」两句英文原文（另：官方同页自相矛盾，工程上不赌 MIN/NONE 可被看到）；POST_NOTIFICATIONS 四条坑（13+ 新装默认关 / 升级预授权需已有渠道 / 拒绝后全渠道封锁 / 必须带上下文请求）；Web push 必须带 `TTL`（RFC 8030 *"MUST include the TTL"*，过期后 *"MUST NOT attempt to deliver"*）、`renotify` 必带 `tag`、`actions` 仅 SW 持久通知有效、移动端 `new Notification()` throw TypeError；邮件分类按「主要目的」判（15 U.S.C. §7702 / 16 CFR §316.3(b)），退订 10 个工作日内（§7704(a)(4)(A)(i)）且不得收费或索取额外信息（16 CFR §316.5），一键退订须 `List-Unsubscribe` 含 HTTPS URI + `List-Unsubscribe-Post: List-Unsubscribe=One-Click`（RFC 8058，DKIM 须覆盖这两个头）；GDPR Recital 32 *"Silence, pre-ticked boxes or inactivity should not therefore constitute consent."*；SC 2.2.1 是 3 机制 + 3 例外（不是五个例外），toast 有时限失败只在「没有别的入口能拿到同一信息」时成立。未取到的（M3 角标、Gmail 限额与 0.3% 垃圾率、PECR 软 opt-in、Chrome quiet UI、邮件 600px 宽度）一律不引用，见该资产 §23。
- **判学会了**：能用六问判型把「要不要发」拆成打扰成本 × 信息价值；能说清 P0–P3 四档在 iOS / Android / Web 上各落到哪个具体机制（interruptionLevel / channel importance / 只能「发或立即发」）；能写 pre-permission 并说清拒绝后的三态分流与回捞路径（含 iOS provisional 这条静默投递的第三条路）；能验角标三态、Android 渠道不可变、Web push TTL 与 410 重订阅；能判一封邮件是交易还是营销，并验退订链路与同意依据；材料见 `references/notifications-messaging.md`。

- [ ] 能对任意「要不要发这条通知」走完六段链路判层，并说出为什么通道失败不能换通道补发、以及 P2/P3 在三平台上分别落到什么机制
- [ ] 能写出 pre-permission 的触发点与文案，并列出被拒后的三态分流、iOS provisional 的适用与不适用、以及 Android「拒绝 = 全渠道封锁」的验收口径

## 能力自测（173 条，做到 ≥110 条即达 L2+）

**L0**
- [ ] 眯眼看任何界面，能指出两个打架的元素
- [ ] 能说出一个设计"贵"在哪（不是"好看"这种词）
- [ ] 能判断一段正文行长是否过长

**L1**
- [ ] 说得出导航栏 6 种构型及各自适用场景
- [ ] 知道定价表为什么三档、为什么中档推荐
- [ ] 能指出一个表单的可访问性缺陷
- [ ] 知道 Hero 标题为什么不能超过 2 行
- [ ] 能说出卡片"边框 or 阴影"为什么不能同时用
- [ ] 说得出全局主导航为什么 ≤9 项、底部 tab 为什么 ≤5 项
- [ ] 能指出一个网站导航「职责错配」（如页脚链接混进主导航）
- [ ] 知道 3-click 规则是迷思、信息气味才是关键
- [ ] 能给 tabs 写出正确的 ARIA（tablist/tab/tabpanel + ←/→/Home/End）
- [ ] 能给一场设计评审分清 standalone critique 与 design review，并说清为什么不能混
- [ ] 能说出"分离品味与工艺"是什么意思，并各举一个评审中的例子
- [ ] 知道 NN/g 10 可用性启发式，并能在评审里把"感觉不对"翻成具体条目
- [ ] 知道 design by committee 与 HiPPO 是什么、为什么是头号反模式，评审怎么防

**L2**
- [ ] 能写出三层 token 架构并解释每层职责
- [ ] 知道为什么语义命名优于数值命名
- [ ] 能给出 10 阶色板并说明主色取第几档
- [ ] 说得出暗色模式为什么不是反色
- [ ] 能解释 8 倍数间距系统解决了什么问题

**L3**
- [ ] 能按技术栈选出合适的组件库并说明理由
- [ ] 知道 Core Web Vitals 三个指标的阈值
- [ ] 能说出四档对比度阈值（4.5 / 3 / 3 / 7）且知道**不能四舍五入**
- [ ] 知道焦点框为什么不能只有 2px 内嵌、为什么不能等于品牌主色
- [ ] 能说出模态弹窗的四条焦点要求（入框/循环/Esc/返回）
- [ ] 知道目标尺寸 24/44/60 三档分别对应什么场景
- [ ] 能判断一个库的许可是否可商用
- [ ] 能说出五层反馈（L0–L4）各自解决什么问题，并给一个"错层级"的反例
- [ ] 知道 <1s / 2–10s / >10s 三档分别该用什么加载形态，以及为什么 <1s 不能加 spinner
- [ ] 能一眼指出空态属于五种里的哪一种，并给出对应的唯一主操作
- [ ] 能说出严重错误为什么不能用 toast（而不是"颜色不够红"）
- [ ] 给出任一正文版式，能说出它的行长（字符/字数）、行距比例，并判断是否落在 45–90 字符与 120–145% 的可读区间
- [ ] 拿到一张 A2 海报需求，能独立算出画布尺寸（含 3mm 出血）、安全区、三层信息字号，并说出 3 米外的可读下限
- [ ] 能解释「1080 宽长图正文为什么必须 ≥44px」，并换算任意设计宽度下的等价字号
- [ ] 拿到"帮我设计个 logo"，能先给出 3 个形容词 + 3 个反义词与六维参数，而不是直接开画
- [ ] 能说出标志最小可用尺寸的两种口径（40px/10mm 与「最细笔画 ÷0.75」），并解释为什么缩小到一定程度要换简化版而不是继续缩
- [ ] 能解释「品牌主色为什么是种子色而不是最终色」，并说出三条色阶路线的差别与不可混用的原因
- [ ] 能说出暗色模式品牌色为什么不是反色（primary 40↔80、outline 50↔60），以及主色为什么不能当图表分类色
- [ ] 能解释「暗色表面层级跨度必须大于亮色」（亮色 1.23 vs 暗色 1.50），并说出为什么暗色不能靠阴影表达高度
- [ ] 知道暗色正文为什么不能用 `#fff`（四体系共识），并能说出 Ant 三级文本 45% 在纯黑上只有 4.43 的问题与修法
- [ ] 能判断一个暗色主题的表单边框是否合规（`#424242` 仅 2.09:1 不过 1.4.11，需 `#6f6f6f` 起）
- [ ] 能说出防闪白三件套的正确顺序，并解释 `color-scheme` 不设会导致什么（滚动条与原生控件仍白）
- [ ] 拿到"首屏要不要放背景视频"，能算出它的字节量级（5s 1080p@4Mbps ≈ 2.5MB）并给出把氛围挪到第二屏的替代方案
- [ ] 能解释「同一个 LCP，四段占比该是 40/10/40/10」，并说出为什么单独压图可能一点没快（时间转移到 render delay）
- [ ] 给出 400×300 的展示位与 4000×3000 的源图，能算出 25 倍像素浪费，并说出 DPR 翻倍为什么是 4 倍而不是 2 倍
- [ ] 能说出 `font-display` 五档的阻塞/交换期数值，并解释不写它时 Safari 会怎样（无限期阻塞文本）
- [ ] 能算出 `will-change` 带来的图层内存（宽×高×4），并说明为什么它不能常驻
- [ ] 能判断一个"高级感"效果的价格档位（玻璃拟态/视差/3D/粒子/轮播），并给出至少一个更便宜的替代
- [ ] 能说出小程序单个代码包的上限（2MB）与 `setData` 的两条铁律，并解释为什么"拆组件比减数据更有效"
- [ ] 拿到一个组件，能写出含**九字段**的 spec，并说清哪四类内容才需要标注（例外值/对齐线/尺寸约束/断点）
- [ ] 能说出**9 态矩阵**里最常被漏的两态（read-only 与 loading），并解释为什么 Carbon 的 4.5:1 例外**只给 disabled**
- [ ] 能把一条模糊需求改写成 **3–5 步 Given/When/Then**，且 Then 只验用户可见结果
- [ ] 能说出设计走查的**三遍顺序**与为什么不能从像素开始，并给出 **P0/P1** 的判定差异
- [ ] 能判断一次 token 改名/默认值变更属于 **MAJOR 还是 PATCH**，并说明为什么后者会出事
- [ ] 能说出文案三级尺寸（long/short/micro）各自占界面的比例，并解释为什么 micro 最重要
- [ ] 给一条「用户名无效」的错误提示，能改写成三层结构（发生了什么+为什么+怎么修），并指出原句违反了禁用词表哪几条
- [ ] 能解释为什么按钮禁用 OK，以及 sentence case 为什么是四体系共识（全大写降可读性 10% + 读屏逐字母读）
- [ ] 拿到一个空态需求，能判断属于五种里的哪一种并给出对应的五件套（标题+说明+按钮+次要链接+视觉），并解释为什么失败不能伪装成无数据
- [ ] 能说出演示文稿最小字号 **24pt**（线上 28pt）的原因，并用 Duarte 法验证投影后排可读性
- [ ] 能区分动画（单元素）与转场（整张幻灯片每页 1 个），并说出为什么华丽转场禁用、Morph 只用于跨页位移
- [ ] 给一个 5 行 8 词的幻灯片，能按 **5×5 或 1-6-6** 规则改写，并解释中文 5×5 = 5 行×10 字的原因
- [ ] 拿到「6 项列表依次入场」与「20 项表格入场」两个需求，能分别给出 `200ms + 5×30ms = 350ms` 的 stagger 方案与「整组淡入」的结论，并用 `T = d + (n−1)×s ≤ 400ms` 解释为什么后者不能逐项
- [ ] 能写出 FLIP 的 F/L/I/P 四步与 `invertY = first.top − last.top` 算式，说明为什么预计算必须落在交互后 **100ms 响应窗口**内、以及批量为什么必须「先全读再全写」
- [ ] 能说出 View Transitions 的 UA 默认参数（**0.25s / ease / both**），以及 `view-transition-name` 重名时 `ready` reject、`finished` fulfill、`updateCallback` 仍执行三者为何不矛盾，并解释主流程为什么不能 await `ready`
- [ ] 能画出 `entering/entered/exiting/exited` 四态的状态×事件矩阵，说明快速连点如何从当前视觉值反向恢复，并指出为什么全局 CSS `prefers-reduced-motion` 归零管不住 Svelte / WAAPI 过渡

- [ ] 能说出出海事哪三层要同时改（标记层 / 布局层 / 数据层），并解释为什么「只翻译字符串」在 RTL 与复数上必翻车
- [ ] 能背出 W3C/IBM 膨胀表的分档（**≤10 字符 200–300%** / 11–20 / 21–30 / 31–50 / 51–70 非单调 / >70 130%），并说清为什么 `ux-writing.md` §13 的「+40%」不能用于按钮、Microsoft 的 +40% 又是什么
- [ ] 能解释 `lang` 与 `dir` 为什么是两个东西、WCAG 3.1.1 A 与 3.1.2 AA 分别要求什么，以及 W3C 为什么明令禁止用 CSS 声明 base direction
- [ ] 能把一段写死 `margin-left` / `width` / `left` / `text-align:left` 的 CSS 全量改写成逻辑属性，并说出 RTL 下 `start` 为什么不永远是 left
- [ ] 能列出 Material 镜像白/黑名单各至少 5 项，并解释「媒体进度条不镜像」与「数字不镜像但要本地化字形」两条为什么容易混
- [ ] 能解释 CLDR 复数 `one` 为什么不等于数字 1、为什么中文只有 `other` 反而最容易漏测，并写出一条带 `select` 外层 + `plural` 内层 + `offset:1` 的 ICU 消息
- [ ] 能说出 `Intl` 为什么不是构造器、本机 Node v22.22.2 实测 `Intl.DurationFormat` 抛什么错、生产代码该怎么降级，以及 `zh_cn` 为什么会抛 `RangeError`
- [ ] 能设计一个伪本地化用例（音标 + ①–⑨ + `^` 定界 + microcopy 3× 加长），并说出它能分别暴露哪四类缺陷；能解释为什么姓名表单应只给一个 `Full name`

- [ ] 能说出 Diátaxis 四象限各自读者状态与义务，并解释为什么「在 reference 里展开一段为什么」会同时毁掉参考页和解释页
- [ ] 能默写 GOV.UK 组件页九段式，并指出哪三段构成「活文档四件套」、为什么最容易被砍掉
- [ ] 能用五问验收给一份组件文档打分，并说出示例代码五条硬规则与 descriptive link text / alt 的具体写法
- [ ] 能说出 Docusaurus 官方为什么建议多数站点不做版本化，以及 <10 版本、preview 2–3、patch 不切版本、`unmaintained` banner 四条口径
- [ ] 能写出符合 Keep a Changelog 1.1.0 的 `[Unreleased]` 段落（六类变更齐全），并解释为什么不能倒 git log、MAJOR 迁移文档为什么要能被机器校验
- [ ] 能辨析 DTCG preview draft 与 published 2025.10 该引用哪条 URL，并说出 `$description` / `$deprecated` 如何变成 token 文档源
- [ ] 能写出 Storybook `tags: ['autodocs']` 与 `['!autodocs']` 的差别、MDX `of={}` 的 attached/unattached 之别，并列出 GOV.UK 贡献准入 Useful/Unique 与 Usable/Consistent/Versatile 各属哪道门槛

- [ ] 能说出 AI 设计五层地图每层的人工闸门，并解释为什么「定受众与语气 / 判上线与否 / 担法定责任」三类活不能交给 AI
- [ ] 能背出中国《标识办法》的施行日期与传播端三档文案「属于 / 可能为 / 疑似」，并说出第 10 条禁止的是哪四类行为、无标版日志要留多久
- [ ] 能区分显式标识与隐式标识、列出元数据三类要素，并解释为什么导出·下载·复制环节最容易丢标识
- [ ] 能解释 USCO 的 *"but not the mere provision of prompts"*，并说出「可举证创作链」为什么要留档六步而不是只留一段 prompt
- [ ] 能辨析法定内容标识 / C2PA Content Credentials / 版权归属与商用授权三者，并说出 C2PA 明确**不断言**的四类事项
- [ ] 能说出 EU AI Act Art. 50 的适用日期，并解释「首次交互或首次暴露时告知」为什么是交互设计任务而不是一句隐私政策
- [ ] 能写出 prompt 四区块结构，并判断「换模型快照 / 改默认措辞 / 修错别字」分别属于 MAJOR、MINOR 还是 PATCH
- [ ] 能说出 `DESIGN.md` 九章里哪一章不可省、为什么，并区分「给 AI 读的契约」与「给人读的设计系统文档站」
- [ ] 能用 AI Slop Test 判一份生成稿，并说出 8 维 DO/DON'T 里最容易翻车的两维与生成前必答的三问
- [ ] 能列出 AI 生成界面的 12 类固有缺陷，并说明「九态缺失」「假数据」「token 漂移」分别接回哪份既有资产
- [ ] 能说出 HAX 18 条里「可关闭且记住」「可纠错」「全局控制」「变更通知」对应的编号，并解释为什么官方未逐条标注阶段归属时不能臆造边界
- [ ] 能按选型三问评估一个仓库（许可 / pushed_at / 可验收），并说明 GPL-3.0、AGPL-3.0、NOASSERTION 为什么是商用红灯

- [ ] 能说出 CPPA §7004(a)(2) 拒绝/接受两条路径**步数的起止点**，并列出法规点名的三种不对称按钮构型及其正解
- [ ] 能解释为什么「管理偏好 / Preferences」不能替代拒绝按钮、为什么 `Ask me later` 在语义上等于没有拒绝，并写出 §7004(a)(3) 的三个措辞与控件陷阱
- [ ] 能说出 PIPL 第 15/16 条为什么让 cookie wall 直接违法、第 14 条为什么要求用途变更时**重新**取得同意、第 24 条给个性化推送留了哪两条路
- [ ] 能写出《互联网广告管理办法》第 10 条「一键关闭」的三条可测数值与五类禁止情形，并说明开屏广告为什么同样适用
- [ ] 能裁决「自动续费须提前五日提醒」是否现行法，说出 **2025-03-18 总局令第 101 号 / 2025-05-01 施行** 与现行第十八条的**两个时点**、服务期内义务和第四十一条罚则
- [ ] 能列出《网络交易监督管理办法》第 13/16/17 条对默认值的三条禁区，并解释「记住用户偏好」为什么在搭售场景反而违规
- [ ] 能说出国务院令第 766 号第 42–45 条各自对应的设计动作，尤其是第 44 条「单次与单日累计」双限额与第 45 条三类功能必须整体下线
- [ ] 能解释「无障碍达标仍可能是欺骗性设计」，说出 COGA 八目标中至少四个、以及 `Test with real users` 为什么必须由认知与学习障碍者本人参与而非团队代判
- [ ] 能辨析 `deceptive.design` 现行 18 类与旧教程分类的差异，并解释为什么静态扫描应断言「路径对称 / 默认值为 false」而不是枚举新套路名称
- [ ] 能说清组件 API 的「三份所有权」分别指什么，并举出一个"样式没问题但组件就是难用"的反例归因到错误的所有权划分
- [ ] 能写出受控 / 非受控的唯一判定式（`prop !== undefined`），并说明为什么组件生命周期内不能从受控切到非受控、为什么 `value` 不能是 `undefined` / `null`
- [ ] 能解释 `value` + `defaultValue` 同时传、以及 `value` 无 `onChange` 分别会发生什么，并说出 `defaultChecked` 的正确用途
- [ ] 能列出至少三套「换元素」API（`asChild` / Ariakit `render` / MUI `slots` / Vue slot），并说出各自 props 合并优先级中最容易被忽略的一条
- [ ] 能解释 Ariakit `render` 的元素形态与显式 render function 在 HTML props 合并责任上的差别，以及 `null` 与 `undefined` 的不同待遇
- [ ] 能说清自定义组件「开放扩展」四条，并指出中间层吞掉 `...rest` 会连带丢失哪些用户能力（aria / data / 事件）
- [ ] 能解释 React 19 下为什么不能把「自定义组件必须 `forwardRef`」写成跨版本硬规范，并说明规范里必须标注什么；能说出 `{ open, close }` 命令式 handle 为什么是官方反例
- [ ] 能给出复合组件单 tab stop 的两种焦点策略、focus 与 selection 的视觉区分要求，以及 modal dialog 关闭后焦点该回到哪里
- [ ] 能判级一次组件 API 改动：改默认值 / 改 props 合并优先级 / 改受控判定 / 改键盘策略 / 新增可选 prop / 改文档注释，各属 MAJOR·MINOR·PATCH 哪一级，并说明 MAJOR 必须附带什么

- [ ] 能说出 ISO 9241-11 把可用性拆成的三件独立的事（有效性/效率/满意度），并解释为什么满意度高不能替你证明任务能完成
- [ ] 能算出「5 个用户约暴露 84% 问题、10 个 98%、20 个 100%」的发现率，并解释为什么样本量不是越大越好
- [ ] 能写出定量比例估计公式 `n ≈ Z²·p(1−p)/E²`，并算出 p=50% / 80% / 5% 各自需要多少样本
- [ ] 能说出 SUS 的计分方式（奇偶数反向 ×2.5）、行业基准 68 是什么含义，并解释「一致作答恒为 50」为什么是特性不是缺陷
- [ ] 能解释 A/B 里 p<0.05 只说明「不太可能纯巧合」，并说出为什么必须同时报相对提升、95% CI（CI 跨 0 即无 winner）、护栏指标与随机单元=用户
- [ ] 能区分可用性表与无障碍表，并解释为什么「我们没恶意」不能替已知缺陷辩护
- [ ] 能说出图标统一用 24×24 viewBox、活动区留 2px 边、同一 keyline 同形状的原因（视觉重量一致），并指出跨库碎片化的根因
- [ ] 能说出描边「固定 2px」与「光学缩放」二选一并全库统一的原因，且能指出混用的后果
- [ ] 能判断一个图标是装饰还是有意义，并分别给出 `aria-hidden`+`focusable=false` 与 `role=img`+`aria-label` 的正确写法
- [ ] 能说出图标-文字间距默认 8px（最小 4px）、可点图标命中区 ≥44px、spinner `1–1.4s linear infinite` 且 `prefers-reduced-motion` 降级
- [ ] 能区分内联 SVG / SVG Sprite / 图标字体 / 组件四套交付格式，并说出图标字体为何可访问性差、Material 为何必须子集化
- [ ] 能根据框架绑定 / 风格统一 / 体积敏感三问，从 Lucide / Tabler / Fluent / Material Symbols / Radix 里选库
- [ ] 能解释图标字体读屏念乱码的根因与整库 `aria-hidden` 的解法
- [ ] 能说出图标「永不只靠颜色」的原因，并给出状态图标的形状+颜色+文字三样方案

**L4**
- [ ] 面对"要高级又要热闹"能给出取舍方案
- [ ] 能发现需求里没提但致命的盲区
- [ ] 被质疑时能说清判断依据而非改口
