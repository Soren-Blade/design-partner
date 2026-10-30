# 动效与微交互系统 — Motion System（深度蒸馏）

> 本文件回答「**这个动效该不该做、做多久、用什么曲线、怎么实现、怎么验收**」。凡涉及 hover / 按压 / 弹层 / 抽屉 / 页面切换 / 列表入场 / 滚动动画 / 加载态 / 手势，先读本文件，直接取数值，不要凭感觉调。
> 所有曲线与时长数值来自官方规范原文（M3 tokens-specs、Carbon Motion、Ant Design seed token），**不是二手总结**。快照 2026-10-30

**使用方式**：§1 判该不该动 → §3 取时长 → §2 取曲线 → §4 查场景 → §7 抄代码 → §10 验收。

---

## 1. 决策三问：先判该不该动

动效只有三种合法用途（**说不出属于哪一种，就删掉**）：

| 用途 | 判断标准 | 例 |
|---|---|---|
| **反馈** | 用户动作后 100ms 内有可感知变化 | hover、按压、开关、校验通过 |
| **引导** | 帮用户理解**空间关系**或**过程** | 抽屉从哪来、卡片放大成详情页、步骤条推进 |
| **个性** | 表达品牌性格，**每页 ≤1 处** | 首屏标题逐字浮现、logo 呼吸 |

**三条硬性否决**（命中任一条即不做）：

1. **纯装饰**——删掉不影响任何理解（漂浮粒子、无意义视差、背景流光）。
2. **不可中断**——用户二次操作时动画会跳回起点或锁住输入。CSS `animation` 不可中断，`transition` 可中断；**交互反馈一律用 transition**。
3. **抢占注意力**——首屏 LCP 元素做入场动画（推迟内容可见时间，也伤 LCP 指标）。

**动效预算（每页）**：1 处"主角动效" + ≤3 处滚动触发 + 0 处无限循环装饰。超预算就砍，不是优化。

---

## 2. 曲线：语义决定曲线，不是审美决定

**核心规则（90% 的人搞反的一条）**：

- **入场 → 减速曲线**（先快后慢）。元素"落位"要收敛，符合物体减速停下的直觉。
- **出场 → 加速曲线**（先慢后快）。元素"离开"要加速消失，暗示它真的走了；**时长取入场的 0.7 倍**。
- **双向位移（A 位置 → B 位置，元素始终可见）→ 标准曲线**（两头缓、中间快）。
- **循环（spinner / 进度 / 视差）→ linear**，别加缓动。

### 2.1 四体系精确值对照（可直接抄进 CSS）

| 语义 | Material 3 | Carbon（productive） | Carbon（expressive） | Ant Design | 用途 |
|---|---|---|---|---|---|
| **入场 / 减速** | `cubic-bezier(0, 0, 0, 1)` | `cubic-bezier(0, 0, 0.38, 0.9)` | `cubic-bezier(0, 0, 0.3, 1)` | `motionEaseOutQuint` `cubic-bezier(0.23, 1, 0.32, 1)` | 弹层出现、列表入场、Toast 进 |
| **出场 / 加速** | `cubic-bezier(0.3, 0, 1, 1)` | `cubic-bezier(0.2, 0, 1, 0.9)` | `cubic-bezier(0.4, 0.14, 1, 1)` | `motionEaseInQuint` `cubic-bezier(0.755, 0.05, 0.855, 0.06)` | 弹层消失、Toast 出 |
| **标准 / 双向** | `cubic-bezier(0.2, 0, 0, 1)` | `cubic-bezier(0.2, 0, 0.38, 0.9)` | `cubic-bezier(0.4, 0.14, 0.3, 1)` | `motionEaseInOut` `cubic-bezier(0.645, 0.045, 0.355, 1)` | 抽屉滑入滑出、展开收起、指示条位移 |
| **强调 / 减速** | `cubic-bezier(0.05, 0.7, 0.1, 1)` | — | — | `motionEaseOutCirc` `cubic-bezier(0.08, 0.82, 0.17, 1)` | 全屏转场、卡片放大成详情 |
| **强调 / 加速** | `cubic-bezier(0.3, 0, 0.8, 0.15)` | — | — | `motionEaseInOutCirc` `cubic-bezier(0.78, 0.14, 0.15, 0.86)` | 大范围退出、关闭全屏 |
| **回弹 / 俏皮** | 用弹簧（见 §6） | — | — | `motionEaseOutBack` `cubic-bezier(0.12, 0.4, 0.29, 1.46)` | 点赞、加购、撒花（每页 ≤1） |
| **线性** | `linear` | — | — | — | spinner、进度条、无限滚动 |

> **Ant 的反向曲线**：`motionEaseInBack cubic-bezier(0.71, -0.46, 0.88, 0.6)`（先回撤再走），慎用，仅适合"取消/撤销"的语义。

### 2.2 立场：项目默认用哪套

**给一个 3 曲线最小集就够，不要引入 12 档**：

```css
--ease-enter: cubic-bezier(0.05, 0.7, 0.1, 1);   /* M3 emphasized decelerate：入场 */
--ease-exit:  cubic-bezier(0.3, 0, 1, 1);        /* M3 standard accelerate：出场 */
--ease-move:  cubic-bezier(0.2, 0, 0, 1);        /* M3 standard：双向位移 */
```

- **中后台 / 中文 B 端项目**：直接用 Ant 三档（0.1 / 0.2 / 0.3s + `motionEaseInOut`），与组件库天然一致，改造成本最低。
- **C 端 / 品牌站**：用上面 M3 三曲线，强调曲线留给"主角动效"。
- **Carbon 的价值不在数值，在 productive / expressive 二分法**：日常操作走 productive（快、不抢戏），关键节点（打开新页面、主按钮成功、系统告警）才用 expressive。**一个产品里 expressive 占比不要超过 10%。**

---

## 3. 时长：按距离和面积取，不按心情取

**原理**：位移距离越长、面积越大，人眼需要的追踪时间越长，时长必须递增（Carbon 原话：the larger the change in distance or size, the longer the animation）。但**上限 400ms**，超过就感觉"卡"。

### 3.1 四体系时长刻度

| 档 | Material 3 | Carbon | Ant Design | 适用 |
|---|---|---|---|---|
| 极小 | short1 **50ms** | fast-01 **70ms** | — | 按钮/开关/复选框状态变化 |
| 小 | short2 **100ms** | fast-02 **110ms** | fast **100ms** | 淡入淡出、颜色过渡 |
| 中 | short4 **200ms** / medium1 **250ms** | moderate-01 **150ms** | mid **200ms** | 小展开、短距离移动 |
| 中大 | medium2 **300ms** | moderate-02 **240ms** | slow **300ms** | 展开、Toast、系统提示 |
| 大 | medium3 **350ms** / long1 **450ms** | slow-01 **400ms** | — | 大面积展开、重要通知 |
| 超大 | long2–4 **500 / 550 / 600ms** | slow-02 **700ms** | — | 背景遮罩渐暗、环境型转场 |
| 环境 | extra-long1–4 **700 / 800 / 900 / 1000ms** | — | — | 无人交互的自动轮播、氛围动画 |

> M3 的 700–1000ms 只用于**不涉及用户输入**的环境型转场。任何由点击触发的动画超过 400ms 都是错的。

### 3.2 距离 → 时长（经验法则，按 Carbon 的非线性刻度换算）

| 位移距离 / 变化面积 | 时长 |
|---|---|
| 0（纯颜色/透明度） | 100–150ms |
| ≤ 100px | 150–200ms |
| 100–300px | 200–300ms |
| > 300px 或全屏 | 300–400ms |
| 全页路由切换 | 250–350ms（超过就等得烦） |

**微交互的硬指标**（Carbon 评估清单原文）：用户输入触发的微交互应落在 **90–120ms**，且用 **ease-out**。

---

## 4. 场景速查表（直接取值，不用再算）

覆盖场景：hover / 按钮按压 / 焦点环 / 开关 Toggle / 复选框 / Tooltip / 下拉菜单 Popover / 弹层（Modal、Dialog）/ 抽屉 Drawer / Toast 提示 / 手风琴 / Tab 切换 / 列表入场 / 骨架屏 / 数字滚动 / 侧边栏折叠 / 页面路由转场 / 滚动显现 / 拖拽落位。**找到对应行直接抄数值，不要重新推导。**

| 场景 | 入场 | 出场 | 曲线 | 位移 / 缩放 | 要点 |
|---|---|---|---|---|---|
| hover 变色 / 阴影 | 120–150ms | 同 | `--ease-move` | 无 | 只改 color / background / box-shadow |
| 按钮按压 | 100ms | 松手 150ms | `--ease-enter` | `scale(0.98)` | 不要 `scale(0.9)`，会像坏了 |
| 焦点环出现 | 0–100ms | 0ms | linear | 无 | 焦点必须**即时**可见，别做淡入 |
| 开关 Toggle | 150ms 拇指 / 200ms 轨道 | 同 | `--ease-move` | 位移 ≈ 轨道宽 − 2×内边距 | 颜色与位移同步结束 |
| 复选框打勾 | 150ms | — | `--ease-enter` | 路径描边 `stroke-dashoffset` | 勾号先出、方框后填 |
| Tooltip | 100ms（延迟 300–500ms 再显示） | 70ms | `--ease-enter` / `--ease-exit` | `opacity` + 4px | 出场必须比入场快 |
| 下拉菜单 / Popover | 150–180ms | 120ms | `--ease-enter` | `scale(0.96) → 1`，原点贴触发元素 | `transform-origin` 对准触发按钮 |
| Modal / Dialog | 200–250ms | 150ms | 入 `--ease-enter` / 出 `--ease-exit` | `scale(0.96) → 1` + scrim 200ms | 不要从 `scale(0)` 弹 |
| 抽屉 Drawer | 250–300ms | 200ms | `--ease-move` | 从边缘 100% 位移 | 支持拖拽关闭时 1:1 跟手 |
| Toast | 200ms | 150ms | `--ease-enter` | `translateY(12px) → 0` | 停留 3–5s；可叠加时垂直堆叠 |
| 手风琴展开 | 200–250ms | 180ms | `--ease-move` | `grid-template-rows: 0fr → 1fr` | 别动 `height`（见 §8） |
| Tab 切换 | 150–200ms | — | `--ease-enter` | 内容淡入 + 8px；指示条位移 200ms | 指示条用 transform 而非 left |
| 列表入场 | 200ms + stagger 30ms | — | `--ease-enter` | `translateY(8–16px) → 0` | 总时长 ≤400ms；>6 项不要逐项 |
| 骨架屏 → 内容 | 150ms 交叉淡出 | — | linear | `opacity` | 骨架尺寸必须与真实内容一致（防 CLS） |
| 数字滚动 | 400–600ms | — | `--ease-enter` | — | 仅关键指标；无障碍要提供最终值文本 |
| 侧边栏折叠 | 200–250ms | 同 | `--ease-move` | 宽 240 → 64px | 文字先淡出（100ms）再改宽 |
| 页面 / 路由切换 | 250–350ms | — | `--ease-enter` | 共享元素优先 | 见 §7.3 View Transitions |
| 滚动显现 | 与滚动绑定 | — | — | `translateY(24px)` + 淡入 | 见 §7.4，必须可降级 |
| 拖拽落位 | 弹簧收敛 | — | spring | 跟手 1:1 | 松手时按速度决定归位还是取消 |

**延迟出场的例外**：Tooltip、二级菜单需要"意图延迟"（300–500ms）避免划过就弹；但**入场动画本身仍要快**（≤100ms）。延迟是防误触，不是慢动作。

---

## 5. 编排：多个元素一起动时的顺序

1. **层级优先**：重要元素先动、动得更久；次要元素**合并成一组同时动**（Fluent：次要元素同步可避免注意力分散）。
2. **stagger 间隔 20–40ms**，总数 ≤6 项。超过 6 项改为"整组淡入"，否则最后一项要等到 800ms 后。
3. **父容器先于子元素**：父容器位移/缩放完成 60% 后再触发子内容淡入，观感才"是一个整体"。
4. **同向原则**：同一次转场里所有元素朝同一方向运动，反向运动只在"对比/切换"语义下用。
5. **重复加载时递减间隔**：同一内容多次加载，stagger 间隔可逐次缩短（首次 40ms → 后续 20ms），避免等待感累积。

---

## 6. 物理感：什么时候用弹簧，什么时候用曲线

| 维度 | cubic-bezier | 弹簧（spring） |
|---|---|---|
| 适合 | 时长确定、可预测的转场 | 跟手拖拽、松手收敛、可被中断的连续交互 |
| 优点 | 实现简单（纯 CSS）、时长可控 | 天然可中断、速度连续、有重量感 |
| 缺点 | 中途被打断会重算 | 时长不确定（需设上限），调试参数多 |

**建议参数（建议值，非官方）**：UI 常规 `stiffness 300–500 / damping 30–40 / mass 1`；需要弹性时降 damping 到 20–26；**永远设置最大时长兜底**（如 `restDelta 0.01` + 超时 600ms 强制结束）。

**M3 Expressive 已整体转向弹簧物理系统**（官方原文：components and motion now use the motion physics system, which uses springs；旧的 easing/duration 体系仅保留给转场且不再维护）。做 Android/M3 风格产品时优先弹簧；做 Web 通用界面时曲线仍是主流，别为了"先进"而上弹簧。

---

## 7. 实现：可直接抄的四段代码

### 7.1 动效 token（贴进 `:root`）

```css
:root {
  /* 时长：4 档够用 */
  --dur-fast: 120ms;   /* 状态反馈 */
  --dur-base: 200ms;   /* 常规转场 */
  --dur-slow: 300ms;   /* 大面积/抽屉 */
  --dur-hero: 400ms;   /* 主角动效上限 */

  /* 曲线：3 条 */
  --ease-enter: cubic-bezier(0.05, 0.7, 0.1, 1);
  --ease-exit:  cubic-bezier(0.3, 0, 1, 1);
  --ease-move:  cubic-bezier(0.2, 0, 0, 1);

  /* 位移尺度：统一，别每处自定 */
  --shift-sm: 4px;
  --shift-md: 12px;
  --shift-lg: 24px;
}
```

### 7.2 从 `display:none` 进入的弹层（`@starting-style`）

原生 `dialog` / `popover` 从 `display:none` 变可见时，直接写 transition 不会触发动画，必须配 `@starting-style` + `transition-behavior: allow-discrete`：

```css
.popover {
  opacity: 1;
  transform: scale(1);
  transition: opacity var(--dur-fast) var(--ease-enter),
              transform var(--dur-fast) var(--ease-enter),
              display var(--dur-fast) allow-discrete,
              overlay var(--dur-fast) allow-discrete;
}
@starting-style {
  .popover { opacity: 0; transform: scale(0.96); }
}
.popover:not(:popover-open) { opacity: 0; transform: scale(0.96); }
```

> 兼容：`@starting-style` / `transition-behavior: allow-discrete` 属 2024 年后的 Baseline 能力（Chrome 117+ / Safari 17.4+ / Firefox 129+）。老浏览器下退化为"瞬间出现"，可接受。

### 7.3 共享元素过渡（View Transitions）

同一元素在 A 视图与 B 视图都标同一个名字，浏览器自动做"从旧位置尺寸平滑过渡到新位置尺寸"：

```css
.card { view-transition-name: card-detail; }        /* 两个视图都要标 */
::view-transition-group(card-detail) {
  animation-duration: var(--dur-slow);
  animation-timing-function: var(--ease-enter);
}
::view-transition-old(card-detail) { animation: none; }  /* 避免双层叠影 */
```

```js
document.startViewTransition(() => renderNewState());   // SPA
```

多页应用（MPA）只需在两个页面 CSS 里各写一行 `@view-transition { navigation: auto; }`，即可获得跨文档转场；配合 `pageswap` / `pagereveal` 事件按导航方向定制。

**什么时候别用**：需要精确控制中途状态、或转场元素 >6 个（快照开销大）。此时退回手写 transform。

### 7.4 滚动驱动动画（无 JS）

```css
@supports (animation-timeline: view()) {
  .reveal {
    animation: rise linear both;
    animation-timeline: view();
    animation-range: entry 20% cover 45%;   /* 进入视口 20% 开始，覆盖 45% 结束 */
  }
  @keyframes rise { from { opacity: 0; translate: 0 24px; } to { opacity: 1; translate: 0 0; } }
}
```

**纪律**：滚动驱动动画只能做"入场"和"进度指示"，**不要做滚动劫持**（用 JS 强行改滚动位置），后者是体验灾难且伤可访问性。

---

## 8. 性能与降级

**只动这两个属性**：`transform`（含 `translate` / `scale` / `rotate`）与 `opacity`——它们走合成层，不触发布局与重绘。

**禁止连续动画的属性**：`width` / `height` / `top` / `left` / `margin` / `box-shadow` / `filter: blur()`。替代方案：

| 想动 | 别动 | 改成 |
|---|---|---|
| 高度展开 | `height: 0 → auto` | `grid-template-rows: 0fr → 1fr`（父 `display:grid`，子 `overflow:hidden`） |
| 位置移动 | `left` / `top` | `translate` |
| 阴影加深 | `box-shadow` | 叠一层 `opacity` 渐变的伪元素阴影 |
| 模糊转场 | `filter: blur()` | 用两张大图交叉淡入 |

**帧预算**：60Hz 每帧 16.7ms，120Hz 每帧 8.3ms。一次掉帧用户未必看见，连续 3 帧掉就会"顿"。

**`will-change` 纪律**：只在动画开始前 1 帧加、结束后移除；常驻 `will-change` 会白吃显存并可能让文字发虚。

**布局稳定**：任何动画都不应改变周围元素的位置（否则产生 CLS）。骨架屏、图片占位必须先定尺寸。

### 8.1 `prefers-reduced-motion` 三档降级（必须做）

WCAG 依据：**2.3.3 Animation from Interactions（AAA）**——交互触发的动效必须可关闭（除非是功能必需）；**2.2.2 Pause, Stop, Hide（A）**——超过 5 秒的自动运动内容必须可暂停；**2.3.1**——每秒闪烁不超过 3 次。

**推荐做法（精细降级，优于全局暴力关闭）**：

```css
@media (prefers-reduced-motion: reduce) {
  /* 1. 杀掉位移/缩放/视差/循环，保留色彩与透明度反馈 */
  .reveal, .parallax, .float, .marquee { animation: none !important; transform: none !important; }
  /* 2. 转场时长压到功能反馈级别（≤100ms），不是 0 */
  *, *::before, *::after {
    animation-duration: 1ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 100ms !important;
    scroll-behavior: auto !important;
  }
  /* 3. 滚动驱动动画退化为"直接显示" */
  .reveal { opacity: 1 !important; }
}
```

**为什么不全设 `0.01ms`**：那会把"按钮按下变深"这类**功能反馈**一起杀掉，反而降低可用性。降级的目标是**去掉空间运动**，不是去掉所有变化。

**低端设备策略**：用 `navigator.hardwareConcurrency` 或首帧帧率采样做一次性降级（关闭视差与大范围模糊），不要做实时检测——检测本身就在耗性能。

---

## 9. 中文场景与小程序

| 场景 | 结论 |
|---|---|
| **微信小程序** | WXSS 支持 `transition` / `@keyframes` / `transform`；**原生组件（video、map、canvas、textarea）层级最高**，动画弹层盖不住它们 → 用 `cover-view` 或转场期间临时隐藏原生组件 |
| 小程序动效选型 | 优先 CSS 动画（包体最小、无 JS 线程开销）；复杂插画才上 Lottie。**不要用已废弃的 `wx.createAnimation`** |
| Lottie 小程序 | `wechat-miniprogram/lottie-miniprogram` ★433，最后提交 2024-05（2026-10-30 实测）→ 已趋停滞，仅作存量方案；新项目评估 Rive/CSS 方案 |
| 序列帧 | 体积杀手。1 秒 24 帧全屏序列帧轻易 >5MB，小程序 2MB 主包根本放不下 → 用 Lottie 或视频 |
| 国内设计系统 | Ant Design 动效 token 已实测：`motionUnit 0.1` → 0.1 / 0.2 / 0.3s，曲线见 §2.1。TDesign（★4120）、Semi（★10447）为同级组件生态，动效数值以各自源码为准，**不臆造** |
| 中文文案动效 | 逐字浮现对中文不友好（中文无词间空格，逐字断句会破词）；要逐字就用**按词分组**，或整句淡入 + 轻微上移 |

---

## 10. 验收清单（10 条，交付前逐条过）

1. 每个动效都能说出属于**反馈 / 引导 / 个性**中的哪一种？说不出的删了没？
2. 用户输入触发的反馈是否 **≤120ms** 出现？
3. 入场用减速曲线、出场用加速曲线？出场时长是入场的 ~0.7 倍？
4. 有没有任何点击触发的动画 **>400ms**？
5. 动画进行中用户再次点击，是否**从当前状态继续**而不是跳回起点？
6. 只动了 `transform` / `opacity`？有没有动 `height` / `top` / `box-shadow`？
7. 每页是否只有 **1 处**主角动效？expressive 类动效占比是否 ≤10%？
8. `prefers-reduced-motion: reduce` 下，位移与循环是否全部消失、功能反馈是否仍存在？
9. 动效有没有造成布局跳动（CLS）或推迟首屏内容可见（LCP）？
10. 移动端弱网/低端安卓机上，滚动时是否掉帧？（DevTools Performance 面板看 FPS 与 Long Tasks）

---

## 11. 反模式（命中即扣分）

- 从 `scale(0)` 弹窗、从 `opacity:0` + `scale(0.5)` 做卡片——真实物体不会从无到有地放大。
- 每个元素都加 hover 放大 + 阴影 + 位移三件套（视觉噪音）。
- 出场和入场一样慢（甚至更慢）——用户等的是"消失"。
- 用 `animation` 做交互反馈（不可中断，连点会跳帧）。
- 无限循环的渐变流光 / 粒子 / 打字机（除非是产品核心表达，且必须可暂停）。
- 滚动劫持 + 逐屏吸附（scroll-jacking），移动端尤其致命。
- 动效时长"凭手感"设成 500ms / 800ms 这种非刻度值，导致全站节奏不齐。
- 只做动效不做降级， vestibular 障碍用户直接无法使用。

---

## 12. 素材与出处

**规范原文（本轮实测）**
- [Material 3 · Easing and duration tokens](https://m3.material.io/styles/motion/easing-and-duration/tokens-specs) — 曲线与时长 token 全表（含 Expressive 转向弹簧的官方说明）
- [Carbon Design System · Motion](https://www.carbondesignsystem.com/elements/motion/overview/) — productive/expressive 二分、6 档时长、3 条曲线、评估清单
- [Ant Design · 动效](https://ant.design/docs/spec/motion-cn) + `components/theme/themes/seed.ts` — 自然/高效/克制三原则与 motion 种子 token
- [Fluent 2 · Motion](https://fluent2.microsoft.design/motion) — 四种转场模式（Enter/Exit、Elevation、Top level、Container transform）与编排原则
- [MDN · prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion) — Baseline 2020-01
- [MDN · View Transition API](https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API) — 同文档/跨文档、伪元素、类型与作用域
- [MDN · CSS scroll-driven animations](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations) — `scroll()` / `view()` / `animation-range`

**库与工具（GitHub API 实测 2026-10-30）**

| 库 | ★ | 最近提交 | 许可 | 定位 |
|---|---|---|---|---|
| [motiondivision/motion](https://github.com/motiondivision/motion)（Framer Motion） | 34666 | 2026-10-30 | MIT | React/Vanilla 声明式动效，弹簧与手势最完整 |
| [airbnb/lottie-web](https://github.com/airbnb/lottie-web) | 32291 | 2025-09-01 | MIT | AE 导出矢量动效播放 |
| [greensock/GSAP](https://github.com/greensock/GSAP) | 29931 | 2026-04-13 | 自定义（核心免费） | 时间轴编排、滚动触发，商业项目注意条款 |
| [pmndrs/react-spring](https://github.com/pmndrs/react-spring) | 29256 | 2026-10-30 | MIT | 物理弹簧，React 生态 |
| [darkroomengineering/lenis](https://github.com/darkroomengineering/lenis) | 16976 | 2026-10-29 | MIT | 平滑滚动（谨慎使用，见 §11） |
| [rive-app/rive-wasm](https://github.com/rive-app/rive-wasm) | 1017 | 2026-10-30 | MIT | 可交互矢量动效（状态机驱动，替代 Lottie 的新选择） |

**灵感与校准**：[60fps.design](https://60fps.design/)（动效实录）、[Motion Primitives](https://motion-primitives.com)（可抄的 React 动效组件）、[easings.net](https://easings.net/)（曲线可视化）、[cubic-bezier.com](https://cubic-bezier.com/)（调曲线）、[IBM Motion Generator](https://ibm.github.io/motion/)（按距离/尺寸算时长）
