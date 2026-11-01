# 响应式与断点体系 · Responsive Layout

> 快照 2026-11-01。数值全部取自官方文档原文（Ant Design Grid/布局规范、MUI Breakpoints、Tailwind 响应式、Bootstrap 5.3 Containers、Carbon 2x Grid、Material 3 Breakpoints、MDN Container Queries / clamp / length / Responsive images、W3C WCAG 2.2 SC 1.4.10），库的 star/许可经 GitHub API 实测。
> 用法：本文件解决「**在哪断、断了怎么变、变了给什么数值**」。视觉风格与元素构型不在这里（见 `patterns.md`），中文排版细节见 `chinese-design.md`，触控与对比度底线见 `accessibility.md`。

---

## 0. 先定策略，再谈数值

绝大多数"响应式做不好"不是断点值选错，而是**顺序错了**：先抄一套断点，再往里塞布局，于是每个断点都在打补丁。

正确顺序是三步，缺一步后面全是补丁：

1. **定策略**：这一屏的变化由**视口**决定，还是由**组件所在容器**决定？→ §1
2. **定断点**：断点加在"布局开始难看"的那一个宽度上，不是加在设备型号上 → §4
3. **定降级动作**：跨过断点时，到底是**露出、分割、缩放、移位**还是**换件**？五个动词选一个，不选就等于没设计 → §6

> **一句话立场**：断点是**结果**，不是**输入**。你说"移动端 375、桌面 1440"时，说的是测试宽度，不是断点。

---

## 1. 视口断点 vs 容器断点：先选对工具

| | 媒体查询 `@media` | 容器查询 `@container` |
|---|---|---|
| 依据 | 视口（浏览器窗口）宽度 | **最近一个声明了 `container-type` 的祖先**的宽度 |
| 适合 | 页面级骨架：导航形态、栅格列数、版心宽度、字号阶梯 | 可复用组件：卡片、列表项、统计块、表单区块 |
| 失效场景 | 同一张卡片放在主栏很宽、放在侧栏很窄——媒体查询给它同一套样式，必然一边难看 | 页面骨架用容器查询会很别扭（容器通常就是 body，绕了一圈等于媒体查询） |
| 浏览器支持 | 全绿 | Baseline 2023，现代浏览器全支持；老 Safari（<16）需 fallback |

**判断规则（照做）**：

- 变化的东西**跟着整页走** → 用 `@media`。
- 变化的东西**跟着自己被塞进多宽的格子走** → 用 `@container`。
- **同一个组件要在 2 种以上宽度里复用**（主栏/侧栏、列表/详情、卡片墙/单列）→ 必须用容器查询，否则你要为每种放置写一套覆盖样式。

**容器查询最小可用写法**：

```css
.card-slot { container-type: inline-size; container-name: card; }

@container card (min-width: 480px) {   /* 容器宽 ≥480px，不是视口 */
  .card { grid-template-columns: 120px 1fr; }
}
```

- `container-type: inline-size` 只对**行内轴**（横排文字的宽度）建立查询上下文，代价最小；`size` 会同时锁住高度，容易把自适应高度搞坏——**默认只用 `inline-size`**。
- 声明容器会引入**布局/尺寸包含**：容器的高度不再由内容撑开参与外部布局。给 `height: auto` 的卡片加 `container-type: size` 会出现塌陷，这是最常见的坑。
- 命名（`container-name`）只在**嵌套容器 ≥2 层**时才需要，否则最近的祖先就是你要的。
- 容器查询单位：`cqw` = 容器宽 1%、`cqh` = 容器高 1%、`cqi`/`cqb` = 行内/块轴 1%、`cqmin`/`cqmax` 取小/大者。**没有匹配容器时退化为 `sv*`（小视口单位）**，不会报错但会悄悄用错基准——排查时先确认容器真的生效了。
- 字号跟着容器缩放用 `cqi` 而非 `vw`：`font-size: clamp(14px, 4cqi, 20px)`。

---

## 2. 六大体系断点精确值对照

同一份设计换到不同技术栈就"断错位"，原因就是各家默认值不一样。**下表全部为官方默认值，可直接抄。**

### 2.1 Ant Design（中文中后台事实标准）

| 断点 | 值 | 语义 |
|---|---|---|
| `xs` | **< 576px** | 手机，也是默认（未匹配时生效） |
| `sm` | **≥ 576px** | 大手机 / 小横屏 |
| `md` | **≥ 768px** | 平板竖屏 |
| `lg` | **≥ 992px** | 平板横屏 / 小笔记本 |
| `xl` | **≥ 1200px** | 桌面 |
| `xxl` | **≥ 1600px** | 大屏 |
| `xxxl` | **≥ 1920px**（v6.3.0 新增） | 超大屏 |

- 栅格 **24 栏**，`gutter` 可为 `{xs:8, sm:16, md:24}` 分断点给值。
- Ant 的断点值遵循 **Bootstrap 4 媒体查询规则**（`sm` 从 576 起，与 Bootstrap 5 的 576 一致，但 Ant 多了 xxl/xxxl）。
- 可通过 `theme.token.screenXS…screenXXXL` 覆盖。

### 2.2 Material UI（React 生态默认）

| 断点 | 值 |
|---|---|
| `xs` | 0 |
| `sm` | 600 |
| `md` | 900 |
| `lg` | 1200 |
| `xl` | **1536** |

- `down(key)` 是**开区间**：`down('md')` = `[0, 900px)`，内部用 `step: 5` 生成 `max-width: 899.95px`。**这就是为什么不要自己手写 `max-width: 899px`**——差 1px 会漏掉 899.5 这类宽度。
- 自定义时**必须给全 5 个键**，否则报错。

### 2.3 Tailwind CSS v4（默认 rem，可换算）

| 前缀 | 最小宽度 | 媒体查询 |
|---|---|---|
| `sm` | 40rem = **640px** | `@media (width >= 40rem)` |
| `md` | 48rem = **768px** | `@media (width >= 48rem)` |
| `lg` | 64rem = **1024px** | `@media (width >= 64rem)` |
| `xl` | 80rem = **1280px** | `@media (width >= 80rem)` |
| `2xl` | 96rem = **1536px** | `@media (width >= 96rem)` |

- **`sm:` 不是"小屏"，是"从 sm 断点起"**。给手机写样式要用**不带前缀**的类。这是 Tailwind 最高频的误用。
- `max-*` 变体是**严格小于**：`max-lg` = `width < 64rem`。做区间用叠加：`md:max-xl:flex`。
- 断点单位统一用 `rem`，混用 `px` 会导致生成顺序错乱、互相覆盖。
- 容器查询尺寸默认 13 档：`@3xs` 256px → `@7xl` 1280px（`@sm` 384、`@md` 448、`@lg` 512、`@xl` 576、`@3xl` 768、`@5xl` 1024）。

### 2.4 Bootstrap 5.3（断点 + 版心一起看）

| 断点 | 最小宽度 | `.container` 的 `max-width` |
|---|---|---|
| xs | < 576px | **100%** |
| sm | ≥ 576px | **540px** |
| md | ≥ 768px | **720px** |
| lg | ≥ 992px | **960px** |
| xl | ≥ 1200px | **1140px** |
| xxl | ≥ 1400px | **1320px** |

**这张表的第二列比第一列更有用**：它给出了一套经过验证的「版心宽度阶梯」——视口变宽时，内容区不是无限拉伸，而是**跳到下一个固定版心**。自己做站时直接抄这一列。

### 2.5 IBM Carbon 2x Grid（列数会变的那一派）

| 断点 | 值 | 列数 | 单列宽 | 内边距 | 外边距 |
|---|---|---|---|---|---|
| Small | **320px** (20rem) | **4** | 25% (80px) | 16px | **0** |
| Medium | **672px** (42rem) | **8** | 12.5% (80px) | 16px | 16px |
| Large | **1056px** (66rem) | **16** | 6.25% (64px) | 16px | 16px |
| X-Large | **1312px** (82rem) | **16** | 6.25% (80px) | 16px | 16px |
| Max | **1584px** (99rem) | **16** | 6.25% (96px) | 16px | **24px** |

- 基础单位是 **8px mini unit**，列宽/行高/间距/内外边距都是它的倍数。
- **列数在断点处翻倍（4→8→16），之后不再增加**——不是无限加列，而是列变宽。这是与 12/24 栅格最大的思路差异：**Carbon 让内容变大，Ant/Bootstrap 让列变多**。
- 内边距恒为 **16px**；外边距 0/16/16/16/24。Small 断点外边距为 0 是因为 320px 上每 1px 都金贵。
- 图文对齐铁律：**文字压在 padding 内侧，不压到 padding 上**。

### 2.6 Material 3（dp，跨 Android/Web）

| 断点 | 宽度 | 典型设备 | 建议分栏数 | 导航形态 |
|---|---|---|---|---|
| Compact | **< 600dp** | 手机竖屏 | **1** | 底部导航栏 / 全屏对话框 |
| Medium | **600–839dp** | 平板竖屏、折叠屏展开竖屏 | 1（推荐）或 2 | 折叠导航栏（rail） |
| Expanded | **840–1199dp** | 手机横屏、平板横屏、桌面 | **2** | 折叠 rail / 标准展开 rail |
| Large | **1200–1599dp** | 桌面 | **2** | 标准展开 rail |
| Extra-large | **≥ 1600dp** | 桌面、超宽屏 | **2–3** | 标准展开 rail |

- 只有 Medium 允许"低密度内容"用两栏；**高信息密度在 Medium 用两栏会降低可用性**。
- 行长约束：**任何断点都保持 40–60 字符/行**（中文对应 25–40 字/行，见 `chinese-design.md`）。宽度增加应该拿去加栏、加图、加留白，不是拉长一行字。
- M3 2025 起把"window size class"正式改称 **breakpoint**，值不变，概念从"设备分类"变成"窗口需要变形的尺寸点"。

### 2.7 一页对照速查

| 语义档 | Ant | MUI | Tailwind | Bootstrap | Carbon | M3 |
|---|---|---|---|---|---|---|
| 手机 | <576 | 0 | — | <576 | 320 | <600 |
| 大手机/小平板 | 576 | 600 | 640 | 576 | — | — |
| 平板竖 | 768 | 900 | 768 | 768 | 672 | 600 |
| 平板横/小笔记本 | 992 | — | 1024 | 992 | 1056 | 840 |
| 桌面 | 1200 | 1200 | 1280 | 1200 | 1312 | 1200 |
| 大屏 | 1600 | 1536 | 1536 | 1400 | 1584 | 1600 |

**读法**：六个体系在同一语义档上最大差 **96px**（平板竖：768 vs 672 vs 600）。所以"抄哪家"不重要，**一套用到底**才重要。混用会出现"某个宽度下两套规则同时生效"的双断点 bug。

---

## 3. 断点该定在哪：内容断，不是设备断

### 3.1 定断点的唯一正确方法

1. 在浏览器里把窗口**从 320px 连续拖到 1920px**，不要跳着看。
2. 找出**布局第一次开始难看**的宽度（换行断裂、文字被挤成 1 个字、卡片比例失衡、按钮被压扁）。
3. 这个宽度 **+1~8px** 就是你的断点。
4. 继续拖，找下一个。

**判断"难看"的三条硬指标**（比审美更可靠）：

- 正文行宽 **< 20 字**（中文）或 **< 40 字符**（英文）→ 该合并栏了
- 正文行宽 **> 45 字**（中文）或 **> 75 字符**（英文）→ 该拆栏或加版心
- 任何元素被挤到 **< 其内容的 min-content** → 该降级了

### 3.2 建议默认（无特殊理由时直接用这套）

| 档 | 值 | 用途 |
|---|---|---|
| 最小支持 | **320px** | WCAG 1.4.10 硬要求，不是"尽量" |
| 手机 | **375 / 390** | 设计稿主档（iPhone 主流逻辑宽） |
| 平板竖 | **768** | 单栏→双栏切换点 |
| 小笔记本 | **1024** | 双栏→三栏、侧栏常驻 |
| 桌面设计画板 | **1440** | 中后台画板标准（Ant 官方统一 1440） |
| 大屏 | **1920** | 加留白、加第四栏，不加行长 |

**只有 3 档也能做出好响应式**：`< 768` 单栏 / `768–1199` 双栏 / `≥1200` 三栏 + 固定侧栏。断点数量不是质量指标，**每档的变化是否说得清**才是。

### 3.3 移动优先还是桌面优先

| | 移动优先（`min-width` 递进） | 桌面优先（`max-width` 递进） |
|---|---|---|
| 默认样式 | 手机 | 桌面 |
| 适合 | C 端、落地页、内容站、绝大多数项目 | **中后台**：主用户就是大屏，且表格/图表在小屏无法真正可用 |
| 代价 | 大屏要不断"加"东西，容易加出堆砌 | 小屏要不断"删"东西，容易删漏关键操作 |

**中后台可以正大光明用桌面优先**，但必须同时满足：① 明确声明"移动端仅支持查看，不支持编辑"；② 320px 下**仍不出现横向滚动**（WCAG 1.4.10 不看你是不是中后台）。做不到就退回移动优先。

**无论哪一派，`@media` 只写一种方向**。同一份 CSS 里 `min-width` 与 `max-width` 混着写，覆盖顺序会变成玄学。

---

## 4. 跨断点做什么：五个动词

M3 的框架最实用——跨断点时只有五种合法动作，**每种都要说得出为什么**。这比"这里改成两栏"具体得多。

| 动词 | 含义 | 典型例子 | 反面 |
|---|---|---|---|
| **露出 Reveal** | 小屏藏起来的，大屏默认打开 | 折叠导航栏 → 展开导航栏；侧栏筛选器大屏常驻 | 大屏只是把同样的东西**放大**，多出来的空间全浪费 |
| **分割 Divide** | 一栏变两栏 / 三栏 | 邮件列表 + 阅读区；列表 + 详情 | Medium 高密度内容硬拆两栏 |
| **缩放 Resize** | 元素本身变大，结构不变 | 卡片从竖版变横版；图片占比提高；字号上台阶 | 无脑 `width: 100%` 把卡片拉成横幅 |
| **移位 Reposition** | 元素换位置 | 底部操作栏 → 右侧操作区；FAB 从右下 → 导航栏内 | 移位后找不到（违反一致性预期） |
| **换件 Swap** | 换成功能等价但形态不同的组件 | 底部 tab bar → 导航 rail；全屏对话框 → 普通对话框；表格 → 卡片列表 | **换成功能不等价的**（按钮换 chip、列表换卡片）→ 用户认知断裂 |

**换件的三条纪律**（M3 明确警告）：

1. 两个组件必须**功能等价**——能完成同一件事。
2. 换件必须服务于**功能或人体工学**（拇指可达、鼠标精度），不是"看起来更丰富"。
3. 换件后**信息不能丢**。底部 tab 5 项换成 rail 还是 5 项，不能悄悄少 2 项。

**写设计说明时的模板**（一句话说清一个断点）：

> `≥1024px`：**露出**常驻侧栏（208px）+ **分割**为列表/详情两栏；`<1024px`：**换件**为抽屉式侧栏，列表全宽。

---

## 5. 栅格与版心：三个必须给的数值

### 5.1 栏数

| 体系 | 栏数 | 断点处是否变 |
|---|---|---|
| Ant Design | **24** | 不变 |
| Bootstrap | **12** | 不变 |
| Carbon | 4 → 8 → **16** | **变**（320/672/1056） |
| Tailwind | 12（`grid-cols-12`，自定义） | 不变 |

**24 栏的理由**：能被 2/3/4/6/8/12 整除，中文中后台四等分（6 栏）、三等分（8 栏）、二等分（12 栏）都落在整数栏上。**12 栏分不出 5 等分**（2.4 栏）。做五列布局时 24 栏更省事。

### 5.2 Gutter 与 Column 谁固定

**铁律：Gutter 固定，Column 流体。**

- Ant 原文：浏览器扩大或缩小时，**Column 宽度随之变化，Gutter 宽度固定**。
- 反面：`gutter` 也用百分比 → 大屏间距被拉到 48px，视觉松散；小屏间距压到 4px，元素粘连。
- 推荐 gutter：**16px（紧凑）/ 24px（常规）/ 32px（宽松）**，与 8 倍数体系一致；分断点给值 `{xs:8, sm:16, md:24}`。

### 5.3 版心（container max-width）

直接抄 Bootstrap 阶梯，或按内容定：

| 内容类型 | 版心宽 | 理由 |
|---|---|---|
| 长文阅读（博客/文档） | **680–760px** | 中文 25–40 字/行，超出即难读 |
| 营销落地页 | **1140–1280px** | 容纳 3–4 列卡片 + 大留白 |
| 中后台内容区 | **不限宽**，随视口伸缩 | 数据密度优先；靠栏数与 gutter 控制节奏 |
| 表单页 | **≤ 640px**（单列） | 单列表单超过 640px 就是浪费眼球移动距离 |
| 定价/对比表 | **960–1140px** | 3–4 列并列的最小舒适宽度 |

**版心与断点的关系**：版心到顶后，**多出来的宽度分给留白**，不再分给内容。这一步不做，1920 屏上就会出现 1600px 宽的一行正文——这是"响应式做了但很业余"的头号特征。

---

## 6. 流式排版：clamp() 的正确用法

### 6.1 公式

```css
/* clamp(最小值, 首选值, 最大值) */
h1 { font-size: clamp(28px, 4vw, 48px); }
```

- 解析规则：`clamp(MIN, VAL, MAX)` = `max(MIN, min(VAL, MAX))`。**若 MIN > MAX，MIN 胜出**（不报错，静默取 MIN）——手滑写反了会得到一个永远不变的字号。
- `+` 和 `-` 两侧**必须有空格**，否则整条声明失效。
- 可用 `rem` 与 `vw` 混算：`clamp(1.5rem, 1rem + 2vw, 2.5rem)`——这种"固定值 + 视口增量"的写法比纯 `vw` 更可控，因为字号下限由 rem 锚定，用户改浏览器字号时能跟着变。

### 6.2 无障碍硬要求（MDN 明确）

> 用 `clamp()` 控制字号时，**最大值必须是相对单位，且不小于最小值的 2 倍**。

原因：WCAG 1.4.4 要求文字能放大到 **200%**。如果 `clamp(16px, …, 20px)`，最大值只有 1.25 倍，用户放大后视觉字号几乎不变 → 失败。

**可抄的两行**：

```css
body { font-size: clamp(1rem, 0.95rem + 0.25vw, 1.125rem); }  /* 16→18px，max=1.125rem 需配合根字号缩放 */
h1   { font-size: clamp(1.75rem, 1.2rem + 2.2vw, 3rem); }      /* 28→48px，3rem ≥ 2×1.75rem ✅ */
```

### 6.3 中文流式排版的三个额外约束

1. **行高不跟着字号线性缩**。中文行高在小字号需要更大比例：14px 用 **1.7**，18px 用 **1.6**，32px+ 用 **1.4**。写成 `line-height: clamp(1.4, 1.8 - 0.01vw, 1.75)` 意义不大——**按字号档位分别给值更可靠**。
2. **行长用 `max-width` 按字数卡，不用百分比**。中文正文 `max-width: 38em`（约 38 字），移动端 `max-width: 22em`。
3. **不要给中文标题用 `letter-spacing` 的流式值**。中文不需要 tracking，负 letter-spacing 会让笔画粘连（`-0.02em` 在 14px 上就开始糊）。

### 6.4 字号阶梯在各断点的取值（建议）

| 角色 | 320–767 | 768–1199 | ≥1200 |
|---|---|---|---|
| 正文 | 16px / 1.7 | 16px / 1.7 | 17–18px / 1.65 |
| 辅助文字 | 13px | 13px | 14px |
| H3 | 18px | 20px | 22px |
| H2 | 22px | 26px | 30px |
| H1 | 28px | 34px | 40–48px |
| 展示数字（KPI） | 28px | 32px | 36–44px |

**只允许 5–6 档**。每多一档，团队就多一个"这个标题该用 26 还是 28"的争论。

---

## 7. 视口单位：`100vh` 是个陷阱

| 单位 | 基准 | 稳定性 | 用在 |
|---|---|---|---|
| `vh` / `vw` | 大视口（当前实现 = `lvh`/`lvw`） | 稳定 | 宽度类布局；**不要用它做全屏高度** |
| `svh` / `svw` | 浏览器 UI **全部展开**时的最小视口 | 稳定 | 内容绝不能被遮挡：底部按钮区、关键操作 |
| `lvh` / `lvw` | 浏览器 UI 收起时的最大视口 | 稳定 | 追求铺满：首屏大图、背景横幅（接受可能被遮挡） |
| `dvh` / `dvw` | 实时可见视口，随地址栏伸缩变化 | **不稳定** | 精确贴合当前屏幕：全屏遮罩、登录页 |
| `dvi` / `dvb` / `cqi` / `cqb` | 逻辑轴（行内/块） | 稳定 | 多语言/竖排场景 |

**关键事实**：`vh` 当前**等同于 `lvh`**，也就是说 `height: 100vh` 在手机上是"地址栏收起时的高度"。地址栏一展开，底部内容被遮住 —— 这是移动端 H5 最常见的 bug。

**照做**：

```css
.hero      { min-height: 100svh; }              /* 首屏，绝不遮挡 */
.overlay   { height: 100dvh; }                  /* 全屏遮罩，精确贴合 */
.bottom-bar{ padding-bottom: max(12px, env(safe-area-inset-bottom)); }
```

- 底部固定栏**必须**配 `env(safe-area-inset-bottom)`，否则 iPhone 上会被小白条压住。
- `dvh` 不要用在大面积、会随滚动反复重排的元素上——尺寸不稳定会引起抖动和掉帧。
- `vw` **包含滚动条宽度**，`width: 100vw` 会造出横向滚动条。要满宽用 `width: 100%`。

---

## 8. 响应式图片：三条规则 + 一个防抖

### 8.1 分辨率切换（同一图，不同大小）

```html
<img
  src="photo-800.jpg"
  srcset="photo-480.jpg 480w, photo-800.jpg 800w, photo-1600.jpg 1600w"
  sizes="(width <= 600px) 480px, (width <= 1200px) 800px, 1200px"
  width="1600" height="1067"
  alt="描述">
```

规则（全部来自 MDN，逐条都是硬要求）：

1. **`w` 描述符写图片固有宽度**（`480w`，不是 `480px`）。
2. `sizes` 里**媒体条件必须从窄到宽排序**——浏览器**只匹配第一个为真的条件**，后面全部忽略。
3. `sizes` **最后一项不带媒体条件**，作为兜底。
4. 槽位宽可用任意 CSS 长度（`480px`、`50vw`），**不能用百分比**。
5. 浏览器选择逻辑：命中条件 → 得到槽位宽 → 选**固有宽最接近或第一个更大的**图。

### 8.2 固定尺寸、多倍屏（logo / 头像 / 图标）

```html
<img src="logo-320.png" srcset="logo-320.png, logo-640.png 2x" width="320" height="80" alt="Logo">
```

**用 `x` 描述符时不写 `sizes`**。`1x` 可省略。

### 8.3 艺术指导（不同构图，不只是不同大小）

```html
<picture>
  <source media="(width < 800px)" srcset="hero-portrait.jpg">
  <source media="(width >= 800px)" srcset="hero-landscape.jpg">
  <img src="hero-landscape.jpg" alt="描述">
</picture>
```

- 必须保留最后的 `<img src alt>` 作为兜底。
- **`media` 只用于艺术指导**；用了 `media` 就不要再在 `sizes` 里写媒体条件。
- 为什么不能 JS 换图：浏览器在解析 CSS/JS **之前**就开始预加载图片，JS 换图 = 先下大图再下小图，双倍流量。

### 8.4 防布局偏移（CLS）

- **永远写 `width` / `height` 属性**。它们只用来确定**宽高比**，不必等于实际渲染尺寸。
- 配 CSS：`img { max-width: 100%; height: auto; }`。
- 艺术指导切换不同比例图时，给容器预设 `aspect-ratio`（桌面 16/9，移动 4/5）+ `object-fit: cover`。
- 首屏外图片加 `loading="lazy"`；**首屏首图不要 lazy**（会推迟 LCP）。装饰图 `alt=""`。

---

## 9. 表格在窄屏的降级（移动端表格 / 手机表格 / 表格变卡片）：四种策略

表格是响应式最难的一环，因为**它天然是二维的**。四种策略各有明确适用条件，选错就白做。

### 9.1 策略对照

| 策略 | 做法 | 适用条件 | 代价 |
|---|---|---|---|
| **A. 横滚容器** | 表格外包 `overflow-x: auto`，保留全部列 | 列 ≥5 且**列间需要横向对比**（对账、报表、排期） | 需配**粘性首列**，否则滑到右边不知道在看哪行 |
| **B. 减列** | 小屏隐藏次要列（`display: none` 或组件级 `responsive`） | 有明确的"主列 3 个 + 次列 N 个" | 信息丢失，必须有"查看详情"出口 |
| **C. 卡片化** | 每行变一张卡，表头变字段名（`<dl>` 或 label + value） | 列 ≤4、**每行是独立实体**（订单、成员、任务） | **失去横向对比能力**——这是不可逆的损失 |
| **D. 主从** | 列表只显示 2–3 个关键字段，点击进详情 | 数据行多、字段多、需要逐条处理 | 多一次点击；必须有返回与位置保持 |

### 9.2 决策规则（按顺序问）

1. **用户在小屏上需要"横向比较同一字段的多行值"吗？**（比价、对账、看谁最高）→ 是 → **A**（横滚 + 粘性首列），不要卡片化。
2. 否则列 ≤4 且每行独立 → **C**。
3. 否则有清晰主次 → **B**（隐藏次要列，保留详情入口）。
4. 否则 → **D**。

**禁止**：把 8 列表格卡片化。8 个字段竖排的卡片，一屏只能看 1 张，比横滚难用 10 倍。卡片化只解决"少列表格"，不解决"宽表格"。

### 9.3 WCAG 1.4.10 的例外边界（常被误读）

原文允许「需要二维布局才能使用或表达含义的部分」例外，明确举例包含 **data tables（但不含单独单元格）**。但有三个边界：

1. **例外只覆盖那一段内容**，不自动延伸到其他内容。
2. **表格内的单元格仍要满足 Reflow**（除非单元格自身需要二维布局）。
3. **表格的标题、搜索框、分页不在例外内**——它们必须正常回流。

→ 所以正确做法是：**只把 `<table>` 包进横滚容器，标题/工具栏/分页留在外面正常回流**。把整页包进横滚容器是明确失败（W3C Figure 13 左图即 Fail）。

### 9.4 可抄骨架

```html
<div class="table-wrap">           <!-- 只包表格 -->
  <table>…</table>
</div>
```
```css
.table-wrap { overflow-x: auto; -webkit-overflow-scrolling: touch; }
.table-wrap table { min-width: 720px; }        /* 低于此宽则横滚 */
.table-wrap th:first-child,
.table-wrap td:first-child {                    /* 粘性首列 */
  position: sticky; left: 0; background: var(--bg);
  box-shadow: 1px 0 0 var(--border);
}
```

- 横滚容器要有**可见提示**（右侧渐隐遮罩或"← 左右滑动 →"），否则用户不知道右边还有内容。
- 粘性首列背景**必须是不透明色**，否则会透出滚动内容。

---

## 10. 表单在窄屏

| 项 | 窄屏（<768） | 宽屏 |
|---|---|---|
| 列数 | **1 列**（无条件） | ≤6 字段 1 列；≥7 字段可 2 列（同一区域内禁多列） |
| 标签 | **顶对齐** | 顶对齐或右对齐（见 `form-table.md` §2） |
| 字段宽度 | **100%**（但保留 `max-width` 防拉成超宽条） | 按内容定宽（验证码 130 / 手机号 160 / 身份证 240） |
| 按钮 | **全宽或粘底** | 与输入框左对齐 |
| 键盘 | `inputmode="numeric"` / `tel` / `email`，`autocomplete` 齐 | 同 |

- **粘底提交栏**：`position: sticky; bottom: 0` + `padding-bottom: env(safe-area-inset-bottom)`。移动端长表单没有粘底按钮，用户会滚到顶部找"提交"。
- **禁止 `user-scalable=no`**：`<meta name="viewport" content="width=device-width, initial-scale=1">` 就够。禁用缩放违反 WCAG 1.4.4，且 iOS 输入框聚焦时会自动放大页面（字号 <16px 时）——把输入框字号设 **≥16px** 才是正解。
- 分步表单在窄屏把步骤条改为**纯文字"第 2 步，共 4 步"**，横向步骤条在 320px 上必然挤成一团。

---

## 11. 导航降级：一条标准路径

| 断点 | 形态 | 关键数值 |
|---|---|---|
| < 768 | 顶部 logo + 汉堡 → 全屏抽屉；或**底部 tab（≤5 项）** | tab 高 56px + safe-area；图标 24px + 文字 10–12px |
| 768–1023 | 顶部导航，菜单项 ≤6；侧栏折叠为图标条 | 折叠侧栏 **64px**，展开 **208–240px** |
| ≥ 1024 | 常驻侧栏 + 顶部工具条 | 侧栏 208–240px；内容区最小 **≥ 720px** |

- **底部 tab 只放 ≤5 项**，超过就用"更多"。M3 与 iOS 都是这个上限。
- 折叠/展开侧栏的图标条宽度 **64px**（Ant 中后台实测值），不是 48 也不是 80——48 放不下 24px 图标 + 左右各 20px 热区，80 又浪费。
- 汉堡菜单里**必须能到所有一级入口**，不能藏"设置"这种高频项。
- 换件纪律见 §4：底部 tab ↔ 导航 rail ↔ 侧栏，三项数一致。

---

## 12. 中后台适配（中文场景专用）

Ant Design 布局规范给了明确口径，直接采用：

**画板与主流分辨率**

- 统一画板宽 **1440px**（组织内统一，减少沟通成本）。
- 用户主流分辨率：**1920 / 1440 / 1366**，少量 **1280**。→ 意味着 **1366 是必须测的宽度**，1280 是必须不崩的宽度。

**两种适配方案**

| 方案 | 做法 | 用在哪 |
|---|---|---|
| **左右布局** | 左侧导航**固定宽**，右侧工作区**动态缩放** | 侧栏导航的中后台（最常见） |
| **上下布局** | 两侧留白设**最小值**，留白到达下限后，中间主内容区才动态缩放 | 顶栏导航、内容居中型页面 |

**关键数值**

- 网格基数 **8**；24 栅格；**gutter 固定、column 流体**。
- 侧栏：展开 208–240px / 折叠 64px；内容区**最小可用宽 ≥ 720px**（低于此表格无法用）。
- 表格 `min-width`：**720px**（6 列以内）/ **960px**（8 列以上）。低于就横滚，不要卡片化（§9）。
- 1366 宽下：侧栏 208 + 内容 1158，去掉左右 24 padding 后剩 1110 → **能放 6 列常规表格**。这是"1366 到底能塞几列"的答案。

**三个高频错误**

1. 侧栏用百分比 → 1920 上侧栏 380px，一眼浪费。**侧栏必须固定 px**。
2. 内容区不设最小宽 → 1024 上表格被压成每条 8 个字。**设 `min-width` + 外层横滚**。
3. 画板 1440 却只测 1440 → 1366 上按钮换行、1280 上表头错位。**验收必须过 1280 / 1366 / 1440 / 1920 四档**。

---

## 13. 触控与鼠标：两套输入不能共用一套假设

| | 鼠标 | 触控 |
|---|---|---|
| 目标尺寸 | 24×24（WCAG 2.5.8 下限） | **44×44**（iOS/WCAG 2.5.5 AAA） |
| hover | 可用 | **不可用**（hover 在触屏上表现为"第一次点击"） |
| 精度 | 高，可点 1px 边框 | 低，需 ≥8px 间距避免误触 |
| 缩放 | Ctrl+滚轮 | 双指缩放（**不能禁用**） |

**照做**：

```css
@media (hover: hover) and (pointer: fine) {
  .card:hover { transform: translateY(-2px); }   /* 只在真 hover 设备生效 */
}
@media (pointer: coarse) {
  .btn { min-height: 44px; min-width: 44px; }
}
```

- **所有靠 hover 才出现的内容（下拉菜单、操作按钮、Tooltip）必须另有触屏路径**：点击展开、长按、或直接常驻。`@media (hover: none)` 下把 `opacity: 0` 的操作按钮改成 `opacity: 1`。
- **触控目标之间留 8px 空隙**，比把图标画大更有效。
- **不要禁用双击缩放**（`user-scalable=no` / `touch-action: manipulation` 全站滥用），会让低视力用户无法放大。

---

## 14. 调试与验收

### 14.1 必测宽度（8 档）

**320 / 375 / 414 / 768 / 1024 / 1280 / 1366 / 1440 / 1920**

320 是 WCAG 下限，375/414 是主流手机，768 是平板，1024 是 iPad 横屏/小笔记本，1280/1366 是"最容易崩"的两档（比设计稿窄但比平板宽），1440 是画板，1920 是大屏。

### 14.2 每档检查 6 件事

1. **有没有横向滚动条**（`document.documentElement.scrollWidth > clientWidth`）→ 有就是 bug，除非是 §9 允许的表格容器。
2. 正文行宽是否在 **25–40 字**之间。
3. 有没有元素被压到 **< min-content**（文字变竖排、按钮变方块）。
4. 触控目标是否 **≥44px**（DevTools 有 "Show rulers"/检查 computed 尺寸）。
5. 图片是否变形/裁掉主体（`object-fit` 是否设了）。
6. 首屏是否有内容被遮（`100vh` 陷阱，§7）。

### 14.3 缩放进阶测试（无障碍必做）

- **200% 缩放**（Cmd/Ctrl + `+` 到 200%）：文字是否可读、是否截断（WCAG 1.4.4）。
- **400% 缩放 / 320px 宽**：是否只剩一个方向滚动（WCAG 1.4.10）。
- **浏览器默认字号改到 20px**：所有 `px` 字号是否跟着不动（应当用 `rem`）→ 不跟 = 用 `px` 写死了。

### 14.4 一条命令自查横向溢出

```js
// 粘到 Console，返回造成横向溢出的元素
[...document.querySelectorAll('*')]
  .filter(el => el.getBoundingClientRect().right > document.documentElement.clientWidth + 1)
  .slice(0, 20)
  .forEach(el => console.log(el, el.getBoundingClientRect().width));
```

---

## 15. 反模式 20 条

1. 先抄断点再设计布局（顺序反了）。
2. 同一份 CSS 里 `min-width` 与 `max-width` 混用。
3. 断点值混用两套体系（Ant 576 + Tailwind 640 同时存在 → 双断点区间）。
4. 用设备型号命名断点（`iphone14`），换机即失效。
5. 只有 2 档断点却声称"全响应式"（手机 / 桌面，平板直接崩）。
6. `height: 100vh` 做全屏（地址栏遮挡底部，§7）。
7. `width: 100vw` 做满宽（含滚动条宽，造出横向滚动）。
8. gutter 用百分比（大屏松、小屏挤）。
9. 版心到顶后还继续拉宽内容（1920 上一行 1600px 正文）。
10. 大屏只是把小屏放大（漏掉 §4 的"露出/分割"）。
11. 8 列表格卡片化（一屏一张卡，比横滚难用）。
12. 整页包进横滚容器（WCAG 1.4.10 明确 Fail）。
13. 横滚表格不设粘性首列（滑到右边不知看哪行）。
14. 粘性列背景半透明（内容透出来）。
15. 禁用 `user-scalable`（违反 1.4.4，低视力用户无法放大）。
16. 输入框字号 <16px（iOS 聚焦自动放大页面）。
17. 靠 hover 才显示的操作按钮，触屏上永远看不到。
18. `clamp()` 最大值 < 最小值（静默取 MIN，字号永远不变）。
19. `clamp()` 最大值不到最小值 2 倍（放大 200% 失效）。
20. 只测设计稿宽度（1440）就交付。

---

## 16. 自检 15 项（有响应式要求时逐条过）

1. 断点数量 **≤5**，且每个断点都能说出一句"这个宽度下什么变了"？
2. 断点值来自**同一套体系**（不混用）？
3. 320px 下**无横向滚动**（除允许的表格容器）？
4. 400% 缩放 / 320px 下只有**一个方向**滚动（1.4.10）？
5. 200% 缩放文字可读不截断（1.4.4）？
6. 正文行宽在 **25–40 字**（中文）/ 40–75 字符（英文）？
7. 版心到顶后**多出的宽度给了留白**，没有给内容？
8. 栅格 **gutter 固定、column 流体**？
9. 跨断点变化能归到**五个动词之一**（露出/分割/缩放/移位/换件）？
10. 换件前后**功能等价、信息不丢**？
11. 全屏高度用 `svh`/`dvh` 而非 `vh`；底部栏有 `safe-area-inset`？
12. 图片有 `width`/`height` + `max-width:100%`，首屏图未 lazy？
13. 表格窄屏策略是**四选一**且有理由（不是默认卡片化）？
14. 触屏目标 **≥44px**，hover 内容有触屏路径？
15. 过完 **320/375/768/1024/1366/1440/1920** 七档？（中后台再加 1280）

---

## 17. 可抄代码

### 17.1 媒体查询骨架（移动优先）

```css
/* 基础：手机，无前缀 */
.page { padding: 16px; }
.grid { display: grid; gap: 16px; grid-template-columns: 1fr; }

@media (min-width: 768px)  { .grid { grid-template-columns: repeat(2, 1fr); gap: 24px; } }
@media (min-width: 1024px) { .page { padding: 24px 32px; } .grid { grid-template-columns: repeat(3, 1fr); } }
@media (min-width: 1440px) { .page { max-width: 1280px; margin-inline: auto; } }
```

### 17.2 容器查询卡片（同一组件两种宽度）

```css
.card-slot { container-type: inline-size; }

.card { display: grid; gap: 12px; grid-template-columns: 1fr; }

@container (min-width: 480px) {
  .card { grid-template-columns: 120px 1fr; align-items: start; }
}
@container (min-width: 720px) {
  .card { grid-template-columns: 160px 1fr auto; }
}
```

### 17.3 流式字号（无障碍合规）

```css
:root {
  --fs-body: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);   /* 16→18 */
  --fs-h3:   clamp(1.125rem, 1rem + 0.6vw, 1.375rem);   /* 18→22 */
  --fs-h2:   clamp(1.375rem, 1.15rem + 1.1vw, 1.875rem);/* 22→30 */
  --fs-h1:   clamp(1.75rem, 1.2rem + 2.2vw, 3rem);      /* 28→48，max = 1.71× min ✅ */
}
body { font-size: var(--fs-body); line-height: 1.7; max-width: 38em; }
```

### 17.4 响应式表格（横滚 + 粘性首列 + 提示）

```css
.table-wrap {
  overflow-x: auto;
  overscroll-behavior-x: contain;
  background:
    linear-gradient(to right, var(--bg) 30%, transparent) left / 32px 100% no-repeat,
    linear-gradient(to left,  var(--bg) 30%, transparent) right / 32px 100% no-repeat;
}
.table-wrap table { min-width: 720px; border-collapse: collapse; }
.table-wrap thead th:first-child,
.table-wrap tbody td:first-child {
  position: sticky; left: 0; z-index: 1;
  background: var(--bg);                    /* 必须不透明 */
  box-shadow: 1px 0 0 var(--border);
}
```

### 17.5 安全区底部操作栏

```css
.action-bar {
  position: sticky; bottom: 0;
  padding: 12px 16px calc(12px + env(safe-area-inset-bottom));
  background: var(--bg);
  border-top: 1px solid var(--border);
}
```

### 17.6 只在真 hover 设备上做悬停效果

```css
@media (hover: hover) and (pointer: fine) {
  .row:hover { background: var(--hover); }
  .row .actions { opacity: 0; transition: opacity 120ms; }
  .row:hover .actions { opacity: 1; }
}
@media (hover: none) {
  .row .actions { opacity: 1; }              /* 触屏常驻 */
}
```

---

## 18. 与其他资产的分工

| 问题 | 去哪 |
|---|---|
| 具体元素的构型与参数（导航/Hero/卡片…） | `patterns.md` |
| 中文行高、字号、避头尾、行长按字算 | `chinese-design.md` |
| 触控尺寸、对比度、焦点、缩放合规原文 | `accessibility.md` |
| 断点、版心、栅格、容器查询、视口单位、图片、表格降级 | **本文件** |
| 表格行高/列对齐/分页/批量（与宽度无关的部分） | `form-table.md` |
| 加载/空态在窄屏的形态 | `feedback-states.md` |
| 断点 token 怎么进三层 token 体系 | `design-tokens.md` |
| DESIGN.md 里「Responsive Behavior」一章怎么写 | `design-md-format.md` §8 |

---

## 19. 数据来源

- Ant Design Grid（24 栅格与 xs→xxxl 精确值）：https://ant.design/components/grid
- Ant Design 布局规范（画板 1440、主流分辨率、两种适配方案、8 网格）：https://ant.design/docs/spec/layout-cn
- Material UI Breakpoints（600/900/1200/1536、`down` 开区间与 step:5）：https://mui.com/material-ui/customization/breakpoints/
- Tailwind CSS 响应式（640/768/1024/1280/1536、`max-*` 严格小于、容器查询 13 档）：https://tailwindcss.com/docs/responsive-design
- Bootstrap 5.3 Containers（版心阶梯 540/720/960/1140/1320）：https://getbootstrap.com/docs/5.3/layout/containers/
- IBM Carbon 2x Grid（320/672/1056/1312/1584、4→8→16 列、8px mini unit、padding 16 / margin 0·16·16·16·24）：https://carbondesignsystem.com/elements/2x-grid/overview/
- Material 3 Breakpoints（<600 / 600–839 / 840–1199 / 1200–1599 / 1600+、分栏数、40–60 字符行长、五动词）：https://m3.material.io/foundations/layout/breakpoints/window-size-classes
- MDN CSS Container Queries（`container-type`、`@container`、`cq*` 单位、`sv*` 退化）：https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries
- MDN `clamp()`（解析规则、MIN>MAX 取 MIN、无障碍 max ≥ 2×min）：https://developer.mozilla.org/en-US/docs/Web/CSS/clamp
- MDN `<length>`（`vh` ≡ `lvh`、`svh`/`dvh` 稳定性权衡）：https://developer.mozilla.org/en-US/docs/Web/CSS/length
- MDN Responsive images（`srcset`/`sizes` 排序规则、`x` 描述符、`<picture>` 艺术指导）：https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Responsive_images
- W3C WCAG 2.2 SC 1.4.10 Reflow（320×256、400% 等效、二维例外边界）：https://www.w3.org/WAI/WCAG22/Understanding/reflow.html
- GOV.UK Table（小屏减字号 `govuk-table--small-text-until-tablet`、数字右对齐）：https://design-system.service.gov.uk/components/table/
- GitHub API 实测（2026-11-01）：tailwindcss 98269★ MIT · bootstrap 174969★ MIT · material-ui 99291★ MIT · ant-design 100025★ MIT · carbon 9594★ Apache-2.0 · container-query-polyfill 1149★ Apache-2.0 · react-responsive 7182★ MIT · fresnel 1298★ NOASSERTION · tailwindcss-container-queries 1433★ MIT
