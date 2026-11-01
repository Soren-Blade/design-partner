# 性能与设计的关系（Performance × Design）

> **一句话**：性能不是"开发做完再优化"的收尾工序，而是**和对比度、字号一样的设计约束**——你在稿子上画的每一个大图、每一种字体、每一层模糊，都已经决定了这个页面能不能在 2.5 秒内被看见。
>
> 本文件解决六个问题：**凭什么管**（三条硬因果与证据）、**卡在哪**（CWV 三指标 + LCP 四分解 + INP 三阶段 + CLS 公式）、**给多少**（性能预算与分页面类型配额）、**哪些手法贵**（视觉手法的性能价格表 + 图层内存与帧预算算术）、**怎么降级**（弱网、低端机、省流、小程序）、**怎么验**（18 项自检 + 20 条反模式）。

**读法**：赶时间 → 先看 §10 价格表 + §12 决策分级；要方案 → §6 预算 + §7 图片 + §8 字体；被质疑"为什么不能上这个效果" → §1 因果 + §3 LCP 分解。

> 快照 2026-11-01。阈值、时长、权重取自 web.dev / Chrome for Developers / 微信开放文档**官方原文**；图层内存、像素浪费倍数、视频体积由**公式现场计算**（算式写在文中，可复核）；标注「量级估计」的为工程经验值，非实测，不得当验收线用。

---

## 1. 为什么性能是设计约束：加载速度就是设计决策

### 1.1 三条硬因果

| 因果 | 证据 | 对设计意味着什么 |
|---|---|---|
| **慢 = 没人看见你的设计** | 中位网页 JS 约 **350KB**（min+gzip，未压缩 >1MB），此类页面移动端可交互 **>14s**；Addy Osmani 实测 CNN 首页 JS 在 iPhone 8 约 **4s**、Moto G4 约 **13s**、Alcatel 1X 约 **36s** | 精心调的渐变，在第 8 秒才出现，等于不存在 |
| **慢直接吃掉转化** | Pinterest 把 JS 从 **2.5MB 降到 <200KB**，TTI **23s → 5.6s**，注册 **+753%**、移动周活 **+103%**、收入 **+44%** | "再放一个轮播"不是审美问题，是收入问题 |
| **慢是不平等** | 同一份 JS，高端机与低端机处理耗时差约 **9 倍**；Android "在变便宜而不是变快" | 你在 M3 MacBook 上评审的流畅度，不代表用户看到的 |

### 1.2 一个必须纠正的直觉

**字节不等于字节**。一个 200KB 的脚本和一个 200KB 的图片，下载时间相同，但成本完全不同：

- 图片：下载 → 解码 → 栅格化 → 绘制（可离开主线程）
- JS：下载 → **解析 → 编译 → 执行** → 布局/样式计算（抢占主线程）

V8 中 parse + compile 占总处理时间的 **10–30%**，且"大型脚本很少能在 50ms 内真正执行完"。所以：

> **判断一个设计元素贵不贵，先问它引入了多少 JS，而不是它有多大。**

### 1.3 设计师该在什么时候介入

```
需求阶段 → 定载体/首屏结构 →【性能预算】← 在这里定，成本最低
视觉阶段 → 选图/选字/选效果 →【价格表比对】← 在这里定，改动便宜
开发阶段 → 只能优化，不能重设计 ← 到这里已经晚了
```

**性能是唯一一个"越早决定越便宜"的设计维度**：改一张首屏图的构图，在设计阶段是 10 分钟；在上线后发现 LCP 4.2s，是重做首屏。

---

## 2. 指标体系：先背下这七个数

### 2.1 Core Web Vitals（三项，官方核心）

| 指标 | 测什么 | 良好 | 需改进 | 差 | 单位 |
|---|---|---|---|---|---|
| **LCP** Largest Contentful Paint | 加载：视口内**最大**图片/文本块渲染完成 | **≤ 2.5s** | 2.5–4.0s | > 4.0s | 秒 |
| **INP** Interaction to Next Paint | 交互：从点击到**下一帧**绘制的延迟 | **≤ 200ms** | 200–500ms | > 500ms | 毫秒 |
| **CLS** Cumulative Layout Shift | 稳定：整个生命周期最大的一次位移爆发 | **≤ 0.1** | 0.1–0.25 | > 0.25 | 无单位 |

**判定口径（官方，别记错）**：

- 取**第 75 百分位**的页面加载，**移动端与桌面端分别统计**；三项**全部**达标才算通过。
- 核心指标"首先是**现场指标**（field）"。Lighthouse 是实验室数据，**不能替代**现场数据——本地缓存、快网、你的机器，都会让分数虚高。
- Lighthouse 无法测 INP（没有真实输入），用 **TBT** 作代理。

### 2.2 辅助指标（不是核心，但诊断时离不开）

| 指标 | 良好 | 差 | 用途 |
|---|---|---|---|
| **TTFB** Time to First Byte | ≤ 800ms | > 1800ms | 诊断 LCP 的服务器段；重定向与回源是常见元凶 |
| **FCP** First Contentful Paint | ≤ 1.8s | > 3.0s | 诊断渲染阻塞（CSS/JS 挡在前面） |
| **TBT** Total Blocking Time | < 200ms | > 600ms | INP 的实验室代理；主线程被长任务占住的总时长 |
| **SI** Speed Index | ≤ 3.4s | > 5.8s | 首屏"看起来填满"的速度，对图片型页面敏感 |

> TBT / TTFB / FCP 之所以不是核心指标：官方理由是"不可在真实环境测量，且不直接反映以用户为中心的产出"。

### 2.3 Lighthouse 性能分怎么算（Lighthouse 10 权重）

| 审计项 | 权重 |
|---|---|
| **Total Blocking Time** | **30%** |
| **Largest Contentful Paint** | **25%** |
| **Cumulative Layout Shift** | **25%** |
| First Contentful Paint | 10% |
| Speed Index | 10% |

**评分色带**：0–49 红（Poor）/ 50–89 橙（Needs Improvement）/ **90–100 绿（Good）**。

**两条必须知道的曲线性质**：

1. 分数不是线性的，来自 HTTP Archive 真实数据拟合的**对数正态分布**：第 25 百分位映射 50 分，第 8 百分位映射 90 分。
2. **0.96 分之后是收益断崖**：99→100 需要的优化量 ≈ 90→94。**别为最后 3 分加班**，把力气花在把 60 分拉到 90。

> 分数会漂：A/B 实验、广告投放、路由变化、浏览器扩展、杀毒软件都会影响。把性能当**分布**看，别当单一数字看。

---

## 3. LCP：把 2.5 秒拆成四段（这是最有用的一张表）

LCP 可无损拆成四个**不重叠、无间隙**的子部分，四段之和即 LCP：

| 子部分 | 官方建议占比 | 含义 | 设计/前端各能做什么 |
|---|---|---|---|
| **TTFB** | **~40%** | 到 HTML 首字节 | 前端：少重定向、CDN 边缘缓存。设计：**别用带随机参数的 URL 做首屏图**（打不中缓存） |
| **Resource Load Delay** | **< 10%** | TTFB 到**开始**下载 LCP 资源 | 关键：让 LCP 资源**被 HTML 预加载扫描器发现**。CSS 背景图必须 `preload` |
| **Resource Load Duration** | **~40%** | 下载 LCP 资源本身 | 设计直接决定：图多大、什么格式、要不要视频 |
| **Element Render Delay** | **< 10%** | 资源到位到**画出来** | 渲染阻塞 CSS/JS、字体、长任务 |

**官方明确提醒**：不要把百分比换算成绝对秒数（不能说"2.5s 里 TTFB 占 1s"），子部分只有**相对**意义。

### 3.1 设计侧的 LCP 决策（最常翻车的五处）

1. **首屏主视觉选什么，直接决定 LCP 上限**
   - 纯 CSS 渐变/几何构成 → LCP 往往是**文本**，几乎无下载成本。最快。
   - 一张照片 → 这张照片就是 LCP，它的字节数就是你的 LCP 下限。
   - 背景视频 → **视频不是 LCP 元素，但它的 poster 是**；且视频会抢带宽，把 LCP 推后。首屏视频是"用转化换氛围"的决定，必须显式确认。
2. **LCP 图禁止 `loading="lazy"`**（官方原文：切勿对 LCP 图片懒加载）。用 `data-src` 的懒加载库同理，会让图片对预加载扫描器不可见。
3. **`fetchpriority="high"` 最多给 1–2 张图**。给多了等于没给。
4. **CSS 背景图不会被自动发现**，必须 `<link rel="preload" as="image" fetchpriority="high">`，且 `type` 写对。
5. **首屏文案依赖自定义字体时，字体就是 LCP 资源**。字体晚到 = LCP 晚到（见 §8）。

### 3.2 一个反直觉的坑

单独优化某一段，时间会**转移**到另一段。例：把首屏图压小 300KB（load duration 变短），但主 JS 还没执行完，浏览器没空渲染 → 时间跑到 render delay，**LCP 不变**。

> 所以性能优化必须**四段一起看**，只看"图片太大"往往会白干。

---

## 4. INP：交互延迟的三段与"设计侧预算"

### 4.1 三段定义（官方）

| 阶段 | 定义 | 典型成因 |
|---|---|---|
| **Input Delay** | 事件回调开始执行之前的等待 | 主线程有**长任务**占着（>50ms） |
| **Processing Duration** | 该帧内**所有**事件回调执行的总时长 | 回调里做了重活：大列表 diff、同步布局、复杂计算 |
| **Presentation Delay** | 回调结束到**帧真正呈现** | 样式/布局/绘制开销大、图层过多 |

**关键限定**：INP 只测到"下一帧被绘制"，**不测**交互的最终结果（网络请求、异步更新）。所以"点了有反应"和"点了数据到了"是两件事，前者是 INP，后者是 §5 反馈设计。

### 4.2 计分口径（容易记错的细节）

- 只统计 **click / tap / 键盘**三类交互。hover、滚动、缩放**不计入** INP。
- 多数站点取**最差的那次交互**；交互量大的页面，**每 50 次交互忽略最高的 1 次**。
- 最终报 **p75**。
- 测量 API 默认只上报 **≥104ms** 的 `event` 条目，`durationThreshold` 最小可设 **16ms**。
- bfcache 恢复时 INP 重置为 0；跨域 iframe 内的交互计入指标但 JS 拿不到。

### 4.3 长任务 50ms：RAIL 与 INP 的分工

- **RAIL**：用户输入应在 **50ms 内**处理完，以保证 **100ms 内**有可见响应（人手感的上限）。
- **INP**：官方把达标线放到 **200ms**，因为"更现实，尤其对慢设备"。
- **Long Task 定义**：占用主线程 **>50ms** 的连续任务。

> 设计含义：**任何"点了要等一下"的交互，都要在 100ms 内先给出视觉变化**（按下态、按钮内 loading），否则用户会重复点击，把 INP 推得更差。这条与 `feedback-states.md` 的 0.1/1/10s 刻度是同一条物理规律。

### 4.4 设计侧能直接改善 INP 的四件事

1. **减少同屏可交互元素数量**：一个页面 300 个按钮，事件委托与命中测试都变贵。
2. **不做"滚动即重算"的效果**：滚动回调里 setState / 读 `offsetTop` / 改样式 → 强制同步布局，INP 与滚动流畅度双杀。
3. **大列表不整表重渲染**：虚拟滚动、分页、骨架屏分段加载。
4. **复杂动效交给合成器**（见 §11），不要在 JS 里逐帧算位置。

---

## 5. CLS：公式、五个位移源、设计侧防抖清单

### 5.1 官方公式

```
layout shift score = impact fraction × distance fraction
```

- **impact fraction**：不稳定元素在前后两帧中**可见区域的并集** ÷ 视口面积（变化前后的位置**都算**）。
- **distance fraction**：该帧内不稳定元素**最大**水平或垂直移动距离 ÷ **视口最大维度**（宽高取大者）。

官方三个例子（可直接用来给团队解释"为什么 0.18 已经很糟"）：

| 场景 | impact | distance | 分数 |
|---|---|---|---|
| 元素整体下移 25% | 0.75 | 0.25 | **0.1875** |
| 底部插入一个按钮 | 0.50 | 0.14 | **0.07** |
| 多个列表项移动 | 0.60 | 0.30 | **0.18** |

**CLS 不是总和，是最大值**：取整个生命周期中**累积分数最高的那个"会话窗口"**。会话窗口 = 多个间隔 **<1s** 的位移，窗口总长 **≤5s**。

### 5.2 什么算位移（判定表）

| 情况 | 计入 CLS |
|---|---|
| 已有元素**改变起始位置** | ✅ |
| 新元素插入 DOM，但**不推动**其他可见元素 | ❌ |
| 已有元素改尺寸，但不推动别人 | ❌ |
| 尺寸变化**导致其他元素移动** | ✅（被推动的那个算） |

### 5.3 五个位移源 + 设计侧对策

| 位移源 | 机制 | 设计侧对策 |
|---|---|---|
| **图片/视频无尺寸** | 加载后撑开 | 必须给 `width`/`height` 或 `aspect-ratio`；**比例在稿子上就定死** |
| **字体交换** | 回退字体与目标字体度量不同 | `size-adjust` / `ascent-override` 对齐度量；或用 `optional` |
| **广告/第三方组件** | 尺寸不可控 | 预留**固定**容器高度，宁可留白也不要跳 |
| **异步内容插入** | 列表/推荐位后到 | 骨架屏占位，且**骨架尺寸 = 真实尺寸** |
| **用户交互触发的位移** | 点开折叠、搜索建议 | 交互后 **500ms 内**的位移会被 `hadRecentInput` 排除（仅离散输入：tap/click/keypress；**滚动/拖拽/缩放不算**） |

> **`hadRecentInput` 的 500ms 是"免责窗口"，不是"允许跳"**。用户点了按钮，界面在 400ms 后把下面内容顶下去，虽然不计分，但观感极差。

### 5.4 设计侧的 CLS 五条铁律

1. **稿子上的每一个图片框，都要标比例**（16:9 / 4:3 / 1:1）。没标比例 = 上线必抖。
2. **骨架屏必须与真实内容同尺寸**。用"3 行骨架"接"5 行文字"是自造 CLS。
3. **字体先定回退栈并调度量**（§8.5），不要等上线再看抖不抖。
4. **横幅/公告条/优惠券浮层**要预留空间或做成覆盖层（overlay），不要插入文档流把内容顶下去。
5. **动画只用 `transform` 与 `opacity`**。改 `height`/`width`/`top`/`left` 既触发布局又可能计 CLS。

---

## 6. 性能预算：给每个页面类型一个数字

### 6.1 官方基线（可直接引用）

> **关键路径资源 < 170KB**（压缩/最小化后）、**TTI < 5s**（慢速 3G + 中位移动设备）。

这组数字来自真实基线设备 + **3G 网速**测算。移动端 JS 预算的通行口径也是 **<170KB（min+gzip）**，未压缩约 0.7MB。

### 6.2 分页面类型的预算表（建议值，需按项目校准）

| 页面类型 | JS (min+gz) | 首屏图 | 字体文件 | LCP 目标 | 说明 |
|---|---|---|---|---|---|
| **落地页 / 官网首页** | ≤ 170KB | ≤ 200KB（AVIF/WebP） | ≤ 2 个，合计 ≤ 120KB | ≤ 2.0s | 氛围可以让位，但不能超预算 |
| **内容页 / 博客 / 文档** | ≤ 120KB | ≤ 120KB | 正文用系统栈 | ≤ 1.8s | 正文阅读体验优先 |
| **电商商品页** | ≤ 200KB | ≤ 250KB（主图必须 LCP 优化） | ≤ 2 个 | ≤ 2.5s | 主图质量 vs 速度是核心取舍 |
| **中后台 / 表单系统** | ≤ 300KB | 基本无大图 | 系统栈 | ≤ 1.5s | 交互密度高，**INP 优先于 LCP** |
| **营销活动 H5** | ≤ 150KB | ≤ 180KB | ≤ 1 个 | ≤ 2.5s | 分享场景，弱网概率高 |
| **微信小程序** | 单包 ≤ 2MB | 走 CDN，不进包 | 谨慎，中文字体极大 | 首屏 ≤ 1.5s | 见 §14 |

**预算的用法（这是关键）**：预算不是给开发看的数字，是**设计评审的否决权**。

> "这个首屏要加 8 张轮播大图" → 8 × 200KB = 1.6MB，超预算 8 倍 → **不是"能不能做"，是"必须换成 1 张主图 + 缩略图条"**。

### 6.3 预算怎么落进流程

| 阶段 | 动作 |
|---|---|
| 需求 | 定页面类型 → 取 §6.2 对应行 → 写进 brief |
| 设计 | 每个视觉决策过一遍 §10 价格表；超预算项当场换方案 |
| 开发 | `bundlesize` / Lighthouse CI 卡阈值，超了就**不能合入** |
| 上线 | 看现场 p75，不看本地 Lighthouse |

超预算时官方给的三选一：**优化现有资产 / 删掉现有功能 / 不加这个功能**。没有第四选项"先上再说"。

---

## 7. 图片：设计师最直接的性能杠杆

### 7.1 格式选择矩阵

| 内容 | 首选 | 次选 | 禁止 |
|---|---|---|---|
| 照片 / 复杂渐变 / 阴影 | **AVIF** | WebP（lossy） | GIF |
| 需要透明 + 照片质感 | AVIF / WebP | PNG（体积大） | JPEG |
| 图标 / logo / 几何图形 | **SVG** | WebP（lossless） | PNG 放大 |
| 截图 / 含文字的图 | AVIF / WebP | PNG（lossless） | — |
| 动图 | **`<video>`（MP4/WebM）** | APNG | **GIF（≤256 色，体积远大于视频）** |
| 需要极高保真的细节 | PNG / WebP lossless | — | — |

**三条硬结论（官方）**：

1. **能用 CSS 做的不要用图**：阴影、渐变、圆角、简单图形用 CSS，矢量、任意分辨率清晰、字节数常常只有几十分之一。
2. **图里不要放文字**。不可选、不可搜、不可缩放、不可访问、高 DPI 下糊。要自定义字体就上 web font。
3. **WebP/AVIF 压缩普遍优于 JPEG/PNG**，配 JPEG/PNG 做兜底。

### 7.2 尺寸数学（这一节能省掉一半流量）

**核心事实**：浏览器会下载**整张图**，然后缩放到显示尺寸。你写 `width: 400px` 不会让浏览器只下载 400px 宽的图。

**像素浪费倍数**（现场计算，可复核）：

| 场景 | 需要的像素 | 实际提供的像素 | 浪费倍数 |
|---|---|---|---|
| 400×300 CSS，DPR 2，源图 4000×3000 | 800×600 = 480,000 | 12,000,000 | **25×** |
| 1440 宽首屏，DPR 2，源图 2880 宽（正确） | 2880×1620 ≈ 4.67M | 4.67M | 1× ✅ |
| 1440 宽首屏，DPR 2，源图 5760 宽（"保险起见给 4K"） | 4.67M | 33.2M | **7.1×** |

**DPR 的真相**：屏幕分辨率翻倍，像素总数**变 4 倍**（横×竖），不是 2 倍。100×100 的图在 3x 屏上是 90,000 像素（未压缩 360KB）。所以：

> **别给"保险"尺寸**。给对的尺寸，用 `srcset` 让浏览器自己挑。

### 7.3 响应式图片五条规则

```html
<img
  src="/hero-800.avif"
  srcset="/hero-480.avif 480w, /hero-800.avif 800w, /hero-1440.avif 1440w, /hero-2880.avif 2880w"
  sizes="(max-width: 768px) 100vw, 50vw"
  width="1440" height="810"
  alt="……"
  fetchpriority="high"
  decoding="async">
```

1. **`srcset` 用 `w` 描述符 + `sizes` 给布局宽度**；`sizes` 写错等于白做（浏览器按 `sizes` 算需要多少像素）。
2. **`width`/`height` 必写**（或用 `aspect-ratio`）——这是 CLS 的第一道防线。
3. **首屏图不 lazy**；`loading="lazy"` 只给折叠线以下的图。
4. **`decoding="async"`** 避免解码阻塞渲染。
5. **`<picture>` + `<source type="image/avif">`** 做格式降级（AVIF → WebP → JPEG）。

### 7.4 LCP 图三规则（与 §3 呼应）

1. `fetchpriority="high"`，且**全页最多 1–2 张**。
2. **绝不 `loading="lazy"`**，绝不 `data-src`。
3. **与首个资源同时开始加载**——判断标准：看瀑布图，LCP 图若晚于 CSS/字体开始，就有优化空间。

### 7.5 质量参数（量级估计，需按图校准）

| 格式 | 建议起点 | 说明 |
|---|---|---|
| AVIF | q **50–60** | 同观感下通常比 JPEG 小 40–60% |
| WebP | q **75–80** | 兼容性最好，压缩略逊 AVIF |
| JPEG | q **80–85** | 兜底用；q<75 渐变色带明显 |
| PNG | 无损 + 减色 | 仅在需要像素级精确时 |

> 这三个区间是**起点不是结论**。做法：同一张图导出三档，在**目标显示尺寸**下（不是 100% 放大）肉眼比对，取第一个"看不出差别"的档。

---

## 8. 字体：最容易被设计师低估的成本

### 8.1 字体为什么贵

- 字体未到时浏览器**通常延迟文本渲染** → 拖 **FCP**，常拖 **LCP**。
- 字体到达时与回退字体**度量不同** → 文本重排 → **CLS**。
- 中文字体动辄 **10,000+ 字符**（拉丁字体通常 100–1000 字形），一个未子集化的中文字重 **3–8MB**。

### 8.2 `font-display` 五档（官方数值）

| 值 | Block period | Swap period | 适合 |
|---|---|---|---|
| `auto` | 因浏览器而异 | 因浏览器而异 | 不推荐（不可控） |
| `block` | **2–3s** | 无限 | 品牌字必须出现（标题/logo 字） |
| `swap` | **0ms** | 无限 | 正文可读优先，接受跳动 |
| `fallback` | **100ms** | **3s** | 折中 |
| `optional` | **100ms** | 无 | **性能优先**：慢网直接不用自定义字体 |

**默认行为（不写时）**：Chromium/Firefox 阻塞文本渲染最长 **3s**；**Safari 无限期阻塞**。这就是"某些手机上首屏一片空白"的常见原因。

**推荐组合（官方认可）**：品牌/视觉元素用 `swap`，正文用 `optional`。

### 8.3 体积四招（按收益排序）

1. **子集化（最大收益）**：`unicode-range` 声明可用字符范围，浏览器按需下载。工具：`subfont`、`glyphhanger`；Google Fonts 支持 `text=` 参数。**中文站必做**：只含首屏常用字的子集常在 30–80KB 量级。
2. **只用 WOFF2**：Brotli 压缩，**比 WOFF 好约 30%**。老浏览器直接用回退字体，不要为它多带一份。
3. **可变字体**：一个文件替代 light/regular/bold。注意：单文件**通常比单款静态字重更大**，只有"确实要用 3 档以上字重"时才划算。
4. **系统字体**：`font-family: system-ui`。正文用系统栈是**零成本**方案，也是大多数产品该选的。

### 8.4 加载三纪律

1. **`@font-face` 声明内联进 `<head>`**（不是外部 CSS），让浏览器尽早发现。但**不要内联字体文件本身**（会延迟 HTML 交付）。
2. **`preload` 谨慎**：会抢其他资源；**会绕过 `unicode-range`**（可能白下一整套）；只预加载**单一格式**、**单一最关键字体**。
3. **第三方字体必须 `preconnect`**，且字体走 CORS 要加 `crossorigin`：

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
```

### 8.5 用 `size-adjust` 消灭字体抖动（CLS）

思路：把**回退字体的度量调成目标字体的度量**，让交换前后占位一致。

```css
@font-face {
  font-family: "Brand Sans";
  src: url("/fonts/brand-sans-subset.woff2") format("woff2");
  font-display: swap;
  unicode-range: U+4E00-9FFF, U+0020-007E;   /* 中英常用区 */
}

/* 回退字体按目标字体度量校正，交换时不重排 */
@font-face {
  font-family: "Brand Sans Fallback";
  src: local("PingFang SC"), local("Microsoft YaHei");
  size-adjust: 96%;
  ascent-override: 92%;
  descent-override: 24%;
  line-gap-override: 0%;
}

body { font-family: "Brand Sans", "Brand Sans Fallback", system-ui, sans-serif; }
```

> `size-adjust` / `ascent-override` / `descent-override` / `line-gap-override` 的**具体百分比必须实测**：用 DevTools 的 Fonts 面板对比两套字体的度量，或用 `capsize` 类工具算。写死一个"看起来对"的值比不写更糟。

### 8.6 字体数量纪律（与 `brand-identity.md` 一致）

- **≤ 2 族、≤ 3 字重**（设计侧）；**≤ 2 个字体文件**（性能侧）。
- 图标**不要用图标字体**：回退字体与图标字形差异极大，CLS 最严重；用 SVG（对无障碍也更好）。
- 中文**不用 500 字重**（多数中文字体缺该档会触发伪粗，既难看又多一次合成）。

---

## 9. JavaScript：设计师看不见但逃不掉的那部分

### 9.1 三条数量级

| 事实 | 数字 |
|---|---|
| 中位页面 JS（min+gz） | ~**350KB**（未压缩 >1MB）→ 移动端 TTI **>14s** |
| 同一份 JS 的高端/低端机差距 | **约 9 倍**（CNN：4s vs 36s） |
| 长任务门槛 | **>50ms** 即算 Long Task |
| parse + compile 占 V8 处理时间 | **10–30%** |

### 9.2 设计决策如何变成 JS

| 设计决定 | 引入的 JS 量级 | 备注 |
|---|---|---|
| 一个轮播组件 | 20–60KB | 原生 CSS `scroll-snap` 可做到 0KB |
| 一个图表库（ECharts 全量） | 300–900KB | 按需引入可降到 100–200KB |
| 一个动效库（GSAP 全量） | ~70KB | 多数界面动效用 CSS transition 就够 |
| 一个 UI 组件库全量 | 300KB–1MB+ | 按需引入是必做项 |
| 一个 3D 场景（three.js） | 600KB+ | 首屏用 = 直接放弃 2.5s |
| 一个客服/统计/AB 测试脚本 | 各 30–200KB | **第三方脚本是隐形大头** |

> **评审时的提问模板**：「这个效果需要引入多少 KB？有没有 0KB 的 CSS 实现？」——这一问能挡掉一半的性能债。

### 9.3 代码分割与第三方脚本

- **路由级分割是默认动作**：只加载当前页需要的 JS。
- **第三方脚本**（统计、客服、AB、广告）常是 Long Task 的主要来源：延后加载、`defer`/`async`、或用 **Partytown**（13.8k★ MIT，把第三方脚本挪到 Web Worker）。
- **不要为了 A/B 测试下发所有变体**：那等于给每个用户加载 N 份 JS。

---

## 10. 视觉手法的性能价格表（本轮核心）

> **怎么用**：设计评审时逐个效果对照。价格是**机制判断 + 量级估计**，不是精确基准；星级越高越该找替代方案。

| 手法 | 价格 | 机制 | 替代/缓解 |
|---|---|---|---|
| CSS 渐变 / 纯色 / 几何构成 | ★☆☆☆☆ | 无网络成本，绘制便宜 | 首选。能做就用它 |
| SVG 图标 / 插画 | ★☆☆☆☆ | 矢量、可 gzip、可缓存 | 注意路径点数，过度复杂会拖慢绘制 |
| 系统字体 + 字号/字重层级 | ★☆☆☆☆ | 零下载 | 大多数正文该走这条 |
| 单张优化后的首屏大图（AVIF） | ★★☆☆☆ | 一次下载，可控 | 必配 `fetchpriority` + 正确尺寸 |
| 卡片阴影 / 圆角 / 边框 | ★★☆☆☆ | 绘制成本低 | 大范围 `box-shadow` 会拖慢滚动，改 1px 边框 |
| 自定义字体（子集化，1–2 文件） | ★★★☆☆ | 字体是 LCP 竞争者 + CLS 源 | 子集化 + `optional`/`size-adjust` |
| 入场动画（transform/opacity） | ★★★☆☆ | 合成器执行，不重排 | 只用这两个属性；`will-change` 别滥用 |
| 玻璃拟态 `backdrop-filter: blur()` | ★★★★☆ | 每帧对**背后区域**做模糊采样，成本随**面积**与**半径**上升；移动端常掉帧 | ① 减小模糊面积（只给标题条）② 用半透明纯色 + 1px 高光边模拟 ③ 只在静态层用 |
| 大面积 `filter: blur()` / 噪点叠加层 | ★★★★☆ | 全屏滤镜每帧重算 | 把噪点做成**静态 PNG/SVG 叠一层**（一次解码），不要用 CSS 生成 |
| 视差滚动（多层位移） | ★★★★☆ | 每帧读滚动位置 + 改 transform；易触发同步布局 | 用 `scroll-timeline`（CSS 滚动驱动）而非 JS；层数 ≤3 |
| 首屏背景视频 | ★★★★★ | 5s 1080p @4Mbps ≈ **2.5MB**（算术：4×5÷8）；抢带宽、推后 LCP、耗电 | ① 用 poster 图当 LCP ② 视频延后 1s 再加载 ③ 移动端只留图 ④ 短循环 + `preload="none"` |
| 大图轮播（自动播） | ★★★★★ | N 张全尺寸图 + JS + 抢优先级 | 1 张主图 + 缩略图条；或 CSS `scroll-snap` |
| 3D / WebGL 首屏场景 | ★★★★★ | 600KB+ JS + GPU 内存 + 移动端发热 | 静态渲染图 + 交互后再加载；或只做装饰性 CSS 3D |
| 粒子 / 连线背景 | ★★★★★ | 逐帧重绘全屏 canvas | 静态图 / 视频 / 极低密度 + 暂停不可见时 |
| 自定义鼠标光标 + 拖尾 | ★★★★☆ | 每帧 `mousemove` + 改样式；触屏无意义 | 只做 hover 态变化；触屏设备不加载 |
| 全站无缝页面转场 | ★★★☆☆ | 依赖 View Transitions（现代浏览器） | 有原生方案就用原生，别自己写一套 |
| 滚动数字增长 / 打字机 | ★★★☆☆ | 逐帧改文本 → 重排 | 用 `tabular-nums` 固定宽度；或用 CSS `@property` 动画 |
| 长列表无限滚动 + 复杂卡片 | ★★★★☆ | DOM 数量爆炸 + 图片并发 | 虚拟滚动 + 图片 `lazy` + 骨架占位 |
| 图片走 CDN 自动裁切/转格式 | ★☆☆☆☆ | 反而**降低**成本 | 强烈推荐：imgproxy（11.2k★ Apache-2.0）等 |

**三条从价格表直接推出的结论**：

1. **"高级感"最贵的两个来源是视频和模糊**。想要氛围，先试 CSS 渐变 + 高质量静态图 + 克制动效——这三样加起来通常 <300KB，观感能到 80%。
2. **任何"全屏每帧重算"的效果都是红灯**：全屏 blur、全屏 canvas、全屏滤镜、全屏视差。**限定面积**是唯一便宜的解法。
3. **触屏设备不该为桌面效果付费**：光标拖尾、hover 视差、鼠标跟随在触屏上零收益，必须条件加载。

---

## 11. 渲染性能：帧预算与图层内存（可算的数）

### 11.1 帧预算

| 刷新率 | 每帧可用时间 | 含义 |
|---|---|---|
| 60Hz | **16.67ms** | 主流基线。超过就掉帧 |
| 90Hz | 11.1ms | |
| 120Hz | **8.33ms** | 高刷屏，预算直接砍半 |

这 16.67ms 要同时装下：事件处理 + JS + 样式计算 + 布局 + 绘制 + 合成。所以**留给 JS 的时间实际只有 ~10ms 量级**。

### 11.2 只动 `transform` 与 `opacity`

| 属性 | 触发的流水线阶段 | 代价 |
|---|---|---|
| `transform` / `opacity` | **仅合成**（compositor） | 可在 GPU 线程完成，不阻塞主线程 ✅ |
| `background-color` / `color` | 绘制 | 小面积可接受 |
| `width` / `height` / `top` / `left` / `margin` | **布局 → 绘制 → 合成** | 最贵，且可能计 CLS ❌ |
| `filter` / `backdrop-filter` | 绘制（每帧重算） | 面积越大越贵 ❌ |

**展开动画的正确写法**（不碰 `height`）：

```css
.accordion { display: grid; grid-template-rows: 0fr; transition: grid-template-rows 200ms cubic-bezier(0.2,0,0,1); }
.accordion[open] { grid-template-rows: 1fr; }
.accordion > div { overflow: hidden; }
```

### 11.3 图层内存：`will-change` 的真实代价

`will-change: transform` 会让元素**提升为独立合成层**，内存按 **宽 × 高 × 4 字节**（RGBA）计：

| 元素尺寸 | 图层内存（计算） |
|---|---|
| 375×812（手机全屏） | 375×812×4 = **1.22MB** |
| 1440×900（桌面视口） | 1440×900×4 = **5.18MB** |
| 1920×1080（全屏） | 1920×1080×4 = **7.93MB** |
| 2880×1620（2x 全屏图） | 2880×1620×4 = **17.8MB** |

**结论**：

- 一个页面同时提升 5 个全屏层 = 几十 MB 显存，**低端机直接崩**。
- `will-change` **只在动画前 100–200ms 加，动画结束就移除**；写在常驻 CSS 里是最常见的性能反模式。
- 移动端同时活跃的合成层建议 **≤ 5–8 个**（量级经验值）。

### 11.4 三个高频性能反模式（代码级）

| 反模式 | 后果 | 正确做法 |
|---|---|---|
| 滚动回调里读 `offsetTop` / `getBoundingClientRect` 再改样式 | **强制同步布局**，每帧一次全量重排 | 用 `IntersectionObserver` 替代"滚动到某处就……" |
| 用 `setInterval` 逐帧改样式做动画 | 与刷新率不同步，掉帧且耗电 | CSS `transition`/`animation`，或 `requestAnimationFrame` |
| 长列表每项一个 `box-shadow` + `border-radius` + 背景图 | 绘制成本线性叠加 | 简化到 1px 边框；图片 `lazy`；虚拟滚动 |

---

## 12. 设计决策分级：什么时候可以"花"性能

不是所有页面都该为速度牺牲表现力。**先判页面类型，再判可花的额度**。

### 12.1 三档

| 档位 | 页面类型 | 可花的额度 | 底线 |
|---|---|---|---|
| **A · 效率优先**（不许花） | 中后台、表单、审批流、设置页、错误页、支付 | 几乎为 0：系统字体、无大图、动效只留反馈 | LCP ≤1.5s、INP ≤200ms、**INP 优先于一切** |
| **B · 平衡**（有限花） | 电商、内容站、SaaS 落地页、工具产品 | 1 张首屏大图 + 1–2 个字体文件 + 1 处克制动效 | LCP ≤2.5s、CLS ≤0.1 |
| **C · 表达优先**（可花） | 品牌官网首页、活动专题、作品集、发布会页 | 可上视频/3D/重动效，但**必须给降级路径** | LCP ≤2.5s（首屏仍要达标）；移动端必须有静态版 |

### 12.2 C 档的四条硬约束（否则就是"自我感动的设计"）

1. **首屏仍要 2.5s**：氛围放在**首屏之后**（滚动第二屏再放视频/3D），不要拿 LCP 换。
2. **必须有静态降级**：`prefers-reduced-motion` / 省流模式 / 低端机 → 直接出静态版。
3. **必须可跳过**：视频/开场动画有"跳过"或 3s 内自动结束。
4. **移动端单独设计**：桌面视频背景 → 移动端静态图，这不是"偷懒"，是标准做法。

### 12.3 一句可复用的立场

> **性能预算不是"不能做好看"，是"必须选择在哪里好看"。**
> 一个页面只能有一个地方挥霍。挥霍两处，整页都平庸。

---

## 13. 弱网与低端设备：降级不是可选功能

### 13.1 三层降级

| 层 | 触发条件 | 动作 |
|---|---|---|
| **系统偏好** | `prefers-reduced-motion: reduce` | 杀位移/缩放/循环动画，保留 ≤100ms 色彩反馈（见 `motion-system.md`） |
| **省流** | `prefers-reduced-data: reduce` 或 `Save-Data: on` | 不自动播视频、降图质量、关预加载 |
| **运行时** | `navigator.connection.effectiveType` 为 `2g`/`slow-2g`，或 `deviceMemory` 低 | 关背景视频、只加载首屏图、延后第三方脚本 |

```css
@media (prefers-reduced-data: reduce) {
  .hero-video { display: none; }
  .hero-image { background-image: url("/hero-640.avif"); }
}
```

```js
// 只在网络和设备允许时加载重资产
const c = navigator.connection || {};
const slow = /2g/.test(c.effectiveType || "") || c.saveData === true;
if (!slow) import("./hero-scene.js");   // 3D / 视频 / 粒子
```

### 13.2 弱网下的设计对策（不是技术对策）

| 现象 | 设计对策 |
|---|---|
| 图片慢慢"刷出来" | 用**主色/模糊占位色块**（LQIP）或纯色块，别留白框 |
| 首屏空白 3 秒 | 骨架屏必须**与真实布局同构**（见 `feedback-states.md`） |
| 字体晚到导致跳动 | `font-display: optional` + 系统栈正文 |
| 用户不知道在等什么 | >2s 给骨架，>10s 给进度 + 取消（与 `feedback-states.md` 时间刻度一致） |
| 图片加载失败 | **必须有失败占位**（图标 + 重试），不要留破图 |

### 13.3 一条常被忽略的规则

**首屏之外的图片一律 `loading="lazy"`，但"首屏"的定义是视口内，不是"页面顶部"。**

判断方法：在 375×667（最小主流视口）下看，凡是**第一屏能看到的**都不 lazy。

---

## 14. 微信小程序：另一套物理规律

### 14.1 官方硬数值

| 项 | 数值 | 出处 |
|---|---|---|
| **单个代码包体积上限** | **2MB** | 官方《代码包体积优化》原文："小程序单个代码包的体积上限为 2M" |
| 总包上限 | 20MB（普通小程序，以后台上传提示为准） | 后台限制，类目可能更高 |
| 代码包压缩算法 | **ZSTD** | 官方原文 |
| 图片/音视频/字体在包内 | **难以被进一步压缩，对下载耗时影响远大于代码** | 官方原文 |

### 14.2 五条官方优化手段（按收益排序）

1. **分包加载**（官方称"优化启动耗时效果最明显的手段"）：按功能/使用频率拆包，按需加载。
2. **独立分包**：广告页、活动页、支付页等"要求启动快且相对独立"的页面，**进入时不下载主包**。
3. **分包预下载**：解决"首次进分包页要等下载"的体验断层。
4. **分包异步化**：把插件/组件/逻辑从主包剥离到分包，运行时异步加载——官方称"能有效解决主包大小过度膨胀"。
5. **按需注入（`lazyCodeLoading`）**：不开时，编译期把所有 JS 打成**一个文件一次性注入并执行所有页面与组件代码**。

### 14.3 设计侧最该记的三条

1. **图片不要进包，走 CDN**。官方明确：包内图片/字体"难以进一步被压缩"，影响远大于代码。包内只放小图标。
2. **全局自定义组件与插件是隐形税**：`app.json` 里 `usingComponents` 全局引用的组件、`plugins` 全局引入的插件，**启动时随主包一起下载并注入**。只在某个分包用的组件，就写在页面/分包的配置里。
3. **`setData` 的两条铁律**：
   - **只传变化的字段**，禁止 `this.setData(this.data)`。
   - **`data` 只放渲染相关字段**，非渲染数据挂 `this.xxx` 或纯数据字段。
   - 影响性能的第一因素是**组件 Shadow 树节点总量**（官方原文："前者的影响比后者更大"），所以**合理拆组件比减小数据量更有效**。
   - **避免在滚动回调里每次 setData**；避免页面切后台后仍高频更新。

### 14.4 小程序性能自检（5 条）

- [ ] 主包 ≤ 2MB？有没有把只在分包用的组件写进全局 `usingComponents`？
- [ ] 开了 `lazyCodeLoading: "requiredComponents"`？
- [ ] 高频入口页是否放在**独立分包**？
- [ ] 包内是否有 >50KB 的图片/字体？（应走 CDN）
- [ ] `setData` 是否只传 diff、`data` 是否只有渲染字段、滚动回调里有没有 setData？

---

## 15. 度量与验收：看哪个数、在哪看

### 15.1 工具分工

| 工具 | 类型 | 用途 | 注意 |
|---|---|---|---|
| **CrUX / Search Console** | 现场 | 真实用户 p75，唯一"真相" | 有延迟（约 28 天滚动） |
| **PageSpeed Insights** | 现场 + 实验室 | 两者对照看 | 现场数据来自 CrUX |
| **Lighthouse**（31.0k★ Apache-2.0） | 实验室 | 开发期定位问题 | **测不了 INP**，用 TBT 代理 |
| **Lighthouse CI**（7.1k★ Apache-2.0） | 实验室 | 卡预算、防回归 | 必须进 CI，否则预算形同虚设 |
| **web-vitals**（8.7k★ Apache-2.0） | 现场 | 自建 RUM，含 LCP 四段归因 | 生产环境必装 |
| **sitespeed.io**（5.0k★ MIT） | 实验室 | 多页面批量、趋势 | 适合定期巡检 |
| **DevTools Performance** | 实验室 | 长任务、强制同步布局定位 | 看灰色 Task 上的红三角 |

### 15.2 验收顺序（别搞反）

```
① 现场 p75 达标？
   ├─ 否 → 用 Lighthouse 定位是哪一段（LCP 四分解 / TBT / CLS 源）
   └─ 是 → ② 预算是否仍在阈值内（防回归）
③ 弱网 + 低端机复测（3G 限速 + 4x CPU 降速）
④ 真机：低亮度、灰度、省电模式
```

**"本地 Lighthouse 100 分"不是验收通过**。官方明确：实验室测量不能替代现场测量。

### 15.3 性能预算进 CI 的三行配置（示意）

```jsonc
// lighthouse-ci 配置要点
{
  "ci": {
    "assert": {
      "assertions": {
        "largest-contentful-paint": ["error", { "maxNumericValue": 2500 }],
        "cumulative-layout-shift":   ["error", { "maxNumericValue": 0.1 }],
        "total-blocking-time":       ["error", { "maxNumericValue": 200 }],
        "performance":               ["error", { "minScore": 0.9 }]
      }
    }
  }
}
```

---

## 16. 反模式清单（20 条，逐条对照）

1. 首屏用背景视频，且 poster 是 2MB 的 PNG。
2. LCP 图写了 `loading="lazy"`。
3. 全页 6 张图都写了 `fetchpriority="high"`。
4. 图片只写 `width` 不写 `height`（或都没有），靠"加载后自适应"。
5. 给 400px 的展示位提供 4000px 的源图（25 倍浪费）。
6. 中文站用未子集化的中文字体（3–8MB）。
7. `font-display` 不写，指望浏览器默认行为（Safari 无限期阻塞）。
8. 同时用 4 个字重 + 2 个字族 + 1 个图标字体。
9. 图标用图标字体（CLS 最严重的一类）。
10. 玻璃拟态铺满整屏，`blur(30px)` 常驻。
11. 噪点/颗粒用 CSS 逐帧生成，而不是静态图叠层。
12. `will-change: transform` 写在全局常驻样式里。
13. 滚动回调里读布局属性再改样式（强制同步布局）。
14. 首屏上 three.js 做装饰性 3D。
15. 自动播放的大图轮播（5 张全尺寸图）。
16. 无限滚动列表不做虚拟化，DOM 上万个节点。
17. 用 `setData(this.data)` 图省事。
18. 第三方脚本（统计/客服/AB）同步加载在 `<head>`。
19. 只在本地 Lighthouse 验收，不看现场 p75。
20. 为拿 99→100 分投入两周，却放着 4.2s 的 LCP 不管。

---

## 17. 交付自检（18 项，全过才算过关）

**首屏与 LCP**
1. 首屏主视觉是什么？它的**字节数**是多少？这个数字 ≤ 预算吗？
2. LCP 元素是哪一个？它有没有 `fetchpriority="high"` 且**没有** `lazy`？
3. CSS 背景图（若为 LCP）有没有 `preload`？
4. 首屏文案是否依赖自定义字体？若字体晚到，首屏还成立吗？

**稳定性 CLS**
5. 每张图/视频都标了 `width`/`height` 或 `aspect-ratio`？
6. 骨架屏尺寸 = 真实内容尺寸？
7. 字体回退栈调过 `size-adjust` 或用了 `optional`？
8. 有没有"插入文档流"的公告条/优惠券/推荐位？

**交互 INP**
9. 每次点击 **100ms 内**有可见变化？
10. 滚动回调里没有 setData / 读布局 / 改样式？
11. 长列表做了虚拟化或分页？
12. 同屏可交互元素数量合理（不是几百个按钮）？

**资源与降级**
13. 图片格式是 AVIF/WebP + 兜底？动图用 `<video>` 而非 GIF？
14. 字体 ≤2 文件、中文已子集化、只用 WOFF2？
15. `prefers-reduced-motion` 与 `prefers-reduced-data` 都有分支？
16. 移动端是否加载了只有桌面有意义的效果（光标/视差/3D）？

**验收**
17. 在 **3G + 4x CPU 降速**下走过一遍？首屏可读吗？
18. 预算进了 CI？看的是现场 p75 而不是本地分数？

---

## 18. 可抄代码

### 18.1 首屏 LCP 图（最优组合）

```html
<link rel="preload" as="image" href="/hero-1440.avif"
      type="image/avif" fetchpriority="high" media="(min-width: 769px)">

<picture>
  <source type="image/avif"
          srcset="/hero-480.avif 480w, /hero-800.avif 800w, /hero-1440.avif 1440w, /hero-2880.avif 2880w"
          sizes="100vw">
  <source type="image/webp"
          srcset="/hero-480.webp 480w, /hero-800.webp 800w, /hero-1440.webp 1440w"
          sizes="100vw">
  <img src="/hero-800.jpg" alt="产品主视觉：……"
       width="1440" height="810"
       fetchpriority="high" decoding="async">
</picture>
```

### 18.2 折叠线以下图片（防 CLS + 懒加载）

```html
<img src="/card-400.avif" alt="……"
     width="400" height="300" loading="lazy" decoding="async"
     style="aspect-ratio: 4 / 3; object-fit: cover;">
```

### 18.3 字体（子集 + 度量对齐 + 性能优先）

```css
@font-face {
  font-family: "Brand Sans";
  src: url("/fonts/brand-sans-zh-subset.woff2") format("woff2");
  font-weight: 400 700;              /* 可变字体范围 */
  font-display: optional;            /* 正文：慢网宁可用系统字 */
  unicode-range: U+4E00-9FFF, U+3000-303F, U+0020-007E;
}
@font-face {
  font-family: "Brand Sans Fallback";
  src: local("PingFang SC"), local("Microsoft YaHei"), local("Noto Sans CJK SC");
  size-adjust: 96%;                  /* 实测值，非拍脑袋 */
  ascent-override: 92%;
  descent-override: 24%;
  line-gap-override: 0%;
}
:root {
  --font-body: "Brand Sans", "Brand Sans Fallback", system-ui, -apple-system, sans-serif;
}
```

### 18.4 只动合成器属性的入场动画

```css
.card {
  opacity: 0;
  transform: translateY(12px);
  transition: opacity 200ms cubic-bezier(0.05, 0.7, 0.1, 1),
              transform 200ms cubic-bezier(0.05, 0.7, 0.1, 1);
}
.card.is-in { opacity: 1; transform: none; }

@media (prefers-reduced-motion: reduce) {
  .card { transition: opacity 100ms linear; transform: none; }
}
```

### 18.5 用 IntersectionObserver 替代滚动回调

```js
const io = new IntersectionObserver((entries) => {
  for (const e of entries) {
    if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); }
  }
}, { rootMargin: "0px 0px -10% 0px" });

document.querySelectorAll(".card").forEach((el) => io.observe(el));
```

### 18.6 省流与慢网降级

```js
const conn = navigator.connection || {};
const slowNet = conn.saveData === true || /(^|-)2g$/.test(conn.effectiveType || "");
const lowMem = (navigator.deviceMemory || 8) <= 2;

if (!slowNet && !lowMem && !matchMedia("(prefers-reduced-data: reduce)").matches) {
  // 只有这时才加载重资产
  import("./hero-video.js");
  import("./ambient-particles.js");
}
```

---

## 19. 数据来源

- [web.dev · Web Vitals](https://web.dev/articles/vitals)：LCP ≤2.5s / INP ≤200ms / CLS ≤0.1、**75 百分位**、移动桌面分段、现场优先、TBT 作为 INP 代理
- [web.dev · Optimize LCP](https://web.dev/articles/optimize-lcp)：四子部分与 **40/10/40/10** 占比、"不要换算成绝对秒数"、`fetchpriority` 只用 1–2 张、LCP 图禁 lazy
- [web.dev · INP](https://web.dev/articles/inp)：三阶段定义、200/500ms、每 50 次交互忽略最高 1 次、`durationThreshold` 默认 104ms / 最小 16ms、仅 click/tap/键盘
- [web.dev · CLS](https://web.dev/articles/cls)：0.1/0.25、`impact × distance` 公式与三个算例、会话窗口 <1s 且 ≤5s、`hadRecentInput` **500ms** 仅离散输入
- [web.dev · Long Tasks](https://web.dev/articles/long-tasks-devtools)：Long Task = **>50ms**、RAIL 50ms 处理 / 100ms 响应、INP 放宽到 200ms 的理由
- [web.dev · Font best practices](https://web.dev/articles/font-best-practices)：`font-display` 五档的 block/swap 期数值、默认阻塞 3s 与 Safari 无限期、WOFF2 **比 WOFF 好 30%**、拉丁 100–1000 / CJK >10,000 字形、`preload` 绕过 `unicode-range`
- [web.dev · Choose the right image format](https://web.dev/articles/choose-the-right-image-format)：格式矩阵、DPR 像素 4 倍/9 倍、GIF 换 `<video>`、图内禁文字、CSS 效果优先
- [web.dev · Performance budgets 101](https://web.dev/articles/performance-budgets-101)：**关键路径 <170KB**、**TTI <5s（3G + 中位设备）**、预算三选一
- [Chrome for Developers · Lighthouse performance scoring](https://developer.chrome.com/docs/lighthouse/performance/performance-scoring)：Lighthouse 10 权重（TBT 30 / LCP 25 / CLS 25 / FCP 10 / SI 10）、0–49/50–89/90–100 色带、对数正态曲线与 0.96 断崖
- [Addy Osmani · The Cost of JavaScript](https://medium.com/@addyosmani/the-cost-of-javascript-in-2018-7d8950fbb5d4)：CNN 4s/13s/36s、parse+compile 占 10–30%、中位页面 350KB→TTI 14s+、Pinterest 2.5MB→200KB 的转化数据（2018 实测，注意时效）
- [微信开放文档 · 代码包体积优化](https://developers.weixin.qq.com/miniprogram/dev/framework/performance/tips/start_optimizeA)：**单个代码包上限 2M**、ZSTD、分包/独立分包/预下载/异步化、全局组件与插件的启动税、包内资源难以压缩
- [微信开放文档 · 合理使用 setData](https://developers.weixin.qq.com/miniprogram/dev/framework/performance/tips/runtime_setData)：Shadow 树节点量是首要因素、只传 diff、`data` 只放渲染字段、滚动回调禁 setData
- [MDN · prefers-reduced-data](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-data)、[MDN · size-adjust](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/size-adjust)、[MDN · will-change](https://developer.mozilla.org/en-US/docs/Web/CSS/will-change)
- 仓库实测（2026-11-01，GitHub API）：lighthouse 30992★ Apache-2.0 · web-vitals 8668★ Apache-2.0 · lighthouse-ci 7123★ Apache-2.0 · squoosh 26083★ Apache-2.0 · sharp 32812★ Apache-2.0 · sitespeed.io 5047★ MIT · fontsource 6255★ MIT · lazysizes 17713★ MIT · critical 10299★ Apache-2.0 · workbox 13040★ MIT · imgproxy 11165★ Apache-2.0 · partytown 13807★ MIT（QwikDev）· calibreapp/image-actions 1578★ **GPL-3.0（商用注意）**
- **已归档，勿再推荐**：GoogleChromeLabs/critters（3425★，2024-10 归档）· GoogleChromeLabs/preload-webpack-plugin（2142★，2021-01 归档）
