# 设计 Token 体系 — Design Tokens（深度蒸馏）

> 本文件解决「**怎么用一套数值统管整个产品**」。内容蒸馏自 Ant Design 官方规范（values/colors/font/layout 四篇原文）+ Material Design 3 + Apple HIG 的交叉比对，中文设计系统矩阵经 GitHub API 于 **2026-10-29** 逐库验证（star 数与最近推送）。
> 使用时机：L2 系统级任务、需要输出 token 表 / DESIGN.md / 主题系统时**必读**。
> 快照 2026-10-29

---

## 一、三层架构（唯一正确的组织方式）

| 层 | 名称 | 存什么 | 命名示例 | 谁改它 |
|---|---|---|---|---|
| **L1** | Base / 原始值 | 纯数值，无语义。全量色阶、字号、间距 | `--blue-6: #1677ff`<br>`--space-4: 16px` | 几乎不改，只在换品牌时整体替换 |
| **L2** | Semantic / 语义角色 | 把原始值绑到用途上 | `--color-primary: var(--blue-6)`<br>`--color-text-secondary`<br>`--space-gutter` | 换主题、暗色模式改这层 |
| **L3** | Component / 组件专用 | 单个组件的局部覆盖 | `--button-height: 40px`<br>`--card-padding: 24px` | 只在组件需要偏离系统时用 |

**铁律**：
1. 组件代码**只能引用 L2/L3**，绝不直接写 L1 或硬编码色值。
2. L3 存在的前提是"确实需要偏离"，不是"图省事"。L3 泛滥 = 系统失效。
3. 暗色模式只改 L2 的映射，L1 不动（色阶本身不变）。

**实证**：Pinterest 线上 CSS 变量正是这套三层——`--base-*` / `--sema-*` / `--comp-*`（见 `design-md-format.md` 的 Pinterest 条目）。这不是理论，是一线产品的实际做法。

---

## 二、Ant Design 数值体系（中文语境最完整的一套）

Ant Design 的字体方案基于「动态秩序」原则，**结合自然对数与音律规则**推导；布局基于柯布西耶模度思想。以下是可直接抄用的数值。

### 2.1 色彩

| 项 | 数值 | 说明 |
|---|---|---|
| 基础色板总量 | **120 色** | 12 个主色 × 10 阶（`-0` 到 `-9`） |
| 12 个主色 | red / volcano / orange / gold / yellow / lime / green / cyan / **blue** / geekblue / purple / magenta | 每色带情绪标签（如 blue=包容·科技·普惠） |
| 品牌主色选取规则 | **取色阶第 6 档**（从浅到深第 6 个） | Ant 品牌色 = `blue-6` = **#1677ff** |
| 中性色 | **13 色**（白→黑） | 用**透明度**实现，而非固定灰值 |
| 色彩模型 | **HSB** | 便于调整时有明确心理预期，也便于团队沟通 |
| 正文/标题对比度 | **≥ 7:1（WCAG AAA）** | 比 AA 的 4.5:1 更严 |

**中性色的透明度实现（浅色 / 深色双值）**：

| 角色 | 浅色 | 深色 |
|---|---|---|
| 标题 / 一级文本 | `#000000E0` | `#FFFFFFD9` |
| 二级文本 | `#000000A6` | `#FFFFFFA6` |
| 禁用文本 | `#00000040` | `#FFFFFF40` |
| 一级边框 | `#D9D9D9` | `#424242` |
| 分割线 | `#0505050F` | `#FDFDFD1F` |
| 布局背景 | `#F5F5F5` | `#000000` |

> **为什么用透明度**：同一个 `E0` 叠在任意背景上都自动适配明暗，省掉一整套深色色板。代价是叠多层时颜色会累积——不要在同一区域叠三层半透明文本色。

**色彩使用态度**：克制的。色彩只服务于「信息传递、操作引导、交互反馈」，不做装饰。插画/展示页可适度破例。

### 2.2 字体

| 项 | 数值 |
|---|---|
| 主字号 | **14px**（由 12 升级而来；依据：显示器阅读距离 50cm、最佳阅读角度 0.3） |
| 主字号对应行高 | **22px** |
| 字阶数量 | **10 个**尺寸（受五音阶与自然律启发） |
| 一套系统实际使用 | **3–5 种**（"保持克制"，展示型页面除外） |
| 字重 | 只用 **400 / 500**；英文加粗用 **600**（semibold） |
| 数字 | `font-variant-numeric: tabular-nums`（等宽，便于纵向对比） |

**字体族栈（直接可用）**：

```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
  'Helvetica Neue', Arial, 'Noto Sans', sans-serif,
  'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol',
  'Noto Color Emoji';
```

> 中文项目需在此栈**前面**插入中文字体（见 `chinese-design.md` §1.3），否则中文会落到 Arial 的字体回退上，字形难看且字重不全。

**字体三条建议（Ant 原文）**：
1. **体系化**：先统一规划主/次/辅助/标题/展示五类，再落地微调。
2. **少即是多**：避免用大量字阶、颜色、字重去制造对比。
3. **像音符一样跳跃**：需要拉开差距时**跳档选字号**（14→20→32），不要逐级 14→16→18，跳档才有韵律。

### 2.3 布局与间距

| 项 | 数值 |
|---|---|
| 统一画板 | **1440px** |
| 主流分辨率 | 1920 / 1440 / 1366，个别 1280 |
| 网格基数 | **8**（偶数思维 + 匹配主流设备） |
| 栅格 | **24 栅格**；Column 随视口缩放，**Gutter 固定** |
| 常用模度 | 8 的倍数双数组（8/16/24/32/40/48/64…） |

**两种适配范式**：
- **左右布局**：左侧导航固定宽度，右侧工作区动态缩放。
- **上下布局**：两侧留白先设最小值，留白到限值后再缩放中间主内容区。

**设计交付给工程师的四件事**：① 明确动态布局范围 ② 保持偶数思维 ③ 交付 Gutter 与 Column 关键值 ④ 区块从 column 起、到 column 止。

### 2.4 圆角与阴影（跨体系通用建议）

| 档 | 值 | 用途 |
|---|---|---|
| 小 | 4–6px | 标签、输入框、小按钮 |
| 中 | 8–12px | 卡片、弹层（**全站主档，占 80%**） |
| 大 | 16–24px | 大容器、Hero 卡 |
| 全圆 | 999px / 50% | 胶囊按钮、头像、徽标 |

**阴影三层足够**：`sm` 悬停微起 / `md` 卡片默认 / `lg` 弹层浮起。**阴影与边框二选一**，同时用会显脏。

---

## 三、三大体系对比（选哪套取决于产品语境）

| 维度 | **Ant Design** | **Material Design 3** | **Apple HIG** |
|---|---|---|---|
| 语境 | 中后台 / 企业级 / 高信息密度 | 跨平台应用 / Android 优先 | iOS / macOS 原生体验 |
| 主字号 | 14px | 14–16px（body large 16） | 17pt（iOS body） |
| 间距基数 | 8 | 4（4dp 基础网格） | 8（点） |
| 色彩 | 12 主色 × 10 阶，品牌色取第 6 档 | **动态色彩**（从壁纸/图像提取种子色生成 tonal palette） | 语义色 + 系统色，强调自适应 |
| 中性色 | 透明度实现 | tonal surface（带主色调的表面色阶） | 语义化（label / separator / fill） |
| 圆角 | 2–6px（克制） | 0–28px 多档（表达性强） | 连续圆角（squircle） |
| 动效 | 克制，功能性 | 强调「表达性动效」，时长偏长 | 物理感（弹簧、惯性） |
| 适用 | 后台/工具/表单密集 | 消费级 App、跨端统一 | 原生 App、追求系统融合 |

**选择规则**：
- 后台、审批、表格、B 端工具 → **Ant Design**（信息密度与中文适配最好）
- 消费级 App、需要品牌表达 → **Material 3**（动态色彩省一套换肤工作量）
- iOS 原生 / 追求"不像网页" → **HIG**
- **不要混用**：三套的圆角语言与间距基数不同，混用必然撕裂。

---

## 四、中文设计系统矩阵（GitHub 验证 · 2026-10-29）

| 系统 | 仓库 | ★ | 最近推送 | 许可 | 定位 |
|---|---|---|---|---|---|
| **Ant Design** | `ant-design/ant-design` | 99,982 | 2026-10-29 | MIT | 中文 B 端事实标准，规范文档最完整 |
| **Element Plus** | `element-plus/element-plus` | 27,827 | 2026-10-29 | MIT | Vue 3 生态主流，后台管理系统首选 |
| **Vant** | `youzan/vant` | 24,406 | 2026-10-27 | MIT | 移动端 Vue，电商场景成熟 |
| **Ant Design Mobile** | `ant-design/ant-design-mobile` | 12,085 | 2026-09-14 | MIT | 移动端 React，与 AntD 同语言 |
| **Semi Design** | `DouyinFE/semi-design` | 10,440 | 2026-10-29 | 见仓库 | 字节系，设计+代码双轨，AI 友好 |
| **NutUI** | `jd-opensource/nutui` | 6,512 | 2026-04-02 | MIT | 京东系移动端（**推送较旧，谨慎新项目**） |
| **Arco Design** | `arco-design/arco-design` | 5,751 | 2026-10-12 | MIT | 字节系 React，视觉更现代 |
| **TDesign** | `Tencent/tdesign` | 4,120 | 2026-10-28 | MIT | 腾讯系，多端多框架（React/Vue/小程序） |
| **Arco Design Vue** | `arco-design/arco-design-vue` | 3,116 | 2026-10-21 | MIT | Arco 的 Vue 实现 |
| **TDesign React** | `Tencent/tdesign-react` | 973 | 2026-10-29 | MIT | TDesign 的 React 子包 |

**选型规则**：
- Vue 后台 → Element Plus；React 后台 → Ant Design；移动端 → Vant / AntD Mobile
- 要"看起来不像传统后台" → Semi / Arco（视觉更轻）
- 需要小程序 + Web + 多框架统一 → TDesign
- 有官方设计规范文档可读的只有 **Ant Design**（这也是它排第一的真实原因）

---

## 五、Token 输出格式（三种落地形态）

### 5.1 CSS 变量（推荐，最通用）

```css
:root {
  /* L1 base */
  --blue-6: #1677ff;
  --gray-1: #ffffff;
  --space-4: 16px;
  --radius-md: 10px;

  /* L2 semantic */
  --color-primary: var(--blue-6);
  --color-bg: var(--gray-1);
  --color-text-primary: #000000e0;
  --color-text-secondary: #000000a6;
  --space-card: var(--space-4);
}

[data-theme="dark"] {
  --color-bg: #000000;
  --color-text-primary: #ffffffd9;
  --color-text-secondary: #ffffffa6;
}
```

### 5.2 Tailwind 配置（工程侧）

```js
theme: {
  extend: {
    colors: {
      primary: 'var(--color-primary)',
      surface: 'var(--color-bg)',
      'text-primary': 'var(--color-text-primary)',
    },
    spacing: { 4: '16px', 6: '24px', 8: '32px' },
    borderRadius: { md: '10px', lg: '16px' },
  }
}
```

### 5.3 JSON（给设计工具 / agent 用）

```json
{
  "color": {
    "primary": { "value": "#1677ff", "type": "color", "description": "主操作、强调" },
    "text": {
      "primary": { "value": "#000000e0", "type": "color" },
      "secondary": { "value": "#000000a6", "type": "color" }
    }
  },
  "space": { "card": { "value": "16px", "type": "dimension" } }
}
```

> 一份 token 三处输出（CSS / Tailwind / JSON）是标准做法；**源头只能有一份**，其余由脚本生成，否则必然漂移。

---

## 六、常见错误（逐条对照）

| 错误 | 后果 | 修法 |
|---|---|---|
| 组件里硬编码 `#1677ff` | 换主题要全局搜索替换 | 改引用 `var(--color-primary)` |
| 用数值命名 `--gray-600` 当语义 | 暗色模式下语义错乱 | 语义层单独定义 |
| 色阶少于 8 档 | 悬停/按下/禁用态无级可用 | 补齐 10 档 |
| 中性色用固定灰值 | 深色模式需整套重做 | 改透明度实现 |
| 字阶用了 7 种 | 页面失序，看不出层级 | 砍到 3–5 种，跳档对比 |
| 圆角 4 种以上混用 | 视觉语言撕裂 | 定 2–3 档 |
| 阴影与边框同时用 | 显脏、显廉价 | 二选一 |
| L3 组件 token 泛滥 | 系统名存实亡 | 每个 L3 需写清"为什么必须偏离" |
| 正文对比度按 AA 4.5:1 就满足 | 中文小字发虚 | 正文按 7:1 更稳（Ant 做法） |
| 暗色模式直接反色 | 刺眼、失去层次 | 降饱和 + 提亮文字层级 + 表面色带主色倾向 |
