# 图标设计系统 · Iconography

> 每日升级 #22（v25 → v26）。取源：Lucide / Material Symbols / Ant Design Icons / Heroicons / Carbon / Fluent / Radix Icons 官方文档 + GitHub API 实测（star/license/pushed_at）。
> 接线：SKILL.md 路由 + 第 5 步原则 + 第 6 步自检；aliases.json；knowledge-map 支线 T；Design-related websites.txt 已补图标分区。

## 0. 一句话立场

**图标是「视觉速记」，不是「装饰」。** 它只在「图形比文字更快被识别」时胜出；其余场景要么配文字，要么直接用文字。图标系统的全部工作，是把这套「识别」做到**跨尺寸可读、跨库一致、跨工具可达**。

---

## 1. 何时用图标 / 文字 / 两者（决策树）

| 条件 | 选择 | 理由 |
|---|---|---|
| 空间极紧（标签页、工具栏 16–20px 槽位）且图标高度惯例化（搜索/设置/关闭） | **仅图标** + 必带 `aria-label` | 图形识别快于文字，但必须可命名 |
| 图标语义有歧义（「分享」「更多」长相不统一）或首次出现的品牌图标 | **图标 + 文字** | 降低认知负荷，消除歧义 |
| 正文、按钮主文案、导航一级项 | **仅文字**（可配前置图标做点缀） | 文字零歧义、可本地化、SEO/可访问性最好 |
| 状态指示（成功/警告/错误） | **图标 + 颜色 + 文字** 三者至少两样 | 永不只靠颜色（WCAG 1.4.1） |

**反模式预警**：用图标替代一切文字 = 把可用性赌在用户的「图标素养」上；国际化和首因效应都会反噬。

---

## 2. 图标网格系统（Grid & Keylines）

### 2.1 基础网格
- **viewBox 统一 24×24**（Lucide / Material / Heroicons outline / Feather / Carbon / Fluent 默认）。这是行业事实标准，导出 SVG 一律 `viewBox="0 0 24 24"`。
- **内边距 2px**：图形主体落在 20×20 活动区，留 2px 呼吸边（Material keyline 由此而来）。个别「出血」图形（如全屏箭头）可贴边，但默认留 2px。
- **像素对齐**：所有坐标落在整数或半像素（`.5`）；避免亚像素模糊。导出前在 1× 下肉眼巡检 16px 渲染。

### 2.2 Keylines（关键形，Material 体系权威取值）
| 形状 | 尺寸 | 用途 |
|---|---|---|
| 圆形 | ⌀ 20（r=10） | 定位、播放、账户类 |
| 方形 | 18×18（圆角 2） | 大多数 App 图标、卡片 |
| 矩形 | 20×16 / 18×14 | 浏览器、手机、屏幕 |
| 三角形 | 高 17 / 宽 20 | 播放、警告 |

> 同一套图标里，相同语义类别的图形**必须贴同一 keyline**，否则视觉重量会飘。这是「跨库一致」的地基。

---

## 3. 描边与笔画（Stroke）

| 库 | viewBox | stroke-width | linecap / join | 说明 |
|---|---|---|---|---|
| Lucide | 24 | **2** | round / round | 线性极简，1.5 也可 |
| Heroicons outline | 24 | **1.5** | round / round | 描边版 |
| Tabler | 24 | **2**（可 1.5/1.25） | round / round | 偏技术感 |
| Carbon | 16/20/24/32 | **1.5** | butt/round | 数据产品首选 |
| Feather | 24 | **2** | round / round | 前身规范 |
| Fluent | 16–48 | **1**（光学加粗） | round / round | 微软体系 |
| Material Symbols | 24dp | wght 100–700（默认 400） | — | 变量字体，无固定描边 |
| Ant Design Icons | 24（默认 1em） | 描边/填充两族 | — | `Outlined`/`Filled`/`TwoTone` 三主题 |

**铁律**：
- **圆头圆角（round）** 是默认；方头（butt）只用于刻意硬朗的风格（Carbon 部分）。
- **圆角半径 1–2px**（在 24 网格下），过尖刺眼、过圆发软。
- **固定描边 vs 缩放描边** 二选一且全库统一：
  - *固定*（Lucide 做法）：`stroke-width="2"` 写死，渲染到 16px 时线变细 → 小尺寸更精致，但极小时可能断。
  - *缩放*（Material 做法）：用 `opsz` 光学尺寸自动调权重，小尺寸也保重量。
  - 不要混用——同一产品里一半图标固定、一半缩放 = 视觉抖。

---

## 4. 尺寸阶梯（Sizing Scale）

| 档位 | px | 典型用途 |
|---|---|---|
| xs | **12** | 行内状态点、角标 |
| sm | **16** | 表格操作、列表项、工具栏 |
| md | **20** | 按钮内图标、表单前缀 |
| lg | **24** | 导航、空态主图、卡片头 |
| xl | **32** | 大留白页、营销块 |
| xxl | **48** | 登录/引导页英雄图标 |

- **密度驱动**：紧凑界面默认 16，宽松默认 20–24；不要一套尺寸打天下。
- **与字号联动**：图标高度 ≈ 行内文字的 `1em`（Ant 默认即 `1em`），保证与文字基线上对齐。
- **最小可点**：若图标是**唯一**可点目标（icon-only 按钮），命中区 ≥ **24×24**，理想 **44×44**（见 accessibility.md 44 档）；图标本身可 20，但 `padding` 撑到 44。

---

## 5. 图标与文字间距（Icon–Text Spacing）

- **默认 8px**（图标 16–20 配 14–16px 文字）。Material/Carbon/Heroicons 一致推荐 8px。
- **最小 4px**：超紧布局下限，再小会「粘」在一起。
- **对齐**：图标用 `vertical-align: middle` 或 flex `align-items: center` + 负 margin 修正基线；图标光学中心与文字 x-高度中心对齐，不是几何中心。
- **RTL**：间距用 `margin-inline-start`，镜像时自动翻转（呼应 i18n-localization.md 的逻辑属性）。

---

## 6. 填充 / 描边 / 双色（Fill · Stroke · Duotone）

| 形态 | 何时用 | 代表 |
|---|---|---|
| **描边（线性）** | 默认、低密度、现代极简 | Lucide / Heroicons outline / Feather |
| **填充（实心）** | 高对比、小尺寸、状态强调 | Heroicons solid / Material FILL=1 |
| **双色（duotone）** | 品牌个性、插画感 | Ant `TwoTone`、Phosphor duotone |
| **变量填充** | 状态过渡（未选中→选中） | Material `FILL` 轴 0→1 可做过渡动画 |

- **状态用填充切换**：选中态把描边图标 `FILL` 0→1（Material），或描边→实心（Heroicons），让用户「看到」状态而非只靠颜色。
- **双色需守约**：主色 + 副色（`twoToneColor`），副色用主色的浅阶，**不要引入第三个品牌色**。

---

## 7. 光学对齐与修正（Optical Alignment）

- **视觉居中 ≠ 几何居中**：圆形/三角形比方形「显小」，需向中心**过冲 1–2%**（overshoot）才显得等大。
- **重量平衡**：同一 keyline 下，方形图标描边外扩、圆形图标内收，使视觉重量一致。
- **不对称图标**：重心偏左的（如「播放」三角）整体右移半像素，让留白在视觉上对称。
- **清边距（clear space）**：图标四周留 ≥ 图标 50% 尺寸的空白（呼应 brand-identity.md 的 clear space 三口径），密集列表里用 `gap` 而非贴边。

---

## 8. 状态图标（State Icons）

- **加载转圈（spinner）**：`rotate` 动画，`1–1.4s linear infinite`（连续无限循环，呼应 motion-system.md 持续型 ≤1.4s）。不要用 `ease`（会一顿一顿）。
- **不确定进度**（indeterminate）：环缺一段 + 旋转，或线段来回扫。
- **确定性进度**：SVG `stroke-dasharray` + `stroke-dashoffset` 随百分比走。
- **prefers-reduced-motion**：`reduce` 时停转、保留静态或极慢（见 §10、motion-system.md 降级）。
- **不要做「假加载」**：转圈时间固定 3s 假装加载 = 欺骗性设计（见 design-ethics-inclusion.md）。

---

## 9. 交付格式（Delivery Formats）

| 格式 | 优点 | 缺点 | 何时选 |
|---|---|---|---|
| **内联 SVG** | 可 `currentColor`、可加 `aria`、可动画、无请求 | HTML 膨胀、难复用 | 少量关键图标、需主题色 |
| **SVG Sprite** | 一次请求、可 `use` 引用、可 `currentColor` | 需构建步骤 | 中大型站点 |
| **图标字体** | 字重/尺寸靠 `font-size`、易用 | **可访问性差**（读屏念乱码）、失焦、`currentColor` 受限、FOUC | 仅旧系统；新项目不推荐 |
| **组件（React/Vue）** | tree-shaking、类型安全、props 控制 | 绑定框架 | 组件化项目首选 |

- **Material Symbols 字体体积实测**：默认全量 **295 KB**；按 `icon_names` 子集化 **1.7 KB**；全变量轴 **7.9 MB** → 必须子集化，且加 `&display=block` 防 FOUC。
- **结论**：优先「SVG 组件 / Sprite + `currentColor`」，图标字体只在 legacy 场景保留。

---

## 10. 可访问性（Accessibility）⚠️ 高频翻车点

| 场景 | 正确做法 |
|---|---|
| **装饰性图标**（纯美化，无信息） | `aria-hidden="true"` **且** `focusable="false"`（SVG 在 IE/旧 Edge 可被聚焦） |
| **有意义图标**（单独传达含义） | `role="img"` + `aria-label="意思"`；或 `<title id>` + `aria-labelledby` |
| **icon-only 按钮** | 按钮本身 `aria-label`，图标 `aria-hidden`（避免「按钮+图标」双重播报） |
| **图标+文字** | 图标 `aria-hidden`，让文字担纲可访问名 |
| **非文本对比度** | 有意义图标 ≥ **3:1**（WCAG 1.4.11 非文本对比度） |
| **永不只靠颜色** | 状态用「图标形状 + 颜色 + 文字」至少两样（WCAG 1.4.1） |
| **动效** | spinner/动画尊重 `prefers-reduced-motion: reduce` |
| **RTL** | 方向性图标（箭头、播放）用逻辑属性或 `dir` 镜像（呼应 i18n-localization.md） |

> 图标字体最大坑：读屏会把连字念成「home settings」之类乱码 → 必须 `aria-hidden` 整字库，另用视觉隐藏文字兜底。

---

## 11. 动画（Animation）

- **spinner**：`rotate 360deg` + `1–1.4s linear infinite`。
- **stroke-draw**：`stroke-dasharray` + `stroke-dashoffset` 0，时长 **200–500ms**，缓出。
- **状态切换**：FILL/描边↔实心用 `200–300ms` 缓出（呼应 motion-system.md 时长刻度）。
- **入场**：图标随列表 stagger，单条 ≤ **400ms**（见 motion-orchestration.md `T=d+(n-1)s≤400ms`）。
- **降级**：`prefers-reduced-motion: reduce` → 停转、跳过 draw、保留终态。

---

## 12. 命名与交付清单（Naming & Delivery Checklist）

- **命名 kebab-case**：`arrow-right.svg`、`user-settings.svg`；与库约定一致（Material 用 snake_case `arrow_forward`，混用前先定约）。
- **导出整数坐标**：无 transform、无小数缩放、无 group 嵌套冗余。
- **多尺寸同稿**：同一语义提供 **16 / 20 / 24**（至少 2 档），小尺寸单独优化（不是大图缩放下放）。
- **双形态**：描边 + 实心（或 duotone）成对交付。
- **颜色用 `currentColor`**：让 CSS 控色，暗色模式零改图（呼应 dark-mode.md 不用纯白）。
- **附 token**：`--icon-size` / `--icon-color` / `--icon-gap` 进设计 token（见 design-tokens.md）。
- **可访问性自检**：每个有意义图标有命名方案，装饰图标已 `aria-hidden`。

---

## 13. 库选型矩阵（Library Matrix · GitHub API 实测）

| 库 | ★（本次实测） | License | 特点 | 末次 push |
|---|---|---|---|---|
| Lucide | **25,616** | NOASSERTION¹ | 1600+ 线性、tree-shaking、24 网格、stroke 2 | 2026-11-06 |
| Tabler Icons | **22,572** | MIT | 5000+ 线性、stroke 2、技术感 | 2026-10-29 |
| Fluent UI System Icons | **10,962** | MIT | 微软体系、16–48 多档、1px 光学描边 | 2026-11-06 |
| Radix Icons | **2,707** | MIT | 极简、配 Radix Primitives | 2026-04-02 |
| Material Symbols | — | Apache-2.0 | 2500+ 变量字体、四轴可调、子集化 | — |
| Heroicons / Carbon / Phosphor / Feather / Ant Design Icons | 未本轮实测² | MIT / Apache-2.0 等 | 各体系标杆 | — |

> ¹ Lucide 在 GitHub API 返回 `NOASSERTION`（GitHub 未自动归类标准 SPDX；社区实际以 ISC 发布）——商用前以仓库 LICENSE 文件为准。
> ² 本轮 GitHub API 限频（未认证 60/min），未逐库重测；star/许可以各库公开页为准，凡未取得实时数值的一律不写入资产正文。

**选型三问**（呼应 ai-design-toolchain.md 的「选型三问」）：
1. 框架绑定？（React→Lucide/Heroicons；Vue→Lucide/Tabler；无框架→Sprite）
2. 风格统一？（极简线性→Lucide；数据产品→Carbon；微软生态→Fluent）
3. 体积敏感？（都要子集化；Material 必须 `icon_names`）

---

## 14. 与既有参考的接线（Wiring）

- **patterns.md**：图标是「元素设计模式」的高频项，本文补其精确数值。
- **brand-identity.md**：logo 的 clear space / 网格规则与图标 keyline 同源。
- **accessibility.md**：图标 a11y 是 §10 的具体落点；44px 命中区来自其 44 档。
- **dark-mode.md**：`currentColor` 让图标随表面层级变色，零改图。
- **motion-system.md / motion-orchestration.md**：spinner/状态切换时长与降级在此。
- **design-tokens.md**：`--icon-size/color/gap` 应进 token，不写死。
- **i18n-localization.md**：方向性图标 RTL 镜像用逻辑属性。
- **design-ethics-inclusion.md**：假加载 spinner = 欺骗性设计，禁用。

---

## 15. 12 场景（Scenarios）

1. 工具栏仅图标按钮 → icon-only + `aria-label` + 44 命中区
2. 导航一级项 → 图标+文字（消除歧义）
3. 表格行内操作（编辑/删除）→ 16px 图标 + `aria-hidden`，行有文字标签
4. 表单前缀图标（搜索/用户）→ `aria-hidden`，label 担纲
5. 空态主图 → 24–48 描边图标 + 文案 + 行动按钮
6. 加载中 → spinner `1–1.4s linear infinite` + `prefers-reduced-motion` 降级
7. 成功/警告/错误 → 图标+颜色+文字，不靠颜色
8. 选中态切换 → 描边↔实心 / FILL 0→1，200–300ms
9. 暗色模式 → `currentColor` 自动适配，不另出图
10. RTL 语言 → 箭头/播放用逻辑属性镜像
11. 极小尺寸 12px → 单独优化稿，非大图缩放
12. 设计系统交付 → 16/20/24 多档 + 描边/实心 + token + a11y 方案

---

## 16. 20 反模式（Anti-patterns）

1. 用图标替代一切文字（赌用户图标素养）
2. 图标无 `aria-label` 又无文字（icon-only 不可命名）
3. 装饰图标忘了 `aria-hidden`（读屏念「图」）
4. SVG 漏 `focusable="false"`（旧浏览器可聚焦）
5. 图标字体整库未 `aria-hidden`（读屏念乱码）
6. viewBox 不统一（有的 20 有的 24 → 对齐崩）
7. 描边固定与缩放混用（视觉抖）
8. 小尺寸直接大图缩放（细线断、糊）
9. 图标与文字 0 间距（粘在一起）
10. 只靠颜色表状态（违反 WCAG 1.4.1）
11. 有意义图标对比度 < 3:1（违反 1.4.11）
12. 假加载 spinner 固定 3s（欺骗性设计）
13. spinner 用 `ease` 缓动（一顿一顿）
14. 不尊重 `prefers-reduced-motion`（眩晕风险）
15. 方向性图标在 RTL 下不镜像
16. 双色图标引入第三品牌色
17. Material 字体不子集化（295KB→7.9MB 风险）
18. 图标命中区 < 24（仅 16 图标不可点）
19. 命名大小写/连字符不统一（维护灾难）
20. 暗色模式另出一套图标（应 `currentColor` 复用）

---

## 17. 20 自检（Self-checks）

- [ ] 每个图标 viewBox 都是 `0 0 24 24`？
- [ ] 装饰图标是否 `aria-hidden="true"` + `focusable="false"`？
- [ ] 每个有意义 / icon-only 图标是否有可访问名？
- [ ] 图标字体是否已整库 `aria-hidden`？
- [ ] 有意义图标对比度是否 ≥ 3:1？
- [ ] 状态是否至少有「形状 + 颜色 + 文字」两样？
- [ ] 描边策略（固定/缩放）是否全库统一？
- [ ] 是否提供 16/20/24 至少两档？
- [ ] 小尺寸是否单独优化稿？
- [ ] 图标-文字间距是否 ≥ 4px（默认 8px）？
- [ ] 图标命中区是否 ≥ 24（可点目标 ≥ 44）？
- [ ] 是否用 `currentColor` 控色（暗色零改图）？
- [ ] spinner 是否 `1–1.4s linear infinite`？
- [ ] 是否尊重 `prefers-reduced-motion: reduce`？
- [ ] RTL 下方向性图标是否镜像？
- [ ] 双色图标是否只用主色 + 浅阶副色？
- [ ] Material 字体是否子集化（`< 10KB`）？
- [ ] 命名是否 kebab-case 统一？
- [ ] 是否附 `--icon-size/color/gap` token？
- [ ] 是否与 patterns / brand / a11y / motion / tokens 接线？

---

## 18. 可抄代码（Copy-paste）

### 18.1 SVG 模板（24 网格 · currentColor · 可访问）
```svg
<!-- 装饰性 -->
<svg viewBox="0 0 24 24" width="20" height="20" fill="none"
     stroke="currentColor" stroke-width="2" stroke-linecap="round"
     stroke-linejoin="round" aria-hidden="true" focusable="false">
  <path d="M12 5v14M5 12h14"/>
</svg>

<!-- 有意义（按钮内） -->
<button aria-label="新增">
  <svg viewBox="0 0 24 24" width="20" height="20" fill="none"
       stroke="currentColor" stroke-width="2" stroke-linecap="round"
       stroke-linejoin="round" aria-hidden="true" focusable="false">
    <path d="M12 5v14M5 12h14"/>
  </svg>
</button>
```

### 18.2 React 图标组件（tree-shaking + currentColor）
```tsx
type IconProps = React.SVGProps<SVGSVGElement> & { title?: string };
export function PlusIcon({ title, ...props }: IconProps) {
  return (
    <svg viewBox="0 0 24 24" width="20" height="20" fill="none"
      stroke="currentColor" strokeWidth={2} strokeLinecap="round"
      strokeLinejoin="round" aria-hidden={title ? undefined : true}
      focusable="false" role={title ? 'img' : undefined}
      aria-label={title} {...props}>
      <path d="M12 5v14M5 12h14" />
    </svg>
  );
}
```

### 18.3 spinner（尊重 reduced-motion）
```css
.spin { animation: dp-spin 1.2s linear infinite; }
@keyframes dp-spin { to { transform: rotate(360deg); } }
@media (prefers-reduced-motion: reduce) {
  .spin { animation: none; }
}
```

### 18.4 Material Symbols 子集化（防 295KB）
```html
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined&icon_names=home,settings,close&display=block" rel="stylesheet" />
```

---

## 19. 取源与验证（Sources & Verification）

- **官方文档（读原文）**：Lucide Guide、Google Material Symbols Guide、Ant Design Icons（默认 1em、`Outlined/Filled/TwoTone`、`currentColor`）、Heroicons、Carbon Icons、Fluent UI Icons、Radix Icons。
- **GitHub API 实测（2026-11-07）**：lucide 25,616★（license NOASSERTION）、tabler/tabler-icons 22,572★ MIT、microsoft/fluentui-system-icons 10,962★ MIT、radix-ui/icons 2,707★ MIT；Tabler/icons、phosphor-icons 因限频未取到（已剔除不可靠线索）。
- **数值口径纪律**：所有网格/描边/尺寸/间距数值来自官方文档或本次 API 实测；Lucide stroke=2、Heroicons outline stroke=1.5、Carbon stroke=1.5、Material opsz 20–48/wght 100–700/GRAD −50..200/FILL 0–1、字体 295KB→1.7KB 均为文档原文或实测；未逐库重测的 star/许可一律不入资产正文。
- **未决项**：Lucide 实际许可证（API 返回 NOASSERTION，社区称 ISC）——以仓库 LICENSE 文件为最终准；本轮未改动该表述。
