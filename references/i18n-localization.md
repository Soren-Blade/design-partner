# 国际化与本地化设计（i18n / L10n / RTL / 多语言）

> 快照 2026-11-05 · 全部数值来自 W3C / WAI / Unicode CLDR / ICU / MDN / Material / Microsoft 官方原文，或 Node v22.22.2 `Intl` API 本机实测；二手总结一律不采信。
>
> **与 `ux-writing.md` §13 的分工**：§13 是「写文案时别踩坑」的 5 条速记；本文件是**工程实现层与验收层**——布局弹性怎么算、`dir` 怎么标、复数怎么分支、`Intl` 怎么调、伪本地化怎么测、上线前查什么。两者不重复，冲突处以本文件为准（见 §2.3 对「+40%」的裁决）。
>
> **本文件回答的核心问题**：一个中文/英文界面要出海，到底要改什么？答案是三层——**标记层**（`lang`/`dir`）、**布局层**（弹性 + 逻辑属性 + 镜像）、**数据层**（复数/日期/数字/姓名/排序）。只换翻译文本 = 三层全漏。

---

## 一、判层：国际化与本地化 i18n / L10n / 翻译 / 多语言 / RTL 不是同一件事

先分层，否则会把「加个语言包」当成全部工作。

| 层 | 定义 | 谁负责 | 典型失败 |
|---|---|---|---|
| **i18n（国际化）** | 让产品**具备**承载多语言/多地区的能力，与具体语言无关 | 设计 + 前端架构 | 字符串写死在组件里、`width` 写死、图标带文字、`left` 写死 |
| **L10n（本地化）** | 针对某个 locale 做**适配**：文案、日期、货币、图像、合规 | 译员 + 本地团队 | 只翻了文字，日期还是 `03/09/2026` |
| **Translation（翻译）** | L10n 的子集，仅文本转换 | 译员 | 逐句翻、变量被拆开、语气不统一 |
| **RTL / 双向文本** | 阿拉伯语、希伯来语等从右到左书写的**方向性**适配 | 设计 + 前端 | 只做了文本右对齐，图标、进度条、导航没镜像 |
| **locale ≠ language** | `en-US` / `en-GB` 是同一语言不同 locale；`zh-Hans` / `zh-Hant` 是同一语言不同脚本 | 架构 | 用 `lang` 推断地区、用语言推断方向 |

**三条立场**：

1. **i18n 是架构决策，不是上线前的一道工序。** 需要改组件 API 的事（字符串外置、逻辑属性、变量化文案）在画第一张稿时就要定；等翻译回来再改，成本是重做。
2. **「多语言」不等于「RTL」。** 中→英是双向 LTR，不需要镜像；中→阿才需要。别为了「以后可能出海」提前给全站加 RTL 分支，但**逻辑属性应当默认写**（见 §4），因为它零成本。
3. **locale 必须完整传递，不能只传语言。** 实测：`Intl.DateTimeFormat('en-US')` → `Monday, March 9, 2026`，`en-GB` → `Monday, 9 March 2026`；同一 `en` 不同 region 输出不同。只存 `lang='en'` 会丢掉这层。

### 1.1 什么时候要读本文件

| 信号 | 去哪一节 |
|---|---|
| 「按钮翻译后文字放不下 / 换行 / 截断」 | §2 |
| 「多语言页面要不要写 lang」「读屏念得不对」 | §3、§20 |
| 「阿拉伯语布局怎么翻」「箭头要不要反」 | §4、§5 |
| 「1 条 / 2 条 / 0 条消息怎么翻」 | §6、§7 |
| 「日期、货币、千分位怎么显示」 | §9、§10 |
| 「姓名表单要不要分姓和名」 | §12 |
| 「怎么在没翻译前先测出 bug」 | §14 |
| 「出海验收清单」 | §18、§19、§20 |

---

## 二、文案膨胀 text expansion：翻译后文字变长、按钮放不下，+40% 不是安全值

**本轮最重要的一条修正。** 现有 `ux-writing.md` §13 写「按钮和标签必须能容纳 **+40%** 的文字长度」，Microsoft 伪本地化也给「+40%」启发式——但对**短字符串**而言这是错的，而且错得刚好落在按钮、标签、tab 这些最容易出事的地方。

### 2.1 W3C / IBM 官方膨胀表（逐字取，不要自行「修正」）

W3C《Text size in translation》转引 IBM《Guidelines to design global solutions》，给出英译欧洲语言的**平均预期膨胀率**：

| 英文源字符数 | 平均膨胀 | 换算后长度系数 |
|---|---|---|
| **≤ 10** | **200–300%** | **2.0–3.0×** |
| 11–20 | 180–200% | 1.8–2.0× |
| 21–30 | 160–180% | 1.6–1.8× |
| 31–50 | 140–160% | 1.4–1.6× |
| 51–70 | 151–170% | 1.51–1.70× |
| > 70 | 130% | 1.3× |

> **原文表格在 51–70 档不是单调的**（151–170% 高于 31–50 档的 140–160%）。这是官方原表的样子，本文件照录，不擅自平滑，也不据它编造「规律」。能确定的只有 W3C 自己那句结论：**源消息越短，翻译后长度越可能变长**。

### 2.2 Flickr "views" 实测比例表（W3C 原文）

同一个短词 `views`（Flickr 的「392 views」），翻译成各语言的**长度比**（以英文为 1）：

| 语言 | 译文 | 比例 |
|---|---|---|
| 韩语 | 조회 | 0.8 |
| 英语 | views | 1 |
| 中文 | 次檢視 | 1.2 |
| 葡萄牙语 | visualizações | 2.6 |
| 法语 | consultations | 2.6 |
| 德语 | -mal angesehen | 2.8 |
| 意大利语 | visualizzazioni | **3.0** |

W3C 特别注明：**由于字形宽度，每个中文/韩文字符按 2 个英文字符宽度计**。所以「中文更短」只在字符数层面成立，在物理宽度层面不一定。原文结论：对一个这么小的字符串，英→意 **300%** 膨胀毫不奇怪。

同一篇文章的缩写例子：`FAQ` 在德语、法语里仍是 `FAQ`，但葡萄牙语是 `Perguntas freqüentes`、西语是 `Preguntas frecuentes` —— **缩写是设计给英语用的，不是设计给翻译用的**。

### 2.3 裁决：+40% 用在哪、2–3× 用在哪

三个来源并不矛盾，它们说的是不同长度档：

| 来源 | 数值 | 适用对象 |
|---|---|---|
| W3C / IBM（≤10 字符） | **200–300%** | 按钮、标签、tab、字段名、导航项、徽标——**microcopy** |
| W3C / IBM（>70 字符） | **130%** | 段落、说明、长帮助文本 |
| Microsoft 伪本地化 | **+40% 启发式**；极端 **200% / 400%** | 全局**测试串**的加长量，不是设计余量 |
| `ux-writing.md` §13 | +40% | 应理解为**长文案**的经验值，被误用到了短串 |

**明确立场（本技能的设计规则）**：

- **microcopy（≤10 英文字符 / ≤4 汉字）按 2–3× 宽度设计弹性**，不是 +40%。一个 5 字符英文按钮（`views`）按 +40% 只留 7 字符，装不下 `visualizzazioni`（15 字符）。
- **短文案（11–50 字符）按 1.6–2.0×**；**段落按 1.3×**。
- **不要把余量做成「更宽的按钮」**，而是做成**能伸缩**：`min-inline-size` + `max-inline-size` + 允许换行 / 省略（有 `title` 或 tooltip 兜底）。W3C 原话：*Allow text to reflow and avoid small fixed-width containers or tight squeezes where possible*；并特别警告 *Be especially careful about fitting text snugly into graphic designs*。
- **W3C 指出的双重挤压**：越短的英文文本，膨胀率越高；同时越短的英文文本越容易被塞进小空间（表单字段旁、图形里、定宽 tab 里）。两个效应同向叠加，这是短串翻车的根因。
- **收缩也是问题**：西语 `Idioma de la interfaz` → 英语 `Interface language` 变短、→ 马来语 `Bahasar pegantar untuk penelusuran` 变长；W3C 明确说「更小的译文若留下大片空白，问题不比变长小」。所以弹性是**双向**的，不是「留大一点」。
- **数据库字段宽度同样按字符长度算**，W3C 要求设计 DB 字段时把这套膨胀一起考虑（见 §12「4 字日文名 UTF-8 可能占 12 字节」）。

### 2.4 四类「不只是变长」的复杂因素（W3C 原文）

| 因素 | 官方例子 | 对设计的要求 |
|---|---|---|
| **复合词** | 英语 `Input processing features` 可轻易折成两行；德语 `Eingabeverarbeitungsfunktionen` 是一个词，**不会自动换行** | 定宽容器内必须能处理超长不可断词；`overflow-wrap: break-word` / `hyphens: auto` 要按语言给（德语自动连字符） |
| **字符宽度** | `desktop` → `デスクトップ`：日语**少一个字符**，横向占位却更大 | 不能用字符数估像素；中文/韩文按 2 个英文字符宽计（W3C 口径） |
| **字符与行高** | 泰文同两行但垂直空间显著更大；阿拉伯语（尤其 Nastaliq 字体）、中文、天城文（印地语）、日文、韩文、藏文都需要更高字形与更大行距 | 行高不能写死 px；用无单位倍数并按脚本调；按钮/单元格高度允许增长 |
| **缩写** | 为了塞进小空间而缩写 `FAQ`，翻译时不可复制；阿拉伯语词的词根-前缀-后缀结构很难缩写而不丢意义 | 不要用缩写解决布局问题；若确需缩写，给译员一份**缩写展开表** |

### 2.5 布局弹性清单（可交付给前端）

- [ ] 所有文字容器用 `min-inline-size` / `max-inline-size`，不用固定 `width`；`inline-size: fit-content` + `max-inline-size` 是常用组合。
- [ ] 按钮不设 `white-space: nowrap`（除非同时给省略与 tooltip）；标签允许 2 行。
- [ ] flex/grid 子项 `min-inline-size: 0`（否则长词会撑破轨道，这是 CSS 默认 `min-width: auto` 的经典坑）。
- [ ] 表单标签与输入框**上下排布优先**：左右排布时标签列必然定宽，短串膨胀首先在这里炸。
- [ ] 图标 + 文字不要做成一张位图；文字必须可替换重排。
- [ ] 图片/视频里的文字（banner、引导图、社媒图）单独出可翻译源文件或做文字层（见 §15）。
- [ ] 表格列宽允许按内容重算；表头与单元格都能换行。
- [ ] 数据库 `VARCHAR` 长度按目标语言重新估，全链路 UTF-8。
- [ ] 用 §14 的伪本地化把上述所有点跑一遍，别等到真翻译回来。

---

## 三、lang 与 dir：BCP 47 语言声明、RTL 方向、WCAG 3.1.1 / 3.1.2

标记层是**无障碍硬要求**，不是「锦上添花的语义」。

### 3.1 WCAG 2.2 原文

| 条款 | 级别 | 原文要点 |
|---|---|---|
| **3.1.1 Language of Page** | **Level A** | 「The default human language of each web page can be **programmatically determined**.」 |
| **3.1.2 Language of Parts** | **Level AA** | 「The human language of each **passage or phrase** in the content can be programmatically determined except for proper names, technical terms, words of indeterminate language, and words or phrases that have become part of the vernacular of the immediately surrounding text.」 |

- 3.1.1 的充分技术 **H57**：在 **HTML 元素**上使用语言属性。WAI 明确：页面多语言时，默认语言取**用得最多的那种**；若几种用得一样多，取**最先出现的**那种。
- 3.1.2 的充分技术 **H58**：用 `lang` 标出语言变化，例如 `It can be a <span lang="fr">faux pas</span> ...`。WAI 明确 **passage/phrase = 一个或多个词**，因此**单个词也可能受约束**（例外见上表）；有疑问时看该词在周围语言里发音是否基本相同。
- WAI 特别注明：面向 Level A 的多语言站点，工作组**强烈建议**也遵循 3.1.2（虽然是 AA）。
- 作用：读屏加载正确的发音规则、浏览器正确显示字形、媒体播放器正确显示字幕。

### 3.2 `lang` 的规则与反模式（W3C《Declaring language in HTML》）

**必须**：

```html
<html lang="zh-Hans">
```

- **在 `html` 元素上，不是 `body`**——W3C 给的理由：`body` 覆盖不到 `head` 里的文本（`title` 等）。
- 值取自 **IANA Language Subtag Registry**，语法由 **BCP 47** 定义（`en`、`fr`、`zh-Hans`、`zh-Hant-TW`…）。BCP 47 涵盖并超出 ISO 语言/国家码集合。
- 页面内含另一种语言时，在**包裹该内容的元素**上加 `lang`：`<p>The title is "<span lang="fr">Le Bon Usage</span>".</p>`；没有现成元素就加 `<span>` / `<bdi>` / `<div>`。
- 元素**正文与属性值语言不同**时用嵌套元素拆开，别把 `lang` 挂在同一个元素上：
  ```html
  <!-- 错：title="Spanish" 也被声明成西语 -->
  <a lang="es" title="Spanish" href="...">Español</a>
  <!-- 对 -->
  <a title="Spanish" href="..."><span lang="es">Español</span></a>
  ```
- XHTML 1.x / polyglot 同时写 `lang` 与 `xml:lang`，**两者值必须相同**；纯 XML MIME 只需 `xml:lang`。

**禁止 / 无效**：

- ❌ `<meta http-equiv="Content-Language" ...>` 声明页面语言（W3C：*should never use*）。HTTP `Content-Language` header 只表示**目标受众**，且**页内 `lang` 永远覆盖 HTTP 信息**。
- ❌ **用 CSS 声明语言**（W3C：*it is not possible to declare the language of text using CSS*）。
- ❌ 从 `DOCTYPE` 里的 `EN` 推断语言——那是 **schema 的语言**，与文档内容无关。
- ❌ 从字符编码推断语言——Latin-1 可同时编码法语和英语，阿拉伯语可用 Windows-1256 / ISO-8859-6 / UTF-8；W3C 结论是**没有一对一映射**。（现在全站 UTF-8，这一点已成历史问题，但推理仍成立。）
- ⚠️ `title` 元素与属性值内**无法**给多语言片段标记（只允许纯字符，不能有标记）——W3C 明说「目前没有好的解法」，只能避免这种混排。
- ⚠️ 记得**同时**用 `dir` 处理阿拉伯语、希伯来语等双向文本（见下）。

### 3.3 `dir`：方向是标记层的，不是样式层（W3C《Structural markup and RTL text in HTML》）

```html
<!DOCTYPE html>
<html dir="rtl" lang="ar">
```

- `dir` 用于设置 base direction，以便 **Unicode 双向算法（UBA）** 正确重排文本，同时设置段落默认对齐。支持 RTL 脚本：Adlam、Arabic、Hebrew、N'Ko、Syriac、Thaana（W3C 列举）。
- HTML 中 base direction 只有两种来源：① 最近的带 `dir` 的父元素（通常是 `html`）；② 都没有则 **默认 LTR**。所以 LTR 页面**不需要**写 `dir`，写了 `dir="ltr"` 也无害。
- `html` 上加 `dir="rtl"` 后，W3C 列出的 **8 个连带效果**：
  1. 段落等块级元素右对齐
  2. 双向文本正确地从右到左流动
  3. 标点出现在相对文本的正确位置
  4. **表格列从右向左推进**，单元格内容右对齐
  5. 表单输入默认从右侧开始
  6. 含自然语言文本的属性（`alt` / `title`）继承元素方向
  7. 样式表写对（逻辑属性）时，**CSS 自动镜像布局**
  8. 设置 overflow 的方向
- **W3C 原文的硬禁令**：*「Never use CSS to apply the base direction.」* / *「Do not use CSS to apply base direction in HTML pages.」* 理由是：*「you want the directional information to be available even when the CSS is not. The directional information can affect the semantics of your content, and so should be part of the markup」*；并注明 **CSS 与 HTML 两份规范都给出同样的告诫**。
- 配套正面指令：**用逻辑属性**（`start`/`end`）写 margin / padding / alignment；**避免 `left`/`right` 取值的 HTML 属性**，改用 CSS 选择器；只在真的需要覆盖 `dir` 产生的对齐时才用 `text-align`。
- **W3C 的明确警告**：*「do not make the mistake of assuming that language declarations indicate directionality, or vice versa! Even if the language declaration has a script subtag it won't affect the directionality of the text in the user agent. **You must always declare the directionality using the dir attribute.**」*
  - 反例：阿塞拜疆语 `az` 既可用 RTL 的阿拉伯字母，也可用 LTR 的拉丁/西里尔字母 —— 语言码无法决定方向。
- ⚠️ **与 `Intl.Locale.prototype.textInfo` 的分工**：实测 `new Intl.Locale('ar-EG').textInfo.direction === 'rtl'`、`he-IL` 也是 `'rtl'`，CLDR **确实能推断**方向。但这是**数据层的推断**，绝不能替代 markup 的 `dir`——理由同上（语义、CSS 失效时仍要成立、WCAG）。可以用它做**兜底校验**（比对 `textInfo.direction` 与 `document.dir`，不一致就报警），不能用来生成 `dir`。

### 3.4 `dir="auto"` 与 `dirname`

**`dir="auto"`**（W3C）：浏览器查看元素内**第一个强方向字符**（first strongly typed character）决定该元素的 base direction。

- 适用：运行时插入的数据库内容、用户输入、表单、聊天消息、搜索结果——**方向事先未知**时。
- 查首强字符时会**跳过** `<bdi>` 内容、`<script>`、`<style>`、`<textarea>`，以及**任何带 `dir` 属性的元素**。
- **不 foolproof**：W3C 自己举例，一段以阿拉伯字符开头的英文句子会被判成 RTL，导致右对齐、问号跑到最左边。所以「知道方向就显式写死，只有真不知道才用 auto」。
- `<textarea>` / `<pre>` 可含多个段落且无法在段落内加标记；设 `dir="auto"` 后**每段独立**按首强字符判定。无强方向字符的行（如 `123-456`）用 LTR 排列字符，但**对齐存在浏览器差异**：WebKit 保持右对齐，Blink/Gecko 左对齐。
- `<input dir="auto">`：用户输入英文书名时自动变 LTR，输入阿拉伯语时自动变 RTL。

**`dirname`**（W3C）：把表单字段**计算出的方向**一起提交给服务器，供之后在别处显示时复用。

```html
<form action="addcomment.cgi" method="get">
  <p><label>Comment: <input type="text" name="comment" dirname="commentdir" required></label></p>
  <p><button name="mode" type="submit" value="add">Post Comment</button></p>
</form>
```

提交体：`comment=%D9%85%D8%B1%D8%AD%D8%A8%D8%A7&commentdir=rtl&mode=add`

- `dirname` 值可任意取（**不能为空**），就是提交参数名；不仅配合 `dir="auto"`，在 `dir="rtl"` / `ltr` 时也能提交，适合存储多语言混合内容的数据库。

### 3.5 行内双向文本（W3C《Inline markup and bidirectional text in HTML》）

**统一做法，不要逐例判断**：把**每一个**反方向短语用 `dir` **紧包裹**（tightly wrap = 元素包含整个反方向短语，且只包含它）。`dir` 不仅设 base direction，浏览器还会**方向隔离**（directionally isolate）该元素，避免后续数字/另一段反方向文本发生 spillover。

```html
<!-- 嵌套方向 -->
<p>the title is <cite dir="rtl">AN INTRODUCTION TO <span dir="ltr">c++</span></cite> in arabic.</p>

<!-- 运行时未知：dir=auto 或 bdi -->
<p>we found the phrase <q dir="auto">$phrase</q> 5 times.</p>
<p><bdi>$restaurantName</bdi> - 5 reviews</p>
```

- `<bdi>` **不写 `dir`** 时行为等同 `dir="auto"`；有现成元素就给它加 `dir="auto"`，没有就包 `bdi`（或 `<span dir="auto">`）。
- `&rlm;`（U+200F）/ `&lrm;`（U+200E）：紧跟短语后、取**周围文本**的 base direction，只解决**隔离**问题，不替代紧包裹；W3C 说这主要面向 legacy / non-conformant 浏览器。
- 不能用标记的位置（`title` 元素、属性值）才用 Unicode 隔离字符：`U+2067 RLI` / `U+2066 LRI` / `U+2069 PDI` / `U+2068 FSI`（模拟 auto）。
- **不推荐** `U+202B RLE` / `U+202A LRE` / `U+202C PDF`——它们不做方向隔离。
- `<bdo>` 只用于覆盖算法的特殊/教学场景，**必须**带 `dir="rtl"` 或 `dir="ltr"`，**不能是 `auto`**；不要和 `<bdi>` 搞混。

---

## 四、CSS logical properties：逻辑属性 inline / block、start / end 与 RTL 自动镜像

MDN 定义：CSS Logical Properties and Values 模块定义「与**书写方向**相对」而非「与物理方向绑定」的属性。

### 4.1 两根轴

| 轴 | 官方定义 | 水平书写模式 | 竖排（中/日/韩/蒙） |
|---|---|---|---|
| **block** | 垂直**于**一行内文本的流动方向 | 纵向（top→bottom） | 横向 |
| **inline** | 平行**于**一行内文本的流动方向 | 横向（LTR 左→右 / RTL 右→左） | 纵向 |

MDN 的关键句：*「**The start of a line is not always the left side of a line.**」* 流相对值：`block-start` / `block-end` / `inline-start` / `inline-end` / `start` / `end`。

### 4.2 物理 → 逻辑全映射（MDN 精确属性名）

| 物理（LTR 水平书写参照） | 逻辑属性 | RTL 下落到 |
|---|---|---|
| `margin-left` / `margin-right` | `margin-inline-start` / `margin-inline-end` | 右 / 左 |
| `margin-top` / `margin-bottom` | `margin-block-start` / `margin-block-end` | 上 / 下（不变） |
| `padding-left` / `padding-right` | `padding-inline-start` / `padding-inline-end` | 右 / 左 |
| `padding-top` / `padding-bottom` | `padding-block-start` / `padding-block-end` | 上 / 下 |
| `border-left` / `border-right` | `border-inline-start` / `border-inline-end` | 右 / 左 |
| `border-top` / `border-bottom` | `border-block-start` / `border-block-end` | 上 / 下 |
| `width` / `height` | **`inline-size`** / **`block-size`** | 仍是横向 / 纵向尺寸 |
| `min-width` / `max-width` | `min-inline-size` / `max-inline-size` | 同 |
| `min-height` / `max-height` | `min-block-size` / `max-block-size` | 同 |
| `left` / `right` | `inset-inline-start` / `inset-inline-end` | 右 / 左 |
| `top` / `bottom` | `inset-block-start` / `inset-block-end` | 上 / 下 |
| `text-align: left` / `right` | **`text-align: start` / `end`**（换的是**值**，不是属性名） | 右 / 左 |
| `border-top-left-radius` 等 | `border-start-start-radius` / `start-end-radius` / `end-start-radius` / `end-end-radius` | 随流翻转 |

简写：`margin-block` / `margin-inline`、`padding-block` / `padding-inline`、`border-block` / `border-inline`、`inset` / `inset-block` / `inset-inline`；border 子属性还有 `border-inline-start-{color,style,width}` 与 `border-block-start-*` 等。W3C 补充：`float: inline-start | inline-end`、`justify-content: flex-start | flex-end`、`grid-column-start/end`、`align-content`。

**可抄的一行**：

```css
.card {
  padding-inline: 16px;
  padding-block: 12px;
  margin-inline-start: 8px;
  inline-size: min(100%, 320px);
  border-inline-start: 3px solid var(--accent);
  text-align: start;
}
```

### 4.3 什么时候**仍然**用 `left` / `right`

W3C：*「Left and right values may still be useful, occasionally, if you want the item you are positioning to remain in a fixed location, independent of the language of the text.」* 判据是**设计意图**：想跟随阅读方向 → 逻辑；想钉死在屏幕物理位置（如固定的关闭按钮、与语言无关的硬件示意图）→ 物理。把这句话写进代码评审清单，能挡掉一半「全量替换成逻辑属性」的误伤。

### 4.4 常见漏网点

- `transform: translateX(20px)` / `rotate()` 不会自动镜像，需要按 `dir` 显式分支或改写成逻辑方向。
- `background-position: left`、渐变方向、`box-shadow` 的 x 偏移是物理值。
- `scrollLeft`、滚动容器、轮播的「下一张」方向。
- SVG / Canvas / 图表内坐标（见 §5 不镜像清单）。
- `text-align: left` 写在一个继承了 `dir="rtl"` 的组件里，会把 RTL 文本强行左对齐——W3C 建议尽量不用 `text-align`，让 `dir` 自己决定。
- 图标字体 / icon 组件内部若有方向性笔画，需要单独的 RTL 变体（见 §5）。

---

## 五、RTL 镜像规则：该镜像与不该镜像清单（Material Design Bidirectionality 官方）

Material 定义：把 UI 从 LTR 切到 RTL 通常叫 **mirroring**，RTL 布局是 LTR 布局的镜像，影响 layout / text / graphics。**时间的流逝**在 LTR 里表现为左→右，RTL 里表现为右→左。

### 5.1 应该镜像（白名单）

| 元素 | 规则 |
|---|---|
| 布局 / 标题 / 图标 / UI 元素整体流向 | 从右到左流动 |
| 文本（已译为 RTL 语言） | 右对齐 |
| 文本字段的图标 | 换到字段的另一侧 |
| 导航按钮 | 顺序反转；**返回箭头指向右**（LTR 指左） |
| 方向性图标（箭头、前进/后退、自行车朝前） | 镜像；LTR 自行车朝右 = 前进，RTL 朝左 = 前进 |
| 主按钮 / 次按钮 | 位置镜像以匹配阅读方向 |
| Checkbox / Radio | 出现在文字的**右侧** |
| tab 与滑动方向 | 首个 tab 靠右，向右滑看更多 |
| 进度条 | **按内容阅读方向填充**（注意 §5.3 的媒体例外） |
| 时间线 / 事件序列 | 从右到左推进 |
| 带滑块的音量图标 | 滑块 RTL 推进，声波从右侧发出 |
| 含文本表意的图标 | 段落缩进、首行、段落末尾未填满行、右侧毛边、聊天气泡尾巴都要镜像 |
| 段落工具栏 | LTR 文档里编辑 RTL 段落时，**该段落的缩进/列表按钮应为 RTL**（即使主 UI 是 LTR） |
| redo / undo | 同时含「水平」与「圆周」两种时间方向，RTL 下**必须二选一**，不要两个都翻 |

### 5.2 不应该镜像（黑名单）

| 元素 | Material 给的理由 |
|---|---|
| **数字**、数字图标内的数字 | 数字本身不镜像；但**数字字形要本地化**（孟加拉、马拉地、尼泊尔、部分阿拉伯语 locale 用不同数字） |
| **未翻译文本**（URL、品牌名、LTR 词） | 即使嵌在 RTL 短语里，仍保持 LTR；W3C 的 `dir` 紧包裹负责这件事 |
| 时钟、电话号码、钟表数字 | 数字不镜像 |
| **不传达方向的图标**（相机等） | 无方向语义 |
| **图表与图形**（charts / graphs） | 数据坐标不随阅读方向翻转 |
| **圆周方向的时间** | 时钟仍顺时针；圆形**刷新/进度**、**历史**图标不镜像 |
| 物理对象图标 | 键盘、耳机「各地长得一样」 |
| **右手持物图标** | 放大镜（手柄在右下）、咖啡杯——RTL 国家多数人也是右撇子 |
| **媒体播放按钮与媒体进度条** | 反映的是**磁带走带方向**，不是时间方向；Material 明确「media controls for playback are always LTR」 |
| 斜线（slash 表示 off 态） | 「Most RTL countries do not mirror slashes」，保持原图 |

### 5.3 三个最易错的边界

1. **一般进度条 vs 媒体进度条**：Material 一边说「Progress bars fill in the same direction as content is read」，一边说「Do not mirror media playback buttons and the media progress indicator」。裁决：**下载/安装/步骤进度条镜像；音视频播放进度条不镜像**。同一个词，两套规则。
2. **线性时间 vs 圆周时间**：箭头前进/后退（线性）镜像；刷新、历史、时钟（圆周）不镜像。redo/undo 两者兼有 → 选一个方向表现，别双重翻转。
3. **数字「不镜像」≠「不本地化」**：数字顺序与数值不变，但字形要换。实测 `Intl.NumberFormat('ar-EG').format(1234567.89)` → `١٬٢٣٤٬٥٦٧٫٨٩`；`Intl.Locale('ar-EG').numberingSystems` → `['arab']`，而 `he-IL` → `['latn']`。所以**按 locale 取 numberingSystem，不是按 RTL 一刀切**。

### 5.4 Material 2 的精确数值（RTL 前后保持相同，变化的是左右归属）

| 项目 | 值 |
|---|---|
| tab 触控高度 | 48dp |
| 首个 tab 距屏幕边缘 | 72dp |
| tab 标签下内边距 | 20dp |
| tab 标签左右内边距 | 12dp |
| 图标距屏幕边缘 | 16dp |
| 标题距屏幕边缘 | 72dp |
| 标题下内边距 | 20dp |
| 导航栏高度 | 56dp |
| 溢出菜单内边距 | 16dp |
| 列表项高度 | 72dp |

平台支持（Material 官方标注）：Android / iOS / Web / Flutter **均 Available**。

### 5.5 RTL 页面验收动作

切到 `dir="rtl"` 后逐项看：返回箭头方向、主次按钮顺序、checkbox 在文字右侧、字段图标换边、tab 起始位置、进度条填充方向、图标镜像白名单是否误伤黑名单、数字是否仍是 LTR 且字形正确、URL/品牌名是否保持 LTR、标点位置、表格列推进方向、overflow 方向、`alt`/`title` 方向。

---

## 六、复数 plural：CLDR 六类、ICU 复数规则、不同语言复数形式（Node 实测）

### 6.1 CLDR 官方类别（逐字取）

CLDR 使用 6 个助记标签：`zero` / `one` (singular) / `two` (dual) / `few` (paucal) / `many`（也用于有独立类别的分数）/ **`other`（required — general plural form — 也是「语言只有一种形式」时使用的类别）**。

三条官方强调：

- *「These categories are only mnemonics -- the names don't necessarily imply the exact contents of the category.」*
- *「A common mistake is to think that "one" is only for only the number 1. Instead, "one" is a category for **any number that behaves like 1**.」* 例如某些语言 `one` 覆盖 1 / 21 / 151 但不包括 11 / 111；**法语的 0 也归入 `one`**（因为 0 修饰的单位用单数形式）。
- *「If no forms change, then stop (there are no plural rules — everything gets "other")」* → 中文/日语/韩语等只有 `other`。
- CLDR 还指出历史命名例外：Russian 和 Arabic 的 `many` / `other` 当年应该对调，但已太晚不能改。
- 命名准则里 `two` / `zero` 被限定为「整数值以 2 / 0 结尾」的形式，`few` / `many` 由剩余集合中「最小剩余数」决定（如 4 / 10）。
- 官方全 6 类的示例语言是 **Welsh**（`0 cŵn / 1 ci / 2 gi / 3 chi / 6 chi / 4 ci`）。

### 6.2 CLDR 49 语言复数规则图表：各 locale 的 `cardinal` 类别

| locale | cardinal 类别 |
|---|---|
| `zh` / `ja` / `ko` / `id` / `vi` | 仅 `other` |
| `en` | `one`, `other` |
| `fr` | `one`, `many`, `other` |
| `ru` / `pl` | `one`, `few`, `many`, `other` |
| `ar` | `zero`, `one`, `two`, `few`, `many`, `other`（全 6 类） |
| `cy`（Welsh） | 全 6 类 |

> 口径：只看 **cardinal**（普通名词/单位复数）。图表另有 `ordinal` 与 `range` 行，例如 `en` 的 ordinal 有 `one/two/few/other`，**不要**混进 cardinal 的表。

### 6.3 Node v22.22.2 `Intl.PluralRules` 本机实测（本章最有价值的表）

`new Intl.PluralRules(locale).select(n)` 实测输出：

| locale | 0 | 1 | 2 | 3 | 5 | 11 | 21 | 100 |
|---|---|---|---|---|---|---|---|---|
| `en-US` | other | **one** | other | other | other | other | other | other |
| `de-DE` | other | **one** | other | other | other | other | other | other |
| `fr-FR` | **one** | one | other | other | other | other | other | other |
| `ja-JP` | other | other | other | other | other | other | other | other |
| `zh-CN` | other | other | other | other | other | other | other | other |
| `ar-EG` | **zero** | one | **two** | **few** | **few** | **many** | **many** | other |
| `ru-RU` | **many** | one | **few** | **few** | many | many | **one** | many |
| `pl-PL` | many | one | few | few | many | many | many | many |
| `cy` | zero | one | two | few | other | other | other | other |
| `hi-IN` | **one** | one | other | other | other | other | other | other |

**三条直接推翻直觉的结论**：

1. **`ru` 的 21 → `one`、11 → `many`**：所以「`n % 10 == 1` 就是单数」这种手写规则是错的，俄语 21 是单数、11 不是。
2. **`fr` 的 0 → `one`、`hi` 的 0 → `one`**：把 0 硬塞进「复数」分支在法语/印地语里是语法错误。
3. **`ar` 在 0–100 区间就跑遍 6 类中的 5 类**：给阿拉伯语只准备 `one` / `other` 两个分支，会直接漏掉 2、3、11 三种形态。

补充实测：

- 分数：`ar` 的 0.5 → `other`（不是 `few`）；`en` 的 1.5 → `other`；`ru` 的 0.5 → `other`。**别把整数规则套到小数上**。
- `type: 'ordinal'`（`en-US`）：`1→one, 2→two, 3→few, 4→other, 11→other, 21→one`。
- `fr-FR` 在 0–100 区间未出现 `many`，但 CLDR 图表列出 `many`（大数如 1 000 000 才触发）→ **手写分支表时以 `Intl.PluralRules` 运行时结果为准，并始终保留 `other` 兜底**。

### 6.4 设计含义

- 任何含数量的 UI 文案（「已删除 N 项」「N 条未读」「N 天前」）都**必须**走 ICU `plural` / `selectordinal`，不能写 `n === 1 ? A : B`。
- 中文只有 `other`，所以**中文产品最容易漏测**——在自己语言里永远看不到 bug，一出海就炸。
- 给译员的表格要为**目标语言**列全 CLDR 类别，不是照抄英文的 `one`/`other`。CLDR 原文：*「The translation system and the translator together need to add "one", "few" etc. if and as necessary per target language」*。
- 数字本身交给 `Intl.NumberFormat`（§10），不要把 `{n}` 手动拼进句子。

---

## 七、ICU MessageFormat：禁拼接字符串、单句完整翻译、select / plural / selectordinal

ICU 用户指南的出发点直接点名拼接的危害：*「If the user-visible string were concatenated directly from fragments and formatted elements, then translators would not be able to rearrange the pieces」* —— 消息必须**作为一个整体**编写与翻译。

### 7.1 三种复杂参数

- `plural`：按数值 + 该语言复数规则选子消息
- `select`：按固定关键字集合选子消息（性别、类别、平台…）
- `selectordinal`：序数复数
- 旧的 `choice` 类型 **ICU 明确不推荐**（处理不了很多语言的复数规则）

### 7.2 官方示例（逐字取，含 `offset` 与 `#`）

```
{gender_of_host, select,
  female {
    {num_guests, plural, offset:1
      =0 {{host} does not give a party.}
      =1 {{host} invites {guest} to her party.}
      =2 {{host} invites {guest} and one other person to her party.}
      other {{host} invites {guest} and # other people to her party.}}}
  male { ... }
  other { ... }}
```

- `offset:1`：把「主人本人」从计数里扣掉，`#` 输出的是 **扣除 offset 后的值**（不是原始 `num_guests`）。
- `=0` / `=1` / `=2` 是**精确匹配**，优先于类别分支。
- ICU 原文的 Note：若英文消息同时有 `=0` 和 `=1`（直到 `=offset+1`），**就不需要 `one` 分支**（永远选不中）；但**永远需要 `other`**。
- 译文里要按目标语言**自行补** `one` / `few` 等分支（见 §6.4）。

### 7.3 嵌套顺序的官方建议

> *「If possible, use complex arguments as the **outermost structure** of a message, and write **full sentences** in their sub-messages. If you have nested select and plural arguments, place the **select** arguments (with their fixed sets of choices) on the **outside** and nest the plural arguments (hopefully at most one) inside.」*

理由：只把句子的一小段包进 complex argument，译者① 看不懂片段与句子其余部分如何相互作用，② 不知道能不能扩大/缩小 argument 覆盖范围来让整句在目标语言里成立。

**所以**：`select` 外层 → `plural` 内层 → 每个子消息写**完整句子**。

### 7.4 引号 / 转义（最容易踩的坑）

- 语法字符在文本部分要用**成对的 ASCII 撇号**包起来；一对 ASCII `''` 代表一个 ASCII `'`，类似 `printf` 的 `%%`：
  `This '{isn''t}' obvious` → `This {isn't} obvious`
- **ICU 4.8 起**：ASCII 撇号**只在紧邻「需要引用的字符」时**才开启引用文本（"only where needed"），嵌套子消息里行为与顶层一致；4.8 之前行为不一致，是历史 bug 源。
- **官方推荐**：面向人的文本用真正的撇号 **`’` U+2019**；ASCII `'` U+0027 只留给程序语法。这同时也解决了「译员把 `it's` 里的单引号当语法字符」的问题。

### 7.5 参数格式化的官方取舍

| 方式 | ICU 立场 |
|---|---|
| 预定义 style：`short/medium/long/full`、`integer/currency/percent` | ✅ 推荐 |
| **Skeleton**（`::` 前缀，如 `::dMMMM`、`::jmm`） | ✅ **推荐**，locale-independent；骨架按 MessageFormat 的 locale 本地化，能享受 CLDR 已策展的格式 |
| **先单独格式化参数再传字符串** | ✅ 推荐（最大控制力） |
| String pattern（自定义日期 pattern） | ❌ 不推荐：locale-sensitive，需要译员本地化，易写出非法 ICU 语法；且多数公司只翻「泛型语言」(fr/es/ar)，一套 pattern 会被几十个国家复用 |
| Custom Format 对象（`setFormat`） | ❌ 不推荐：只有顶层参数可见，嵌套子消息里的参数「invisible」 |

官方示例输出 `At 4:34 PM on March 23, there was a disturbance in the Force on planet 7.` 的模式：
`At {1,time,::jmm} on {1,date,::dMMMM}, there was {2} on planet{0,number,integer}.`

> 备注：ICU 用户指南注明 **MessageFormat 2.0** 正由 working group 制定（ICU4J 已有 Technical Preview）。本文件记录的是当前长期使用的 `MessageFormat` API；MF2 落地后需重新核对语法。

### 7.6 反模式速查

- ❌ `"Welcome " + name + "!"`（语序可能不同）
- ❌ `"共 " + n + " 项"` + 另写一套复数（变量被拆开、中文看不到 bug）
- ❌ 把 `{count}` 手动 `String(n)` 后再拼（丢掉 locale 数字格式）
- ❌ 只给英文的 `one`/`other` 两个 key 让译员填阿语
- ❌ 在字符串里写日期 pattern / 货币符号
- ❌ `select` 分支里翻译成句子片段而不是完整句

---

## 八、Intl API 全表与本机实测（Node v22.22.2）

MDN 官方定义：*`Intl` is not a constructor* —— 不能用 `new`，也不能当函数调用；所有属性和方法都是静态的（类似 `Math`）。它是 **namespace object**，里面装的是构造器与公共能力。

### 8.1 完整清单

| 类别 | 精确名称 | 用途 |
|---|---|---|
| 构造器 ×10 | `Intl.Collator` | 语言敏感的字符串比较/排序 |
| | `Intl.DateTimeFormat` | 日期时间格式化 |
| | `Intl.DisplayNames` | 语言/地区/脚本名称的一致翻译 |
| | `Intl.DurationFormat` | 时长格式化 |
| | `Intl.ListFormat` | 列表连接 |
| | `Intl.Locale` | Unicode locale identifier 对象 |
| | `Intl.NumberFormat` | 数字/货币/单位格式化 |
| | `Intl.PluralRules` | 复数类别选择 |
| | `Intl.RelativeTimeFormat` | 相对时间 |
| | `Intl.Segmenter` | 按 locale 分词/分句/分字 |
| 静态属性 | `Intl[Symbol.toStringTag]` | 初值 `"Intl"`，供 `Object.prototype.toString()` |
| 静态方法 ×2 | `Intl.getCanonicalLocales()` | 返回规范化的 locale 名 |
| | `Intl.supportedValuesOf()` | 返回实现支持的 calendar / collation / currency / numberingSystem / unit 的**有序唯一值数组** |

**实测能力警告（本轮独有）**：MDN 列出了 `Intl.DurationFormat`，但本机 Node **v22.22.2** 执行 `new Intl.DurationFormat('zh', ...)` 抛 **`TypeError: Intl.DurationFormat is not a constructor`**。即「规范/文档已列出 ≠ 运行时已实现」。生产代码必须做能力检测（`typeof Intl.DurationFormat === 'function'`）并准备降级，**不要照抄 MDN 清单当兼容性表**。

`Intl.supportedValuesOf('calendar')` 实测 **18** 个（前 8：`buddhist, chinese, coptic, dangi, ethioaa, ethiopic, gregory, hebrew`）；`Intl.supportedValuesOf('currency')` 实测 **162** 个。

### 8.2 `Intl.Locale` 元数据实测（日历 / 数字系统 / 周 / 方向）

| locale | `textInfo.direction` | `calendars` | `numberingSystems` | `weekInfo` |
|---|---|---|---|---|
| `ar-EG` | `rtl` | `gregory, coptic, islamic, islamic-civil, islamic-tbla` | `arab` | `firstDay:6, weekend:[5,6], minimalDays:1` |
| `he-IL` | `rtl` | `gregory, hebrew, islamic, islamic-civil, islamic-tbla` | `latn` | `firstDay:7, weekend:[5,6], minimalDays:1` |
| `zh-CN` | `ltr` | `gregory, chinese` | `latn` | `firstDay:1, weekend:[6,7], minimalDays:1` |
| `en-US` | `ltr` | `gregory` | `latn` | `firstDay:7, weekend:[6,7], minimalDays:1` |

**设计含义**：日历控件的**周起始日**和**周末**必须按 locale 取，不能写死周一或周日——实测 `zh-CN` 周一、`en-US` 周日、`ar-EG` 周六（firstDay 6）、`he-IL` 周日；`ar-EG` 周末是周五+周六。这也是「多语言日历」最高频的视觉 bug。

> 再次强调 §3.3：`textInfo.direction` 是 CLDR 推断，**不得**替代 markup 的 `dir`。用途是兜底校验与生成测试用例。

### 8.3 语言协商（locale negotiation）与 `navigator`

MDN：所有国际化构造器都接受 `locales` + `options`，用 `options.localeMatcher` 指定的算法，把请求的 locale 与实现支持的 locale 协商。

- `localeMatcher` 仅两个值：`"lookup"`（遵循 **BCP 47 Lookup 算法**）/ `"best fit"`（运行时可给出比 lookup 结果更合适的 locale，为默认）。
- `locales` 可以是 `undefined`（用默认 locale）、单个 locale 字符串 / `Intl.Locale`、或按优先级排序的**数组**。
- 错误处理：非字符串非对象 → `TypeError`；语法非法的字符串 → `RangeError`；well-formed 但实现不认识 → **忽略并尝试下一个**，最终回退系统 locale。
- 无 `locales` 或无匹配 → 运行时默认 locale。选定后，Unicode extension（如 `-u-co-phonebk`）用于定制行为，各构造器支持的 key 子集不同。
- 浏览器接入：`navigator.language`（首选语言）、`navigator.languages`（**有序**偏好列表，可直接传给构造器实现基于偏好的回退）。

本机实测：

```
Intl.getCanonicalLocales('zh_cn')            → RangeError: Incorrect locale information provided
Intl.getCanonicalLocales('ZH-cn')            → ['zh-CN']
Intl.getCanonicalLocales('zh-Hans-CN')       → ['zh-Hans-CN']
new Intl.NumberFormat(['zz-ZZ','fr-FR'], {localeMatcher:'lookup'}).resolvedOptions().locale → 'fr-FR'
```

**结论**：BCP 47 用**连字符**，`zh_cn` 这类下划线写法在 `Intl` 里直接抛 `RangeError`。后端常见的 `zh_CN` 命名在传给 `Intl` 前必须转换。

---

## 九、日期 / 时间 / 日历 / 时区格式（Node 实测）

同一个 `Date('2026-03-09T16:05:00Z')`，`dateStyle:'full'`、`timeZone:'UTC'`：

| locale | `Intl.DateTimeFormat` 输出 |
|---|---|
| `en-US` | `Monday, March 9, 2026` |
| `en-GB` | `Monday, 9 March 2026` |
| `de-DE` | `Montag, 9. März 2026` |
| `ja-JP` | `2026年3月9日月曜日` |
| `zh-CN` | `2026年3月9日星期一` |
| `ar-EG` | `الاثنين، ٩ مارس ٢٠٢٦` |
| `ja-JP-u-ca-japanese` | `令和8年3月9日月曜日` |
| `ar-EG-u-ca-islamic` | `٢٠ رمضان ١٤٤٧ هـ` |

`hourCycle` 实测：`en-US → h12`、`fr-FR → h23`、`ar-EG → h12`。

**规则**：

- **永远不要硬编码 `MM/DD/YYYY`**。`03/09/2026` 在 `en-US` 是 3 月 9 日，在 `en-GB` 是 9 月 3 日——是**歧义**而不只是「不好看」。
- 用 `Intl.DateTimeFormat` / `toLocaleDateString()`，或在服务端按 locale 格式化；**把时区显式传进去**（`timeZone`），不要依赖运行环境。
- 日期选择器要按 locale 给**周起始日、周末、日历系统、firstDayOfWeek**（§8.2）；`ar-EG` 与 `he-IL` 虽都是 RTL，但数字系统不同（`arab` vs `latn`）、周起始日也不同。
- 时间用 `hourCycle` 而不是假定 12/24 小时制；实测 `fr-FR` 是 `h23`。
- 相对时间用 `Intl.RelativeTimeFormat`：实测 `numeric:'auto'` 下 `-1 day` → `en: "yesterday"` / `zh: "昨天"`。`numeric:'always'` 会得到 `-1 day` 对应的数字形式，适合紧凑表格。
- 时长用 `Intl.DurationFormat`（**先做能力检测**，见 §8.1）；降级时用 `Intl.NumberFormat` + `Intl.ListFormat` 组合或产品自定义模板。
- 骨架优先（§7.5）：ICU 场景用 `::dMMMM` 之类，别在译文里放 pattern。

---

## 十、数字 / 货币 / 单位 / 千分位格式（Node 实测）

`Intl.NumberFormat` 格式化 `1234567.89`：

| locale | 输出 | 分组特征 |
|---|---|---|
| `en-US` | `1,234,567.89` | 逗号分组、点小数 |
| `de-DE` | `1.234.567,89` | **分隔符与 en-US 完全对调** |
| `fr-FR` | `1 234 567,89` | 窄不换行空格（U+202F）分组 |
| `hi-IN` | `12,34,567.89` | **印度 3-2-2 分组**，不是每 3 位 |
| `ar-EG` | `١٬٢٣٤٬٥٦٧٫٨٩` | 阿拉伯-印度数字字形 + 阿拉伯千分位/小数点 |
| `zh-CN` | `1,234,567.89` | 拉丁数字 |

货币（`EUR`, `1234.5`）：`en-US → €1,234.50`（符号在前）/ `de-DE → 1.234,50 €`（符号在后且前有空格）/ `fr-FR → 1 234,50 €`。
`JPY` 无小数：实测 `new Intl.NumberFormat('ja',{style:'currency',currency:'JPY'}).format(1234.5)` → `￥1,235`。
`currencyDisplay:'name'`：实测 `de` → `12,00 Euro`。
单位：实测 `80` km/h → `en: "80 kilometers per hour"` / `zh: "每小时80公里"`（**单位词序完全不同**）。

**规则**：

- 数字、货币、单位、百分号一律交给 `Intl.NumberFormat`，不要在文案里写 `¥` 或 `,` 或 `%`。
- **货币符号 ≠ 货币**：`¥` 可能是 CNY 也可能是 JPY；用 ISO 4217 code + `currencyDisplay`，需要区分时显式写 `CNY`/`JPY`。
- 金额列右对齐 + `font-variant-numeric: tabular-nums`（见 `form-table.md`），但**RTL 下「右」是 `text-align: end`**，别写死 `right`。
- 小数位数按货币取（JPY 0 位、多数 2 位），不要统一 `toFixed(2)`。
- 输入框里的数字解析要按 locale 反解（`1.234,50` 在 de-DE 是 1234.5），不要直接 `parseFloat`——这是表单国际化最高频的数据错误。
- 千分位空格可能是 U+202F 窄不换行空格，做文本比对/测试快照时不要当成普通空格。

---

## 十一、列表 / 相对时间 / DisplayNames / 排序 Collator / 中文分词 Segmenter（Node 实测）

| API | 实测 |
|---|---|
| `Intl.ListFormat(l, {type:'conjunction'})` 格式化 `['A','B','C']` | `en-US: "A, B, and C"`（**牛津逗号**）/ `de-DE: "A, B und C"` / `zh-CN: "A、B和C"` / `ar-EG: "A وB وC"` |
| `Intl.RelativeTimeFormat(l,{numeric:'auto'}).format(-1,'day')` | `en: "yesterday"` / `zh: "昨天"` |
| `Intl.DisplayNames(['zh-CN'],{type:'region'}).of('DE')` | `德国` |
| `Intl.DisplayNames(['zh-CN'],{type:'language'}).of('ar')` | `阿拉伯语` |
| `Intl.Segmenter('zh',{granularity:'word'}).segment('国际化与本地化设计')` | `国际｜化｜与｜本地｜化｜设计` |
| `['ä','a','z'].sort(new Intl.Collator('de').compare)` | `['a','ä','z']` |
| `['ä','a','z'].sort(new Intl.Collator('sv').compare)` | `['a','z','ä']`（**瑞典语 ä 排在 z 之后**） |
| `['10','2','1'].sort(new Intl.Collator('en',{numeric:true}).compare)` | `['1','2','10']`（不开 `numeric:true` 是 `['1','10','2']`） |

**规则**：

- **不要用 `+ ', ' +` 拼列表**，也不要自己实现「最后一项用 and」——`ListFormat` 覆盖 `conjunction` / `disjunction` / `unit` 与 `style`。
- **排序必须用 `Intl.Collator`**，不能用 `Array.sort()` 默认（按 UTF-16 码位）或 `localeCompare` 的隐式 locale。德语与瑞典语对 `ä` 的位置完全相反，实测如上。含数字的编号要开 `numeric: true`。
- **中文分词不能靠空格**：`Segmenter` 实测把「国际化与本地化设计」切成 6 段。搜索高亮、字数统计、换行断行、双击选词都要按 locale 分词。
- 语言/地区/脚本**选择器**用 `DisplayNames`，别自己维护一张中文国家名表。
- 姓名排序见 §12（不总按姓排）。

---

## 十二、姓名 / 地址 / 称呼：不要 first name + last name（W3C《Personal names around the world》）

W3C 开宗明义：设计表单/数据库/本体的人常常不知道别国姓名可以有多不同，于是**假设过多**。

### 12.1 官方点名的反例（按类型）

| 文化 | 例子与要点 |
|---|---|
| 中文 | **毛泽东**：`Mao` 是姓且在最前；`Ze` 是字辈名（毛泽民/毛泽覃/毛泽紅 共用）；**姓名各部分之间不加空格**；称呼 `毛泽东先生` 或 `毛先生` |
| 日/韩/匈牙利 | 同样是**姓在前、名在后**；日语汉字读音多义（東海林 可读 Tōkairin 或 Shōji），需要 kana 读音字段才能排序 |
| 西语 | **María José Carreño Quiñones**：`José` 是 given name 的一部分（不是 middle name）；两个姓典型为**父+母**，巴西可为**母+父**甚至 3–4 个姓；中间可能有 `de` / `e`；称呼 `Señorita Carreño` |
| 阿拉伯语 | `Abu Karim Muhammad al-Jamil ibn Nidal ibn Abdulaziz al-Filistini` —— 由亲属关系、称号、族谱、地点构成的长姓名 |
| 冰岛 | **Björk Guðmundsdóttir**：第二部分是 patronymic（父名 + `-son`/`-dóttir`），**不是西式 family name**；冰岛人按 **given name** 称呼和排序（电话簿也按 given name） |
| 单名 mononym | 南印度、马来西亚、印尼大量人只有 given name，无 patronym；`Isa bin Osman`（`bin` = son of，女性 `binti`） |
| 越南 | `Nguyễn Tấn Dũng`（姓-中-名），但正式称呼用 **given name**：`Mr. Dũng` 而非 `Mr. Nguyễn` |
| 泰国 | 常有不随正式姓名的 nickname：`Thaksin Shinawatra` → `Maew (แม้ว)` |
| 俄语 | `givenName-patronymic-familyName`，patronymic 与姓的词尾标示性别 |
| 印度（Kerala 等） | `V. S. Achuthanandan` = `familyName-fathersName-givenName`；另有 `villageName-fathersName-givenName-lastName` 等混合顺序 |

### 12.2 官方设计建议（可直接作为表单规范）

**首选**：**单一 `Full name` 字段**，按用户原样输入。W3C：*「it will be simpler, where it is possible, to just use the full name as the user provides it」*。先自问「是否真的需要拆成 given/family」。

**需要拆时才拆，且按用途加字段**：

- 避免 `first name` / `last name` 标签（会让姓在前的人困惑）；通用标签可用 `Family name` / `Other/given names`，但 W3C 说冰岛人仍不适用。
- 称呼：加 `What should we call you?`（也能处理泰国 nickname）——因为不是所有人都乐意被陌生人直呼 given name，且各地 formality 差异极大（德国 `Herr Professor Doktor Schmidt`、日本 `Tanaka-sama` / `Tanaka-bucho`）。
- 排序：加**读音字段**（日语 kana）；W3C 明确「不能总从表意字符判断读音」。
- 脚本：需要时分成 `Name (in your alphabet)` + `Latin transcription (if different)`，日语可能还要第三个音节文字字段。
- 改过名：用 `Previous name`，**不要** `Maiden name` / `née`（不只是女性改姓）。

**必须避免**（W3C 逐条）：

- ❌ 强制 `family name`。W3C 原话：否则用户会往里填 `.` 或 `Mr.` 只为逃出表单。
- ❌ 依赖自动拆分姓名的算法（点名 v-card / h-card 的 implied "n" optimization 对中文姓名会出错）。
- ❌ 假设家庭成员同姓；假设给定顺序是「名后跟姓」。
- ❌ 把单字母姓名当缩写并阻止提交（应给 warning，不 block）。
- ❌ 规范化大小写（`McNamara`、`van der Waals`）；强制全大写；禁止空格/连字符/撇号等标点。
- ❌ 强制 title（若要性别就直接问性别，别用 `Mr./Mrs./Ms.` 逼女性透露婚姻状况）。
- ❌ 限制输入框/显示区/**数据库字段**长度。W3C 特别提醒：**不要以为 4 个字的日文名在 UTF-8 里占 4 字节——很可能需要 12**。
- ❌ 假设所有列表按 family name 排序；`von` / `de` / `van` 等小词是否参与排序各地不一。
- ✅ 全链路 Unicode / UTF-8（页面、后端 DB、中间所有软件）；若系统只接受 ASCII，必须**明确告知用户和译员**（W3C 给的标签示例 `Full name (Use only letters A to Z with no accents.)`）。

**地址**：同样不要假定「省-市-街道-邮编」结构、不要假定必有邮编、不要把 `address1/address2` 当成通用模型；用 `Intl` 无法解决地址格式，应落到按国家配置的字段模板 + 一个自由文本块兜底。

---

## 十三、语言协商 locale negotiation 与回退策略

把 §8.3 的运行时规则落到产品上：

1. **优先级来源**：URL/用户显式设置 > 用户账号偏好 > `navigator.languages` 有序列表 > `navigator.language` > 系统默认 > 产品默认。
2. **locale 全链路传递**：`zh-Hans-CN` 不要在中途截断成 `zh`；地区决定日期、货币、周起始日（§8.2、§9）。
3. **回退要有边界**：`zh-Hant-TW → zh-Hant → zh → 默认`。但 `best fit` 可能给出「更宽」的匹配，别假设回退链一定逐级。
4. **缺失译文处理**：显示可识别的占位（键名或源语言）+ 上报，**不要显示空白或 `undefined`**；伪本地化的 `^` 定界符（§14）就是为暴露这类问题。
5. **别按 IP 静默定语言**：会与账号偏好、分享链接冲突；至少提供可见切换器，并记住选择。
6. **格式化与翻译分离**：文本走消息目录，日期/数字/复数走 `Intl`；两者都按同一个 locale，别出现「德语界面 + 美式日期」。
7. **服务端渲染要显式传 locale**：Node/容器的默认 locale 可能与用户不同；`toLocaleString()` 不传 locale 就有不确定性。
8. **缓存按 locale 分片**：HTML/JSON 响应、CDN key、图片文字层都要带 locale 维度。

---

## 十四、伪本地化 pseudolocalization / 伪翻译 / 伪 locale（Microsoft Learn 官方）

**定义**：不真的翻译，用自动转换源文本来**模拟翻译的常见副作用**，在翻译开始前就能验证产品可本地化性，并贯穿整个开发周期持续回归。Microsoft 说这些手段在圈内简称 "pseudo"。

### 14.1 伪翻译的五种变换（官方原文）

| 变换 | 官方内容与数值 | 能暴露什么 |
|---|---|---|
| **加重音/其它脚本字符** | `a` 随机替换为 `αäáàāāǎǎăăåå` 之一；数字 1–9 换成带圈数字 **①–⑨（U+2460–U+2468）** | 字体缺字、编码问题、硬编码字符假设 |
| **加长字符串** | 源语言为英语时，**好的启发式是 +40%**；实践中极端情况可达 **200% 甚至 400%**；**一两个词的串按比例增长得比长串更多** | 布局、截断、换行 |
| **填充到膨胀长度** | 用希腊、西里尔、亚洲、印度文字字符补齐到目标长度 | 裁剪与字体处理问题 |
| **加定界符** | 用一对 `^` 包住每个字符串 | **末尾定界符缺失 = 截断**；定界符出现在显示文本中间 = **拼接字符串** |
| **加唯一标识** | 资源 id 的 hash 或别的唯一数据 | 快速定位界面上那串文案来自哪个资源 |

另两个官方要点：

- **没被伪翻译的资源会非常显眼** → 直接暴露「哪些字符串没外置」。
- **译文变短（shrinkage）通常问题较少且难模拟，所以伪本地化不模拟它**（与 §2.3 的「收缩也是问题」并不冲突：这是测试手段的取舍，不是设计可以不管）。
- 伪翻译**不能替代**真译应用的验证。

### 14.2 伪 locale（专测格式化与解析）

Windows 定义三个伪 locale：

| 伪 locale | 名称 |
|---|---|
| `qps-ploc` | Base |
| `qps-plocm` | **Mirrored**（测 RTL 镜像） |
| `qps-ploca` | East Asian-language（测东亚文字） |

ICU 提供两个：`en-XA`（**A** for Accents）、`en-XB`（**B** for bidirectional）。

**命名规则（RFC 4646 §2.2.1.3）**：`qaa`–`qtz` 是为私有用途保留的 language subtag，Windows 三个伪 locale 都以 `qps` 开头，落在保留段内。

Microsoft 给的历史教训很值得记：早期用 **`tk-TM`**（土库曼语）当伪 locale，结果下一版 Windows 真把 `tk-TM` 做成了正式 locale，导致构建/测试系统大量 bug。结论：**伪 locale 名必须合法但永远不会描述真实语言**。`ps-PS` 也不合适（可被解读为 Pashto）。

### 14.3 可执行的伪本地化验收流程

1. 全站切到 `en-XA`（或自定义 40% 加长 + 音标 + `^` 定界）→ 检查截断、换行、重叠、`min-inline-size` 是否生效。
2. 对 **microcopy 单独跑 200% 加长**（§2.3：40% 对短串不够）→ 检查按钮、tab、表头、标签。
3. 切到 `en-XB` / `qps-plocm` → 检查 §5 的镜像白/黑名单。
4. 切到 `qps-ploca` → 检查行高、字宽、字体回退（§2.4）。
5. 检查所有 `^...^` 成对出现；成对定界符出现在**一句中间** = 有拼接，立即修。
6. 检查仍有英文原文的地方 = 字符串未外置。
7. 记录唯一 id 与界面位置的映射，交给译员做上下文。

---

## 十五、文化适配：颜色、图标、图像、示例数据与数字字形

- **颜色含义不通用**：`ux-writing.md` §13 给的例子是白色在西方=婚礼、东亚=丧礼。做法不是「背一张颜色文化表」，而是**为目标市场做一次调研并写进 locale brief**，尤其语义色（成功/危险/警告）与营销主色。同时注意：`dark-mode.md` / `accessibility.md` 的对比度硬指标**不因文化让步**（4.5:1 / 3:1 是生理与规范约束，不是审美选择）。
- **图标**：手势、动物、货币符号、邮箱图形（各国信箱不同）、房屋轮廓、宗教符号都可能不成立；带文字的图标必须本地化（§2.5、§5 数字字形）。
- **图像里的人与场景**：本地化插图比纯翻译成本高，但首屏用错文化符号的代价更高；给译员/本地团队一份「可替换图层」清单。
- **数字字形**：Material 明确 Bengali、Marathi、Nepali 及部分阿拉伯语 locale 用不同数字形式；用 `Intl.Locale().numberingSystems` 取（§5.3），不要按 RTL 一刀切。
- **示例数据**：电话号码、邮编、地址、人名、车牌、身份证样例都要按 locale 换；中国手机号 11 位、验证码 6 位（见 `form-table.md`）不能当全球默认。
- **度量与时间制**：英里/公里、摄氏/华氏、12/24 小时制、周起始日（§8.2）都按 locale。
- **不要靠国旗表示语言**：语言 ≠ 国家（英语不只有英国、西班牙语不只有西班牙；中文涉及多个地区）。用语言名（本地化后的）或语言码 + `DisplayNames`。
- **合规与本地法规**：适老化/无障碍本地法规（如中国《无障碍环境建设法》、GB/T 37668，见 `accessibility.md`）与隐私同意 UI 也属 L10n 范围。

---

## 十六、给译者的交付规格：字符预算、变量说明、截图与术语表（与 `handoff-collaboration.md` 衔接）

翻译不是「把 JSON 发出去」。每条消息应带：

| 字段 | 内容 | 为什么 |
|---|---|---|
| `id` | 稳定唯一键 | 伪本地化定位、译文回填 |
| `message` | 完整单句（ICU MessageFormat） | 语序可调整（§7） |
| `description` / `context` | 这个字符串出现在哪、谁在什么时候看到 | 无上下文必然翻错（如 `Book` 名词/动词） |
| `variables` | 每个变量的**类型、示例值、是否人名/数字/日期** | 决定复数分支与格式化方式 |
| `charLimit` | 按 §2.3 分档给的**字符预算** | microcopy 给 2–3× 目标宽度对应的上限，段落给 1.3× |
| `pluralCategories` | **目标语言**的 CLDR 类别清单（§6.2） | 译员要补 `one/few/many` 分支 |
| `screenshot` | 该串在 LTR 与 RTL 两种界面中的截图 | 镜像与截断判断 |
| `glossary` | 术语表（见 `ux-writing.md` §10） | 同概念同词 |
| `doNotTranslate` | 品牌名、变量名、占位符、URL | 防止译者翻坏语法 |

**验收**：译文回填后立刻跑 §14 的三套伪 locale 对照 + §5 的 RTL 白黑名单 + §20 自检；不要等发布前一周才做。

---

## 十七、框架与工程落地：React / Vue / Next / MUI RTL、字体、能力检测

### 17.1 生态仓库（GitHub API 实测 2026-11-05，star / license / 最近推送）

| 仓库 | ★ | 许可 | pushed | 定位 |
|---|---|---|---|---|
| `vercel/next.js` | 143343 | MIT | 2026-11-05 | 框架级 i18n 路由 / locale 分发 |
| `mui/material-ui` | 99303 | MIT | 2026-11-05 | 组件级 RTL 支持（需 `direction: 'rtl'` + stylis 插件） |
| `formatjs/formatjs` | 14753 | NOASSERTION | 2026-11-05 | ICU MessageFormat + CLDR + ECMA-402（react-intl） |
| `i18next/i18next` | 8663 | MIT | 2026-11-04 | 通用 i18n 框架，生态最广 |
| `lingui/js-lingui` | 5934 | MIT | 2026-11-03 | ICU 消息目录 + 编译时提取 |
| `globalizejs/globalize` | 4835 | MIT | 2025-09-29 | CLDR 驱动格式化（**维护趋缓**，慎选新项目） |
| `unicode-org/icu` | 3637 | NOASSERTION | 2026-11-03 | ICU 本体，规则源头 |
| `intlify/vue-i18n` | 2711 | MIT | 2026-11-05 | Vue 生态消息与复数 |
| `projectfluent/fluent` | 1689 | Apache-2.0 | 2026-03-21 | Mozilla Fluent，非 ICU 的另一套消息模型 |
| `unicode-org/cldr` | 1170 | NOASSERTION | 2026-11-05 | CLDR 数据仓库（复数/日历/数字规则） |

> `NOASSERTION` 表示 GitHub API 的 `license.spdx_id` 未给出标准 SPDX 值（多为自定义/多许可/未标注），**不是「无许可」**；采用前须查仓库 LICENSE 原文。本表只记实测结果，不臆测。

### 17.2 落地纪律

- **字符串全部外置**，组件内不出现面向用户的字面量；数字/日期/复数不进消息目录，交给 `Intl`。
- **一个 locale 一个 Provider**，并在 `<html>` 同步 `lang` + `dir`（SSR 时服务端就要写对，避免 hydration 后跳变）。
- **能力检测**：`Intl.DurationFormat`、`Intl.Segmenter`、`View Transitions` 这类「文档已列但运行时可能没有」的 API 一律 `typeof` 检测 + 降级（§8.1 实测）。
- **字体**：为每种脚本准备回退栈；中文/日文/韩文/阿拉伯文/泰文/天城文不要共用一套行高与字重；CJK 子集化见 `performance-design.md`（CJK >10000 字形，不能整套打包）。
- **RTL 样式方案**：优先逻辑属性（§4）；若框架用 CSS-in-JS 的 RTL 转换器（stylis-plugin-rtl 等），要确认 `transform` / 阴影 / 渐变这些**物理值不会被自动处理**（§4.4）。
- **测试矩阵**：至少 `LTR-long`（en-US）、`LTR-CJK`（zh-CN）、`RTL`（ar-EG 或 he-IL）、`pseudo-accent`（en-XA）、`pseudo-bidi`（en-XB）五套，加 §14 的 200% microcopy。
- **CI 门禁**：查硬编码字符串、查 `left/right` 物理属性、查 `<html lang>` 与 `dir` 存在性、跑 §20 自检的自动化部分。

---

## 十八、12 个场景速查

| # | 场景 | 直接做法 |
|---|---|---|
| 1 | 按钮英译德后文字溢出 | §2.3 按 2–3× 弹性；改 `min/max-inline-size`，不设 nowrap；别缩写源文 |
| 2 | 表单标签在德文里被截断 | 标签改上下排布；标签列不给固定宽 |
| 3 | 中文界面加英文，需不需要 RTL | 不需要；但 `<span lang="en">` 与逻辑属性仍要给 |
| 4 | 要支持阿拉伯语 | `<html dir="rtl" lang="ar">` + §4 逻辑属性 + §5 白黑名单 + `dir="auto"` 给用户输入 |
| 5 | 阿语界面里 URL 被倒过来 | §3.5 用 `dir="ltr"` 紧包裹或 `<bdi>`；URL 属黑名单不镜像 |
| 6 | 「已删除 N 项」在俄语里语法不对 | §6/§7 ICU `plural`，按 CLDR 补 `one/few/many/other`，别手写 `n===1` |
| 7 | 日期 `03/09/2026` 被英美用户理解成不同日期 | §9 `Intl.DateTimeFormat` + 显式 `timeZone`，禁硬编码格式 |
| 8 | 德国用户输入 `1.234,50` 存成 1.234 | §10 按 locale 反解数字，不直接 `parseFloat` |
| 9 | 日历控件周末高亮错 | §8.2 按 `Intl.Locale().weekInfo` 取 firstDay/weekend |
| 10 | 姓名表单逼用户填姓 | §12 改单一 `Full name`，只按用途加字段 |
| 11 | 翻译还没回来，想先测出布局问题 | §14 伪翻译 + `en-XA`/`en-XB` + 200% microcopy |
| 12 | 图标里嵌了文字/数字 | §2.5 拆出文字层；§5.3 数字字形按 locale 换，顺序不镜像 |

---

## 十九、20 条反模式

1. 把「加个语言包」当成国际化全部工作（漏掉标记层、布局层、数据层）。
2. 用 **+40%** 给按钮/标签留余量（短串实测需要 200–300%，§2.3）。
3. 用固定 `width` + `white-space: nowrap` 装翻译文本。
4. 为了塞进布局而**缩写源语言文案**（`FAQ` 在很多语言里无法缩写，§2.4）。
5. 用字符数估算像素宽度（CJK 按 2 英文字符宽，`desktop→デスクトップ` 少一字更宽）。
6. 图标、banner、引导图里烧死文字。
7. 认为「中文更短」所以中文版可以塞更紧（W3C 明确中文是**特别容易膨胀的源语言**之一）。
8. 在 `body` 上写 `lang`，或用 `<meta http-equiv="Content-Language">` 声明页面语言。
9. 用 `lang` 推断方向、用语言码决定 RTL（阿塞拜疆语 `az` 可 LTR 可 RTL）。
10. 用 CSS `direction` 设 base direction（W3C 明令禁止；CSS 不可用时方向信息会丢）。
11. 把 `lang` 与 `dir` 混为一谈；或以为 `zh-Hans` 的 script subtag 能决定方向。
12. 全站硬编码 `margin-left` / `text-align: left` / `left: 0` / `translateX(20px)`。
13. 把**所有**图标一刀切镜像（时钟、刷新、放大镜、键盘、媒体播放、斜线都不镜像）。
14. 把**一般进度条**和**媒体进度条**用同一套镜像规则。
15. 数字按 RTL 一刀切换字形（`he-IL` 用 `latn`，`ar-EG` 用 `arab`）。
16. 拼接字符串生成句子；只把一小段句子包进 `plural`。
17. 复数只准备 `one` / `other` 两个分支；手写 `n % 10 === 1` 判断单数。
18. 在译文里写日期 pattern、货币符号、千分位、百分号。
19. 姓名表单强制 `first name` + `last name` + `family name` 必填，并限制字段长度、规范化大小写。
20. 等真翻译回来才做布局测试；或以为伪本地化能替代真译验证。

---

## 二十、20 项自检（出海交付前逐条过）

1. `<html>` 上有**正确且完整**的 `lang`（BCP 47 / IANA），不是 `body`、不是 meta？
2. 页面内其它语言片段用 `lang` 标出（WCAG 3.1.2 AA），例外四类核对过？
3. RTL 页面 `<html dir="rtl">` 存在；`dir` 由 markup 而非 CSS 提供？
4. 运行时/用户输入内容用 `dir="auto"` 或 `<bdi>`；表单需要时用 `dirname` 提交方向？
5. 所有 margin/padding/border/inset/size/对齐用逻辑属性？物理 `left/right` 都有「钉死在物理位置」的明确理由？
6. `transform` / `box-shadow` x 偏移 / 渐变方向 / 背景位置 / 轮播方向这些**不会被逻辑属性覆盖**的地方单独处理过？
7. §5 镜像白名单逐项过、黑名单逐项确认没被误伤？一般进度条与媒体进度条分开处理？
8. 数字仍按 LTR 排列，但字形按 `numberingSystems` 本地化？URL/品牌名未被倒置？
9. microcopy 按 **2–3×** 弹性、短文案 1.6–2.0×、段落 1.3× 验证过？flex/grid 子项设了 `min-inline-size: 0`？
10. 长复合词（德语）、宽字形（CJK）、高字形（泰文/阿拉伯文/天城文）三类都测过行高与溢出？
11. 每条消息是**完整单句**的 ICU MessageFormat，无拼接、无译员可见的日期/货币 pattern？
12. `plural` 分支按**目标语言** CLDR 类别补全且始终有 `other`；`select` 外层、`plural` 内层？
13. 撇号用 U+2019，ASCII `'` 只用于语法？`offset` 与 `#` 语义核对过？
14. 日期/时间/时区、数字/货币/单位、列表/相对时间/名称显示全部走 `Intl`，并显式传 locale 与 `timeZone`？
15. 日历的 `weekInfo`（周起始日/周末）、`hourCycle`、`calendars` 按 locale 取？
16. 排序用 `Intl.Collator`（含 `numeric:true` 判断）；中文分词/字数用 `Segmenter`？
17. 姓名为单一 `Full name`，未强制姓/名/title，未限制长度，允许空格连字符撇号，保留原大小写？UTF-8 全链路？
18. 伪本地化跑过 `en-XA` / `en-XB`（或 `qps-plocm`）+ **200% microcopy**；`^` 定界符成对、无字符串拼接、无未外置英文？
19. 五套测试矩阵（en-US / zh-CN / ar-EG / en-XA / en-XB）+ 320px 窄屏 + 200% 浏览器缩放都过？对照 `responsive-layout.md` §WCAG 1.4.10。
20. 新用到的 `Intl` API 做过**能力检测**（特别是 `Intl.DurationFormat`，本机 Node v22.22.2 实测未实现）？后端 locale 名是连字符而非下划线？

---

## 二十一、6 段可抄代码

### 21.1 文档骨架：`lang` + `dir` + 逻辑属性基线

```html
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
  <a class="back" href="/"><svg aria-hidden="true">…</svg> رجوع</a>
  <a class="ext" href="https://example.com" dir="ltr" lang="en">example.com/docs</a>
</body>
</html>
```

```css
:root { --gap: 8px; }
.back {
  display: inline-flex;
  align-items: center;
  gap: var(--gap);
  padding-inline: 12px;
  padding-block: 8px;
  text-align: start;
}
/* 只有「方向性」图标镜像；方向由 markup 的 dir 决定 */
[dir="rtl"] .back svg { transform: scaleX(-1); }
.card {
  inline-size: min(100%, 320px);
  min-inline-size: 0;
  border-inline-start: 3px solid var(--accent);
  margin-inline-start: var(--gap);
}
```

### 21.2 复数/选择：ICU MessageFormat（完整单句 + select 外层）

```js
// react-intl / formatjs 消息目录
const messages = {
  en: {
    inbox: '{count, plural, =0 {No new messages} one {# new message} other {# new messages}}',
    invite: `{gender, select,
      female {{n, plural, offset:1
        =0 {{host} is not giving a party.}
        =1 {{host} is inviting {guest} to her party.}
        other {{host} is inviting {guest} and # other people to her party.}}}
      other {{n, plural, offset:1
        =0 {{host} is not giving a party.}
        =1 {{host} is inviting {guest} to their party.}
        other {{host} is inviting {guest} and # other people to their party.}}}}`
  },
  // 阿语译文必须补 zero / two / few / many 分支（§6.2）
};
```

### 21.3 按 locale 安全的格式化封装（含能力检测）

```js
const hasDuration = typeof Intl.DurationFormat === 'function';

export const fmt = {
  number: (v, locale, opts) => new Intl.NumberFormat(locale, opts).format(v),
  money:  (v, locale, currency) =>
    new Intl.NumberFormat(locale, { style: 'currency', currency }).format(v),
  date:   (v, locale, opts = { dateStyle: 'medium', timeZone: 'UTC' }) =>
    new Intl.DateTimeFormat(locale, opts).format(v),
  list:   (arr, locale) => new Intl.ListFormat(locale, { type: 'conjunction' }).format(arr),
  plural: (n, locale) => new Intl.PluralRules(locale).select(n),
  duration: (d, locale) => hasDuration
    ? new Intl.DurationFormat(locale, { style: 'long' }).format(d)
    : fmt.list(Object.entries(d).map(([k, v]) => `${v} ${k}`), locale),
};
```

### 21.4 语言协商 + 周起始日 / 方向兜底校验

```js
// navigator.languages 是有序偏好列表，直接交给 Intl 协商
const locales = navigator.languages?.length ? navigator.languages : [navigator.language];
const resolved = new Intl.DateTimeFormat(locales, { localeMatcher: 'best fit' })
  .resolvedOptions().locale;                       // 例如 'zh-Hans-CN'
const L = new Intl.Locale(resolved);
const week = L.weekInfo;                          // { firstDay, weekend, minimalDays }
const cldrDirection = L.textInfo?.direction;      // 'rtl' | 'ltr'（仅用于校验）

// 只做一致性告警，绝不用来生成 dir（W3C：方向属于 markup）
if (cldrDirection && document.documentElement.dir &&
    cldrDirection !== document.documentElement.dir) {
  console.warn('[i18n] dir 与 CLDR 推断不一致，请人工确认', resolved);
}
```

### 21.5 伪本地化变换（含 200% microcopy 档）

```js
const ACCENTS = 'αäáàāāǎǎăăåå';
const pad = (s, ratio) => {
  const target = Math.ceil(s.length * ratio);
  const filler = 'αäáàāǎåВЖЗЙ中文ひらがना';
  return (s + filler.repeat(Math.ceil(target / filler.length) + 1)).slice(0, target);
};
function pseudo(str, { ratio = 1.4 } = {}) {
  // microcopy 走 3×，长段落走 1.3–1.4×（§2.3）
  const r = str.length <= 10 ? 3 : str.length > 70 ? 1.3 : ratio;
  const accented = str.replace(/[a]/g, () => ACCENTS[Math.floor(Math.random() * ACCENTS.length)])
                      .replace(/[1-9]/g, d => String.fromCharCode(0x2460 + Number(d) - 1));
  return `^${pad(accented, r)}^`;   // 定界符暴露截断与拼接
}
```

### 21.6 CI 静态检查：硬编码方向 / 物理属性 / 缺失 lang

```js
import fs from 'node:fs';
const files = process.argv.slice(2);
const RULES = [
  [/\bmargin-left\b|\bpadding-left\b|\btext-align:\s*left\b/, '物理左值 → 改用 *-inline-start / text-align:start'],
  [/\bdirection\s*:\s*rtl\b/, '不要用 CSS 设 base direction → 改 <html dir="rtl">'],
  [/<html(?![^>]*\slang=)/, '<html> 缺 lang（WCAG 3.1.1 Level A / H57）'],
  [/\b(0[1-9]|1[0-2])\/(0[1-9]|[12]\d|3[01])\/\d{4}\b/, '疑似硬编码日期 → Intl.DateTimeFormat'],
  [/\b(n|count)\s*===?\s*1\s*\?/, '疑似手写复数分支 → ICU plural / Intl.PluralRules'],
];
let bad = 0;
for (const f of files) {
  const t = fs.readFileSync(f, 'utf8');
  for (const [rx, msg] of RULES) if (rx.test(t)) { console.error(`${f}: ${msg}`); bad++; }
}
process.exit(bad ? 1 : 0);
```

---

## 二十二、数据来源（官方原文 + API 实测）

**W3C / WAI**

- W3C · Text size in translation（IBM 膨胀表 / Flickr 比例表 / 复合词·字宽·字高·缩写四因素）：https://www.w3.org/International/articles/article-text-size.en
- W3C · Declaring language in HTML（`html lang` / BCP 47 / IANA / meta 禁令 / CSS 不能声明语言 / `xml:lang`）：https://www.w3.org/International/questions/qa-html-language-declarations.en.html
- W3C · Structural markup and right-to-left text in HTML（`dir` 8 效果 / Never use CSS to apply the base direction / `dir=auto` / `dirname` / logical properties）：https://www.w3.org/International/questions/qa-html-dir.en.html
- W3C · Inline markup and bidirectional text in HTML（紧包裹 / `bdi` / `&rlm;`&`&lrm;` / U+2067·2066·2069·2068 / `bdo`）：https://www.w3.org/International/articles/inline-bidi-markup/
- W3C · Personal names around the world（单 Full name / 各文化姓名 / 长度与 UTF-8 / 排序与称呼）：https://www.w3.org/International/questions/qa-personal-names.en.html
- WAI · Understanding SC 3.1.1 Language of Page（Level A / H57 / 默认语言取最多）：https://www.w3.org/WAI/WCAG22/Understanding/language-of-page.html
- WAI · Understanding SC 3.1.2 Language of Parts（Level AA / H58 / passage 定义与例外）：https://www.w3.org/WAI/WCAG22/Understanding/language-of-parts.html
- WAI · H57 Using the language attribute on the HTML element：https://www.w3.org/WAI/WCAG22/Techniques/html/H57
- W3C · Language tags in HTML and XML（BCP 47 语法入门）：https://www.w3.org/International/articles/language-tags/

**Unicode / ICU / ECMA-402**

- Unicode CLDR · Plural Rules（六类别 / `one`≠1 / `other` required / Welsh 全 6 类 / 命名例外）：https://cldr.unicode.org/index/cldr-spec/plural-rules.html
- Unicode CLDR · Language Plural Rules chart（逐语言 cardinal 类别）：https://www.unicode.org/cldr/charts/latest/supplemental/language_plural_rules.html
- ICU User Guide · Formatting Messages（禁拼接 / complex arguments 外层 / select 外层 plural 内层 / `offset` 与 `#` / 撇号转义 / skeleton vs pattern / MF2）：https://unicode-org.github.io/icu/userguide/format_parse/messages/
- MDN · `Intl`（非构造器 / 10 构造器 + 2 静态方法 / `localeMatcher` lookup·best fit / `navigator.languages`）：https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl
- MDN · CSS logical properties and values（block/inline 轴 / start-end / 物理→逻辑映射 / 竖排）：https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_logical_properties_and_values
- CSS Logical Properties and Values Level 1 规范：https://drafts.csswg.org/css-logical/

**设计体系与工程方法**

- Material Design 2 · Bidirectionality（镜像白/黑名单 / 线性 vs 圆周时间 / 媒体播放不镜像 / 数字字形 / 48·72·20·12·16·56dp / 四平台支持）：https://m2.material.io/design/usability/bidirectionality.html
- Microsoft Learn · Pseudolocalization（伪翻译五变换 / +40% 启发式与 200%·400% 极端 / `^` 定界符 / `qps-ploc`·`qps-plocm`·`qps-ploca` / `en-XA`·`en-XB` / RFC 4646 qaa–qtz / `tk-TM` 撞车教训）：https://learn.microsoft.com/en-us/globalization/methodology/pseudolocalization
- FormatJS · ICU MessageFormat / CLDR / ECMA-402 集成（首页示例 `Intl.PluralRules('en').select(42)`）：https://formatjs.io/

**本机实测环境**

- Node.js **v22.22.2**：`Intl.PluralRules` 10 locale × 8 数值表、分数与 ordinal、`Intl.NumberFormat`（6 locale 数字 + EUR/JPY/unit）、`Intl.DateTimeFormat`（6 locale + 和历/伊斯兰历 + hourCycle）、`Intl.ListFormat`、`Intl.RelativeTimeFormat`、`Intl.DisplayNames`、`Intl.Segmenter`、`Intl.Collator`（de/sv + numeric）、`Intl.Locale`（textInfo/calendars/numberingSystems/weekInfo）、`Intl.supportedValuesOf`、`Intl.getCanonicalLocales`、localeMatcher 回退，以及 `Intl.DurationFormat` 未实现的 TypeError。
- GitHub REST API 实测 10 个仓库 star / license / pushed_at，日期 **2026-11-05**（见 §17.1）。

> 所有数值要么逐字来自上述官方页面，要么是本机 `node` 输出；没有引用二手博客的统计数字。W3C 膨胀表 51–70 档的非单调值按原文照录，未做平滑。
