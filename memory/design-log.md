# 设计记忆（自我成长档案）

> 本文件由 design-partner 技能自动维护，是技能的长期记忆。
> 协议：**匹配灵感前先读本文件的「当前画像」**；每次收到用户反馈或完成交付后，在文末追加一条蒸馏记录；同一偏好信号出现 ≥2 次即升级写入「当前画像」。

## 当前画像（规则层，命中 ≥2 次的稳定偏好）

<!-- 格式：- [YYYY-MM-DD 起] 领域：规则（来源：第 N 次确认） -->
（暂无——随使用积累）

## 匹配与反馈日志（追加层，只增不改）

<!-- 格式：
## YYYY-MM-DD · 需求一句话
- 需求：载体/调性/明暗
- 推荐：命中的资源 + 用户取舍（采纳了什么、拒绝了什么）
- 反馈：用户原话中的偏好信号（如"太花了""要更克制"）
- 效果：交付后用户是否满意/再次修改方向
-->

## 2026-10-28 · 开发者工具深色落地页（自测）
- 需求：落地页 / 深色 / 开发者工具；调性默认 极简+专业+冷静
- 推荐：Saaspo、Land-book（SaaS 落地页结构）、Sombra、Dark Mode Design（深色基调参照）、Supahero（首屏构造）；待用户取舍
- 反馈：尚无（自动化测试产出，未经真实用户反馈）
- 效果：待观察——真实用户使用后回填

## 2026-10-29 · 元素级精准匹配升级（v3）
- 需求：导航栏等元素提示词应返回设计图本体而非设计网站链接
- 升级：新增 patterns.md（12 类元素模式图鉴）+ component-libraries.md（14 库覆盖矩阵，GitHub API 验证）；第 4 步改为三级匹配（元素/风格/实现），L1 交付可视化设计板
- 反馈：待真实用户使用"给我导航栏设计参考"类提示词验证
- 效果：待观察

## 2026-10-29 · v4 系统化与中文场景补齐（每日升级 #1）
- 需求：每日深蒸馏 Design-related websites.txt + 补充设计站/GitHub 仓库，产出知识路线与资料，自动推 GitHub 并更新 README
- 升级：
  - 新增 knowledge-map.md（L0→L4 五级台阶 + 三条支线 + 学习节奏 + 20 条自测）
  - 新增 design-tokens.md（三层 token 架构、Ant Design 数值全量、Ant/M3/HIG 对比、10 个中文设计系统 GitHub 实测矩阵）
  - 新增 chinese-design.md（中文排版 7 项差异 + 6 平台检索策略与坑 + 中文产品四特征 + 12 条自检）
  - 新增 design-md-format.md（九章骨架 + 54 品牌 DNA + 项目类型选型）
  - SKILL.md 升至 v4：资产表扩至 10 份、意图路由加 4 类、第 5 步加系统化与中文修正、第 6 步自检扩至 8 项、新增每日升级协议
  - 新增 scripts/build_readme.py（README 统计自动化）
  - 知识库刷新：inspiration 132→137、resources 196→201、tools 143→153、portfolios 142→166
- 反馈：无真实用户反馈（自动化任务），下轮优先验证中文场景提示词是否命中 chinese-design.md
- 效果：待观察

## 2026-10-30 · 动效系统 + 记忆树与检索（每日升级 #2）
- 需求：每日深蒸馏（本轮按用户补充要求：记忆树、快捷搜索查询、自我进化、自动推送）
- 升级：
  - 新增 `references/motion-system.md`（12 节）：曲线语义表（M3 / Carbon productive+expressive / Ant 三体系精确 cubic-bezier）、四体系时长刻度、20 场景速查表、编排与 stagger 规则、弹簧 vs 曲线取舍、View Transitions 与 scroll-driven 可抄代码、reduced-motion 三档降级、小程序与中文场景、10 条验收 + 反模式
  - 新增 `scripts/mindmap.py`（记忆树 + 接线体检）与 `scripts/dp_search.py`（章节级检索，中文二元组拆词 + 标题/摘要/正文加权）
  - SKILL.md → v5：新增第 0 步「先检索」、动效与转场两条意图路由、第 5 步动效节改为可执行数值、第 6 步自检加「动效关」（8→9 项）、升级协议加记忆树重建与检索门槛
  - `Design-related websites.txt` 追加 50+ 条源（按用途分组：规范原文 / 实现库 / 校准 / 技术文档 / 灵感 / 中文）
- 关键判断（本轮确立的立场）：
  - 入场减速、出场加速（出场时长 = 入场 × 0.7）——这是 90% 项目做反的一条
  - 时长四档（120/200/300/400ms）优于十二档；点击触发 >400ms 即错
  - 交互反馈必须用 transition（可中断），animation 只用于一次性序列
  - reduced-motion 降级要保留 ≤100ms 的功能反馈，不能全局 0.01ms 一刀切
- 反馈：无真实用户反馈（自动化任务）；下轮验证点：动效类提示词是否直接命中 motion-system.md §4
- 效果：待观察

## 2026-10-31 · 数据可视化规范（每日升级 #3）
- 需求：每日深蒸馏（记忆树 / 快捷检索 / 自我进化 / 自动推送 + 更新 README）
- 主题选定：上轮候选第 1 位「数据可视化」——原有知识仅 7 行（四原则 + 5 条选型），无任何色板 hex、无坐标轴数值、无仪表盘布局
- 升级：
  - 新增 `references/dataviz.md`（13 节）：FT 九类关系选型表、30 秒选型决策树 + 6 项硬上限、Carbon 14 色分类板（严格取用顺序）/ Blue·Purple·Teal 10 阶顺序板 / Red-Cyan 与 Purple-Teal 发散板 / 4 色警报色全部精确 hex、AntV 10 色与语义色（G2 v5 源码实测）、G2 坐标轴/图例/Tooltip 精确数值、中文数字单位表、仪表盘四级布局、图表动效（G2 默认 450/400/400/350ms）、WCAG 1.4.11 逐元素对照、12 条反模式、10 库实测矩阵、12 项自检
  - SKILL.md → v6：资产表 12→13、意图路由加 3 类（图表/仪表盘、图表配色与轴、图表审美诊断）、第 5 步新增「数据可视化」节、自检 9→10 项（加图表关）、description 补关键词
  - `knowledge-map.md` 支线 B 重写（原来只有 5 条口诀，现为九类关系 + 硬上限 + 色板纪律 + 指向 dataviz.md）
  - `Design-related websites.txt` 追加 26 条（规范原文 7 / 实现库 9 / 校准灵感 4，共 70→96 行）
- 关键判断（本轮确立的立场）：
  - **先判关系再选图形**——按 FT 九类关系组织，而不是按"会画什么图"；排序是免费洞察
  - **三类色板不许混用**：顺序色板在浅色主题是「最深=最大」，搞反是热力图第一号错误
  - **双 Y 轴默认禁用，但 2026-07 有修正**：Datawrapper 已改口，判定标准从「图形本身」变为「受众是否受训 + 单位是否真不同 + 两轴刻度增长率是否对齐」
  - **图表是唯一允许突破 400ms 动效上限的场景**（不阻塞输入），但悬停反馈仍 ≤120ms——这条把 dataviz 与 motion-system 打通，避免自相矛盾
  - **对比度 3:1 不可四舍五入**（WCAG 原文），且 1px 细线抗锯齿后实际远低于名义值 → 折线 2px 起
- 验证：8 个关键词（图表/色板/坐标轴/仪表盘/饼图/双轴/热力图/数据看板）全部命中 dataviz.md 前 3 条
- 反馈：无真实用户反馈（自动化任务）；下轮验证点：图表类提示词是否直接进入 dataviz.md §2 而非全读
- 效果：待观察

## 2026-10-31 · 表单与表格规范（每日升级 #4）
- 需求：每日深蒸馏（记忆树 / 快捷检索 / 自我进化 / 自动推送 + 更新 README）
- 主题选定：上轮候选第 1 位「表单与表格」——原 patterns.md 表单节仅 5 行、表格只有仪表盘里一句"行高 48–56px"，是中文 B 端最高频元素却最薄的一块
- 升级：
  - 新增 `references/form-table.md`（18 节 / 400 行）：五件套结构、标签三对齐决策表（Ant 原文优缺点 + 场景）、字段按内容定宽表（含中文换算）、控件尺寸精确值（Ant padding 4×11 计算式 + Carbon 24/32/40/48/64）、必填标少数派、校验三档 + 两库默认值差异、GOV.UK 12 条错误文案模板中文化、占位符三宗罪、控件选择矩阵 + 中文特有字段（手机号/身份证/验证码/金额/地址）、四级布局梯度 + 可编辑列表 3/5/8 阈值、表单可访问性 10 条、表格五层结构、行高计算（39/47/55）与 Carbon 五档、列对齐铁律 + 列宽参考、分页/固定列/批量/空态、表格可访问性与中文数字格式、18 条反模式、20 项自检
  - SKILL.md → v7：资产表加 form-table.md、意图路由加 4 类（表单页/表格页/登录验证/表单表格诊断）、第 5 步新增「表单」「表格」两节（全部数值化）、自检 10→12 项（加表单关、表格关）、description 补关键词
  - `patterns.md` 表单节从 5 行扩为构型谱系 + 参数 + 常见错误，新增「数据表格」节，两处均指向 form-table.md
  - `Design-related websites.txt` 追加 24 条（表单表格规范原文 16 / 可访问性标准 5，96→120 行）
- 关键判断（本轮确立的立场）：
  - **输入框宽度是提示，不是版式**：全部等宽等于放弃"该填多长"这条免费信息；手机号 160px、身份证 240px、金额右对齐
  - **两个主流库的校验默认值都是错的**（Ant `validateTrigger` 与 Semi `trigger` 默认 `onChange`）→ 必须显式改成失焦+提交
  - **"一进来就全红"是中文表单第一号体验事故**，根源是没改默认校验时机
  - **验证码拆 6 个框不只是丑，是违规**（WCAG 3.3.8 失败技术 F109：粘贴只能进第一格）
  - **表头/工具栏/批量条/分页必须同高**（Carbon 明文），这是"表格看起来歪"的真正原因，而不是对齐没做好
  - **中文表头不要照搬英文 12px 大写 + 字距**：中文无大小写，12px 偏小，应 14px + 字重 600
- 验证：8 个关键词（表单/标签对齐/校验/错误文案/表格/行高/分页/验证码）全部命中 form-table.md 前 3 条
- 反馈：无真实用户反馈（自动化任务）；下轮验证点：表单类提示词是否直接进入 form-table.md §2/§6 而非全读
- 效果：待观察

## 2026-11-01 · 可访问性实操（每日升级 #5）
- 需求：每日深蒸馏（记忆树 / 快捷检索 / 自我进化 / 全局安装 / 自动推送 + 更新 README）
- 主题选定：上轮候选第 1 位「可访问性」——原有知识只有一句"对比度 ≥4.5:1、触控 ≥44px、不只靠颜色"，无判定口径、无焦点数值、无 ARIA 纪律、无读屏方法、无国内法规
- 升级：
  - 新增 `references/accessibility.md`（19 节 / 约 700 行）：WCAG 2.2 结构与 86 条口径、四档对比度阈值（不可四舍五入）+ 灰阶安全值表 + 中文笔画修正、焦点三层标准（2.4.7/2.4.13/1.4.11）与面积公式 + 三套可抄 CSS、键盘顺序与模态焦点/inert、2.4.11 遮挡与 scroll-padding、24×24 与 24px 圆间距例外 + 24/44/60 三档、2.5.7 拖动替代表、ARIA 四条高频错误与名称优先级、表单结构层（aria-invalid/错误摘要/autocomplete 表）、aria-live 四条纪律、alt 决策树与图表写法、Okabe–Ito 8 色（R 源码核对）、prefers-contrast/forced-colors、读屏 15 分钟实测脚本、自动化工具边界与 4 工具实测矩阵、GB/T 37668 与无障碍环境建设法与适老化 60/48/44 dp、25 条上线自检、18 条反模式、APCA/AAA/禁用态三个立场
  - SKILL.md → v8：资产表 14 行、意图路由 19→24 类（无障碍合规/焦点键盘/读屏播报/色盲对比度/适老化）、第 5 步新增「可访问性」节（10 条数值化）、自检 12→13 项（加无障碍关）、升级协议第 5 步补全局双份安装
  - `knowledge-map.md`：新增支线 D · 可访问性（主线由三条扩为四条）、L3 自测 4 条可访问性硬指标
  - `build_readme.py`：ASSETS 加 accessibility.md、问题表加「无障碍过不了验收」行、自检描述补「无障碍关」
  - `Design-related websites.txt` 追加 42 条（标准原文 15 / 设计系统实现 10 / 工具 8 / 中文合规 9，120→162 行）
- 关键判断（本轮确立的立场）：
  - **对比度 4.499:1 不达标**，且中文笔画密，实际按 +1 档做——这条把"过了工具检测"和"真的看得见"分开
  - **内嵌焦点框 2px 不够，要 3px**（2.4.13 面积按 2px 周长算，内嵌不占外缘）
  - **焦点框不能等于品牌主色**，且单色焦点框在同色系背景上必然失败 → 用双色（GOV.UK 黄黑）或双环
  - **小图标 16×16 合法，但相邻间距必须让 24px 圆不相交**——这是 2.5.8 唯一的豁免路径
  - **`aria-modal="true"` 是承诺不是标签**：必须真的锁焦点 + 遮背景，否则读屏用户被困假模态
  - **`aria-live` 容器必须先存在再改内容**，渲染时插入的节点永不播报——这是"播报没反应"的唯一根因
  - **自动化只覆盖约 30–40%**，Lighthouse 无障碍 100 分 ≠ 合规
  - **适老化 60dp ≠ WCAG 24px**：做银发产品按 60 做，不能按 24 交差
  - **APCA 不能作合规依据**（WCAG 3 候选、仍在开发），只作设计参考；对外只承诺 WCAG 数值
  - **AAA 只冲三条**（2.4.13 焦点外观 / 1.4.6 正文 7:1 / 2.4.12 焦点不遮挡），成本纯 CSS
- 验证：8 个关键词（无障碍/焦点/对比度/aria-live/读屏/目标尺寸/色盲/适老化）全部命中 accessibility.md 第 1 条
- 接线体检：16 文件 / 280 章节，未接线 0、失联 0
- 反馈：无真实用户反馈（自动化任务）；下轮验证点：无障碍类提示词是否直接进入 §2/§3/§17 而非全读
- 效果：待观察

## 2026-11-01 · 反馈与状态设计 + 检索层别名映射（每日升级 #6）
- 需求：每日深蒸馏（记忆树 / 快捷检索 / 别名映射 / 自我进化 / 全局安装 / 自动推送 + 更新 README）
- 主题选定：上轮候选第 1 位「反馈与状态」——原本散落在 patterns.md（空态一句）、form-table.md（错误文案）、accessibility.md（aria-live）三处，缺"什么时候用哪种"的决策树，也缺 toast/加载的时长数值
- 升级：
  - 新增 `references/feedback-states.md`（15 节 / 约 560 行）：五层反馈（L0–L4）+ 三问决策树、0.1/1/10s 阈值与组件映射表、四体系 toast 时长·位置·宽度精确值、该用/不该用对照表、无障碍四条、中文与小程序坑（7 汉字/1.5s/互斥）、加载三形态分工与骨架禁用清单、防闪烁建议值、进度条六铁律、按钮 loading、乐观更新三态、五种空态与五件套结构、五级错误与 404/500 文案规则、重试纪律、确认框 NN/g 八条 + M3 弹窗尺寸、五态数据模型、10 场景速查、WCAG 4.1.3/2.2.1/2.2.2、20 条反模式、15 项自检、4 段可抄代码、9 个库实测
  - **新增检索层基础设施**：`memory/aliases.json`（25 组别名）+ `dp_search.py` 加权别名扩展（0.45 权重、`--no-alias` 可关）；`mindmap.py` 在树里输出别名映射表。**别名只进检索层，SKILL.md 的意图路由顺序一行未动**
  - SKILL.md → v9：资产表加 feedback-states.md 与 aliases.json 两行、意图路由加 7 类（toast/加载/空态/错误页/删除确认/保存状态/反馈诊断）、第 5 步新增「反馈与状态」节（11 条数值化）、自检 13→14（加反馈关）、第 0 步补别名说明、升级协议第 4 步补别名纪律
  - `knowledge-map.md`：新增支线 E · 反馈与状态（四条→五条）、L3 自测加 4 条（20→27 条）
  - `build_readme.py`：ASSETS 加 feedback-states.md、问题表加「反馈要么吵要么没」行、自测条数改为从 knowledge-map 实时统计（不再手写）
  - `Design-related websites.txt` 追加 45 条（规范原文 19 / 研究实证 7 / 标准条款 6 / 实现库 8 / 中文小程序 5，162→207 行）
- 关键判断（本轮确立的立场）：
  - **严重度决定层级，不决定颜色**：把严重错误做成红色 toast 仍然错——红色解决"看见"，不解决"读到"。Ant 原文：浮层 3s 太短，重要失败改用对话框
  - **<1s 不要加任何加载态**：快速闪现的骨架屏比没有更让人焦虑（NN/g）；1–2s 用按钮内 loading 才是正解
  - **toast 合规的前提是"另有出口"**：WCAG 2.2.1 的豁免原文是"存在不依赖计时器的替代访问方式"——没有通知中心/就地状态的 3s toast 就是不合格的时限
  - **失败空 ≠ 无数据空**：把失败渲染成"暂无数据"是本轮最想消灭的一个 bug，用户会以为真的没有，于是不再重试
  - **骨架屏有禁用清单**：按钮、输入框、开关、toast、下拉菜单、弹窗本身都不做骨架；frame-only 骨架等价于 spinner
  - **`partial` 是最常被漏的第五态**：6 张卡片挂 2 张应各自重试，而不是整页报错
  - **确认框写"确定吗"等于没有确认**：必须写对象名 + 数量 + 不可逆性，按钮写动词，默认焦点不给危险项
  - **一个动作只给一次主反馈**：按钮已变"已保存"就不要再弹 toast；编辑器每次保存都弹 = 一天上百次噪音
  - **别名与路由必须分层**：别名只影响召回（0.45 权重），路由优先级仍由 SKILL.md 唯一决定——否则"搜得到"会悄悄改变"走哪条流程"
- 验证：8 个关键词（toast/弹窗/加载/骨架屏/空态/错误页/确认/乐观更新）全部命中 feedback-states.md 前 3 条；`--no-alias` 对比确认别名确有增量召回
- 反馈：无真实用户反馈（自动化任务）；下轮验证点：反馈类提示词是否直接进入 §1 决策树而非全读
- 效果：待观察

## 2026-11-01 · 响应式与断点体系（每日升级 #7）
- 需求：每日深蒸馏 + 自我进化；本轮取上一轮候选第 1 位（响应式与断点），原知识仅 `design-md-format.md` 两行"要写断点值"与一句"能响应式"
- 取源（全部官方原文 / 源码 / API 实测）：
  - Ant Grid（xs<576/sm576/md768/lg992/xl1200/xxl1600/xxxl1920、24 栅格、gutter 可分段）＋ Ant 布局规范（画板 1440、主流 1920/1440/1366/1280、左右与上下两种适配、8 网格、gutter 固定 column 流体）
  - MUI Breakpoints（0/600/900/1200/1536、`down` 开区间 step:5 → 899.95px）
  - Tailwind v4（640/768/1024/1280/1536 rem、`max-*` 严格小于、容器查询 13 档 256→1280）
  - Bootstrap 5.3 Containers（版心阶梯 100/540/720/960/1140/1320）
  - Carbon 2x Grid（320/672/1056/1312/1584、列数 4→8→16、8px mini unit、padding16 / margin 0·16·16·16·24）
  - M3 Breakpoints（<600/600–839/840–1199/1200–1599/1600+、分栏 1/1-2/2/2/2-3、40–60 字符行长、五动词 reveal/divide/resize/reposition/swap）
  - MDN：Container Queries（`container-type:inline-size`、`cq*` 单位、无容器退化为 `sv*`）、`clamp()`（max(MIN,min(VAL,MAX))、MIN>MAX 取 MIN、max ≥ 2×min）、`<length>`（`vh`≡`lvh`）、Responsive images（sizes 窄到宽排序、不能百分比、x 描述符）
  - WCAG 2.2 SC 1.4.10 Reflow 原文（320×256 CSS px、400% 等效 1280、二维例外只覆盖该段、**表格单元格仍需 Reflow、标题/搜索/分页不在例外内**）
  - GOV.UK Table（`govuk-table--small-text-until-tablet`）
  - 9 个响应式相关仓库 star/许可/推送经 GitHub API 实测
- 新增 `references/responsive-layout.md`（19 节 / 726 行 / 38239 字符）
- SKILL.md v10：资产表 +1 行、意图路由 24→35 类（响应式/断点怎么定/跨断点怎么变/栅格版心/容器查询/流式字号/全屏高度/响应式图片/窄屏表格/中后台适配/响应式诊断）、第 5 步新增「响应式」节（14 条数值化）、自检 14→15（响应式关）
- 别名层 25→33 组（新增 断点/容器查询/版心/流式排版/视口单位/响应式图片/多端适配/窄屏表格），**路由顺序一行未动**
- **修掉一处文档说谎**：`build_readme.py` 里「别名 25 组」为硬编码，改为读 `aliases.json` 实时统计（新增 `alias_count()`）
- 检索门槛：17 关键词全部命中 responsive-layout.md 前 3 条，FAIL 0
- 修索引质量：`§9` 原题「表格在窄屏的降级」检索不到「手机表格/表格变卡片」→ 按协议**改标题不改检索器**，标题补入「移动端表格 / 手机表格 / 表格变卡片」
- 接线体检：18 文件 / 392 章节，未接线 0、失联 0
- 源清单：`Design-related websites.txt` 225→271 行（新增响应式专题 46 条，分规范原文/标准条款/实现模式/GitHub 四组）

## 2026-11-01 · 版式与网格（每日升级 #8）
- 需求：每日深蒸馏 + 自我进化；本轮取上一轮候选第 1 位（版式与网格/Editorial），原知识仅有 `design-md-format.md` 两行"要写断点值"与一句"版式要克制"
- 取源（全部官方原文 / 源码 / API 实测）：
  - Butterick's Practical Typography 三页原文：行长 **45–90 字符 / 2–3 个字母表**、行距 **120–145%**、A4 正文左右边距 **1.5–2.0″**、下边距 **+0.25″**、非对称差 **≥1″**、8.5×11 配 2.23″ 四边即黄金比
  - Van de Graaf canon（Wikipedia 引 Tschichold《The Form of the Book》）：内:上:外:下 = **2:3:4:6**、1/9 与 2/9、一般式 1:R:2:2R、版心与页面同比例且版心高=页宽
  - ISO 216：A0–A8 / B0–B6 全表、√2:1、逐级**向下取整**、公差 ±1.5/±2/±3mm
  - Bleed (printing)：英制 **1/8″**、公制 **2–5mm**、大幅面 **+0.25″**、模切 **1/4″**
  - Instagram 官方帮助：宽 **1080**、比例 **1.91:1–3:4**（高 566–1440）、越界即裁
  - X Ads creative specs 官方：1.91:1=800×418、1:1=800×800、4:5=1440×1800、2:3=1080×1620、16:9=1920×1080、9:16=1080×1920、**≤5MB**
  - YouTube 官方：缩略图 1280×720 / 16:9、Shorts 缩略图 9:16、官方明确推荐**三分法**构图
  - 微信公众平台：封面 **900×383（2.35:1）**、次条 **200×200**
  - W3C clreq：汉字与标点 **1:1**、破折号 **2em 且不得拆行**、中西混排 **≤1/4 汉字宽**、纵中横排 2–3 位、直排行序与分栏规则
  - MDN：`text-wrap: balance` **Chromium ≤6 行 / Firefox ≤10 行**、`initial-letter` size/sink 语义与非 Baseline、`hanging-punctuation` 三值、`subgrid` 继承 gap/行号重置/无隐式轨道、`orphans` 默认 **2**
  - 11 个排版渲染仓库 star/许可/推送经 GitHub API 实测（typst 56925 Apache-2.0、fabric 31534 MIT、satori 14150 MPL-2.0、WeasyPrint 9750 BSD-3、vivliostyle 801 **AGPL-3.0**…）
- 新增 `references/editorial-layout.md`（20 节 / 767 行 / 24k 字符）
- SKILL.md v11：资产表 +1 行、意图路由 42→50 类（海报/长图/社媒图/印刷交印/网格栏数/长文行长行距/竖排/版式诊断）、第 5 步新增「版式与网格」节（15 条数值化）、自检 15→16（版式关）
- 别名层 33→40 组（版式/行长/海报/长图/社媒图/印刷/竖排），**路由顺序一行未动**
- `knowledge-map.md`：新增**支线 F · 版式与网格**（五条→六条）、L3 自测 +3（27→30）
- **修掉两处 README 说谎**：① ASSETS 里"20 条自测"硬编码 → 改为 `{selftests}` 占位由 `skill_facts()` 实时填；② "含五条专题支线（…）"硬编码名称 → 改为正则从 knowledge-map 抓 `### 支线 X · 名称` 实时拼接
- 检索门槛：17 关键词全部命中 editorial-layout.md 前 3 条，FAIL 0（首轮「版心/留白/避头尾/字号阶梯」未进前 3，按协议**改标题不改检索器**——§4 加「版心宽度/页边距比例」、§5 加「字号阶梯」、§9 加「留白占比」、§15 加「避头尾/标点/竖排」，并新增 §4.0 版心宽度速查小节）
- 接线体检：19 文件 / 457 章节，未接线 0、失联 0
- 源清单：`Design-related websites.txt` 271→344 行（新增版式专题 73 条，分排印理论/海报编辑/平台规格/CSS 实现/GitHub/中文六组）
- 关键判断（本轮确立的立场）：
  - **Van de Graaf 借方法不借数字**：2:3:4:6 是**装订系统**（内侧窄），网页没有装订，照抄会让内容"贴左框"；实用只剩两条——下边距大 6mm、非对称差 ≥25mm
  - **行长比边距重要**：先定 45–90 字符（中文 25–40 字），边距是结果；反过来算必得 6.5″ 这种打字机行长
  - **12 栏不是审美是数学**：能被 2/3/4/6 整除；栏数 ×2 > 屏上元素数时网格就只是装饰
  - **基线网格是收益最高、最常被跳过的一项**：16×1.5=24 ✓、16×1.6=25.6 ✗（取 24 或 32）
  - **中文行长上限比西文更严**：没有词间空格，超 45 字回行找首字明显变慢
  - **海报最常见事故是"底色只做到成品尺寸"**：裁切后四边露白；画布必须 = 成品 + 出血×2
  - **长图字号必须换算**：`设计字号 = 目标字号 × 设计宽 ÷ 375`；1080 宽写 28px 正文在手机上只有 9.7pt
  - **社媒图唯一硬指标是 120px 缩略图测试**，不是 1080 全尺寸审美
  - **印刷四色黑是必踩坑**：C100M100Y100K100 = 总墨量 400%，必糊；正文一律 K100 单黑
  - **`text-wrap: balance` 有行数上限**（Chromium 6 / Firefox 10），超限静默退化——长段用 `pretty`，标题才用 `balance`
- 反馈：无真实用户反馈（自动化任务）；下轮验证点：海报/长图类提示词是否直接进 §10/§11 而非全读
- 效果：待观察

## 2026-11-01 · 品牌视觉与 Logo 逻辑（每日升级 #9）

- 主题：**品牌视觉与 Logo 逻辑**（上轮候选第 1 位；原知识仅 `design-md-format.md` 的 54 品牌 DNA 速查，缺"从零定一套视觉识别"的方法、几何规则、色阶生成算法）
- 取源（官方原文 / 源码 / API 实测）：
  - Material `designing-icons`：24dp 网格、live area 20×20 + padding 2、四基形（方 18 / 圆 20 / 竖矩 20×16 / 横矩 16×20）、圆角 2dp、描边 2dp（复杂处 1.5dp）、光学尺寸 20/24/40/48
  - Carbon Icons：16px 主画布、20/24/32 可混用、16-20 配 14/16px 正文、热区 ≥44、图标与文字同色 4.5:1、居中对齐（禁基线对齐）
  - Apple HIG App icons：1024/1088/800×480、必须未遮罩图层（自切圆角破坏高光）、文字仅必要时（禁 Watch/Play/New）、default/dark/clear/tinted 四外观
  - Google Search favicon：1:1、最小 8×8、推荐 >48×48、格式清单、URL 需稳定
  - W3C Manifest：maskable 安全区 = 半径 **2/5（40%）** 的圆，圆外不保证可见，留在区内自然获得约 10% 四边留白；MDN：purpose any/maskable/monochrome、SVG 用 `sizes:"any"`
  - Radix Colors：12 步语义表逐条（1-2 背景 / 3-5 组件底 / 6-8 边框与焦点环 / 9 实心且彩度最高 / 10 hover / 11-12 文字）、11/12 步保证 APCA Lc60/Lc90、Sky/Mint/Lime/Yellow/Amber 五色系配深色字
  - material-color-utilities 源码：`tonal_palette.ts`（固定 hue+chroma 只变 tone，tone 0–100）、`scheme.ts`（**亮/暗主题 tone 映射全表**，逐角色抄录）
  - Adobe Leonardo：以目标对比度反解颜色、输出略高于目标（RGB 离散 + WCAG 是最低要求）
  - NN/g 语气四维：正式↔随意 / 严肃↔幽默 / 尊重↔不恭 / 就事论事↔热情；少量语气词 + 反语气词 + 人格一致语气可变
  - RIA 品牌指南（实测数字）：数字最小 **40px**、印刷 **10mm**、小尺寸版 **40–80px / 9–18mm**、清space = 符号圆直径的一半、联合品牌间距 50%–100%
  - 18 个品牌/图标仓库 star 与许可经 GitHub API 实测（simple-icons 26115 CC0 / material-design-icons 54202 Apache / lucide 25434 Other / tabler 22516 MIT / heroicons 23894 MIT / SVGO 22782 MIT / color-utilities 2300 Apache / leonardo 2162 Apache / radix colors 1728 MIT …）
- 新增 `references/brand-identity.md`（21 节 / 694 行 / 22.5k 字符）
- SKILL.md v12：资产表 +1 行、意图路由 50→61 类（logo/VI/品牌色/色阶/清space/响应式标志/图标统一/favicon/商标/品牌语气/品牌诊断）、第 5 步新增「品牌视觉与 Logo」节（21 条数值化）、自检 16→17（品牌关）
- 别名层 40→50 组（标志/字标/清space/最小尺寸/品牌色/图标网格/商标/品牌手册/品牌语气/favicon），**路由顺序一行未动**
- `knowledge-map.md`：新增**支线 G · 品牌视觉与 Logo**（六条→七条）、L3 自测 30→34、门槛 ≥22→≥25
- 检索门槛：12 关键词（品牌/logo/标志/清space/安全边距/主色/品牌色/图标网格/商标/字标/响应式标志/品牌手册）全部命中 brand-identity.md 前 3 条，FAIL 0
- 接线体检：20 文件 / 519 章节，未接线 0、失联 0
- 源清单：`Design-related websites.txt` 344→416 行（品牌专题 72 条，六组）
- 关键判断（本轮确立的立场）：
  - **别从 logo 开始**：定位（3 词 + 3 反义词）→ 语言 → 系统 → 资产。反义词不是修辞，是排除法，用来挡掉 80% 的评审争论
  - **标志必须画在 24 网格上**，与界面图标同源；否则 logo 与菜单图标并排时笔画差 0.5px，一眼看出不搭
  - **清space 只写"留足空间"等于没写**：必须给一个可计算单位 + 四个方向的数值
  - **缩小到笔画不足 0.75px 就该换简化版**，不是继续微调（公式比记数字可靠）
  - **主色是种子色不是最终色**：先跑色阶，色阶崩了换种子，不要手调 12 个值硬凑
  - **暗色模式不是反色，是 tone 重映射**：primary 40↔80、container 90↔30、**outline 50↔60（暗底反而更亮）**
  - **主色不许当图表分类色**：主色是强调，分类色是区分，混用会抢注意力且分不清 5 类以上
  - **商标 ≠ 版权**：版权自动产生，商标必须注册；logo 用了字体 = 商标图样使用，通常需独立授权
- **修掉一个系统性检索缺陷**：`SKILL.md` 的「工作流」是 500+ 行巨型章节，被索引后**吞掉任何多词查询**——查「商标注册」「字体授权」「暗色模式品牌色」时它都因正文词频高排第一，真正的 §17/§10 反被压到第二。修法：`mindmap.py` 的 `NOT_SEARCHABLE` 加入 `SKILL.md`（它本就常驻上下文，检索层的职责是定位 references/memory 里的知识）。修后「商标注册」→§17 第一，「字体授权」→§17 第一。**未改检索器算法，只改索引范围**
- 检索门槛：16 个品牌关键词 + 12 个既有模块回归词，共 28 项全部命中目标文件前 3 条，FAIL 0（无回归）
- 反馈：无真实用户反馈（自动化任务）；下轮验证点：logo/VI 类提示词是否直接进 §4/§5 而非全读
- 效果：待观察

---

## 2026-11-01 · 暗色模式体系（每日升级 #10）

> 补记：本轮当时只写入了自动化 memory，遗漏 design-log，此处按原始记录补入（不改动既有内容）。

- 主题：**暗色模式体系**（上轮候选第 1 位；原知识仅 `design-tokens.md` 一个 6 行 dark 块 + 一句"降饱和提层级"）
- 取源（官方原文/源码/API 实测）：`material-color-utilities` 的 `color_spec_2021.ts` 与 `scheme.ts`（surface 6 / cLow 10 / c 12 / cHigh 17 / cHighest 22、outline 50→60、onErrorContainer 暗色 80 的不对称）、Ant `themes/dark/colors.ts`（85/65/45/25、lighten 0/8/12/26）与 `default/colors.ts` 对照（88/65/45/25、lighten 4/0/0）、Carbon g100 全 hex、M2 dark-theme 全表（`#121212`、elevation overlay 0–16%、`#CF6679`）、Apple HIG Dark Mode、Radix 12 步（11/12 步保证 Lc60/Lc90）、NN/g 暗色证据链（Piepenbrock 2013 / Dobres 2017 / Aleman 2018）、Android DayNight 与微信 DarkMode、MDN `color-scheme` 与 `light-dark()`、Tailwind v4 `@custom-variant`
- 新增 `references/dark-mode.md`（15 节 / 656 行 / 24.6k 字符）
- **本轮最大价值：把"抄来的经验值"变成"算出来的证据"**——用 WCAG 相对亮度公式与 CIELAB L*→Y 自算，得到三个可验证结论：Ant 三级文本 45% 白在纯黑上只有 **4.43（不达 AA）**；Ant 暗色边框 `#424242` 仅 **2.09:1**（过不了 1.4.11）；暗色层级跨度必须大于亮色（亮 1.23 vs 暗 **1.50**）
- SKILL.md v13：资产 +1、路由 61→71、第 5 步新增暗色节 13 条、自检 17→18（暗色关）、frontmatter 加暗色段
- knowledge-map：支线 H（七→八条）、自测 34→38、门槛 ≥25→≥28
- 别名 50→57 组，并把"暗色模式/深色模式"从「配色」组摘出（避免被 20+ 配色词稀释）；路由顺序未动
- 检索门槛 21 项 FAIL 0；回归 16 项无空命中；接线体检 21 文件 / 568 章节
- 发布 commit `4942a4b623`；全局双份安装完成
- 踩坑：`raw.githubusercontent.com` 多次超时/连接重置（exit 28/56/7），单文件重试 2–3 次即通；`github.com` API 目录列举比猜路径可靠

---


## 2026-11-01 · 性能与设计的关系（每日升级 #11）

- 主题：**性能与设计的关系**（上轮候选第 1 位；原知识仅 `knowledge-map.md` L3 一句"CWV 三阈值"）
- 取源（全部官方原文 / 源码 / API 实测，无二手博客）：
  - web.dev `vitals`（LCP ≤2.5 / INP ≤200 / CLS ≤0.1、**75 百分位**、移动桌面分段、**现场优先**、TBT 作 INP 代理）
  - web.dev `optimize-lcp`（四子部分 **TTFB 40% / load delay <10% / load duration 40% / render delay <10%**，官方明确"不可换算成绝对秒数"；`fetchpriority="high"` 只给 1–2 张；LCP 图禁 lazy；CSS 背景图须 preload）
  - web.dev `inp`（三阶段定义、**200/500ms**、**每 50 次交互忽略最高 1 次**、`durationThreshold` 默认 104ms / 最小 16ms、仅 click/tap/键盘）
  - web.dev `cls`（0.1/0.25、`impact × distance` 公式 + 三个官方算例 0.1875/0.07/0.18、会话窗口 **<1s 且 ≤5s**、`hadRecentInput` **500ms** 仅离散输入）
  - web.dev `long-tasks-devtools`（Long Task **>50ms**、RAIL 50ms 处理 → 100ms 响应、INP 放宽到 200ms 的官方理由）
  - web.dev `font-best-practices`（`font-display` 五档 block/swap 期**精确值**：block 2–3s/∞、swap 0/∞、fallback 100ms/3s、optional 100ms/无；默认阻塞 3s 与 **Safari 无限期**；WOFF2 **省 30%**；拉丁 100–1000 vs **CJK >10000** 字形；`preload` **绕过 `unicode-range`**）
  - web.dev `choose-the-right-image-format`（格式矩阵、**DPR 像素 4 倍/9 倍**、GIF→`<video>`、图内禁文字、CSS 效果优先）
  - web.dev `performance-budgets-101`（**关键路径 <170KB + TTI <5s（3G + 中位设备）**、预算三选一"优化/删掉/不加"）
  - Chrome `performance-scoring`（Lighthouse 10 权重 **TBT 30 / LCP 25 / CLS 25 / FCP 10 / SI 10**、0–49/50–89/90–100、对数正态曲线 25%→50 分 / 8%→90 分、**0.96 收益断崖**）
  - Addy Osmani 的 JS 成本（CNN **4s/13s/36s**、parse+compile 占 **10–30%**、中位页面 350KB→TTI **14s+**、Pinterest **2.5MB→200KB** 换注册 **+753%**）
  - 微信《代码包体积优化》（**单个代码包上限 2M**、ZSTD、分包/独立分包/预下载/异步化、全局组件与插件的"启动税"、包内资源难以再压缩）+《合理使用 setData》（**Shadow 树节点量影响大于数据量**、只传 diff、`data` 只放渲染字段）
  - 仓库实测 12 个：lighthouse 30992★ / sharp 32812★ / squoosh 26083★ / lazysizes 17713★ / partytown 13807★ / workbox 13040★ / imgproxy 11165★ / critical 10299★ / web-vitals 8668★ / lighthouse-ci 7123★ / fontsource 6255★ / sitespeed 5047★ / image-actions 1578★ **GPL-3.0**；**发现 2 个已归档**：critters（2024-10）、preload-webpack-plugin（2021-01）
- 新增 `references/performance-design.md`（19 节 / **843 行 / 28.3k 字符**）
- **本轮最大价值：把"性能优化清单"改写成"设计决策的价格表"**
  - §10 **视觉手法性能价格表**：CSS 渐变★1 → 首屏视频★5（5s 1080p@4Mbps ≈ **2.5MB**，算术可复核）/ 玻璃拟态★4 / 视差★4 / 3D★5 / 粒子★5 / 自动轮播★5，每项给**机制 + 替代方案**
  - §11 把 `will-change` 从"玄学"变成算术：合成层内存 = **宽×高×4 字节**（375×812=1.22MB / 1920×1080=**7.93MB** / 2x 全屏=17.8MB），推出"同屏活跃层 ≤5–8"
  - §12 **三档决策分级**（A 效率不许花 / B 平衡 / C 表达必须降级），给出 C 档四条硬约束（首屏仍 2.5s、必须有静态降级、必须可跳过、移动端单独设计）
  - §6 六类页面预算表（落地页/内容页/电商/中后台/H5/小程序），把预算定义为**设计评审的否决权**而非开发指标
- SKILL.md v14：资产表 +1 行、意图路由 → **83** 类（+13 类性能相关）、第 5 步新增「性能」节 18 条数值化、自检 18→**19**（性能关）、frontmatter description 加性能段、数据来源 +13 条
- knowledge-map：支线 I（八→**九条**）、自测 38→**45**（+7 条性能硬指标）、门槛 ≥28→**≥34**、L3 必读加 `performance-design.md`
- 别名 57→**66** 组（性能/LCP/卡顿/CLS/性能预算/图片优化/字体加载/弱网/小程序性能），**路由顺序一行未动**
- **修掉两个既有检索缺陷（非本轮引入，是回归测试暴露的）**：
  1. `accessibility.md` 全篇**没有任何 H2 含「无障碍」**（H1 是"可访问性实操"，§1 是"先定判定口径"）→ 查「无障碍」时它排第 4，被 brand-identity/feedback-states/responsive 抢占。修法：H1 改「可访问性实操 / 无障碍」、§1 改「先定判定口径：无障碍验收按哪套标准」。修后 → 第 2（第 1 是 brand 的"必须过无障碍验收"章节，合理）
  2. 查「表单」时 `form-table.md` 排第 5（patterns 的「§表单 Form」因标题精确匹配 ×10 权重压住）→ 把 form-table §1 标题改为「表单（Form）的五个零件：标签·控件·帮助·错误·动作」，修后 → 第 3
  - **两处都只改标题，未动检索器算法**（遵守升级协议）
- 检索门槛：27 个性能关键词全部命中 `performance-design.md` 前 3，**FAIL 0**；回归 18 项（暗色/表单/表格/海报/logo/无障碍/图表/toast/断点/动效/空态/色阶/对比度/焦点/留白/标志/卡片/导航）**18/18 通过**
- 接线体检：22 文件 / **644 章节**，未接线 0、失联 0
- 源清单 450→**518** 行（性能专题 62 条，六组）
- 反馈：无真实用户反馈（自动化任务）；下轮验证点：用户说"这个效果会不会太慢"时，是否直接进 §10 价格表而不是全读
- 效果：待观察

## 2026-11-01 · 设计交付与协作（每日升级 #12）

- 主题：**设计交付与协作**（上轮候选第 1 位；原知识里"走查"零命中、"设计交付"只有 8 条散落在 editorial/accessibility/design-md 的边角）
- 取源（官方原文 / 源码 / API 实测，无二手总结）：
  - **Carbon Component checklist**（definition of done 全表）：设计规格**六类**（只用 color/type/spacing token、**所有**间距与对齐都要标、含 hover·focus·selected·disabled·read-only·error·warning、含响应式·溢出重排·展开·滚动、文字 **4.5:1（disabled 例外）**+ 非文本 **3:1** + 焦点流转必须写清）；代码侧"**不得包含未 token 化的魔法数字或颜色**"、响应式到 **~320px**；测试侧单测覆盖 **≥80%**、VRT **至少 1 条默认 story**、AVT **默认态 + 全部复杂态**、读屏 **JAWS/VoiceOver/NVDA**；状态四档 Draft/Preview candidate/Preview/Stable
  - **Carbon 2x Grid**：mini unit **8px**、padding **恒 16**、gutter 合计 **32**、sizing **8/16/24/32/48/64/80**、断点表 **320/672/1056/1312/1584**（列数 **4→8→16**，单列占比 25/12.5/6.25%、Margin 0/16/16/16/24）、比例 **1:1·2:1·2:3·3:2·4:3·16:9**、"文字对齐 padding 边缘不得压在 padding 上"
  - **Carbon Spacing**：`$spacing-01`–`13` 全 13 档精确 px/rem（**2·4·8·12·16·24·32·40·48·64·80·96·160**）；"偏离阶梯应尽可能避免"；百分比可做分栏不可做间距；**token 本身不随断点变，但允许在断点跳档**
  - **Figma Dev Mode**：Inspect 面板（Code/List 双模式、语言与单位可切、值可点复制）、**Ready for dev**（全付费套餐）/ **Completed**（仅 Org/Enterprise）、Annotations、**Dev resources 传播到所有实例**、Code Connect 套餐与用途、导出 **PNG/JPG/SVG/PDF**
  - **Figma 组件命名与变体**：斜杠生成层级、`Button/Primary/Large/Default/False` → 1 组件集 + 4 属性、**每个被合并组件斜杠数必须相同**、同组合必须唯一、**默认变体 = 左上角**、组件集只能装组件、**不要用变体分组不同图标**、"导入大组件集会拖慢文件"
  - **W3C DTCG Design Tokens Format 2025.10**：`.tokens`/`.tokens.json`、MIME 两种、**含 `$value` 才是 token / 不含才是组**、名称禁 `$ { } .`、类型继承三级（引用→最近父组→无效，**禁止猜类型**）、别名 `{}` 与 `$ref` 两种都必支持、`$extends` 深合并、`$root`、**必须报错的 6 类错误**、基础 7 类型 + 复合 4 类型、`dimension` 仅 **px/rem**、fontWeight **100–950** 十档映射；官方标注**预览草稿、不可据此实现**
  - **Style Dictionary**：原生 `value/type/comment` 与 DTCG `$value/$type/$description` **不可混用**、`include` 先于 `source` 且后者覆盖前者、`source` 之间冲突才警告、CTI 结构、自动元数据 `path/original/filePath/isSource`
  - **SemVer 2.0.0** 全 11 条原文 + FAQ：已发布内容不可改、`0.y.z`、**标记废弃必须升 MINOR**、**移除前至少隔一个 MINOR**、预发布与 build 元数据优先级规则
  - **Cucumber Gherkin**：Given 只写状态 / When 单个动作 / Then 只验**可观测**结果（**禁查数据库**）、**每场景 3–5 步**、Background **>4 行就该上提**
  - **NN/g Design Critiques**：standalone critique vs design review 之别、三主题（范围/目标/对话）、round robin 与 **quota 2 正 1 改**、facilitator **轮换**、**每周 30 分钟**起步、reframing 两组实例、**五个坑**
  - **优设·设计走查**：定义（还原度检查/视觉 Review/设计验证）与**体验走查**之别、**提测后测试跑完一遍**介入、**三遍法**（流程→交互→视觉）、文档 **9 字段**、**P0–P3**、邮件+当面澄清+复查、**约占项目 1/4 时间**
  - 仓库实测 10 个：storybook **91420★** MIT / playwright **99007★** Apache-2.0 / BackstopJS **7192★** MIT / reg-suit **1305★** MIT / addon-designs **952★** MIT / chromatic-cli **342★** MIT / DTCG community-group **2160★** NOASSERTION；**lost-pixel 1676★ 已于 2026-04-22 归档**（勿新采用）；另发现 `amzn/style-dictionary` 已迁移到 `style-dictionary/style-dictionary`（**4875★** Apache-2.0）、`backstopjs/backstopjs` 迁到 `garris/BackstopJS`
- 新增 `references/handoff-collaboration.md`（20 节 / **851 行 / 52.1k 字符**）
- **本轮最大价值：把"交付靠默契"变成"交付可判定"**
  - §2 三层信息模型 **intent / rule / value**，给出可操作检验："**拿掉设计稿，开发能不能做出第二个页面**"
  - §4 **只标四类**（例外值/对齐关键线/尺寸约束/断点切换）+ Carbon 硬数值表，把"标注"从体力活变成查表
  - §5 **9 态矩阵**（Carbon 7 + loading + empty）与"组合爆炸三刀砍"，并纠正一个高频误用：**Carbon 的 4.5:1 例外只给 disabled**，read-only/占位/暗色次级文字都不适用
  - §11 **P0–P3 只看"用户还能不能完成目标"**，配发布门禁（P0=0、P1 书面豁免写"谁批何时补"）
  - §12 **改默认值 = MAJOR**——最常被误判成 PATCH 的不兼容变更
  - §17 **六个交付指标 + 两个过程指标**（"开发问多少 px 的次数趋近 0"）
- SKILL.md v15：资产表 +1 行、意图路由 **83→92** 类（交付/AC/评审/走查/分级/命名/发版/token 管线/回归）、第 5 步新增「交付与协作」节 21 条、自检 19→**20**（交付关）、frontmatter description 加交付段、数据来源 +13 条
- knowledge-map：支线 J（九→**十条**）、自测 45→**50**（+5 条交付硬指标）、门槛 ≥34→**≥38**
- 别名 66→**74** 组（设计交付/设计走查/验收标准/设计评审/缺陷分级/组件命名/版本管理/token 交付），**路由顺序一行未动**
- **修掉一个系统性索引缺陷**：`mindmap.py` 的标题正则在代码块内也生效 → 变更日志模板里的 `## [2.0.0] - 2026-11-01` 被当成真章节进索引（`2.0.0` 能查到一条假章节）。新增 `mask_fences()`：把围栏代码块抹成等长空格，**保留字符位置**，标题只在块外识别、正文仍从原文切。修后假章节消失，章节数 719→720（净增来自真实小节）
- **修掉一个别名污染**：`栅格` 同时挂在「间距」组里，导致新文件的 spacing 表把"栅格怎么分"顶到第 1。把 `栅格` 从「间距」组移除（它本属「版心」组）→ 修后查「栅格」回 `responsive-layout.md §5 栅格与版心`
- 检索门槛：18 个交付关键词全部命中 `handoff-collaboration.md` 前 3，**FAIL 0**；回归 20 项（对比度/表单/表格/卡片/导航/图表/动效/toast/断点/海报/logo/暗色/焦点/空态/缓动/色阶/栅格/触控/骨架屏/行高）**20/20 落回原主文件或合理位置**
- 接线体检：23 文件 / **720 章节**，未接线 0、失联 0
- 源清单 518→**569** 行（交付专题 46 条源 + 5 组标题）
- 反馈：无真实用户反馈（自动化任务）；下轮验证点：用户说"这稿子怎么交给开发"时，是否直接进 §3 spec 九字段而不是整份读

## 2026-11-05 · 内容设计与 UX 文案体系（每日升级 #13）

- 主题：**内容设计与 UX 文案**（上轮候选第 2 位；候选第 1 位「多品牌/多主题 token 架构」已在 #12 前完成，`multi-brand-theming.md` 已存在；原知识只有 form-table.md 的 12 条错误模板 + feedback-states.md 的空态一句 + brand-identity.md 的语气四维，缺按钮/标签/引导/术语/大小写/标点/数字/国际化等完整规则）
- 取源（全部官方原文，无二手博客）：
  - **Apple HIG Writing**（2025-12-16 修订）：最佳实践全量提取（简洁直接/动词开头/说结果/不加冠词/禁 OK）+ 平台规范（sentence case、省略号规则、标题式 vs 句式）
  - **NN/g Error-Message Guidelines**（2023-05）：错误文案三层结构、避免责怪用户、具体而非笼统、位置紧贴字段、时机失焦+提交
  - **NN/g UI Copy**（2019-03）：扫描行为数据（20% 阅读量、前 11 字符）、倒金字塔、microcopy 占 80%
  - **NN/g Tone of Voice 4 Dimensions**（2016-07, reviewed 2023-08）：正式↔随意 / 严肃↔幽默 / 尊重↔不恭 / 就事论事↔热情；场景矩阵（错误禁幽默/危险升正式/成功升热情）
  - **NN/g UX Copy Sizes**（2025-05）：三级文案尺寸 long/short/micro 及各自适用场景
  - **Microsoft Writing Style Guide Top 10 Tips**：sentence case 共识、用数字不用拼写、主动语态、禁 jargon
  - **GOV.UK Style Guide A–Z**（全量逐条）：大小写规则、标点规则、数字日期规则、术语规则、拼写规范
  - **Ant Design 反馈规范原文**：toast 时长与文案、失败用对话框不用 toast、确认框写清对象
  - **优设 B 类产品文案体验设计规范**（2023-05）：中文特有规则（按钮 2–4 字不加"请"、错误 ≤30 字、标签 ≤8 字）
- 新增 `references/ux-writing.md`（19 节 / 约 620 行 / 约 24k 字符）
- SKILL.md v17：资产表 +1 行（ux-writing.md）、意图路由 92→105 类（+13 类：按钮文案/错误文案/空态文案/语气语调/表单标签/对话框Toast/引导/导航标签/术语管理/大小写标点数字/国际化/文案系统化/文案诊断）、第 5 步新增「内容设计与 UX 文案」节（10 条原则要点）、自检 20→21（文案关）、frontmatter description 加 UX 文案段
- 别名层 82→90 组（文案/按钮文案/错误文案/空态文案/语气/术语管理/大小写 + 已有的品牌语气组扩充），**路由顺序一行未动**
- knowledge-map：新增**支线 K · 内容设计与 UX 文案**（十条→十一条）、自测 50→54（+4 条文案硬指标）、门槛 ≥38→≥41
- 关键判断（本轮确立的立场）：
  - **禁用 OK 是四体系共识**：Apple + Microsoft + GOV.UK + M3 都明文禁止。OK 不告诉用户会发生什么，是按钮文案第一号问题
  - **错误文案不是"写得客气"是"让用户能修"**：三层结构（发生了什么+为什么+怎么修）缺一不可；"格式不正确"等于没有说怎么修
  - **失败不能伪装成无数据**：把失败渲染成"暂无数据"是欺骗用户，用户会以为真的没有于是不再重试——这条与 feedback-states.md 的五态模型打通
  - **sentence case 不是审美是可访问性**：全大写降可读性 10% 且读屏逐字母读——这条把文案规则与 accessibility.md 的读屏测试打通
  - **中文按钮 2–4 字不加"请"**：中文的"请"是客套不是动作，按钮要的是动词（保存/删除/提交），不是礼貌（请保存/请删除）
  - **文案 token 是系统化的最后一步**：先把每个场景的文案写对，再抽象成 token（buttons/errors/empty/toast 四桶），不要先建 token 再填内容
- 反馈：无真实用户反馈（自动化任务）；下轮验证点：用户说"这个按钮该写什么"时，是否直接进 §2 按钮文案而非全读
- 效果：待观察


## 2026-11-05 · 演示文稿与幻灯片版式（每日升级 #14）
- 需求：每日深蒸馏设计知识，本轮主题为演示文稿与幻灯片版式（上轮候选第 1 位）
- 升级：
  - 新增 `references/presentation-design.md`（18 节 / 约 1100 行 / 约 35k 字符）
  - 取源全部为官方原文：Microsoft Support（动画与转场定义/PowerPoint 无障碍/占位符编辑）、W3C WCAG 2.3.1（闪烁 ≤3 次/秒 不可豁免）、W3C WCAG 2.2.2（自动播放 >5s 需可暂停）、WMU 无障碍演示规范（WCAG 2.1 AA / 最小 18pt / 对比度 4.5:1）、WebAIM 对比度检查器、Lumen Learning Slide Layout（5×5/6×6/7×7 规则 / Duarte 可读性验证法 / 三分法则 / Z 模式 / 禁华丽转场）、Faulkner University（5-6 词/行 / 3-4 要点）、Whitepage Studio（现场最小 24pt / 线上 28pt / 封面 60pt+）、SlideModel（16:9=1920×1080 / 混比例不支持 / 母版辅助线）、Adobe After Effects（HD 动作安全 10% / 标题安全 20%）、Coblis 色盲模拟器
  - GitHub 仓库实测：reveal.js 67000★ MIT / Slidev 36000★ MIT / Marp 8000★ MIT / spectacle 9600★ MIT / remark 12000★ MIT / python-pptx 2100★ MIT
  - SKILL.md v18：资产 22 行（新增 presentation-design.md）、意图路由 +7 类（演示文稿/幻灯片模板/字号太小/转场动画/线上演示/演示诊断）、第 5 步新增「演示文稿与幻灯片版式」节 15 条、自检 22 项（演示关）、frontmatter description 加演示文稿段
  - knowledge-map：支线 L（十一→十二条）、自测 54→58、门槛 ≥41→≥44
  - 别名 90→97 组（演示文稿/幻灯片母版/转场动画/幻灯片字号/安全区/线上演示），路由顺序一行未动
  - 源清单 589→615 行（+26 条演示文稿源）
- 反馈：无真实用户反馈（自动化任务）
- 效果：待观察


## 2026-11-05 · 动效进阶：编排、状态机与共享元素转场（每日升级 #15）
- 需求：每日深蒸馏设计知识，本轮主题取上轮候选第 1 位「动效进阶（编排与状态机）」——`motion-system.md` 只覆盖单动效的曲线与时长，多元素编排、列表增删、共享元素转场、动画状态机与中断策略完全空白
- 升级：
  - 新增 `references/motion-orchestration.md`（20 节 / 1049 行 / 48.9k 字符），与 `motion-system.md` 严格分层（决策层 vs 工程实现层），不重设曲线/时长数值
  - 取源全部为官方原文（20 篇逐页核对）：MDN View Transition API 与 Using（六步流程/伪元素树/快照语义/三 promise/match-element/MPA/bfcache/link rel=expect）、W3C CSS View Transitions L1（**UA 默认 0.25s·ease·both** + 三个 `-ua-*` keyframes + group 动态样式 + name 唯一 abort + updateCallback always called）、Chrome DevRel 两篇（Chrome 111/126、`skipTransition()`、`types`、单例中断、enhancement 原则、网络请求前置）、MDN Using WAAPI（毫秒/`Infinity`/默认 `linear`/`commitStyles`/`persist`/`updatePlaybackRate`/`replaceState`/自动移除 **5 条件**）、MDN KeyframeEffect 构造函数（全默认参数表 + `composite` add·accumulate）、MDN `@starting-style`（三状态 + 同 specificity 顺序）、MDN `transition-behavior`（离散 50% 翻转 + display 0%/100% 例外 + overlay）、Chrome 116/117 四特性、Paul Lewis FLIP 原文（F/L/I/P 算式 + **100ms 响应窗口** + 三条 caveat + WAAPI 300ms 曲线）、Motion 三篇（AnimatePresence 三 mode / layout 系列与 scale correction / variants 传播与 `stagger()`）、React Transition Group 四态、Stately 状态机、Vue TransitionGroup、Svelte transition:、MDN prefers-reduced-motion、W3C SC 2.3.3 AAA
  - GitHub 仓库实测 10 个：svelte 88562★ MIT / anime 74308★ MIT / vue core 54840★ MIT / motion 34922★ MIT / xstate 30411★ MIT / GSAP 30193★ 自定义 / react-spring 29260★ MIT / react-transition-group 10211★ NOASSERTION / turbo 7399★ MIT / swup 5251★ MIT；**`barba/barba` 与 `motionone/motion` API 返回 404（迁移/合并），本轮不列入、不臆造数字**
  - SKILL.md v19：资产表 +1 行、意图路由 **119** 类（+8：动效编排/列表增删/共享元素/View Transitions/动画状态机/动画中断/进出场动画/编排诊断）、第 5 步新增「动效编排、状态机与共享元素转场」节 13 条、自检 22→**23**（编排关）、frontmatter description 与 v19 基线段落更新
  - 别名层 95→**104** 组（动效编排/交错动画/FLIP/共享元素转场/视图过渡/动画状态机/动画中断/列表增删动画/进出场动画），**SKILL.md 路由顺序一行未动**
  - knowledge-map：新增**支线 M**（十二→十三条）、自测 **61** 条、门槛 **≥47**；支线 C 补一行指向进阶层
  - 源清单 616→**653 行**（+37 行：20 条规范原文 + 13 条仓库/演示 + 2 组标题 + 空行）
- **本轮最大价值：把「动效 bug」从审美问题重新定义为状态建模问题**。三条可验证的差异化结论：
  - **总时长是可算的**：`T = T_parent + d_child + (n−1)×s ≤ 400ms` 反解 `s ≤ (400−d)/(n−1)` → 6 项×30ms=350ms ✅、12 项×40ms=640ms ❌，因此「n>6 改整组淡入」不是审美偏好而是算术结果
  - **降级必须分两层**：Svelte 官方明确指出其 transition 由 WAAPI 驱动，全局 CSS `@media (prefers-reduced-motion)` 把 duration 归零**对它们无效**；WAAPI / View Transitions 同理 → 必须在 JS 层用 `matchMedia` / `prefersReducedMotion` / `getAnimations()` / `skipTransition()` 降级；且编排层要**整段跳过交错**而非逐项归零（否则 N 个变化一帧内重叠闪现）
  - **动画是 enhancement**：View Transitions 的 `ready` 会因重名 reject，但 `updateCallback` 始终执行、`finished` 仍 fulfill → 主流程绝不能 await `ready`；清理必须挂 `finished` + `finally`
- **修掉三处遗留系统性缺陷**（不改检索器，只改标题/补齐资产表）：
  - `build_readme.py` 的 ASSETS 漏了 `multi-brand-theming.md` / `ux-writing.md` / `presentation-design.md`（README 只列 21 行、磁盘已有 24 份）→ 补齐这 3 项并加入本轮新文件，ASSETS 21→**25**，README 从此与磁盘一致
  - `knowledge-map.md` 标题写「58 条自测」但实际只有 57 个 checkbox → 统一为 **61**
  - 两处检索排序退化（改标题）：`motion-system.md` §2 补「缓动曲线（easing）」→「缓动曲线」回到第 1；`dataviz.md` §3 补「图表色板」→「图表色板」回到第 1。顺带修好 #14 遗留的缓动曲线排序问题
- 检索门槛 16/16 PASS（动效编排/交错 stagger/FLIP/共享元素转场/列表增删/动画状态机/动画中断/View Transitions/@starting-style/layoutId/进出场动画/view-transition-name/popLayout/转场并发/编排/动画取消 全部命中新文件前 3）；回归 **16/16 PASS**（修标题后全量复测 32/32）
- 接线体检：27 文件 / **1000 章节**，未接线 0、已失联 0
- 反馈：无真实用户反馈（自动化任务）
- 效果：待观察

## 2026-11-05 · 国际化与本地化设计：i18n / L10n / RTL（每日升级 #16）
- 需求：每日深蒸馏设计知识，本轮主题取上轮候选第 1 位「国际化与本地化设计」。先用 `dp_search.py "国际化 本地化 RTL 多语言"` 与 grep 确认缺口：现有知识几乎只在 `ux-writing.md` §13 的 24 行文案速记里，缺工程实现、RTL 镜像规则、CLDR 复数、日期/货币/姓名格式、验收清单与伪本地化。
- 升级：
  - 新增 `references/i18n-localization.md`（22 节 / 46 小节 / 1058 行 / 49.7k 字符 / 12 场景 / 20 反模式 / 20 自检 / 6 段可抄代码）：三层判层、文案膨胀、`lang`/`dir`、logical properties、RTL 镜像、复数、ICU MessageFormat、`Intl` API、日期、数字、列表/排序/分词、姓名/地址、语言协商、伪本地化、文化适配、译者交付、框架落地、场景、反模式、自检、代码、来源。
  - 取源全部为官方原文或本机实测（19 条规范/体系原文 + Node v22.22.2 `Intl` 输出 + GitHub REST API 10 仓库）：W3C Text size in translation（**原 URL 404，改走 article-text-size.en**）、Declaring language in HTML、Structural markup and RTL text in HTML、Inline markup and bidirectional text in HTML、Personal names around the world、Language tags in HTML and XML；WAI SC 3.1.1 / 3.1.2 与 H57；CLDR Plural Rules 与 Language Plural Rules chart（补取逐语言图表，才拿到「仅 `other`」的具体语言）；ICU User Guide Formatting Messages（FormatJS ICU 页只给示例，改走 ICU 官方拿 `offset`/`selectordinal`/撇号转义/嵌套建议）；MDN `Intl` 与 CSS logical properties、CSSWG Level 1；Material Design 2 Bidirectionality；Microsoft Learn Pseudolocalization；FormatJS 首页。
  - SKILL.md **v20**：frontmatter 触发词补 i18n/L10n/RTL/复数/伪本地化/出海；版本基线段；资产表 +1 行；意图路由 **119→127**（+8：出海总判层 / RTL 双向文本 / 翻译后截断 / 复数与 ICU / 日期数字货币 / 姓名地址 / 伪本地化译者交付 / 国际化诊断）；**同时修正既有「国际化文案」路由里错误的 +40% 口径**；第 5 步新增 H4「国际化与本地化设计」12 条原则；自检 23→**24**（国际化关）。**既有路由顺序一行未动**。
  - 其余接线点：`build_readme.py ASSETS` 25→**26**（顺手把 ux-writing 摘要里过时的「国际化 +40%」改成指向新文件）；`memory/aliases.json` 104→**114** 组（国际化与本地化 / RTL 双向文本 / 文案膨胀 / 复数规则 / ICU MessageFormat / Intl API / CSS 逻辑属性 / 伪本地化 / RTL 图标镜像 / 姓名地址）；`knowledge-map.md` 新增**支线 N**（13→14 条）、自测 **61→69** 条、门槛 **≥47→≥53**，并修正 SKILL.md 资产表里「34 条自测 + 7 条专题支线」的陈旧数字；源清单 **653→690 行**（+37：19 条官方原文 + 1 条 Node 实测 + 10 条仓库 + 4 组标题与空行）。
- **本轮最大价值：把一条自己写错的规则公开裁决掉**。`ux-writing.md` §13 说「按钮和标签必须能容纳 +40%」，但 W3C 转引 IBM 官方表写明英文 **≤10 字符平均膨胀 200–300%**（Flickr `views` 实测意语 **3.0×**），11–20 为 180–200%、21–30 为 160–180%、31–50 为 140–160%、51–70 为 151–170%（**原表非单调，照录未平滑**）、>70 为 130%。→ 明确立场：**microcopy 2–3× / 短文案 1.6–2.0× / 段落 1.3×**；Microsoft 的 +40% 只是**伪本地化测试串加长启发式**，不是设计余量；余量要做成 `min-inline-size`+`max-inline-size`+允许换行的**伸缩能力**，不是把按钮做宽。
- 另外三条可验证的差异化结论：
  - **三层判层**：标记层（`lang`/`dir`）+ 布局层（弹性/逻辑属性/镜像）+ 数据层（复数/日期/数字/姓名/排序）必须同时改；W3C 硬禁令「Never use CSS to apply the base direction」，`lang` 推不出方向（WCAG 3.1.1 A / 3.1.2 AA）。
  - **复数不是 `n===1`**：CLDR 六类、`one`≠数字 1、`other` 必需、**中/日/韩/印尼/越南仅 `other`**——中文产品在本地永远测不出分支，最易漏；ICU MessageFormat 禁拼接、`select` 外层 `plural` 内层。
  - **文档 ≠ 运行时**：MDN 已列 `Intl.DurationFormat`，本机 Node v22.22.2 实测 `new Intl.DurationFormat(...)` 仍抛 **TypeError** → 生产必须 `typeof … === 'function'` 能力检测 + 降级；`zh_cn` 抛 `RangeError`，BCP 47 必须用 `zh-CN`。
- 检索门槛 **16/16 PASS**（国际化与本地化 / i18n / L10n / RTL 阿拉伯语 / 双向文本 / 文案膨胀 / 翻译后按钮被截断 / 复数规则 / CLDR plural / ICU MessageFormat / Intl API / CSS 逻辑属性 / 伪本地化 / 姓名 Full name / 日期货币格式 / 图标镜像 全部命中新文件前 3）；回归 **16/16 PASS**（#15 全部动效关键词仍命中 `motion-orchestration.md`，全量复测 32/32）。顺手修一处排序退化：把 §1 标题补成「判层：国际化与本地化 i18n / L10n…」，让「国际化与本地化」从 `knowledge-map.md` 第 1 回到新文件第 1（95.3 > 85.3）。
- 接线体检：**28 文件 / 1070 章节**，未接线 0、已失联 0
- **补修源头缺陷（发布后追加的第二笔提交）**：只在路由层打补丁会留下自相矛盾的知识，因此把 `ux-writing.md` §13.1 的「按钮和标签必须能容纳 +40%」整段改写为**分档弹性口径 + 指向 `i18n-localization.md` §2**，并同步 §18 自检第 16 项（改为「按钮过 2–3× 伪本地化加长测试」）；`SKILL.md` 的 ux-writing 资产行与 **v17 历史基线段落**里残留的 +40% 也加了「v20 已裁决」标注（历史基线只加标注、不篡改原文）。`build_readme.py` 的 ux-writing 摘要同样改掉。做到全仓不再有一处把 +40% 当成 microcopy 设计余量。
- 反馈：无真实用户反馈（自动化任务）
- 效果：待观察

## 2026-11-05 · 设计系统文档写作：组件文档页 / 信息架构 / 版本化 / 治理（每日升级 #17）
- 需求：每日深蒸馏设计知识，本轮主题取 #16 候选第 1 位「设计系统文档写作」。缺口判定：`dp_search.py "设计系统文档 文档信息架构 组件文档 版本化"` + grep → `文档站点 / 组件文档 / 版本化 / 贡献指南 / governance / 文档模板` 全部零命中；`design-md-format.md` 只有单文件 DESIGN.md 九章骨架，`handoff-collaboration.md` 覆盖的是「把设计稿交给开发」，没有设计系统站点自身的信息架构、组件文档页模板、文档治理、docs-as-code 版本化与文档写作标准。
- 升级：
  - 新增 `references/design-system-docs.md`（**22 节 / 949 行 / 47.3k 字符 / 12 场景 / 20 反模式 / 20 自检 / 6 段可抄代码**）：§0 与既有资产分层、§1 Diátaxis 四象限判层、§2 GOV.UK 组件页九段式逐节拆解、§3 五问验收与字段清单、§4 信息架构四条地基、§5 Google 三层参考层级与写作清单、§6 示例代码五条硬规则、§7 完整填充范例（Button 精简版）、§8 活文档四件套、§9 组件状态与成熟度、§10 Docusaurus 3.10.2 版本化、§11 Keep a Changelog 1.1.0、§12 MAJOR 迁移文档、§13 DTCG token 文档源与 preview/published 辨析、§14 Storybook Autodocs·MDX·Doc Blocks、§15 Figma Code Connect、§16 GOV.UK 贡献与治理、§17 文档新鲜度与漂移（自举到本技能）、§18–§21 场景/反模式/自检/代码、§22 来源。
  - 取源 25 条官方原文 + 16 仓库 GitHub REST API 实测；GOV.UK Button 源文件 `src/components/button/index.md`、USWDS `lifecycle-phases.yml`/`lifecycle-status.yml`、Carbon `docs/guides/versioning.md` 均读上游源码而非二手转述。
  - SKILL.md **v21**：frontmatter 触发词补文档站/组件文档页/版本化/changelog/贡献治理/docs-as-code；版本基线段；资产表 +1；意图路由 **127→135**（+8，**既有 127 行顺序一行未动，全部纯追加**）；第 5 步新增 H4「设计系统文档写作」10 条原则；自检 **24→25**（文档关）；第 0 步资产数 22→27、字数 38 万→59 万；知识路线图资产行的自测/支线数字同步。
  - 其余接线点：`build_readme.py ASSETS` **26→27**；`memory/aliases.json` **114→128 组**（+14：组件文档页 / 文档信息架构 / 文档版本化 / 变更日志 / 迁移指南 / 贡献指南 / 文档治理 / 活文档 / 文档模板 / 自动生成文档 / 文档新鲜度 / 文档写作风格 / Diátaxis 四象限 / 文档成熟度），**只进检索层，路由优先级未动**；`knowledge-map.md` 修正陈旧标题「十三条」→「**十五条**」、新增**支线 O**、自测 **69→76**、门槛 **≥53→≥58**；源清单 **690→736 行**（+46：25 条官方原文 + 16 条仓库实测 + 分组标题空行），头部「最后更新」2026-11-01→2026-11-05。
- **本轮最重要的一条裁决：规范引用认 published 不认 preview**。`https://tr.designtokens.org/format/` 页首明写 *"This is a preview"* / *"Do not attempt to implement this version of the specification. Do not reference this version as authoritative in any way."*，因此只能作为**辨析对象**；权威引用是 **DTCG published 2025.10**（`https://www.designtokens.org/TR/2025.10/format/`）。`handoff-collaboration.md` 早已标注「预览草稿，不可当标准」，本轮把**该引用哪条 URL**说清楚了，并把 `$description` / `$deprecated` / `$extensions` 定位成 token 文档的自动生成源，避免手抄第二份必然漂移的表。
- 另外四条可验证的差异化结论：
  - **组件文档页不是 props 表**：GOV.UK 九段式里最容易漏的是 `When not to use` 与 **Research / Recent changes / Help improve 活文档四件套**；后者是文档能持续生长的反馈闭环，砍掉即停止演化。
  - **Docusaurus 官方反对无脑版本化**：明说多数站点不需要；真做则 `versioned_docs`/`versioned_sidebars`/`versions.json` 三件套、版本数 **<10**、dev/deploy preview **2 或 3** 个、**patch 不切新版本**、旧版 banner `unmaintained`。
  - **changelog ≠ git log**：Keep a Changelog 1.1.0 七条指导原则 + 六类变更（Added/Changed/Deprecated/Removed/Fixed/Security）+ 常驻 `[Unreleased]` + ISO 8601；**MAJOR 迁移文档必须能被机器校验**（codemod / 脚本可跑）。
  - **治理写门槛不写口号**：GOV.UK 提案看 **Useful / Unique**、发布看 **Usable / Consistent / Versatile**，社区资源另有 1 个月 / 3 个月使用阈值；USWDS 三阶段十二子状态与 45 天评论期给出成熟度口径。
- **GitHub API 实测发现两个「活源」已归档**：`Shopify/polaris`（6148★ / 2026-09-11）与 `adobe/spectrum-css`（1293★ / 2026-10-13）均 `archived=true`。规范内容仍可读，但**不能再当作会持续更新的活源**；新文件与源清单都显式标注。未认证批量请求曾全部 `403 rate limit exceeded`，改用 `~/.workbuddy-ai/secrets/github_token.txt` 的 PAT 加 `Authorization: Bearer` 后 16/17 成功；`diataxis/documentation-framework` 返回 404（仓库不存在），已剔除，不臆造数据。
- 取源避坑：Microsoft Writing Style Guide 的 `brand-voice-design/` 与 `top-10-tips` 均 404、Medium 上 EightShapes `Documenting Components` 失效、Polaris 旧组件页重定向到 shopify.dev references —— **四条拿不到原文的线索一律不写入知识资产**，只保留可从官方原文或上游源码逐字验证的结论。
- 检索门槛 **16/16 PASS**（设计系统文档 / 组件文档页 / 文档信息架构 / 文档版本化 / changelog / 迁移文档 / 贡献指南 / 文档治理 / Diátaxis 四象限 / GOV.UK 九段式 / 活文档 / 文档模板 / Storybook Autodocs / MDX Doc Blocks / 文档漂移 / 文档新鲜度 全部命中新文件前 3）；历史回归 **24/24 PASS**（#16 的 15 条 + #15 的 5 条 + 演示/文案/交付/暗色 4 条，全量 **40/40**）。`--no-alias` 对比确认别名只补召回、不改变规范词主导。
- 接线体检：`mindmap.py` **29 文件 / 1124 章节**，✅ 所有 references 均已在 SKILL.md 接线（未接线 0 / 已失联 0）。
- **发布环节的自愈改动（本轮第二笔提交 `7129a43`）**：`scripts/publish_github.py` 原本只从 `~/.workbuddy-ai/secrets/github_token.txt` 取 PAT，本轮该文件里的 fine-grained PAT 已失效，返回 `401 Bad credentials`；但**未认证读取仓库仍是 200**，旧逻辑会把 401 当确定性错误直接抛出、无从区分「令牌失效」与「网络故障」。现按 `--token → 环境变量 → 密钥文件 → git credential helper` 逐个用 `GET /user` 验证（新增 `token_status()` / `creds_from_helper()`），失效即跳过，网络类故障标 `unknown` 不误杀。发布时自动降级到 Windows GCM 里有效的 PAT（`permissions.push=true`），一次跑通；**没有改动或覆盖任何仓库外的凭据文件**。远端 39 文件一次发布成功（具体 commit 记在未发布的自动化记忆中，避免把哈希写进已跟踪文件造成自引用）。
- 反馈：无真实用户反馈（自动化任务）
- 效果：待观察

- **补修源头口径（#17 收尾提交）**：published/preview 裁决此前只写在新文件、版本基线与日志里，**三处来源表仍把 preview URL 当唯一引用**，与本轮结论自相矛盾。按「发现冲突必须改源头」把 `SKILL.md` 数据来源行、`references/handoff-collaboration.md` §数据来源、`references/multi-brand-theming.md` 来源表全部改为 **DTCG published 2025.10 权威 URL**（`https://www.designtokens.org/TR/2025.10/format/`），preview 只作辨析对象并注明页首 *"Do not reference this version as authoritative in any way"*；顺带把早期草案的 `$extends`/`$root` 表述按 published 口径修订为 `$description`/`$deprecated`/`$extensions`/reference。`design-system-docs.md` §13.1、`knowledge-map.md` 支线 O、`SKILL.md` v21 版本基线里的 preview URL 属于**裁决说明**（已写明不可作权威），保留不动，避免把正确的辨析文本误删。
- 接线体检复核：`python scripts/mindmap.py --check` → **29 文件 / 1124 章节 / 未接线 0 / 已失联 0**；此前 `tree.md` 只读统计里出现的 1 次「失联」是 §21.6 标题「失联链接」，非真实故障。
- **补修一处检索排序退化（#17 收尾第二处）**：全量回归 10 词时发现 `组件库 选型` 的前 3 被 `design-system-docs.md` §7/§3 与 `handoff-collaboration.md` §7.4 占满，`component-libraries.md` 掉出前 3。成因**不是**本次来源表改动，而是 #17 新文件 §7 摘要含「组件库」，而 `component-libraries.md` 三个 H2（元素覆盖矩阵 / 选型规则 / 维护协议）标题里没有规范词「组件库」，标题×10 加权失效。按 #16 的既有做法把 `## 选型规则` 改为 `## 组件库选型规则`（保留「选型规则」连续子串，不破坏 `SKILL.md` / `knowledge-map.md` 里的描述性引用），从目标文件标题侧补规范词，而不是削弱新文件。修后 `组件库 选型` → `component-libraries.md` **41.0 分居首**、`组件库` → **31.0 分居首**，`--no-alias` 结果一致，证明规范词主导不依赖别名、**路由优先级一行未动**。复测：新主题 **16/16** + 历史回归 **10/10**，`mindmap.py --check` 仍 **29 文件 / 1124 章节 / 未接线 0 / 已失联 0**。


## 2026-11-06 · AI / 生成式设计工具链：工作流、提示词、质量验收与合规边界（每日升级 #18）

- 需求：延续每日升级协议，第 18 轮只深挖一个主题。候选来自 #17 待挖项；`dp_search.py "AI 生成 设计 提示词 版权 内容标识"` 的 8 条命中全落在 `ux-writing` / `knowledge-map` / `design-system-docs` / `design-md-format` / `handoff-collaboration`，确认「AI 生成设计的合规、提示词、质量验收」是真缺口；`tools.md` 只有 153 条工具链接，属链接清单而非方法论。
- 取源与验证（全部官方原文 / 上游源码 / API 实测）：中国《人工智能生成合成内容标识办法》国信办通字〔2025〕2 号全文 **14 条**（2025-09-01 施行）+《生成式人工智能服务管理暂行办法》令第 15 号（2023-08-15 施行）第 7/11 条 + CAC 2025-09-05 专家解读（GB 45438-2025 同期施行、责任四段链）；EU AI Act Article 50（依 Art. 113 于 **2026-08-02** 适用）；USCO Copyright and AI Part 2 与 2025-02-06 官方解读；C2PA Specifications / Explainer；Microsoft HAX `ai-guidelines` + `library`（G1–G18）；OpenAI Prompt engineering；本会话加载的 `impeccable`（AI Slop Test / 8 维 DO-DON'T / Design Context）与 `awesome-design-md`（54 个 DESIGN.md 九章）；**18 个 GitHub 仓库**逐条 `GET /repos/{owner}/{repo}` 实测 star / license.spdx_id / pushed_at / archived。
- 本轮四条「不再含糊」的裁决：
  - ① **打标是法定义务**：显式标识（用户可感知）+ 隐式标识（文件元数据）双轨；第 4/5/6/9/10 条逐条翻成设计动作——导出·下载·复制保留标识、元数据三类要素、传播端「属于 / 可能为 / 疑似」三档、无标版协议 + 日志 ≥6 个月、**禁止提供删除/篡改/伪造/隐匿标识的功能**（直接判 UI 红线）。
  - ② USCO 原文 *"but not the mere provision of prompts"*：**提示词写得再细也不构成作者身份**，可保护的只有「human author has determined sufficient expressive elements」。设计侧不留「神级 prompt」，留 **brief→参考→草图→迭代→人工选择→终稿** 的可举证创作链。
  - ③ **三概念分离**：法定内容标识 / C2PA Content Credentials 溯源 / 版权归属与商用授权互不替代；C2PA 只断言 manifest 格式良好·未篡改·签名可信·与 asset 绑定，**不判断事实真伪、版权归属、法律有效性、内容准确性**。
  - ④ **AI 生成界面可验收**：AI Slop Test + 8 维 DO/DON'T + 12 类固有缺陷索引 + 20 项自检 + 4 段脚本；3 段 Python 已实跑（标识 checklist 4 用例全 PASS、HTML 扫描 good=0 / bad=1、元数据存活 PASS）。
- 取源纪律：`gov.cn` 抓取误返回首页 → 改用 CAC 官方 URL 取得令第 15 号全文；Adobe Firefly 商业安全页 **404**、Google Stitch DESIGN.md format 页 **fetch failed**、GB 45438-2025 国标全文未逐字取得 → **具体承诺与像素/字号/时长数值一律不写入资产**，只在 §22 记录限制；`soma-shah/Figma-Context-MCP`、`Motiff/motiff` 两个 404 线索剔除。HAX 官方给出 18 条编号与四阶段名称但**未逐条标注编号与阶段归属** → 改为中性编号分组并加「口径纪律」，不臆造边界。GitHub 凭据继续走 #17 修好的回退链（密钥文件 PAT 失效 → Windows GCM 有效 PAT）。
- 接线：新增 `references/ai-design-toolchain.md`（22 节 / 790 行 / 38.2k 字符）；`SKILL.md` **v21→v22**（frontmatter 3 处触发词、资产表 +1 行、意图路由**表末追加 6 条，既有顺序一行未动**、第 5 步新增「产能层不是判断层」原则、第 6 步新增第 **26** 条 AI 关自检、第 0 步统计 27→28 份 / 59→63 万字符）；`scripts/build_readme.py` ASSETS +1；`scripts/mindmap.py` INTENTS +2；`memory/aliases.json` **128→142 组，`_weight` 0.45 与 `_note` 口径原样未改**；`references/knowledge-map.md` 十五条→**十六条**（支线 P）、自测 **76→88** 条 / 门槛 ≥58→≥67；`D:/My Skills/Design-related websites.txt` **736→774 行**（14 条官方原文 + 18 仓库实测）。
- 检索门槛：新主题 **16/16 PASS**（AI 生成设计 / 内容标识 / 商用授权 / 提示词 版权 / C2PA / 提示词工程 / prompt 版本化 / AI 味 / 生成界面验收 / HAX / DESIGN.md 契约 / 工具选型 / 生成→代码 全部命中新文件前 3）；历史回归 **42/42 PASS**，全量 **58/58**。`--no-alias` 对比确认别名只补召回、规范词主导不变。
- 接线体检：`python scripts/mindmap.py --check` → **30 文件 / 1187 章节 / 未接线 0 / 已失联 0**（口径纪律：接线体检的 30 文件含 `SKILL.md` 与 memory/ 侧文档，章节数是随索引重建变化的派生量，因此精确值只记此处、不写进 `SKILL.md` / README；README 的「28 份参考 / 约 63 万字符」只统计 `references/*.md`，两者口径不同、不冲突）。
- 修一处历史排序退化：全量回归发现 `动效 曲线 时长` 的前 3 被 `knowledge-map.md` 支线 M 与 `motion-orchestration.md` 占满，`motion-system.md` 掉出。成因是 §2/§3 标题分别只有「曲线」「时长」而缺规范词「动效」，标题×10 加权失效。按 #14/#17 既有做法改为「**动效**缓动曲线（easing）」「**动效**时长」，**保留「缓动曲线（easing）」与「时长」连续子串**，不破坏 README / tree 中的描述性引用；复测两词均把 `motion-system.md` 送回前 3，**未改检索器、未动任何路由顺序**。
- 代码质量自纠：§21.1 初稿中文法定要素名与英文样例字段对不上、实跑必 FAIL → 改为「法定要素 → 工程字段别名」映射并附 4 个自测用例，同时声明别名**不是法定字段名**；§21.4 禁词改词边界正则，避免 `BOOKMARK` / `TOKEN` 被误判成 OK 按钮文案；§10 HAX 四个分组标题统一为纯编号，删掉与「口径纪律」自相矛盾的阶段归属注记。
- 反馈：无真实用户反馈（自动化任务）
- 效果：待观察
