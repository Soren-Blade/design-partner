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

## 2. 动效缓动曲线（easing）：语义决定曲线，不是审美决定

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

## 3. 动效时长：按距离和面积取，不按心情取

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
>
> 上表是各体系**原值**，不是本库刻度；本库只有 120/200/300/400 四档（numeric-truth §1.3）。同一档各家数值不同，照抄某一家就是第二套刻度。

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
| Tooltip | 100ms（延迟 300–500ms 再显示） | 70ms | `--ease-enter` / `--ease-exit` | `opacity` + 4px | 延迟只防划过就弹，入场仍要 ≤100ms；出场比入场快 |
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
| 页面 / 路由切换 | 250–350ms | — | `--ease-enter` | 共享元素优先 | 见 `motion-orchestration.md` §6 |
| 滚动显现 | 与滚动绑定 | — | — | `translateY(24px)` + 淡入 | 见 §7.2，必须可降级 |
| 拖拽落位 | 弹簧收敛 | — | spring | 跟手 1:1 | 松手时按速度决定归位还是取消 |

---

## 5. 编排：多个元素一起动时的顺序

**细则见 `motion-orchestration.md` §2 / §3**：stagger 间隔 20–40ms、总数 ≤6（>6 改整组淡入或分组），`n > 6` 为何会破 400ms 的算术关系、父容器先于子元素、同向原则、重复加载递减间隔，都在那里给过公式，本文件不重复。

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

## 7. 实现：可直接抄的两段代码

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

> 弹层从 `display:none` 进出的 `@starting-style` 四件套见 `motion-orchestration.md` §12；共享元素 / View Transitions 的伪元素树、唯一 name、UA 默认值见同文件 §6。实现细节不在本文件重复，这里只留判据与数值。

### 7.2 滚动驱动动画（无 JS）

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

### 8.2 可见性默认成立：隐藏是增强，不是前提

**规则**：内容在无 JS、IO 未触发、打印、爬虫、动效库加载失败时都必须可读。隐藏态只在探到「能恢复」的能力时启用，且隐藏与恢复写在同一处。

```html
<script>document.documentElement.classList.add('js')</script>  <!-- head 内联，先于首帧 -->
```
```css
.js .reveal { opacity: 0; translate: 0 var(--shift-lg); }
@media (prefers-reduced-motion: no-preference) {
  @supports (animation-timeline: view()) { .reveal { animation: rise linear both; animation-timeline: view(); } }
}
@media print { .reveal { opacity: 1 !important; translate: none !important; } }
```

**四条边界**：

1. **LCP**：`opacity:0` 的元素不做 LCP 候选（Chrome 口径），非零重绘才记账——首屏主图 / 主标题别做入场，`fetchpriority="high"` 与淡入会互相抵消。必须保留时用 CSS `@keyframes`（首帧即 >0）且 <300ms，别用等 `DOMContentLoaded` 的 JS 过渡。
2. **降级不能只接 `prefers-reduced-motion`**：它只覆盖一类用户；禁 JS、IO 不触发、打印、邮件预览都不在里面。验收三测：禁 JS、reduce、打印预览。
3. **别用 `display:none` 做 reveal**：整块脱布局，恢复时重排产生 CLS；且 `loading="lazy"` 的图在 `display:none` 下不发起请求，`opacity:0` 下照常下载（白付带宽）。
4. **`opacity:0.01` 不是正解**：它让元素留在 LCP 候选里，但语义仍是「先藏后显」，各家口径有差异（W3C LCP 仓库 issue #148 仍是讨论，非标准），只能当临时手段。

---

## 9. 中文场景与小程序

| 场景 | 结论 |
|---|---|
| **微信小程序** | WXSS 支持 `transition` / `@keyframes` / `transform`；**原生组件（video、map、canvas、textarea）层级最高**，动画弹层盖不住它们 → 用 `cover-view` 或转场期间临时隐藏原生组件 |
| 小程序动效选型 | 优先 CSS 动画（包体最小、无 JS 线程开销）；复杂插画才上 Lottie。**不要用已废弃的 `wx.createAnimation`** |
| Lottie 小程序 | `wechat-miniprogram/lottie-miniprogram` 最后提交 2024-05（2026-10-30 实测）→ 已趋停滞，只作存量方案；新项目评估 Rive/CSS |
| 序列帧 | 体积杀手。1 秒 24 帧全屏序列帧轻易 >5MB，小程序 2MB 主包根本放不下 → 用 Lottie 或视频 |
| 国内设计系统 | Ant Design 动效 token 已实测：`motionUnit 0.1` → 0.1 / 0.2 / 0.3s，曲线见 §2.1。TDesign、Semi 为同级组件生态，动效数值以各自源码为准，**不臆造** |
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
8. `prefers-reduced-motion: reduce` 下，位移与循环是否全部消失、功能反馈是否仍存在？**禁 JS / 打印 / IO 不触发时内容是否仍可读**（§8.2）？
9. 动效有没有造成布局跳动（CLS）或推迟首屏内容可见（LCP）？
10. 移动端弱网/低端安卓机上，滚动时是否掉帧？（DevTools Performance 面板看 FPS 与 Long Tasks）

---

## 11. 反模式（命中即扣分）

- 从 `scale(0)` 弹窗或从 `opacity:0 + scale(.5)` 做卡片入场——真实物体不会从无到有地放大。
- 每个元素都叠 hover 放大 + 阴影 + 位移三件套（视觉噪音）。
- 滚动劫持 + 逐屏吸附（scroll-jacking），移动端尤其致命。
- 把可见性挂在动效上：`opacity:0` 等 JS / IO / 转场才显示——见 §8.2。

> 其余反模式正文已给判据，不重复收录：无限流光、出场比入场慢、用 `animation` 做交互反馈、时长凭手感、不做降级，分别见 §1、§2、§3.1、§8.1。

---

## 12. 素材与出处

**规范原文（本轮实测）**
- [Material 3 · Easing and duration tokens](https://m3.material.io/styles/motion/easing-and-duration/tokens-specs) — 曲线与时长 token 全表（含 Expressive 转向弹簧的官方说明）
- [Carbon Design System · Motion](https://www.carbondesignsystem.com/elements/motion/overview/) — productive/expressive 二分、6 档时长、3 条曲线、评估清单
- [Ant Design · 动效](https://ant.design/docs/spec/motion-cn) + `components/theme/themes/seed.ts` — 自然/高效/克制三原则与 motion 种子 token
- [Fluent 2 · Motion](https://fluent2.microsoft.design/motion) — 四种转场模式（Enter/Exit、Elevation、Top level、Container transform）与编排原则
- [MDN · prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion) — Baseline 2020-01
- [MDN · CSS scroll-driven animations](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations) — `scroll()` / `view()` / `animation-range`
- [Shopify · Don't hide LCP images behind animations](https://shopify.dev/docs/storefronts/themes/best-practices/performance/dont-hide-lcp-image-behind-animations) — `opacity:0` 不进 LCP 候选、`display:none` 更糟（§8.2）

**库与工具（选型只看许可与定位；★ 数不作质量证据）**

| 库 | 许可 | 定位 |
|---|---|---|
| [motiondivision/motion](https://github.com/motiondivision/motion)（Framer Motion） | MIT | React/Vanilla 声明式动效，弹簧与手势最完整 |
| [airbnb/lottie-web](https://github.com/airbnb/lottie-web) | MIT | AE 导出矢量动效播放 |
| [greensock/GSAP](https://github.com/greensock/GSAP) | 自定义（核心免费） | 时间轴编排、滚动触发，商业项目注意条款 |
| [pmndrs/react-spring](https://github.com/pmndrs/react-spring) | MIT | 物理弹簧，React 生态 |
| [darkroomengineering/lenis](https://github.com/darkroomengineering/lenis) | MIT | 平滑滚动（谨慎使用，见 §11） |
| [rive-app/rive-wasm](https://github.com/rive-app/rive-wasm) | MIT | 可交互矢量动效（状态机驱动，替代 Lottie 的新选择） |

**灵感与校准**：[IBM Motion Generator](https://ibm.github.io/motion/)（按距离/尺寸算时长）；动效实录与曲线可视化工具见 `knowledge-map.md` 支线 M，不重复列。
