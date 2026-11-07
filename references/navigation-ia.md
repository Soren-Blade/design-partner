# 导航与信息架构 · Navigation & Information Architecture

> 每日升级 #23（v26 → v27）。取源：Apple HIG · Navigation（tab bar 5 项上限）/ Material 3 Navigation（bar 3–5 · rail 3–7 · drawer 在 Expressive 中被 expanded rail 取代）/ Nielsen Norman Group（信息气味 · 汉堡菜单可发现性 · 3-click 迷思）/ WAI-ARIA APG（tabs / disclosure）/ WCAG 2.4.x 导航类成功准则 / GOV.UK Navigation 模式。
> 接线：SKILL.md 路由 + 第 5 步原则 + 第 6 步自检；aliases.json；knowledge-map 支线 U；Design-related websites.txt 已补「导航与信息架构」分区。

## 0. 一句话立场

**导航不是「放几个链接」，是「替用户画一张随时能找到自己的地图」。** 任何界面在用户眼里只有两个问题：*我在这、怎么去那*。其余一切（菜单数量、汉堡还是 tab、面包屑、搜索）都是为这两个问题服务。可访问性是这条线的及格线——键盘到不了、读屏念不出的导航等于没写。

---

## 1. 导航的四类职责（先分清楚再用形态）

| 类型 | 作用 | 典型载体 | 错配后果 |
|---|---|---|---|
| **全局导航**（Global） | 跨全站跳转主要区域，常驻 | 顶部水平 / 侧边栏 / 底部 tab | 用户迷路，靠浏览器后退硬闯 |
| **局部导航**（Local） | 当前区域内的下钻（子栏目、章节） | 侧栏二级、抽屉、标签页 | 进了一级出不来，重复点进同一处 |
| **上下文导航**（Contextual） | 内容体内的相关跳转（「查看更多」「上一篇」） | 内联链接、翻页、上一/下一 | 阅读中断，需回退再找 |
| **辅助导航**（Auxiliary） | 不进主任务流的入口（页脚链接、帮助、法律） | 页脚、帮助入口 | 次要但缺失会被判「不专业」 |

**关键判断**：一个产品的导航混乱，90% 不是「链接太少/太多」，而是**四类职责混在同一根线上**（把 footer 链接塞进主导航、把上下文链接做成主导航项）。先给每根线定性，再选形态。

---

## 2. 形态决策矩阵（什么时候用什么）

| 场景 | 首选形态 | 证据 / 数值 |
|---|---|---|
| 5 个以内**同级顶级目的地**、内容型 App | **底部 tab bar**（移动）/ 顶部水平（桌面） | Apple HIG 硬上限 **5 项**；Material 3 navigation bar **3–5 项**；超出自动收进「More」 |
| 6–12 个顶级区、中后台 / 工具型 | **左侧常驻侧栏**（展开 208–240 / 折叠 64） | 侧栏无 5 项硬上限，但需视觉分组；与 `responsive-layout.md` §9 侧栏数值一致 |
| ≥13 个区、或层级深、或空间稀缺 | **汉堡抽屉**（Drawer） | NN/g：抽屉牺牲可发现性换空间；仅在顶级区真多到放不下时用 |
| 同级并列区域、内容区内部切换 | **标签页 Tabs**（非导航） | ARIA tabs pattern；与主导航职责不同（见 §6 纪律） |
| 大屏 + 中量目的地 | **Material navigation rail**（3–7 项） | 介于 tab 与 drawer 之间；桌面/平板侧条 |
| 信息密度极高、专业读者 | **顶部 + 侧栏双层**（global + local） | 中后台 1440 画板惯例；global 顶、local 左 |

**响应式降级路径**（与 `responsive-layout.md` 对齐）：`<768` → 汉堡或底部 tab（≤5 项）；`768–1023` → 顶部导航 / 图标条；`≥1024` → 常驻侧栏 / 双层。折叠侧栏 **64px**、展开 **208–240px**、内容区最小 **≥720px**。

---

## 3. 项数铁律（数量是有科学依据的，不是审美）

- **米勒法则（Miller's Law）**：工作记忆容量约 **7±2**；导航项按 **5–9** 分组是舒适上限。超过就靠**视觉分组 / 二级折叠**，不要硬排一行。
- **全局主导航 5–9 项**：顶级目的地超过 9 个，用户扫描成本陡增；用 mega menu、二级、或把低频项移到页脚 / 侧栏。
- **底部 tab ≤5 项**（Apple + Material 共识）：第 6 项起体验断崖；Apple 直接把多余项收进「More」。
- **侧栏**：无硬上限，但每 7–9 项做一次视觉分组（小标题 / 分隔线）；单屏超过 ~15 项必须可滚动且分组。
- **汉堡抽屉**：容纳项最多，但**可发现性最差**——顶部区若 ≤5，优先 tab 而非抽屉。
- **一个区域内禁止多列**：破坏阅读顺序（与 `form-table.md` 同律）。

---

## 4. 信息架构地基（深度 vs 广度）

- **3-click 规则是迷思**：NN/g 反复实证——用户不在乎点击次数，**只在乎每一步是否知道「点下去会得到什么」**（信息气味，information scent）。把树压到 3 层但每层气味稀薄，比 5 层但气味浓更糟。
- **广度优先于深度**：宁可一层多几个并列项（靠分组管理），不要一路径深 5 层；深层路径用户会放弃。
- **扁平化有上限**：顶级 ≤9、每节点子项 ≤9、总深度 ≤3（内容型）/ ≤4（工具型）是可维护区间。
- **用语义分组，不用字母序**：按用户心智模型（任务/对象）分组，而非按拼音或数据库字段。
- **验证方法**：卡片分类（card sorting）定分组、树测试（tree testing）验路径——比「我觉得合理」可靠（`design-measurement-research.md` §卡片分类 / 树测试）。上线后用**路径分析**看真实找路成本，而非靠主观。

---

## 5. 面包屑（Breadcrumb）

| 类型 | 适用 | 写法纪律 |
|---|---|---|
| **位置型**（Location） | 层级深的站，定位「我在哪」 | 最后一级**纯文字不可点**（当前页）；分隔符 ` / ` 或 `›`，**不**用 `>`（像按钮） |
| **属性型**（Attribute） | 电商筛选结果（分类 > 颜色 > 尺码） | 每项可点回该筛选；清空某属性即移除该项 |
| **路径型**（Path） | 多步向导（已访问历史） | 仅在线性流程用；非线性内容禁用（会误导） |

**位置纪律**：面包屑第一项通常是首页/全站名；当前页项禁用 `href` 且 `aria-current="page"`；移动端空间不够可省略，但**不能**用面包屑替代主导航的可达性。`responsive-layout.md` 已述窄屏表格纪律，面包屑同理——窄屏可截断中间项保留首尾（`… 分类 当前页`），但首尾必须真链接。

---

## 6. 标签页 Tabs（ARIA 的正确打开方式）

- **Tabs ≠ 导航**：了一个最常见的职责错配——用 ARIA `role="tab"` 做整站主导航是**错误**。Tabs 表示「同一内容区内的并列视图」，切换不应改变页面 URL/上下文；跨页面的跳转用链接 + 导航 landmark。
- **APG tabs 键盘契约**：Tab 键进入 tablist 停在**当前激活 tab**（仅一次 tab stop），`←/→` 在 tab 间移动、`Home/End` 跳首尾；有手动激活与时激活两模式（自动激活需 `aria-selected` + 焦点联动）。
- **tabpanel**：每个面板 `role="tabpanel"`、`aria-labelledby` 指向对应 tab、`tabindex="0"`（激活面板可聚焦）；非激活面板 `hidden` 或 `tabindex="-1"`。
- **何时用 tabs vs 侧栏**：≤5 个并列视图且常切 → tabs；层级深或视图多 → 侧栏。不要把 12 个工具塞进 tabs。

---

## 7. 移动端导航降级

- **底部 tab ≤5 项**：Apple HIG 与 Material 共识；图标 + 文字标签（icon-only 在底部 tab 上可，但需 `aria-label`）。
- **Material 3 三形态**：**navigation bar**（手机底，3–5 项）/ **navigation rail**（大屏侧条，3–7 项）/ **navigation drawer**（在 M3 Expressive 更新中**已不再推荐**，改用 expanded navigation rail——它跨断点更顺、功能近乎等价）。老项目抽屉仍可保留，新项目优先 rail。
- **汉堡的代价**：NN/g 多次实验显示汉堡菜单降低低频功能的**可发现性**（用户看不到 = 不存在）；只在该藏时才藏。内容型、品牌型产品**优先可见 tab**，工具型、层级深产品才用抽屉。
- **底部 tab 与拇指区**：底部 tab 落在单手拇指可达区，是移动端最高频操作的最优位置；把「首页 / 搜索 / 我的」这类核心放这里，而非顶部。

---

## 8. 当前位置指示（"You are here"）

- **必须有激活态**：当前导航项用颜色 + 字重 + 图标 + 左侧指示条**至少两项**组合，**永不只靠颜色**（WCAG 1.4.1）。
- **`aria-current` 是机器版「你在这」**：当前项加 `aria-current="page"`（或 `step`/`true`），读屏用户才知道位置；纯 CSS 高亮对读屏无效。
- **位置一致性**：同一页在导航、面包屑、标题三者说的位置必须一致；不一致 = 用户在两个地图间反复核对。
- **聚焦态独立于激活态**：焦点框（2.4.7/2.4.13）与激活高亮是两套视觉，不能互相替代。

---

## 9. 可访问性导航（及格线，不是加分项）

| WCAG SC | 要求 | 落到导航的具体动作 |
|---|---|---|
| **2.4.1 Bypass Blocks** | 跳过重复块 | 每个页面第一个可聚焦元素是「跳到主内容」skip link（`#main`）；导航前插入 |
| **1.3.1 Info & Relationships** | 结构用语义 | 主导航包 `<nav aria-label="主导航">`；多个 nav 必须各有可区分 label（「主导航」「页脚导航」） |
| **2.4.2 Page Titled** | 每页有唯一标题 | `<title>` 反映当前位置，面包屑末级与之对应 |
| **2.4.3 Focus Order** | 焦点顺序 = 阅读顺序 | DOM 顺序：skip link → 主导航 → 内容；`tabindex>0` 一律禁止 |
| **2.4.5 Multiple Ways** | ≥2 种找页方式 | 导航 + 搜索 + 站点地图/页脚索引，至少两套并存 |
| **2.4.6 Headings & Labels** | 标题/标签描述性 | 导航项用语义名词（见 `ux-writing.md` §9：名词 ≤4 字、同级平行） |
| **2.4.7 / 2.4.13 Focus Visible** | 焦点可见 | 导航链接焦点框 ≥2px 周长且状态变化 ≥3:1；内嵌 ≥3px（见 `accessibility.md` §3） |
| **1.4.13 Content on Hover/Focus** | 悬停/聚焦内容可达 | 悬停展开的 mega menu、下拉，必须键盘可开、可停留、Esc 关、不挡焦点 |
| **2.5.5 Target Size（AAA）** | 触控目标 ≥44×44 | 导航链接/图标热区 ≥44dp（见 `accessibility.md` 目标尺寸三档） |

**地标纪律**：一个页面最多一个 `banner`(`<header>`)、一个 `contentinfo`(`<footer>`)、一个 `main`；导航用 `nav` 且多 nav 各带 `aria-label`。读屏用户靠 landmark 跳转，「裸」div 导航等于隐形。

**skip link 可抄结构**（§13.1）：`<a class="skip" href="#main">跳到主内容</a>` + `#main{tabindex:-1}` + CSS `:focus` 才显形。

---

## 10. 搜索与导航协同

- **搜索是导航的备份，不是替身**：WCAG 2.4.5 要求「多种找路方式」，导航 + 搜索二者至少并存；纯靠搜索 = 用户先猜关键词。
- **搜索框位置**：桌面右上或顶栏内嵌；移动端常收进一个放大镜图标（注意：收起降低可发现性，核心产品应常驻）。
- **默认值与示例**：搜索框内占位符写**具体示例**（「搜索产品、文档、API」）而非「搜索」，降低输入门槛（`ux-writing.md` §6：占位符写示例禁替代标签）。
- **即时反馈**：输入即出联想（`autocomplete`），键盘可上下选；联想列表 `role="combobox"`+`listbox`（APG combobox pattern）。
- **零结果也是状态**：搜索无结果要给出「换个词 / 清除筛选 / 联系」三件套（同 `feedback-states.md` 空态五分法）。

---

## 11. 反模式 20 条

1. 全局主导航塞进 9+ 项还不分组
2. 把页脚链接 / 上下文相关链接做成主导航项（职责混淆）
3. 用 `role="tab"` 实现整站主导航（应为导航 + 链接）
4. 底部 tab 放 6+ 项
5. 当前项只靠颜色区分（色盲失效）
6. 导航项 `aria-current` 缺失，读屏不知道在哪
7. 没有 skip link，每次 Tab 都要穿过整条主导航
8. 多个 `<nav>` 不写 `aria-label`，读屏分不清
9. 面包屑最后一级还做成可点链接（循环回自身）
10. 汉堡抽屉藏了核心功能，可发现性归零
11. 下拉/mega menu 鼠标悬停才出、键盘进不去、Esc 关不掉
12. 焦点顺序与视觉顺序不一致（DOM 乱序）
13. `tabindex > 0` 硬控焦点顺序（灾难）
14. 移动端把核心入口全收进抽屉，且抽屉默认关闭
15. 导航项文案含糊（「更多」「其他」「服务」），信息气味稀薄
16. 深度堆到 5 层以上且每层都不解释「点下去得到什么」
17. 用字母序 / 数据库字段序分组，而非用户心智模型
18. 窄屏把导航硬挤成横向滚动条
19. 搜索框占位符写「搜索」两字，零引导
20. 激活态与聚焦态视觉同一套，键盘用户分不清自己在哪、在选哪

---

## 12. 自检 20 项

1. [ ] 主导航项 ≤9 且做了视觉分组？
2. [ ] 底部 tab ≤5 项、移动端核心功能未全藏抽屉？
3. [ ] 每个导航项用名词、同级平行、≤4 字？
4. [ ] 当前项用 ≥2 种视觉信号且含 `aria-current`？
5. [ ] 第一个可聚焦元素是 skip link 且指向 `#main`？
6. [ ] 每个 `<nav>` 都有可区分的 `aria-label`？
7. [ ] 页面只有一个 `<main>`、一个 `<header>`、一个 `<footer>`？
8. [ ] 面包屑末级是纯文字且非链接？
9. [ ] tabs 用的是 ARIA tab pattern、键盘 ←/→/Home/End 可达？
10. [ ] 下拉/mega menu 键盘可开、可停留、Esc 关、不挡焦点（1.4.13）？
11. [ ] 焦点顺序 = DOM 顺序，无 `tabindex>0`？
12. [ ] 导航链接焦点框 ≥2px 周长且变化 ≥3:1（内嵌 ≥3px）？
13. [ ] 搜索与导航并存（≥2 种找路方式，2.4.5）？
14. [ ] 搜索框占位符写具体示例而非「搜索」？
15. [ ] 搜索零结果给出「换词 / 清除 / 联系」三件套？
16. [ ] 信息架构深度 ≤3（内容）/ ≤4（工具），广度靠分组而非深路径？
17. [ ] 分组按用户心智模型，非字母/字段序？
18. [ ] 窄屏导航无横向滚动、无硬挤？
19. [ ] 激活态与聚焦态视觉可区分？
20. [ ] 用路径分析/树测试验证过真实找路成本，而非只靠主观？

---

## 13. 可抄代码

### 13.1 Skip link + 语义导航骨架
```html
<a class="skip-link" href="#main">跳到主内容</a>

<header>
  <nav aria-label="主导航">
    <ul>
      <li><a href="/" aria-current="page">首页</a></li>
      <li><a href="/products">产品</a></li>
      <li><a href="/docs">文档</a></li>
    </ul>
  </nav>
</header>

<main id="main" tabindex="-1">
  <!-- 页面内容 -->
</main>

<footer>
  <nav aria-label="页脚导航"><!-- 法律/帮助等低频链接 --></nav>
</footer>
```
```css
.skip-link {
  position: absolute; left: -9999px; top: 0;
  padding: 8px 12px; background: #fff; z-index: 1000;
}
.skip-link:focus { left: 8px; }   /* 仅聚焦时显形，2px+ 焦点框 */
#main:focus { outline: none; }     /* 容器聚焦不画框，避免双击选中难看，但保留 tabindex=-1 接住焦点 */
```

### 13.2 响应式导航（桌面侧栏 / 移动抽屉）
```css
.nav { width: 240px; }                 /* 展开侧栏 */
@media (max-width: 767px) {
  .nav { position: fixed; transform: translateX(-100%); width: 80vw; max-width: 320px; }
  .nav.open { transform: translateX(0); }
  /* 折叠态 64px 见 responsive-layout.md §9；移动端改抽屉 */
}
/* 当前项：颜色 + 左条 + 字重，三项里至少两项 */
.nav a[aria-current="page"] { font-weight: 600; border-left: 3px solid var(--brand); color: var(--brand); }
```

### 13.3 ARIA Tabs 键盘处理（手动激活）
```html
<div role="tablist" aria-label="设置分类">
  <button role="tab" id="t1" aria-selected="true"  aria-controls="p1">通用</button>
  <button role="tab" id="t2" aria-selected="false" aria-controls="p2" tabindex="-1">通知</button>
</div>
<div role="tabpanel" id="p1" aria-labelledby="t1" tabindex="0">…</div>
<div role="tabpanel" id="p2" aria-labelledby="t2" tabindex="0" hidden>…</div>
```
```js
// ←/→ 移动焦点并同步选中（自动激活时额外切面板）；Home/End 跳首尾
tablist.addEventListener('keydown', e => {
  const tabs = [...tablist.querySelectorAll('[role=tab]')];
  const i = tabs.indexOf(document.activeElement);
  if (e.key === 'ArrowRight') tabs[(i+1)%tabs.length].focus();
  if (e.key === 'ArrowLeft')  tabs[(i-1+tabs.length)%tabs.length].focus();
  if (e.key === 'Home') tabs[0].focus();
  if (e.key === 'End')  tabs[tabs.length-1].focus();
});
```

### 13.4 面包屑（位置型，末级非链接）
```html
<nav aria-label="面包屑" class="breadcrumb">
  <ol>
    <li><a href="/">首页</a></li>
    <li><a href="/products">产品</a></li>
    <li aria-current="page">设计伙伴</li>   <!-- 末级：纯文字，不可点 -->
  </ol>
</nav>
```

### 13.5 搜索框 + combobox 联想（APG pattern 节选）
```html
<label for="q">搜索</label>
<input id="q" role="combobox" aria-expanded="false"
       aria-controls="suggestions" aria-autocomplete="list" />
<ul id="suggestions" role="listbox" hidden>
  <li role="option" id="o1">设计系统文档</li>
</ul>
```

---

## 14. 与其他参考的接线

- 项数/分组 → 本节 §3、§4（米勒 7±2、深度≤3）
- 工具栏/图标按钮可访问性 → `iconography.md` §10、`accessibility.md` §3
- 窄屏断点/侧栏数值 → `responsive-layout.md` §9、§12
- 导航文案（名词 ≤4 字、同级平行）→ `ux-writing.md` §9
- 焦点框/目标尺寸 → `accessibility.md` §3（24/44/60 三档）
- 搜索零结果空态 → `feedback-states.md` §5（空态五分法）
- 树测试/卡片分类验证 → `design-measurement-research.md` §研究方法
- 汉堡降级路径 → `responsive-layout.md` §9（导航降级路径）
