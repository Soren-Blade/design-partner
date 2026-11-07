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

## 十九条专题支线（可与主线并行）

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

## 能力自测（120 条，做到 ≥92 条即达 L2+）

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
