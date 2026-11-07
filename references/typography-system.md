# 字体排印系统（Typography System）

> 快照 2026-11-07 · 30 节 · 12 场景 · 20 反模式 · 20 自检 · 6 段可抄代码

把「字体靠挑好看的、字号随手写、行距凭感觉」变成**可计算的决策**。本文件不替代 `design-tokens.md`（token 三层架构）/`performance-design.md`（字体加载与 CLS 预算）/`chinese-design.md`（中文场景惯例）/`visual-style-taxonomy.md`（风格四维信号里的 Typography 维）/`brand-identity.md`（品牌字体人格），而是给它们补上**字体本身的底层机制**：字号为什么不能用 px、用户把间距改到 WCAG 门槛时页面为什么不许塌、数字为什么会在表格里跳、`font-family` 到底怎么回退、可变字体和 OpenType 特性怎么用、字体授权哪些事不能做。

**一句话立场**：排印不是「选一款字体」，是**六层契约**——覆盖（有没有字）、尺度（能不能缩放）、节奏（行高/行长/段距）、字形（数字与特性）、加载（FOIT/CLS）、授权（能不能分发）。任何一层没签，成品都会在某个用户手里翻车。

---

## 1 · 为什么单列字体排印系统

字体排印是和色彩科学并列的**基础设计支柱**，但此前本知识库没有独立文件：字体知识散落在 `performance-design.md`（19 行，讲加载）、`brand-identity.md`（13 行，讲人格）、`visual-style-taxonomy.md`（10 行，讲风格信号）、`knowledge-map.md`（8 行，讲路线）等边角。上游文件都在**用**字体，没人讲**字体本身怎么算、怎么被用户改、怎么被浏览器回退**。这一层不补，「正文 16px、行高 1.5」就永远是一条没有理由的口诀。

**本轮三条最重要裁决**（后文逐条给官方原文与验收方法）：

1. **`font-size` 用 px 写正文＝把用户的最小字号设置锁死**。MDN 原文：*"To maximize accessibility, it is generally best to use values that are relative to the user's default font size."* 且 *"Defining font sizes in `px` is **not accessible**, because the user cannot change the font size in some browsers."* → 正文字号走 `rem`（相对根元素），不用 `em`（会 compounding），`px` 只允许出现在非文本尺寸与边框/描边。配合 WCAG 2.2 **SC 1.4.4 Resize Text（AA）**：除字幕与图片文字外，文本须能**无辅助技术放大到 200%** 而不丢内容或功能。
2. **WCAG 2.2 SC 1.4.12 Text Spacing 是「抗压测试」，不是「默认样式表」**。官方 Note 1 原文：*"Content is not required to use these text spacing values. The requirement is to ensure that when a user overrides the authored text spacing, content or functionality is not lost."* 四项门槛是 `line-height ≥ 1.5×`、`段后距 ≥ 2×`、`letter-spacing ≥ 0.12×`、`word-spacing ≥ 0.16×`（均相对 font size），且**同时设置、不改其他属性**；验收动作是「用户覆盖后不裁切、不重叠、不丢功能」，不是「作者默认写成 1.5」。这条被广泛误读，是固定高度卡片/按钮/表单在间距覆盖下炸开的主因。
3. **`font-family` 是逐字符回退，不是逐字体回退**。第一款字体装了不代表就停在它；缺 glyph 会继续往下找，最后才是 generic family（**必须放最后、不能加引号**）。所以「中文 + 西文 + 符号 + emoji」混排必须显式写完整回退链，并配 `unicode-range` 分片，否则字体加载与 CLS 一起失控。

与色彩科学的对照：配色有 OKLCH 这套可计算坐标，排印没有「唯一正确字号」，但有**一组不可协商的可访问性边界 + 一组可复现的工程契约**；越界就是缺陷，不是品味差异。

---

## 2 · 排印决策的六层模型（先判层，再谈审美）

需求里出现「字体 / 字号 / 行距 / 排版」时，先定位是哪一层出问题，不要一上来换字体。可访问性、对比度、表单与验收问题往往落在第 2/3 层，换一款字体根本修不了。

| 层 | 问的问题 | 判据 | 主要落点 |
|---|---|---|---|
| L1 **覆盖** | 这个字有没有？ | 字符集 / `unicode-range` / CJK 分片 / 缺字 tofu | §12 §13 |
| L2 **尺度** | 用户能不能放大？ | `rem` / 200% 缩放 / `clamp()` / 不写死高度 | §4 §8 |
| L3 **节奏** | 覆盖间距后塌不塌？ | 1.4.12 四项 / 1.4.8 行宽 / 行高比率 / 段距 | §5 §6 §7 |
| L4 **字形** | 数字会不会跳、斜体有没有？ | `tabular-nums` / 可变轴 / 高位属性优先 | §9 §10 §11 |
| L5 **加载** | FOIT 多久、CLS 多少？ | `font-display` 五档 / `size-adjust` 度量对齐 | §14 §15 |
| L6 **授权** | 能不能打包分发与改字？ | OFL 1.1 五条件 / RFN / 逐字体 license | §18 |

**裁决顺序**：L6 先过（授权不合规整案作废）→ L1（没字什么都别谈）→ L2/L3（可访问性硬边界）→ L4（可读性细节）→ L5（性能），**最后**才谈「衬线还是无衬线 / 气质对不对」。气质判断归 `brand-identity.md` 与 `visual-style-taxonomy.md §2`，本文件不越界。

---

## 3 · 字体选型：覆盖 / 回退 / 授权三个前置，而不是「挑好看的」

选型的可访问性、加载性能与合规验收都从这三个前置开始；「好不好看」是三关全过之后才允许问的第四个问题。缺字、锁死缩放、授权不清，都会让界面在特定用户或分发场景下直接失效。

1. **覆盖**：先列出产品实际字符集（简中 / 繁中 / 日文 / 韩文 / 拉丁扩展 / 阿拉伯数字 / 货币符号 / emoji / 图标 private-use）。CJK 字体不是「装一款就够」，`notofonts/noto-cjk`、`adobe-fonts/source-han-sans` 这类是**按语言子集**分发（SC/TC/JP/KR 字形有差异），W3C clreq 也明确**区域差异大于简繁差异**。
2. **回退**：写完整链并在真实设备上测「缺字是否落 tofu」「西文是否用了中文字体的拉丁字形（通常很丑）」「emoji 是否彩色」。generic family 放最后且**不加引号**（`"sans-serif"` 是字体名不是通用族）。
3. **授权**：逐字体查 license，别只看仓库级 license。GitHub API 对 `google/fonts`、`adobe-fonts/source-han-sans`、`notofonts/noto-cjk`、`unicode-org/icu` 均返回 `NOASSERTION`（混合/自定义许可），**不能据此推断「无许可」或「OFL」**，必须进对应字体目录读 `OFL.txt` / `LICENSE`。

**可执行判据**：选一款字体要能同时答出 ① 目标字符覆盖率与分片方案 ② 回退链完整顺序 ③ 许可文件位置 + 是否允许 web embedding + RFN 是否保留。三问答不出，不进生产。

---

## 4 · 字号阶梯与相对单位（px 不可访问裁决）

「正文用多大字号」「排版很挤该调哪里」先落到这一层：字号是**可访问性与验收**问题，用户在浏览器里改默认字号、改到 200%，界面必须还能读、不裁切、不重叠，表单与按钮不能丢功能。这一层出错，后面所有排印细节都没有意义。

- **MDN 原文（已核验）**：`font-size` 的 `<length>` 里，`em`/`ex` 相对父元素，`rem` 相对根 `<html>`；Note：*"To maximize accessibility, it is generally best to use values that are relative to the user's default font size."*；Pixels 段：*"Defining font sizes in `px` is **not accessible**, because the user cannot change the font size in some browsers… Avoid using them for font sizes if you wish to create an inclusive design."*
- **`em` 的 compounding**：MDN 举例父 `1.6em` 再嵌 `1.6em` → 16px 基准下外层 25.6px、内层 **40.96px**（16×1.6×1.6）。`rem` 就是为绕开这个发明的，同一例子三层全是 25.6px。→ 字号阶梯一律 `rem`；`em` 只用于「相对当前字号的间距」（如 `padding: 0.5em`）这种**有意**跟随的场景。
- **换算基准**：浏览器默认 `medium` = 通常 16px（不是保证值，用户可改）。`em 换算公式 = 目标 px ÷ 父元素 px`（MDN 原文）。写 `rem` 时不要反推成死 px，标注「以 16px 计约等于」即可。
- **阶梯取值**：沿用 `SKILL.md` 第 5 步的 12/14/16/20/24/32/48，改成 rem（0.75/0.875/1/1.25/1.5/2/3），**正文从 1rem 起**；中文正文按 `chinese-design.md` 与 `visual-style-taxonomy.md §7` 不低于 14px（0.875rem）。
- **流式字号**：`clamp()` 可用，但下限必须 ≥1rem 且中间项带 `rem`/`vw` 混合，不能只给 `vw`（纯视口单位同样绕过用户字号设置）。响应式细节见 `responsive-design.md`。
- **`px` 允许出现的地方**：边框宽度、描边、`letter-spacing` 的绝对值微调（但要能承受 1.4.12 覆盖）、图标尺寸、栅格 gutter——**不用于 `font-size` 与承载文字的固定高度**。

---

## 5 · 行高、行长与段落节奏（可计算，不靠感觉）

行高与行长决定长文可读性，也是对比度、可访问性与验收里最常被跳过的一组数值；三段式节奏（行内 / 段间 / 块间）必须分开定，不能一个 `line-height` 打天下。

- **行高比率（M3 官方，已核验）**：`applying-type` 原文——*"For larger type legibility using styles like title, headline, and display, we recommend a line height ratio of **1.2 times** the type size"*；*"For smaller body copy using styles like body and label, we recommend a line height ratio **around 1.5 times** the type size."* 太紧破坏阅读流，太松行与行不成组。
- **本知识库既有口径**：`SKILL.md` 第 5 步「正文 16px 起，行高 1.5–1.7，行长 60–75 字符」；`presentation-design.md` 给中文演示行距 1.4–1.6。两者不冲突：M3 的 1.2 只给**大字号标题**，正文仍走 1.5 上下。写 token 时按角色分两档，不要全局一个值。
- **行长（WCAG 2.2 SC 1.4.8 Visual Presentation，AAA）**：文本块宽度 **≤80 characters or glyphs（CJK ≤40）**、`Text is not justified`（禁两端对齐）、段内行距 `space-and-a-half`、段间距至少 `1.5 times larger than line spacing`。行长超标时优先缩容器而不是缩字号。
- **三段节奏分离**：`line-height`（行内）/ `margin-block-end`（段间，≥2× font size 才扛得住 1.4.12）/ 块间距（章节，走 spacing token）。三者都写死 `px` 会在间距覆盖时叠爆。
- **两端对齐是硬禁**：`text-align: justify` 在窄栏与 CJK/西文混排下制造词间「河流」，1.4.8 明令 `Text is not justified`；中文也不靠加字距凑齐行尾。
- **中文行高**：汉字 1:1 方框（clreq §1.2）、字面率高，同字号视觉比拉丁更满，正文行高通常需比拉丁略宽松；`visual-style-taxonomy.md §7` 给中文极简场景 ≥1.6。

---

## 6 · WCAG 2.2 三关硬数值（1.4.4 / 1.4.8 / 1.4.12）

字体排印在 WCAG 2.2 里有三条独立准则（Resize Text / Visual Presentation / Text Spacing）；把字号放大不等于过关，三条各有自己的门槛与例外，混成一句「字号够大就行」会漏掉文本间距与行宽。

| 准则 | 级别 | 硬数值 / 原文要点 | 常见翻车点 |
|---|---|---|---|
| **SC 1.4.4 Resize Text** | AA | 除 `captions` 与 `images of text` 外，文本应能**无辅助技术放大到 200 percent** 且无内容/功能损失 | `height` 写死的按钮、Canvas 文字、`overflow:hidden` 卡片 |
| **SC 1.4.8 Visual Presentation** | AAA | 前景/背景用户可选；行宽 **≤80 字符（CJK ≤40）**；**Text is not justified**；段内行距 `space-and-a-half`；段间距 ≥1.5× 行距；无辅助技术放大 200% 且**无横向滚动** | 两端对齐、超宽正文栏、`white-space:nowrap` 长标签 |
| **SC 1.4.12 Text Spacing** | AA | 同时设 `line-height ≥1.5×`、`段后距 ≥2×`、`letter-spacing ≥0.12×`、`word-spacing ≥0.16×` font size，**且 changing no other style property**，结果 `no loss of content or functionality` | 固定高度容器、`text-overflow:ellipsis` 误伤、绝对定位标签 |

**三条最容易写错的口径**：

1. **1.4.12 不是默认样式表**。官方 *Note 1*：*"Content is not required to use these text spacing values. The requirement is to ensure that when a user overrides the authored text spacing, content or functionality is not lost."*；*Author Responsibility*：*"This SC does not dictate that authors must set all their content to the specified metrics, or provide a mechanism to do so."*；并明确 *"The values in the SC are a baseline… not see them as a ceiling."* → **验收是「抗压」，不是「照抄」**。
2. **例外与不适用**：条文 Exception——不使用某些 text style properties 的语言/文字只需符合实际存在的属性；Applicability 明确 PDF 不适用、视频内嵌字幕与图片文字不预期适配，`canvas` 文字按 images of text 处理。Note 2 提醒部分书写系统用段首缩进等本地做法。
3. **文本对比度是另一条签字**：M3 `applying-type` 给 **大文本 3:1 / 小文本 4.5:1**，且 *"Hyperlinked text must also be underlined."*（链接不能只靠颜色）。与 `color-science.md §6` 的 WCAG 2.x 相对亮度算法、非文本 ≥3:1 一起过；排印改字号会改变「大文本」判定，别在改完字号后忘记重算对比度。

---

## 7 · 文本间距覆盖验收（注入式实测五步）

这条是 1.4.12 的**可执行脚本**：把四项间距一次性注入页面，检查按钮、卡片与输入框是否裁切、重叠、丢功能。不改其他属性是条文硬要求，注入时别顺手改 `font-size` 或 `padding`。

**验收五步**：

1. 注入书签/CSS（见 §23.3）：`* { line-height: 1.5 !important; letter-spacing: 0.12em !important; word-spacing: 0.16em !important; } p { margin-block-end: 2em !important; }`。注意 `em` 在这里相对当前 `font-size`，正好等于条文的「× font size」。
2. 逐屏看**裁切**：固定 `height` 的按钮/标签/badge、单行 `text-overflow: ellipsis` 的表格单元格、`overflow:hidden` 的卡片标题。
3. 逐屏看**重叠**：绝对定位的角标、图标与文字、多列卡片里高度锁死的 footer。
4. 逐表单看**功能**：label 是否被挤出可视区、错误提示是否与输入框重叠、必填星号是否遮住文字、`input` 高度是否写死导致字被切（WCAG 场景里最高频的失败）。
5. 看**横向滚动**：1.4.8 要求 200% 放大且无横向滚动；长词、URL、代码、表格数字列最容易破。

**修复优先级**：去掉固定高度 → 用 `min-height` + `padding` → 允许换行或 `overflow-wrap:anywhere` → 最后才考虑缩小字距（但别把用户覆盖抵消掉）。**不要**用 `!important` 把作者样式顶回用户覆盖之上，那正是条文禁止的「干扰用户覆盖」。

---

## 8 · 200% 缩放与容器弹性（按钮 / 输入框 / 卡片）

200% 文本缩放与 1.4.12 间距覆盖是**两次独立测试**：一个改字号，一个改间距，两者都会让固定高度的表单与按钮失效。只测其中一次等于没验收。

- **测法 A（文本缩放）**：浏览器「仅放大文字」到 200%，或把 `<html>` 默认字号从 16px 改到 32px（等效）。检查正文不裁切、按钮文字不出框、表单 label 与帮助文案不重叠、无横向滚动。
- **测法 B（浏览器整页缩放）**：Ctrl+`+` 到 200%，此时 `rem` 与 `px` 一起放大，容器也变窄——**这不能替代测法 A**，因为它掩盖了「px 字号不跟随用户设置」的问题。两个都要跑。
- **容器三条硬规则**：① 承载文字的元素不写 `height`，写 `min-height` + `padding`；② 不写 `white-space: nowrap` 在动态文案上（用户姓名、翻译串、金额）；③ 表格数字列用 `tabular-nums` + 允许横向滚动容器，但整页不出现横向滚动（1.4.8）。
- **与 i18n 叠加**：`i18n-localization.md` 已裁决英文→欧洲语言短串膨胀 200–300%、microcopy 按 2–3× 弹性。文本缩放与文案膨胀会**叠乘**，验收要用「最长语言 × 200% 字号 × 1.4.12 间距」三重叠加，不是单跑一遍。
- **`canvas` 文字是 dead end**：1.4.12 把 canvas 文字当 images of text，不预期适配；业务文字一律用 DOM，别画进画布。

---

## 9 · Variable Fonts 与五个注册轴

可变字体把「一款字重一个文件」变成连续轴，能同时解决加载体积与 CLS：但轴用错会破坏对比度与视觉层级，且必须遵守「高层 CSS 属性优先」。

- **五个 registered axes（OpenType 规范）**：`wght`（weight）、`wdth`（width）、`slnt`（slant）、`ital`（italic）、`opsz`（optical size）。注册轴 **小写**；custom axes **大写**（如 `GRAD`）。
- **高层属性优先**：能用 `font-weight` / `font-stretch` / `font-style` / `font-optical-sizing` 表达的，就不要写 `font-variation-settings`。后者是低位 API，直接写会**绕过**高层属性的级联与继承语义，且多个声明顺序敏感。
- **`GRAD` 轴的价值**：custom axis 可在**不改变字形 advance（不触发 reflow）**的前提下调整笔画粗细密度——适合 hover / 暗色模式下微调文字重量而不让布局跳动；这是普通 `font-weight` 做不到的。用它之前确认字体确实带这个轴。
- **`opsz` 与展示字号**：M3 `applying-type` 明确 *"If available, set the appropriate optical size to your usage."*；display / headline 允许更表现性的字体，body / label 禁装饰字体（*"Avoid expressive or decorative fonts for body text"*）。
- **文件数不是越少越好**：可变字体单文件覆盖多字重，但 CJK 全字集依然是体积大头；仍要与 §13 的 `unicode-range` 分片配合。
- **动效无关**：可变轴变化不是 motion，但连续动画轴值会引发重绘，不进「有目的才动」的动效系统；`prefers-reduced-motion` 不覆盖静态轴设置。

---

## 10 · 数字特性与 tabular-nums（表格 / 时钟 / 频繁变化数值）

数字是排印里最容易被忽略的**布局稳定性与对比度**问题：比例数字让表格列歪、让计时器每跳一秒抖一次；这不是审美，是缺陷。

- **M3 官方（已核验）**：`applying-type` 原文——*"Use tabular figures (also known as monospaced numbers) rather than proportional digits in tables or places where values may change often, such as clocks."*，理由 *"to keep values optically aligned for better scanning"* 与 *"prevent layout shifting when values change"*。
- **`font-variant-numeric` 与 OpenType tag 对照（MDN 已核验）**：

  | CSS 值 | tag | 用途 |
  |---|---|---|
  | `lining-nums` | `lnum` | 数字全坐基线，表格/UI 默认 |
  | `oldstyle-nums` | `onum` | 3/4/7/9 带下伸，长文正文更融合 |
  | `proportional-nums` | `pnum` | 数字宽度不等，正文内嵌数字 |
  | `tabular-nums` | `tnum` | **等宽数字**，表格/时钟/金额/倒计时/频繁变化值 |
  | `diagonal-fractions` | `frac` | 1/2 斜线分数 |
  | `stacked-fractions` | `afrc` | 上下堆叠分数 |
  | `ordinal` | `ordn` | 1st / 2nd / 1a 上标序数 |
  | `slashed-zero` | `zero` | 带斜杠 0，区分 O/0（代码、ID、验证码） |

- **落地规则**：表格、仪表盘、价格、倒计时、实时数值、表单里的金额输入 → `font-variant-numeric: lining-nums tabular-nums;`；长文段落里的年份/数量 → `proportional-nums` 可保留；ID/验证码 → 追加 `slashed-zero`。
- **与 dataviz 的界线**：图表坐标轴数字归 `dataviz.md`，但要同样开 `tabular-nums`，否则刻度标签会左右游移。
- **别用「等宽字体」代替**：`font-family: monospace` 会把字母也等宽化，是排版降级；要的只是数字等宽，用 `tnum`。

---

## 11 · 高位属性优先，低位 API 兜底

OpenType 特性的可访问性与验收风险在于「写错层级」：低位 API 会绕过继承与级联，导致同一段文字在不同组件里表现不一致，且难以被用户样式覆盖。

- **MDN 原文（已核验）**：`font-feature-settings` 页开头——*"Whenever possible, Web authors should instead use the `font-variant` shorthand property or an associated longhand… These lead to more effective, predictable, understandable results than `font-feature-settings`, which is a **low-level feature** designed to handle special cases where no other way exists"*；并特别点名 *"`font-feature-settings` shouldn't be used to enable small caps."*（small caps 走 `font-variant-caps`）。
- **低位语法三条**：tag 名**必须是 4 个 ASCII 字符**（多于/少于 4 个或含 `U+20–U+7E` 之外字符即整条 descriptor 无效）；`on`/`off` 等价 `1`/`0`；省略值默认 `1`。非布尔特性（如 `salt`）的数值表示选第几个替代字形。
- **优先级反直觉点**：`font-variant-*` 是高层、可继承、语义清晰；`font-feature-settings` 是**逐声明**的字符串列表，后写的会覆盖先写的同名 tag，且不会因为父元素设了就自动继承语义（虽然属性本身 inherited，但值是原始字符串）。混用两者时以低位为准 → 组件库里最容易出现「全局开了 tnum、某组件被 `font-feature-settings: "pnum"` 悄悄关掉」。
- **裁决**：`font-variant-*` 覆盖 90% 场景；`font-feature-settings` 只用于字体独有的 custom feature（如 `ss01`、`cv05`）且必须写在组件内、附注释说明「为什么没有高层属性」。

---

## 12 · font-family 逐字符回退算法（加载 / 缺字 / 验收）

`font-family` 的回退不是「找第一款已安装字体」，而是**逐字符**匹配；这条机制决定了 CJK 混排、缺字 tofu 与字体加载量的全部行为，也是 CLS 与验收的常见盲区。

- **算法**：浏览器对**每一个字符**依次尝试列表里的字体；第一款字体装了但**缺这个 glyph**，会继续往下一款找，直到找到或落到 generic family。所以「列表里第一款装了就停」是错的。
- **generic family 放最后且不加引号**：`"sans-serif"` 加引号后是一个**字体名**，不是通用族；加了引号就失去兜底。CSS generic families 含 `serif` / `sans-serif` / `monospace` / `cursive` / `fantasy` / `system-ui` / `ui-serif` / `ui-sans-serif` / `ui-monospace` / `ui-rounded` / `math` / `fangsong` 等。
- **`system-ui` 的适用边界**：适合 UI 控件文案（按钮、菜单、系统标签），**不适合大段正文**——它跟随 OS 变更，跨平台行高与字面率不一致，长文可读性不可控。正文字体要显式指定。
- **回退链书写范式**：`font-family: "Inter", "Noto Sans SC", system-ui, sans-serif;`——西文字体在前（先接住拉丁字符），CJK 字体在中（接住汉字），`system-ui` 与 generic 在后兜底。反过来写会让中文正文被中文字体自带的拉丁字形接管。
- **验收**：拿一段含「中文 + English + １２３ 全角 + €¥ + emoji + 生僻字」的测试串，逐字看是否 tofu、是否有字符明显来自另一款字体（字重/基线不齐）。这一步不能靠设计稿目测。

---

## 13 · unicode-range 子集化与 CJK 分片（性能 / CLS / 验收）

「中文字体太大」「字库太大」的正解是 CJK 分片，不是缩字号：字体子集化直接决定加载体积与 LCP/CLS，也是 CJK 站点最有效的性能手段；但「分片粒度」与「下载触发条件」写错会让优化完全失效。

- **MDN 原文（已核验）**：*"If the page doesn't use any character in this range, the font is not downloaded; if it uses at least one, **the whole font is downloaded**."* → **触发条件是「至少一个字符」，且下载的是整个 font resource**。所以分片必须按「页面实际可能出现的字符集」切，粒度过粗等于没优化。
- **语法三种**：单码点 `U+26`；区间 `U+0025-00FF`；通配符 `U+4??`（等价 `U+400–U+4FF`）。初始值 `U+0-10FFFF`（即全量）。Baseline widely available since July 2015。
- **CJK 分片策略**：按 Unicode 区块 + 使用频率切成多片（常用字 / 次常用 / 扩展 A/B / 标点 / 拉丁 / 假名 / 谚文），每片一个 `@font-face` + 独立 `unicode-range`；Google Fonts 对 Noto Sans SC 就是这么做的。**注意**：只要页面出现某一片里的**一个**字，该片整份下载 → 用「高频字集」做第一片收益最大。
- **与 §14 联用**：每片都要写同一个 `font-display`，否则不同字符的 FOIT 行为不一致，长文会出现「半页已经换了字体、半页还是 fallback」的抖动。
- **与 §15 联用**：分片后各片的 fallback 度量可能不同，`size-adjust` 要按片调，否则换字体瞬间仍会跳。
- **口径**：CJK 全字集 >10000 字形（`performance-design.md` 既有结论）；WOFF2 相对 WOFF 约省 30%。这些是量级判断，**具体字节数必须实测自己的字体文件**，不照抄别人的数字。

---

## 14 · font-display 时间线与五档选择（性能 / CLS / 验收）

字体加载策略决定 FOIT/FOUT 与 CLS，是排印与性能的交界；五档不是「哪个更好」，是「哪个能接受字体不出现」。

- **MDN 原文（已核验）**：三阶段——**font block period**（字体未加载时渲染*不可见*的 fallback，即 FOIT）、**font swap period**（渲染可见 fallback，加载成功后替换，即 FOUT）、**font failure period**（视为加载失败，走正常回退）。计时从 UA 首次尝试使用该 font face 开始。初始值 `auto`，Baseline widely available since **January 2020**。
- **五档语义（MDN 逐条）**：

  | 值 | block period | swap period | 行为 |
  |---|---|---|---|
  | `auto` | UA 决定 | UA 决定 | 默认，通常等同 `block`，**别依赖** |
  | `block` | 短 | 无限 | 先隐身再换，长文风险最高 |
  | `swap` | 极短 | 无限 | 立刻显示 fallback，加载完再换（FOUT + 潜在 CLS） |
  | `fallback` | 极短 | 短 | 短窗口内换，超时就永久用 fallback |
  | `optional` | 极短 | 无 | 首屏慢就干脆不换，**CLS 最优、品牌一致性最差** |

- **裁决**：品牌展示页/标题字重极自定义 → `swap` + §15 度量对齐（把 CLS 压住）；正文/长文/弱网 → `optional` 或 `fallback`（可读性优先于字体一致性）；**禁止 `block` 用在正文**；`auto` 不写进规范（UA 差异不可验收）。
- **与性能预算的界线**：`performance-design.md` 已给 `font-display` 五档与 WOFF2/CJK 子集化，本文件补的是**「为什么这么选」与三阶段术语**；LCP/CLS 阈值与预算表仍以 `performance-design.md` 与 `color-science.md` 的既有口径为准，不在此重复声明数值。
- **验收**：`preload` 只对**首屏必然用到**的字体片生效；预加载了没用的片会浪费带宽。弱网降级见 `performance-design.md` 的 `prefers-reduced-data` / `Save-Data` 三层。

---

## 15 · size-adjust / font-size-adjust 度量对齐（FOUT 不跳版）

FOUT 的 CLS 根因不是「换字体」，是**两款字体的度量不同**；把度量对齐后，`swap` 才能既保品牌又保布局稳定，这是可访问性与验收里最划算的一处工程修复。

- **`@font-face size-adjust`**：初始值 `100%`；按百分比缩放该 font face 的 **glyph outlines、advances、baseline tables** 等度量，使自定义字体与 fallback 的视觉尺寸/字宽对齐。它改的是「这款字体怎么被度量」，不是「元素字号」。
- **`font-size-adjust`**：公式 `u = (m / m′) s`（`s` 为指定字号、`m` 为首选字体的度量、`m′` 为实际字体的度量、`u` 为调整后字号）；支持 `ex-height` / `cap-height` / `ch-width` / `ic-width` / `ic-height` / `from-font`。用途是让 **fallback 字体保持与首选字体相同的 x-height**，避免换字体时小字突然变小/变大。
- **两者区别**：`size-adjust` 在 `@font-face` 里、作用于被定义的自定义字体；`font-size-adjust` 在元素上、作用于**任何**实际渲染字体的字号计算。常见组合是 `size-adjust` 调自定义字体 + `font-size-adjust` 保 x-height。
- **可验收做法**：在同一段测试文字上分别渲染「仅 fallback」与「自定义字体」，用 `getBoundingClientRect()` 量行盒高度与文本宽度，反复调 `size-adjust` 直到差值接近 0；CLS 用 `PerformanceObserver` 的 `layout-shift` 条目实测，**不要凭目测宣布通过**。
- **注意**：`size-adjust` 只调度量不调字面造型，x-height 差异大的两款字体仍可能有视觉跳变；必要时换一款与品牌字体度量接近的 fallback（见 `system-fonts/modern-font-stacks`，CC0-1.0，GitHub API 实测 3540★）。

---

## 16 · 中文排版（W3C clreq 原文核验）

中文排版的区域/locale 差异大于简繁差异；把视觉排版需求写进文本存储层、或按码位处理光标，都会在 CJK 与 emoji 场景下出错。以下四条均取自 W3C《Requirements for Chinese Text Layout》原文。

1. **汉字与西文/阿拉伯数字间的空白（§2.1.3）**：原文 *"Use a spacing of **no more than one-quarter of the width of a Han character** between Han characters and Western letters or European numerals. However, when the Western text appears at the beginning or end of a line, **no extra spacing is required**."* → 是**上限**不是固定值，行首/行尾不加。落地用 CSS `margin`/`text-spacing` 或排版引擎，**不要手敲空格到文本里**（会把视觉需求写进内容层）。
2. **汉字与标点 1:1 正方形（§1.2）**：*"In principle, the characters, including Han characters (Hanzi) and punctuation, used in Chinese composition are **squares with the ratio of 1:1**, and are seamlessly arranged with one another."* §2.1.1 Note 补充 `square character frame`，直横排可共用活字、部分标点需按书写方向调整分布。→ 中文栅格与行高按方框推，别套拉丁 baseline 习惯。
3. **不要把视觉需求写进文本层（§4.1 Note）**：*"Nowadays, when storing text, **avoid using** [fullwidth ASCII] Latin letters and European numerals; leave proportional/monospace display requirements to the typesetting engine."* 同段还纠正「半角/全角」是**度量宽度的概念**，现代西文字体多为比例字体，把 ASCII 一概称「半角」并不准确。→ 数据库存标准 ASCII，显示交给 CSS。
4. **光标/删除/选择按字素丛（§4.2.1）**：*"Cursor movement, deletion, and selection should operate on **grapheme cluster boundaries** rather than on code point or code unit boundaries. A caret should never be placed inside a grapheme cluster, and the Backspace and Delete keys should remove the whole cluster."* 边界由 **UAX #29** 定义，组合附加符号、变体选择符、ZWJ emoji 序列都算一个字素丛。→ 输入框、富文本、字符计数都要用 `Intl.Segmenter`（见 `i18n-localization.md`），不能用 `str.length`。
- **未证实，不写入硬规范**：本次抓取片段**未**证实「标点挤压」「避头尾（禁则处理）」「中文必须用着重号代替 italic/bold」的具体规则数值，因此本文件只作定性提醒、不给数值与「必须」。需要时另查 clreq 相应章节原文。

---

## 17 · M3 type scale 与 token 化（可复现，不抄二手数值表）

M3 提供的是**角色结构 + 行高比率 + 命名约定**，不是一张可以照抄的 15 行数值表；把它落成 token 时，角色与比率可复现，精确数值必须回官方动态页或源码复核。

- **五角色 × 三尺寸（官方已核验）**：`applying-type` 原文——*"The Material 3 type scale organizes styles into **five roles** that are named to describe their purposes: **display, headline, title, label, body**. Each role has **three sizes: large, medium, and small**."* → 15 个 baseline styles。官方 2025-05 起另有 emphasized 变体，使总数成为 30（15 baseline + 15 emphasized）；2026-08 更新支持按 language script height category 自动适配 line height。**取源限制**：官方 `overview` / `type-scale-tokens` 为动态渲染页，本机未能取得完整 15 行 `size / line-height / weight / tracking` 字面表，故**不在此伪造数值**；上线前以官方页面或 `material-web` token 源码为准。
- **角色语义（官方）**：display 保留给短而重要的文字/数字、适合大屏、可用表现性字体并设 optical size；headline 适合小屏短高强调文本；title 中等强调、较短、**慎用**表现性字体；body 用于长段落、**禁**装饰字体；label 用于组件内文字与 caption（按钮用 label large）。
- **行高比率（官方）**：大字号（title/headline/display）≈ `1.2×`，小正文/标签 ≈ `1.5×`（见 §5）。
- **数字与链接（官方）**：表格/时钟/频繁变化值用 tabular figures；大文本 3:1 / 小文本 4.5:1；**超链接必须加下划线**（见 §6 §10）。
- **Web 的排版盒模型（官方）**：*"In web UIs, the line height and bounding box height are the same. Text is vertically centered within the bounding box, following the **half-leading** behavior established by CSS."* → Web 用 `line-height + padding + 容器测量`；Android 用 baseline；两套标法不能混写进同一份 spec（与 `handoff-collaboration.md` 的标注纪律一致）。
- **token 命名（material-web）**：ref 层 `--md-ref-typeface-brand` / `--md-ref-typeface-plain`；sys 层 `--md-sys-typescale-<scale>-<size>-<property>`，`property` 含 `font` / `size` / `line-height` / `weight`。→ 自建 token 时也分 ref（字体族）/ sys（角色×尺寸×属性）两层，落 DTCG 格式（见 `design-tokens.md`）。
- **token 化四步**：定角色 → 每角色定 3 尺寸 → 每档写 `size`（rem）/ `line-height`（比率）/ `weight` / `tracking` → 映射到 semantic token，**组件只引用 semantic**。改品牌字体只换 ref，不动组件。

---

## 18 · 字体授权（OFL 1.1）：能做与不能做

授权不合规会让整个产品无法分发；这一层先于审美，且**逐字体**检查而不是看仓库级 license。以下取自 SIL OFL 1.1 官方英文原文（Preamble + PERMISSION & CONDITIONS 五条件）。

**可以做**：`use, study, copy, merge, embed, modify, redistribute, and sell modified and unmodified copies of the Font Software`——即随软件打包、嵌入网页/App、修改字形、再分发、随软件销售。

**五条硬条件**：

1. **不可单独售卖**：*"Neither the Font Software nor any of its individual components, in Original or Modified Versions, may be sold **by itself**."* → 可以随软件卖，不能开一个「字体包」单独标价。
2. **随软件分发必须带版权声明与 license**：*"each copy contains the above copyright notice and this license"*，可以是独立文本文件、可读 header 或**易被用户查看的机器可读 metadata 字段**。Web 字体打包常漏这条。
3. **Reserved Font Name（RFN）**：Modified Version 不得使用 RFN，除非对应版权持有人书面许可；此限制**只作用于呈现给用户的主字体名**。
4. **不得借原作者/版权持有人名义宣传、背书或广告** Modified Version（致谢贡献除外，或需书面许可）。
5. **衍生字体必须继续 OFL**：*"must be distributed entirely under this license, and must not be distributed under any other license"*；Preamble 亦写明 *"The fonts and derivatives, however, cannot be released under any other type of license."*

**两条关键澄清**：

- **文档不受字体 license 约束**：条件 5 与 Preamble 均明确 *"The requirement for fonts to remain under this license does not apply to any document created using the Font Software"*。→ 用 OFL 字体做的海报、PDF、网页设计稿，其版权归设计者，不被 OFL 传染。
- **TERMINATION 条款**：任一条件不满足，授权即 `null and void`。所以「先上线后补 license 文件」在法律上等于从未获得授权。

**许可核查三问**：① 许可文件在哪（字体目录 / 仓库根 / 字体 metadata）？② 是否允许 web embedding 与 self-host？③ 有没有 RFN、我们是否改名？另：`rsms/inter` 的 GitHub API 实测为 **OFL-1.1**；`google/fonts`、`adobe-fonts/source-han-sans`、`notofonts/noto-cjk`、`unicode-org/icu` 返回 `NOASSERTION`（混合许可），必须逐字体目录读 `OFL.txt`，**不能凭仓库级字段下结论**。

---

## 19 · 工具链与 GitHub API 实测数据（2026-11-07）

凡涉及 star / 许可 / 更新时间一律用 GitHub REST API 实测，不凭记忆写数字；`NOASSERTION` 不等于「无许可」，只代表 API 未自动识别，需进仓库读许可文件。

| 仓库 | ★ | license (API) | pushed_at | 用途 |
|---|---|---|---|---|
| `google/fonts` | 20,734 | `NOASSERTION`（混合，逐字体 OFL） | 2026-11-07 | Google Fonts 源、CJK 分片参考 |
| `rsms/inter` | 20,043 | `OFL-1.1` | 2024-11-19 | UI 无衬线、可变字体、tabular 特性齐 |
| `adobe-fonts/source-han-sans` | 17,450 | `NOASSERTION` | 2025-06-25 | 思源黑体 / 泛 CJK 子集 |
| `notofonts/noto-cjk` | 4,142 | `NOASSERTION` | 2025-12-16 | Noto CJK 语言子集与字形差异 |
| `opentypejs/opentype.js` | 5,043 | `MIT` | 2026-08-08 | 浏览器/Node 读字体表、检查轴与 glyph 覆盖 |
| `fonttools/fonttools` | 5,311 | `MIT` | 2026-11-05 | `pyftsubset` 子集化、改名、度量检查 |
| `system-fonts/modern-font-stacks` | 3,540 | `CC0-1.0` | 2026-03-10 | 系统字体回退链（度量接近的 fallback 首选） |
| `googlefonts/fontations` | 854 | `Apache-2.0` | 2026-11-06 | Rust 字体解析（工具链活源） |
| `unicode-org/icu` | 3,637 | `NOASSERTION` | 2026-11-07 | UAX #29 字素丛 / 断行 / 区域数据 |

**选型三问（沿用本技能既有纪律）**：许可（是否允许 self-host / 商业分发 / 改名）→ 活源（`pushed_at` >12 个月不进生产依赖）→ 可验收（能否跑出覆盖率/体积/度量的可复现数字）。`rsms/inter` 推送停在 2024-11，属「成熟稳定但非活跃迭代」，用它可以，但要固定版本、自己盯上游，不把它当持续更新的活源。

**工具用途对齐**：`pyftsubset` 出 `unicode-range` 分片 + WOFF2；`opentype.js` 验可变轴与 `tnum`/`lnum` 等 feature tag 是否真的存在于字体里（**字体没有 `tnum` 表时写 CSS 也不会生效**）；`Intl.Segmenter` 验字素丛；`PerformanceObserver` 验 CLS；`getBoundingClientRect()` 验度量对齐。

---

## 20 · 场景速查（12）

| # | 场景 | 直接动作 | 依据 |
|---|---|---|---|
| 1 | 从零定一套正文字号 | `rem` 阶梯 0.75/0.875/1/1.25/1.5/2/3，正文 ≥1rem，标题比率 1.2 / 正文 1.5 | §4 §5 §17 |
| 2 | 用户说「字太小 / 要长辈版」 | 先查是不是 px 锁死；改 rem + 去固定高度 + 跑 200% 缩放 | §4 §8；`accessibility.md §16` |
| 3 | 卡片/按钮在间距覆盖下裁切 | 去 `height`，`min-height`+`padding`，允许换行，勿用 `!important` 顶回覆盖 | §7 |
| 4 | 表格数字左右跳 / 倒计时抖动 | `font-variant-numeric: lining-nums tabular-nums` | §10 |
| 5 | 中文正文密得喘不过气 | 行高 ≥1.6、行长 CJK ≤40 字、禁 justify、段距 ≥2× | §5 §6 §16 |
| 6 | 中英混排哪里加空格 | 视觉空白 ≤1/4 汉字宽、行首行尾不加；用 CSS 不手敲进文本 | §16 |
| 7 | 首屏字体加载白字或跳动 | 选 `swap`/`optional`，配 `size-adjust` 度量对齐，实测 CLS | §14 §15 |
| 8 | CJK 站点字体几个 MB | `unicode-range` 高频字集分片 + WOFF2 + `pyftsubset` | §13 |
| 9 | 想用可变字体做 hover 加粗但不跳版 | 优先高层属性；有 `GRAD` 轴且不改 advance 才用它 | §9 |
| 10 | 品牌字体要自托管分发 | 逐字体查 license + 版权声明 + RFN；OFL 衍生必须仍 OFL | §18 |
| 11 | 设计稿交给开发对齐不上 | Web 用 `line-height`+padding+盒模型（half-leading），别混 Android baseline 标法 | §17 |
| 12 | 不确定该查哪份文件 | `python scripts/dp_search.py "字体 行高 可访问性"`；风格侧查 `visual-style-taxonomy.md`，性能侧查 `performance-design.md` | §2 |

---

## 21 · 反模式（20）

1. 正文 `font-size: 14px` 写死 → 用户改不了默认字号，MDN 判为 not accessible（§4）。
2. 全站 `em` 嵌套做字号 → compounding 让内层字号失控（MDN 实测 40.96px）（§4）。
3. 把 WCAG 1.4.12 四项当成作者默认样式照抄 → 条文 Note 1 明确不要求，验收方向搞反（§6）。
4. 用 `!important` 把作者 `line-height` 顶在用户覆盖之上 → 正是条文禁止的「干扰用户覆盖」（§7）。
5. 承载文字的按钮写死 `height` → 200% 缩放与间距覆盖双爆（§8）。
6. 动态文案上 `white-space: nowrap` → 翻译膨胀 + 缩放叠乘后必裁切（§8 `i18n-localization.md`）。
7. 长文 `text-align: justify` → 1.4.8 明令 `Text is not justified`（§5 §6）。
8. 正文栏宽 100ch 且不分栏 → 超 80 字符（CJK 40）门槛（§5 §6）。
9. 大标题沿用正文 1.5 行高 → M3 大字号应约 1.2×，标题松散不成组（§5 §17）。
10. 表格用 `font-family: monospace` 代替 `tabular-nums` → 字母也被等宽化，是排版降级（§10）。
11. 全局开 `tnum`、组件里又写 `font-feature-settings: "pnum"` → 低位覆盖高位，静默失效（§11）。
12. 用 `font-feature-settings: "smcp"` 做小型大写 → MDN 明确不应这么做，走 `font-variant-caps`（§11）。
13. `font-family: "sans-serif"` 加引号 → 变成字体名，失去通用族兜底（§12）。
14. 回退链里把 CJK 字体放西文前面 → 中文正文的拉丁字符被中文字体自带字形接管（§12）。
15. `system-ui` 用作大段正文字体 → 跨平台 x-height 与行高不可控（§12）。
16. `unicode-range` 切一大片 CJK 全字集还以为优化过 → 命中一个字就整片下载（§13）。
17. 正文 `@font-face` 用 `font-display: block` → 长 FOIT，弱网等于空白页（§14）。
18. 写了 `swap` 却不调 `size-adjust` → FOUT 换字体时行盒变化，CLS 依然高（§15）。
19. 往数据库里存全角 ＡＢＣ１２３ 追求「对齐」 → clreq §4.1 明确文本存储应避免（§16）。
20. 用 `str.length` 做中文/emoji 字符计数与截断 → 应按 UAX #29 字素丛（§16 `i18n-localization.md`）。

---

## 22 · 自检（20）

- [ ] 正文字号是 `rem` 而非 `px`，且能说清 MDN「Defining font sizes in px is not accessible」的理由？
- [ ] 全局没有 `em` 嵌套做字号（只用于有意跟随当前字号的间距）？
- [ ] 跑过 200% **仅文字缩放**与**整页缩放**两种测试，表单、按钮、卡片都没裁切/重叠？
- [ ] 注入 1.4.12 四项（且未改其他属性）后无内容或功能丢失，固定高度容器全部换成了 `min-height`+`padding`？
- [ ] 知道 1.4.12 是「用户覆盖抗压」而非「作者默认样式」，能引用 Note 1？
- [ ] 正文行宽 ≤80 字符（CJK ≤40）、`text-align` 不是 `justify`、段间距 ≥1.5× 行距？
- [ ] 大标题行高约 1.2×、正文/标签约 1.5×，两档分别落在 token 里？
- [ ] 文本对比度按大文本 3:1 / 小文本 4.5:1 重算过（改字号后没忘记重判「大文本」）？
- [ ] 超链接在正文里除了颜色还带下划线？
- [ ] 表格/时钟/金额/实时数值开了 `tabular-nums`，ID/验证码开了 `slashed-zero`，且确认字体真有 `tnum` 表？
- [ ] 用 `font-variant-*` 而非 `font-feature-settings`，后者只用于字体独有 custom feature 且带注释？
- [ ] `font-family` 链顺序正确（西文 → CJK → 系统 → generic），generic 放最后且**未加引号**？
- [ ] 拿含中文/西文/全角/货币/emoji/生僻字的测试串验过无 tofu、无跨字体混排不齐？
- [ ] `unicode-range` 按高频字集分片，每片都写了同一个 `font-display`？
- [ ] `font-display` 按场景选（正文不 `block`、不依赖 `auto`），并用 `PerformanceObserver` 实测过 CLS？
- [ ] 用 `size-adjust` / `font-size-adjust` 对齐过 fallback 度量，用 `getBoundingClientRect()` 量过行盒差？
- [ ] 中文与西文间空白 ≤1/4 汉字宽、行首行尾不加、由 CSS 而非手敲空格实现？
- [ ] 文本存储层没有全角 ASCII；光标/删除/计数按字素丛（`Intl.Segmenter` / UAX #29）？
- [ ] M3 五角色×三尺寸的 role/size/line-height/weight 已落 token，且**没有**抄未经官方核验的 15 行精确数值？
- [ ] 逐字体查过 license（非仅仓库级）、带了版权声明与 license 文件、确认 RFN 与 self-host 权限？

---

## 23 · 可抄代码（6 段）

### 23.1 CSS · rem 字号阶梯与两档行高（可抄）

```css
:root {
  /* 字号阶梯：以用户默认字号为基准，绝不写死 px */
  --type-size-xs:   0.75rem;   /* 12 */
  --type-size-sm:   0.875rem;  /* 14 */
  --type-size-md:   1rem;      /* 16 正文起点 */
  --type-size-lg:   1.25rem;   /* 20 */
  --type-size-xl:   1.5rem;    /* 24 */
  --type-size-2xl:  2rem;      /* 32 */
  --type-size-3xl:  3rem;      /* 48 */

  /* 行高两档（M3 applying-type）：大字号 1.2，小正文/标签 1.5 */
  --type-leading-display: 1.2;
  --type-leading-body:    1.55;

  /* 段距按 1.4.12 抗压门槛取 2× font size */
  --type-paragraph-gap: 2em;
}

body {
  font-family: "Inter", "Noto Sans SC", system-ui, sans-serif; /* generic 不加引号 */
  font-size: var(--type-size-md);
  line-height: var(--type-leading-body);
  /* 不写 height，让 200% 缩放与间距覆盖都能撑开 */
}

h1, h2, h3 { line-height: var(--type-leading-display); }
p { margin-block-end: var(--type-paragraph-gap); }

/* 承载文字的按钮：min-height + padding，不写死 height */
.button {
  min-height: 2.75em;
  padding: 0.5em 1em;
  font-size: var(--type-size-md);
  white-space: normal;          /* 动态文案允许换行 */
}

/* 表格 / 时钟 / 金额 / 实时数值 */
.table td.num, .timer, .price {
  font-variant-numeric: lining-nums tabular-nums;
}
.id-code {
  font-variant-numeric: lining-nums tabular-nums slashed-zero;
}
```

### 23.2 CSS · @font-face 三件套（font-display / unicode-range / size-adjust）

```css
/* 高频汉字片：命中一个字即整片下载，故第一片只放最常用字 */
@font-face {
  font-family: "Brand Sans SC";
  src: url("/fonts/brand-sc-common.woff2") format("woff2");
  font-style: normal;
  font-weight: 100 900;        /* 可变字体用范围，不逐字重出文件 */
  font-display: swap;          /* 正文/品牌展示：立刻可见 + 度量对齐压 CLS */
  size-adjust: 102%;           /* 与 fallback 度量对齐，实测后调，不是拍脑袋 */
  unicode-range: U+4E00-4EFF, U+3000-303F, U+FF00-FFEF;
}
@font-face {
  font-family: "Brand Sans SC";
  src: url("/fonts/brand-sc-ext.woff2") format("woff2");
  font-style: normal;
  font-weight: 100 900;
  font-display: swap;          /* 每片同一个值，否则半页换字体半页没换 */
  size-adjust: 102%;
  unicode-range: U+3400-4DBF, U+20000-2A6DF;
}

/* fallback 侧保 x-height，避免换字体瞬间小字突然变小 */
body { font-size-adjust: from-font; }

/* 弱网/长文可选：干脆不换字体，CLS 最优 */
@media (prefers-reduced-data: reduce) {
  /* 由服务端或构建期切换到 font-display: optional 的样式表 */
}
```

### 23.3 CSS · WCAG 2.2 SC 1.4.12 文本间距覆盖验收书签

```css
/* 用法：注入 bookmarklet / DevTools，只改这四项，不改其他 style property。
   条文：line-height ≥1.5×、段后距 ≥2×、letter-spacing ≥0.12×、word-spacing ≥0.16×
   （均相对 font size，故此处用 em）。验收：无裁切、无重叠、无功能丢失。 */
html body * {
  line-height: 1.5 !important;
  letter-spacing: 0.12em !important;
  word-spacing: 0.16em !important;
}
html body p {
  margin-block-end: 2em !important;
}

/* 注入后重点看：固定 height 的按钮/badge、ellipsis 表格单元、
   absolute 定位角标、表单 label 与错误提示、长 URL/代码是否触发横向滚动。
   注意：这是「验收工具」，不是产品默认样式；不要把它合进生产 CSS。 */
```

### 23.4 CSS · 可变字体：高层属性优先 + custom 轴兜底

```css
.headline {
  /* 能用高层属性就别碰 font-variation-settings */
  font-weight: 700;
  font-stretch: 100%;          /* wdth */
  font-style: italic;          /* ital / slnt 由字体决定 */
  font-optical-sizing: auto;   /* opsz：M3 明确 display 要设合适的 optical size */
}

/* 只有字体独有的 custom axis（大写 4 字符 tag）才用低位 API，并写清理由 */
.headline:hover {
  /* GRAD：改笔画密度但不改 advance，hover 时不会触发 reflow / CLS；
     使用前须用 opentype.js 确认该字体确实带 GRAD 轴。 */
  font-variation-settings: "GRAD" 60;
}

/* 反例（不要写）：
   font-feature-settings: "smcp";      -> 应走 font-variant-caps: all-small-caps
   font-variation-settings: "wght" 700; -> 应走 font-weight: 700
*/
```

### 23.5 Python · 排印静态扫描 lint（含自测用例）

```python
"""扫描 CSS/组件源码里的排印可访问性反模式。
用法: python typography_lint.py <file_or_dir>
规则: px 字号 / 固定 height 承载文字 / justify / 引号 generic / 低位 API 滥用
"""
import re, sys
from pathlib import Path

RULES = [
    # (id, 正则, 说明)
    ("PX_FONT_SIZE",   re.compile(r"font-size\s*:\s*\d+(\.\d+)?px", re.I),
     "正文用 px 锁死用户字号设置（MDN: not accessible）→ 改 rem"),
    ("FIXED_HEIGHT",   re.compile(r"(?:^|[;{])\s*height\s*:\s*\d+(\.\d+)?(?:px|rem|em)", re.I | re.M),
     "承载文字的元素写死 height → 200% 缩放 / 1.4.12 覆盖会裁切，改 min-height+padding"),
    ("JUSTIFY",        re.compile(r"text-align\s*:\s*justify", re.I),
     "WCAG 2.2 SC 1.4.8 要求 Text is not justified"),
    ("QUOTED_GENERIC", re.compile(r'font-family\s*:[^;]*["\'](?:sans-serif|serif|monospace)["\']', re.I),
     "generic family 加引号会变成字体名，失去兜底"),
    ("SMCP_LOWLEVEL",  re.compile(r'font-feature-settings\s*:[^;]*["\']smcp["\']', re.I),
     "MDN: 不应使用 font-feature-settings 启用 small caps → 走 font-variant-caps"),
    ("NOWRAP_DYNAMIC", re.compile(r"white-space\s*:\s*nowrap", re.I),
     "动态文案/翻译串禁 nowrap（文案膨胀 × 200% 缩放叠乘必裁切）"),
]

def lint(text: str):
    return [(rid, why) for rid, rx, why in RULES if rx.search(text)]

if __name__ == "__main__":
    bad = """ .btn { font-size: 14px; height: 40px; white-space: nowrap; }
              p { text-align: justify; }
              .x { font-family: "sans-serif"; font-feature-settings: "smcp"; } """
    good = """ .btn { font-size: 1rem; min-height: 2.75em; padding: .5em 1em; white-space: normal; }
               p { text-align: start; }
               .x { font-family: "Inter", system-ui, sans-serif; font-variant-caps: all-small-caps; }
               .num { font-variant-numeric: lining-nums tabular-nums; } """
    hits_bad = {r[0] for r in lint(bad)}
    hits_good = {r[0] for r in lint(good)}
    expected = {"PX_FONT_SIZE", "FIXED_HEIGHT", "JUSTIFY", "QUOTED_GENERIC", "SMCP_LOWLEVEL", "NOWRAP_DYNAMIC"}
    assert hits_bad == expected, f"漏报/误报: {hits_bad}"
    assert not hits_good, f"合规样例被误报: {hits_good}"
    print(f"self-test PASS: 6/6 反模式命中，合规样例 0 误报")
    for arg in sys.argv[1:]:
        p = Path(arg)
        files = [p] if p.is_file() else list(p.rglob("*.css")) + list(p.rglob("*.tsx"))
        for f in files:
            for rid, why in lint(f.read_text(encoding="utf-8", errors="ignore")):
                print(f"{f}:{rid}: {why}")
```

### 23.6 CSS · 中文混排与字素丛友好的输入层

```css
/* 中英空白：clreq §2.1.3 —— 不多于 1/4 汉字宽，行首/行尾无空白。
   交给排版层，不往文本里手敲空格；数据库只存标准 ASCII（§4.1）。 */
.prose { text-spacing: normal; overflow-wrap: anywhere; }
.prose :is(h1, h2, h3) { line-height: 1.35; }   /* 中文标题按 1:1 方框略放宽 */

/* 长 URL / 代码 / 长姓名：允许换行，避免 1.4.8 的横向滚动 */
.prose a, .prose code { overflow-wrap: anywhere; }

/* 表单：label / 帮助 / 错误三层都不写死高度，间距覆盖时不重叠 */
.field label { display: block; margin-block-end: 0.375em; }
.field .hint, .field .error { display: block; line-height: 1.5; }
.field input { min-height: 2.75em; padding: 0.5em 0.75em; font-size: 1rem; }
```

```js
// 字符计数/截断按 UAX #29 字素丛（clreq §4.2.1），不用 str.length
const segments = [...new Intl.Segmenter("zh", { granularity: "grapheme" }).segment(text)];
const count = segments.length;              // emoji / 组合符 / 变体选择符算 1 个
const limited = segments.slice(0, max).map(s => s.segment).join("");
```

---

## 24 · 取源与限制（公开记录）

- **已逐条联网核验（官方原文）**：W3C WCAG 2.2 Understanding SC 1.4.12（四项数值、Exception、Note 1/2、Applicability、Author/User Responsibility）；MDN `font-size`（相对单位建议、px not accessible、em compounding 25.6/40.96px、rem 消除 compounding）；MDN `font-display`（五档、三阶段、初始 `auto`、Baseline 2020-01）；MDN `unicode-range`（「至少一个字符即整片下载」、三种语法、初始 `U+0-10FFFF`、Baseline 2015-07）；MDN `font-variant-numeric`（8 个值 ↔ tag 全表）；MDN `font-feature-settings`（高层优先、4 字符 ASCII tag、on/off=1/0、省略默认 1、small caps 禁用）；M3 `applying-type`（五角色×三尺寸、1.2×/1.5× 行高比率、tabular figures、3:1 / 4.5:1、链接必须下划线、half-leading）；W3C clreq（§2.1.3 不多于 1/4 汉字宽与行首行尾例外、§1.2 1:1 正方形、§4.1 全角 ASCII 与半角术语、§4.2.1 字素丛与 UAX #29）；SIL OFL 1.1 官方英文原文（Preamble + 五条件 + TERMINATION + 文档不受约束）。
- **GitHub REST API 实测（2026-11-07，未认证读取 200）**：§19 表格九个仓库的 star / `license.spdx_id` / `pushed_at` / `archived` 均为当次实测；`NOASSERTION` 按「API 未自动识别」如实记录，未推断具体许可。`modernfontstacks/modern-font-stacks` 返回 404，已剔除，不写入。
- **未取得、因此不臆造**：
  - **M3 15 档 type scale 的精确 `size / line-height / weight / tracking` 表**——官方 `overview` / `type-scale-tokens` 为动态渲染页，`material-web` 的 `_md-sys-typescale.scss` 未含可直接引用的字面数值表。本文件只写「五角色×三尺寸」「30 = 15 baseline + 15 emphasized（2025-05 起）」「2026-08 language script height category」「行高比率」「token 命名」，**不给伪造数值**；上线前以官方页面或 `material-web` token 源码为准。
  - clreq 的「标点挤压」「避头尾（禁则处理）」「中文强调须用着重号替代 italic/bold」——本次抓取片段未证实，**只作定性提醒不写规范与数值**。
  - 各字体的实际子集体积、`size-adjust` 的具体百分比、CLS 实测值——必须针对自己的字体与页面实测（§15 §19 给了方法），不照抄任何二手数字。
  - iOS Safari `<16px` 自动缩放等中文社区/二手说法未作为硬规范依据，只作线索，不写入。
- **口径纪律**：`size-adjust` 百分比、`font-size-adjust` 公式 `u=(m/m′)s`、五个注册轴、`material-web` token 命名、M3 30 styles 与 language script height category 来自官方页面/规范但本轮未逐条重取动态页原文，标注为「以官方为准」；凡标「以官方为准」的数值不臆造逐字与精确版本号。`NOASSERTION` ≠ 无许可；1.4.12 ≠ 默认样式表；`optional` ≠ 一定不下载，只是不 swap。

---

**判学会了**：能解释为什么正文不能用 px、能当场注入 1.4.12 四项并指出哪个容器会塌、能说清 `font-family` 逐字符回退与 `unicode-range` 整片下载的关系、能用 `tabular-nums` 修掉表格抖动而不换成等宽字体、能判断一款字体能不能自托管分发 → 见 `typography-system.md` 全文与 §22 的 20 项自检。
