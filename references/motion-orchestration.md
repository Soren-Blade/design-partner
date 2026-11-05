# 动效进阶 — 编排、状态机与共享元素转场（深度蒸馏）

> 本文件回答「**多个元素一起动、一个元素跨两个视图动、动画被中途打断时，怎么组织、怎么实现、怎么不炸**」。
> 与 `motion-system.md` 严格分工：那份管**单个动效**该不该做、做多久、用什么曲线（决策层）；这份管**编排与工程实现**（实现层）。两者冲突时以 `motion-system.md` 的曲线/时长为准，本文件不重设数值。
> 全部机制与数值取自官方原文（MDN / W3C CSS View Transitions Module Level 1 / CSS Transitions Level 2 / Chrome DevRel / Motion / React Transition Group / Vue / Svelte / XState / Paul Lewis FLIP 原文），star 与许可经 GitHub API 实测。**快照 2026-11-05**。

**使用方式**：§1 判该查哪层 → §2 定时间结构 → §3 交错 → §4/§5 列表与 FLIP → §6/§7/§8 共享元素与跨文档 → §9/§10/§11 状态机与中断 → §12 CSS 进出场 → §13 降级 → §14 性能 → §19 抄代码 → §18 验收。

---

## 1. 分工与决策树：单动效、编排、状态机三层

动效问题分三层，**先判层再查文件**，否则会把「一个按钮反馈」做成状态机，或把「列表增删」当成单个 transition。

| 层 | 判据 | 查哪份 | 核心问题 |
|---|---|---|---|
| **L1 单动效** | 一个元素、一个状态变化、无其他元素配合 | `motion-system.md` | 该不该动？多久？什么曲线？ |
| **L2 编排** | 同一时刻有 ≥2 个元素在动，或元素有先后顺序 | **本文件 §2–§5** | 谁先谁后？总时长多少？打断怎么办？ |
| **L3 状态机** | 存在「进场中 / 已进场 / 退场中 / 已退场」等**互斥状态**，或元素需要跨视图配对 | **本文件 §6–§11** | 状态怎么迁移？中断后回到哪个状态？ |

**三条判层口诀**：

1. 用户说「加个动效 / 这个动画怪」→ L1，去 `motion-system.md`。
2. 用户说「**依次**出现 / 列表删掉会跳 / 卡片点开变成详情页 / 两个动画打架」→ L2+L3。
3. 用户说「**连点**就乱 / 中途取消 / 点了没反应 / 快速切换页面」→ L3 的中断与状态机（§9–§11），这是最难的一层，也是本文件的主要价值。

> **立场**：动效 bug 有 80% 不在曲线好不好看，而在**状态没建模**。`animationend` 没触发、DOM 提前移除、两个转场并发、key 用了 index——全都是状态问题，调 easing 永远修不好。

---

## 2. 编排的四种时间结构与总时长公式

**编排 = 给 N 个动画分配起始时刻**。只有四种结构，所有框架都是这四种的包装：

| 结构 | 定义 | 适用 | 总时长 |
|---|---|---|---|
| **并行（parallel）** | 全部 t=0 起跑 | 同一逻辑组的元素（一张卡片的图标+标题+正文） | `max(d_i)` |
| **串行（sequence）** | 前一个结束才起下一个 | 一次只呈现一个信息（轮播、向导、`mode="wait"`） | `Σ d_i` |
| **重叠（overlap）** | 前一个进行到 p% 时起下一个 | 父子容器（父位移 60% 后子内容淡入） | `d_1 + (1−p)·d_2` |
| **交错（stagger）** | 等间隔 s 依次起跑 | 列表/网格入场 | `d + (n−1)·s` |

### 2.1 总时长硬上限与可算的 stagger

`motion-system.md` 定了「点击触发 ≤400ms」「stagger 间隔 20–40ms」「≤6 项」——这三条其实是**同一个公式的三个约束**：

```
T_total = T_parent_offset + d_child + (n − 1) × s      （正向交错）
约束：T_total ≤ 400ms（点击触发）
反解：s ≤ (400 − d_child) / (n − 1)
```

| 项数 n | 单项 d | 间隔 s | 总时长 | 结论 |
|---|---|---|---|---|
| 6 | 200ms | 30ms | 200 + 5×30 = **350ms** | ✅ 标准做法 |
| 8 | 200ms | 30ms | 200 + 7×30 = **410ms** | ❌ 超限，砍到 7 项或 s=25ms |
| 12 | 200ms | 40ms | 200 + 11×40 = **640ms** | ❌ 最后一项 640ms 才出现 → **整组淡入** |
| 20 | 200ms | 20ms | 200 + 19×20 = **580ms** | ❌ 同上 |

**结论（可执行）**：`n > 6` 时不要逐项 stagger，改为「整组淡入 + 分组」（每组 4–6 项并行，组间 40ms）。这不是审美偏好，是 400ms 上限的算术结果。

**反向交错**（`staggerDirection: -1` 或 CSS `calc((N − 1 − var(--index)) × s)`）：从最后一项往回播，只用于「收起 / 关闭 / 撤销」语义；**入场一律正向**，反向入场会让用户先看到最不重要的末尾项。

### 2.2 编排的层级纪律（与 `motion-system.md` §5 对齐并补全）

- **父先子后用 `when`**：`when: "beforeChildren"` 进场、`when: "afterChildren"` 退场。退场必须等子内容先走完，否则父容器消失会把子元素一起拽掉。
- **同一逻辑组必须并行**：Fluent 的原则——次要元素同步可避免注意力分散；把一张卡片的标题、图标、正文拆成三个 stagger 是设计错误。
- **同向原则**：同一次转场所有元素朝同一方向。反向运动只在「对比 / 切换」语义下出现（旧页往左出、新页从右进是同向，不是反向）。
- **编排不得改变功能时序**：DOM 更新、数据提交、焦点迁移**不能**依赖动画结束事件。动画是增强（enhancement），失败不能让状态变更失败——Chrome DevRel 原文明确要求「app shouldn't enter an error state if the DOM change succeeds, but the transition fails」。

---

## 3. 交错编排 stagger：variants 传播与多框架实现

### 3.1 Motion for React：variants 传播是编排的地基

**传播规则**（官方原文）：「Variants will flow down through `motion` components」——父级 `motion` 组件切换 variant 标签时，所有子级 `motion` 组件会**自动**切换到同名 variant；子级不需要接收任何 prop。

```jsx
import { motion } from "motion/react"

const list = { visible: { opacity: 1 }, hidden: { opacity: 0 } }
const item = { visible: { opacity: 1, x: 0 }, hidden: { opacity: 0, x: -100 } }

<motion.ul initial="hidden" whileInView="visible" variants={list}>
  <motion.li variants={item} />
  <motion.li variants={item} />
  <motion.li variants={item} />
</motion.ul>
```

**默认行为**：子动画与父动画**同时开始**（官方原话 "children animations will start simultaneously with the parent"）。要改时序，只能用父级 `transition` 里的编排 prop。

### 3.2 两代编排 API（重要：官方文档已换写法）

| | 新版（motion.dev 现行文档） | 旧版（Framer Motion 时代，存量项目大量存在） |
|---|---|---|
| 父先子后 / 子先父后 | `when: "beforeChildren"` / `"afterChildren"` | 同名，沿用 |
| 交错 | `delayChildren: stagger(0.3)`（`stagger()` 函数返回动态延迟） | `staggerChildren: 0.05`（固定秒数） |
| 方向 | 由 `stagger()` 的选项/`staggerDirection: -1` 控制 | `staggerDirection: 1 / -1` |
| 子级延迟 | 同上 | `delayChildren: 0.2` |

**新版官方原文代码**：

```js
const list = {
  visible: {
    opacity: 1,
    transition: {
      when: "beforeChildren",
      delayChildren: stagger(0.3), // Stagger children by .3 seconds
    },
  },
  hidden: {
    opacity: 0,
    transition: { when: "afterChildren" },
  },
}
```

> 注意：`stagger(0.3)` 是 **0.3 秒**（函数参数用秒），而 `staggerChildren: 0.05` 也是秒；但 WAAPI 的 `duration`/`delay` 全用**毫秒**（§11）。三套单位混用是工程事故高发点，**项目里统一写一张换算表**。

### 3.3 原生 CSS 交错（无框架、包体最小）

```css
.list > * {
  animation: rise 200ms cubic-bezier(0.05, 0.7, 0.1, 1) both;
  animation-delay: calc(var(--index) * 30ms);
}
@keyframes rise {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

`--index` 由渲染层写入（`style="--index:3"`）。**纪律**：`animation-fill-mode: both` 必写，否则延迟期间元素以「已可见」状态闪一下再开始动。

### 3.4 Vue / Svelte / GSAP 的等价写法

- **Vue `<TransitionGroup>`**：用 `:css="false"` + JS hooks，把 index 写进 `data-index`，`delay: el.dataset.index * 0.15`（官方示例用 GSAP `onComplete: done`）。**必须调用 `done()`**，否则 Vue 认为动画没结束、元素永不移除。
- **Svelte**：`transition:` 是双向可反转的（官方原文 "smoothly reversed while the transition is in progress"）——这是它相对 CSS 的最大优势。`transition:fade` 默认 local，加 `|global` 才在父块销毁时也播。自定义 transition 返回 `{ delay, duration, easing, css(t,u) }`，`css` 走 Web Animations API 可**脱离主线程**；能用 `css` 就别用 `tick`（`tick` 每帧回调在主线程）。
- **GSAP**：`gsap.timeline()` 的 position 参数（`"+=0.1"` / `"<"` / `"<0.2"`）本质就是串行/并行/重叠三种结构；`stagger` 支持 `each` / `from` / `grid`。许可为自定义（核心免费，商业插件需授权），入库前确认条款。

### 3.5 中文长列表与「逐字动画」陷阱

- 中文无词间空格，**逐字 stagger 会破词**（`motion-system.md` §9 已给结论）。中文列表按「整行」交错，不要按字符交错。
- 中文 B 端表格 20 行数据：逐行 stagger 是反模式，用户来读数据不是看动画。用整表 `opacity` 150ms 淡入即可。
- 交错只在**首次呈现 / 新增一批**时用。筛选、排序、翻页复用同一批 DOM 时，用 FLIP 位移（§4）而不是重新入场。

---

## 4. FLIP：共享元素位移的通用算法（First · Last · Invert · Play）

**来源**：Paul Lewis（Aerotwist, 2015-02，2022-05 更新），Google I/O 2015 与 Chrome Dev Summit 站点的实际做法。它**不是框架，是一种思路**：把逐帧的昂贵布局计算预先算完，只把 `transform` / `opacity` 留给逐帧。

### 4.1 四步与精确算式

| 步 | 动作 | 代码 / 算式 |
|---|---|---|
| **F** First | 变化前读位置尺寸 | `const first = el.getBoundingClientRect()` |
| **L** Last | 直接把元素放到最终状态，再读一次 | `el.classList.add('final'); const last = el.getBoundingClientRect()` |
| **I** Invert | 用 transform 把它**视觉上拉回** First | `invertY = first.top − last.top`；`invertX = first.left − last.left`；`scaleX = first.width / last.width`；`scaleY = first.height / last.height`；`transform-origin: top left` |
| **P** Play | 打开过渡、移除 invert，让它跑到 Last | `requestAnimationFrame(() => el.style.transform = '')` 或 `el.animate([{transform: t(invert)}, {transform: 'none'}], {duration: 300})` |

**原文 WAAPI 版本**（可直接抄，含官方给的曲线）：

```javascript
var first = el.getBoundingClientRect();
el.classList.add('totes-at-the-end');
var last = el.getBoundingClientRect();
var invert = first.top - last.top;
var player = el.animate([
  { transform: `translateY(${invert}px)` },
  { transform: 'translateY(0)' }
], {
  duration: 300,
  easing: 'cubic-bezier(0,0,0.32,1)',
});
player.addEventListener('finish', tidyUpAnimations);
```

### 4.2 为什么快：100ms 响应窗口

原文核心论断：「**There is a window of 100ms after someone interacts with your site where you're able to do work without them noticing**」。

- 交互后的 100ms 内，用户仍觉得「页面立刻响应了」；这段时间可以用来做 `getBoundingClientRect()` / `getComputedStyle()` 这类**强制同步布局**的昂贵预计算。
- 预计算完成后，动画本身只剩 `transform` + `opacity`，走合成器、不触发 paint，稳 60fps。
- **硬约束**：预计算必须落在 100ms 内。超过就「appear non-responsive」，用 DevTools 盯这个预算。

### 4.3 三条原文 caveat（工程上最容易踩）

1. **别超 100ms 窗口**——批量元素时先全部读、再全部写（§14），不要「读一个写一个」。
2. **编排时别互相踩**——原文："that's going to interrupt the animation that's in flight, which is bad"。两个 FLIP 不能同时重新测量；预计算放在 idle 或响应窗口内，且**同一时刻只允许一个 FLIP 编排在跑**（与 View Transitions 的「单例」规则同源，§6.6）。
3. **内容会缩放失真**——用 `scale` 模拟尺寸变化时，子元素、文字、`border-radius`、`box-shadow` 会被拉伸。解法：拆成独立元素分别 FLIP；或只 FLIP 位置、尺寸用 snap（Motion 的 `layout="position"` 就是这个思路）。

### 4.4 FLIP vs View Transitions 的选型

| | FLIP（手写 / Motion `layout`） | View Transitions API |
|---|---|---|
| 原理 | 真实 DOM 用 transform 补间 | 浏览器给旧/新状态拍**快照**，在伪元素树上动画 |
| 中途可交互 | ✅ 全程是真实 DOM | ⚠️ 旧快照是静态图不可交互，新快照是 live DOM 可交互 |
| 需要唯一 name | ❌ 不需要 | ✅ `view-transition-name` 必须唯一，重复会 abort |
| 滚动变化 | 可用 `layoutScroll` / `layoutRoot` 补偿 | ❌ 官方列出 "Doesn't account for scroll"：滚动变化会被错误计入位移 |
| 嵌套延迟元素 | Motion 用 parent-relative 计算，不会被父级落下 | ❌ 官方列出 "No relative animations"：带 delay 的子元素会被落下 |
| 浏览器支持 | 全平台（transform 是古董级能力） | Chrome 111+（SPA）/ 126+（MPA），需降级 |
| 结论 | **默认选它**；需要精确控制中途状态、多元素相对动画时必选 | 跨文档 MPA、想少写代码、且能接受快照语义时选 |

---

## 5. 列表增删与重排：四种操作的动画策略

列表是动效 bug 最密集的场景，因为**同一批 DOM 会经历四种完全不同的变化**，而多数人只写了「入场」一种。

| 操作 | 视觉目标 | 正确做法 | 常见错 |
|---|---|---|---|
| **新增** | 新项淡入 + 其余项平滑让位 | 新项 `@starting-style` / `enter-from`，其余项 FLIP 或 `.list-move` | 其余项瞬间跳位 |
| **删除** | 旧项淡出 + 其余项平滑合拢 | 旧项 `position: absolute` 脱离布局流，其余项 FLIP | 旧项还占位 → 合拢算错，或 DOM 立刻 remove 导致退场看不见 |
| **重排 / 筛选** | 保留项从旧位置滑到新位置 | FLIP（或 `layout` / `.list-move`） | 整列表重新入场（用户失去空间连续性） |
| **整批替换（翻页）** | 旧批出 + 新批入 | `mode="wait"` 串行，或交叉淡入 | 新旧批同时占位导致高度跳变 |

### 5.1 key 稳定性是所有列表动画的前提

**官方一致口径**（Motion / Vue / React 三家都写了）：

- Motion `AnimatePresence`：「Direct children must each have a unique `key`」；用 `index` 作 key 是 bad，因为重排后 index 不再对应同一个 item → 应用 `item.id`。
- Vue `<TransitionGroup>`：「Elements inside are **always required** to have a unique `key` attribute」。
- 原因：框架靠 key 判断「哪个元素还在、哪个走了、哪个换了位置」。key 错了，退场动画会挂到错误的元素上，FLIP 的 First/Last 配对也会错。

### 5.2 退场元素必须脱离布局流（Vue 官方解法）

```css
.list-move,
.list-enter-active,
.list-leave-active { transition: all 0.5s ease; }
.list-enter-from,
.list-leave-to { opacity: 0; transform: translateX(30px); }
/* 关键一行：离开项脱离布局流，其余项的位移才算得对 */
.list-leave-active { position: absolute; }
```

### 5.3 AnimatePresence 的三种 mode（Motion 官方）

| mode | 行为 | 适用 |
|---|---|---|
| `sync`（默认） | 进出同时发生，不干预排序与布局 | 元素位置不冲突；冲突时自己用 `position:absolute` 解决 |
| `wait` | 新的等旧的**退场完**再入场 | 一次只呈现一个信息（轮播、向导）。**只支持一个 child** |
| `popLayout` | 退场元素被「弹出」布局，周围元素立刻 reflow | 配合 `layout` 做列表删除 |

**三个官方排错点**（照抄）：
1. `AnimatePresence` 必须**在**卸载条件**外面**：`<AnimatePresence>{isVisible && <C/>}</AnimatePresence>` ✅；`isVisible && <AnimatePresence><C/></AnimatePresence>` ❌（它自己被卸载了就管不了退场）。
2. `mode="popLayout"` 下，直接子组件是自定义组件时必须 `forwardRef` 把 ref 透传到 DOM 节点。
3. `popLayout` 靠 `position:absolute` 实现；任何带 transform 的父元素会成为 offsetParent，因此**动画父容器必须设 `position` 非 `static`**（官方示例 `style={{ position: "relative" }}`）。

**混合 exit + layout 动画时要包 `LayoutGroup`**：因为两个组件若不同时 re-render，出于性能另一个检测不到自己的布局变化；`LayoutGroup` 让组内任一组件检测到变化时全组一起触发布局动画。

### 5.4 View Transitions 的列表方案：`match-element`

给每个列表项手写唯一 `view-transition-name` 太笨重，浏览器提供 `view-transition-name: match-element`（MDN 官方）：自动给所有选中元素设置唯一名称。配套的 `view-transition-class` 只能**去重动画样式**，不能替代唯一名称（Chrome DevRel 原文 Important 提示）。

```css
#cards-wrapper > div {
  view-transition-name: match-element;  /* 自动唯一命名 */
  view-transition-class: card;          /* 统一套同一份动画样式 */
}
html::view-transition-group(.card) { animation-timing-function: var(--bounce); }
```

> **`view-transition-class` 的边界**：它只是把多个快照归到一个 class 好写 CSS，**名字该唯一还得唯一**。误以为「加了 class 就不用唯一名」是常见误解。

---

## 6. 共享元素转场 A：View Transitions 完整机制

### 6.1 六步流程（MDN 原文顺序）

1. **触发**：SPA 调 `document.startViewTransition(updateCallback)`；MPA 由同源导航触发（两页 CSS 都写 `@view-transition { navigation: auto }`）。
2. **拍旧快照**：对 view transition scope 内、声明了非 `none` `view-transition-name` 的元素拍**静态图像快照**。默认 scope 是整个 document（`document-scoped`）或调用元素子树（`element-scoped`）。
3. **执行 DOM 更新**：`updateCallback` 被调用；成功后 `updateCallbackDone` fulfill。
4. **拍新快照 + 建伪元素树**：新视图是 **live / interactive DOM region**；伪元素树建成后 `ready` fulfill。
5. **动画运行**：旧快照 opacity 1→0，新快照 0→1（cross-fade）；`::view-transition-group` 同时补间 width/height/transform。
6. **结束**：快照销毁，`finished` fulfill，新页面完全可见可交互。`waitUntil(promise)` 可延后 finished。

**快照语义的关键差别**（MDN "An aside on snapshots"）：旧 UI 快照是**静态图**，用户不能在它退场时交互；新 UI 快照是**交互式 DOM 区域**，用户可以在入场过程中就开始点。所以「转场期间禁止交互」不是 API 强加的，是开发者自己要决定的策略。

### 6.2 伪元素树（原文结构）

```
root
  ├─ ::view-transition                          # overlay 根，盖在所有内容之上
  │  └─ ::view-transition-group(root)
  │     └─ ::view-transition-image-pair(root)
  │        ├─ ::view-transition-old(root)       # 旧视图静态快照
  │        └─ ::view-transition-new(root)       # 新视图 live 快照
  ├─ head
  └─ body …
```

- `::view-transition-old()` / `new()` 都按 **replaced content** 渲染（像 `<img>`/`<video>`），因此可以用 `object-fit` / `object-position`。
- 同时影响 old/new 的样式**推荐写在 `::view-transition-group()` 上**（MDN：因层级与 UA 默认样式，写在 group 上会被两者继承），也避免 group 与 old/new 的 duration 不一致。
- `*` 可作伪元素标识符匹配所有快照；`::view-transition-group(.card)` 用 `view-transition-class` 批量选中。
- MPA 的伪元素树**只在目标文档可用**；要双向转场，两个文档都要写 CSS。

### 6.3 默认动画精确值（W3C CSS View Transitions Level 1 UA stylesheet 原文）

```css
:root::view-transition-group(*) {
  position: absolute;
  top: 0;
  left: 0;
  animation-duration: 0.25s;
  animation-fill-mode: both;
}
:root::view-transition-image-pair(*),
:root::view-transition-old(*),
:root::view-transition-new(*) {
  animation-duration: inherit;
  animation-fill-mode: inherit;
  animation-delay: inherit;
  animation-timing-function: inherit;   /* 由 group 统一定时，默认即 ease */
  animation-iteration-count: inherit;
  animation-direction: inherit;
  animation-play-state: inherit;
}
@keyframes -ua-view-transition-fade-out { to   { opacity: 0; } }
@keyframes -ua-view-transition-fade-in  { from { opacity: 0; } }
@keyframes -ua-mix-blend-mode-plus-lighter {
  from { mix-blend-mode: plus-lighter }
  to   { mix-blend-mode: plus-lighter }
}
```

- **默认 0.25s（quarter-second）、`ease`**、cross-fade、`fill-mode: both`；子伪元素全部 `inherit` 定时，因此**改时长写 group 一处即可**。
- `::view-transition-group()` 的 `width`/`height`/`transform` 动画值**不是静态 CSS**，由 *dynamic view transition style sheet* 在转场开始时按旧/新元素的 border box 尺寸与 screen space transform 动态生成。
- 全部动画是 CSS animations → 可用普通 CSS 覆盖（`animation-name` / `animation-duration` / `animation-delay`）。

### 6.4 `view-transition-name` 唯一性（最容易炸的一条）

| 规则 | 官方表述 |
|---|---|
| 唯一性 | 每个已渲染元素的 `view-transition-name` 必须唯一；两个同时渲染的元素同名 → `ready` reject、transition **abort / skipped** |
| 跨状态配对 | 旧状态元素叫 `foo`、新状态另一个元素叫 `foo` → **视为同一概念实体的两个视觉状态并配对**（这正是共享元素转场的原理） |
| 失败不阻断状态变更 | `updateCallback` **always called**，即使因重名无法转场；"It's only the visual transition that's skipped, not the underlying state change" |
| promise 表现 | `ready` 因重名/回调 reject 而 **reject**；`finished` 仍 **fulfill**（最终状态到达） |
| 有效值 | 唯一 `<custom-ident>`、`none`、`match-element`；`none/auto/match-element` 不能当自定义标识符 |
| 作用域 | `view-transition-name` 是 tree-scoped name；`view-transition-scope` 可把快照发现限制在某个子树（element-scoped 转场） |
| 页面隐藏 | 若 `document` 的 visibility state 为 `hidden` 时调用，transition **整段跳过** |

> **工程纪律**：动态设置 name 后必须在转场结束清理；尤其在 MPA + bfcache 场景（§8.2），残留 name 会在用户按返回键时造成重名 → 转场被跳过。

### 6.5 三个 Promise 与 `skipTransition()`

| Promise | 时机 | 用途 / 陷阱 |
|---|---|---|
| `updateCallbackDone` | DOM 更新回调完成 | 主流程**可以**等它（确认状态变更完成） |
| `ready` | 伪元素树建成、动画将开始 | 自定义 JS 动画（如 `document.documentElement.animate(..., {pseudoElement: '::view-transition-new(root)'})`）；**会 reject → 必须 try/catch，不要让主流程 await 它** |
| `finished` | 动画结束、快照销毁、新视图可交互 | **清理状态用它**（即使被 skip 仍 fulfill）；只在 `updateCallback` 返回 rejected promise 时 reject |

`skipTransition()` **只跳过动画，不跳过 DOM 更新**（官方："This won't skip calling `updateCallback`"`）。这是把「用户关闭动效偏好」接入 View Transitions 的标准入口，也用于并发时显式结束旧转场。

**`types`**（Chrome DevRel 现代写法，替代已 deprecated 的 root class name 方案）：

```js
const t = document.startViewTransition({
  update: updateTheDOMSomehow,
  types: ['slide', direction],   // 数组 → 自动转 Set-like
});
t.types.clear(); t.types.add('forwards'); t.types.delete('slide');
// CSS: html:active-view-transition-type(forwards) { ... }
```

`types` 只在 capturing / performing 期间生效，结束后自动清理；`:active-view-transition` 匹配任意进行中的转场。因为 types 只在转场期生效，可以用它在转场期间**临时设置或取消** `view-transition-name`。

### 6.6 并发与中断：单例规则

> **"Only one view transition is allowed to run at a time. If a new view transition starts while one is already running, the old transition skips to the end."**

- 转场是**单例**。快速连点导航时，旧转场被强行跳到终点，DOM 状态仍按序落地。
- 显式处理：持有 `currentTransition`，新请求先 `skipTransition()` → `await updateCallbackDone` → 再起新的；清理逻辑放 `await t.finished` 的 `finally`。
- **`startViewTransition()` 的 callback 期间页面被冻结**（render suppressed）。因此**网络请求必须放在调用之前**，callback 里只做必要的 DOM 更新；否则用户会觉得整页卡住。
- 把转场当 enhancement：`switchView()` 不该因 `ready` reject 而 reject，正确做法是等 `updateCallbackDone`（或 `finished`）。

---

## 7. 共享元素转场 B：layoutId 与 Motion 布局动画

Motion（原 Framer Motion）用 `layout` 系列 prop 在**真实 DOM** 上做 FLIP，不需要浏览器快照。

| prop | 作用 | 官方要点 |
|---|---|---|
| `layout` | 自动动画该组件自身的尺寸/位置变化 | 用 CSS `transform`（translate + scale）而非真的动 width/height，避免 paint |
| `layout="position"` | 只动位置、尺寸直接 snap | 专治「图片/文字宽高比变化时被拉伸」 |
| `layoutId` | 匹配两个不同组件，做共享元素转场 | 新组件带相同 `layoutId` 进入时，从旧组件位置动画出来；旧组件仍在页面上时两者**自动 crossfade** |
| `LayoutGroup` | 同步多个组件的布局动画 | 解决「两个组件不同时 re-render、但互相影响布局」时检测不到变化 |
| `layoutScroll` | 可滚动容器上必须加 | 让 Motion 计入 scroll offset |
| `layoutRoot` | `position: fixed` 容器上必须加 | 计入页面滚动偏移 |
| `layoutAnchor` | 改变测量锚点 | `{x:0.5,y:0.5}` 居中心；取值 0–1，0=top/left，1=bottom/right |
| `transition.layout.path` | 改直线运动为弧线 | `arc()`，也适用 `layoutId` 共享转场 |

**官方 caveat 清单**：

- 布局变化要通过 `style` / `className` 触发，**不要用 `animate` / `whileHover`** 去改布局（`layout` 自己负责动画）。
- 共享布局动画时，**使用「动画到」的那个元素上定义的 transition**（"the transition defined for element we're animating to will be used"）。
- `transform: scale()` 会拉伸子元素、`border-radius`、`box-shadow`：给直接子元素也加 `layout`（Motion 会算 counter-scale）；`border-radius`/`box-shadow` 必须用 `style`/`animate` 设置才会被自动校正。
- 真实 `border` 不要动：改 border 会触发布局重算、且 1px 下限限制了 scale correction → 用父级 padding 模拟边框。
- `display: inline` 元素不生效（浏览器不对 inline 应用 transform）；**SVG 不支持 layout 动画**（直接动 `cx` 等属性）；水平窗口 resize 期间布局动画被主动阻断。
- 滚动条出现会改变布局 → 用 `body { overflow-y:auto; scrollbar-gutter: stable; }` 预留空间。
- 要让元素动画回原位，用 `AnimatePresence` 把它留在 DOM 直到退场结束。

**Motion 官方给出的两条 View Transitions 差异**（选型直接依据）：

| 差异 | 说明 |
|---|---|
| 多个同名元素 | Layout animations **允许**多个元素带同一 `layoutId`；View Transitions 在旧元素未移除时会 break |
| 滚动 | View Transitions **不计算 scroll**，页面滚动变化时元素会错误地把滚动量算进位移 |
| 相对动画 | View Transitions **没有 relative animations**：嵌套元素带 delay 会被父级「落下」；Motion 用 parent-relative 计算不会 |

---

## 8. 跨文档转场（MPA）与导航方向类型

### 8.1 触发与版本

- **无需 JavaScript**：同源跨文档导航 + 两个文档 CSS 都写 `@view-transition { navigation: auto; }` 即触发。
- Chrome **111+** 支持 same-document（SPA），**126+** 支持 cross-document（MPA）。当前仅同源（same-origin）；重定向链中若有跨源 URL，`PageSwapEvent.activation` 返回 `null`。
- `pageswap`（`PageSwapEvent.viewTransition` + `.activation`）在旧文档、导航前触发；`pagereveal`（`PageRevealEvent.viewTransition`）在新文档首次渲染时触发（含 bfcache / prerender 激活）。可用它们按 from/to URL 定制进出场动画。

### 8.2 bfcache 的隐藏陷阱（MDN 明确警告）

在 `pageswap` 里给元素**临时**设置 `view-transition-name` 后，转场结束必须移除。原文："If we left them set, they would persist in the page state saved in the bfcache upon navigation." 用户按返回键时，`pagereveal` 又会给另一批元素设同名 → 重名 → **view transition is skipped**。

```js
window.addEventListener('pageswap', async (e) => {
  if (!e.viewTransition) return;
  markClickedCard();                       // 临时设 view-transition-name
  await e.viewTransition.finished;
  clearNames();                            // 必须清理，别带进 bfcache
});
```

### 8.3 首帧稳定化

跨文档转场要求「关键内容已解析」才有稳定快照。Chrome DevRel 建议用 render blocking 保证：① 关键样式已加载应用；② 关键脚本已执行；③ 用户首屏可见的 HTML 已解析。

```html
<link rel="expect" href="#hero" blocking="render">
```

- `script` / `link` / `style` 带 `blocking="render"` 时**必须位于 `<head>`** 才生效；`<link rel="expect">` 可加 `media` 让窄屏/宽屏阻塞不同数量的内容。
- 默认样式表本身就是 render blocked（除非脚本动态插入）。

---

## 9. 动画状态机：四态/六态模型与 XState

### 9.1 经典四态（react-transition-group `<Transition>` 官方）

```
        in = true                  timeout 结束
  ┌────────────────►  entering  ──────────────►  entered
  │                                                 │
exited ◄──────────  exiting   ◄────────────────────┘
        timeout 结束           in = false
```

四个主状态：`'entering'`、`'entered'`、`'exiting'`、`'exited'`。`in` prop 切换时进入对应阶段，`timeout` 毫秒后自动切下一状态。children 作为函数时收到当前状态字符串。

**六个回调**（按触发顺序）：`onEnter`（进入 entering 前）→ `onEntering` → `onEntered`；`onExit` → `onExiting` → `onExited`。`addEndListener` 可用 `transitionend` 自定义结束判定，`timeout` 仅作兜底。

**配套 props**：`nodeRef`（推荐，避免 deprecated 的 `findDOMNode`）、`mountOnEnter` / `unmountOnExit`（默认子组件保持挂载）、`appear`（首次挂载也播入场）、`enter` / `exit`（分别开关）、`timeout` 可给 `{appear, enter, exit}` 三档（默认 enter/exit = 0，appear 取 enter 值）。

> **这四态就是动画状态机的最小完备模型**。任何框架的进出场动画，本质上都在实现它；自己写时先画这张图，别直接写 `setTimeout`。

### 9.2 为什么必须是状态机（XState / Stately 官方定义）

- 状态机「capture all the states, events and transitions」，好处是「**find impossible states and spot undesirable transitions**」。
- 转迁是**确定性**的（deterministic）：同一 (state, event) 永远指向同一 next state。
- 状态（asleep/awake）、事件触发转迁、initial state 只能有一个顶层、final state 用双边框、parent/compound state 含子状态、atomic state 无子状态、parallel state 的所有 region 同时激活、self-transition 是「doing something, not going somewhere」。
- Statechart 在 FSM 上加了 **hierarchy / concurrency / communication**，能表达「动画在跑，同时数据在加载」这种并行。

**XState 最小代码**（官方原文）：

```js
import { createMachine } from 'xstate';
const machine = createMachine({
  id: 'dialog', initial: 'closed',
  states: {
    closed: { on: { OPEN: 'entering' } },
    entering: { on: { ANIM_END: 'open', CANCEL: 'exiting' } },
    open: { on: { CLOSE: 'exiting' } },
    exiting: { on: { ANIM_END: 'closed', CANCEL: 'entering' } },
  },
});
```

### 9.3 状态 × 事件矩阵（可直接贴进设计交付文档）

| 当前状态 \ 事件 | `OPEN` | `CLOSE` | `ANIM_END` | `CANCEL`（二次点击） |
|---|---|---|---|---|
| `closed` | → entering | — | — | — |
| `entering` | — | → exiting | → open | → exiting |
| `open` | — | → exiting | — | — |
| `exiting` | → entering（反向） | — | → closed | → entering |

**关键收益**：「快速连点」不再是一堆 `if`，而是 `exiting` 收到 `OPEN` → 反向回 `entering`，且**从当前插值继续**（§10）。`isLoading && isSuccess` 这类不可能状态在建模阶段就被消灭。

**并行状态的用法**：把「动画轴」（entering/open/exiting）与「数据轴」（idle/loading/success/error）设为两个并行 region——动画结束不该被网络请求阻塞，网络失败也不该把弹窗强行关掉。这比用两个 boolean 更不容易漏态。

---

## 10. 中断与取消：可中断性的工程定义

`motion-system.md` 说「交互反馈一律用 `transition`（可中断）」——这里给出**可中断的精确定义**与实现手段。

### 10.1 定义

> **可中断 = 动画进行中收到新事件时，从「当前视觉值」平滑迁移到新目标，而不是跳回起点、跳过终点或卡在中间。**

三种打断策略，按语义选：

| 策略 | 手段 | 适用 |
|---|---|---|
| **从当前值重启** | `transition` 天然支持；WAAPI 先读 `getComputedStyle` 当前值作新动画首帧 | 按钮 hover/按压、拖拽、开关 |
| **叠加** | WAAPI `composite: 'add'` / `'accumulate'` | 多个独立动画同时作用于同一属性（如基础位移 + 抖动） |
| **跳到终点** | `Animation.finish()`、`ViewTransition.skipTransition()` | 用户关闭动效、并发转场、页面即将卸载 |

### 10.2 WAAPI 播放控制（MDN 精确语义）

| 方法 | 行为 |
|---|---|
| `play()` / `pause()` | 播放 / 暂停；`Element.animate()` **立即播放**，想延迟就定义后立刻 `pause()`，或用 `new Animation()`（不调 `play()` 就不播） |
| `cancel()` | 中止动画并移除其效果，触发 `oncancel`；`finished` promise **reject** |
| `finish()` | 跳到终点，触发 `onfinish` |
| `reverse()` | 把 `playbackRate` 设为负值倒放 |
| `commitStyles()` | 把动画当前计算样式写进目标元素 `style` 属性——**推荐用它持久化终态**，而不是长期挂 `fill: forwards` |
| `persist()` | 阻止浏览器自动移除，`replaceState` 变为 `persisted` |
| `updatePlaybackRate()` | 平滑改速率；**直接设 `playbackRate` 不平滑**（官方："we use `updatePlaybackRate()` instead of setting the `playbackRate` directly since that produces a smooth update"） |
| `Document.getAnimations()` | 遍历页面所有动画；无障碍示例用它把所有 `playbackRate` **减半** |

**为什么不要用 `fill: forwards` 长期保态**（官方两条理由）：① 浏览器得维护仍 active 的动画状态，持续耗资源；② 动画样式在 cascade 中优先级高于指定样式，之后想覆盖很难。

### 10.3 自动移除 filling animations 的 5 个条件（全部满足才移除）

1. 动画处于 filling（正向播放时 `fill: forwards`、倒放时 `backwards`、或 `both`）；
2. 已 finished（因 fill 仍有效果）；
3. timeline 单调递增（`DocumentTimeline` 恒真；`scroll-timeline` 可能倒退）；
4. **不是**由声明式标记（CSS）控制；
5. 其 `AnimationEffect` 的每一个样式效果都被另一个同样满足上述条件的动画覆盖。

移除时触发 `remove` 事件；`replaceState` 三值：`removed` / `persisted` / `active`。前四条保证「没有 JS 干预时效果永不改变」，第五条保证「它已完全不再影响任何样式」。这套机制正是为了防住「同一元素叠了一堆 forwards-fill 动画 → 内存泄漏」。

### 10.4 `transitionend` / `animationend` 的四个坑

1. **冒泡**：子元素过渡结束也会冒泡到父容器 → 必须检查 `event.target === el` 与 `event.propertyName`。
2. **`cancel()` 不触发**：动画被取消时不发 `animationend`，只发 `cancel` 事件 → 清理逻辑不能只挂在 end 上。
3. **`display:none` / 元素移除**：退化时不触发，必须配超时兜底（`react-transition-group` 的 `timeout` 就是这个兜底）。
4. **多属性多次触发**：`transition: opacity, transform` 会触发两次 → 用计数器或只监听一个属性。

**统一纪律**：清理状态挂在 `finished`（Promise）+ `finally`，而不是挂在 DOM 事件上。这也是 Chrome DevRel 推荐 `await transition.finished` 做清理的原因——即使转场被 skip 它也 fulfill。

---

## 11. WAAPI 精确参数表（KeyframeEffect / Element.animate）

以下全部为 MDN `KeyframeEffect()` 与 Using WAAPI 的**官方默认值**，与 CSS 动画默认值不同处已标出：

| 参数 | 默认 | 取值 / 说明 |
|---|---|---|
| `duration` | **0** | 毫秒；**0 等于不播放**。WAAPI 只吃毫秒（`3000` 不是 `3s`） |
| `delay` | 0 | 毫秒 |
| `endDelay` | 0 | 毫秒；主要用于「基于前一个动画结束时刻」排序 |
| `easing` | **`linear`** | ⚠️ CSS `animation-timing-function` 默认是 `ease`。WAAPI 默认线性，这是最容易造成的视觉不一致 |
| `direction` | `"normal"` | `normal` / `reverse` / `alternate` / `alternate-reverse` |
| `fill` | `"none"` | `none` / `backwards` / `forwards` / `both` |
| `iterations` | `1` | `Infinity`（JS 关键字），**不是**字符串 `"infinite"` |
| `iterationStart` | `0.0` | `0.5` = 从第一次迭代中点开始；2 次迭代会在第三次的中点结束 |
| `composite` | **`replace`** | `replace`（覆盖）/ `add`（拼接，如 `translateX(-200px) rotate(20deg)`）/ `accumulate`（智能累加，`blur(2)`+`blur(5)` → `blur(7)`） |
| `iterationComposite` | `replace` | `accumulate` / `replace`，控制迭代间如何累积 |
| `pseudoElement` | — | 字符串如 `"::before"`；View Transitions 自定义动画用 `'::view-transition-new(root)'` |

**关键帧格式**：数组，每个对象对应 CSS 的一个 key；**至少两个关键帧**（某些浏览器只有一个会抛 `NotSupportedError` / `DOMException`）；未写 `offset` 时按数量等分（三帧 → 中间帧在 50%）；`offset: 0.3` 可显式指定。`getComputedTiming()` / `effect` / `currentTime` / `activeDuration` 用来算播放进度（官方 Alice 示例：8 秒动画，设 `currentTime = 4` 即中点）。

> **单位统一表**（贴进项目规范）：CSS 秒（`0.3s`）· WAAPI 毫秒（`300`）· Motion 秒（`0.3`）· React Transition Group 毫秒（`timeout={300}`）。混用是「动画快了 10 倍 / 慢了 10 倍」的头号原因。

---

## 12. CSS 入场/退场状态机：`@starting-style` 四件套

### 12.1 三个状态，不是两个（MDN 原文）

`@starting-style` 定义「元素**没有 previous state** 时的起始值」，让 CSS transitions 在首次渲染或从 `display:none` 变可见时也能触发。

| 状态 | 何时生效 |
|---|---|
| **starting-style state** | 元素首次渲染进 DOM，或从 `display:none` → 可见值时 |
| **transitioned state**（如 `:popover-open` / `[open]`） | 打开后的目标态 |
| **default state** | 元素的基础规则 |

**关键**：从目标态**退回去时不再用 `@starting-style`**，而是过渡回 default state。所以**入场与退场可以是不同的两条路径**（官方示例：div 首次加入 red→blue，移除 `showing` 后 blue→yellow，而不是回 red）。这正是设计「下进上出」弹窗的原生做法。

### 12.2 四件套（缺一不可）

```css
/* 0. IS-OPEN STATE：目标态 + transition 清单 */
dialog[open] {
  translate: 0 0;
  opacity: 1;
}
/* 1. BEFORE-OPEN STATE：必须写在原规则之后 */
@starting-style {
  dialog[open] { translate: 0 100vh; opacity: 0; }
}
/* 2. EXIT STATE：默认态即退场终点 */
dialog {
  translate: 0 100vh;
  opacity: 0;
  transition: translate 0.7s ease-out, opacity 0.7s ease-out,
              display 0.7s allow-discrete,
              overlay 0.7s allow-discrete;
}
```

| 件 | 作用 | 漏了会怎样 |
|---|---|---|
| `@starting-style` | 给入场提供 from 值 | 元素直接出现，**入场动画不发生** |
| `display` 进 transition 清单 | 让元素在进出全程可见 | **退场动画看不见**，元素瞬间消失 |
| `overlay` 进 transition 清单 | 把「退出 top layer」推迟到动画结束 | popover/dialog 立刻被祖先裁剪/遮盖，看不见平滑退场 |
| `transition-behavior: allow-discrete` | 允许离散属性参与过渡 | 上述 display/overlay 都不生效 |

### 12.3 `allow-discrete` 的 50% 规则与两个例外（MDN 原文）

- 初始值 `normal`；`allow-discrete` 让离散属性也参与过渡。
- 离散属性一般在**缓动进度 50%** 处翻转两个值。
- **例外**：`display: none` / `content-visibility: hidden`——`none → block` 在 **0%** 翻（全程可见），`block → none` 在 **100%** 翻（全程可见）。否则入场/退场动画会被截断。
- **简写陷阱**：`transition` 简写会把 `transition-behavior` 重置回 `normal`，因此独立声明 `transition-behavior: allow-discrete` **必须写在简写之后**；或在简写里逐属性写 `display 0.5s allow-discrete`。多个离散属性要**逐个**加。
- **顺序陷阱**：`@starting-style` 与原规则**同 specificity**，写在前面会被原规则覆盖 → **必须放在后面**（Chrome DevRel 与 MDN 都写了 Important note）。
- **适用范围**：只对 **CSS transitions** 有意义；用 CSS animations 实现同类效果时不需要它。
- **版本**：Chrome 116 起 `display`/`content-visibility` 可进 keyframes；Chrome 117 起 `transition-behavior` / `@starting-style` / `overlay`；MDN 标注 **Baseline 2024 · Newly available（自 2024-08）**。

### 12.4 DOM 增删：先播退场，再移除节点

MDN 示例流程：点击关闭 → 给元素加 `.fade-out`（其内设 `display:none` + `opacity/scale` 终点）→ **`setTimeout(() => el.remove(), 1000)`** 延迟移除，确保动画播完再删 DOM。

> 这条与 §9 的四态模型完全一致：`exiting` 状态必须在 DOM 里存在到 `ANIM_END` 才切 `exited`。Vue 的 `done()`、Motion 的 `AnimatePresence`、React 的 `unmountOnExit` 都是这个机制的封装。

---

## 13. 编排层编排的无障碍降级（WCAG 2.3.3 / 2.2.2 / prefers-reduced-motion）

### 13.1 三条 WCAG 条款原文口径

| 条款 | 级别 | 要求 |
|---|---|---|
| **2.3.3 Animation from Interactions** | AAA | 「**Motion animation triggered by interaction can be disabled, unless the animation is essential** to the functionality or the information being conveyed.」 |
| **2.2.2 Pause, Stop, Hide** | A | 页面**自动**发起、超过 5 秒的运动内容必须可暂停/停止/隐藏（与 2.3.3 的区别：一个是交互触发，一个是自动发起；同一动画可能同时违反两条） |
| **2.3.1 Three Flashes** | A | 闪烁 ≤3 次/秒 |

**`motion animation` 的官方定义**：「addition of steps between conditions to create the illusion of movement or to give a sense of a smooth transition」。**颜色变化、模糊、opacity 变化（不改变感知的大小/形状/位置）不算 motion animation**（W3C 有 errata 修正 blur 表述）。这就是为什么降级时**保留色彩与透明度反馈**是合规的，而位移必须去掉。

**官方给的三条解法（任选其一）**：避免非必要动画 / 提供全局关闭开关 / 利用 UA 或 OS 的 reduce motion 偏好。充分技术：C39（CSS `prefers-reduced-motion`）、SCR40（JS 中 `matchMedia`）、Gx（用户自定义偏好）。

**触发后果不是「不好看」**：W3C 原文列举 vestibular disorder 反应包括 dizziness、nausea、migraine headaches，「potentially needing bed rest to recover」。

### 13.2 `prefers-reduced-motion` 精确语义（MDN）

- `no-preference`：用户未表态，该值求值为 **false**；`reduce`：求值为 **true**。
- `@media (prefers-reduced-motion)` **等价于** `@media (prefers-reduced-motion: reduce)`。
- 缩放/平移大物体是典型 vestibular 触发源；官方示例的降级做法是换成 `dissolve`（不改变尺寸的柔和变化）。
- 各系统开关位置：Windows 11「辅助功能 → 视觉效果 → 动画效果」、macOS「辅助功能 → 显示/移动 → 减少动态效果」、iOS「辅助功能 → 动态效果」、Android 9+「辅助功能 → 移除动画」、GTK/GNOME `gsettings set org.gnome.desktop.interface enable-animations false`、Firefox `about:config` 的 `ui.prefersReducedMotion`（0 全动画 / 1 减弱）。

### 13.3 编排层降级的四条纪律（本文件的差异化结论）

1. **整段跳过，不要逐个归零**。把 stagger 序列里每个元素的 `animation-duration` 都设成 1ms，结果是 N 个变化在一帧内重叠闪现——比不做降级更糟。正确做法：命中 reduce 时**取消交错**（`--index` 系数置 0、或整组只做 100ms opacity），或直接跳过整段编排。
2. **View Transitions 用 `skipTransition()` 接偏好**：Chrome DevRel 明确把 `skipTransition: true` 列为「site has a user preference to disable transitions」的标准做法。DOM 更新照常发生。
3. **WAAPI / Svelte 不受 CSS media query 影响**——⚠️ Svelte 官方 Accessibility 章节原文：「Transitions are driven by the Web Animations API rather than by CSS. A global `@media (prefers-reduced-motion: reduce)` rule that zeroes `transition-duration` and `animation-duration` therefore **has no effect on them**.」必须用 `prefersReducedMotion`（Svelte store）或 JS `matchMedia` 在**代码层**调整/禁用。同理，任何 `Element.animate()` 创建的动画都要在 JS 侧判断偏好。
4. **WAAPI 全局降级**：`document.getAnimations().forEach(a => a.updatePlaybackRate(0.5))`（MDN 无障碍示例是 halve playbackRate），或直接 `cancel()` + 落到终态。

> **结论**：`motion-system.md` §8.1 给的是 CSS 层降级模板；只要项目里出现 WAAPI / Svelte / View Transitions / JS 编排，**必须再补一层 JS 降级**，否则 CSS 模板形同虚设。

---

## 14. 性能：100ms 响应窗口、读写分离与快照开销

| 约束 | 精确值 / 规则 | 来源 |
|---|---|---|
| 响应窗口 | 交互后 **100ms** 内可做预计算而不被察觉 | Paul Lewis FLIP 原文 |
| 帧预算 | 60Hz = **16.67ms/帧**；120Hz = 8.33ms | `performance-design.md` §11 |
| 强制同步布局 | 读 `getBoundingClientRect()` 后立刻写样式 → 浏览器被迫提前 layout | FLIP 原文 "This forces a sync layout, so be careful" |
| 批量纪律 | **先全部读、再全部写**（`firsts[]` → `lasts[]` → 统一 `animate()`） | FLIP 两条 caveat 的工程解 |
| 快照开销 | 每个 `view-transition-name` 一张快照；**>6 个**退回手写 transform | `motion-system.md` §7.3 + 本文件 §6 |
| 冻结窗口 | `startViewTransition()` callback 期间页面冻结 → 网络请求前置 | Chrome DevRel |
| 可动属性 | 只有 `transform` / `opacity` 走合成层 | `motion-system.md` §8 |
| `will-change` | 只临时加、结束移除（常驻白吃显存 + 文字发虚） | 同上 |

**FLIP 批量模板**（先读后写，避免 N 次 sync layout）：

```js
const firsts = items.map(el => el.getBoundingClientRect());   // ① 全读
mutateLayout();                                              // ② 一次性改 DOM
const lasts = items.map(el => el.getBoundingClientRect());   // ③ 全读
items.forEach((el, i) => {                                    // ④ 全写
  const dy = firsts[i].top - lasts[i].top;
  if (!dy) return;
  el.animate([{ transform: `translateY(${dy}px)` }, { transform: 'none' }],
             { duration: 300, easing: 'cubic-bezier(0,0,0.32,1)' });
});
```

---

## 15. 跨框架实现矩阵与选型决策

| 方案 | 编排 | 共享元素 | 退出态 | 状态机 | 适用场景 |
|---|---|---|---|---|---|
| **原生 CSS** | `--index` 级联 / `@starting-style` | ❌ | `allow-discrete` + `setTimeout` | 手写 | 包体最小、无框架、小程序 |
| **WAAPI** | `delay` / `endDelay` / `composite` | 手写 FLIP | `cancel` / `commitStyles` | 手写 + promise | 需要精确控制播放速率、伪元素 |
| **View Transitions** | 伪元素树 + `types` | ✅ 原生 | 快照自动销毁 | `ready/finished` + `skipTransition` | SPA 路由 / MPA 跨文档 / 少代码 |
| **Motion for React** | variants + `stagger()` + `when` | `layoutId` | `AnimatePresence` mode | `useIsPresent` / `usePresence` | React 复杂交互、拖拽、共享元素 |
| **Vue** | `<TransitionGroup>` + `:css="false"` + GSAP | 手写 FLIP / `.list-move` | `.list-leave-active` + `done()` | 内置 hooks | Vue 列表增删、重排 |
| **Svelte** | `transition:` / `animate:flip` | `crossfade` | 块内元素留到全部结束 | 内置 + `prefersReducedMotion` | 轻量、需要可反转过渡 |
| **GSAP** | `timeline` position / `stagger` | Flip Plugin | `onComplete` | 自建 | 复杂时间轴、营销页 |
| **微信小程序** | WXSS `transition` / `@keyframes` | 手写 | 与 CSS 同 | 手写 | 包体敏感；**禁用废弃的 `wx.createAnimation`**；原生组件层级最高，弹层用 `cover-view` 或转场期临时隐藏 |

**选型决策树**：

```
跨文档 MPA？ ── 是 ──► @view-transition + types（需 Chrome 126+ 与降级）
   │否
React 项目且要共享元素/拖拽？ ── 是 ──► Motion layoutId + AnimatePresence
   │否
需要精确控制中途状态 / 相对动画 / 滚动补偿？ ── 是 ──► FLIP（手写或 Motion layout）
   │否
只是列表入场？ ── 是 ──► CSS --index 级联（≤6 项）或整组淡入（>6 项）
   │否
单元件进出场？ ──► @starting-style 四件套 / 原生 transition
```

---

## 16. 场景速查（16 条，直接取结论）

| 场景 | 结论 |
|---|---|
| 6 项列表依次入场 | `d=200ms, s=30ms` → 350ms ✅；父级 `when: "beforeChildren"` |
| 20 项表格加载 | **禁逐行 stagger**；整表 opacity 150ms 淡入 |
| 筛选项变化 | FLIP 位移保留项，**不要**整表重新入场 |
| 列表删一项 | 退场项 `position:absolute` 脱离布局流，其余项 FLIP/`layout` 合拢 |
| 弹窗连点开关 | 四态状态机，`exiting` 收到 `OPEN` → 反向 `entering` 且从当前值继续 |
| `dialog`/`popover` 进出场 | `@starting-style` + `display` + `overlay` + `allow-discrete` 四件套 |
| 卡片 → 详情页 | View Transitions 同名 `view-transition-name`（旧/新跨状态配对），或 Motion `layoutId` |
| 缩略图 → 大图（宽高比变） | Motion `layout="position"` 只动位置、尺寸 snap；VT 会拉伸内容 |
| SPA 路由快速连点 | 转场单例：显式 `skipTransition()` → `await updateCallbackDone` → 起新转场 |
| MPA 前进/后退不同动画 | `types: ['slide', direction]` + `:active-view-transition-type(forwards/backwards)` |
| bfcache 返回键转场失效 | `pageswap` 里临时设的 name 在 `finished` 后**必须清理** |
| 嵌套元素带 delay 被落下 | 别用 VT（无 relative animations），改 Motion parent-relative 或 FLIP |
| 页面转场时发生滚动 | 别用 VT（不计算 scroll），改 Motion `layoutScroll` / `layoutRoot` |
| `prefers-reduced-motion` + Svelte | 全局 CSS 归零**无效**，用 `prefersReducedMotion` store 在 JS 层禁用 |
| WAAPI 动画默认曲线不对 | 默认 `linear`，CSS 默认 `ease` → 显式写 `easing` |
| 动画结束后样式改不掉 | 用了 `fill: forwards` → 改 `commitStyles()` 持久化，`cancel()` 释放 |

---

## 17. 反模式（20 条，命中即扣分）

1. **用 `index` 作列表 key** —— 重排后退场动画挂到错误元素（Motion / Vue 官方都点名）。
2. **`AnimatePresence` 写在卸载条件里面** —— 它自己被卸载，管不了退场。
3. **`popLayout` 父容器还是 `position: static`** —— 退场元素 absolute 定位错乱。
4. **`>6` 项还逐项 stagger** —— 总时长超 400ms，最后一项要等 600ms+。
5. **入场用反向 stagger** —— 用户先看到最不重要的末尾项。
6. **把 stagger 序列每项 duration 归零当降级** —— N 个变化一帧内重叠闪现。
7. **以为全局 CSS `prefers-reduced-motion` 能管住 WAAPI / Svelte 过渡** —— 官方明确说无效。
8. **`view-transition-name` 重复** —— `ready` reject、转场 abort；MPA bfcache 残留是高发原因。
9. **误以为 `view-transition-class` 能替代唯一 name** —— 它只去重动画样式。
10. **在 `startViewTransition()` 回调里发网络请求** —— 页面冻结期间用户以为卡死。
11. **在主业务流里 `await transition.ready`** —— ready 会 reject，导致「DOM 已更新但函数报错」。
12. **`display` / `overlay` 没进 transition 清单** —— 退场动画根本看不见。
13. **`transition-behavior: allow-discrete` 写在 `transition` 简写之前** —— 被简写重置回 `normal`。
14. **`@starting-style` 写在原规则之前** —— 同 specificity，起始样式被覆盖。
15. **长期用 `fill: forwards` 保态** —— 资源占用 + cascade 优先级压过指定样式。
16. **直接设 `playbackRate` 改速率** —— 不平滑，应用 `updatePlaybackRate()`。
17. **只监听 `transitionend` 做清理** —— 冒泡、`cancel()`、多属性、`display:none` 四种情况都会漏。
18. **FLIP 里「读一个写一个」** —— N 次强制同步布局，突破 100ms 响应窗口。
19. **两个编排同时在跑还重新测量** —— 互相打断（FLIP 原文 caveat 2 / VT 单例规则）。
20. **用 `animate` / `whileHover` 去触发布局变化再配 `layout`** —— Motion 官方要求用 `style` / `className`。

---

## 18. 自检清单（20 条，动效编排交付前逐条过）

1. 判过层了吗（L1 单动效 / L2 编排 / L3 状态机）？有没有把简单反馈做成状态机、把列表增删当成单个 transition？
2. 编排结构归到**并行/串行/重叠/交错**哪一种了？总时长算过且 ≤400ms？
3. `n > 6` 时改成整组淡入或分组了吗？stagger 间隔在 20–40ms？
4. 入场正向、退场 `when: "afterChildren"`？父子层级顺序对吗？
5. 列表每项都有**稳定唯一 key**（不是 index）？
6. 退场元素脱离布局流了吗（`.list-leave-active { position:absolute }` / `popLayout`）？
7. `AnimatePresence` 在卸载条件**外面**？`popLayout` 父容器 `position` 非 static、自定义组件 `forwardRef`？
8. 重排/筛选走的是 FLIP 位移，不是整列表重新入场？
9. 共享元素用的是跨状态同名配对（VT）还是 `layoutId`？宽高比变化时避免了 scale 拉伸吗？
10. 所有 `view-transition-name` 唯一？`pageswap` 临时设的 name 在 `finished` 后清理了？
11. `view-transition-class` 只用于统一样式、没被当成唯一名替身？
12. 转场是单例吗？快速连点时旧转场被 skip、清理挂在 `finished` + `finally`？
13. 网络请求在 `startViewTransition()` **之前**完成？主流程等的是 `updateCallbackDone` 而不是 `ready`？
14. 四态/六态画过状态 × 事件矩阵了吗？快速连点有明确迁移路径且不产生不可能状态？
15. 中断策略定了吗（从当前值重启 / 叠加 / 跳终点）？二次操作不会跳回起点？
16. 保态用 `commitStyles()` 而非长期 `fill: forwards`？`cancel()` / `remove` 事件处理了吗？
17. `@starting-style` 四件套齐吗（起始样式 / display / overlay / allow-discrete）？顺序与 specificity 对吗？
18. DOM 移除延迟到退场结束（`setTimeout` / `done()` / `unmountOnExit`）？
19. `prefers-reduced-motion` 在 **CSS 与 JS 两层**都降级了吗？WAAPI / Svelte / View Transitions 有没有在 JS 层接偏好？降级是整段跳过而非逐项归零？
20. FLIP 是先全读再全写吗？预计算在 100ms 窗口内？只动了 `transform` / `opacity`？`will-change` 是临时的？

---

## 19. 可抄代码（8 段）

### 19.1 Motion 交错编排（新版 + 旧版对照）

```jsx
import { motion, stagger } from "motion/react"

// 新版（motion.dev 现行文档）：stagger() 返回动态延迟
const list = {
  hidden:  { opacity: 0, transition: { when: "afterChildren" } },
  visible: { opacity: 1, transition: { when: "beforeChildren", delayChildren: stagger(0.03) } },
}
const item = {
  hidden:  { opacity: 0, y: 8 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.2, ease: [0.05, 0.7, 0.1, 1] } },
}

// 旧版（存量项目）：固定秒数
// visible: { transition: { staggerChildren: 0.03, delayChildren: 0.1, staggerDirection: 1 } }

export function List({ items }) {
  return (
    <motion.ul initial="hidden" animate="visible" variants={list}>
      {items.slice(0, 6).map(i => <motion.li key={i.id} variants={item} />)}
      {/* >6 项：整组淡入，不逐项 stagger */}
    </motion.ul>
  )
}
```

### 19.2 CSS `--index` 级联 + 编排层降级

```css
.list > * {
  animation: rise 200ms cubic-bezier(0.05, 0.7, 0.1, 1) both;
  animation-delay: calc(var(--index, 0) * 30ms);
}
@keyframes rise {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* 降级：整段跳过交错，只留 100ms 透明度反馈（不是把 duration 归零） */
@media (prefers-reduced-motion: reduce) {
  .list > * {
    animation: none;
    animation-delay: 0s;
    opacity: 1;
    transform: none;
    transition: opacity 100ms linear;
  }
}
```

### 19.3 FLIP 批量重排（先全读、再全写，100ms 窗口内）

```js
export function flipReorder(items, mutate) {
  const firsts = items.map(el => el.getBoundingClientRect());  // ① 全读
  mutate();                                                    // ② 一次性改 DOM
  const lasts = items.map(el => el.getBoundingClientRect());   // ③ 全读
  items.forEach((el, i) => {                                   // ④ 全写
    const dy = firsts[i].top - lasts[i].top;
    const dx = firsts[i].left - lasts[i].left;
    if (Math.abs(dx) < 0.5 && Math.abs(dy) < 0.5) return;
    el.animate(
      [{ transform: `translate(${dx}px, ${dy}px)` }, { transform: 'none' }],
      { duration: 300, easing: 'cubic-bezier(0,0,0.32,1)' }   // FLIP 原文曲线
    );
  });
}
```

### 19.4 列表增删（Vue TransitionGroup + Motion popLayout）

```css
/* Vue：官方三行关键 CSS */
.list-move, .list-enter-active, .list-leave-active { transition: all .5s ease; }
.list-enter-from, .list-leave-to { opacity: 0; transform: translateX(30px); }
.list-leave-active { position: absolute; }  /* 脱离布局流，位移才算得对 */
```

```jsx
// Motion：popLayout + 父容器 position:relative + LayoutGroup
import { LayoutGroup, AnimatePresence, motion } from "motion/react"
<LayoutGroup>
  <motion.ul layout style={{ position: "relative" }}>
    <AnimatePresence mode="popLayout">
      {items.map(i => <motion.li layout key={i.id} exit={{ opacity: 0 }} />)}
    </AnimatePresence>
  </motion.ul>
</LayoutGroup>
```

### 19.5 View Transitions 增强封装（单例 + types + 偏好 + 清理）

```js
let current;

export async function navigate(update, { types = [], reduced = false } = {}) {
  if (!document.startViewTransition) { await update(); return; }   // 降级：状态变更照常

  if (current) {                        // 单例：显式结束旧转场
    current.skipTransition();
    try { await current.updateCallbackDone; } catch {}
  }

  const t = document.startViewTransition({ update, types });
  current = t;
  if (reduced) t.skipTransition();      // 用户关闭动效：只跳动画，DOM 照常更新

  // ⚠️ 不要在主流程 await t.ready（重名会 reject）
  try { await t.finished; }            // 即使被 skip 也 fulfill，适合清理
  finally { if (current === t) current = undefined; }
}
```

```css
/* 按导航方向定制，types 只在转场期生效 */
html:active-view-transition-type(forwards) {
  &::view-transition-old(content) { animation-name: slide-out-left; }
  &::view-transition-new(content) { animation-name: slide-in-right; }
}
html:active-view-transition-type(backwards) {
  &::view-transition-old(content) { animation-name: slide-out-right; }
  &::view-transition-new(content) { animation-name: slide-in-left; }
}
::view-transition-group(*) { animation-duration: 300ms; }  /* 改时长写 group 一处 */
```

### 19.6 动画状态机（XState 四态 + WAAPI 从当前值重启）

```js
import { createMachine } from 'xstate';

export const dialogMachine = createMachine({
  id: 'dialog', initial: 'closed',
  states: {
    closed:   { on: { OPEN: 'entering' } },
    entering: { on: { ANIM_END: 'open',    CANCEL: 'exiting', CLOSE: 'exiting' } },
    open:     { on: { CLOSE: 'exiting' } },
    exiting:  { on: { ANIM_END: 'closed', OPEN: 'entering' } },  // 连点反向恢复
  },
});

// 从当前视觉值重启：读计算样式作首帧，避免跳回起点
export function animateFromCurrent(el, to, opts = {}) {
  const cs = getComputedStyle(el);
  document.getAnimations().filter(a => a.effect?.target === el)
          .forEach(a => a.commitStyles());       // 持久化当前值，再释放
  const from = { opacity: Number(cs.opacity), transform: cs.transform };
  return el.animate([from, to], { duration: 200, easing: 'cubic-bezier(0.05,0.7,0.1,1)', ...opts });
}
```

### 19.7 `@starting-style` 四件套（dialog 下进上出）

```css
dialog {
  translate: 0 100vh; opacity: 0;
  transition: translate .3s var(--ease-enter), opacity .3s var(--ease-enter),
              display .3s allow-discrete, overlay .3s allow-discrete;
}
dialog[open] { translate: 0 0; opacity: 1; }
@starting-style {                       /* 必须写在 dialog[open] 之后 */
  dialog[open] { translate: 0 100vh; opacity: 0; }
}
/* 退场走 default state（下方），与入场路径不同——这是 @starting-style 三状态的用法 */
```

### 19.8 JS 层 reduced-motion 降级（覆盖 WAAPI / Svelte / VT）

```js
const mq = window.matchMedia('(prefers-reduced-motion: reduce)');

export function applyMotionPreference() {
  if (!mq.matches) return;
  // ① WAAPI / Svelte 过渡：CSS media query 管不到，必须 JS 层处理
  document.getAnimations().forEach(a => {
    a.updatePlaybackRate(0.5);          // 或 a.cancel() 直接落终态
  });
}
mq.addEventListener('change', applyMotionPreference);

// ② View Transitions：把偏好透传给封装
const reduced = mq.matches;
navigate(updateDOM, { types: ['slide'], reduced });   // → t.skipTransition()

// ③ 交错：命中 reduce 时不逐项，整组直接可见
document.documentElement.dataset.reducedMotion = String(mq.matches);
```

---

## 20. 素材与出处（本轮实测 / 官方原文）

### 20.1 规范与官方原文（全部逐页读取，非二手总结）

- [MDN · View Transition API](https://developer.mozilla.org/en-US/docs/Web/API/View_Transitions_API) — 接口、伪元素、properties、pseudo-classes、`:active-view-transition-type()`、`view-transition-scope`
- [MDN · Using the View Transition API](https://developer.mozilla.org/en-US/docs/Web/API/View_Transitions_API/Using) — 六步流程、快照语义、伪元素树、三个 promise、`match-element`、MPA `@view-transition` / `pageswap` / `pagereveal` / bfcache / `<link rel="expect" blocking="render">`
- [W3C · CSS View Transitions Module Level 1](https://drafts.csswg.org/css-view-transitions-1/) — UA stylesheet `0.25s` / `both` / `inherit` 全表、`-ua-*` 三个 keyframes、group 动态 width/height/transform、name 唯一性 abort、`updateCallback` always called、`ready` reject / `finished` fulfill
- [Chrome DevRel · Smooth transitions with the View Transition API](https://developer.chrome.com/docs/web-platform/view-transitions) — Chrome 111 / 126、三个构建块（快照 / DOM 更新时抑制渲染 / CSS animations）、MPA 触发
- [Chrome DevRel · Same-document view transitions](https://developer.chrome.com/docs/web-platform/view-transitions/same-document) — `0.25s` / `ease` 默认值、name 唯一、`skipTransition()`、`types` + `:active-view-transition-type()`、**单例与中断**、enhancement 原则、网络请求前置
- [MDN · Using the Web Animations API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API/Using_the_Web_Animations_API) — 毫秒 / `Infinity` / 默认 `linear`、`commitStyles()` / `persist()` / `updatePlaybackRate()` / `replaceState` 三值、自动移除 5 条件、三个 keyframe 等分、`offset: 0.3`
- [MDN · KeyframeEffect() constructor](https://developer.mozilla.org/en-US/docs/Web/API/KeyframeEffect/KeyframeEffect) — delay/direction/duration/easing/endDelay/fill/iterationStart/iterations/`composite`/`iterationComposite`/`pseudoElement` 全默认值
- [MDN · `@starting-style`](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@starting-style) — 三状态、同 specificity 顺序规则、仅对 transitions 有效、Baseline 2024-08
- [MDN · `transition-behavior`](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/transition-behavior) — `normal` 初始、离散属性 50% 翻转与 `display:none`/`content-visibility` 例外、`overlay` 用途
- [Chrome DevRel · Four new CSS features for smooth entry and exit animations](https://developer.chrome.com/blog/entry-exit-animations/) — Chrome 116/117 四特性、简写重置陷阱、`@starting-style` 放在后面、DOM 增删 `setTimeout` 1000ms
- [Paul Lewis · FLIP Your Animations](https://aerotwist.com/blog/flip-your-animations/) — F/L/I/P、invert 算式、`100ms` 响应窗口、三条 caveat、WAAPI 版代码（`300ms` / `cubic-bezier(0,0,0.32,1)`）
- [Motion · AnimatePresence](https://motion.dev/docs/react-animate-presence) — 唯一 key、`mode` 三档、`propagate`、`custom`/`usePresenceData`、`usePresence`/`safeToRemove`、三个排错点
- [Motion · Layout animations](https://motion.dev/docs/react-layout-animations) — `layout` / `layoutId` / `LayoutGroup` / scale correction / `layoutScroll` / `layoutRoot` / `layoutAnchor` / 与 View Transitions 三条差异
- [Motion · React animation（Orchestration / Propagation）](https://motion.dev/docs/react-animation) — variants 传播、`when: beforeChildren/afterChildren`、`delayChildren: stagger(0.3)`
- [React Transition Group · Transition](https://reactcommunity.org/react-transition-group/transition) — 四个主状态、六个回调、`timeout` 三档、`nodeRef` / `mountOnEnter` / `unmountOnExit` / `addEndListener`
- [Stately · What are state machines and statecharts?](https://stately.ai/docs/state-machines-and-statecharts) — 状态/事件/确定性、initial/final、parent/atomic/parallel、self-transition、XState `createMachine`
- [Vue · TransitionGroup](https://vuejs.org/guide/built-ins/transition-group.html) — 唯一 key、`.list-move` / `.list-leave-active { position:absolute }`、`moveClass`、`data-index` + GSAP `delay` + `done()`
- [Svelte · transition:](https://svelte.dev/docs/svelte/transition) — 双向可反转、local/global、自定义 `css(t,u)` 走 WAAPI、`tick` 性能提示、**CSS reduced-motion 对 WAAPI 无效**、`prefersReducedMotion`
- [MDN · `prefers-reduced-motion`](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion) — `no-preference`=false / `reduce`=true、等价简写、各系统开关
- [W3C WAI · Understanding SC 2.3.3 Animation from Interactions](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html) — AAA 原文、`essential` 例外、`motion animation` 定义、与 2.2.2 分工、C39/SCR40/Gx

### 20.2 仓库实测（GitHub API，2026-11-05）

| 仓库 | ★ | 许可 | 最近提交 | 定位 |
|---|---|---|---|---|
| [sveltejs/svelte](https://github.com/sveltejs/svelte) | 88562 | MIT | 2026-11-05 | `transition:` / `animate:flip` 内置 |
| [juliangarnier/anime](https://github.com/juliangarnier/anime) | 74308 | MIT | 2026-11-02 | 轻量 JS 动画引擎、stagger/timeline |
| [vuejs/core](https://github.com/vuejs/core) | 54840 | MIT | 2026-11-05 | `<TransitionGroup>` / `.list-move` FLIP |
| [motiondivision/motion](https://github.com/motiondivision/motion) | 34922 | MIT | 2026-11-05 | React/Vanilla 声明式动效，`layoutId` + `AnimatePresence` |
| [statelyai/xstate](https://github.com/statelyai/xstate) | 30411 | MIT | 2026-11-05 | 状态机 / statechart / actor |
| [greensock/GSAP](https://github.com/greensock/GSAP) | 30193 | 自定义（核心免费） | 2026-11-04 | timeline / Flip Plugin；商业插件需确认授权 |
| [pmndrs/react-spring](https://github.com/pmndrs/react-spring) | 29260 | MIT | 2026-11-01 | 弹簧物理、天然可中断 |
| [reactjs/react-transition-group](https://github.com/reactjs/react-transition-group) | 10211 | NOASSERTION | 2026-03-05 | 四态模型参考实现（维护趋缓） |
| [hotwired/turbo](https://github.com/hotwired/turbo) | 7399 | MIT | 2026-10-30 | MPA 导航加速，可与跨文档转场配合 |
| [swup/swup](https://github.com/swup/swup) | 5251 | MIT | 2026-11-03 | 服务端渲染站点的页面转场库 |

> 实测备注：`barba/barba` 与 `motionone/motion` 本轮 API 返回 **404**（仓库迁移/合并），故不列入表，也不臆造数字。`motionone` 已并入 `motiondivision/motion`。

---

**快照**：2026-11-05 · 官方原文逐页核对 + GitHub API 实测 · 20 节 / 16 场景 / 20 反模式 / 20 自检 / 8 段可抄代码。
