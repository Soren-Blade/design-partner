# 记忆树 · Knowledge Tree

> 自动生成于 2026-11-11 23:12 ｜ 45 个文件 · 1738 个章节 · 1,490,752 字符
> 由 `scripts/mindmap.py` 重建，**不要手改**（手改会被下次覆盖；要改就改源文件或脚本）。

## 怎么用（三条命令）

```bash
python scripts/dp_search.py "缓动曲线"      # 关键词检索：命中章节 + 行号 + 摘要
python scripts/dp_search.py --topic          # 列出所有主题（章节标题一览）
python scripts/mindmap.py                    # 资产变更后重建本树与 index.json
```

**检索纪律**：先用 `dp_search` 定位到「文件 §章节」，再只读那一段。不要整份读 references——十几份文件全读一遍会吃掉大量上下文，而命中往往只在一节。

## 一、意图 → 位置（快捷路由）

| 用户这么说 | 去哪儿 |
|---|---|
| 从零做视觉 | 第 5 步原则 + patterns.md 取构型 + design-tokens.md 取数值 |
| 改进现有设计 | 按第 5 步逐条诊断；动效问题查 motion-system.md §10 验收清单 |
| 要灵感 / 参考 | patterns.md（元素级）→ inspiration.md（风格级）→ portfolios.md（校准） |
| 要设计规范 / 系统 | design-tokens.md（三层 token）→ design-md-format.md（九章骨架） |
| 对标某品牌 | design-md-format.md §3 品牌 DNA + design-tokens.md 取精确值 |
| 中文项目 | chinese-design.md（排版/生态）→ motion-system.md §9（小程序） |
| 动效 / 微交互 / 动画 | motion-system.md：§2 曲线 · §3 时长 · §4 场景表 · §7 代码 · §10 验收 |
| 滚动动画 / 页面转场 | motion-system.md §7.3 View Transitions · §7.4 scroll-driven |
| 无障碍 / reduced-motion | motion-system.md §8.1 三档降级 |
| 提示 / toast / 弹窗 / 确认 | feedback-states.md：§1 层级决策 · §3 toast 数值 · §7 确认与破坏性操作 |
| 加载 / 骨架屏 / 进度 | feedback-states.md：§2 时间阈值 · §4 加载与进度 · §14.2 骨架代码 |
| 空状态 / 无数据 / 失败空 | feedback-states.md §5（五种空 + 五件套结构 + 文案公式） |
| 错误页 / 报错文案 / 重试 | feedback-states.md §6（五级错误 + 404/500 规则 + 三段式文案） |
| 找工具 / 资产 | tools.md（工具）· resources.md（图标/字体/3D）· component-libraries.md（代码） |
| 想提升自己 / 学习路径 | knowledge-map.md L0→L4 + 20 条自测 |
| AI 生成设计 / AIGC 工作流 | ai-design-toolchain.md §1 五层人工闸门 · §9 八步工作流 · §13 选型三问 |
| AI 内容标识 / 合规 / 版权 / 提示词 / AI 味验收 | ai-design-toolchain.md §2 标识 · §4 USCO 裁决 · §8 提示词 · §11 AI Slop Test · §20 自检 |
| 设计伦理 / 欺骗性设计 / 隐私同意 / 自动续费 / 一键关闭 | design-ethics-inclusion.md §1 三条立场 · §2 现行 18 类 · §4 对称选择 · §8 一键关闭 · §9 反陈旧裁决 · §21 脚本 |
| 包容性设计 / 认知无障碍 / 未成年人 / 成瘾设计 | design-ethics-inclusion.md §11 令第 766 号 · §12 成瘾四红线 · §14 三原则 · §15 七原则 · §16 COGA 八目标 · §17 四象限 |
| 组件 API / props 契约 / 受控非受控 / 组合 / 插槽 / asChild / 换元素 | component-api-design.md §1 三份所有权 · §2 受控契约 · §5 五种换元素 API · §7 合并优先级 · §8 compound components |
| ref 转发 / React 19 forwardRef / 复合组件键盘 / roving tabindex / 组件发版 SemVer / argTypes | component-api-design.md §9 反陈旧裁决 · §12 APG 键盘契约 · §14 API SemVer 六冻结面 · §15 Storybook argTypes · §20 脚本 |
| 设计度量 / 用户研究 / 可用性测试 / SUS / 样本量 / HEART / A-B 测试 | design-measurement-research.md §0 分层导语 · §1 度量三步法 · §3 任务级指标 · §4 SUS/UMUX · §5 问卷量表 · §7 样本量 · §11 A/B 统计 |
| 满意度怎么量化 / 改版有没有效 / 要不要上线 A-B / 该做多少人的研究 | design-measurement-research.md §21 四段可抄代码（问题暴露率·比例样本量·SUS 计分·A/B z 检验）· §23 接线与其他资产 |
| 导航 / 导航栏 / 菜单 / 信息架构 | navigation-ia.md §1 四类职责 → §2 形态决策 → §3 项数铁律 → §7 移动端降级 |
| 信息架构 / 网站结构 / 菜单组织 | navigation-ia.md §4（深度 vs 广度 / 3-click 迷思 / 信息气味 / 卡片分类·树测试） |
| 面包屑 / 当前位置 | navigation-ia.md §5（位置型/属性型/路径型 + 末级非链接 + aria-current） |
| 标签页 Tabs | navigation-ia.md §6（APG tabs 键盘契约 + tabpanel + 何时用 tabs vs 侧栏） |
| 底部 Tab / 移动端导航 / 汉堡 | navigation-ia.md §7（Apple ≤5 项 / Material bar·rail·drawer / NN/g 可发现性）+ responsive-layout §9 降级路径 |
| 当前位置指示 / 激活态 / you are here | navigation-ia.md §8（≥2 信号 + aria-current + 聚焦态独立） |
| 导航可访问性 / skip link / 地标 | navigation-ia.md §9（2.4.1 skip link / 1.3.1 landmark / 2.4.5 multiple ways / 2.4.7 焦点）+ accessibility §3 |
| 搜索与导航 | navigation-ia.md §10（搜索是导航备份 + 占位符写示例 + 零结果三件套） |
| 设计评审 / critique / 设计走查 | references/design-critique.md §1 两种评审分清 + §2 三前提 + §5 RACI/远程异步 |
| 给反馈 / 反馈话术 / I like I wish I wonder / 2 正 1 改 | references/design-critique.md §3 给反馈七铁律 |
| 接收反馈 / 怎么不辩护 / 别人挑刺怎么应对 | references/design-critique.md §4 接收反馈四步 |
| 设计 by committee / HiPPO / 谁说了算 / 委员会改稿 | references/design-critique.md §5 Decider + §7 反模式 |
| 决策留痕 / ADR / 评审结论去哪了 | references/design-critique.md §8 ADR / critique notes 模板 |
| 评判框架 / 严重度 0–4 / NN/g 10 启发式 | references/design-critique.md §6 评判框架 |
| 视觉风格 / 风格匹配 / 做成 XX 那种感觉 / 高级感 / 视觉调性 | references/visual-style-taxonomy.md §2 四维信号 → §4 匹配决策（参考站四步 / 形容词先确认语境） |
| 风格谱系 / 设计运动 / 玻璃拟态 / 新拟态 / 野兽派 / Y2K / Bento | references/visual-style-taxonomy.md §3 编年谱系 + §5 混搭纪律 + §6 趋势生命周期 |
| 风格诊断 / 风格不一致 / 潮流该不该跟 | references/visual-style-taxonomy.md §10 反模式 20 条 + §11 自检 20 项 + §6 生命周期 |
| 字体排印 / 字号 / 行高 / 行距 / 定一套字体系统 / 排版很挤 | references/typography-system.md §2 六层模型判层 → §4 rem 阶梯（px 不可访问）→ §5 行高两档与行长 → §17 M3 五角色×三尺寸落 token |
| 文本间距 / WCAG 1.4.12 / 200% 缩放 / 放大就裁切 / 表单 label 重叠 / 可访问性验收 | references/typography-system.md §6 三关硬数值 + §7 注入验收五步（§23.3 书签）+ §8 两种缩放与容器弹性 + §23.5 静态扫描 |
| 中文排版 / 中英混排 / 缺字 tofu / 字体回退 / 全角半角 / 字素丛 | references/typography-system.md §16 W3C clreq（1/4 汉字宽·1:1 正方形·全角 ASCII·UAX #29）+ §12 逐字符回退 + §13 unicode-range 分片 |
| 数字抖动 / tabular-nums / 可变字体 / 字体加载闪烁 / CLS / 字体商用授权 | references/typography-system.md §10 OpenType 数字特性 + §9 五注册轴 + §14 font-display 五档 + §15 size-adjust + §18 OFL 1.1 五条件 + §19 仓库实测 |
| 不确定知识在哪 | python scripts/dp_search.py "关键词" |
| 圆角 / 形状 / 半径 | shape-elevation.md §10 语法 · §11 corner overlap · §12 同心 r=R−p · §13 七体系精确值 |
| 阴影 / 投影 / 三层阴影 | shape-elevation.md §7 box-shadow 语法 · §8 七体系对照 · §9 物理分解 · §23.1 token |
| 高度层级 / elevation / 表面浮起 | shape-elevation.md §3 语义裁决 · §4 六级 dp · §15 Carbon Layering · §19 深度语言 |
| 边界看不见 / 阴影当 3:1 | shape-elevation.md §5 实跑对比度 · §6 非文本 3:1 正确落点 · accessibility.md §2 |
| 材质 / 毛玻璃 / z-index | shape-elevation.md §16 Apple Materials · §17 性能红线 · §18 语义 z-index · §23.6 渐进增强 |
| 格式塔 / 完形 / 组织律 / 邻近性 / 分组 | visual-hierarchy-gestalt.md §7 IxDF 12 条全表 · §8 可验收四规则 · §9 前注意 pop-out |
| 视觉层级 / 重点不突出 / 主次不清 / 眯眼测试 / 单焦点 | visual-hierarchy-gestalt.md §2 三层模型判层 · §3 F 型非目标 · §10 图形背景与多稳态 · §15 Von Restorff |
| 眼动 / F 型 / 扫描模式 / RTL 动线 / 用户只看标题 | visual-hierarchy-gestalt.md §3 NN/g 逐字裁决 · §4 八种扫描模式诊断表 · §6 RTL 与断点复核 |
| 认知负荷 / 7±2 / 选项太多 / 希克定律 / 菲茨定律 / 组块 | visual-hierarchy-gestalt.md §11 三分与 7±2 误用 · §12 Hick 公式与失效条件 · §13 Fitts 三形式 · §14 chunking |
| DOM 顺序 / 焦点顺序 / 标题结构 / tabindex / 三顺序一致性 | visual-hierarchy-gestalt.md §5 四条 WCAG 准则逐字原文 · §6 一致性验收 · §23.2 静态扫描器 · §23.5 C27 正例 |
| 内容找不到 / 搜不到 / 可发现性 / 多路径 / 站点地图 | content-findability.md §2 四层链路判层 → §3 SC 2.4.5 至少两条路 → §4 搜索入口 → §19 位置感清单 |
| 链接文案 / Learn More / 信息气味 / 前 11 个字符 | content-findability.md §10 SC 2.4.4 A · 2.4.9 AAA · 3.2.4 AA → §9 信息气味 → §12 nano-content → §13 三种改法 → §26.2 扫描器 |
| 可扫读 / 阅读等级 / 简明语言 / Flesch / 中文 | content-findability.md §11 NN/g 79%/16% → §14 SC 3.1.5 九年门槛 → §15 三公式不可换算 → §16 中文代理指标 → §17 Plain Writing Act → §26.1 计算器 |
| 零结果 / 404 / 自动补全 combobox / placeholder 不是 label | content-findability.md §5 SC 3.3.2 → §6 APG combobox 契约 → §18 零结果与 GOV.UK 404 四条禁令 → §26.3 契约检查器 |
| 树测试 / findability / directness / 卡片分类 | content-findability.md §20 度量口径（定性结果不可冒充百分比）→ §21 六步构建流程 |
| 拖拽 / 拖放 / 列表重排 / 排序 / 直接操纵 | direct-manipulation.md §2 四段链路判层 → §3 SC 2.5.7 单指针无拖动 → §4 G219 四类替代 → §7 完整状态机 |
| 指针事件 / pointercancel / setPointerCapture / touch-action | direct-manipulation.md §9 PE3 规范性抑制链 → §10 MDN 工程契约 → §11 touch-action 全值表 → §12 HTML DnD 七事件 |
| 拖动无障碍 / 键盘拖放 / 读屏播报 / Escape 取消 | direct-manipulation.md §5 SC 2.5.1 交叉约束 → §6 SC 2.5.2 与 G210 → §13 dnd-kit 键盘默认 → §14 live region |
| 目标尺寸 / 点击区 / 触控目标 / 24×24 / 44×44 / 48dp | direct-manipulation.md §8 三口径裁决表 → §17 阈值与时序决策表 → §25.1 目标尺寸判定器 |
| 手势 / 路径手势 / 长按 / 触屏拖动 / 磁吸 | direct-manipulation.md §5 SC 2.5.1 路径手势 → §15 NN/g signifier → §16 1cm×1cm 与约 100ms → §19 替代路径矩阵 → §20 库生态选型 |
| 对话式界面 / 聊天 UI / chatbot / 流式输出 / 打字机效果 | conversational-generative-ui.md §2 五段链路判层 → §3 SC 4.1.3 裁决一 → §4 ARIA23 role=log → §5 live region 契约 → §12 状态边界播报一次 |
| 生成式界面 / GenUI / streamUI / 组件白名单 / 动态组件 | conversational-generative-ui.md §6 裁决二 → §7 RSC experimental 与生产路径 → §8 message.parts → §20 代码 4 白名单分派 |
| 对话状态机 / useChat / message.parts / AG-UI 事件 | conversational-generative-ui.md §8 四态逐字 → §9 AG-UI 三模式与生命周期边界 → §13 状态归位表 → §20 代码 1 事件流校验器 |
| AI 答错了 / 停止生成 / 重新生成 / 纠错 / 撤销自动化动作 | 先读 conversational-generative-ui.md §11 HAX G9 四档恢复链 → §12 → §13；HAX 原则层 18 条归 ai-design-toolchain.md §10 |
| 混合界面 / Hybrid UI / RICH 范式 / 读屏刷屏 / aria-busy | conversational-generative-ui.md §10 RICH 四要素与 WIMP 判型 → §5 aria-busy 三出口 → §16 来源与引用 → §17 场景 7/8 |
| 模态判型 / 焦点陷阱 / inert / aria-modal / 四问判型 | overlays-modality.md §1 四问判型 → §3 APG 焦点契约 → §4 aria-modal 双条件 → §20.1 判型器 |
| 原生 dialog / showModal / closedby / ::backdrop / returnValue | overlays-modality.md §5 showModal 与 top layer → §7 ::backdrop 与 z-index 分界 → §13 关闭契约 → §20.4 原生骨架 |
| Popover API / popover 三态 / auto hint manual / 顶层栈 | overlays-modality.md §6 always non-modal 与双栈六规则 → §7 top layer → §14 层叠嵌套 → §15 组件族谱 |
| hover 浮层 / tooltip / SC 1.4.13 / Dismissible Hoverable Persistent | overlays-modality.md §9 三条件 → §12 SC 3.2.1 help dialog 失败例 → §20.2 校验器 |
| 浮层遮挡 / SC 2.4.11 / F110 / C43 / 退出契约 | overlays-modality.md §10 modal always pass 与 Note 2 三出路 → §11 SC 2.1.2 → §13 关闭契约 → §20.3 遮挡裁决器 |

## 一·B、别名映射（检索层，不改路由优先级）

> 用户在说法上不会统一：说「弹窗」还是 dialog、说「转圈」还是 loading。`memory/aliases.json` 把这些说法归到同一个规范词，`dp_search.py` 检索时以 **0.45 权重**追加召回——**只影响召回，不影响上表的意图路由顺序**。

| 规范词 | 别名 / 俗称 / 中英对应 |
|---|---|
| **轻提示** | toast · message · snackbar · 提示条 · 消息提示 · 浮层提示 · 冒泡 · 轻提示 |
| **模态** | modal · dialog · 弹窗 · 对话框 · 模态框 · 遮罩 · popconfirm · 确认框 · 气泡确认 |
| **加载** | loading · 加载中 · 骨架屏 · skeleton · spinner · 进度条 · progress · 转圈 · 等待状态 · 占位 |
| **空态** | empty · 空状态 · 无数据 · 空页面 · 没有内容 · empty state |
| **错误** | error · 报错 · 异常 · 失败提示 · 错误页 · 404 · 500 · 503 · 服务不可用 · 出错 |
| **动效** | motion · animation · 动画 · 微交互 · 过渡 · transition · easing · 缓动 · 曲线 · 转场 |
| **配色** | color · 色彩 · 色板 · palette · 主题色 · 主色 · 颜色 |
| **排版** | typography · 字体 · font · 字号 · 行高 · 字重 · 字阶 · 文本层级 |
| **间距** | spacing · 留白 · padding · margin · grid · 节奏 · 8pt · 4px |
| **token** | design token · 设计变量 · 变量 · 语义化 · tokens · 主题变量 |
| **图表** | chart · 可视化 · dataviz · 仪表盘 · dashboard · 大屏 · BI · KPI · 折线图 · 柱状图 · 饼图 · 看板 |
| **表单** | form · 输入框 · 校验 · 验证 · 报错文案 · 登录页 · 注册 · 填写 · 字段 |
| **表格** | table · 列表页 · 数据表 · 分页 · 列宽 · 行高 · 批量操作 · 筛选 |
| **无障碍** | a11y · accessibility · 可访问性 · 读屏 · 屏幕阅读器 · 焦点 · 对比度 · 键盘操作 · 色盲 · 适老化 · WCAG |
| **按钮** | button · CTA · 主按钮 · 次按钮 · 操作按钮 · 提交按钮 |
| **导航** | navbar · 导航栏 · 顶栏 · 菜单 · 侧边栏 · tab bar · 底部导航 · 面包屑 |
| **卡片** | card · 卡片布局 · 容器 · 信息块 · tile |
| **中文** | chinese · 汉字 · 中文字体 · 标点 · 全角 · 避头尾 · 中英混排 · clreq |
| **品牌** | brand · 品牌视觉 · logo · 视觉识别 · VI · 品牌调性 |
| **响应式** | responsive · 断点 · breakpoint · 移动端 · 适配 · 自适应 · 容器查询 |
| **断点** | breakpoint · 媒体查询 · media query · @media · 屏宽 · 视口宽 · viewport · 最小宽度 · min-width · max-width · 响应式断点 · 栅格断点 |
| **容器查询** | container query · @container · container-type · cqw · cqi · 组件自适应 · 按容器宽度 · 卡片自适应 |
| **版心** | container · 最大宽度 · max-width · 内容区宽度 · 栅格系统 · grid system · 24栅格 · 12栅格 · gutter · 槽宽 · column · 栏宽 |
| **流式排版** | clamp · fluid type · 流体排版 · 自适应字号 · 字号缩放 · 响应式字号 · min() · max() · 字号随屏幕变 |
| **视口单位** | vh · vw · 100vh · dvh · svh · lvh · 全屏高度 · 地址栏遮挡 · safe-area · 安全区 · 刘海屏 · 满屏 |
| **响应式图片** | srcset · sizes · picture · 图片适配 · 多倍图 · 2x图 · 懒加载 · lazy · 图片跳动 · CLS · 艺术指导 |
| **多端适配** | 多端 · H5 · 手机端 · PC端 · 平板 · iPad · 折叠屏 · 大屏 · 小屏 · 窄屏 · 中后台适配 · 1366 · 1440 · 1920 |
| **窄屏表格** | 移动端表格 · 手机表格 · 表格变卡片 · 表格转卡片 · 卡片化 · responsive table · 横滚表格 · 横向滚动表格 · 表格太宽 · 表格横向滑动 |
| **作品集** | portfolio · 案例 · 个人站 · 审美校准 |
| **图标** | icon · iconfont · 图标设计 · Iconography · 图标系统 · 图标规范 · 图标库 · 图标字体 · 线性图标 · 面性图标 · 描边图标 · 填充图标 · 双色图标 · duotone · 图标可访问性 · 图标对比度 · 图标按钮 · 图标间距 · 图标尺寸 · sprite 图标 · Lucide · Heroicons · Tabler · Material Symbols · Fluent Icons · Radix Icons · Phosphor · Feather Icons · Ant Design Icons |
| **工具** | tool · 插件 · 效率工具 · 截图 · 录屏 · 生成器 |
| **学习路径** | 怎么学 · 路线图 · 知识地图 · 入门 · 进阶 · 能力自测 |
| **规范文档** | DESIGN.md · 设计规范 · 设计系统文档 · 风格指南 · style guide |
| **版式** | layout · editorial · 版面 · 构图 · 网格系统 · grid system · 分栏 · 栏数 · gutter · 版心 · 页边距 · margin · 基线网格 · baseline grid · 栅格系统 |
| **行长** | measure · line length · 每行字数 · 行宽 · 一行多少字 · 行距 · leading · line-height · 字距 · tracking · 缩进 · 段间距 |
| **海报** | poster · 展板 · 主视觉 · key visual · KV · 活动图 · 宣传图 · 易拉宝 · banner 图 · 三折页 |
| **长图** | long image · 信息图 · infographic · 一图流 · 滑动长图 · 详情页长图 · 长图海报 · 竖长图 |
| **社媒图** | social image · 封面图 · 首图 · 缩略图 · thumbnail · OG image · og:image · 分享卡 · 小红书封面 · 公众号封面 · 视频封面 · 头图 |
| **印刷** | print · 出血 · bleed · 安全区 · safe area · CMYK · 300dpi · 300ppi · 印厂 · 交印 · PDF/X · 总墨量 · 转曲 · 套印 · 裁切线 |
| **竖排** | vertical writing · writing-mode · 直排 · 竖排版 · 纵中横排 · 从右往左 · 繁体竖排 |
| **标志** | logo · logotype · wordmark · symbol mark · 图形标 · 标徽 · 标志设计 · 标志规范 · 品牌符号 |
| **字标** | wordmark · lettermark · monogram · 字母标 · 组合标 · 徽章标 · emblem · 文字标志 · 横排标 · 竖排标 |
| **清space** | clear space · clearspace · 安全边距 · 净空 · 保护空间 · 隔离区 · 留白区 · 最小间距 · clear zone |
| **最小尺寸** | minimum size · 最小使用尺寸 · 缩小极限 · 缩放下限 · 最细笔画 · 小尺寸版 · 简化版标志 · 响应式标志 |
| **品牌色** | brand color · 主色 · 种子色 · seed color · 品牌主色 · 色阶 · 色阶生成 · 调色板生成 · tonal palette · HCT · 品牌调色板 |
| **图标网格** | icon grid · keyline · 基形 · 图标画布 · 24dp · 图标规范 · 笔画粗细 · 图标对齐 · 图标家族 |
| **商标** | trademark · 注册商标 · 尼斯分类 · 商标注册 · 版权 · 著作权 · 商用授权 · 字体授权 · 素材授权 · logo 侵权 |
| **品牌手册** | brand guidelines · 品牌规范 · VI 手册 · 视觉识别手册 · brand book · 品牌指南 · 一页式规范 · brand identity |
| **品牌语气** | tone of voice · 语气 · 品牌声音 · 文案语气 · 品牌人格 · 语气词 · 反语气词 · brand voice |
| **favicon** | 网站图标 · 标签页图标 · app icon · 应用图标 · 桌面图标 · PWA 图标 · maskable · 触屏图标 · apple-touch-icon |
| **暗色模式** | dark mode · dark theme · 深色模式 · 深色主题 · 夜间模式 · 暗黑模式 · 暗色主题 · 暗色版 · night mode · 黑色主题 · 深色版 · 暗色 · 暗黑 |
| **表面层级** | surface · surface container · 表面色 · 层级 · elevation · 高度层级 · 卡片层级 · 浮层 · 层阶 · 层叠 · 深度 · z轴 · 表面变亮 |
| **暗色底色** | 纯黑 · 纯黑背景 · 深灰 · 底色 · 暗色背景 · background color · #121212 · #161616 · 黑底 · 背景明度 |
| **主题切换** | theme switch · 切换主题 · 跟随系统 · prefers-color-scheme · 闪白 · FOUC · 主题持久化 · 三态 · 亮暗切换 · 换肤 · theme.json · color-scheme |
| **暗色文字** | 白字 · 纯白文字 · 文字透明度 · 文字层级 · 晕光 · halation · 光渗 · 暗色下看不清 · 字发虚 · 刺眼 |
| **遮罩层** | scrim · 蒙层 · overlay · 半透明遮罩 · 背景变暗 · 遮罩透明度 |
| **涨跌色** | 红涨绿跌 · 涨跌 · 涨色 · 跌色 · 红绿 · 金融配色 · 股票颜色 · up down color · 盈亏色 |
| **性能** | performance · perf · 加载速度 · 打开速度 · 首屏速度 · 网页性能 · 跑得慢 · 太慢了 · 性能优化 · 速度优化 |
| **LCP** | 最大内容绘制 · 首屏渲染 · 首屏时间 · 首屏加载 · 最大元素 · largest contentful paint · 首屏大图 |
| **卡顿** | INP · 交互延迟 · 点击延迟 · 响应慢 · 掉帧 · 帧率 · 长任务 · 主线程阻塞 · FID · 点了没反应 |
| **CLS** | 布局偏移 · 抖动 · 页面跳动 · 内容跳 · 闪动 · 布局抖动 · cumulative layout shift · 跳一下 |
| **性能预算** | performance budget · 体积上限 · 包体积 · 资源上限 · KB 预算 · 预算表 · 超预算 |
| **图片优化** | 压缩 · 图片格式 · AVIF · WebP · 图片尺寸 · 懒加载 · lazy · srcset · 图片太大 · 图片糊 |
| **字体加载** | font-display · 字体闪烁 · FOIT · FOUT · 子集化 · 字体子集 · WOFF2 · 可变字体 · 字体体积 · 字体太大 |
| **弱网** | 慢网 · 2G · 3G · 省流 · 低端机 · 降级 · Save-Data · reduced-data · 弱网环境 |
| **小程序性能** | 分包 · 主包 · 代码包 · setData · 小程序启动 · 独立分包 · 按需注入 · 包大小 · 小程序慢 |
| **设计交付** | handoff · 设计交接 · 标注稿 · 标注规范 · spec · 设计规格 · 交付文档 · 交付物 · 交付清单 · 切图 · 交图 · 交接 |
| **设计走查** | 走查 · 还原度 · 视觉走查 · 交互走查 · design QA · 还原度检查 · 视觉还原 · 走查表 · 走查清单 · 提测 · 上线前检查 |
| **验收标准** | acceptance criteria · 验收 · 验收条件 · 完成标准 · definition of done · DoD · 算做完 · 验收口径 · 通过标准 · given when then |
| **设计评审** | 评审 · critique · 设计评审会 · 评稿 · design review · 评审会 · 过稿 · 设计批评 · 方案评审 |
| **缺陷分级** | P0 · P1 · P2 · P3 · 优先级分级 · 严重程度 · bug 分级 · 阻断问题 · 发布门禁 · 能不能上线 |
| **组件命名** | 命名规范 · 命名 · 变体命名 · 图层命名 · naming · 命名约定 · 组件属性 · variant 属性 · 组件 API · 属性命名 |
| **版本管理** | semver · 语义化版本 · 版本号 · 发版 · 变更日志 · changelog · 废弃 · deprecation · 迁移 · codemod · 版本级别 |
| **token 交付** | dtcg · tokens.json · .tokens · style dictionary · 变量导出 · token 管线 · 变量同步 · 导出 token · token 格式 |
| **多品牌** | multi-brand · multibrand · 白标 · white label · whitelabel · 租户主题 · 租户换肤 · 客户品牌 · 品牌切换 · 多子品牌 · 私有化换肤 · 换肤 |
| **主题架构** | theming · 主题系统 · 主题矩阵 · 主题轴 · theme matrix · 多主题 · 主题引擎 · 四层 token · brand input · 主题组合 |
| **品牌色生成** | 色阶生成器 · palette generation · brand ramp · 种子色生成 · 品牌色阶 · 自动生成色阶 · hct 生成 · tonal palette · 色度常量 |
| **对比度护栏** | 品牌色校验 · contrast guard · 对比度边界 · 亮度边界 · 前景字色 · 白字还是黑字 · on-brand 颜色 · 自动修正颜色 · 合规校验 |
| **变量作用域** | scoped variables · 变量作用域 · data-brand · data-theme · 作用域化 · 多品牌同页 · 同页多主题 · 嵌套 provider · cssVar · portal 逃逸 |
| **层叠层** | @layer · cascade layer · 层叠层 · 层叠优先级 · 未分层样式 · 覆盖不掉 · 样式优先级 |
| **运行时主题** | runtime theming · 构建期换肤 · 编译期主题 · modifyVars · css 变量换肤 · zero runtime · 预编译样式 · 动态换肤 |
| **主题治理** | 品牌注册表 · 品牌准入 · 主题治理 · 品牌白名单 · 客户自定义边界 · 换肤审计 · 主题变更 |
| **文案** | ux writing · content design · microcopy · 微文案 · 界面文案 · ui copy · 内容设计 · 文案设计 · 文案规范 · 界面文字 |
| **按钮文案** | button text · button copy · 按钮文字 · cta 文案 · 提交按钮文案 · 确认按钮文案 · 按钮该写什么 |
| **错误文案** | error message · error copy · 报错文案 · 错误提示 · 错误信息 · 校验提示 · 验证错误 · form error · 错误消息 |
| **空态文案** | empty copy · empty state copy · 空状态文案 · 无数据文案 · 空页面文案 · empty text |
| **语气** | tone of voice · brand voice · 语气语调 · 品牌语气 · 文案语气 · tone · voice · 品牌人格 · 语气词 |
| **术语管理** | terminology · glossary · 术语表 · 术语统一 · 词汇表 · controlled vocabulary · 同义词管理 |
| **大小写** | capitalization · sentence case · title case ·  casing · 大写 · 小写 · 全大写 · 首字母大写 · 大小写规则 |
| **演示文稿** | presentation · PPT · ppt · 幻灯片 · slides · deck · 演示 · 讲演 · slide deck · keynote · google slides · 汇报 · 答辩 · 课件 |
| **幻灯片母版** | slide master · master slide · 母版 · 模板 · template · 版式 · layout · 占位符 · placeholder · 主题模板 · potx |
| **转场动画** | transition · 转场 · 切换效果 · 切换 · morph · 变体 · fade · 淡入淡出 · 幻灯片切换 · 页面切换 |
| **幻灯片字号** | PPT字号 · 幻灯片字体大小 · 标题字号 · 正文字号 · 最小字号 · 投影字号 · 后排看不清 · 字太小 · point size · pt |
| **安全区** | safe area · safe margin · 安全边距 · 标题安全区 · 动作安全区 · title safe · action safe · 过扫 · overscan · 边缘裁切 · 投影裁切 |
| **线上演示** | online presentation · remote presentation · 线上汇报 · 远程演示 · Zoom演示 · Teams分享 · 屏幕共享 ·  webinar · 网络研讨会 · 视频会议演示 |
| **动效编排** | orchestration · 编排 · 动画顺序 · 序列动画 · 多个动画 · 时间轴 · timeline · 动画调度 · 依次动画 · 同时动 |
| **交错动画** | stagger · staggerChildren · delayChildren · staggerDirection · 交错 · 错峰 · 逐项入场 · 依次出现 · 瀑布式 · 级联动画 |
| **FLIP** | flip · First Last Invert Play · 布局动画 · layout animation · 位移补间 · 重排动画 · 位置补间 · getBoundingClientRect |
| **共享元素转场** | shared element · shared element transition · layoutId · 卡片放大 · 缩略图变大图 · hero transition · 跨视图元素 · 共享布局动画 |
| **视图过渡** | View Transitions · view transition · view-transition · startViewTransition · view-transition-name · match-element · 伪元素树 · 快照转场 · 跨文档转场 · MPA转场 · pageswap · pagereveal |
| **动画状态机** | state machine · statechart · XState · 四态 · entering · exiting · 状态迁移 · 进出场状态 · unmountOnExit · AnimatePresence 状态 |
| **动画中断** | 可中断 · 打断 · 连点就乱 · cancel · commitStyles · skipTransition · 竞态 · 并发转场 · 动画取消 · replaceState · updatePlaybackRate |
| **列表增删动画** | 列表动画 · 增删动画 · AnimatePresence · TransitionGroup · list-move · popLayout · 列表重排 · 退场动画 · exit animation · LayoutGroup |
| **进出场动画** | @starting-style · allow-discrete · transition-behavior · display none 动画 · 入场动画 · 退场看不见 · popover 动画 · overlay · 顶层动画 |
| **国际化与本地化** | i18n · l10n · internationalization · localization · 出海设计 · 多语言 · 全球化设计 · 语言包 · 翻译适配 · locale |
| **RTL 与双向文本** | right-to-left · bidi · bidirectional text · 阿拉伯语 · 希伯来语 · dir=rtl · 从右到左 · 双向文字 · 双向排版 · base direction |
| **文案膨胀** | text expansion · text size in translation · 翻译膨胀 · 字数变长 · 德语太长 · 按钮撑破 · 翻译后溢出 · 文字截断 · 字符余量 · 长度余量 |
| **复数规则** | plural rules · pluralization · cldr plural · Intl.PluralRules · 复数类别 · 数量文案 · one few many other · 中文没有复数 |
| **ICU MessageFormat** | icu message · message format · formatjs · selectordinal · offset:1 · 字符串拼接 · 变量插值 · 整句翻译 |
| **Intl API 与数据格式化** | Intl.DateTimeFormat · Intl.NumberFormat · Intl.DurationFormat · 日期格式 · 货币格式 · 数字格式 · 千分位 · 印度数字分组 · BCP 47 · zh_CN · navigator.language · localeMatcher |
| **CSS 逻辑属性** | logical properties · inline-size · margin-inline-start · inset-inline-start · inline-start · block axis · 逻辑属性 · 方向无关布局 |
| **伪本地化** | pseudolocalization · pseudo-localization · en-XA · en-XB · qps-ploc · qaa-qtz · 加长测试 · 漏译检测 · 定界符暴露截断 |
| **RTL 图标镜像** | mirroring · bidi mirroring · 图标翻转 · 方向性图标 · 进度条镜像 · 媒体控件不镜像 · 数字不镜像 |
| **姓名与地址本地化** | Full name · 姓名字段 · 单名 · 双姓 · patronymic · 地址格式 · 姓名排序 · given name family name |
| **组件文档页** | component documentation · 组件文档 · 组件说明 · component page · 组件页模板 · props 表 · API 文档 · component docs |
| **文档信息架构** | documentation IA · 文档导航 · 文档目录 · docs IA · 信息架构 · 文档站点结构 · docs navigation · sidebar |
| **文档版本化** | docs versioning · versioned docs · 版本化文档 · 多版本文档 · versioned_docs · versions.json · 版本化维护 |
| **变更日志** | changelog · CHANGELOG.md · 更新日志 · 发版说明 · release notes · 版本记录 · Keep a Changelog · Unreleased |
| **迁移指南** | migration guide · 迁移文档 · 升级指南 · breaking changes · codemod · 升级手册 · migration |
| **贡献指南** | contribution criteria · 贡献规范 · 贡献指南 · CONTRIBUTING · 提案门槛 · 准入标准 · contributing |
| **文档治理** | governance · 文档治理 · 文档评审 · docs governance · 维护责任 · owner 归属 · 文档准入 |
| **活文档** | living documentation · 活文档 · 研究证据 · 已知问题 · 近期变更 · Recent changes · Research on this component · Help improve |
| **文档模板** | doc template · 文档模板 · 组件页模板 · documentation template · 文档骨架 · 文档范例 |
| **自动生成文档** | Autodocs · docs-as-code · MDX · Doc Blocks · Storybook docs · 代码即文档 · 自动生成文档 · Code Connect |
| **文档新鲜度** | docs drift · 文档漂移 · 文档陈旧 · 新鲜度 · stale docs · 文档一致性 · 文档腐烂 |
| **文档写作风格** | style guide · 写作规范 · 文档写作 · sentence case · descriptive link · Google style · Microsoft style · alt 文本 |
| **Diátaxis 四象限** | diataxis · 四象限 · tutorials how-to reference explanation · 教程与操作指南 · 技术参考 · 解释型文档 |
| **文档成熟度** | lifecycle · 组件状态 · 成熟度 · USWDS · 45 天评论期 · deprecated component · beta 组件 |
| **AI 生成设计** | AIGC · 生成式设计 · 生成式 AI · generative design · AI 出图 · AI 辅助设计 · AI 做设计 · 文生图 |
| **AI 内容标识** | 生成合成内容标识 · 显式标识 · 隐式标识 · AI 打标 · AI 水印 · 标识办法 · 国信办通字〔2025〕2 号 · GB 45438-2025 |
| **AI 版权** | AI 著作权 · 提示词版权 · prompt copyright · human authorship · USCO · 可举证创作链 · 作者身份 |
| **AI 商用授权** | AI 素材商用 · 商用授权 · 生成素材许可 · 训练数据来源 · 素材授权链 |
| **Content Credentials** | C2PA · 内容凭证 · provenance · 溯源清单 · 内容来源凭证 · 机器可读标记 |
| **提示词工程** | prompt engineering · prompt · 提示词模板 · few-shot · structured outputs · 结构化输出 · developer message |
| **prompt 版本化** | prompt versioning · 模型快照 · model snapshot · eval suite · 提示词回归 · fixtures · rubric |
| **AI 味** | AI Slop Test · AI slop · 一眼 AI · 紫蓝渐变 · 万物皆卡片 · 塑料感 · AI 感 |
| **AI 生成界面验收** | 生成 UI 验收 · AI 页面体检 · ai_ui_audit · 静态扫描 · 九态缺失 · 假数据 |
| **AI 功能界面** | HAX · Human-AI Interaction · 人机交互准则 · AI 助手设计 · 不确定性披露 · 置信度展示 · 全局控制 |
| **DESIGN.md 契约** | Agent Prompt Guide · 九章格式 · 设计契约 · 风格一致性 · design.md for agents · 给 AI 读的规范 |
| **AI 工具选型** | AI 工具链 · ComfyUI · ControlNet · screenshot-to-code · Figma-Context-MCP · 选型三问 · 生成工具 |
| **生成到代码** | 截图转代码 · design to code · AI 写代码 · 代码生成 · 衔接层 |
| **AI 合规** | AI 法规 · EU AI Act Article 50 · 生成式 AI 暂行办法 · 令第 15 号 · deepfake 披露 · 首次暴露告知 |
| **欺骗性设计** | dark patterns · deceptive design · 暗黑模式 · 黑暗模式 · 诱导设计 · 操纵性界面 · 套路设计 · confirmshaming · roach motel · privacy zuckering · 设计伦理 |
| **对称选择** | symmetry in choice · §7004 · 拒绝路径 · 同意对称 · mirroring effect · 撤回同等容易 · 步数测量 |
| **隐私同意** | cookie banner · 同意弹窗 · cookie 同意 · 授权弹窗 · consent UI · 隐私弹窗 · 追踪同意 · 拒绝全部 |
| **一键关闭** | 关闭标志 · 开屏广告 · 弹窗广告 · 两次点击 · 计时关闭 · 广告关闭 · 第十条 |
| **自动续费** | 自动展期 · 续费提醒 · 第 18 条 · 第十八条 · 前五日 · 总局令第 101 号 · 等日期前 |
| **取消订阅** | 难取消 · hard to cancel · 退订 · 解约 · 订阅陷阱 · 随时取消 |
| **默认勾选** | preselection · 预勾选 · 默认授权 · 概括授权 · 捆绑授权 · defaultChecked · 默认值禁区 |
| **成瘾设计** | addictive design · 无限滚动 · 自动播放 · 连胜 · streak · 变比率奖励 · 无限下拉 |
| **未成年人模式** | 防沉迷 · 防沉迷制度 · 适龄提示 · 消费上限 · 令第 766 号 · 监护人控制 · 青少年模式 · 打榜 |
| **包容性设计** | inclusive design · Persona Spectrum · 认知无障碍 · COGA · 认知与学习障碍 · 同理心提示 · Solve for one |
| **反操纵红线** | 反模式 · UI 红线 · 合规验收 · design ethics · 伦理评审 · 静态扫描 |
| **隐藏费用** | hidden costs · junk fees · 埋条款 · 搭售 · 结算加价 · 隐藏订阅 |
| **PIPL 同意** | 个人信息保护法 · cookie wall · 便捷撤回 · 第 16 条 · 自动化决策 · 大数据杀熟 · 个性化推荐开关 |
| **组件 API 设计** | component api · 组件契约 · props 设计 · props 语义 · API surface · 组件接口 · 组件规范 · component contract |
| **受控组件** | controlled · controlled component · 受控 · 非受控 · uncontrolled · value onChange · useControllableState · defaultValue · defaultChecked · isControlled |
| **状态提升** | lifting state up · 状态提升 · 单一数据源 · single source of truth · 状态所有权 · 谁持有状态 |
| **组合模式** | composition · compound components · 复合组件 · 组合优于继承 · composition vs inheritance · children · render prop · 渲染属性 |
| **插槽** | slot · slots · 插槽 · 具名插槽 · named slots · scoped slots · 作用域插槽 · slot outlet · Vue slot · renderless component |
| **asChild** | asChild · 换元素 · 换标签 · Radix Slot · mergeProps · polymorphic · as prop · 渲染成别的标签 |
| **ref 转发** | forwardRef · ref as a prop · React 19 · useImperativeHandle · 命令式 API · imperative handle · open close handle · ref 透传 |
| **props 透传** | 透传 props · spread props · 剩余属性 · props 合并优先级 · merge priority · 开放扩展 · open for extension |
| **v-model** | modelValue · update:modelValue · 双向绑定 · two-way binding · model modifiers · one-way data flow · props 单向流 · Boolean casting |
| **键盘契约** | roving tabindex · aria-activedescendant · 单个 tab stop · tab sequence · 焦点管理 · keyboard interface · APG keyboard · focus vs selection |
| **data 状态属性** | data-state · data-* 状态 · 状态属性 · data attributes · 样式钩子 · 状态暴露 |
| **API SemVer** | 组件发版 · component semver · 改默认值 · breaking change · codemod · 迁移脚本 · 冻结面 · deprecated prop |
| **argTypes** | Storybook Controls · controls 面板 · control false · table.disable · requiredFirst · props 文档 · autodocs |
| **组件库** | component library · 组件库 · design system 代码 · headless ui · Radix · Ariakit · MUI slots · shadcn |
| **设计度量** | 设计度量 · 设计指标 · 度量设计效果 · 设计衡量 · 设计评估指标 · UX 指标 · UX metrics |
| **用户研究** | 用户研究 · 用研 · 用户调研 · UXR · 用户洞察 · user research |
| **可用性测试** | 可用性测试 · usability testing · 出声思考 · think aloud · 发声思考 · 可用性实验 · 主持式测试 · 非主持式测试 |
| **SUS 系统可用性量表** | SUS · System Usability Scale · 系统可用性量表 · 易用性量表 · 系统可用性 |
| **UMUX 微型可用性量表** | UMUX · UMUX-Lite · 微型可用性量表 · 迷你可用性量表 |
| **样本量** | 样本量 · 样本大小 · 多少人 · sample size · 多少用户 · 招募多少人 · 样本量怎么算 |
| **任务成功率** | 任务成功率 · 任务完成率 · completion rate · 成功失败率 · 错误率 · 任务时长 |
| **HEART 框架** | HEART · Google HEART · 幸福感参与采纳留存任务成功 · heart framework |
| **A-B 测试** | A/B 测试 · AB 测试 · 灰度测试 · 对照实验 · 拆分测试 · 实验设计 · ab test · 线上实验 |
| **置信区间** | 置信区间 · 95% 置信区间 · confidence interval · CI · 误差区间 · 置信度 |
| **问卷设计** | 问卷 · 问卷设计 · survey · 量表 · 李克特 · Likert · 问卷调查 |
| **NPS 净推荐值** | NPS · 净推荐值 · 净推荐分 · 推荐意愿 |
| **卡片分类** | 卡片分类 · card sorting · 开放式分类 · 封闭式分类 · IA 结构 · 信息架构分类 |
| **树测试** | 树测试 · tree testing · 信息架构测试 · IA 测试 |
| **研究方法** | 研究方法 · 定性研究 · 定量研究 · 态度行为 · 2x2 研究方法 · 研究设计 |
| **导航** | navigation · nav · navbar · 菜单 · menu · 侧边栏 · sidebar · 汉堡菜单 · hamburger · 汉堡 · 面包屑 · breadcrumb · 标签页 · tabs · 信息架构 · IA · information architecture · 当前位置 · you are here · skip link · 跳转链接 · 全局导航 · 底部导航 · tab bar · 主导航 · 导航栏 · 菜单项 |
| **设计评审** | critique · design critique · 设计走查 · 评审 · 评审会 · 反馈 · 给反馈 · feedback · design review · 走查 · i like i wish i wonder · 设计by committee · design by committee · hippo · 委员会改稿 · 决策留痕 · adr · 评审反馈 · 怎么评审 · 接收反馈 |
| **色彩科学** | color science · 色彩理论 · 色彩空间 · oklch · oklab · OKLCH · OKLab · Display P3 · display-p3 · 感知均匀 · 色相旋转 · 色板生成 · 调色 · 配色方案 · 渐变插值 · APCA · 相对亮度 · HSL 撒谎 · sRGB · 色域 |
| **风格** | 视觉风格 · 风格谱系 · 设计运动 · 设计风格 · 视觉调性 · 做成XX感觉 · 做成XX那种感觉 · 高级感 · 复古感 · 科技感 · 温暖感 · 视觉语言 · 极简风 · 扁平风 · 拟物 · skeuomorphism · 玻璃拟态 · glassmorphism · 新拟态 · neumorphism · soft ui · 野兽派 · brutalism · 新野兽派 · neo-brutalism · 瑞士风格 · swiss style · 孟菲斯 · memphis · y2k · 赛博朋克 · cyberpunk · 极繁 · maximalism · 极简主义 · minimalism · 便当盒 · bento · 黏土风 · claymorphism |
| **字体排印** | typography system · 字体排印系统 · 排印 · type scale · 字号阶梯 · font-size · font size · font-weight |
| **行距节奏** | line height · 字间距 · letter-spacing · 词间距 · word-spacing · 段距 · 行长太长 · 行长多少 |
| **中文混排** | 中文排版 · 中西文混排 · 全角半角 · 全角 ASCII · 字素丛 · grapheme cluster |
| **逐字符回退** | 字体回退 · fallback 字体 · font-family · generic family · 缺字 · tofu · 方框乱码 · 字体覆盖 |
| **可变字体轴** | variable font · variable fonts · 变体轴 · 注册轴 · wght · wdth · slnt · ital · opsz · GRAD · font-variation-settings |
| **数字特性** | 等宽数字 · 数字抖动 · 数字会跳 · tabular-nums · tabular figures · tnum · linum · onum · pnum · slashed-zero |
| **OpenType 特性** | font-variant-numeric · font-feature-settings · font-variant-caps · small caps · 小型大写 |
| **字体交付** | size-adjust · font-size-adjust · unicode-range · web font · webfont · 自托管字体 |
| **字体许可** | 字体商用 · 字体版权 · OFL · SIL OFL · Reserved Font Name · RFN |
| **文本间距覆盖** | 文本间距 · 文字间距 · text spacing · WCAG 1.4.12 · 1.4.12 · 200% 缩放 · 放大文字 · resize text |
| **圆角** | 圆角 · radius · border-radius · 倒角 · 圆角半径 · 胶囊 · pill · 全圆角 · 方角 · 直角 |
| **阴影** | 阴影 · box-shadow · drop-shadow · 投影 · 三层阴影 · 阴影token · blur-radius · spread-radius · inset |
| **形状尺度** | shape scale · 形状 · corner · 几何 · 轮廓 · 圆角阶 · shape token · 形状系统 |
| **材质层** | 毛玻璃 · backdrop-filter · 材质 · Liquid Glass · blur · 模糊 · 半透明 · vibrancy · dimming layer |
| **层叠刻度** | z-index · 层叠顺序 · 层叠上下文 · stacking context · 浮起 · 抬起 · dp · elevation scale |
| **圆角几何** | 嵌套圆角 · 同心圆角 · concentric radius · 内外圆角 · 圆角重叠 · corner overlap · squircle · corner-shape · superellipse · 连续圆角 |
| **格式塔组织律** | 格式塔 · 完形 · Gestalt · 组织律 · 邻近性 · 相似性 · 闭合性 · 连续性 · 共同区域 · 共同命运 |
| **视觉层级** | 视觉层次 · 信息层级 · 视觉动线 · 主次不清 · 重点不突出 · 焦点不清晰 · 层级不清 · 视觉重量 · 眯眼测试 |
| **扫描模式** | 眼动 · F型 · F 型 · F-pattern · Z型 · 层叠蛋糕 · layer-cake · spotted · bypassing · commitment |
| **认知负荷** | 工作记忆 · 组块 · chunking · 7±2 · 米勒定律 · 选择过载 · 心智负担 · 信息过载 · 记不住 |
| **希克定律** | Hick · Hick's Law · 选项太多 · 决策时间 · 选择耗时 · 菜单项数 · 渐进披露 |
| **菲茨定律** | Fitts · Fitts's Law · 目标尺寸 · 按钮太小 · 点不到 · 命中区域 · 边缘角落 · 运动距离 |
| **前注意属性** | 选择性注意 · pop-out · 弹出效应 · 特征整合 · Treisman · 图形背景 · 多稳态 · 孤立效应 · Von Restorff · 序列位置 |
| **顺序一致性** | DOM 顺序 · dom · 视觉顺序 · 焦点顺序 · 标题结构 · tabindex · 阅读顺序 · 语义顺序 · CSS 重排 |
| **内容可发现性** | 可发现性 · findability · 内容找不到 · 找不到内容 · 搜不到 · 找路 · 站点可发现性 · 内容线索 |
| **搜索体验** | 搜索框 · 站内搜索 · 搜索体验 · site search · search UX · 自动补全 · autocomplete · 联想词 · 搜索建议 · 搜索结果页 · combobox |
| **链接目的** | 链接文案 · link purpose · Learn More · 了解更多 · 点击这里 · 描述性链接 · 脱离上下文 · 重复链接文本 · 链接可预测性 |
| **可扫读性** | 可扫读 · scannability · 扫读 · 阅读等级 · reading level · Flesch · FKGL · SMOG · 简明语言 · plain language · 前置关键词 · front-loading |
| **信息气味** | 信息气味 · information scent · 线索密度 · 首词 · 前 11 个字符 · nano-content |
| **零结果** | 零结果 · no results · 没有结果 · 无搜索结果 · 搜索无结果 · 空结果 |
| **拖拽交互** | 拖拽 · 拖放 · 拖动 · drag and drop · direct manipulation · 直接操纵 · 拖动排序 · 拖动重排 · dnd |
| **指针事件** | Pointer Events · pointercancel · setPointerCapture · releasePointerCapture · hasPointerCapture · pointerdown · pointermove · pointerType · isPrimary · 隐式指针捕获 |
| **拖动替代路径** | 单指针无拖动 · G219 · 点击目标位置 · 移动到下拉菜单 · 箭头逐步移动 · 数字位置输入 · 拖动取消 |
| **触控目标尺寸** | 24×24 CSS px · 44×44 CSS px · 48 x 48 dp · 8dp 间距 · spacing 例外 · 24 CSS px 直径圆 · touch target · WCAG 2.5.8 · WCAG 2.5.5 |
| **手势与取消** | path-based gesture · 路径手势 · touch-action · G210 · No Down-Event · Up Reversal · Abort or Undo · path-based · 手势取消 |
| **拖放库** | dnd-kit · react-dnd · SortableJS · pragmatic-drag-and-drop · interact.js · use-gesture · 25px 位移 · aria-roledescription |
| **对话式界面** | chatbot · 聊天机器人 · 聊天 UI · 对话 UI · AI 助手 · 对话式界面 · 聊天气泡 · 会话界面 · Copilot · 助手面板 |
| **流式输出** | streaming · 流式输出 · 逐字输出 · 打字机效果 · 逐字蹦 · token 流 · SSE · 边生成边显示 · 流式渲染 |
| **生成式界面** | Generative UI · GenUI · streamUI · 生成式 UI · 生成式组件 · 组件白名单 · 动态组件路由 · AI SDK RSC |
| **对话状态机** | useChat · message.parts · AG-UI · RunStarted · RunFinished · TextMessageStart · ToolCallStart · 四态状态机 |
| **聊天无障碍** | role=log · ARIA23 · aria-live · aria-busy · aria-atomic · SC 4.1.3 · Status Messages · 读屏刷屏 · polite |
| **AI 纠错** | 停止生成 · 重新生成 · regenerate · 编辑原消息重放 · 撤销自动化动作 · HAX G9 · 四档恢复链 · Hybrid UI · RICH 范式 |
| **模态判型** | 模态性 · modality · 焦点陷阱 · focus trap · inert · 背景不可交互 · aria-modal · 非模态 · modeless · top layer · 顶层栈 |
| **原生对话框** | showModal · HTML dialog · closedby · ::backdrop · returnValue · autofocus · 焦点返回 · dialog 元素 · show() |
| **Popover API** | popover · popovertarget · popovertargetaction · showPopover · hidePopover · togglePopover · beforetoggle · auto state · hint state · manual state · auto stack · hint stack |
| **WCAG 遮挡** | SC 1.4.13 · Dismissible · Hoverable · Persistent · SC 2.4.11 · Focus Not Obscured · F110 · C43 · scroll-padding · SC 2.1.2 · No Keyboard Trap · SC 3.2.1 |
| **浮层组件族** | bottom sheet · 底部抽屉 · drawer · command palette · 命令面板 · 气泡卡片 · 非模态浮层 · date picker · mega menu |
| **退出契约** | Escape 关闭 · 点击外部关闭 · light dismiss · 关闭契约 · 焦点返回触发元素 · 无鼠标退出 · F6 切层 · 退出路径 |

新增别名改 `memory/aliases.json`；`dp_search.py "词" --no-alias` 可关闭扩展做对比。

## 二、知识树（按文件）

### `SKILL.md` · Design Partner 设计伙伴
_985 行 · 快照 — · 12 节_

- **工作流：接到任何设计任务时按此执行** `L116` — 资产已 43 份参考、约 118 万字符。整份读完等于浪费上下文，而答案通常只在一节。动手前：
  - **第 0 步 · 先检索，别整份读** `L118` — 资产已 43 份参考、约 118 万字符。整份读完等于浪费上下文，而答案通常只在一节。动手前：
  - **第 1 步 · 识别设计意图** `L131`
  - **第 2 步 · 完善需求（设计 brief 澄清）** `L353` — 动手前检查以下要素。只问缺失且影响方向的项（一次最多 3 个，给选项不给开放题）；要素齐全就直接进第 3 步。用户不在场时选合理默认值并注明假设。
  - **第 3 步 · 可行性 × 美观性预判（自我判断，反馈给用户）** `L368` — 执行前对需求本身给出结构化评审——这一步的产出是给用户的反馈，不是自我怀疑。用户在线时先给评审再动手；不在线时把评审作为交付说明的开头。
  - **第 4 步 · 匹配灵感（三级精准匹配）** `L394` — 先读 memory/design-log.md 的「当前画像」：用户既定偏好优先于通用推荐（画像说不要渐变，就不出现渐变变体）。
  - **第 5 步 · 按设计原则执行** `L425` — 从策展标准（craft / utility / clarity / relevance）展开，适用于任何视觉产出：
  - **第 6 步 · 产出前自检 + 交付评审** `L863` — 交付前逐条检查，不达标先修再交：
- **自我成长机制（用得越多越准）** `L941` — 记忆档案 memory/design-log.md 分两层，协议如下：
- **自我进化机制（知识保鲜）** `L954` — - 自动刷新：references 头部标注快照日期。快照 30 天、或用户说"更新知识库/刷新灵感库"时，执行 python <技能目录/scripts/refreshcatalog.py——它重抓 designeer.xyz 目录 AP
  - **每日升级协议（Deep Distillation Loop）** `L961` — 定时任务按此五步跑，每次只深挖一个主题，不做广度摊平：
- **边界与习惯** `L977` — - 给立场：评审和对比都先给明确结论和理由，再列备选；不和稀泥。

### `references/accessibility.md` · 可访问性实操 / 无障碍（Accessibility in Practice）
_690 行 · 快照 2026-11-01 · 58 节_

- **§1 先定判定口径：无障碍验收按哪套标准（否则后面全是空谈）** `L9` — - WCAG 2.1 有 78 条成功标准；2.2 新增 9 条、废弃 1 条（4.1.1 Parsing）→ 合计 86 条。
  - **1.1 WCAG 2.2 的结构** `L11` — - WCAG 2.1 有 78 条成功标准；2.2 新增 9 条、废弃 1 条（4.1.1 Parsing）→ 合计 86 条。
  - **1.2 2.2 新增的 9 条（这轮升级的主要增量）** `L17`
  - **1.3 本技能的默认目标线** `L31` — - 默认 AA：这是法律与采购的实际门槛（欧盟 EAA、美国 ADA 判例、国内适老化评测均以 AA 为基线）。
- **§2 对比度：四个阈值、一条铁律、一个中文陷阱** `L38` — 大文本的精确边界（W3C 原文）：≥ 18pt（≈ 24px）或 ≥ 14pt 粗体（≈ 18.5px）。换算 1pt = 1.333px。
  - **2.1 四个阈值（精确值，不许记错）** `L40` — 大文本的精确边界（W3C 原文）：≥ 18pt（≈ 24px）或 ≥ 14pt 粗体（≈ 18.5px）。换算 1pt = 1.333px。
  - **2.2 铁律：不可四舍五入** `L53` — W3C 原文：4.499:1 不满足 4.5:1。工具显示 "4.5" 时要看三位小数。设计交付前把色值代进公式自己算一遍：
  - **2.3 灰阶速查（省去每次开工具）** `L58` — 以纯白 #FFFFFF 为背景，正文需 4.5:1 → 文字不得浅于 #767676（约 4.54:1）。
  - **2.4 中文特有的对比度陷阱** `L77` — 拉丁字母笔画细、字腔大；汉字笔画密度高、字腔小。同样的对比度，中文的可读性明显更差，尤其是 12–14px 的细体。
- **§3 焦点可见：三层标准叠着用** `L89` — 焦点是键盘用户的"鼠标指针"。三层标准必须同时满足：
  - **3.1 面积怎么算（2.4.13 的唯一硬指标）** `L101` — - 贴边实心框：2px 粗即达标。
  - **3.2 可直接抄的焦点样式（三选一，全站统一）** `L109` — A. GOV.UK 方案（最稳，任何背景都能过） —— 官方功能色：focus = #FFDD00，focus-text = #0B0C0C。
  - **3.3 :focus-visible 的纪律** `L145` — - 只用 :focus-visible，不用 :focus 做视觉样式。:focus 会让鼠标点击也出现焦点框（用户觉得丑）→ 团队就会 outline: none → 键盘用户彻底失去焦点。
  - **3.4 焦点反模式（逐条对照）** `L152` — 1. outline: none 且无替代 → 直接失败 2.4.7。
- **§4 键盘：顺序、陷阱、返回** `L164` — - 顺序 = DOM 顺序。视觉顺序必须与 DOM 顺序一致；用 order / grid-area / flex-direction: row-reverse 改视觉顺序会造成焦点跳跃。
  - **4.1 Tab 顺序** `L166` — - 顺序 = DOM 顺序。视觉顺序必须与 DOM 顺序一致；用 order / grid-area / flex-direction: row-reverse 改视觉顺序会造成焦点跳跃。
  - **4.2 跳转链接（Skip link）** `L172` — 每个页面第一个可聚焦元素应是"跳到主内容"：
  - **4.3 模态：焦点必须被管住** `L186` — 按 WAI-ARIA APG Dialog (Modal) 的硬要求：
  - **4.4 焦点可见性之外：焦点不能丢** `L213` — - 删除列表项后，焦点会掉到 body。必须手动把焦点移到逻辑邻居（下一项，或空态的"新建"按钮）。
- **§5 焦点不被遮挡（2.4.11）：粘性栏的账要还** `L221` — 判定是二值的：组件被作者内容完全遮住 → 失败（F110）；哪怕露一条边 → AA 通过。
- **§6 目标尺寸：24 是底线，44 是好用，48/60 是适老** `L241` — - 目标区域必须能完整容纳一个 24×24 CSS px 的轴对齐正方形。圆角、裁剪、异形都会导致装不下 → 判定"undersized"。
  - **6.1 2.5.8（AA）的精确判定** `L243` — - 目标区域必须能完整容纳一个 24×24 CSS px 的轴对齐正方形。圆角、裁剪、异形都会导致装不下 → 判定"undersized"。
  - **6.2 本技能的三档目标尺寸** `L254` — 视觉尺寸 ≠ 点击尺寸：图标画 16px，热区用 padding 撑到 44×44。不要靠"图标画大"来解决。
- **§7 拖动必须有替代（2.5.7）** `L273` — 条文：所有用拖动完成的功能，必须能用单指针不拖动完成（除非拖动是 essential，或功能由 UA 决定且作者未改）。
- **§8 语义与 ARIA：原生优先，ARIA 是补丁不是方案** `L290` — No ARIA is better than Bad ARIA.（APG 原文）
  - **8.1 第一原则** `L292` — No ARIA is better than Bad ARIA.（APG 原文）
  - **8.2 四条最容易犯的 ARIA 错误** `L308` — 1. aria-label 覆盖可见文本：<button aria-label="关闭对话框"×</button 尚可；但 <button aria-label="提交订单"提交</button 会让语音控制用户说"提交订单"点不到——可见
  - **8.3 可访问名称的优先级（从高到低）** `L315` — aria-labelledby → aria-label → 原生 <label for → 元素内含文本 → title → placeholder（最弱，不能当标签）。
  - **8.4 图标按钮必须有名称** `L321` — 只有图标、没有可访问名称的按钮，读屏会念"按钮"——用户完全不知道它干什么。
- **§9 表单无障碍：只补 form-table.md 没说的** `L330` — form-table.md §11 已给 10 条表单可访问性要点。这里补结构层的四件事：
  - **9.1 错误与帮助的关联（ARIA 侧）** `L334` — - aria-describedby 同时挂帮助和错误，读屏聚焦时会一起念。
  - **9.2 错误摘要（多字段表单必做）** `L350` — 提交失败时，在表单顶部放一个可聚焦的错误摘要，列出全部错误并链接到对应字段：
  - **9.3 autocomplete 是 AA 要求，不是优化项** `L366` — WCAG 1.3.5 Identify Input Purpose（AA）要求表单字段能程序化识别用途。落地就是 autocomplete。中文场景高频值：
  - **9.4 3.3.7 冗余录入：多步流程必须回填** `L385` — 同一流程内已填信息不得再要一遍，除非：回填会让流程失效（记忆游戏）、安全需要（密码确认）、原信息已失效（验证码过期）。
- **§10 动态内容播报：aria-live 用对了才有用** `L393` — 四条纪律：
- **§11 图片、图标、图表的替代文本** `L418` — 1. 纯装饰 → alt=""（空字符串，明确告诉读屏跳过）。不要省略 alt 属性，省略会让读屏念文件名。
  - **11.1 alt 决策树（四选一，不许空着）** `L420` — 1. 纯装饰 → alt=""（空字符串，明确告诉读屏跳过）。不要省略 alt 属性，省略会让读屏念文件名。
  - **11.2 图表的具体写法** `L427` — 内联 SVG 若含可聚焦元素或大量 <path，加 aria-hidden="true" 并把文字说明放在外部。dataviz.md §9 的对比度要求与此处并行：视觉可读与语义可读是两件事。
  - **11.3 图标字体** `L439` — 图标字体（iconfont）的字符读屏会念成乱码。必须：
- **§12 不靠颜色单独传达（1.4.1）** `L448` — 条文：颜色不得是传达信息、指示动作、区分元素的唯一视觉手段。
  - **12.1 色觉障碍的实际比例** `L462` — - 红绿色觉异常（deuteranopia/protanopia）在男性约 8%、女性约 0.5%。中文 B 端产品一个 200 人团队里通常有 6–10 人。
  - **12.2 色盲友好色板：Okabe–Ito 8 色（R grDevices 内置值，逐字核对）** `L467` — 用法：需要 ≤8 类无序分类且必须色盲可辨时优先用它（论文/科研图、公共信息图）。日常产品界面仍用品牌色板（dataviz.md §3），但必须补第二通道。
  - **12.3 检查方法** `L484` — - 浏览器 DevTools → Rendering → Emulate vision deficiencies（Deuteranopia/Protanopia/Tritanopia/Achromatopsia）。
- **§13 用户偏好媒体查询（三条，别只做第一条）** `L491` — forced-colors 是最容易被忽略的一条：Windows 高对比度模式下，box-shadow、background-image、linear-gradient 全部被抹掉。凡是"靠阴影表达层级""靠渐变区分按钮"的界面，在这个模式
- **§14 读屏实测：不做实测等于没做** `L517` — 自动化工具只能发现约三分之一的问题（结构性、可判定的）。焦点顺序、播报质量、语义是否通顺，必须人耳听。
  - **14.1 组合矩阵（各平台各选一个，不必全装）** `L521`
  - **14.2 十五分钟最小实测脚本（每次交付前跑一遍）** `L533` — 1. 只用 Tab：能否到达全部可交互元素？顺序是否与视觉一致？焦点是否始终可见？
- **§15 自动化工具的边界（别把它当验收）** `L548` — 行业共识：自动化覆盖约 30%–40% 的问题，且偏向"有无"而非"好坏"。任何"Lighthouse 无障碍 100 分"都不等于合规。
  - **15.1 能测 / 不能测** `L550` — 行业共识：自动化覆盖约 30%–40% 的问题，且偏向"有无"而非"好坏"。任何"Lighthouse 无障碍 100 分"都不等于合规。
  - **15.2 工具矩阵（star / 许可实测于 2026-11-01）** `L562` — CI 落地：npx @axe-core/cli <url --exit 或 Playwright + @axe-core/playwright，把 critical/serious 设为失败门禁。moderate 先告警不阻断（否则历史债务
- **§16 中文场景：法规、国标、适老化（国外规范不管的部分）** `L577` — GB/T 37668 与 WCAG 的关系：框架对应（四原则），但不是逐条等同，且多了"兼容性"的国产浏览器/读屏要求。做政府、金融、医疗项目时，验收口径常是"GB/T 37668 + WCAG 2.1 AA 双达标"。
  - **16.1 法规与标准三层** `L579` — GB/T 37668 与 WCAG 的关系：框架对应（四原则），但不是逐条等同，且多了"兼容性"的国产浏览器/读屏要求。做政府、金融、医疗项目时，验收口径常是"GB/T 37668 + WCAG 2.1 AA 双达标"。
  - **16.2 适老化的硬数字（工信部 APP 规范）** `L589` — - 主要组件可点击焦点区域：适老版界面 ≥ 60×60 dp/pt；其他页面 ≥ 44×44 dp/pt。
  - **16.3 中文界面三个专属坑** `L599` — 1. 字号下限：WCAG 没有最小字号（靠缩放），但中文 12px 在 1080p 上已接近不可读。中文正文 16px 起，辅助文字 ≥12px 且必须 ≥4.5:1（chinese-design.md §1）。
- **§17 上线前自检：25 条（按可判定性排序）** `L607` — A 级（必过，8 条）
- **§18 反模式 18 条（评审时逐条对照）** `L644` — 1. outline: none 全局重置，无替代焦点样式。
- **§19 三个常见争议，本技能给立场** `L667` — Q1：APCA 能不能用？
- **参考来源（本文件数值的出处）** `L680` — - WCAG 2.2 正式标准与 Understanding 文档：https://www.w3.org/TR/WCAG22/、https://www.w3.org/WAI/WCAG22/Understanding/（2.4.11 / 2.

### `references/ai-design-toolchain.md` · AI / 生成式设计工具链：工作流、提示词、质量验收与合规边界
_790 行 · 快照 2026-11-06 · 61 节_

- **0. 与既有资产的分层（先判该读哪份）** `L9` — 边界纪律：本文件不重讲 WCAG 阈值、不断点数值、不 toast 时长、不色板 hex。需要数值去对应专项文件读，§12 是索引不是副本。副本必然漂移。
- **1. 判层：AI 在设计流程的五个位置，以及哪些活不该交出去** `L25` — 1. 合规判断：能不能商用、要不要打标、是否侵权、是不是 deepfake —— AI 会 confidently 编造法条。只认 §2–§5 的官方原文，并让法务复核。
  - **1.1 五层地图（每层都要有人工闸门）** `L27`
  - **1.2 三类活不要交给 AI（给立场，不和稀泥）** `L37` — 1. 合规判断：能不能商用、要不要打标、是否侵权、是不是 deepfake —— AI 会 confidently 编造法条。只认 §2–§5 的官方原文，并让法务复核。
  - **1.3 一条效率判据** `L43` — AI 适合"生成可丢弃的选项"，不适合"生成不可回退的结论"。
- **2. 合规地基（一）：中国 AI 生成内容标识，是法定义务不是设计建议** `L50` — ⚠️ 口径纪律：GB 45438-2025 的具体像素、字号、音频时长等数值，本文件不臆造。国标全文未逐字取得时，只写"标准规定了显式标识的时长、尺寸与隐式标识要素"（此结论来自网信办 2025-09-05 专家解读原文），落地时以国标全文
  - **2.1 三层法规栈（日期必须记准）** `L52` — ⚠️ 口径纪律：GB 45438-2025 的具体像素、字号、音频时长等数值，本文件不臆造。国标全文未逐字取得时，只写"标准规定了显式标识的时长、尺寸与隐式标识要素"（此结论来自网信办 2025-09-05 专家解读原文），落地时以国标全文
  - **2.2 《标识办法》逐条翻译成设计动作（14 条，原文口径）** `L62`
  - **2.3 设计交付清单（可直接贴进 spec）** `L79` — - [ ] 生成结果在界面上有显式标识（文字/声音/图形，位置按第 4 条按载体分）
- **3. 合规地基（二）：中 / 欧 / 美三法域矩阵（出海产品必读）** `L93`
  - **3.1 三条落地判据** `L105` — 1. 按最严法域做一套，不要做三套：中国要求显式（人读）+ 隐式（机读）双轨，欧盟要求机器可读标记，二者可共用同一份元数据管线；"符合中国双轨"是充分条件里的较强者。欧盟额外多的是"告知在与 AI 交互"与"deepfake 披露"，这是界
- **4. 裁决一：提示词写得再细，也不构成作者身份（本轮最重要的一条）** `L115` — 美国版权局《Copyright and Artificial Intelligence, Part 2: Copyrightability》于 2025-01-29 发布。其官方解读（U.S. Copyright Office / Libr
  - **4.1 权威口径** `L117` — 美国版权局《Copyright and Artificial Intelligence, Part 2: Copyrightability》于 2025-01-29 发布。其官方解读（U.S. Copyright Office / Libr
  - **4.2 被纠正的常见说法** `L130`
  - **4.3 设计侧的可执行结论：留下可举证的创作链** `L139` — 既然"人类决定了足够的表达元素"是保护门槛，交付时就要把这件事留痕：
- **5. 裁决二：Content Credentials / 打了 AI 标 ≠ 版权清晰 ≠ 内容为真** `L153` — C2PA（Coalition for Content Provenance and Authenticity，Joint Development Foundation 项目）现行规范门户为 2.5（含 Content Credentials
  - **5.1 C2PA 到底断言什么** `L155` — C2PA（Coalition for Content Provenance and Authenticity，Joint Development Foundation 项目）现行规范门户为 2.5（含 Content Credentials
  - **5.2 它不断言什么（原文边界）** `L166` — "Content Credentials do not provide value judgments about whether a given set of provenance data is 'true', but instead 
  - **5.3 三个必须分开的概念（最容易混）** `L176` — ⚠️ 三者互不替代：一个文件可以有合规标识、有 Content Credentials，却没有可用版权（纯 AI 输出）；也可以有人类充分创作（可版权）但没打法定标识（违规）。把"打了标"当成"可以商用"是本轮要消灭的误解。
  - **5.4 中国隐式标识与 C2PA 的关系** `L186` — - 中国第 5 条要求的是文件元数据中的生成合成内容属性信息 + 服务提供者名称/编码 + 内容编号；并鼓励数字水印。
- **6. AI 素材的来源与授权链** `L194` — 提供者应当依法开展预训练、优化训练等训练数据处理活动：①使用具有合法来源的数据和基础模型；②涉及知识产权的不得侵害他人依法享有的知识产权；③涉及个人信息的取得同意或符合法定情形；④提高训练数据质量，增强真实性、准确性、客观性、多样性；⑤遵守
  - **6.1 训练数据侧的法定要求（《暂行办法》第 7 条，原文五款）** `L196` — 提供者应当依法开展预训练、优化训练等训练数据处理活动：①使用具有合法来源的数据和基础模型；②涉及知识产权的不得侵害他人依法享有的知识产权；③涉及个人信息的取得同意或符合法定情形；④提高训练数据质量，增强真实性、准确性、客观性、多样性；⑤遵守
  - **6.2 输入侧：别把客户的资产贴进外部模型** `L202` — 《暂行办法》第 11 条要求提供者不收集非必要个人信息、不非法留存可识别使用者身份的输入信息和使用记录、不非法向他人提供。对应到设计侧：
  - **6.3 授权四查（与 brand-identity.md §17 串联）** `L210` — 1. 模型/服务 ToS：商用是否允许、是否要求署名、是否有赔偿条款、输出权利归谁（注意 §4：ToS 给的是 license，不是著作权转让）。
- **7. DESIGN.md：把"风格一致性"变成 AI 可读的契约** `L219` — design-md-format.md 已给九章骨架；本节补的是为什么它是 AI 工具链的关键节点，而不是抄一遍骨架。
  - **7.1 三条纪律** `L225` — 1. 第 9 章最常被漏，但它是"可执行"的关键：给 agent 的 3–5 条生成指令 + 一段可直接用的 prompt 模板。没有它，前 8 章只是给人看的说明书。
  - **7.2 与 token 体系对齐** `L231` — DESIGN.md 里的色值/字号/间距必须与 design-tokens.md 的三层架构和 multi-brand-theming.md 的 L0–L3 一致。AI 生成 UI 最常见的系统性故障不是"不好看"，而是每次生成的十六进制值
- **8. 提示词工程：把设计 brief 变成可复用、可评估的 prompt** `L237` — developer message 推荐按 Identity → Instructions → Examples → Context 组织：
  - **8.1 官方结构（OpenAI Prompt Engineering 指南口径）** `L239` — developer message 推荐按 Identity → Instructions → Examples → Context 组织：
  - **8.2 输出与评估的工程化（不是"多试几次"）** `L255` — - 指定输出格式：JSON Schema / Structured Outputs、严格单值输出、"不要 Markdown 只返回代码"；前端场景明确 Markdown standards（inline code / fences / 表格
  - **8.3 设计 brief → prompt 转换表（本技能第 2 步的落地）** `L266` — 设计上下文不能靠读代码库推断（impeccable 纪律）：代码只说明"构建了什么"，不说明"为谁构建 / 应该有什么感觉"。目标受众、用例、品牌调性必须由人给，或读项目根 .impeccable.md / Design Context 段
  - **8.4 一段可复用模板** `L279` — 见 §21.2。核心是 四区块 + 硬约束清单 + 输出 schema + 自检 rubric，且把"给立场、列反例、标不确定"写成指令，而不是期望模型自发做到。
- **9. AI 辅助设计的工作流（可直接落地的 8 步）** `L285` — 1. 写 brief（人）：受众 / 用例 / 品牌调性 / 硬约束 / 成功标准，最多 3 个澄清问题、给选项不给开放题（本技能第 2 步）。
- **10. AI 功能界面：微软人机交互 18 条准则（HAX G1–G18）** `L300` — 来源：Microsoft HAX Toolkit《Guidelines for Human-AI Interaction》，综合 20+ 年研究，2019 CHI 获奖论文；官方说明其设计模式贯穿 Initial / During inte
  - **准则 1–6** `L306`
  - **准则 7–11** `L316`
  - **准则 12–13** `L325`
  - **准则 14–18** `L331`
  - **接线：18 条准则接回本技能既有资产** `L340` — - G2 / G11（不确定性披露） ↔ feedback-states.md §1 五层决策树：AI 建议属于低风险可撤销反馈，别用模态打断；但"生成失败/内容被拦截"属于错误，要按 §6 三级错误文案写清发生了什么 + 为什么 + 怎么
- **11. AI 味验收：AI Slop Test 与 8 维 DO/DON'T** `L350` — 来源：impeccable（基于 Anthropic frontend-design 技能，Apache-2.0，仓库 pbakaus/impeccable 实测 104380★ / Apache-2.0 / 2026-11-05）。
  - **11.1 一句话测试** `L354` — "如果你把这个界面展示给某人并说'这是 AI 做的'，他们会立刻相信吗？如果是，那就是问题所在。"
  - **11.2 8 维 DO / DON'T 速查** `L361` — 与既有资产一致性：色彩/字体的"不用纯黑纯白"与 dark-mode.md §3「不用纯白」同源；动效的"不动画化布局属性"与 performance-design.md §11「只动 transform/opacity」同源；响应式的容器
  - **11.3 生成前的三个必答问题（Design Context）** `L376` — 1. Target audience：谁用？在什么情境下？
- **12. AI 生成界面的 12 类固有缺陷 → 接回既有专项** `L386` — 本节是索引，不复制规则。每条给出「症状 → 去哪份读 → 自动检查」。
- **13. AI 设计工具链五层地图与选型（GitHub REST API 实测 2026-11-06）** `L407` — 数据由 api.github.com/repos/{owner}/{repo} 实测（凭据经 GET /user 验证）；star 为快照值，许可取 license.spdxid，NOASSERTION 表示非标准/自定义许可，商用前必须自
  - **13.1 选型三问（比 star 更重要）** `L434` — 1. 许可能不能进商业项目？ GPL-3.0 / AGPL-3.0 / NOASSERTION 三个红灯，尤其 AGPL 对 SaaS 有网络交互条款；Apache-2.0 / MIT / BSD-3-Clause 相对安全。
- **14. 生成 → 代码：衔接层与三个陷阱** `L442` — 三个陷阱：
- **15. Prompt 版本化、eval 与 SemVer** `L458` — 官方 eval 纪律（§8.2）：prompt 存代码库 → 类型化输入 → representative fixtures + evaluation checks → feature flag 灰度 → 固定模型快照 → 升级前跑全量 e
- **16. 不确定性与披露：把"可能错"设计出来** `L472` — 1. AI 身份告知（欧盟 Art. 50(1)）：与人直接交互的系统须告知对方在与 AI 交互，除非对合理知情、观察、审慎的人而言显而易见；Art. 50(5) 要求最迟在首次交互/首次暴露时以清晰可区分方式提供，并符合适用无障碍要求。
- **17. 隐私、输入与组织边界** `L483` — - 《暂行办法》第 11 条：不收集非必要个人信息、不非法留存可识别身份的输入与使用记录、不非法向他人提供；须及时受理查阅/复制/更正/补充/删除请求。
- **18. 12 场景速查** `L493` — ---
- **19. 20 条反模式** `L512` — 1. 把合规判断交给模型——AI 会编法条；只认官方原文。
- **20. AI 关 20 项自检（第 6 步新增，逐条可判 PASS/FAIL）** `L537` — 1. 判层：五个位置都标了人工闸门，最终取舍由人做（§1）。
- **21. 6 段可抄代码** `L562` — python
  - **21.1 标识合规 checklist（放进 CI，纯 Python 无依赖）** `L564` — path 保留在签名里是为了接 §21.5 的「导出后元数据存活」抽检；本段只校验要素齐全与 UI 红线，不假装能判断标识是否「显著」——显著性需人工复核（对应 GB 45438-2025 的尺寸/时长要求，本资产不臆造数值）。
  - **21.2 设计 prompt 四区块模板（OpenAI 指南结构）** `L623`
  - **21.3 DESIGN.md 最小可用骨架（九章，第 9 章不可省）** `L659`
  - **21.4 AI 生成界面自动验收（HTML 静态扫描，零依赖）** `L675` — 这是第一道闸门，不替代 axe-core / Lighthouse / 读屏实测；对比度与真实焦点顺序仍需专项检查（accessibility.md §2/§3/§14）。
  - **21.5 元数据存活检查（导出 → 压缩 → CDN 后抽检）** `L708`
  - **21.6 AI 输出 eval 清单（YAML，换模型快照时全量跑）** `L734` — ---
- **22. 数据来源（全部官方原文 / 上游源码 / API 实测）** `L761` — 法规与官方解读

### `references/brand-identity.md` · 品牌视觉与 Logo 逻辑（Brand Identity）
_694 行 · 快照 2026-11-01 · 60 节_

- **1. 一页速查：品牌视觉从零到交付** `L8` — 最短路径（4 小时版）：§3 三个词 → §4 选类型 → §5 用 24 网格画 → §6/§7 定清space与最小尺寸 → §8 选种子色 → §9 跑色阶 → §15 出交付包 → §20 自检。
- **2. 品牌视觉的四层结构（别从 logo 开始）** `L25` — 绝大多数"logo 做得挺好看但整个品牌立不住"的项目，都是跳过了第 1、2 层直接画图。
- **3. 从三个词到视觉：定位翻译表** `L47` — 不可翻译的词（说了等于没说）：专业、高端、国际化、有温度、年轻化、科技感。
  - **3.1 形容词必须"可翻译"** `L49` — 不可翻译的词（说了等于没说）：专业、高端、国际化、有温度、年轻化、科技感。
  - **3.2 六维翻译表（把词变成参数）** `L56`
  - **3.3 三个词的组合纪律** `L67` — - 最多 3 个词，且必须分属不同维度（如"锐利（形）+ 冷静（色）+ 档案感（图）"）。三个词都在"形"维度上 = 只有一个词。
- **4. 标志类型学：七型与选择决策** `L78`
  - **选择决策树** `L90` — 三条硬立场：
- **5. 标志几何构造：网格 / 基形 / 笔画 / 光学修正** `L123` — Material 的图标网格是目前最完整、可直接复用的几何体系（官方原文）：
  - **5.1 用 24 网格画（与图标同源）** `L125` — Material 的图标网格是目前最完整、可直接复用的几何体系（官方原文）：
  - **5.2 光学修正四条（几何正确 ≠ 视觉正确）** `L146` — 1. 圆要溢出：直径 20 的圆与 18 的方看起来才"一样大"。纯几何等宽会让圆显小。
  - **5.3 描边统一纪律** `L155` — - 一个标志里只允许两档笔画：主笔画 + 细节笔画（主 ×0.5 或 ×0.75）。出现第三档就是没控制住。
- **6. 标志清space（安全边距）三口径** `L163` — "清space"= 标志四周不许放任何东西的最小距离。手册里只写"留足空间"等于没写，必须给一个可计算的单位。
  - **6.1 三种主流口径（选一个，写死）** `L167` — 推荐：有图形符号的用「半符号口径」（视觉上最稳，且和 co-branding 间距规则天然一致）；纯字标用「字高口径」。
  - **6.2 落地写法（不要用 margin，用 padding）** `L177` — 四个必须写进手册的数值：top / right / bottom / left 各多少 px（按最小尺寸算一次、按主尺寸算一次）。
  - **6.3 联合品牌（co-branding）间距** `L191` — RIA 官方口径可直接借用：两个 logo 之间 ≥ 各自清space（= 50% 符号直径），理想值 = 1 个符号直径。
- **7. 最小尺寸与响应式标志四档（多小算太小 / 缩小到什么时候换版）** `L198` — 判定公式（比记数字更可靠）：最小可用尺寸 = 最细笔画宽度 ÷ 0.75 px。最细笔画 1.5px 的标志，缩小到笔画不足 0.75px 就开始虚——这时候该换简化版，不是继续缩小。
  - **7.1 最小尺寸（有官方实测值，别再凭感觉）** `L200` — 判定公式（比记数字更可靠）：最小可用尺寸 = 最细笔画宽度 ÷ 0.75 px。最细笔画 1.5px 的标志，缩小到笔画不足 0.75px 就开始虚——这时候该换简化版，不是继续缩小。
  - **7.2 响应式标志四档（一套系统，不是一张图）** `L213` — 切换纪律：
- **8. 品牌色：主色怎么定（不是"选个好看的颜色"）** `L229` — 1. 对比度余量：这个色做按钮底、白字压上去，能过 4.5:1 吗？过不了 → 它只能做装饰色，不能做 primary。
  - **8.1 选色四问（顺序不能反）** `L231` — 1. 对比度余量：这个色做按钮底、白字压上去，能过 4.5:1 吗？过不了 → 它只能做装饰色，不能做 primary。
  - **8.2 品牌色配额** `L240` — 60-30-10 的准确含义：60% 中性底、30% 次级中性/辅助、10% 主色。主色超过 15% 就不再是强调，而是噪音。
- **9. 色阶生成三条路线（选一条，别混）** `L253` — Material 的色彩工具链用 HCT（Hue / Chroma / Tone）：
  - **路线 A · 等感知明度（HCT tone）——最适合"要一套能跑双主题的系统"** `L255` — Material 的色彩工具链用 HCT（Hue / Chroma / Tone）：
  - **路线 B · 12 步语义色阶（Radix 口径）——最适合"要给工程一套不会用错的变量"** `L264` — Radix 每一步对应唯一用途（官方原文，逐条照抄）：
  - **路线 C · 对比度优先（Leonardo 口径）——最适合"必须过无障碍验收"** `L287` — Adobe Leonardo 的核心思想：以目标对比度为输入，反解颜色，而不是"先选色再审计"。
- **10. 品牌色双主题：M3 官方 tone 映射表（亮色/暗色精确值，可直接抄进 token）** `L300` — Material 参考实现（scheme.ts）里亮/暗主题的角色取值，是现成的、经过验证的"品牌色→语义角色"映射：
- **11. 品牌色的边界：图表 / 大屏 / 印刷 / 多品牌** `L342` — 主色是"强调"，分类色是"区分"。用主色做图表分类色会出两个问题：① 与界面强调色抢注意力；② 单色阶无法区分 5 类以上。
  - **11.1 主色不能当图表分类色** `L344` — 主色是"强调"，分类色是"区分"。用主色做图表分类色会出两个问题：① 与界面强调色抢注意力；② 单色阶无法区分 5 类以上。
  - **11.2 大屏（暗底远看）** `L350` — - 暗底上品牌色要提亮 1–2 档（tone +10~20），否则在投影/拼接屏上直接变黑。
  - **11.3 印刷** `L356` — - CMYK 先转再看：屏幕上鲜艳的蓝/绿转 CMYK 后普遍发灰（尤其 RGB 蓝紫），品牌主色必须在 CMYK 里重新校一次。
  - **11.4 多品牌 / 子品牌** `L362` — 纪律：无论哪种结构，图标网格、色阶生成算法、字体授权必须共用一套——共用这三样，视觉上自然像一家人，比强行统一 logo 有效。
- **12. 字体系统：品牌字体与系统栈** `L374` — 两族搭配的唯一硬指标：x-height 接近（差 ≤8%）。x-height 差太多，同一行混排时小写字母会"高低不平"。其次看字重档位是否互补（一族有 Light，另一族至少有 Regular）。
  - **12.1 三档配置（按预算选）** `L376` — 两族搭配的唯一硬指标：x-height 接近（差 ≤8%）。x-height 差太多，同一行混排时小写字母会"高低不平"。其次看字重档位是否互补（一族有 Light，另一族至少有 Regular）。
  - **12.2 品牌字体 vs 系统栈** `L386` — - 品牌字体只用于"品牌露出位"：logo 字标、大标题、封面、海报主张。正文用系统栈——加载成本、中文覆盖率、渲染一致性都更优。
  - **12.3 中文品牌字的三个坑** `L392` — 1. 不要用 500 字重：多数中文字体没有 Medium，浏览器合成伪粗 → 笔画粘连。
  - **12.4 数字必须等宽** `L398` — 价格、统计、表格、倒计时里的数字用 font-variant-numeric: tabular-nums，否则数字列会左右跳动（form-table.md §13 已强调，品牌侧同样适用）。
- **13. 图形语言：图标网格三体系 + 插画五参数** `L404` — 落地纪律：
  - **13.1 图标网格对照（笔画粗细 / 对齐 / 两套已验证体系）** `L406` — 落地纪律：
  - **13.2 插画/纹理/摄影五参数（把"风格"写成可验收的规格）** `L427` — 任何视觉素材（插画、3D、摄影、纹理）都按这五项定义，缺一项就会出现"这次和上次不像"：
- **14. 品牌声音与文案语气（NN/g 四维）** `L443` — 用法（NN/g 原文口径）：
  - **14.1 四个维度（各是一条光谱）** `L445` — 用法（NN/g 原文口径）：
  - **14.2 落地到界面文案** `L460` — - 同一动作在全站只能一种说法：保存 / 提交 / 确认 三选一，不许混。
- **15. 资产交付清单与文件格式** `L469` — SVG 三条硬要求：① 转曲（否则换机器字体就变形）；② 不用 text 元素；③ 跑一遍 SVGO 压体积（logo 通常能压 40–60%，且不损视觉）。
  - **15.1 矢量源（一切的基础）** `L471` — SVG 三条硬要求：① 转曲（否则换机器字体就变形）；② 不用 text 元素；③ 跑一遍 SVGO 压体积（logo 通常能压 40–60%，且不损视觉）。
  - **15.2 位图与平台图标** `L484` — Apple HIG 的三条明确要求：图层必须是未遮罩的正方形（自己切圆角会破坏高光效果并产生锯齿）；文字只在必要时代替（不支持无障碍与本地化，不要重复 App 名，禁止 "Watch/Play/New" 这类指令或情境词）；iOS 需考虑 
  - **15.3 品牌手册（两种体量）** `L499` — 一页式（One-pager）：标志 + 清space + 最小尺寸 + 色值表 + 字体 + 3 条 do/don't。适合小团队、外包对接。
- **16. 品牌一致性的十条检查（交付前逐条过）** `L506` — 1. 主色在亮/暗两个主题下都过对比度（文字 4.5:1、非文本 3:1）。
- **17. 商标与授权合规（不做这步，前面全白做）** `L521` — 最容易踩的坑：以为"我画的 logo 就是我的商标"。不注册 = 没有商标权，别人在同类上注册了，你可能要改标。
  - **17.1 商标 ≠ 版权（两件事）** `L523` — 最容易踩的坑：以为"我画的 logo 就是我的商标"。不注册 = 没有商标权，别人在同类上注册了，你可能要改标。
  - **17.2 类别（尼斯分类 1–45 类）** `L534` — - 1–34 类 = 商品，35–45 类 = 服务。
  - **17.3 素材授权链（四项必查）** `L541` — 开源图标库的实测许可（2026-11-01 GitHub API）：
- **18. 可抄代码** `L557` — html
  - **18.1 标志清space + 响应式四档** `L559`
  - **18.2 单色标志跟随文字色** `L579`
  - **18.3 品牌色双主题（tone 映射，不是反色）** `L591`
  - **18.4 favicon / manifest 最小套件** `L608` — ---
- **19. 反模式 20 条** `L625` — 1. 从 logo 开始做品牌，定位一句话说不出来。
- **20. 自检 18 项（交付前逐条打勾）** `L650` — 1. 能说出 3 个形容词 + 3 个反义词，且每个词能落到 §3.2 六维表的 ≥2 个维度？
- **21. 数据来源** `L673` — 官方规范 / 源码（逐字核对）

### `references/chinese-design.md` · 中文设计场景 — Chinese Design（排版规范 + 生态地图）
_195 行 · 快照 2026-10-29 · 14 节_

- **一、中文排版：为什么不是"英文换字"** `L10` — 对照英文：英文正文 16px / 1.5 就够；中文同样 16px 需要 1.7–1.8 才不压抑。直接沿用英文行高是中文排版最常见的错误。
  - **1.1 三个根本差异** `L12`
  - **1.2 字号与行高（关键差异表）** `L20` — 对照英文：英文正文 16px / 1.5 就够；中文同样 16px 需要 1.7–1.8 才不压抑。直接沿用英文行高是中文排版最常见的错误。
  - **1.3 中文字体族栈（可直接用）** `L32` — 衬线 vs 无衬线：中文正文用无衬线（黑体）更清晰；宋体适合长文阅读、文化/出版调性、大标题。混用两套中文衬线/无衬线是灾难，最多 1 套中文 + 1 套西文。
  - **1.4 字重陷阱（中文特有）** `L57` — - 中文字体普遍缺 500（Medium）档，font-weight: 500 会被渲染成 400 或伪粗体（faux bold）——笔画糊、边缘脏。
  - **1.5 标点与避头尾（clreq 核心规则）** `L64` — 全角标点：中文标点占一个汉字宽（全角）。，。；：？！「」『』（）《》 等。
  - **1.6 行长（中文按字数算）** `L102` — 换算：中文 1 字 ≈ 2 个西文字符宽，所以 max-width: 36em（英文标准）对中文约等于 36 字，在舒适区间内。但中文正文用 max-width: 40em 时行长约 40 字，已接近上限。
  - **1.7 竖排（了解即可）** `L112` — writing-mode: vertical-rl 支持中文竖排，但：
- **二、中文设计生态地图（平台怎么用、哪里有坑）** `L121` — Dribbble 使用纪律（重要）：看到喜欢的 shot，问三个问题再决定要不要借鉴——
  - **2.1 六个核心平台（用户指定清单）** `L123`
  - **2.2 补充平台（按需扩展）** `L134`
  - **2.3 检索策略（按需求类型直接跳）** `L146` — Dribbble 使用纪律（重要）：看到喜欢的 shot，问三个问题再决定要不要借鉴——
- **三、中文产品形态的四个特征（影响设计决策）** `L167` — 中后台 vs 消费级的分野：
- **四、中文排版自检清单（交付前逐条过）** `L182` — - [ ] 正文字号 ≥14px（内容页 ≥16px），行高 ≥1.6

### `references/color-science.md` · 色彩科学（Color Science for Designers）
_399 行 · 快照 2026-11-07 · 24 节_

- **1 · 为什么单列色彩科学** `L9` — 配色不是纯审美，是一组有最优解的计算：
- **2 · 色彩模型谱系（先认坐标，再谈配色）** `L21` — 核心结论：凡是要「生成 / 插值 / 比较亮暗」的操作，走 OKLab/OKLCH；只在「给人类看一个直观旋钮」时用 HSL。
- **3 · 感知均匀性：HSL 为什么撒谎** `L37` — HSL 的「L」是相对亮度（亮底上才亮），不是感知亮度。后果：
- **4 · 伽马（gamma）：为什么不能直接对 sRGB 插值** `L49` — sRGB 存储的是经过伽马编码的值（V = 1.055·L^0.4167 − 0.055），不是线性光。直接对两个 sRGB 十六进制做线性插值，等于在「编码后的非线性刻度」上取中点——中间会发灰、发脏、偏暗。
- **5 · OKLab / OKLCH：公式与用法** `L59` — Björn Ottosson（2020）公开公式，已成为 CSS Color 4/5 与主流设计工具的实践标准。
- **6 · 对比度：两套算法，不是只有 WCAG 2.x** `L104` — 相对亮度：
  - **6.1 WCAG 2.x 相对亮度（现行强制标准）** `L106` — 相对亮度：
  - **6.2 APCA（WCAG 3 候选，长文/暗色更准）** `L121` — APCA 用 Lc（感知亮度对比，可正可负，符号表文字/背景关系），不分「正文/大文本」一刀切，而是按文本尺寸与权重给分档：
- **7 · 色盲：三型 + Okabe–Ito 8 色** `L143` — 约 8% 男 / 0.5% 女有某种色觉缺陷。三型：
- **8 · 色板生成科学：四条可复现路线（选一不许混）** `L162` — 混用不同路线会导致色阶错序（如第 9 档比第 10 档还亮），必须选一条：
- **9 · 渐变与插值：在 OKLab 空间做** `L175` — sRGB 直插 → 中间发灰发脏（§4）。正解：
- **10 · 色彩无障碍 beyond 1.4.11** `L194` — - 不只靠颜色单通道：错误 = 红 + 图标 + 文案；状态 = 颜色 + 形状 + 文字；涨跌 = 颜色 + 符号。色盲与「看不清颜色」用户都要能读（WCAG 1.4.1）。
- **11 · 工程实现（落地要点）** `L204` — 现代 CSS（2023–2024 可用，原生无依赖）：
- **12 · 场景速查（12）** `L234` — 1. 生成一套浅→深主色阶 → OKLCH 固定 H、L 从 95%→30% 步进（§8 路线 1）。
- **13 · 反模式（20）** `L251` — 1. 在 HSL 里转色相生成色板（错序、重量不均）。
- **14 · 自检（20）** `L276` — 1. 色板是在 OKLCH/OKLab 生成的，不是 HSL 旋转？
- **15 · 可抄代码（6 段）** `L301` — css
  - **15.1 CSS · OKLCH 生成浅→深主色阶** `L303`
  - **15.2 CSS · OKLab 渐变（干净过渡）** `L318`
  - **15.3 JS · WCAG 2.x 相对亮度 + 对比度（可直接用）** `L325`
  - **15.4 JS · 简化 APCA（Lc）计算（以官方 Lookup 为准校准）** `L346`
  - **15.5 Python · OKLCH 色相旋转生成分类色板（culori）** `L360`
  - **15.6 Python · 反解「过 4.5:1 的最深主色」（对比度优先思路）** `L374` — 15.4/15.5/15.6 为思路骨架：APCA 用官方常量校准（§6.2 取源限制），culori 以其实 API 为准；15.3 为完整可用实现。
- **16 · 取源与限制（公开记录）** `L392` — - 已吸收并交叉验证：OKLab/OKLCH 公式（Björn Ottosson 2020 公开）、WCAG 2.1 相对亮度公式与阈值、Okabe–Ito 8 色 hex、sRGB γ 编码与线性化、Display P3 比 sRGB 宽

### `references/component-api-design.md` · 组件 API 设计与组合模式：状态所有权、渲染所有权、契约可演进
_917 行 · 快照 2026-11-07 · 42 节_

- **0. 与既有资产的分层（先判该读哪份）** `L9` — 缺口证据（升级前实测）：dpsearch.py "组件 API 设计 组合模式 props 语义 受控 非受控" 最高命中仅 handoff-collaboration.md §7 组件 API 与设计稿 1:1 对齐（40.0 分）与 d
- **1. 组件 API 设计：三份所有权与三条不可商量的原则（先给立场，不和稀泥）** `L25` — 1. 状态只有一个所有者。同一份值不能既在组件内部 useState 又在父级 props 里；React 官方把组件分为 controlled（"important information is driven by props"）与 un
- **2. 受控 / 非受控：唯一真相源（React 官方定义 + Radix 上游源码）** `L42` — React Sharing State Between Components 的口径：controlled 组件是「重要信息由 props 驱动」，uncontrolled 是「由自身 local state 驱动」；结论是 single 
  - **2.1 官方定义与三元组** `L44` — React Sharing State Between Components 的口径：controlled 组件是「重要信息由 props 驱动」，uncontrolled 是「由自身 local state 驱动」；结论是 single 
  - **2.2 Radix useControllableState 的四条硬规则（上游源码逐字）** `L56` — 取自 radix-ui/primitives → packages/react/use-controllable-state/src/use-controllable-state.tsx（官方 controlled-state 文档 URL
  - **2.3 React <input 五条门禁（官方原文）** `L100` — 1. value / checked + onChange 必须同步更新 backing value，否则输入被「弹回」。
  - **2.4 PASS / FAIL 判定表** `L108` — ---
- **3. 状态提升与派生状态（别把 state 复制两份）** `L122` — - 共同父级原则：把 state 放到「所有需要它的组件的最近共同祖先」，再通过 props 下传；不要在两个兄弟组件各存一份再想办法同步。
- **4. 组合 vs 继承：多个「洞」怎么开（React + Vue 对照）** `L133` — React legacy 官方 Composition vs Inheritance 给了两级结构（该页明确标注 "These docs are old and won't be updated. Go to react.dev"，故只取可
- **5. 五种「换元素」API 的完整对照（选型先看这个，别看 star）** `L158`
  - **5.1 Radix asChild 的合并规则（slot.tsx 上游源码逐字）** `L168` — 官方口径：所有会渲染 DOM 元素的 Radix primitive part 都接受 asChild；组合自定义组件时 "Your component must spread props" 与 "Your component must f
  - **5.2 Ariakit render 的合并规则（官方原文）** `L204` — "The style, className, ref and event props will be automatically merged. In all other cases, defined rendered element pr
  - **5.3 MUI component / slots / slotProps（官方口径）** `L217` — - component：只覆盖 root slot，且保留该 slot 的样式（这是与 slots 最关键的区别）。
  - **5.4 选型决策树** `L225` — ---
- **6. 「自定义组件必须开放扩展」四条硬规则（Radix + Ariakit 共识）** `L240` — Ariakit 官方章节标题就是 "Custom components must be open for extension"，原文："it should pass the incoming props, including event l
- **7. props 合并优先级：一张能判 PASS/FAIL 的算子表** `L274` — 把 §5–§6 的三套规则统一成合并算子（slot = 组件库内部算出来的 props，child = 使用方传进来的 props）：
- **8. 复合组件 / Compound Components 与状态共享** `L295` — - 定义：<Tabs + <Tabs.List + <Tabs.Tab + <Tabs.Panel 这类由多个 part 组成的组件，状态（当前 tab）由 root 通过 context 下发，part 只负责渲染与交互。
- **9. ref 与命令式 API：React 19 反陈旧裁决（本轮第二重要的裁决）** `L308` — React forwardRef 参考页顶部现在挂着 ### Deprecated，逐字：
  - **9.1 官方现行口径** `L310` — React forwardRef 参考页顶部现在挂着 ### Deprecated，逐字：
  - **9.2 命令式 handle 的准入清单** `L333` — 可以做（官方列举的 imperative behaviors）：滚动到节点、聚焦节点、触发动画、选中文本——这些都是「无法用 props 表达」的浏览器副作用。
  - **9.3 ref cleanup 与 TypeScript 连带变化（React 19）** `L343` — - 现在 ref callback 可以返回 cleanup function，卸载时 React 调用它；对 DOM ref、class ref、useImperativeHandle 都生效。
- **10. 组件契约的最小字段集（API surface，可直接当评审表）** `L353` — 以 Radix Switch 官方 API 为范例（逐字字段名与默认值）：
- **11. 回调契约：onChange 到底承诺了什么** `L384` — Vue 的一条硬提醒（官方 props 页）：props 是 one-way-down，子组件不得直接 mutate；对象 / 数组类型的 prop 虽然技术上能改嵌套字段，但同样破坏单向流且难以追踪。v-model 是「语法糖 + 显式 
- **12. 无障碍不是 props 的附属品：键盘契约在 API 层怎么落** `L399` — WAI-ARIA APG Developing a Keyboard Interface 的硬要求（官方原文口径）：
- **13. 状态暴露：别把 9 态做成 9 个布尔 props** `L422` — 判定：一个组件公开的布尔 props 若 5 个，基本可以断定它把内部状态当成了配置项。回到 §1 原则 1——状态只有一个所有者，内部状态不该有第二个出处。设计侧的「9 态矩阵」（default / hover / focus / act
- **14. API 版本化：组件特有的破坏性判级（改默认值 = MAJOR 的延伸）** `L435` — 沿用 handoff-collaboration.md 的 SemVer 11 条，本轮补组件 API 特有的判级表：
- **15. Storybook argTypes：把 API 契约变成机器可读、可在 CI 校验的东西** `L458` — 官方 Controls 文档口径（/docs/essentials/controls；/docs/api/argtypes 返回 404，规范链接为 /docs/api/arg-types，见 §22）：
  - **15.1 把 §10 十类字段映射到 argTypes** `L467`
  - **15.2 三条可直接执行的裁决** `L480` — 1. control: false ≠ table.disable：前者保留文档、只关控件，后者连文档一起删。组件库里 ref、asChild 内部结构、内建 aria 注入应走 control: false——文档要能被查到，但不能被当成
- **16. 类型即文档：TypeScript 契约的四条底线** `L490` — 1. 原生属性用 ComponentPropsWithoutRef<'button'（或 Vue 的 attrs 透传）继承，不要逐条手抄 disabled / type / title / aria-——抄不全就是 §6 的 FAIL。
- **17. 16 场景决策矩阵（先查表，再动手）** `L501` — ---
- **18. 20 条反模式（逐条可判 FAIL）** `L524` — 1. value 给了却没给 onChange → 输入框只读，用户以为坏了。
- **19. 22 项上线自检（组件 API 关）** `L549` — - [ ] 1. 每个有状态的组件都说得出「谁持有这个值」，且只有一处 useState / props 之一？
- **20. 可抄代码（3 段 Python 已实跑，含双用例断言）** `L576` — 把 §2 / §6 / §9 / §13 / §18 的红线做成可进 CI 的检查。输入是组件源码文本，输出 (rule, line, message) 列表；FAIL 级别即门禁不通过。
  - **20.1 componentapilint.py — 组件 API 契约静态检查（已实跑）** `L578` — 把 §2 / §6 / §9 / §13 / §18 的红线做成可进 CI 的检查。输入是组件源码文本，输出 (rule, line, message) 列表；FAIL 级别即门禁不通过。
  - **20.2 mergeprops.py — 可执行的两套合并算子（已实跑）** `L656` — 复刻 Radix mergeProps 语义，并加 Ariakit render 元素形态的 undefined / null 规则。组件库写自己的组合层时可直接拿去对照。
  - **20.3 apisemver.py — 契约 diff 与 MAJOR 门禁（已实跑）** `L761` — 把 §14 的判级表做成可执行脚本：输入新旧两份 API 契约，输出版本级别与变更清单。MAJOR 必须附带 codemod 路径，否则 CI 拒绝发版。
  - **20.4 Storybook 契约模板（TS，可抄）** `L819` — 把 §15 的裁决落成一份可直接用的 meta：必填项排前、内部项保留文档但关控件、高级项条件折叠。
- **21. 取源清单与 GitHub API 实测（2026-11-07 快照）** `L856` — 选型三问（沿用 ai-design-toolchain.md 的口径，比 star 更重要）：① 许可——NOASSERTION / None 需人工复核后再用于商业项目；② 活源——tailwindlabs/headlessui 的 pu
  - **21.1 官方原文（逐字口径来源）** `L858`
  - **21.2 GitHub REST API 实测（15 仓库，GET /repos/{owner}/{repo}，2026-11-07）** `L879` — 选型三问（沿用 ai-design-toolchain.md 的口径，比 star 更重要）：① 许可——NOASSERTION / None 需人工复核后再用于商业项目；② 活源——tailwindlabs/headlessui 的 pu
- **22. 取源限制与不臆造声明（本轮公开记录）** `L903` — 1. Radix controlled-state 文档 URL 返回 404：https://www.radix-ui.com/primitives/docs/guides/controlled-state 页面为 # 404 / Thi

### `references/component-libraries.md` · 组件库与设计 GitHub 地图 — Component Libraries
_37 行 · 快照 2026-10-29 · 3 节_

- **元素覆盖矩阵** `L5`
- **组件库选型规则** `L24` — - 要"复制类名就用"（无 JS 依赖）：HyperUI TailGrids daisyUI Meraki UI
- **维护协议** `L34` — - 快照：2026-10-29。任何条目链接失效或用户报告质量下降时：先 GitHub API 复核该库（star/推送/许可），再决定降级或替换，并在本文件更新快照日期。

### `references/content-findability.md` · 内容可发现性与可扫读性（Content Findability / Search UX / Scannability）
_956 行 · 快照 2026-11-09 · 32 节_

- **1 · 为什么单列「内容可发现性」** `L19` — 39 份参考里，「搜索体验 / 内容可发现性」没有独立资产。缺口用 dpsearch.py 与全域词频统计判定为结构性空白，不是覆盖不足。
- **2 · 四层链路模型：先判哪一层断，再谈改文案** `L31` — 任何「找不到 / 搜不到 / 看不下去 / 用户流失」的问题，先判落在哪一层。
- **3 · 裁决一：SC 2.4.5 是「至少两条路」，不是「有个搜索就行」** `L46` — W3C《Understanding SC 2.4.5 Multiple Ways》（Level AA）逐字：
- **4 · 搜索入口的可发现性：位置、形态、宽度** `L66` — NN/g《Search: Visible and Simple》（Jakob Nielsen, 2001-05-12）是本节的实证底座，以下数值均来自该文正文：
- **5 · 搜索框的标签契约：placeholder 不是 label** `L87` — 「把 placeholder 当 label 用」「输入提示一打字就消失」「表单可访问性过不了关」——这三种真实投诉都落在同一处：搜索框的标签契约。三条 W3C 准则在这一处交汇：
- **6 · APG combobox 契约：自动补全不是「弹个下拉」** `L99` — W3C《ARIA Authoring Practices Guide — Combobox Pattern》逐字契约，本轮核验：
- **7 · 联想、筛选与结果：第一次查询基本就是决战** `L130` — NN/g《Search: Visible and Simple》的电商研究数值（同一段落逐字）：
- **8 · 决策一图流：从入口到死胡同** `L151` — ---
- **9 · 信息气味：一个相对量，不是一个形容词** `L173` — NN/g《Information Scent: How Users Decide Where to Go Next》（Raluca Budiu, 2020-02-02）逐字定义：
- **10 · 裁决二：链接目的的 WCAG 契约族（五条准则）** `L198` — 2.4.4 的「可程序化上下文」到底是什么：Key Terms 定义 "additional information that can be programmatically determined from relationships wi
- **11 · 可扫读性：79% / 16% 与 124% 的原文口径** `L220` — NN/g《How Users Read on the Web》（Jakob Nielsen, 1997-09-30）逐字：
- **12 · nano-content：前 11 个字符决定要不要读下去** `L245` — NN/g《First 2 Words: A Signal for the Scanning Eye》（Jakob Nielsen, 2009-04-06）：
- **13 · 「Learn More」的三种改法与信息气味的重合** `L272` — NN/g《"Learn More" Links: You Can Do Better》（Katie Sherwin, 2015-12-13）Summary 逐字："The phrase 'Learn More' is increasingl
- **14 · 裁决三：阅读等级的合规门槛是「九年学校教育」** `L288` — 「Flesch / FKGL / SMOG 算到多少分才算合规？」——先记住裁决：分数不是合规门槛，SC 3.1.5 要的是「九年学校教育」。W3C《Understanding SC 3.1.5 Reading Level》（Level A
- **15 · 三条可读性公式、精确系数与「不可换算」** `L310` — 以下系数来自 ReadabilityFormulas.com 两个逐字核验页（Brian Scott，2025-11-14 / 2025-02-07），解释表与限制来自 Wikipedia《Flesch–Kincaid readabilit
- **16 · 中文可读性：音节公式失效，改用可解释的代理指标** `L346` — 为什么不能直接套：FRE / FKGL / SMOG 的输入全是「英文音节数 / 英文词数」。中文一字一音节，词边界需分词，成语与专业术语的难度不随字数线性增长；把 ASW 硬套到中文几乎恒为 1.0，公式会退化成纯句长函数，输出数值看似精
- **17 · 简明语言：Plain Writing Act 与四份官方指南** `L365` — Digital.gov《Plain language guide series》（内容改编自 PlainLanguage.gov）逐字：
- **18 · L4 死胡同治理：零结果与 404** `L379` — 零结果不是「没有结果」四个字。NN/g 的数据说明它代价极高：首次查询失败后 "almost half the users whose first search failed gave up immediately"，第二/三次成功率掉到 
- **19 · 多条路径与当前所在指示的落地清单** `L398` — L4 的位置感（SC 2.4.8）与 L1 的多条路径（SC 2.4.5）合并为一张落地清单，逐项标明权威依据与归属资产：
- **20 · 可发现性的度量：tree testing 与 findability** `L415` — NN/g《Tree Testing: Evaluate Menu Labels and Categories》（Page Laubheimer, 2023-08-06，Last reviewed 2026-08-19）逐字定义：
- **21 · 六步构建流程** `L439` — 1. 盘路径（L1）：列出目标页全部可达路径，确认 ≥2 条互不依赖（§3 §19），标出流程产物例外页。
- **22 · 与既有资产的边界矩阵** `L450` — ---
- **23 · 场景速查（12）** `L467` — 1. 「我们网站有搜索啊，为什么还说我不可访问」 → §3 SC 2.4.5 要 ≥2 条；搜索只算 G161 一条，补目录/站点地图/全页链接。
- **24 · 反模式（20）** `L484` — 1. 把「有搜索框」当成满足 SC 2.4.5。
- **25 · 自检（20）** `L509` — 1. 目标页有 ≥2 条互不依赖的可达路径，且没有把流程产物例外扩大到全站？
- **26 · 可抄代码（5 段；§26.1–§26.3 为 Python，本轮已实跑 PASS）** `L534` — python
  - **26.1 英文可读性计算器 + 中文守卫（Python，已实跑）** `L536` — 本轮实跑输出（python 执行，非手写）：
  - **26.2 链接文本静态扫描器（Python，已实跑）** `L618` — 本轮实跑输出：
  - **26.3 可发现性契约静态检查器（Python，已实跑）** `L713` — 本轮实跑输出：
  - **26.4 符合 APG 契约的搜索框骨架（HTML，契约示意）** `L838`
  - **26.5 中文可扫读代理指标（JS，工程约定）** `L872` — const clean = text.replace(/ /g, '');
- **27 · 取源与限制（公开记录）** `L908` — W3C / WAI（本轮逐页逐字核验）：Understanding WCAG 2.2 的 link-purpose-in-context.html（SC 2.4.4 A，含 Key Terms、16 项 Sufficient、F63/F89

### `references/conversational-generative-ui.md` · 对话式与生成式界面：流式输出、混合界面与可纠错契约
_747 行 · 快照 2026-11-11 · 31 节_

- **0. 一句话立场与三条裁决** `L10` — 对话式与生成式界面（Conversational & Generative UI）不是「把聊天气泡套个皮」，而是一条五段并存且每一段都会失败的链路：发得出 → 等得住 → 读得动 → 改得动 → 收得回；任何一段没建模，界面就会在「模型正在
- **1. 为什么这是结构性空白（缺口实测）** `L24` — 结构性空白是指：不是覆盖不足，而是全域没有独立资产，检索会把问题路由到完全不相干的文件。本轮用 scripts/dpsearch.py 与全域词频实测（v35 基线，41 份参考）判定。
- **2. 五段链路判层模型（L1 发得出 → L5 收得回）** `L43` — 先判问题落在哪一段，再动手改界面；一上来改气泡样式是典型的判层失败。
- **3. 裁决一：流式文本不是状态消息，状态边界才播报（SC 4.1.3 逐字）** `L59` — WCAG 2.2 SC 4.1.3 Status Messages (Level AA) 规范条文逐字：
- **4. ARIA23 role=log 与隐性 aria-live=polite / aria-atomic=false** `L92` — W3C Technique ARIA23《Using role=log to identify sequential information updates》是 SC 4.1.3 Situation C 的充分技术（Techniques a
- **5. 聊天界面播报工程契约：chatbot 流式输出的状态边界（空容器、aria-busy、aria-relevant、assertive 双播）** `L118` — 以下为工程约定（规范未强制逐条），但每条都能追溯到官方机制，验收时按此清单过：
- **6. 裁决二：生成式界面 streamUI 是组件白名单里的路由，不是任意组件** `L137` — Vercel AI SDK RSC《Streaming React Components》官方原文逐字：
- **7. AI SDK RSC experimental 与生产推荐路径（口径不张冠李戴）** `L182` — RSC 文档页首逐字（这句话只在这一页）：
- **8. useChat 四态状态机与 message.parts（parts 不是 content）** `L207` — AI SDK UI Chatbot 官方对 useChat 的定位逐字：
- **9. AG-UI 对话状态机：RunStarted / RunError / TextMessageStart 与 messageId 归属** `L240` — AG-UI（Agent-User Interaction Protocol）官方逐字：
- **10. Hybrid UI 混合界面与 RICH 范式（WIMP 不是唯一解）** `L282` — Ant Design X 官方 RICH 设计范式四要素：Intention（意图）、Role（角色）、Conversation（会话）、Hybrid UI（混合界面）。其官方立场是：AI 对话不是要取代 WIMP（Window / Ico
- **11. 裁决三：AI 答错了要高效纠错（HAX G9）——四档恢复链，不是重新生成按钮** `L302` — Microsoft HAX Design Library G9 逐字：
- **12. stop / regenerate / setMessages 与状态边界播报一次（含清空队列）** `L337` — 把 §11 落成事件-动作对照，供实现直接抄：
- **13. 状态归位表：每个动作后哪些状态必须复位** `L358` — 收口（L5）是「模型输出不确定」带来的特有缺陷域：传统界面状态由用户操作驱动，AI 界面状态由远端事件驱动，事件丢失就永久错位。
- **14. 流式渲染工程：增量 Markdown、未闭合块、节流、自动滚动纪律** `L378` — 流式 Markdown 不是「把字符串拼起来交给 renderer」——任意切分点都可能落在代码块、表格、链接、加粗标记中间。§20 代码 3 实跑证明：同一段含代码围栏的 Markdown，按 7 / 13 / 29 字符切分，处于未闭合
- **15. L1 输入与发送：Enter / Shift+Enter、禁用提交、队列、中文场景** `L391` — ---
- **16. 来源、引用与置信度呈现（与 HAX 18 条的边界）** `L405` — 本文件不重列 HAX G1–G18，但要把三条界面落点说清，避免与 ai-design-toolchain.md §10 互相抢路由：
- **17. 12 个高频场景速查** `L417` — ---
- **18. 反模式 20 条** `L436` — 1. 把每个 token 塞进 aria-live="assertive" —— 官方 Failure 族 + chatty 风险。
- **19. 自检 20 项（交付前逐条过）** `L461` — 1. [ ] 对话容器是 role="log" 且有 accessible name？隐性 polite / atomic=false 有没有被手动改坏？
- **20. 可抄代码 5 段（3 段 Python 实跑，输出为本轮实测）** `L486` — 校验 RunStarted / RunError 生命周期边界、Start-Content-End 三元组闭合、messageId 归属。
  - **代码 1 · AG-UI 事件流校验器（Python，实跑）** `L488` — 校验 RunStarted / RunError 生命周期边界、Start-Content-End 三元组闭合、messageId 归属。
  - **代码 2 · live region 契约扫描器（Python，实跑）** `L546` — 静态扫描 role=log / role=status / assertive 滥用 / aria-busy 未复位。
  - **代码 3 · 流式 Markdown 分片鲁棒性（Python，实跑）** `L584` — 证明任意切分点会落在未闭合围栏内，必须 hold。
  - **代码 4 · 生成式 UI 组件白名单分派（TypeScript / React）** `L610`
  - **代码 5 · 对话容器的无障碍骨架（HTML）** `L639` — ---
- **21. GitHub API 实测仓库（2026-11-11 经 GitHub API）** `L666` — star / license / pushedat / archived 均为本轮 api.github.com/repos/... 实测，不凭记忆写数字；NOASSERTION 表示 GitHub 未检出明确 SPDX，不代表「无许可」。
- **22. 与其他资产的边界（避免重复与抢路由）** `L684` — ai-design-toolchain.md 的分流表已同步修正：原则层（HAX 18 条）仍归该文件，链路层（流式 / 混合界面 / 纠错）归本文件。
- **23. 取源限制（公开记录，不臆造）** `L702` — 1. W3C WAI-ARIA 1.2 TR #log 被 Cloudflare 拦截：只返回 Just a moment...，未取得 normative definition / Superclass Role / Implicit V
- **24. 数据来源清单** `L715` — - W3C WCAG 2.2 Understanding SC 4.1.3 Status Messages — https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html
- **25. 术语与口径速记** `L732` — ---

### `references/dark-mode.md` · 暗色模式体系（Dark Mode System）
_656 行 · 快照 2026-11-01 · 47 节_

- **1. 先决定：该不该做暗色（含反面证据）** `L13` — NN/g 的 Raluca Budiu 综述了学界研究，结论不利于"暗色默认"：
  - **1.1 NN/g 的证据链（与直觉相反，必须先知道）** `L15` — NN/g 的 Raluca Budiu 综述了学界研究，结论不利于"暗色默认"：
  - **1.2 但暗色确实有不可替代的场景** `L29`
  - **1.3 决策树** `L40` — 三条硬规矩：
- **2. 表面层级：暗色的核心是"重排"，不是"反相"** `L58` — 亮色模式里，#fff 背景 + 阴影 = 高度。暗色模式里，阴影在深底上几乎不可见，所以必须换一种信号：表面越靠前，颜色越亮。这就是 M2 的 elevation overlay、M3 的 surface container tone、An
  - **2.1 为什么不能反相（一句话原理）** `L60` — 亮色模式里，#fff 背景 + 阴影 = 高度。暗色模式里，阴影在深底上几乎不可见，所以必须换一种信号：表面越靠前，颜色越亮。这就是 M2 的 elevation overlay、M3 的 surface container tone、An
  - **2.2 Material 3：tone 全表（源码逐字，非二手）** `L67` — 来源：material-color-utilities/typescript/dynamiccolor/colorspec2021.ts + scheme/scheme.ts。
  - **2.3 Ant Design：暗色是"黑底 + 白 alpha 提亮"** `L88` — 来源：components/theme/themes/dark/colors.ts，colorBgBase='#000'，getSolidColor = lighten(brightness)。
  - **2.4 Carbon：g100 的 layer 阶梯（hex 全部来自 @carbon/colors 11.61.0 包内源码）** `L103` — Carbon 灰阶（实测取值）：gray10 #f4f4f4 · gray20 #e0e0e0 · gray30 #c6c6c6 · gray40 #a8a8a8 · gray50 #8d8d8d · gray60 #6f6f6f · gr
  - **2.5 选底色的三种做法与取舍** `L124` — M2 的原话立场：默认用深灰 #121212 而非纯黑，因为"深灰能表达更丰富的色彩、高度和深度，因为阴影在灰色上比在黑色上更易看见"；纯黑只留给"需要高效省电的产品"。
- **3. 文字：暗色下不能用纯白（暗色对比度与文字层级）** `L141` — 原因：亮色文字在深底上会因光渗（halation）在视觉上"发胖"、边缘扩散，纯白尤其明显；同时纯白 + 纯黑是 21:1 的极端对比，长时间阅读反而更累。降到 tone 90 档既保住可读性，又削掉晕光。
  - **3.1 四家体系的"不用纯白"是共识（可验证）** `L143` — 原因：亮色文字在深底上会因光渗（halation）在视觉上"发胖"、边缘扩散，纯白尤其明显；同时纯白 + 纯黑是 21:1 的极端对比，长时间阅读反而更累。降到 tone 90 档既保住可读性，又削掉晕光。
  - **3.2 Ant Design 四档文本透明度 + 实测对比度（重点看第三档）** `L154` — 这张表暴露了两个真实陷阱：
  - **3.3 文字层级推荐表（可直接抄）** `L169` — 中文字体的额外注意：中文笔画细密，暗底上光渗更明显。同一字号下，中文在暗色里的可读性下降比拉丁文更快。暗色下中文正文建议：行高 +0.05~0.1、字重不降、字号不小于 14px；12px 中文在暗色里几乎不可读（NN/g 的"字号越小浅色
- **4. 边框与分隔线：暗色下不可依赖** `L183` — 这意味着：抄 Ant 的暗色边框（#424242）做输入框描边，不满足 WCAG 2.2 SC 1.4.11（非文本对比 3:1）——因为输入框边界是"识别控件所必需"的。Carbon 用 ui04（gray60）就达标。
  - **4.1 实测：主流暗色的边框都不达 3:1** `L185` — 这意味着：抄 Ant 的暗色边框（#424242）做输入框描边，不满足 WCAG 2.2 SC 1.4.11（非文本对比 3:1）——因为输入框边界是"识别控件所必需"的。Carbon 用 ui04（gray60）就达标。
  - **4.2 三条规则** `L195` — 1. 表单控件边界必须 ≥3:1。用 #6f6f6f 起步，不要用 #424242。
- **5. 阴影与高度：两派做法与正确用法** `L203` — 怎么选：
  - **5.1 两派（存在真实分歧，不要以为只有一种对）** `L205` — 怎么选：
  - **5.2 高度与表面值的对照（把两套合成一张表）** `L216` — 注意 §3 的连带影响：表面越亮，白字对比越低。#424242 上的白字只有 10.05、85% 白只有 7.83——仍达标，但如果再往上提（比如 #525252，白字 7.81），就要检查正文 4.5:1 是否还成立。M2 的原始约束就是
- **6. 品牌色与语义色：降饱和，不是反相** `L230` — - 不要用高饱和色做暗色主题的主色。原因两条：过不了 AA 4.5:1；在深底上产生光学振动（optical vibration），加剧眼疲劳。
  - **6.1 M2 的精确规则（可直接执行）** `L232` — - 不要用高饱和色做暗色主题的主色。原因两条：过不了 AA 4.5:1；在深底上产生光学振动（optical vibration），加剧眼疲劳。
  - **6.2 M3 的做法：不是"取 200 阶"，是"tone 重映射"** `L240` — 两处易错点（源码实测，别自作聪明"对称化"）：
  - **6.3 中国特色：涨跌色在暗色下必须重调** `L260` — A 股/中文金融场景的红涨绿跌在暗色下有两个坑：
- **7. 图像、插画、图标** `L273` — - "Soften the color of white backgrounds"：内容图里带白底的，暗色下要轻微压暗，否则白底在深色界面里"发光"。
  - **7.1 Apple 的明确要求** `L275` — - "Soften the color of white backgrounds"：内容图里带白底的，暗色下要轻微压暗，否则白底在深色界面里"发光"。
  - **7.2 Web 落地规则** `L282`
  - **7.3 一张必查清单（图片在暗色里的四个死法）** `L293` — 1. 白底图 → 发光（压暗 + 边框）
- **8. 状态与交互反馈在暗色下的差异** `L302` — Focus 环在暗色的具体值：GOV.UK 的 #FFDD00 焦点黄在深底上依然可用（黄在暗色里对比极高），但内圈必须配深色（#0B0C0C）形成双色环。或者用主色 tone 80 的 2px 环 + 2px offset。完整焦点三件套
- **9. 切换实现：四端与防闪白** `L318` — html
  - **9.1 Web：三件事必须一起做** `L320` — MDN 明确的三点：
  - **9.2 防闪白（FOUC）：唯一正确顺序** `L355` — 内联脚本必须在 CSS 之前、且不能 defer。Tailwind 官方示例也是这个思路（"best to add inline in head to avoid FOUC"）：
  - **9.3 三态切换的存储约定** `L373` — 删除键 vs 存 "system"：删键能让"用户从未选择过"和"用户主动选了跟随系统"在逻辑上合并，少一个分支。若要支持"系统主题变化时实时跟随"，监听 matchMedia('(prefers-color-scheme: dark)')
  - **9.4 Tailwind v4 的两种写法** `L383` — 推荐 data-theme：和 CSS 变量方案统一，且不会和第三方库的 .dark class 打架。
  - **9.5 微信小程序暗色适配（theme.json 官方配置逐字）** `L398` — - 用 @变量名 引用："navigationBarBackgroundColor": "@navBgColor"。
  - **9.6 iOS / Android** `L419`
  - **9.7 切换动画** `L428` — - 全局 transition: background-color .2s, color .2s 只加在容器与文字上，不要 { transition: all }（会把布局属性也带上，卡顿）。
- **10. 暗色专属的无障碍陷阱** `L436` — ---
- **11. 场景速查（12 个高频问题 → 直接答案）** `L451` — ---
- **12. 上线自检（22 项，逐条打勾）** `L470` — 决策层
- **13. 反模式（20 条，看到就是错）** `L510` — 1. filter: invert(1) 整页反相——图片、品牌色、肤色全毁
- **14. 可抄代码（4 段）** `L535` — css
  - **14.1 完整变量骨架（亮/暗双套，含层级与文字四档）** `L537`
  - **14.2 防 FOUC 的三行脚本（放 <head 最前，不 defer）** `L583`
  - **14.3 三态切换组件逻辑** `L598`
  - **14.4 暗色图片处理** `L620` — ---
- **15. 参考来源** `L642` — - Material Design 3 · Color roles / 源码：material-color-utilities 的 dynamiccolor/colorspec2021.ts（surface 与容器 tone、Contras

### `references/dataviz.md` · 数据可视化规范 · Data Visualization
_376 行 · 快照 2026-10-31 · 26 节_

- **0. 四条总原则（AntV 官方，可直接引用）** `L8` — 交互三层（AntV）：数据获取 → 信息加工 → 知识流转；口诀「概览第一，聚焦过滤，再按需查看详情」。做仪表盘时按这个顺序设计，不要一上来就给明细表。
- **1. 先判关系，再选图形（FT Visual Vocabulary 九类）** `L21` — FT 的核心主张：按"你要表达什么关系"组织，而不是按"你会画什么图"组织。选图前先回答"我想让读者看到什么关系"。
- **2. 图表选型决策树（30 秒版）** `L43` — 硬上限（超过就换图形，不要硬塞）：
- **3. 图表色板：三类用途（分类 / 顺序 / 发散），不许混用** `L76` — 这是数据可视化里最容易翻车的一环。 三类色板解决三个不同问题，混用等于撒谎：
  - **3.1 分类色板 · Carbon 14 色（IBM，精确值，必须按序取用）** `L86` — 原文规定："The colors of this palette should be applied in sequence strictly as described below." —— 顺序经专门编排以最大化相邻色对比度。不要自己挑颜
  - **3.2 分类色板 · AntV 默认 10 色（中文项目常用，G2 v5 源码实测）** `L102` — 配套语义色（状态用，不要当分类色）：危险 #F4664A｜成功 #30BF78｜警告 #FAAD14。
  - **3.3 顺序色板（连续值 / 热力 / 地图）** `L114` — 规则（Carbon 原文）：浅色主题下最深 = 最大；深色主题下最浅 = 最大。这条搞反是热力图最常见的错误。
  - **3.4 发散色板（同比增减、偏离基准）** `L126` — 铁律：中点必须是中性色或极浅色，两侧必须阶数对称、明度对称。中点不对称 = 暗示偏移不存在。
  - **3.5 状态色（警报）** `L135` — #da1e28 错误/危险 ｜ #ff832b 严重警告 ｜ #f1c21b 常规警告 ｜ #198038 正常/成功（Carbon 精确值）
  - **3.6 选色纪律（六条）** `L141` — 1. 先问有几个类别，再决定用哪种色板；不要先选好看的颜色再套数据。
- **4. 坐标轴铁律（含 G2 精确数值）** `L152` — 1. 柱状图 / 面积图 / 堆叠图必须从 0 开始。截断基线等于用长度撒谎。折线图可以截断（趋势比绝对值重要），但必须在轴上留截断符号或直接标注首末值。
  - **4.1 三条不可违反的** `L154` — 1. 柱状图 / 面积图 / 堆叠图必须从 0 开始。截断基线等于用长度撒谎。折线图可以截断（趋势比绝对值重要），但必须在轴上留截断符号或直接标注首末值。
  - **4.2 数值规格（AntV G2 v5 light 主题，源码实测，可直接抄）** `L160`
  - **4.3 布局规则** `L173` — - 网格线只保留横向（柱状/折线）。纵向网格线删掉——它和柱子重复。
- **5. 图例、标签、注释** `L184` — 信息优先级：直接标注 图例 Tooltip。每往下一级，读者多一次视线跳跃。
- **6. 中文数字与单位（中文项目必做）** `L204` — 中文图表字号比英文 +1px：轴标签 12px 在中文里偏小，建议 12–13px，下限 11px；数据标签 13–14px。中文字宽等宽，同样的 12px 中文比英文"重"，行高需 1.4–1.5（英文 1.2 即可）。
- **7. 仪表盘布局** `L223` — 结构顺序按读者的决策路径，不按数据表顺序：结论（KPI）→ 趋势（折线）→ 结构（占比/排名）→ 明细（表格）。
- **8. 图表动效（与 motion-system.md 的关系）** `L242` — 图表是唯一被允许突破 400ms 上限的场景——因为它不阻塞用户输入，且数据过渡需要可读时间。但这条豁免仅限"图表入场与数据更新"。
- **9. 可访问性（图表最容易漏的一节）** `L265` — WCAG 2.2 SC 1.4.11 非文本对比度：理解内容所必需的图形对象，与相邻颜色对比 ≥ 3:1。原文强调 3:1 是阈值，2.999:1 不通过，不可四舍五入。
- **10. 反模式清单（逐条给改法）** `L289` — 1. 柱状图不从 0 开始 → 改回 0 基线；若差异确实小，改用点图/棒棒糖图（可不从 0）。
  - **10.1 图形与比例** `L291` — 1. 柱状图不从 0 开始 → 改回 0 基线；若差异确实小，改用点图/棒棒糖图（可不从 0）。
  - **10.2 双 Y 轴（有立场，但要说清条件）** `L299` — 默认禁用。Datawrapper 2018 原文的核心论证仍然成立：两个轴的比例是任意的，读者会默认按单轴折线图去读，从而得出"两条线同速增长"这类错误结论（研究：Isenberg et al. 2011 对 15 人的实验显示双轴图在准确
  - **10.3 表达与标注** `L315` — 7. Y 轴刻度不整或跳变（0、3、6、9）→ 改 0、25、50、75、100。
- **11. 实现选型（GitHub API 实测 2026-10-31）** `L325` — 选型规则：
- **12. 自检 12 项（图表交付前逐条过）** `L349` — 1. 关系对了吗：图形是否匹配 §1 的关系类型？（不是"我觉得好看"）
- **13. 素材与出处** `L366` — - FT Visual Vocabulary — 九类数据关系与图形选型（本文件 §1 骨架，多语言版含简体中文）

### `references/design-critique.md` · 设计评审与反馈 · Design Critique & Feedback
_260 行 · 快照 2026-11-07 · 27 节_

- **0. 先分清：本文件补什么** `L10` — handoff-collaboration.md §9 已经把"一场评审会怎么开"讲清楚了（30 分钟、2 正 1 改、Presenter/Critiquer 角色、三前提）。本文件补的是它没展开的 评审手艺与评判尺子：
- **1. 两种评审，别混在一场会** `L23` — 把两者混在一个会里，结果是"既没改进也没结论"。 中文团队最常见的失败：名为评审会，实为汇报会 —— presenter 逐页讲，下面只点头。要拆就拆成两场，或同一场先 critique（前半段禁决策）再 review（后半段只决策）。
- **2. 评审前的三个前提（NN/g 原文三主题，必做）** `L36` — 1. 范围清晰：这次评什么、不评什么，必须写死。范围不清的评审 100% 跑偏（有人评配色、有人评流程，互不挨着）。
- **3. 给出反馈的七条铁律** `L46` — 1. 具体非模糊：❌"按钮太大" → ✅"主行动按钮 48px 高、比次按钮大 1.6×，但低于 iOS 44pt 触控下限，建议对齐 44pt 并靠间距拉开层级"。
- **4. 接收反馈的四步（别辩护）** `L63` — 1. 不辩护：辩解会吃掉真正讨论的时间。用"记下来"代替"但是"——哪怕你当场不同意，先落进清单，评审后逐个回应。
- **5. 怎么开一场评审（议程 / RACI / 远程异步）** `L72` — - R Presenter：讲目标 → 讲故事（遇到什么问题、为什么这么决策）→ 明确想要哪类反馈，快速讲完。
  - **5.1 RACI（handoff §9 讲的是角色动作，这里补权责）** `L74` — - R Presenter：讲目标 → 讲故事（遇到什么问题、为什么这么决策）→ 明确想要哪类反馈，快速讲完。
  - **5.2 远程与异步** `L80` — - 同步远程：共享屏幕 + 静音纪律；critique 阶段全员开麦，review 阶段只 Decider 说话。
  - **5.3 时长铁律** `L84` — - 单场 ≤ 45 分钟；超过就拆。注意力在第 30 分钟后断崖。
- **6. 评判框架（把"好不好"变成可讨论的尺子）** `L90` — 1. 系统状态可见（反馈及时）
  - **6.1 NN/g 10 可用性启发式（当作 critique 检查表）** `L92` — 1. 系统状态可见（反馈及时）
  - **6.2 严重度评级（Nielsen 0–4）** `L106` — - 0 不值得改（锦上添花）
  - **6.3 DFV 三问（Desirability / Feasibility / Viability）** `L114` — - 可取性：用户想要吗？（情感/动机）
  - **6.4 双轴：重要性 × 确定性能** `L120` — 高重要 + 低确定 → 先验证再定（做原型/AB），别在评审桌上靠辩论定生死。低重要无论确定与否 → 放权给执行者。
  - **6.5 可取性测试（desirability testing）** `L123` — 用语词配对（给一组形容词让用户选）测情感共鸣，区分"好看"和"想要"——好看不等于想要，评审常把两者混为一谈。
- **7. 反模式 15 条** `L128` — 1. design by committee（设计委员会化 / 委员会改稿）：人人能改、无人负责，结果最安全的平庸方案；评审无 Decider 时必然滑向这里。
- **8. 决策记录（ADR / critique notes）** `L148` — 评审中争议点 + 涉及的相关目标/启发式
  - **8.1 ADR 模板（Architecture/Decision Record 套路借用到设计）** `L150`
  - **8.2 critique notes（问题行）** `L165` — 铁律：没有处置结论的反馈行 = 这条反馈没发生。
- **9. 工具** `L174` — - Figma comments：原地注释 + 解决状态，异步评审主力。
- **10. 自检 20 项（评审前 / 中 / 后）** `L184` — 前（材料）：
- **11. 可抄模板（4 段）** `L214` — - like：这一屏把主行动放最右、层级清楚，一眼知道点哪。
  - **11.1 反馈话术清单（给反馈的人照着说）** `L216`
  - **11.2 评审议程（45 分钟）** `L225`
  - **11.3 ADR 片段** `L234`
  - **11.4 异步评审 checklist** `L244` — ---
- **12. 接线** `L255` — - 配套：会议流程/角色/RACI 看 handoff-collaboration.md §9（本文件补"评审手艺"，不重复）。

### `references/design-ethics-inclusion.md` · 设计伦理与包容性：欺骗性设计、隐私同意 UI、成瘾机制与认知无障碍
_799 行 · 快照 2026-11-06 · 39 节_

- **0. 与既有资产的分层（先判该读哪份）** `L9` — 边界纪律：本文件不重讲 WCAG 四档对比度、不重讲 toast 时长、不重讲断点数值。它们是必要条件不是充分条件——一个对比度 7:1 的按钮，如果「拒绝」藏在第三层设置里，依然是欺骗性设计。两套判据必须同时过。
- **1. 三条不可商量的原则（先给立场，不和稀泥）** `L27` — 1. 对称优于说服。 同意 UI 的合法性不看主按钮多醒目，看拒绝路径与接受路径是否等长、等难、等耗时。这是 CPPA §7004(a)(2) 的法条原文，不是行业最佳实践。
- **2. 分类体系裁决：别再照抄旧教程的那一套（暗黑模式 / dark patterns 现行 18 类）** `L37` — deceptive.design（原 darkpatterns.org）现行 /types 页经本轮抓取，链接共 18 类，与大量中文教程仍在流传的旧分类（Roach Motel / Privacy Zuckering / Forced C
- **3. EDPB Guidelines 03/2022 v2.0：六类机制（官方 PDF 74 页，一手）** `L70` — 来源：EDPB《Guidelines 03/2022 on deceptive design patterns in social media platform interfaces》Version 2.0, 14 February 202
- **4. CPPA §7004：把「对称选择」写成可测量的步数（本轮最硬的规则）** `L94` — 来源：California Privacy Protection Agency《CCPA Regulations》最终文本 20230329finalregstext.pdf（66 页）§ 7004. Requirements for Me
  - **4.1 (a) 五条设计原则（逐条翻成界面动作）** `L98`
  - **4.2 (a)(2) 步数怎么数（法规自己给了起止点）** `L108` — 原文规定：opt-out 步数从用户点击 "Do Not Sell or Share My Personal Information" 链接起算，到请求完成；opt-in 步数从用户首次向企业表示有意 opt-in 起算，到请求完成。两者必
  - **4.3 (a)(3) 措辞与控件的三个陷阱** `L122` — - 在 Do Not Sell or Share My Personal Information 这句话旁边放 Yes / No = 双重否定，法规明确列为混淆。
  - **4.4 (a)(4) 选择架构：不许捆绑** `L128` — 法规举例：提供基于位置的服务（如查附近油价）时，不得把「为提供服务所合理必要的位置使用」与「把地理位置卖给数据中介」这种不兼容用途捆成一个同意。必须给单独选项。→ 设计动作：按用途拆分同意项，每项独立开关，服务必需项不出现在同意弹窗里（它本
  - **4.5 (a)(5) 易执行：功能必须真的能跑** `L134` — - 点击 Do Not Sell or Share My Personal Information 后，不得要求用户在隐私政策长文里搜索/滚动去找提交机制。
  - **4.6 (b)(c) 法律效力与「意图不是决定性因素」** `L142` — - (b) 不符合 (a) 的方法可被认定为 dark pattern；通过 dark pattern 取得的同意不构成同意——法规举例：用 dark pattern 取得出售个人信息的同意，企业处于「从未取得过同意」的地位。
- **5. CPPA §7003：可读性、无障碍与「显著链接」的具体要求** `L149` — 同一份法规 § 7003. Requirements for Disclosures and Communications to Consumers：
- **6. 同意 UI 的 PASS/FAIL 构型表（可直接拿去评审）** `L163` — 一条容易漏的：管理偏好 / Preferences 不是拒绝按钮。它把用户带进更长的路径，恰恰构成 §7004(a)(2)(C) 点名的不对称。允许保留它，但只能作为第三个入口。
- **7. 中国《个人信息保护法》五条 UI 底线（官方全文逐字）** `L184` — 来源：全国人大 npc.gov.cn 公布的《中华人民共和国个人信息保护法》全文。以下为条文原意与逐字要点，均可直接转成 UI 验收项。
- **8. 中国《互联网广告管理办法》第 10 条：一键关闭的量化红线** `L200` — 施行：2023-05-01。第 10 条对弹出等形式发布的互联网广告，要求「显著标明关闭标志，确保一键关闭」，并明确列举禁止情形：
- **9. 自动续费：2025 年修正后的现行规则，以及一条必须纠正的过期口径** `L221` — 大量设计/合规文章、甚至地方法院普法稿仍在写：《网络交易监督管理办法》第 18 条要求自动续费日期前五日提醒。这是 2021 年旧版的表述。
  - **9.1 ⚠️ 反陈旧裁决：「续费前五日」已不是现行表述** `L223` — 大量设计/合规文章、甚至地方法院普法稿仍在写：《网络交易监督管理办法》第 18 条要求自动续费日期前五日提醒。这是 2021 年旧版的表述。
  - **9.2 现行第十八条 → 四条 UI 验收项** `L246` — 罚则（同份全文第四十一条）：违反第十八条第二款，法律、行政法规无规定的，责令限期改正，可以处三万元以下罚款；违反第十八条第一款、第二十一条的，依《消费者权益保护法实施条例》第五十条处理。
- **10. 默认勾选、概括授权、搭售与商业信息：同份规章的另外三条** `L261` — 《网络交易监督管理办法》（2025 修正版）还有三条直接约束 UI 默认值，逐字要点：
- **11. 未成年人防沉迷：国务院令第 766 号第 42–45 条逐条落成设计动作** `L276` — 来源：中国政府网《未成年人网络保护条例》，国务院令第 766 号，2023-09-20 国务院第 15 次常务会议通过，2023-10-24 发布，自 2024-01-01 起施行。
- **12. 成瘾设计：机制清单与「可关闭」红线** `L294` — 取源纪律（重要）：U.S. Surgeon General 2023《Social Media and Youth Mental Health》advisory 官方 PDF 在本机出口多次返回 403（返回体是 473/490 字节 HT
- **13. 欧盟 DSA 第 25 条与 FTC 2022：两套执法口径，别混成一句** `L319` — European Commission digital-strategy.ec.europa.eu 的 DSA 政策页把 "Ban on dark patterns" 列为平台义务：禁止以设计、组织或操作在线界面的方式欺骗或操纵用户、或实质
  - **13.1 DSA Article 25** `L321` — European Commission digital-strategy.ec.europa.eu 的 DSA 政策页把 "Ban on dark patterns" 列为平台义务：禁止以设计、组织或操作在线界面的方式欺骗或操纵用户、或实质
  - **13.2 FTC 2022 报告的四类 tactics** `L327` — 来源：FTC 官方 press release（2022-09）FTC Report Shows Rise in Sophisticated Dark Patterns Designed to Trick and Trap Consumer
  - **13.3 判法域的决策顺序（写进评审模板）** `L338` — ---
- **14. 包容性设计地基：不是「无障碍的补充」，是另一种起点** `L354` — Microsoft Inclusive Design 的三条原则（官方表述）：
- **15. Inclusive Design Principles 七原则（逐条 + 设计动作）** `L375` — 来源：https://inclusivedesignprinciples.info/，贡献者为 Henny Swan、Ian Pouncey、Heydon Pickering、Léonie Watson。页面立场原文："designing 
- **16. W3C COGA 八个目标：认知无障碍的可验收问句** `L393` — 来源：W3C《Making Content Usable for People with Cognitive and Learning Disabilities》（w3.org/TR/coga-usable/），章节 3.1–3.8，八个 
- **17. 合规达 ≠ 包容：两套判据的正交关系** `L418` — 给评审的一句话：「无障碍审查看能不能用，伦理审查看是不是被引导着用」。两张检查表都要签，不能互相顶替。
- **18. 决策矩阵：什么场景套哪套** `L431` — ---
- **19. 反模式 20 条：反操纵红线与合规验收判据（每条都能判 FAIL）** `L450` — 1. Accept All 配 More Information / Preferences，把「拒绝」变成一条更长的路。
- **20. 上线自检 22 项** `L475` — 同意与隐私
- **21. 可抄代码（4 段，3 段 Python 已实跑）** `L509` — 三段 Python 均只依赖标准库，直接从本文件复制即可跑。设计意图：把 §4 / §8 / §9 / §10 的条文变成能进 CI 的断言，而不是评审会上的口头约定。每段都自带 PASS 与 FAIL 双用例。
  - **21.1 同意 UI 对称性检查器（CPPA §7004 / PIPL 15·16 / EDPB mirroring）** `L513`
  - **21.2 一键关闭静态扫描（《互联网广告管理办法》第 10 条）** `L594`
  - **21.3 自动续费 UI 检查器 + 陈旧法条守卫（《网络交易办法》18 条 2025 修正）** `L637`
  - **21.4 包容性 / COGA 验收清单（YAML，进 CI 或 PR 模板）** `L684` — 实跑结果（2026-11-06，本机 Python 标准库）：consentsymmetry → good PASS 14 checks / 0 violations、bad FAIL 14 checks / 13 violations；a
- **22. 数据来源与取源纪律** `L728` — 一手法规 / 官方原文
- **23. 本轮让哪类问题不再含糊** `L788` — 1. 「这个同意弹窗合不合规」 → 不再是审美讨论：CPPA §7004 给了步数起止点、Accept All + Decline All 的固定构型、双重否定与按钮顺序反转的明令禁止，配上 §21.1 的 14 条断言，能判 PASS/F

### `references/design-md-format.md` · DESIGN.md 规范与品牌 DNA — Design Spec
_190 行 · 快照 2026-10-29 · 13 节_

- **一、DESIGN.md 是什么，为什么值得作为交付物** `L10` — 定义：一份纯 Markdown 的设计系统文档，放在项目根目录，AI 编码 agent 读了就能生成风格一致的 UI。
- **二、九章骨架（照此结构写，不增不减）** `L26` — 篇幅参考：一份合格 DESIGN.md 约 230–370 行（本地 54 份实测区间）。低于 150 行通常不够具体。
- **三、54 品牌 DNA 速查** `L44` — 用途：用户说"做成 XX 那种感觉"时，先在此定位气质，再读对应文件取精确数值。
  - **3.1 AI 与机器学习（12）** `L49`
  - **3.2 开发者工具与平台（14）** `L66`
  - **3.3 基础设施与 API（6）** `L85`
  - **3.4 生产力与协作（10）** `L96`
  - **3.5 金融科技（4）** `L111`
  - **3.6 消费品牌与巨头（8）** `L120` — ---
- **四、项目类型 → 风格推荐（选风格先看场景）** `L135` — 兜底规则：用户说"随便/你决定"→ 默认 Vercel（干净、现代、专业，最不易出错），并明确告知"我先用 Vercel 风格（简约黑白），不喜欢随时换"。
- **五、何时把 DESIGN.md 作为交付物** `L153` — 产出流程：
- **六、写 DESIGN.md 的四条纪律** `L173` — 1. 数值优先于形容词。"圆角 10px，全站统一" 优于 "圆角柔和"。
- **七、与本技能其他文件的衔接** `L182`

### `references/design-measurement-research.md` · 设计度量与用户研究：可用性指标、研究方法与统计验收
_505 行 · 快照 2026-11-07 · 50 节_

- **0. 与既有资产的分层（先判该读哪份）** `L9` — 缺口证据（升级前实测）：dpsearch.py "设计度量 用户研究 SUS 样本量 A/B 测试 可用性测试 任务成功率 HEART" 最高命中仅 knowledge-map.md 的泛化条目与 feedback-states.md 的「
- **1. 先给立场：度量三步法 + 三层判层** `L23` — 任何一次「我要看看效果」都先走这三步，顺序不能反：
- **2. 可用性的定义：ISO 9241-11 三指标（一切度量的根）** `L41` — ISO 9241-11:2018 把 usability（可用性） 定义为：指定用户在特定使用情境下，为达成指定目标而使用某系统 / 产品 / 服务时所达到的有效性（effectiveness）、效率（efficiency）与满意度（sat
- **3. 任务级指标：成功率、任务时间、错误率（最容易落地的三类）** `L55` — 这三类是每次可用性测试都必须记的原始数据，比任何问卷都硬：
  - **3.1 任务成功率（Task Completion Rate / TCR）** `L59` — - 定义：完成人数 / 参与人数，末位退出 / 求助后完成 / 走错路但最终到 = 通常记为「部分成功 0.5」；建议同时报告「完全成功 / 部分 / 失败」三段。
  - **3.2 任务时间（Time on Task / TOT）** `L64` — - 从任务说明结束到用户自认完成；必须同时记错误与求助，否则「快」可能是「乱点蒙对了」。
  - **3.3 错误率（Error Rate）** `L68` — - 每任务平均错误次数，或「至少犯一次错误的用户比例」。错误分「可恢复」（用户自己发现纠正）与「致命」（导致任务失败）。
  - **3.4 与反馈组件的接线** `L72` — 把 §3 的指标接回 feedback-states.md：错误率高是「五态里的 error / partial 没设计好」的直接证据；任务时间 10s 的区间对应「进度条 + 取消」（§反馈时间刻度）；任务失败的用户进了 error 空态
- **4. SUS 系统可用性量表（10 题 · 0–100 · 基准 68 · 曲线分级）** `L77` — SUS（System Usability Scale，Brooke 1996）是行业最通用的单页可用性问卷，10 个陈述句、5 点 Likert（1=强烈反对，5=强烈同意）：
- **5. UMUX / UMUX-Lite（4 题 / 2 题 · 与 SUS 强相关）** `L112` — SUS 有 10 题偏长，UMUX（Usability Metric for User Experience）用 4 题也能拿到与 SUS 高度相关的分数；UMUX-Lite 只用 2 题，更省。
- **6. SEQ 单题易用度 + SUPR-Q 标准百分等级 + NPS** `L123` — 每个任务结束后问一道题：「整体而言，这个任务：1=非常困难 … 7=非常容易」（或反向 1=非常容易…7=非常困难，需统一）。易用侧通常取 5–7。
  - **6.1 SEQ（Single Ease Question）** `L125` — 每个任务结束后问一道题：「整体而言，这个任务：1=非常困难 … 7=非常容易」（或反向 1=非常容易…7=非常困难，需统一）。易用侧通常取 5–7。
  - **6.2 SUPR-Q（Standardized UX Percentile Questionnaire）** `L130` — 8 题 → 输出标准百分等级（你的产品在全体参研样本里的位置），含 NPS、Trust、Appearance 子量表。适合与竞品 / 行业基准对标；要先有常模数据才有意义，小团队自测意义有限。
  - **6.3 NPS（Net Promoter Score）** `L133` — 「你有多大可能把我们推荐给朋友 / 同事？0–10」
- **7. HEART 框架（Google 五指标 + 三层落地法）** `L141` — Google 的 HEART（Happiness / Engagement / Adoption / Retention / Task success）把模糊的「体验」拆成 5 类可度量目标，每类按 信号（Signal）→ 指标（Metri
- **8. 样本量：定性「发现」与定量「下结论」是两回事** `L157` — 这是最被误用的环节。NN/g 与 Sauro 的结论是：你需要的样本量取决于你要「发现」还是「下结论」。
  - **8.1 定性可用性测试：5 人足够「发现」问题** `L161` — - NN/g 经典结论：单个同质子群体，约 5 名用户能发现约 85% 的可用性问题（假设单个用户遇到某问题的概率 λ≈0.31，公式 1−(1−λ)^n：5 人≈85%、10 人≈97%）。
  - **8.2 定量：要能算比例与置信区间** `L166` — - 要回答「任务成功率到底多少、误差多大」，按二项分布正态近似估样本量：n ≈ Z²·p(1−p) / E²（E 为半宽，Z 取 1.96 对应 95% 置信度）。
  - **8.3 一口诀** `L171` — 「要找问题用 5，要下结论用 100」；问卷与 A/B 必须按 §8.2 / §13.2 反推样本量，不能拍脑袋。
- **9. 研究方法全景：先定 2×2 再选工具** `L176` — NN/g 把方法按两个轴划分，先用轴定位再用具体方法，避免「只会做问卷」或「只会做可用性测试」：
- **10. 可用性测试：moderated / unmoderated 与出声思考** `L194` — - Moderated（有主持人）：实时观察、追问、捕捉「为什么」；适合早期定性发现（§8.1 的 5 人）。
  - **10.1 两种形态** `L196` — - Moderated（有主持人）：实时观察、追问、捕捉「为什么」；适合早期定性发现（§8.1 的 5 人）。
  - **10.2 任务脚本纪律** `L200` — - 给目标不给操作步骤：写「找到并下单一件 <¥100 的红色外套」，不要写「点顶部搜索框、输入…」。操作路径是你要观测的，不能预先规定。
  - **10.3 招人** `L206` — - 按子群体而非「随便找人」：新手/专家、移动/桌面、目标客群；每人 30–60 分钟，录屏 + 记三个原始指标（§3）。
- **11. 卡片分类与树测试（信息架构验证，最被低估的两招）** `L211` — 信息架构（导航、分类、标签）对不对，不能靠设计师拍脑袋，两招验证：
  - **11.1 卡片分类（Card Sorting）** `L215` — - Open（开放式）：给用户一堆写有内容/功能名的卡片，让他们自由分组并命名 → 发现用户的心理模型。
  - **11.2 树测试（Tree Testing）** `L220` — - 只给纯文本导航树（没有视觉），让用户从根找到目标项 → 测「能不能找着」与「找了多久」，不测「好不好看」。
- **12. 问卷与访谈设计：偏差规避（数据垃圾进、垃圾出）** `L227` — 问卷是度量里最容易被自己骗自己的地方。六类高频偏差与对策：
- **13. A/B 测试统计：显著≠值得上线** `L244` — 改版上线前用 A/B（对照实验）而非「我觉得」，但 A/B 的统计纪律比多数团队想的多：
  - **13.1 基本逻辑** `L248` — - 两组（对照 A / 实验 B）随机分流，单一主指标（Primary Metric），其余作护栏（Guardrail）。
  - **13.2 样本量与 MDE（最小可检出效应）** `L252` — 两比例 z 检验，每组所需样本：
  - **13.3 判定：p 值 + 置信区间，不是「A 比 B 高」** `L258` — - p < 0.05 只说明「差异不太可能是纯随机」，不说明改动好、不说明幅度可靠；必须同时报差异的 95% 置信区间。
  - **13.4 顺序检验与早停** `L264` — - 中途反复偷看 p 值、一显著就停，会虚高假阳性率；用 alpha spending（O'Brien–Fleming 类） 控制：越早治疗越严、接近预定样本才放宽。
- **14. 分析数据：事件、漏斗、留存、同期群** `L270` — 线上行为数据三件套，回答「用户在哪流失」：
- **15. 证据分级与混合方法（别把噪声当信号）** `L281` — 沿用 §2 与 accessibility.md 的立场：「用户能不用（无障碍/有效性）」和「用户愿不愿用（可用性/满意度/转化）」是两张表。一个改动可能无障碍过关但满意度崩（如强制精简步骤让用户找不到功能），也可能满意度高但有效性低（好看
  - **15.1 可用性 ≠ 无障碍，两列签字** `L283` — 沿用 §2 与 accessibility.md 的立场：「用户能不用（无障碍/有效性）」和「用户愿不愿用（可用性/满意度/转化）」是两张表。一个改动可能无障碍过关但满意度崩（如强制精简步骤让用户找不到功能），也可能满意度高但有效性低（好看
  - **15.2 证据层级（按「可信度」加权，不是按「人数」）** `L286` — NN/g 的立场是没有单一金标准，但可分层：
  - **15.3 三角验证（Triangulation）** `L293` — 一个结论至少用两种独立方法互相印证（如「树测试找不到入口」+「漏斗在某步掉 40%」+「访谈用户说找不到」）。只有一种方法时，明确标注证据等级，不做过度推断。
- **16. 研究运营与研究库（Research Ops / Repository）** `L298` — 规模化团队要把研究当资产沉淀，不是「每次用完就扔」：
- **17. 工具矩阵（注明：本轮 star/许可未实测）** `L308` — 取源限制（公开记录）：本轮 GitHub API 与多数官网限频（reset 2026-11-07 20:21 UTC+8），下列工具的 star / 开源许可 / 实时定价未逐条核验，仅按公开功能定位归类，下一轮用 GitHub API 
- **18. 场景决策矩阵（12 场景：凭问题选度量方案）** `L327` — ---
- **19. 20 条反模式（研究者与设计师都容易犯）** `L346` — 1. 5 人问卷下结论：把 5 人定性发现说成「80% 用户喜欢」（§8.1）。
- **20. 20 项自检（交付一份研究方案 / 看一份数据报告时逐条过）** `L371` — 1. 这次度量要回答的问题写清楚了吗（有效性/效率/满意度/转化/留存，不是「看看效果」）？
- **21. 可抄代码（4 段 Python，已实跑）** `L396` — python
  - **21.1 样本量：定性发现率 + 定量比例置信区间** `L398` — 实跑输出：5 人≈84% / 10 人≈98% / 20 人≈100%；p=50%→97 人 / p=80%→62 人 / p=5%→19 人（与 §8.1/§8.2 一致）。
  - **21.2 SUS 计分（奇偶反向 × 2.5）** `L418` — 实跑：50.0 / 50.0 / 100.0，与 §4 公式一致（一致作答恒为 50 是 SUS 的已知特性，别误读为「中性=差」）。
  - **21.3 A/B 两比例 z 检验 + 差异置信区间** `L436` — 实跑：A 5.0%→B 6.0% 得 p≈0.0019（显著）、相对 +20%、CI 不跨 0 → B 赢（与 §13.3 口径一致）；若把 B 降到 525/10000（5.25%），p≈0.43、CI 跨 0 → 未分胜负，哪怕点估计 
  - **21.4 UMUX-Lite 重标定（1–7 → 0–100，无需校准）** `L462` — 实跑：100.0 / 50.0 / 33.3，与上面公式一致；把 UMUX-Lite 当 SUS 用的回归系数请在自己样本上标定，不在本文件给出（避免传播未核验数字）。
- **22. 来源与取源限制（公开记录）** `L480` — 逐字口径取自（官方原文 / 权威著作，本轮已对照）：
- **23. 与既有资产的最短接线（防止知识孤岛）** `L499` — - 任务成功率 / 错误率 → feedback-states.md（五态 error/partial）、form-table.md（表单流失）、dataviz.md（漏斗图）。

### `references/design-system-docs.md` · 设计系统文档写作：组件文档页 / 信息架构 / 版本化 / 治理
_949 行 · 快照 2026-11-05 · 51 节_

- **0. 与既有资产的分层（先判读哪一份，别读错）** `L7` — 一句话分层：DESIGN.md 是给机器读的约束，design-system-docs.md 是给人读的系统。handoff-collaboration.md 的终点是"开发能做出第二个页面"，本文件的终点是"半年后第三个团队也能自己查到、
- **1. 判层：先分清你要写的是哪一种设计系统文档（Diátaxis 四象限）** `L20` — 最常见的失败不是写得不好，是把四种文档混在一页里：一个组件页里既塞入门教程、又塞 props 表、又夹一段"我们为什么这样设计"，结果谁都找不到自己要的东西。
- **2. 组件文档页九段式：GOV.UK 逐节拆解（最经得起检验的模板）** `L54` — GOV.UK Design System 的 Button 页是全球被抄最多的组件文档结构。直接读其源文件 src/components/button/index.md，可逐字核对，不是二手总结。
  - **2.1 源文件 frontmatter（7 个字段，一个都不能少）** `L58`
  - **2.2 正文九段（按源文件与渲染页逐节对照）** `L80`
  - **2.3 九段里最常被漏掉的是 7/8/9 —— 而它们才是"活文档"的原因** `L94` — 多数设计系统只有 1–6（实例 + 用法 + 变体 + props），于是半年后没人敢信它：
- **3. 五问验收 + 组件页字段清单（能打分才算规范）** `L106` — 可量化的最低门槛：一个组件页至少 1 个可交互实例 + 2 段判断（use / not use）+ 3 个状态或变体 + 1 条带出处的证据 + 1 条带日期的变更记录。低于此不要标 stable（见 §9）。
  - **3.1 五问（缺一即判该组件文档「未完工」）** `L108` — 可量化的最低门槛：一个组件页至少 1 个可交互实例 + 2 段判断（use / not use）+ 3 个状态或变体 + 1 条带出处的证据 + 1 条带日期的变更记录。低于此不要标 stable（见 §9）。
  - **3.2 NN/g 的六字段（与九段式的映射）** `L120` — NN/g Design Systems 101（2021-04-11 发布，2026-08-27 复审）列出组件库除视觉示例外必须包含：
- **4. 信息架构：目录、命名、链接、检索（文档写作的四条地基）** `L140` — 中文场景补充：中文组件页常见「一句英文术语 + 三种中文译法」。ux-writing.md 的术语表规则在此同样适用——建一张文档术语表，同概念同词（variant ≠ 变体 ≠ 样式 ≠ 状态），并在 frontmatter 的 alia
- **5. 文档写作规范：Google 三条参考层级 + 可直接执行的清单** `L157` — Google developer documentation style guide（About 页）给出的参考优先级是设计系统文档最该照抄的治理结构：
- **6. 示例代码的可抄性：五条硬规则（写错就没人用）** `L188` — GOV.UK 每个例子都给 HTML + Nunjucks 双 tab + 新窗口打开；NN/g 更进一步要求 code snippets 与框架说明。合成本技能的验收口径：
- **7. 完整填充范例：一个可直接复制的组件文档页（Button 精简版）** `L202` — 下面是模板骨架，不是给某个具体组件库的规范值。方括号处必须替换；带 ⚠️ 的是最常被漏掉的字段。把这一段存成 components/button.md 即可作为新组件页的起点。
- **8. 活文档四件套：研究 / 已知问题 / 近期变更 / 帮助改进（证据与反馈闭环）** `L293` — GOV.UK 把它做成了产品机制而不是文案：discussionId 是 frontmatter 字段，Help improve 直接给 GitHub 讨论串与 propose a content change using GitHub 指
- **9. 组件文档状态与成熟度（USWDS 生命周期 + Carbon semver 对照）** `L311` — USWDS 把组件状态存在 data/lifecycle-status.yml（statusmajor + statusminor 两个字段），阶段定义存在 data/lifecycle-phases.yml。这是状态数据化的范例：文档页不
  - **9.1 USWDS 三阶段 / 十二子状态（读 data/lifecycle-phases.yml 源码所得）** `L313` — USWDS 把组件状态存在 data/lifecycle-status.yml（statusmajor + statusminor 两个字段），阶段定义存在 data/lifecycle-phases.yml。这是状态数据化的范例：文档页不
  - **9.2 Carbon 把"什么改动算什么版本"做成了可查表（源码 docs/guides/versioning.md）** `L337` — Carbon 直接引用 SemVer 三段定义，并给出 @carbon/react 的逐改动类型版本表：
- **10. 文档版本化（Docusaurus 3.10.2 官方规则 + SemVer 对接）** `L360` — Docusaurus Versioning 原文三条警告（逐字）：
  - **10.1 先问"要不要版本化" —— 官方立场是否定的** `L362` — Docusaurus Versioning 原文三条警告（逐字）：
  - **10.2 需要版本化时的精确规则** `L372` — PATCH 不要切文档版本（官方原文）：包从 1.0.0 修到 1.0.1，"Should you cut a new documentation version 1.0.1? You probably shouldn't"，理由是 "1.
- **11. Changelog：Keep a Changelog 1.1.0 的七条指导原则与六类变更** `L404` — "All notable changes to this project will be documented in this file."
- **12. 迁移文档：MAJOR 必带，且必须能被机器校验** `L461` — SemVer FAQ 关于废弃的原文要求："When you deprecate part of your public API, you should do two things: (1) update your documentatio
- **13. Token 文档自动生成：DTCG 2025.10 把 $description 明确定位成文档源** `L480` — handoff-collaboration.md §13.2 与来源清单写的是 https://tr.designtokens.org/format/，标注「预览草稿」。本轮打开该页核对，页首状态为：
  - **13.1 ⚠️ 先裁决一个本技能自己引用过的 URL 口径** `L482` — handoff-collaboration.md §13.2 与来源清单写的是 https://tr.designtokens.org/format/，标注「预览草稿」。本轮打开该页核对，页首状态为：
  - **13.2 规范里原生就有「文档工具」这一类** `L492` — DTCG §3.5 原文定义 Documentation tool："A tool for documenting design tokens usage"，并列举 Storybook / Zeroheight / Backlight / 
  - **13.3 能直接喂给文档生成器的字段（全部来自规范正文）** `L498` — 可抄的 token → 文档最小范例（$description 与 $deprecated 均按规范正文写法）：
  - **13.4 三条落地纪律** `L530` — 1. 单一真源：token 值是 .tokens.json，文档页由生成器渲染（Style Dictionary / Storybook doc block），禁止在 Markdown 里复制粘贴数值。本技能自己就是这么做的：scripts
- **14. 代码即文档：Storybook Autodocs / MDX / Doc Blocks 精确配置** `L538` — NN/g 要求 code snippets 与 sandbox，DTCG 把 Storybook 列为文档工具，Storybook 官方则把 story 直接定义为文档的基础："When you write component storie
  - **14.1 Autodocs：tags: ['autodocs']（版本相关，逐字配置）** `L542` — 原文规则："If a CSF file contains at least one story tagged with autodocs, then a documentation page will be generated for th
  - **14.2 MDX：结构文档 + 可交互 JSX** `L557` — 官方分工原话：CSF "is great for succinctly defining stories… If you use TypeScript, it also provides type safety and auto-compl
  - **14.3 与九段式的对接表** `L584` — 结论（给立场）：机器负责"值"，人负责"判断"。props、token 值、状态截图、代码 tab 全部自动生成；When not to use、Research、Recent changes、禁令与取舍理由必须人写。把两者混在同一份手写 
- **15. 设计稿 ↔ 文档 ↔ 代码：Figma Code Connect 与命名一致性** `L599` — handoff-collaboration.md 讲「标注只标例外」「Dev resources 传播到所有实例」；本节补上设计组件与真实代码组件之间的连接层。
- **16. 贡献与治理：GOV.UK 的准入标准（含可量化阈值）** `L622` — 可复制的治理动作：提案阶段先要「多团队复用证据 + 不重复」，避免系统变成个人组件收藏夹；发布前要「含残障用户的研究样本 + 跨浏览器/读屏/设备 + 文案与代码规范 + 多场景通用性」。这五条比"PR 里附张截图"严格一个数量级，也正是 
  - **16.1 组件准入：提案 2 条 + 发布前 3 条（Contribution criteria 原文）** `L624` — 可复制的治理动作：提案阶段先要「多团队复用证据 + 不重复」，避免系统变成个人组件收藏夹；发布前要「含残障用户的研究样本 + 跨浏览器/读屏/设备 + 文案与代码规范 + 多场景通用性」。这五条比"PR 里附张截图"严格一个数量级，也正是 
  - **16.2 社区资源/工具准入的七条带数值要求（原文）** `L636` — 链接到设计系统的第三方资源须满足：有明确 owner；不会被误认为官方；有文档说明如何使用、如何贡献、如何获得支持；support tickets 1 个月内答复；写明支持哪个 GOV.UK Frontend 版本；落后最新版本不超过 3 
  - **16.3 USWDS 的公开决策节奏** `L642` — Proposal open for comment 阶段最少 45 天公开评论期，状态数据存在仓库里（lifecycle-status.yml），而不是会议纪要。结合 NN/g 的最小团队编制（1 交互 + 1 视觉 + 1 开发，理想配 
- **17. 文档新鲜度与漂移：可测指标 + 本技能自身的防漂移机制（自举）** `L650` — design-partner 为了对抗自身 26+ 份参考的漂移，已经跑通四层，正好对应本文的四个论点：
  - **17.1 六项可自动检查的指标** `L652`
  - **17.2 本技能自己就是这套机制的活样本（可直接抄架构）** `L663` — design-partner 为了对抗自身 26+ 份参考的漂移，已经跑通四层，正好对应本文的四个论点：
  - **17.3 一条反直觉但重要的结论** `L678` — 文档越"自动生成"越要写判断。能自动生成的（props、token 值、故事截图、变更列表）不写反而更准；不能自动生成的（何时别用、证据、取舍、已知问题）不写就永远没人补。所以文档工作量不会因自动化减少，只是从抄数值转向写立场。
- **18. 十二场景速查（设计系统文档写作）** `L684` — ---
- **19. 二十条反模式（写了等于没写）** `L703` — 1. 只有截图和 props 表，没有「什么时候不用」。
- **20. 二十项自检（组件文档上线前逐条打勾）** `L728` — 1. 页面属于四象限中的哪一类？混合页是否有固定分区（§1）？
- **21. 六段可抄代码（文档团队直接拿去用）** `L753` — python
  - **21.1 组件页 frontmatter 校验（Python，CI 里跑）** `L755`
  - **21.2 Docusaurus 版本化配置（单 major 长期维护，避免维护两份）** `L781`
  - **21.3 CHANGELOG 格式校验（六类 / ISO 日期 / Unreleased / breaking）** `L800`
  - **21.4 token 文件 → 文档表格生成器（用 $description / $deprecated）** `L820`
  - **21.5 Storybook MDX 组件页（人写判断 + 机器给值）** `L843`
  - **21.6 文档新鲜度巡检（owner / stale / 失联链接）** `L879` — ---
- **22. 来源（2026-11-05 取源，全部官方原文 / 上游源码 / API 实测）** `L899` — 组件页结构与准入：

### `references/design-tokens.md` · 设计 Token 体系 — Design Tokens（深度蒸馏）
_231 行 · 快照 2026-10-29 · 13 节_

- **一、三层架构（唯一正确的组织方式）** `L9` — 铁律：
- **二、Ant Design 数值体系（中文语境最完整的一套）** `L26` — Ant Design 的字体方案基于「动态秩序」原则，结合自然对数与音律规则推导；布局基于柯布西耶模度思想。以下是可直接抄用的数值。
  - **2.1 色彩** `L30` — 中性色的透明度实现（浅色 / 深色双值）：
  - **2.2 字体** `L56` — 字体族栈（直接可用）：
  - **2.3 布局与间距** `L83` — 两种适配范式：
  - **2.4 圆角与阴影（跨体系通用建议）** `L99` — 阴影三层足够：sm 悬停微起 / md 卡片默认 / lg 弹层浮起。阴影与边框二选一，同时用会显脏。
- **三、三大体系对比（选哪套取决于产品语境）** `L112` — 选择规则：
- **四、中文设计系统矩阵（GitHub 验证 · 2026-10-29）** `L133` — 选型规则：
- **五、Token 输出格式（三种落地形态）** `L156` — css
  - **5.1 CSS 变量（推荐，最通用）** `L158`
  - **5.2 Tailwind 配置（工程侧）** `L183`
  - **5.3 JSON（给设计工具 / agent 用）** `L199` — 一份 token 三处输出（CSS / Tailwind / JSON）是标准做法；源头只能有一份，其余由脚本生成，否则必然漂移。
- **六、常见错误（逐条对照）** `L218`

### `references/direct-manipulation.md` · 直接操纵与指针交互（Direct Manipulation / Pointer, Gesture & Drag-and-Drop）
_893 行 · 快照 2026-11-10 · 31 节_

- **1 · 为什么单列「直接操纵与指针交互」** `L19` — 40 份参考里，「拖拽 / 手势 / 指针 / 拖放」没有独立资产。缺口用 dpsearch.py 与全域词频统计判定为结构性空白，不是覆盖不足。
- **2 · 四段链路模型：先判哪一段断，再谈改动画** `L31` — 任何「拖不动 / 拖到一半飞了 / 手机上不生效 / 读屏用户完全用不了 / 放错位置回不来」的问题，先判落在哪一段。
- **3 · 裁决一：SC 2.5.7 要的是「单指针无拖动」，不是「键盘也能拖」** `L46` — W3C《Understanding SC 2.5.7 Dragging Movements》（Level AA）逐字：
- **4 · G219 的四类无拖动替代与两步验收** `L64` — W3C Technique G219（Sufficient for 2.5.7）逐字描述目标："ensure that people with motor impairments who cannot carry out dragging 
- **5 · 裁决二：路径手势、拖动、指针取消是三条不同的准则** `L85` — 三者常被混成一句「手势要可访问」，但 W3C 分了三条不同级别、不同判据的准则。
- **6 · SC 2.5.2 与 G210：取消是硬要求，撤销不是可选项** `L108` — W3C《Understanding SC 2.5.2 Pointer Cancellation》（Level A）逐字四选一：
- **7 · 拖放的完整状态机：从 down-event 到可撤销** `L126` — 把 §3–§6 的条文落到同一套状态机，避免「合规条款各自看过、代码里还是 pointerdown 提交」。
- **8 · 裁决三：目标尺寸三套口径，24×24 是 AA 下限不是设计值** `L143` — W3C SC 2.5.8 Target Size (Minimum)（AA） 逐字：
- **9 · W3C Pointer Events Level 3 的规范性因果链：pointercancel 什么时候必然触发** `L179` — touch-action 为什么不能用 preventDefault() 代替（PE3 §4.1.3.1 逐字）：
- **10 · MDN PointerEvent 工程契约：设备、事件、捕获、取消** `L207` — MDN《Pointer events》逐字定义："Pointer events are DOM events that are fired for a pointing device. They are designed to create
- **11 · touch-action 全值表、形式语法与三条工程陷阱** `L233` — MDN《touch-action》正式语法（逐字）：
- **12 · HTML Drag and Drop API：七事件、DataTransfer 与 drop target 规则** `L267` — MDN《HTML Drag and Drop API》逐字："The user may select draggable elements with a mouse, drag those elements to a droppable e
- **13 · 键盘拖放契约：dnd-kit 的逐字键盘参数** `L297` — W3C APG 的通用键盘原则先立地基（《ARIA Authoring Practices Guide — Keyboard Interface》本轮逐字核验）："The visual focus indicator must always
- **14 · 读屏指令、live region 播报与中文 announcements** `L326` — dnd-kit 的三问框架（逐字）："1. Identity: What element is the user interacting with? 2. Operation: How can the user interact with 
- **15 · signifier 与两类反馈：NN/g 的可发现性裁决** `L373` — NN/g《Drag-and-Drop: How to Design for Intuitive Interactions》（2020-02-23）Summary 逐字："Clear signifiers and clear feedback
- **16 · 触屏拖放的硬性前提：1cm×1cm、几毫秒、约 100ms** `L393` — NN/g 对触屏的判断是本主题最强的「别做」依据。逐字：
- **17 · 阈值与时序决策表** `L417` — 把散落在各源的数值收成一张可执行表；「工程约定」列一律不是标准。
- **18 · 决策一图流** `L439` — ---
- **19 · 替代路径矩阵：四种输入各自满足哪条 SC** `L472` — 这张表用来回答「我们做了键盘模式，为什么还不过审」。
- **20 · 库生态实测与选型** `L488` — GitHub API 实测（2026-11-10，GET /repos/{owner}/{repo}，star / license / pushedat / archived 均为实测值）：
- **21 · 与既有资产的边界矩阵** `L509` — ---
- **22 · 场景速查（12）** `L526` — ---
- **23 · 反模式（20）** `L545` — 1. 用「补了 Space + 方向键」申报 SC 2.5.7 合规（键盘不是 single pointer）。
- **24 · 自检（20）** `L570` — 1. 所有「元素跟随指针」的功能都列出来了吗？逐个有单指针无拖动路径吗（2.5.7 / G219）？
- **25 · 可抄代码（5 段；§25.1–§25.3 为 Python，本轮已实跑 PASS）** `L595` — python
  - **25.1 · WCAG 2.5.8 目标尺寸与 24px 圆间距判定器** `L597`
  - **25.2 · 三体系目标尺寸对照 + CSS 静态风险扫描** `L668`
  - **25.3 · 拖拽可访问性契约静态扫描器** `L729`
  - **25.4 · Pointer Events + touch-action + capture + Esc 取消骨架（JS/CSS）** `L792`
  - **25.5 · dnd-kit 中文指令与 position 播报（JS，模板见 §14）** `L839` — ---
- **26 · 取源与限制（公开记录）** `L863` — W3C / WAI（本轮逐页逐字核验）：Understanding WCAG 2.2 的 pointer-gestures.html（SC 2.5.1 A、path-based 定义、slider/carousel 三态判例、keyboar

### `references/editorial-layout.md` · 版式与网格（Editorial Layout）
_767 行 · 快照 2026-11-01 · 63 节_

- **§0 一页速查（赶时间只看这里）** `L18` — ---
- **§1 先判载体：五类产出的本质差异** `L38` — 版式不是一套规则通吃。先定载体，再定网格，顺序反了会做出"网页排版的海报"。
- **§2 网格类型与选择** `L54` — 选择顺序（照做即可）：
- **§3 栏数、gutter 与基线网格** `L74` — 12 的约数有 2、3、4、6——同一套栏线可以切出 1/2、1/3、1/4、1/6 的所有组合，这是它成为默认值的唯一原因（数学，不是审美）。
  - **3.1 为什么是 12 栏** `L76` — 12 的约数有 2、3、4、6——同一套栏线可以切出 1/2、1/3、1/4、1/6 的所有组合，这是它成为默认值的唯一原因（数学，不是审美）。
  - **3.2 gutter 与栏宽的关系** `L90` — - gutter 固定、栏宽流体（与响应式一致）：gutter 用百分比会导致大屏松、小屏挤。
  - **3.3 基线网格（最容易被跳过、收益最大的一项）** `L96` — 规则：所有垂直尺寸（行高、段间距、图高、卡片高、模块间距）都是同一个基线单位的整数倍。
- **§4 版心与页边距（版心宽度 / 页边距比例）** `L108` — 版心先定，边距是结果——不要先给 margin 再算内容宽度，会得到 6.5″ 这种"打字机行长"。
  - **4.0 版心宽度速查（一句话答案）** `L110` — 版心先定，边距是结果——不要先给 margin 再算内容宽度，会得到 6.5″ 这种"打字机行长"。
  - **4.1 Van de Graaf canon（唯一有几何证明的边距系统）** `L123` — 对任意页面比例都成立，2:3 页面时结果最漂亮：
  - **4.2 实用边距表** `L139` — 两条硬规则：
  - **4.3 版心宽度与开本** `L154` — - 版心宽 ≈ 页宽 × 0.55–0.70（书页）；低于 0.5 显空，高于 0.75 显挤。
- **§5 字号模数与层级（字号阶梯）** `L161` — 以正文为基准（1.0），乘同一个比例得到各级字号：
  - **5.1 模数比例（modular scale）** `L163` — 以正文为基准（1.0），乘同一个比例得到各级字号：
  - **5.2 中文的字号修正** `L182` — - 中文同字号视觉上比西文小（字面率低），整体 +1–2px：正文 16–18px（内容页）/ 14px（中后台）。
- **§6 行长与行距（最影响"读得下去"的两项）** `L191` — 西文（Butterick 原文）：
  - **6.1 行长（measure）** `L193` — 西文（Butterick 原文）：
  - **6.2 行距（leading）** `L205` — 西文（Butterick 原文）：120%–145% 字号。低于 110% 太挤，高于 170% 太散。
  - **6.3 行长 × 行距联动表（直接用）** `L215`
  - **6.4 段落间距 vs 首行缩进（二选一，不许并用）** `L224` — 中文特例：首段不缩进（跟随标题），后续段缩进 2 字——这是书籍惯例；网页一律用段间距。
- **§7 段落细节与断行（工艺层，差一点就差很多）** `L236` — - orphan（孤行）：段落首行被留在页/栏底部，单独一行。
  - **7.1 孤行与寡行（widows & orphans）** `L238` — - orphan（孤行）：段落首行被留在页/栏底部，单独一行。
  - **7.2 断行算法（CSS 三件套）** `L245` — 标题一行放不下时的正确顺序：① 改文案（最有效）→ ② 缩字号一档 → ③ text-wrap: balance → ④ 手动 <br 控制断点。永远不要靠 letter-spacing 硬塞。
  - **7.3 标点悬挂（hanging punctuation）** `L256` — - 西文：hanging-punctuation: first last; 让首行开引号/末行闭引号探出版心，左边缘视觉才齐。
  - **7.4 两端对齐（justify）的代价** `L262` — - 中文：text-align: justify 可用且推荐（方块字天然等宽，不会出现大河）。
- **§8 视觉动线与焦点** `L270` — 海报/社媒图一律用单点式：先定"3 秒后用户记住的那一个东西"（一句话/一个数字/一张脸），其余元素降级为配角。
  - **8.1 三种动线模型** `L272` — 海报/社媒图一律用单点式：先定"3 秒后用户记住的那一个东西"（一句话/一个数字/一张脸），其余元素降级为配角。
  - **8.2 分割线与落点** `L282` — - 三分法（rule of thirds）：把画面切 3×3，主体放在交点上（0.333 / 0.667）。YouTube 官方缩略图指南明确推荐用三分法构图。
  - **8.3 视觉重量（判断"哪边重"）** `L288` — 按重量从大到小：人脸/眼睛 高对比色块 大字号 深色块 图形 细线 留白。
- **§9 留白与密度（留白占比）** `L296` — 四条纪律：
- **§10 海报（Poster）** `L314` — ISO 216 规则：A 系列同一比例 √2:1，每级面积为上一级一半，向下取整到毫米；尺寸公差 ≤150mm 为 ±1.5mm、150–600mm 为 ±2mm、600mm 为 ±3mm。
  - **10.1 尺寸与文件** `L316` — ISO 216 规则：A 系列同一比例 √2:1，每级面积为上一级一半，向下取整到毫米；尺寸公差 ≤150mm 为 ±1.5mm、150–600mm 为 ±2mm、600mm 为 ±3mm。
  - **10.2 出血与安全区（做错必被印厂退回）** `L330` — 常见事故：把底色做成"成品尺寸"→ 裁切后四边露白边 1–2mm。底色画布 = 成品 + 出血 ×2。
  - **10.3 海报的信息层级（三层封顶）** `L342` — 远距离可读性经验公式（标牌行业惯例，非标准）：字高（mm）≈ 观看距离（m）× 8。
  - **10.4 海报构图四选一** `L355` — 必查：文字压在图上时，局部对比度 ≥4.5:1（不是整图平均）。做法：给文字区加单向渐变遮罩（黑 0%→60%），不要给整图加暗角。
- **§11 长图（Long Image / 信息长图）** `L368` — 长图在手机上被缩放到屏宽显示，所以设计稿字号必须按比例放大：
  - **11.1 尺寸与字号换算（这一步错了整张图都小）** `L370` — 长图在手机上被缩放到屏宽显示，所以设计稿字号必须按比例放大：
  - **11.2 分段节奏（长图的真正难点）** `L382` — - 一屏一个信息点。屏高按 1080 × 1.4 ≈ 1500px 估算（手机可视区约 1.4 屏宽高比）。
  - **11.3 切图与导出** `L389` — - 单张高度 ≤ 20000px（部分平台/工具上限），超出切成 2–3 段，重叠 100–200px 保证接缝连续。
- **§12 社媒图（各平台尺寸表）** `L398` — 标注「官方」= 平台文档明确写出；标注「惯例」= 行业通行但平台未承诺，上线前以平台当前页面为准。
  - **12.1 尺寸表** `L402`
  - **12.2 缩略图测试（社媒图的唯一硬指标）** `L424` — 把成品缩到 120px 宽看一眼：
  - **12.3 平台裁切安全区** `L433` — ---
- **§13 印刷交付（设计做完不等于能印）** `L445` — - 字体转曲（outline） 或嵌入字体。转曲后不能再改字，保留一份可编辑源文件。
  - **13.1 五个必查项** `L447`
  - **13.2 字体与文件** `L457` — - 字体转曲（outline） 或嵌入字体。转曲后不能再改字，保留一份可编辑源文件。
  - **13.3 纸张与工艺（影响设计决策）** `L464` — ---
- **§14 CSS 实现（可抄）** `L476` — css
  - **14.1 编辑型网格（12 栏 + subgrid 对齐）** `L478` — subgrid 关键事实（MDN）：grid-template-columns: subgrid 让子网格复用父级轨道尺寸，gap 默认继承（可覆盖）；子网格内行号从 1 重新计数；子网格维度不会生成隐式轨道——自动放置超出时会挤进最后一轨
  - **14.2 长文排版（一次给全）** `L503`
  - **14.3 首字下沉（drop cap）** `L527` — 注意（MDN）：initial-letter: 3 等价 3 3（sink = size）；3 1 是凸起（raised）效果。中文不用首字下沉（方块字下沉后与后续字基线错位，视觉很怪）。
  - **14.4 多栏文本（杂志内页）** `L539`
  - **14.5 竖排（中文/日文传统版式）** `L552` — clreq 要点：直排时行由右向左、栏水平切割、书页由左页起；西文单词顺时针旋转 90°，并在与汉字间加 ≤1/4 汉字宽字距（行首行尾除外）；2–3 位数字用纵中横排。
  - **14.6 图片按版心比例裁切** `L566` — ---
- **§15 中文版式专项（避头尾 / 标点 / 竖排）** `L579` — 中文排版三条最常翻车的：① 用 letter-spacing 拉大字距冒充"高级感"（方块结构散了）；② 用 text-align: justify 但不处理标点挤压（出现"孤字成行"）；③ 中英混排不加空隙（2026年11月1日 与 20
- **§16 工具链（star / 许可实测 2026-11-01）** `L598` — 选型建议：
- **§17 反模式（20 条，逐条对照）** `L621` — 1. 正文通栏 1200px，一行 130 字符 —— 读者第三行就串行。
- **§18 自检（18 项，交付前逐条过）** `L646` — 网格与版心
- **§19 三套可抄模板** `L676` — html
  - **19.1 A2 海报（上下分割，含出血）** `L678`
  - **19.2 1080 宽长图首屏** `L707`
  - **19.3 OG / 社媒分享卡（Satori 友好：只用 flex）** `L730` — Satori 限制：只支持 flex 子集（无 grid、无 gap 的部分写法、需内联样式或 tw 属性），字体需显式传入。
- **§20 与其他文件的分工** `L756` — 一句话分工：本文件管"版面怎么分、字怎么排、图怎么印"；responsive-layout.md 管"宽度变了怎么办"；chinese-design.md 管"中文特有的字与标点"。

### `references/feedback-states.md` · 反馈与状态设计 — Feedback & States（深度蒸馏）
_587 行 · 快照 2026-11-01 · 54 节_

- **§1 反馈的五个层级与选择决策** `L10` — ① 这条信息需要用户「做一个决定」吗？
  - **1.1 层级表（先定层级，再选组件）** `L12`
  - **1.2 三问决策树（照此走，不要凭手感）** `L22`
  - **1.3 三条硬规则** `L38` — 1. 一个动作只给一次主反馈。点了保存 → 按钮变 loading → 成功后按钮旁出现"已保存"，就不要再弹 toast。双层反馈 = 噪音。
- **§2 时间阈值（唯一的权威刻度）** `L46` — - Ant Design 的口径是 2s 就应给加载状态，并明确"若加载时间较长，应提供取消操作"。
  - **2.1 三个经典阈值（Nielsen，1993 提出，2014 复核仍成立）** `L48`
  - **2.2 现代细化（把三个阈值翻译成组件选择）** `L56` — - Ant Design 的口径是 2s 就应给加载状态，并明确"若加载时间较长，应提供取消操作"。
  - **2.3 两个被明令禁止的做法** `L68` — - ❌ 静态 "Loading…" 文案：任何反馈优于无反馈，但静态提示信息不足——系统卡死时用户无法判断是否需要重启。
- **§3 Toast / Snackbar / Message（轻提示）** `L75` — 取值纪律：同一产品内所有 toast 用同一时长。Carbon 甚至要求时间戳"全有或全无"——混用会训练用户"有的能读完有的读不完"，最终全都不读。
  - **3.1 时长与位置：五个体系的精确值** `L77` — 取值纪律：同一产品内所有 toast 用同一时长。Carbon 甚至要求时间戳"全有或全无"——混用会训练用户"有的能读完有的读不完"，最终全都不读。
  - **3.2 尺寸与内容上限** `L90` — - 行数：Carbon 明确 ≤2 行、内容 1–2 句；M3 要求尽量 1 行，移动端最多 2 行。超 2 行 → 改用带"查看详情"链接的 L2 通知。
  - **3.3 该用 / 不该用（最容易出错的一节）** `L97`
  - **3.4 无障碍（这一节决定能不能过验收）** `L109` — - 必须能被程序化确定：容器用 role="status"（成功/进度）或 role="alert"（错误），见 WCAG 4.1.3 与 §10.1。
  - **3.5 中文与小程序专属坑** `L118` — - wx.showToast：icon 为 success/error/loading 时，title 最多 7 个汉字（超出直接截断，不换行）；icon:'none' 时可显示两行。→ 中文提示超过 7 字就必须用 icon:'none'
- **§4 加载与进度** `L126` — - 不要 frame-only 骨架（只有页头页脚、中间一片空）：NN/g 明确不推荐——它不传达页面结构，用户等久了会以为页面坏了，等价于一个 spinner。
  - **4.1 三种加载形态的分工（Carbon + NN/g 合并口径）** `L128` — - 不要 frame-only 骨架（只有页头页脚、中间一片空）：NN/g 明确不推荐——它不传达页面结构，用户等久了会以为页面坏了，等价于一个 spinner。
  - **4.2 防闪烁（实践建议值，非官方规范）** `L140` — - 请求 < 200ms 返回时不显示任何加载态——避免"闪一下"。
  - **4.3 进度条的六条铁律** `L146` — 1. 10s 必须给百分比，并给粗略时间（"大约还需 1 分钟"）。不要给精确到秒的倒计时——必然不准，且不准会损害可信度。
  - **4.4 按钮内 loading（最高频、最容易做错）** `L156` — - 文案：动词进行时（"保存中…"→"已保存"），不要"提交"→"提交中"→"提交"。
  - **4.5 乐观更新（Optimistic UI）** `L168` — - 适用：成功率高、失败代价小、可回滚（点赞、收藏、勾选完成、拖拽排序、发消息）。
- **§5 空态 / 空状态（五种"空"）** `L177` — 最常见的错误：把失败渲染成无数据。用户会以为"真的没有"，于是不再重试。
  - **5.1 分类（先判是哪一种，文案完全不同）** `L179` — 最常见的错误：把失败渲染成无数据。用户会以为"真的没有"，于是不再重试。
  - **5.2 结构五件套（Carbon）** `L191` — - 标题必须正向。Carbon 原文举例："Start by adding data assets" 比 "You don't have any data assets" 更好；退一步可用 "还没有…"（带"还"字暗示会变）。
  - **5.3 布局与尺寸** `L205` — - 空间不足就只留文字（Carbon 明确）。塞一张缩小的插画比没有更乱。
  - **5.4 文案公式与中文示例** `L216` — 公式：标题（正向，≤12 字） + 说明（这里会出现什么 + 怎么做，≤30 字） + 按钮（动词，≤6 字）
- **§6 错误状态的分级** `L230` — 404（GOV.UK 原文口径）：
  - **6.1 五级错误与承载位置** `L232`
  - **6.2 页面级错误页的规则** `L242` — 404（GOV.UK 原文口径）：
  - **6.3 错误文案三段式（报错文案怎么写）** `L259` — - ❌ "系统错误，请稍后重试"（三样全缺）
  - **6.4 重试的纪律** `L272` — - 重试按钮始终可见可用，不要倒计时锁死 60s。
- **§7 弹窗、确认与破坏性操作** `L281` — 1. 只给严重后果用：毁掉用户成果、花大钱、不可撤销。
  - **7.1 NN/g 八条（原文提炼）** `L283` — 1. 只给严重后果用：毁掉用户成果、花大钱、不可撤销。
  - **7.2 弹窗尺寸与结构（M3 精确值）** `L294`
  - **7.3 形态选择** `L308`
  - **7.4 危险确认的文案模板** `L317` — - 危险按钮用危险色，取消按钮用中性色。两个都红 = 没有重点。
- **§8 五态数据模型（工程落地）** `L333` — idle → loading → success
  - **8.1 每个数据区块都必须实现的五态** `L335` — partial 是最常被漏掉的一态：一个仪表盘 6 张卡片挂了 2 张，正确做法是其余 4 张正常显示 + 2 张各自显示错误与重试，而不是整页报错。
  - **8.2 列表页的加载序列** `L346`
  - **8.3 保存状态指示（编辑器类必做）** `L356` — 三态文案，位置固定在标题栏或状态栏（位置不变，只变文字）：
- **§9 十个高频场景速查** `L372` — ---
- **§10 可访问性与合规** `L389` — - 定义：不是上下文变化、但向用户传达「操作成功/结果、等待状态、流程进度、存在错误」的内容变化。
  - **10.1 WCAG 4.1.3 状态消息（AA，最容易被忽略的一条）** `L391` — - 定义：不是上下文变化、但向用户传达「操作成功/结果、等待状态、流程进度、存在错误」的内容变化。
  - **10.2 WCAG 2.2.1 时限可调（A）——toast 到底算不算时限？** `L407` — - 规则：内容自设的每个时限，至少满足其一：可关闭 / 可调整（≥默认 10 倍） / 到期前警告并给 ≥20 秒延长，且可延长 ≥10 次；或时限 20 小时（长于一个清醒日）。
  - **10.3 加载动画与 2.2.2** `L414` — - 自动播放、移动、闪烁超过 5 秒的内容，需提供暂停/停止/隐藏（轮播、无限滚动动画、持续闪烁的骨架 shimmer）。
  - **10.4 焦点与播报纪律** `L420` — - toast 不抢焦点；模态抢焦点（打开入框、Esc 关闭、关闭后焦点回触发元素、背景 inert）。
- **§11 中文场景与弱网** `L429` — - toast 文案 ≤14 字（微信默认 1.5s，比 web 短一半）；错误文案 ≤30 字。
- **§12 反模式（逐条对照，命中即改）** `L440` — 1. 用 toast 报严重错误（3s 内消失，用户漏掉）
- **§13 上线自检（15 条，全部可判定）** `L465` — 1. 每次点击/按键，100ms 内有可见变化？
- **§14 可抄代码** `L485` — html
  - **14.1 Toast 容器（预置 aria-live，避免"插入即不播报"）** `L487`
  - **14.2 骨架屏（结构对齐 + 尊重 reduced-motion）** `L510`
  - **14.3 按钮 loading（宽度锁定，不跳版）** `L532`
  - **14.4 危险确认（结构 + 焦点纪律）** `L558` — ---
- **§15 工具与库（2026-11-01 GitHub API 实测）** `L573` — 选型规则：shadcn/ui 项目 → sonner（已内置）；需要严格 a11y 与自控样式 → Radix Toast 自己封装；数据层五态 → TanStack Query 的 status/isFetching/isLoading 

### `references/form-table.md` · 表单与表格 — Forms & Tables（深度蒸馏）
_515 行 · 快照 2026-10-31 · 40 节_

- **0. 30 秒速查** `L8` — 表单
- **1. 表单（Form）的五个零件：标签·控件·帮助·错误·动作** `L39` — 任何表单字段都是这五件套，缺一件就出问题：
- **2. 标签：位置三选一，别混用** `L55` — 决策规则：
  - **2.1 三种对齐的取舍（Ant Design 原文结论，可直接引用）** `L57` — 决策规则：
  - **2.2 标签文案** `L71` — - 句首大写、不加冒号、不加句号（GOV.UK / Carbon 一致要求）。中文对应：不加句号，右对齐可保留冒号（Ant 默认带冒号，labelColonMarginInlineStart: 2px、InlineEnd: 8px）；顶对齐
  - **2.3 标签宽度的具体值** `L78` — - 右对齐：标签列固定宽，取最长标签宽度 + 8–16px，常见 80–120px（中文 4–6 字约 80–100px）。
- **3. 字段宽度：按内容长度定宽（最被忽视的一条）** `L86` — 铁律：输入框宽度传达"预期输入多长"。全部等宽 = 放弃了一条免费提示。
- **4. 控件尺寸与内边距（三体系精确值）** `L110` — 计算式（源码）：paddingBlock = (controlHeight − fontSize × lineHeight)/2 − 1；paddingInline = paddingSM(12) − 1。圆角 6px，边框 1px，聚焦时
  - **Ant Design（中文 B 端事实标准）** `L112` — 计算式（源码）：paddingBlock = (controlHeight − fontSize × lineHeight)/2 − 1；paddingInline = paddingSM(12) − 1。圆角 6px，边框 1px，聚焦时
  - **Carbon（IBM，规格最完整）** `L122` — - 标签 12px（$label-01）、字段文字 14px、帮助 12px、错误 12px
  - **选用建议** `L132` — - 中文 B 端桌面：32–40px 高（Ant 默认 32 偏紧，表单页建议 size="large" 40px）。
- **5. 必填与可选：只标少数派** `L140` — 规则（Carbon 明文）：
- **6. 校验时机：三档，各有明确适用** `L154` — 实现差异（坑）：Ant Design Form.Item 的 validateTrigger 默认 onChange；Semi Design 的 trigger 默认也是 'change'。两个库都要显式改成 ['onBlur','onSu
- **7. 错误文案：模板化，禁止「输入有误」** `L173` — 「格式不正确」「输入有误」「非法字符」——这三句等于没说。合格的错误文案必须包含哪里错 + 怎么改，能给例子就给例子。
- **8. 帮助文字、占位符、前缀后缀** `L203` — 1. 用户一开始输入就消失，回看时无从对照，对记忆障碍用户尤其致命；
  - **占位符的三宗罪（GOV.UK 原文，直接引用）** `L205` — 1. 用户一开始输入就消失，回看时无从对照，对记忆障碍用户尤其致命；
  - **帮助文字（Hint）** `L213` — - 一句话，不加句号（GOV.UK）；英文句首大写。
  - **前缀 / 后缀** `L220` — - 放框外（Ant addonBefore/addonAfter、Carbon 也是外置），不要塞进 placeholder。
- **9. 控件选择矩阵（含中文特有字段）** `L228` — 中文特有字段的硬规则：
- **10. 布局梯度：按内容量选，不按审美选** `L259` — Ant Design 表单页规范给出 4 级梯度，每一级兼容前一级：
- **11. 表单可访问性：可执行清单** `L294` — - [ ] 每个控件都有可见 <label for；占位符不算标签。
- **12. 表格结构：五层 + 行高密度** `L309` — 标题/工具栏 → 表头 → 数据行 → 批量操作条 → 分页
  - **12.1 五层结构** `L311` — 标题/工具栏 → 表头 → 数据行 → 批量操作条 → 分页
  - **12.2 行高：三档够用，别自创** `L319` — Ant Design（源码推算，默认 14px 字号 + 22px 行高 + 1px 分隔线）：
  - **12.3 表头样式** `L337` — - 底色：浅灰填充（Ant colorFillAlterSolid），不加粗黑底——黑底表头在长表里抢注意力。
- **13. 列设计：决定表格好不好用的 80%** `L346` — 等宽数字必开：font-variant-numeric: tabular-nums。比例数字下 1 比 8 窄，数字列会左右跳动，右对齐也白做。
  - **13.1 对齐（最容易错，且有官方依据）** `L348` — 等宽数字必开：font-variant-numeric: tabular-nums。比例数字下 1 比 8 窄，数字列会左右跳动，右对齐也白做。
  - **13.2 列宽** `L364` — - 按内容实际长度分配，不要所有列 flex: 1 均分（名称列被压成两行、备注列空一半）。
  - **13.3 截断与空值** `L371` — - 单行 text-overflow: ellipsis + 悬停 Tooltip 显示全文；关键列（名称/主键）不截断，宁可加宽。
  - **13.4 状态与语义** `L377` — - 状态用文字 + 颜色标签，不只靠颜色（色盲可读）。
  - **13.5 序号列** `L383` — 分页时必须计算全局序号：(currentPage − 1) × pageSize + index + 1。直接渲染 index + 1 是常见 bug（每页都从 1 开始）。
- **14. 表格规模化：分页、固定、批量、空态** `L389` — - 默认 pageSize：Ant 是 10；B 端列表建议 20，并提供 10/20/50 切换（Ant showSizeChanger）。
  - **14.1 分页 vs 滚动** `L391` — - 默认 pageSize：Ant 是 10；B 端列表建议 20，并提供 10/20/50 切换（Ant showSizeChanger）。
  - **14.2 固定与滚动** `L403` — - 行数 15 或表格高度受容器限制 → 固定表头（sticky/position: sticky）。
  - **14.3 批量操作** `L410` — - 表头复选框三态：全选 / 未选 / 不确定（indeterminate，部分选中）。
  - **14.4 空态、加载、错误** `L417` — ---
- **15. 表格可访问性与中文细节** `L429` — 语义与键盘：
- **16. 反模式清单（逐条给改法）** `L452` — 1. 占位符当标签 → 加可见标签，占位符只留格式示例。
- **17. 交付自检（表单 10 + 表格 10）** `L475` — 表单
- **18. 出处** `L503` — - Ant Design · 表单（pattern）— 标签对齐优缺点、按钮对齐、主按钮禁用规则、校验三档、输入提示/提醒：2x.ant.design/docs/pattern/form-cn

### `references/handoff-collaboration.md` · 设计交付与协作 / Design Handoff & Collaboration
_851 行 · 快照 2026-11-01 · 73 节_

- **1. 一页速查：交付链的六个关卡** `L9` — 设计交付不是"发个链接"，是六次信息交接。每一次交接都会掉信息，掉的那部分最终会以返工的形式回来。
- **2. 交付的本质：交付决策，不是交付图** `L26` — 一张设计稿里其实有三层信息，交付时经常只传了最表面的一层：
- **3. 交付物清单：spec sheet 的 9 个字段** `L50` — Carbon 把设计规格（design spec）定义为"开发用来在代码里构建组件、设计师用来在 Figma 里构建组件的蓝图，是视觉外观与功能的唯一事实来源"。它要求的六类内容，加上中文项目实际要的沟通字段，合成 9 项：
- **4. 标注规则：标例外，不标全量** `L79` — Carbon 2x Grid 的硬数值（可直接抄）：
  - **4.1 先把网格定死，标注量会掉一个数量级** `L81` — Carbon 2x Grid 的硬数值（可直接抄）：
  - **4.2 spacing token 13 档（Carbon 官方精确值）** `L103` — Carbon 对"能不能用阶梯外的值"的回答是明确的："偏离 spacing 阶梯应尽可能避免"。百分比（50% / 33%）可用于分栏与 max/min 宽度，但不能当间距。
  - **4.3 只标这四类，其余靠 token 与网格** `L123` — 不要标：每一条 8px 的间距、每个 padding、每个已经 token 化的圆角。全量标注的副作用是开发看不见重点——满屏红线等于没有红线。
  - **4.4 单位换算写清楚** `L134` — - 设计稿用 px，代码多用 rem；1rem = 16px 时 24px = 1.5rem、8px = 0.5rem。
- **5. 状态矩阵：9 态，别画 2ⁿ** `L142` — Carbon 列的交互态是 7 个：hover / focus / selected / disabled / read-only / error / warning。加上设计侧必须补的两个：
  - **5.1 组合爆炸的控制** `L160` — 一个按钮 3 尺寸 × 2 类型 × 9 状态 = 54 个变体。不要全画，按下面三刀砍：
  - **5.2 disabled 的对比度例外，别用错地方** `L170` — Carbon 明确写了 4.5:1 "with the exceptions of disabled states"。这条例外只给 disabled——read-only、placeholder、辅助文字、暗色下的次级文字都不适用。把"看起
- **6. 命名四套：图层 / 组件 / 变体 / token** `L176` — 命名的唯一标准：能不能不打开文件就找到它。
  - **6.1 Figma 的斜杠规则（官方机制，不是审美）** `L180` — - 组件名里每个 / 生成一级层级：Button/Primary/Large → 资产面板里 Button Primary Large。
  - **6.2 四套命名规则** `L190`
  - **6.3 为什么"红色"是坏名字** `L199` — color=red 把实现写进了语义。品牌换成紫色那天，red 变成谎言，而且所有调用点都要改。正确写法是 type=danger，颜色由 token 决定。同理：size=big → size=lg（与代码 prop 对齐）、style=
  - **6.4 token 的 CTI 结构** `L205` — Style Dictionary 推荐的 Category / Type / Item 三层（非强制，但用了就不会出现"到底叫 buttoncolorerror 还是 errorbuttoncolor"的争论）：
  - **6.5 中文项目的命名纪律** `L216` — - 图层与组件名统一英文，中文只出现在文案内容与注释里。混写会导致：搜索失效、导出文件名乱码、Figma 插件解析失败。
- **7. 组件 API 与设计稿 1:1 对齐** `L224` — 设计属性与代码 props 必须是同一套词表，否则每次交付都要做一次人工翻译。
  - **7.1 Figma 的四类组件属性** `L228` — Boolean 命名用 is/has/can/show 前缀，默认值取最常见的那个（通常是 false）。默认值错了，每个实例都要手动改一次。
  - **7.2 属性数量的经验上限** `L239` — Figma 官方没有上限，但组合数是乘积：3 属性 × 5 值 = 125 个变体，光是加载就会拖慢文件（官方明确：Importing large component sets will impact Figma's speed and p
  - **7.3 三条官方级禁令** `L245` — 1. 不要用变体分组不同图标（Figma 原文："We don't recommend using variants to group different icons"）。同图标不同尺寸可以，不同图标不行——图标应该各自是组件，靠 Icon
  - **7.4 Code Connect：让开发者看到"你的组件"而不是"自动生成的 div"** `L251` — Dev Mode 默认给的是自动生成代码（可切语言与单位，CSS 单位可改）。接上 Code Connect 后，开发者看到的是设计系统库里真实的组件代码，变体与属性被映射到真实 props。
- **8. 验收标准的写法：Given / When / Then** `L259` — 走查之所以吵，是因为没有事先写"该是什么样"。AC（验收标准）就是那份"该是什么样"。
  - **8.1 Gherkin 的三段语义（官方定义）** `L263` — 官方硬建议：每个场景 3–5 步；步数过多就失去"规格说明"的表达力。Background 复用重复前置，但超过 4 行就该上提成更高层的步骤。
  - **8.2 设计 AC 的五条模板** `L273`
  - **8.3 三种写坏的 AC** `L290` — ---
- **9. 设计评审（critique）：30 分钟，2 正 1 改** `L300` — NN/g 明确区分：
  - **9.1 先分清两种"评审"** `L302` — NN/g 明确区分：
  - **9.2 有效评审的三个前提（NN/g 原文三主题）** `L316` — 1. 范围清晰：这次评什么、不评什么，必须写死。范围不清的评审 100% 会跑偏。
  - **9.3 两种主持方法** `L322`
  - **9.4 角色与节奏** `L329` — - Presenter：讲目标 → 讲故事（遇到什么问题、为什么这么决策）→ 明确提出想要哪类反馈。快速讲完，别为每个决策辩护——辩解会吃掉真正讨论的时间。
  - **9.5 把意见翻译成问题（reframing）** `L338` — 规则：所有反馈必须挂在目标上。挂不上目标的，是个人偏好，记录但不执行。
  - **9.6 五个坑（NN/g 原文）** `L347` — 1. 事先没对齐人物画像/目标
- **10. 设计走查（design QA）：三遍法 + 9 字段文档** `L359` — 设计走查（又叫还原度检查、视觉 Review、设计验证）的目的是保证落地效果与设计稿一致。它在开发完成后的测试阶段进行，是上线前最后一道质检。
  - **10.1 定义与边界** `L361` — 设计走查（又叫还原度检查、视觉 Review、设计验证）的目的是保证落地效果与设计稿一致。它在开发完成后的测试阶段进行，是上线前最后一道质检。
  - **10.2 时机** `L376` — - 在计划提测时间介入：测试同学跑完第一遍流程后开始走查——太早页面还在动，太晚改不动。
  - **10.3 三遍法：先大后小，先流程后像素** `L382` — 为什么不能先抠像素：先抠像素会让你在一条本来就走不通的流程上纠结 2px，而真正的阻断问题排在清单末尾。
  - **10.4 走查文档的 9 个字段** `L392` — 一条一问题。把 5 个问题写进一行，结果一定是修了 3 个、漏了 2 个、还吵了一架。
  - **10.5 沟通纪律** `L408` — 1. 邮件/文档正式发出：正式渠道提高重视度，也留痕（原文："防止日后被甩锅"）。
  - **10.6 走查环境的六个变量（缺一个就会吵）** `L415` — 机型 / 系统版本 / 屏幕分辨率 / 浏览器与版本 / 系统缩放或字体大小 / 是否暗色模式。
- **11. 缺陷分级与发布门禁** `L423` — 分级只看一件事：用户还能不能完成他的目标。不看"改起来多贵"，也不看"谁写的"。
- **12. 版本与变更管理** `L442` — 废弃的正确姿势（SemVer FAQ 原文要点）：① 更新文档告知；② 发一个带废弃声明的 MINOR；③ 在下一个 MAJOR 里才彻底移除——中间至少隔一个 MINOR，让使用方平滑迁移。
  - **12.1 SemVer 2.0.0 的 11 条（设计系统直接照搬）** `L444` — 废弃的正确姿势（SemVer FAQ 原文要点）：① 更新文档告知；② 发一个带废弃声明的 MINOR；③ 在下一个 MAJOR 里才彻底移除——中间至少隔一个 MINOR，让使用方平滑迁移。
  - **12.2 映射到设计系统** `L462` — "改默认值"是最容易被误判成 PATCH 的 MAJOR。默认值一改，所有没显式传值的调用点视觉全变——这是不兼容变更。
  - **12.3 变更日志格式（Keep a Changelog 六类）** `L472` — Added / Changed / Deprecated / Removed / Fixed / Security。每条写影响面，不只写"优化了按钮"：
  - **12.4 MAJOR 必须带 codemod** `L484` — Carbon 的要求写得很直白：如果变更需要消费方迁移，就必须提供自动化迁移脚本（通过 @carbon/upgrade 发布）。理由是"迁移成本乘以所有团队，会显著影响整体产出"。
  - **12.5 三个版本号不要混** `L490` — 事故高发点：设计稿写"v3"，组件库已经到 2.4.0，产品是 5.1.2，三方对不上。交付文档里必须同时写清三个版本号。
- **13. Token 交付管线：从设计变量到代码** `L502` — base（原始值）→ semantic（语义角色）→ component（组件覆盖）。组件层只引用后两层，禁止硬编码。Carbon 的原话是"组件样式不得包含未 token 化的魔法数字或颜色"。
  - **13.1 三层不要混（详见 design-tokens.md）** `L504` — base（原始值）→ semantic（语义角色）→ component（组件覆盖）。组件层只引用后两层，禁止硬编码。Carbon 的原话是"组件样式不得包含未 token 化的魔法数字或颜色"。
  - **13.2 W3C DTCG 格式（2025.10 草案）** `L508` — ⚠️ 重要前提：官方明确标注这是预览草稿（Draft Community Group Report），"请勿直接据此实现"，它既不是 W3C 标准，也不在标准轨道上。用它做交换格式可以，用它做合规承诺不行。
  - **13.3 Style Dictionary 的构建规则** `L547` — 标准管线：
  - **13.4 token 交付的五条纪律** `L570` — 1. 一个 token 一个用途。color-blue-500 可以给多处用；color-button-bg 只能给按钮用。语义 token 被复用成"万能色"，改一次全站崩。
- **14. 回归防线：让"改 A 崩 B"在合并前被发现** `L580` — Carbon 的测试要求可以直接当行业基线：
  - **14.1 工具实测（2026-11-01 · GitHub API）** `L591` — 选型建议：
  - **14.2 设计侧的"回归"：比代码更早** `L611` — Figma Dev Mode 自带两种 diff，走查前先用它们自查：
- **15. 协作节奏：每次交接都要有可验收的产出** `L622`
  - **15.1 冻结后要改怎么办** `L640` — 变更单四问（写不清就不改）：
  - **15.2 异步优先** `L651` — - 设计稿提前发（评审前至少半天），避免"现场第一次看"的直觉反应。
- **16. 中文/本土交付现实** `L661` — 1. Spec（该是什么样）
  - **16.1 术语对齐表（对外沟通直接用）** `L663`
  - **16.2 交付包清单（对外/外包/甲方）** `L675`
  - **16.3 三份签字文件** `L686` — 1. Spec（该是什么样）
  - **16.4 合规口径（政府/金融/医疗/适老化项目）** `L694` — - 无障碍常要求 GB/T 37668 + WCAG 2.1/2.2 AA 双达标（详见 accessibility.md §15）。
  - **16.5 三句可以直接用的话** `L700` — ---
- **17. 度量：交付质量的六个指标** `L710` — 说明：下面是建议基线（本技能立场），不是行业统计数据。目的是让"交付好不好"从感觉变成可讨论的数字。第一轮先测自己的基线，第二轮再谈改善。
- **18. 反模式 20 条** `L730` — 1. 只交图不交规则——开发反推，偏差从第一个像素开始。
- **19. 自检 20 项（交付前逐条打勾）** `L755` — 1. 拿掉设计稿，开发只看文档能做出第二个页面吗？
- **20. 四个可抄模板** `L780` — markdown
  - **20.1 Spec sheet（组件级）** `L782`
  - **20.2 走查表（一行一条）** `L799`
  - **20.3 AC（五条一组）** `L808`
  - **20.4 变更日志（六类）** `L818` — ---
- **数据来源** `L837` — - Carbon · Component checklist（definition of done） — 设计规格六类要求、代码/测试/设计包四组清单、80% 覆盖率、VRT/AVT/三读屏器

### `references/i18n-localization.md` · 国际化与本地化设计（i18n / L10n / RTL / 多语言）
_1058 行 · 快照 2026-11-05 · 68 节_

- **一、判层：国际化与本地化 i18n / L10n / 翻译 / 多语言 / RTL 不是同一件事** `L11` — 先分层，否则会把「加个语言包」当成全部工作。
  - **1.1 什么时候要读本文件** `L29` — ---
- **二、文案膨胀 text expansion / 翻译后按钮被截断 / 字数变长：翻译后文字变长、按钮放不下，+40% 不是安全值** `L44` — 本轮最重要的一条修正。 现有 ux-writing.md §13 写「按钮和标签必须能容纳 +40% 的文字长度」，Microsoft 伪本地化也给「+40%」启发式——但对短字符串而言这是错的，而且错得刚好落在按钮、标签、tab 这些最容
  - **2.1 W3C / IBM 官方膨胀表（逐字取，不要自行「修正」）** `L48` — W3C《Text size in translation》转引 IBM《Guidelines to design global solutions》，给出英译欧洲语言的平均预期膨胀率：
  - **2.2 Flickr "views" 实测比例表（W3C 原文）** `L63` — 同一个短词 views（Flickr 的「392 views」），翻译成各语言的长度比（以英文为 1）：
  - **2.3 裁决：+40% 用在哪、2–3× 用在哪** `L81` — 三个来源并不矛盾，它们说的是不同长度档：
  - **2.4 四类「不只是变长」的复杂因素（W3C 原文）** `L101`
  - **2.5 布局弹性清单（可交付给前端）** `L110` — - [ ] 所有文字容器用 min-inline-size / max-inline-size，不用固定 width；inline-size: fit-content + max-inline-size 是常用组合。
- **三、lang 与 dir：BCP 47 语言声明、RTL 方向、WCAG 3.1.1 / 3.1.2** `L124` — 标记层是无障碍硬要求，不是「锦上添花的语义」。
  - **3.1 WCAG 2.2 原文** `L128` — - 3.1.1 的充分技术 H57：在 HTML 元素上使用语言属性。WAI 明确：页面多语言时，默认语言取用得最多的那种；若几种用得一样多，取最先出现的那种。
  - **3.2 lang 的规则与反模式（W3C《Declaring language in HTML》）** `L140` — 必须：
  - **3.3 dir：方向是标记层的，不是样式层（W3C《Structural markup and RTL text in HTML》）** `L169` — - dir 用于设置 base direction，以便 Unicode 双向算法（UBA） 正确重排文本，同时设置段落默认对齐。支持 RTL 脚本：Adlam、Arabic、Hebrew、N'Ko、Syriac、Thaana（W3C 列举
  - **3.4 dir="auto" 与 dirname** `L193` — dir="auto"（W3C）：浏览器查看元素内第一个强方向字符（first strongly typed character）决定该元素的 base direction。
  - **3.5 行内双向文本（W3C《Inline markup and bidirectional text in HTML》）** `L216` — 统一做法，不要逐例判断：把每一个反方向短语用 dir 紧包裹（tightly wrap = 元素包含整个反方向短语，且只包含它）。dir 不仅设 base direction，浏览器还会方向隔离（directionally isolate）
- **四、CSS logical properties：逻辑属性 inline / block、start / end 与 RTL 自动镜像** `L237` — MDN 定义：CSS Logical Properties and Values 模块定义「与书写方向相对」而非「与物理方向绑定」的属性。
  - **4.1 两根轴** `L241` — MDN 的关键句：「The start of a line is not always the left side of a line.」 流相对值：block-start / block-end / inline-start / inli
  - **4.2 物理 → 逻辑全映射（MDN 精确属性名）** `L250` — 简写：margin-block / margin-inline、padding-block / padding-inline、border-block / border-inline、inset / inset-block / inset-
  - **4.3 什么时候仍然用 left / right** `L283` — W3C：「Left and right values may still be useful, occasionally, if you want the item you are positioning to remain in a fi
  - **4.4 常见漏网点** `L287` — - transform: translateX(20px) / rotate() 不会自动镜像，需要按 dir 显式分支或改写成逻辑方向。
- **五、RTL 镜像规则：该镜像与不该镜像清单（Material Design Bidirectionality 官方）** `L298` — Material 定义：把 UI 从 LTR 切到 RTL 通常叫 mirroring，RTL 布局是 LTR 布局的镜像，影响 layout / text / graphics。时间的流逝在 LTR 里表现为左→右，RTL 里表现为右→左
  - **5.1 应该镜像（白名单）** `L302`
  - **5.2 不应该镜像（黑名单）** `L321`
  - **5.3 三个最易错的边界** `L336` — 1. 一般进度条 vs 媒体进度条：Material 一边说「Progress bars fill in the same direction as content is read」，一边说「Do not mirror media play
  - **5.4 Material 2 的精确数值（RTL 前后保持相同，变化的是左右归属）** `L342` — 平台支持（Material 官方标注）：Android / iOS / Web / Flutter 均 Available。
  - **5.5 RTL 页面验收动作** `L359` — 切到 dir="rtl" 后逐项看：返回箭头方向、主次按钮顺序、checkbox 在文字右侧、字段图标换边、tab 起始位置、进度条填充方向、图标镜像白名单是否误伤黑名单、数字是否仍是 LTR 且字形正确、URL/品牌名是否保持 LTR、标
- **六、复数 plural：CLDR 六类、ICU 复数规则、不同语言复数形式（Node 实测）** `L365` — CLDR 使用 6 个助记标签：zero / one (singular) / two (dual) / few (paucal) / many（也用于有独立类别的分数）/ other（required — general plural f
  - **6.1 CLDR 官方类别（逐字取）** `L367` — CLDR 使用 6 个助记标签：zero / one (singular) / two (dual) / few (paucal) / many（也用于有独立类别的分数）/ other（required — general plural f
  - **6.2 CLDR 49 语言复数规则图表：各 locale 的 cardinal 类别** `L380` — 口径：只看 cardinal（普通名词/单位复数）。图表另有 ordinal 与 range 行，例如 en 的 ordinal 有 one/two/few/other，不要混进 cardinal 的表。
  - **6.3 Node v22.22.2 Intl.PluralRules 本机实测（本章最有价值的表）** `L393` — new Intl.PluralRules(locale).select(n) 实测输出：
  - **6.4 设计含义** `L422` — - 任何含数量的 UI 文案（「已删除 N 项」「N 条未读」「N 天前」）都必须走 ICU plural / selectordinal，不能写 n === 1 ? A : B。
- **七、ICU MessageFormat：禁拼接字符串、单句完整翻译、select / plural / selectordinal** `L431` — ICU 用户指南的出发点直接点名拼接的危害：「If the user-visible string were concatenated directly from fragments and formatted elements, then
  - **7.1 三种复杂参数** `L435` — - plural：按数值 + 该语言复数规则选子消息
  - **7.2 官方示例（逐字取，含 offset 与 #）** `L442` — - offset:1：把「主人本人」从计数里扣掉，# 输出的是 扣除 offset 后的值（不是原始 numguests）。
  - **7.3 嵌套顺序的官方建议** `L461` — 「If possible, use complex arguments as the outermost structure of a message, and write full sentences in their sub-messa
  - **7.4 引号 / 转义（最容易踩的坑）** `L469` — - 语法字符在文本部分要用成对的 ASCII 撇号包起来；一对 ASCII '' 代表一个 ASCII '，类似 printf 的 %%：
  - **7.5 参数格式化的官方取舍** `L476` — 官方示例输出 At 4:34 PM on March 23, there was a disturbance in the Force on planet 7. 的模式：
  - **7.6 反模式速查** `L491` — - ❌ "Welcome " + name + "!"（语序可能不同）
- **八、Intl API 全表与本机实测（Node v22.22.2）** `L502` — MDN 官方定义：Intl is not a constructor —— 不能用 new，也不能当函数调用；所有属性和方法都是静态的（类似 Math）。它是 namespace object，里面装的是构造器与公共能力。
  - **8.1 完整清单** `L506` — 实测能力警告（本轮独有）：MDN 列出了 Intl.DurationFormat，但本机 Node v22.22.2 执行 new Intl.DurationFormat('zh', ...) 抛 TypeError: Intl.Durat
  - **8.2 Intl.Locale 元数据实测（日历 / 数字系统 / 周 / 方向）** `L528` — 设计含义：日历控件的周起始日和周末必须按 locale 取，不能写死周一或周日——实测 zh-CN 周一、en-US 周日、ar-EG 周六（firstDay 6）、he-IL 周日；ar-EG 周末是周五+周六。这也是「多语言日历」最高频
  - **8.3 语言协商（locale negotiation）与 navigator** `L541` — MDN：所有国际化构造器都接受 locales + options，用 options.localeMatcher 指定的算法，把请求的 locale 与实现支持的 locale 协商。
- **九、日期 / 时间 / 日历 / 时区格式（Node 实测）** `L564` — 同一个 Date('2026-03-09T16:05:00Z')，dateStyle:'full'、timeZone:'UTC'：
- **十、数字 / 货币 / 单位 / 千分位格式（Node 实测）** `L593` — Intl.NumberFormat 格式化 1234567.89：
- **十一、列表 / 相对时间 / DisplayNames / 排序 Collator / 中文分词 Segmenter（Node 实测）** `L622` — 规则：
- **十二、姓名 / 地址 / 称呼：不要 first name + last name（W3C《Personal names around the world》）** `L645` — W3C 开宗明义：设计表单/数据库/本体的人常常不知道别国姓名可以有多不同，于是假设过多。
  - **12.1 官方点名的反例（按类型）** `L649`
  - **12.2 官方设计建议（可直接作为表单规范）** `L664` — 首选：单一 Full name 字段，按用户原样输入。W3C：「it will be simpler, where it is possible, to just use the full name as the user provides
- **十三、语言协商 locale negotiation 与回退策略** `L692` — 把 §8.3 的运行时规则落到产品上：
- **十四、伪本地化 pseudolocalization / 伪翻译 / 伪 locale（Microsoft Learn 官方）** `L707` — 定义：不真的翻译，用自动转换源文本来模拟翻译的常见副作用，在翻译开始前就能验证产品可本地化性，并贯穿整个开发周期持续回归。Microsoft 说这些手段在圈内简称 "pseudo"。
  - **14.1 伪翻译的五种变换（官方原文）** `L711` — 另两个官方要点：
  - **14.2 伪 locale（专测格式化与解析）** `L727` — Windows 定义三个伪 locale：
  - **14.3 可执行的伪本地化验收流程** `L743` — 1. 全站切到 en-XA（或自定义 40% 加长 + 音标 + ^ 定界）→ 检查截断、换行、重叠、min-inline-size 是否生效。
- **十五、文化适配：颜色、图标、图像、示例数据与数字字形** `L755` — - 颜色含义不通用：ux-writing.md §13 给的例子是白色在西方=婚礼、东亚=丧礼。做法不是「背一张颜色文化表」，而是为目标市场做一次调研并写进 locale brief，尤其语义色（成功/危险/警告）与营销主色。同时注意：da
- **十六、给译者的交付规格：字符预算、变量说明、截图与术语表（与 handoff-collaboration.md 衔接）** `L768` — 翻译不是「把 JSON 发出去」。每条消息应带：
- **十七、框架与工程落地：React / Vue / Next / MUI RTL、字体、能力检测** `L788` — NOASSERTION 表示 GitHub API 的 license.spdxid 未给出标准 SPDX 值（多为自定义/多许可/未标注），不是「无许可」；采用前须查仓库 LICENSE 原文。本表只记实测结果，不臆测。
  - **17.1 生态仓库（GitHub API 实测 2026-11-05，star / license / 最近推送）** `L790` — NOASSERTION 表示 GitHub API 的 license.spdxid 未给出标准 SPDX 值（多为自定义/多许可/未标注），不是「无许可」；采用前须查仓库 LICENSE 原文。本表只记实测结果，不臆测。
  - **17.2 落地纪律** `L807` — - 字符串全部外置，组件内不出现面向用户的字面量；数字/日期/复数不进消息目录，交给 Intl。
- **十八、12 个场景速查** `L819` — ---
- **十九、20 条反模式** `L838` — 1. 把「加个语言包」当成国际化全部工作（漏掉标记层、布局层、数据层）。
- **二十、20 项自检（出海交付前逐条过）** `L863` — 1. <html 上有正确且完整的 lang（BCP 47 / IANA），不是 body、不是 meta？
- **二十一、6 段可抄代码** `L888` — html
  - **21.1 文档骨架：lang + dir + 逻辑属性基线** `L890`
  - **21.2 复数/选择：ICU MessageFormat（完整单句 + select 外层）** `L926`
  - **21.3 按 locale 安全的格式化封装（含能力检测）** `L947`
  - **21.4 语言协商 + 周起始日 / 方向兜底校验** `L966`
  - **21.5 伪本地化变换（含 200% microcopy 档）** `L984`
  - **21.6 CI 静态检查：硬编码方向 / 物理属性 / 缺失 lang** `L1002` — ---
- **二十二、数据来源（官方原文 + API 实测）** `L1024` — W3C / WAI

### `references/iconography.md` · 图标设计系统 · Iconography
_338 行 · 快照 — · 26 节_

- **0. 一句话立场** `L6` — 图标是「视觉速记」，不是「装饰」。 它只在「图形比文字更快被识别」时胜出；其余场景要么配文字，要么直接用文字。图标系统的全部工作，是把这套「识别」做到跨尺寸可读、跨库一致、跨工具可达。
- **1. 何时用图标 / 文字 / 两者（决策树）** `L12` — 反模式预警：用图标替代一切文字 = 把可用性赌在用户的「图标素养」上；国际化和首因效应都会反噬。
- **2. 图标网格系统（Grid & Keylines）** `L25` — - viewBox 统一 24×24（Lucide / Material / Heroicons outline / Feather / Carbon / Fluent 默认）。这是行业事实标准，导出 SVG 一律 viewBox="0 0
  - **2.1 基础网格** `L27` — - viewBox 统一 24×24（Lucide / Material / Heroicons outline / Feather / Carbon / Fluent 默认）。这是行业事实标准，导出 SVG 一律 viewBox="0 0
  - **2.2 Keylines（关键形，Material 体系权威取值）** `L32` — 同一套图标里，相同语义类别的图形必须贴同一 keyline，否则视觉重量会飘。这是「跨库一致」的地基。
- **3. 描边与笔画（Stroke）** `L44` — 铁律：
- **4. 尺寸阶梯（Sizing Scale）** `L67` — - 密度驱动：紧凑界面默认 16，宽松默认 20–24；不要一套尺寸打天下。
- **5. 图标与文字间距（Icon–Text Spacing）** `L84` — - 默认 8px（图标 16–20 配 14–16px 文字）。Material/Carbon/Heroicons 一致推荐 8px。
- **6. 填充 / 描边 / 双色（Fill · Stroke · Duotone）** `L93` — - 状态用填充切换：选中态把描边图标 FILL 0→1（Material），或描边→实心（Heroicons），让用户「看到」状态而非只靠颜色。
- **7. 光学对齐与修正（Optical Alignment）** `L107` — - 视觉居中 ≠ 几何居中：圆形/三角形比方形「显小」，需向中心过冲 1–2%（overshoot）才显得等大。
- **8. 状态图标（State Icons）** `L116` — - 加载转圈（spinner）：rotate 动画，1–1.4s linear infinite（连续无限循环，呼应 motion-system.md 持续型 ≤1.4s）。不要用 ease（会一顿一顿）。
- **9. 交付格式（Delivery Formats）** `L126` — - Material Symbols 字体体积实测：默认全量 295 KB；按 iconnames 子集化 1.7 KB；全变量轴 7.9 MB → 必须子集化，且加 &display=block 防 FOUC。
- **10. 可访问性（Accessibility）⚠️ 高频翻车点** `L140` — 图标字体最大坑：读屏会把连字念成「home settings」之类乱码 → 必须 aria-hidden 整字库，另用视觉隐藏文字兜底。
- **11. 动画（Animation）** `L157` — - spinner：rotate 360deg + 1–1.4s linear infinite。
- **12. 命名与交付清单（Naming & Delivery Checklist）** `L167` — - 命名 kebab-case：arrow-right.svg、user-settings.svg；与库约定一致（Material 用 snakecase arrowforward，混用前先定约）。
- **13. 库选型矩阵（Library Matrix · GitHub API 实测）** `L179` — ¹ Lucide 在 GitHub API 返回 NOASSERTION（GitHub 未自动归类标准 SPDX；社区实际以 ISC 发布）——商用前以仓库 LICENSE 文件为准。
- **14. 与既有参考的接线（Wiring）** `L200` — - patterns.md：图标是「元素设计模式」的高频项，本文补其精确数值。
- **15. 12 场景（Scenarios）** `L213` — 1. 工具栏仅图标按钮 → icon-only + aria-label + 44 命中区
- **16. 20 反模式（Anti-patterns）** `L230` — 1. 用图标替代一切文字（赌用户图标素养）
- **17. 20 自检（Self-checks）** `L255` — - [ ] 每个图标 viewBox 都是 0 0 24 24？
- **18. 可抄代码（Copy-paste）** `L280` — svg
  - **18.1 SVG 模板（24 网格 · currentColor · 可访问）** `L282`
  - **18.2 React 图标组件（tree-shaking + currentColor）** `L301`
  - **18.3 spinner（尊重 reduced-motion）** `L317`
  - **18.4 Material Symbols 子集化（防 295KB）** `L326` — ---
- **19. 取源与验证（Sources & Verification）** `L333` — - 官方文档（读原文）：Lucide Guide、Google Material Symbols Guide、Ant Design Icons（默认 1em、Outlined/Filled/TwoTone、currentColor）、Her

### `references/inspiration.md` · 灵感与阅读 — Inspiration
_153 行 · 快照 2026-10-29 · 4 节_

- **用法** `L5` — 按需求关键词定位：做 Web/UI 视觉调研 找 Galleries 里对应领域的站点；想 系统提升审美与方法论 读 Reading 里的小节。
- **Galleries (103)** `L9` — - 60fps — Recordings of interfaces that move well.
- **Reading (33)** `L115` — - Interface Craft — Articles exploring modern digital interface craftsmanship.
- **Other (1)** `L151` — - gaki — GAKI 的个人空间：想法、实验、与 AI 一起动手的过程，以及逐渐成形的作品。

### `references/knowledge-map.md` · 设计能力知识路线图 — Knowledge Map（L0→L4）
_686 行 · 快照 2026-11-05 · 60 节_

- **全景：五级台阶与对应产出** `L9` — 级别不是资历，是任务类型。 同一份工作里会反复上下：做落地页是 L0→L1→L2→L3 直落；被问"这版好不好"是 L4 单点。
- **L0 · 视觉感知：先治"看不出来"** `L23` — 为什么排第一：绝大多数"设计不好"不是技法问题，是看不出问题。没有分辨力，学再多规范也只是套模板。
  - **核心概念（4 个）** `L27` — 1. 层级（Hierarchy）——一屏只有一个主角。判断法：眯眼看，还能分清主次吗？
  - **必读材料** `L33` — - 本技能 portfolios.md：选 5 个作品集，逐站回答"它的主角是谁、靠什么手法突出"
  - **练习（必须落成文字）** `L40` — 取任意两个同类站点（如两个 SaaS 首页），写 300 字对比：
  - **验收标准** `L45` — 能对任何界面在 60 秒内说出：主角、视觉路径、最弱的一环。做不到就还在 L0。
- **L1 · 界面语汇：从"感觉"到"构型"** `L50` — 为什么：设计师和普通人的差别不是审美，是知道有几种做法。只会一种做法的人，遇到不合适的场景就只能硬套。
  - **核心概念** `L54` — 1. 构型谱系——每个元素有 4–6 种主流构型，各有适用场景（见 patterns.md）
  - **必读材料** `L60` — - 本技能 patterns.md：12 类元素，每类「构型 → 参数 → 变体 → 速配 → 常见错误」
  - **练习** `L67` — 任选一个元素（导航栏/定价表/表单），产出 4–6 个构型变体的真实渲染设计板（不是截图、不是链接）。
  - **验收标准** `L70` — 给一个元素 + 场景（"文档站导航"），能直接说出该选哪种构型、为什么、参数取多少。答"看情况"就是没学会。
- **L2 · 系统秩序：从"页面"到"系统"** `L75` — 为什么：单个页面好看靠手艺，一整套产品好看只能靠系统。这一步是从"做图"跨到"做设计"。
  - **核心概念** `L79` — 1. 三层 token 架构：base（原始值）→ semantic（语义角色）→ component（组件专用）
  - **必读材料** `L86` — - 本技能 design-tokens.md：Ant Design 数值体系全量蒸馏 + 三大体系对比 + 中文设计系统矩阵
  - **练习** `L94` — 给一个虚构产品写出完整 token 表：12 个语义色 + 5 档字阶 + 8 档间距 + 3 档圆角 + 3 层阴影，并注明每项使用场景。
  - **验收标准** `L97` — token 表能直接翻译成 CSS 变量且无歧义；同一份表能同时生成浅色与深色两套。
- **L3 · 工程落地：从"稿"到"跑起来"** `L102` — 为什么：设计的最终形态是运行中的界面。不懂实现的约束，就会设计出做不出来的东西（或成本高 10 倍的东西）。
  - **核心概念** `L106` — 1. 技术栈匹配：React/Vue/纯 HTML，选库先看栈再看元素覆盖
  - **必读材料** `L113` — - 本技能 component-libraries.md：14 库元素覆盖矩阵 + 选型规则 + 维护协议
  - **练习** `L121` — 把一个 L1 设计板里的变体，用选定组件库实现为可运行页面，并跑一次 Lighthouse。
  - **验收标准** `L124` — 交付物能跑、能响应式、Lighthouse 可访问性 ≥ 90。
- **L4 · 判断与品味：在冲突约束下取舍** `L129` — 为什么：真实项目里需求永远自相矛盾（"要高级又要热闹""信息多又要留白"）。L4 的能力是给立场，不是列选项。
  - **核心概念** `L133` — 1. 约束识别：分清"硬约束"（品牌色、法务文案、性能）与"软偏好"（个人喜好）
  - **必读材料** `L140` — - Ant Design 设计价值观：自然/确定性/意义感/生长性——评价设计的内在标准
  - **练习** `L146` — 拿一个真实需求，写一份可行性 × 美观性预判：3 条风险、每条给缓解方案、最后给"做什么/不做什么/先做什么"。
  - **验收标准** `L149` — 结论有立场、有理由、有代价说明；被反驳时能说清"我为什么仍这样判断"。
- **三十一条专题支线（可与主线并行）** `L154` — 中文不是"英文换字"。字号要 +1~2px、行高要 1.6–1.8、标点全角、避头尾、中英混排要间距。
  - **支线 A · 中文场景（中文项目必走）** `L156` — 中文不是"英文换字"。字号要 +1~2px、行高要 1.6–1.8、标点全角、避头尾、中英混排要间距。
  - **支线 B · 数据可视化** `L160` — - 原则：准确 / 有效 / 清晰 / 美（AntV 四原则）；Data-ink Ratio 最大化
  - **支线 C · 动效（界面"活"起来的那一层）** `L169` — - 三种合法用途：反馈 / 引导（空间关系、过程）/ 个性（每页 ≤1 处）
  - **支线 D · 可访问性（不是"加分项"，是交付门槛）** `L178` — - 四档对比度：正文 4.5:1 / 大文本 3:1（≥24px 或 ≥18.5px 粗体）/ 非文本 3:1 / AAA 正文 7:1。不可四舍五入（4.499:1 不达标）。
  - **支线 E · 反馈与状态（"有没有回应"决定可不可信）** `L188` — - 五层反馈：L0 微反馈（≤120ms）/ L1 toast（3–5s）/ L2 就地状态（常驻）/ L3 模态 / L4 结果页。严重度决定层级，不决定颜色。
  - **支线 F · 版式与网格（海报 / 长图 / 社媒图 / 印刷）** `L198` — - 先判载体：观看距离决定字号，停留时长决定信息量，媒介决定安全区。海报 1–5m 看 3 秒，长图 30cm 连续滑，社媒图缩略图只有 120px。
  - **支线 G · 品牌视觉与 Logo（做"一个品牌"而不是"一个页面"）** `L208` — - 顺序不能反：定位（3 个形容词 + 3 个反义词）→ 语言（形/色/字/图/动/声）→ 系统（token 与网格）→ 资产（文件与手册）。从 logo 开始的项目，评审时一定被打回且说不出原因。
  - **支线 H · 暗色模式（"反一下色"和"设计一套暗色"是两件事）** `L220` — - 先问该不该做：正常视力用户浅色更优（字号越小差距越大）；暗色的正当理由是低视力/白内障、暗环境、OLED 省电、沉浸媒体、长文选项。中后台不要默认暗色。
  - **支线 I · 性能与设计（"好看"必须先"看得见"）** `L231` — - 性能是设计约束，不是开发收尾。首屏主视觉选什么、用几套字体、上不上视频，在稿子上就已经定了 LCP 的上限。
  - **支线 J · 设计交付与协作（画完不等于交完）** `L244` — - 交付的是决策，不是图。稿子里有 intent / rule / value 三层，只给 value，开发必须反推前两层——偏差从这里开始。检验法：拿掉设计稿，开发能做出第二个页面吗？
  - **支线 K · 内容设计与 UX 文案（界面上的每个字都是设计）** `L257` — - 三级文案尺寸：long ≥3 段（引导页/帮助） / short 2–3 段（对话框/结果说明） / micro <3 句（按钮/标签/toast/错误——占界面 80%）。先判尺寸再写。
  - **支线 L · 演示文稿与幻灯片版式（不是"缩小的文档"是"放大的瞬间"）** `L275` — - 3 秒法则：每张幻灯片停留 20–60 秒，观众 3 秒内决定是否继续看。倒金字塔——结论先行。
  - **支线 M · 动效编排与状态机（动效 bug 八成不在曲线，在状态没建模）** `L294` — - 三层分工：L1 单动效（该不该动 / 多久 / 什么曲线）走 motion-system.md；L2 编排（≥2 元素或有先后）；L3 状态机（互斥状态 / 跨视图配对 / 会被打断）走 motion-orchestration.md。
  - **支线 N · 国际化与本地化（出海不是加个语言包，是三层同时改）** `L308` — - 先判三层：① 标记层 <html lang + dir；② 布局层 文案膨胀弹性 / CSS logical properties / RTL 镜像；③ 数据层 复数 / 日期 / 数字 / 姓名 / 排序。翻译只解决字符串，三层不动必
  - **支线 O · 设计系统文档写作（给人读的系统，不是给机器读的约束）** `L321` — - 先分层再判层：design-md-format.md 的 DESIGN.md 是给机器读的约束清单，handoff-collaboration.md 的终点是"开发能做出第二个页面"，本支线的终点是"半年后第三个团队也能自己查到、自己改
  - **支线 P · AI / 生成式设计工具链（产能层不是判断层）** `L331` — - 先判哪层交出去：五层地图（意图与约束 / 生成 / 编辑 / 代码化 / 验收）每层都要有人工闸门；三类活不交给 AI——定受众与语气、判上线与否、担法定责任。AI 只出候选，不出结论。
  - **支线 Q · 设计伦理与包容性（对称优先，默认值即决定）** `L340` — - 先立立场：设计伦理不是道德劝告，是可写进 CI 的路径长度、按钮构型、点击次数和默认值。三条不可商量：① 对称优于说服；② 默认即决定（预勾选/沉默不构成同意）；③ 意图不是辩护理由（CPPA §7004(c)：知情不修、刻意不知情同样
  - **支线 R · 组件 API 设计与组合模式（三份所有权，契约先于样式）** `L351` — - 先立立场：组件 API 不是 props 清单，是三份所有权的书面划分——状态所有权（受控 / 非受控）、渲染所有权（组合 / 换元素）、契约与演进所有权（键盘无障碍 / 语义冻结 / 版本判级）。组件库"不好用"八成不是样式问题，而是
  - **支线 S · 设计度量与用户研究（"好不好"不能只剩「我觉得」）** `L363` — - 先判要度量什么：ISO 9241-11:2018 把可用性拆成三件独立的事——Effectiveness（任务对不对）/ Efficiency（快不快）/ Satisfaction（爽不爽）；三者分别度量、分别签字，满意度高 ≠ 任务能
  - **支线 T · 图标设计系统（Iconography，视觉速记不是装饰）** `L374` — - 先判图标还是文字：图形比文字更快被识别时才用图标；歧义或首现品牌图标配文字，正文与导航一级用文字（见 iconography.md §1 决策树）。
  - **支线 U · 导航与信息架构（结构先于装饰，用户只问两个问题：我在这、怎么去那）** `L384` — - 先分四类职责：全局（跨站常驻）/ 局部（区域下钻）/ 上下文（内容体内跳转）/ 辅助（页脚·帮助）；把页脚或上下文链接塞进主导航是头号错配。
  - **支线 V · 设计评审与反馈（评审是暴露盲点不是挑错，先对齐再动手）** `L393` — - 评审是结构化对话对齐决策，产出「问题清单 + 决策记录」；两种形态的评审（同伴探索 / 带决策权的评审）两场会别混。
  - **支线 W · 色彩科学（配色不是审美是计算）** `L399` — - HSL 撒谎：HSL/HSV 的 H/S/L 不是感知均匀坐标，等数值步长 ≠ 等视觉步长（蓝区 L 段比红区长 30%+），色板生成、明度梯度一律走 OKLCH/OKLab。
- **学习节奏（可持续，不靠意志力）** `L412` — 最后一条最重要：能看出自己旧作的毛病，是能力增长唯一可靠的证据。
  - **支线 X · 视觉风格谱系与设计运动（把"感觉"翻译成信号）** `L426` — - 这是什么：用户说"做成 XX 那种感觉 / 高级感 / 科技感"时，不直接套词，而是拆成 Typography / Color / Shape&Material / Motion&Space 四维信号再落成 token。与 design
  - **支线 Y · 字体排印系统（把字号行距从口诀变成可验收的契约）** `L444` — - 这是什么（六层契约）：字体排印是与色彩科学并列的基础支柱，但不是「挑一款好看的字体」，而是六层契约——覆盖 / 尺度 / 节奏 / 字形 / 加载 / 授权（typography-system.md §2）。需求里出现「字太小 / 放大
  - **支线 Z · 形状与深度系统（把圆角与阴影从口诀变成几何契约）** `L460` — - 这是什么（第三根基础支柱）：与「色彩科学」「字体排印」并列，但此前 37 份参考里零独立文件，圆角/阴影/高度/材质只散落在 dark-mode.md §2/§5、design-tokens.md §2.4、visual-style-t
  - **支线 AA · 视觉层级与格式塔组织律（把"放大加粗"翻译成注意力分配契约）** `L474` — - 这是什么（第四根基础支柱）：与「色彩科学」「字体排印」「形状与深度」并列，但此前 38 份参考里零独立文件，格式塔/眼动/认知负荷只散落在 editorial-layout.md §8、navigation-ia.md、design-e
  - **支线 AB · 内容可发现性与可扫读性（把"搜得到"翻译成四层链路的线索密度）** `L487` — - 这是什么（注意力链路的下游环节）：与「视觉层级（目光先看哪）」「字体排印（字怎么排）」「导航与信息架构（结构怎么搭）」相邻但问题不同；此前 39 份参考里零独立资产，站内搜索链路、链接目的契约族、阅读等级与可发现性度量只在 naviga
  - **支线 AC · 直接操纵与指针交互（把"跟着指针走"翻译成四条并存的完成路径）** `L500` — - 这是什么（认知链路下游的执行端）：与「视觉层级（目光先看哪）」「内容可发现性（能不能找到）」相邻但问题不同；此前 40 份参考零独立资产，dpsearch.py "拖拽 手势 指针交互" 首位返回 performance-design.
  - **支线 AD · 对话式与生成式界面（把"边生成边变化"翻译成五段链路的完成路径）** `L513` — - 这是什么（认知链路下游的输出端）：与「视觉层级（目光先看哪）」「内容可发现性（能不能找到）」「直接操纵（按下指针之后）」相邻但问题不同——前三份都假设内容是确定的，本支线处理输出本身在流动、可能出错、可能带副作用。此前 41 份参考零独
  - **支线 AE · 叠加层交互契约（把 inert 与顶层栈翻译成四问判型的完成路径）** `L528` — - 这是什么（交互契约的边界端）：与语义 z-index 刻度、反馈时长、props 所有权三份资产相邻但问题不同——前三份分别管层看起来多高、文案怎么写、状态归谁，本支线管 inert 是否成立、aria-modal 能否标、Tab 是否
- **能力自测（162 条，做到 ≥110 条即达 L2+）** `L543` — L0

### `references/motion-orchestration.md` · 动效进阶 — 编排、状态机与共享元素转场（深度蒸馏）
_1049 行 · 快照 2026-11-05 · 68 节_

- **1. 分工与决策树：单动效、编排、状态机三层** `L11` — 动效问题分三层，先判层再查文件，否则会把「一个按钮反馈」做成状态机，或把「列表增删」当成单个 transition。
- **2. 编排的四种时间结构与总时长公式** `L31` — 编排 = 给 N 个动画分配起始时刻。只有四种结构，所有框架都是这四种的包装：
  - **2.1 总时长硬上限与可算的 stagger** `L42` — motion-system.md 定了「点击触发 ≤400ms」「stagger 间隔 20–40ms」「≤6 项」——这三条其实是同一个公式的三个约束：
  - **2.2 编排的层级纪律（与 motion-system.md §5 对齐并补全）** `L63` — - 父先子后用 when：when: "beforeChildren" 进场、when: "afterChildren" 退场。退场必须等子内容先走完，否则父容器消失会把子元素一起拽掉。
- **3. 交错编排 stagger：variants 传播与多框架实现** `L72` — 传播规则（官方原文）：「Variants will flow down through motion components」——父级 motion 组件切换 variant 标签时，所有子级 motion 组件会自动切换到同名 varian
  - **3.1 Motion for React：variants 传播是编排的地基** `L74` — 传播规则（官方原文）：「Variants will flow down through motion components」——父级 motion 组件切换 variant 标签时，所有子级 motion 组件会自动切换到同名 varian
  - **3.2 两代编排 API（重要：官方文档已换写法）** `L93` — 新版官方原文代码：
  - **3.3 原生 CSS 交错（无框架、包体最小）** `L122` — --index 由渲染层写入（style="--index:3"）。纪律：animation-fill-mode: both 必写，否则延迟期间元素以「已可见」状态闪一下再开始动。
  - **3.4 Vue / Svelte / GSAP 的等价写法** `L137` — - Vue <TransitionGroup：用 :css="false" + JS hooks，把 index 写进 data-index，delay: el.dataset.index 0.15（官方示例用 GSAP onComplet
  - **3.5 中文长列表与「逐字动画」陷阱** `L143` — - 中文无词间空格，逐字 stagger 会破词（motion-system.md §9 已给结论）。中文列表按「整行」交错，不要按字符交错。
- **4. FLIP：共享元素位移的通用算法（First · Last · Invert · Play）** `L151` — 来源：Paul Lewis（Aerotwist, 2015-02，2022-05 更新），Google I/O 2015 与 Chrome Dev Summit 站点的实际做法。它不是框架，是一种思路：把逐帧的昂贵布局计算预先算完，只把 t
  - **4.1 四步与精确算式** `L155` — 原文 WAAPI 版本（可直接抄，含官方给的曲线）：
  - **4.2 为什么快：100ms 响应窗口** `L181` — 原文核心论断：「There is a window of 100ms after someone interacts with your site where you're able to do work without them noti
  - **4.3 三条原文 caveat（工程上最容易踩）** `L189` — 1. 别超 100ms 窗口——批量元素时先全部读、再全部写（§14），不要「读一个写一个」。
  - **4.4 FLIP vs View Transitions 的选型** `L195` — ---
- **5. 列表增删与重排：四种操作的动画策略** `L209` — 列表是动效 bug 最密集的场景，因为同一批 DOM 会经历四种完全不同的变化，而多数人只写了「入场」一种。
  - **5.1 key 稳定性是所有列表动画的前提** `L220` — 官方一致口径（Motion / Vue / React 三家都写了）：
  - **5.2 退场元素必须脱离布局流（Vue 官方解法）** `L228`
  - **5.3 AnimatePresence 的三种 mode（Motion 官方）** `L240` — 三个官方排错点（照抄）：
  - **5.4 View Transitions 的列表方案：match-element** `L255` — 给每个列表项手写唯一 view-transition-name 太笨重，浏览器提供 view-transition-name: match-element（MDN 官方）：自动给所有选中元素设置唯一名称。配套的 view-transitio
- **6. 共享元素转场 A：View Transitions 完整机制** `L271` — 1. 触发：SPA 调 document.startViewTransition(updateCallback)；MPA 由同源导航触发（两页 CSS 都写 @view-transition { navigation: auto }）。
  - **6.1 六步流程（MDN 原文顺序）** `L273` — 1. 触发：SPA 调 document.startViewTransition(updateCallback)；MPA 由同源导航触发（两页 CSS 都写 @view-transition { navigation: auto }）。
  - **6.2 伪元素树（原文结构）** `L284` — - ::view-transition-old() / new() 都按 replaced content 渲染（像 <img/<video），因此可以用 object-fit / object-position。
  - **6.3 默认动画精确值（W3C CSS View Transitions Level 1 UA stylesheet 原文）** `L302` — - 默认 0.25s（quarter-second）、ease、cross-fade、fill-mode: both；子伪元素全部 inherit 定时，因此改时长写 group 一处即可。
  - **6.4 view-transition-name 唯一性（最容易炸的一条）** `L335` — 工程纪律：动态设置 name 后必须在转场结束清理；尤其在 MPA + bfcache 场景（§8.2），残留 name 会在用户按返回键时造成重名 → 转场被跳过。
  - **6.5 三个 Promise 与 skipTransition()** `L349` — skipTransition() 只跳过动画，不跳过 DOM 更新（官方："This won't skip calling updateCallback"）。这是把「用户关闭动效偏好」接入 View Transitions 的标准入口，也用
  - **6.6 并发与中断：单例规则** `L372` — "Only one view transition is allowed to run at a time. If a new view transition starts while one is already running, the
- **7. 共享元素转场 B：layoutId 与 Motion 布局动画** `L383` — Motion（原 Framer Motion）用 layout 系列 prop 在真实 DOM 上做 FLIP，不需要浏览器快照。
- **8. 跨文档转场（MPA）与导航方向类型** `L418` — - 无需 JavaScript：同源跨文档导航 + 两个文档 CSS 都写 @view-transition { navigation: auto; } 即触发。
  - **8.1 触发与版本** `L420` — - 无需 JavaScript：同源跨文档导航 + 两个文档 CSS 都写 @view-transition { navigation: auto; } 即触发。
  - **8.2 bfcache 的隐藏陷阱（MDN 明确警告）** `L426` — 在 pageswap 里给元素临时设置 view-transition-name 后，转场结束必须移除。原文："If we left them set, they would persist in the page state saved 
  - **8.3 首帧稳定化** `L439` — 跨文档转场要求「关键内容已解析」才有稳定快照。Chrome DevRel 建议用 render blocking 保证：① 关键样式已加载应用；② 关键脚本已执行；③ 用户首屏可见的 HTML 已解析。
- **9. 动画状态机：四态/六态模型与 XState** `L452` — in = true timeout 结束
  - **9.1 经典四态（react-transition-group <Transition 官方）** `L454` — 四个主状态：'entering'、'entered'、'exiting'、'exited'。in prop 切换时进入对应阶段，timeout 毫秒后自动切下一状态。children 作为函数时收到当前状态字符串。
  - **9.2 为什么必须是状态机（XState / Stately 官方定义）** `L472` — - 状态机「capture all the states, events and transitions」，好处是「find impossible states and spot undesirable transitions」。
  - **9.3 状态 × 事件矩阵（可直接贴进设计交付文档）** `L494` — 关键收益：「快速连点」不再是一堆 if，而是 exiting 收到 OPEN → 反向回 entering，且从当前插值继续（§10）。isLoading && isSuccess 这类不可能状态在建模阶段就被消灭。
- **10. 中断与取消：可中断性的工程定义** `L509` — motion-system.md 说「交互反馈一律用 transition（可中断）」——这里给出可中断的精确定义与实现手段。
  - **10.1 定义** `L513` — 可中断 = 动画进行中收到新事件时，从「当前视觉值」平滑迁移到新目标，而不是跳回起点、跳过终点或卡在中间。
  - **10.2 WAAPI 播放控制（MDN 精确语义）** `L525` — 为什么不要用 fill: forwards 长期保态（官方两条理由）：① 浏览器得维护仍 active 的动画状态，持续耗资源；② 动画样式在 cascade 中优先级高于指定样式，之后想覆盖很难。
  - **10.3 自动移除 filling animations 的 5 个条件（全部满足才移除）** `L540` — 1. 动画处于 filling（正向播放时 fill: forwards、倒放时 backwards、或 both）；
  - **10.4 transitionend / animationend 的四个坑** `L550` — 1. 冒泡：子元素过渡结束也会冒泡到父容器 → 必须检查 event.target === el 与 event.propertyName。
- **11. WAAPI 精确参数表（KeyframeEffect / Element.animate）** `L561` — 以下全部为 MDN KeyframeEffect() 与 Using WAAPI 的官方默认值，与 CSS 动画默认值不同处已标出：
- **12. CSS 入场/退场状态机：@starting-style 四件套** `L585` — @starting-style 定义「元素没有 previous state 时的起始值」，让 CSS transitions 在首次渲染或从 display:none 变可见时也能触发。
  - **12.1 三个状态，不是两个（MDN 原文）** `L587` — @starting-style 定义「元素没有 previous state 时的起始值」，让 CSS transitions 在首次渲染或从 display:none 变可见时也能触发。
  - **12.2 四件套（缺一不可）** `L599`
  - **12.3 allow-discrete 的 50% 规则与两个例外（MDN 原文）** `L628` — - 初始值 normal；allow-discrete 让离散属性也参与过渡。
  - **12.4 DOM 增删：先播退场，再移除节点** `L638` — MDN 示例流程：点击关闭 → 给元素加 .fade-out（其内设 display:none + opacity/scale 终点）→ setTimeout(() = el.remove(), 1000) 延迟移除，确保动画播完再删 DO
- **13. 编排层编排的无障碍降级（WCAG 2.3.3 / 2.2.2 / prefers-reduced-motion）** `L646` — motion animation 的官方定义：「addition of steps between conditions to create the illusion of movement or to give a sense of a 
  - **13.1 三条 WCAG 条款原文口径** `L648` — motion animation 的官方定义：「addition of steps between conditions to create the illusion of movement or to give a sense of a 
  - **13.2 prefers-reduced-motion 精确语义（MDN）** `L662` — - no-preference：用户未表态，该值求值为 false；reduce：求值为 true。
  - **13.3 编排层降级的四条纪律（本文件的差异化结论）** `L669` — 1. 整段跳过，不要逐个归零。把 stagger 序列里每个元素的 animation-duration 都设成 1ms，结果是 N 个变化在一帧内重叠闪现——比不做降级更糟。正确做法：命中 reduce 时取消交错（--index 系数置
- **14. 性能：100ms 响应窗口、读写分离与快照开销** `L680` — FLIP 批量模板（先读后写，避免 N 次 sync layout）：
- **15. 跨框架实现矩阵与选型决策** `L709` — 选型决策树：
- **16. 场景速查（16 条，直接取结论）** `L738` — ---
- **17. 反模式（20 条，命中即扣分）** `L761` — 1. 用 index 作列表 key —— 重排后退场动画挂到错误元素（Motion / Vue 官方都点名）。
- **18. 自检清单（20 条，动效编排交付前逐条过）** `L786` — 1. 判过层了吗（L1 单动效 / L2 编排 / L3 状态机）？有没有把简单反馈做成状态机、把列表增删当成单个 transition？
- **19. 可抄代码（8 段）** `L811` — jsx
  - **19.1 Motion 交错编排（新版 + 旧版对照）** `L813`
  - **19.2 CSS --index 级联 + 编排层降级** `L841`
  - **19.3 FLIP 批量重排（先全读、再全写，100ms 窗口内）** `L865`
  - **19.4 列表增删（Vue TransitionGroup + Motion popLayout）** `L884`
  - **19.5 View Transitions 增强封装（单例 + types + 偏好 + 清理）** `L905`
  - **19.6 动画状态机（XState 四态 + WAAPI 从当前值重启）** `L941`
  - **19.7 @starting-style 四件套（dialog 下进上出）** `L966`
  - **19.8 JS 层 reduced-motion 降级（覆盖 WAAPI / Svelte / VT）** `L981` — ---
- **20. 素材与出处（本轮实测 / 官方原文）** `L1005` — - MDN · View Transition API — 接口、伪元素、properties、pseudo-classes、:active-view-transition-type()、view-transition-scope
  - **20.1 规范与官方原文（全部逐页读取，非二手总结）** `L1007` — - MDN · View Transition API — 接口、伪元素、properties、pseudo-classes、:active-view-transition-type()、view-transition-scope
  - **20.2 仓库实测（GitHub API，2026-11-05）** `L1030` — 实测备注：barba/barba 与 motionone/motion 本轮 API 返回 404（仓库迁移/合并），故不列入表，也不臆造数字。motionone 已并入 motiondivision/motion。

### `references/motion-system.md` · 动效与微交互系统 — Motion System（深度蒸馏）
_348 行 · 快照 2026-10-30 · 21 节_

- **1. 决策三问：先判该不该动** `L10` — 动效只有三种合法用途（说不出属于哪一种，就删掉）：
- **2. 动效缓动曲线（easing）：语义决定曲线，不是审美决定** `L30` — 核心规则（90% 的人搞反的一条）：
  - **2.1 四体系精确值对照（可直接抄进 CSS）** `L39` — Ant 的反向曲线：motionEaseInBack cubic-bezier(0.71, -0.46, 0.88, 0.6)（先回撤再走），慎用，仅适合"取消/撤销"的语义。
  - **2.2 立场：项目默认用哪套** `L53` — 给一个 3 曲线最小集就够，不要引入 12 档：
- **3. 动效时长：按距离和面积取，不按心情取** `L69` — 原理：位移距离越长、面积越大，人眼需要的追踪时间越长，时长必须递增（Carbon 原话：the larger the change in distance or size, the longer the animation）。但上限 400
  - **3.1 四体系时长刻度** `L73` — M3 的 700–1000ms 只用于不涉及用户输入的环境型转场。任何由点击触发的动画超过 400ms 都是错的。
  - **3.2 距离 → 时长（经验法则，按 Carbon 的非线性刻度换算）** `L87` — 微交互的硬指标（Carbon 评估清单原文）：用户输入触发的微交互应落在 90–120ms，且用 ease-out。
- **4. 场景速查表（直接取值，不用再算）** `L101` — 覆盖场景：hover / 按钮按压 / 焦点环 / 开关 Toggle / 复选框 / Tooltip / 下拉菜单 Popover / 弹层（Modal、Dialog）/ 抽屉 Drawer / Toast 提示 / 手风琴 / Tab 
- **5. 编排：多个元素一起动时的顺序** `L131` — 1. 层级优先：重要元素先动、动得更久；次要元素合并成一组同时动（Fluent：次要元素同步可避免注意力分散）。
- **6. 物理感：什么时候用弹簧，什么时候用曲线** `L141` — 建议参数（建议值，非官方）：UI 常规 stiffness 300–500 / damping 30–40 / mass 1；需要弹性时降 damping 到 20–26；永远设置最大时长兜底（如 restDelta 0.01 + 超时 6
- **7. 实现：可直接抄的四段代码** `L155` — css
  - **7.1 动效 token（贴进 :root）** `L157`
  - **7.2 从 display:none 进入的弹层（@starting-style）** `L179` — 原生 dialog / popover 从 display:none 变可见时，直接写 transition 不会触发动画，必须配 @starting-style + transition-behavior: allow-discrete：
  - **7.3 共享元素过渡（View Transitions）** `L200` — 同一元素在 A 视图与 B 视图都标同一个名字，浏览器自动做"从旧位置尺寸平滑过渡到新位置尺寸"：
  - **7.4 滚动驱动动画（无 JS）** `L221` — 纪律：滚动驱动动画只能做"入场"和"进度指示"，不要做滚动劫持（用 JS 强行改滚动位置），后者是体验灾难且伤可访问性。
- **8. 性能与降级** `L238` — 只动这两个属性：transform（含 translate / scale / rotate）与 opacity——它们走合成层，不触发布局与重绘。
  - **8.1 prefers-reduced-motion 三档降级（必须做）** `L257` — WCAG 依据：2.3.3 Animation from Interactions（AAA）——交互触发的动效必须可关闭（除非是功能必需）；2.2.2 Pause, Stop, Hide（A）——超过 5 秒的自动运动内容必须可暂停；2.3
- **9. 中文场景与小程序** `L285` — ---
- **10. 验收清单（10 条，交付前逐条过）** `L298` — 1. 每个动效都能说出属于反馈 / 引导 / 个性中的哪一种？说不出的删了没？
- **11. 反模式（命中即扣分）** `L313` — - 从 scale(0) 弹窗、从 opacity:0 + scale(0.5) 做卡片——真实物体不会从无到有地放大。
- **12. 素材与出处** `L326` — 规范原文（本轮实测）

### `references/multi-brand-theming.md` · 多品牌与多主题 Token 架构 — Multi-brand & Multi-theme
_864 行 · 快照 2026-11-01 · 42 节_

- **一、判据：什么时候真的需要多品牌架构** `L11` — 先判「要不要」，再判「怎么做」。多数团队在只需要 1 个品牌 × 2 个模式 时上了四层品牌架构，结果是维护成本翻倍、收益为零。
- **二、主题不是"换色"，是四个正交轴** `L28` — 把主题理解成"一套配色"是最常见的架构错误。真实系统里主题是多个独立轴的笛卡尔积，每根轴改动的东西完全不同：
- **三、四层架构：在原有三层上加一层"品牌输入"** `L52` — design-tokens.md 里的三层（Base / Semantic / Component）是单品牌模型。多品牌必须再加一层，否则品牌值会渗透进语义层：
- **四、从 1 个品牌色算出整套色阶：四条路线与精确参数** `L76` — 客户只会给你一个色值。你必须用它生成 10–16 档可用的色阶，且每档的对比度行为要可预测。四条成熟路线，各有适用面。
  - **4.1 路线 A · M3 HCT 色度常量法（最通用，Android/跨端首选）** `L80` — 做法：把种子色转成 HCT（色相 H、色度 C、明度 tone T），色相继承种子，色度按变体常量固定，明度按需取 0–100 的 tone。关键在于"色度固定"——这样不同品牌色生成的色阶饱和度观感一致，不会一个品牌很灰一个很艳。
  - **4.2 路线 B · Fluent BrandRamp 16 档（需要"最细颗粒"时）** `L112` — Fluent UI 把品牌色阶写成了强制 16 档的类型：
  - **4.3 路线 C · Radix 12 步语义步进（最省心，Web 首选）** `L130` — Radix 把 12 个档位按用途定死，不是按明度：
  - **4.4 路线 D · 中文体系（HCT + 插值拟合 + 品牌倾向中性色）** `L149` — TDesign 的做法值得单独记，因为它解决了"品牌氛围"这个中文 B 端常见诉求：
  - **4.5 路线选择决策表** `L161` — ---
- **五、品牌色护栏：把"客户给什么用什么"变成"算过才用"** `L174` — 这是多品牌系统最容易出事、也最少被写进规范的一节。 客户给你一个品牌色，你直接拿去做主按钮底 + 白字——10 个里 7 个不达 AA。这不是审美问题，是可计算的合规问题。
  - **5.1 亮度边界：一条公式定生死** `L178` — WCAG 相对亮度 L，白字对比度 = 1.05 / (L + 0.05)，黑字对比度 = (L + 0.05) / 0.05。反解出两条绝对边界：
  - **5.2 九个真实品牌色的实测（本技能自算）** `L195` — 三个必须传达的结论：
  - **5.3 三档修正策略（护栏不达标时怎么改）** `L215` — 护栏的正确位置：在生成色阶之后、写入 token 之前，作为生成管线的一道自动校验。人不可能每次手算，所以它必须是代码。
  - **5.4 护栏还要管三件事（不只是按钮）** `L227` — 注意最后一条的陷阱：品牌色不应该直接当图表第一分类色。品牌色是"一个色"，图表需要"一组可辨色"。把品牌色塞进分类色板，会导致"第一类特别突出、其余类失衡"，且品牌色一换图表全变。图表分类色板应独立维护，品牌色最多取一个衍生档做强调。
- **六、主题矩阵的落地：选择器与层叠策略** `L240` — 错误写法（组合爆炸）：
  - **6.1 不要写 2^N 个选择器块** `L242` — 错误写法（组合爆炸）：
  - **6.2 用 @layer 锁死优先级（关键）** `L269` — 主题系统"覆盖不掉"的头号原因是：未分层的样式永远赢过分层样式，而第三方库（组件库 reset）通常是不分层的。
  - **6.3 作用域三选** `L292` — 逃逸陷阱（必记）：position: fixed 的弹层 / dialog / popover 如果 portal 到 body，会离开 [data-brand] 作用域，于是弹层用的是 :root 的默认品牌。解法：portal 目标必须
- **七、运行时切换 vs 构建期编译** `L305` — 这是多品牌架构的第一个分叉决策，选错后面全错。
- **八、多品牌同页共存（最容易被忽略的场景）** `L333` — 以下四种场景必须支持同页多品牌，而多数主题系统做不到：
- **九、四套真实主题矩阵对照（可直接抄结构）** `L353` — Primer 的"反向色阶"值得单独说：它的中性色阶在亮色下从白开始、暗色下从黑开始，方向相反。这样 bgColor-default 这类 functional token 在两个模式下指向同一个档位号，不需要为暗色重写一遍映射。代价是：你
- **十、语义层分叉的边界：什么时候允许"每个品牌一套 L2"** `L381` — 默认禁止。 允许的例外只有三种，且每种都要写书面理由：
- **十一、配置文件结构：DTCG 多品牌写法** `L410` — tokens/
  - **11.1 目录结构（core 与 brand 分离）** `L412` — 铁律：core/ 里不许出现任何品牌色值。brands// 里不许出现任何语义名（--color-text 这种词只属于 core）。
  - **11.2 DTCG 的 $extends 做品牌继承** `L435` — DTCG（2025.10 草案）的组级 $extends 是深合并语义：复制被继承组 → 本地同路径完整替换（不是逐属性合并）→ 新增路径并入 → 禁止循环引用。
  - **11.3 Style Dictionary 多品牌构建（已验证的配置模式）** `L458` — SD 的多品牌不靠"主题插件"，靠两条机制的组合：
- **十二、Figma 侧：变量模式必须与代码轴一一对应** `L495` — 4 个模式的现实约束：如果你有 3 个品牌 × 2 个模式 = 6 个组合，装不进一个 collection。正确解法是拆成 Brand（3 模式）+ Mode（2 模式）两个 collection——组合由 Figma 自动做笛卡尔积，不
- **十三、品牌注入管线：从客户填表到 CSS 生效** `L509` — 六步各自的关键决策：
- **十四、防闪烁：多品牌特有的 FOUC** `L539` — dark-mode.md §9 讲的是"模式闪白"。多品牌多一个更严重的问题：品牌未知时先渲染了默认品牌，然后跳到客户品牌——用户会以为进错了网站。
- **十五、性能成本：变量数量与切换代价** `L561` — 切换主题的代价：
- **十六、治理：品牌准入与变更管理** `L582` — "改默认值 = MAJOR"在多品牌下更严重：单品牌改默认色影响一个产品，多品牌改 L2 映射影响所有品牌的所有页面。所以 L2 的任何改动都要按 MAJOR 走迁移流程（见 handoff-collaboration.md §12）。
- **十七、12 个场景速查** `L597` — ---
- **十八、20 条反模式** `L616` — 1. 每个品牌 fork 一份代码 —— 半年后无法合并，任何 bug 要修 N 次。
- **十九、18 项自检（多品牌/多主题关）** `L641` — 1. 判过要不要做？品牌数 1 或模式数 1 才上架构，否则用 dark-mode.md。
- **二十、可抄代码（6 段）** `L664` — css
  - **20.1 主题矩阵骨架（轴独立 + @layer）** `L666`
  - **20.2 品牌色护栏（生成色阶后、写 token 前必跑）** `L719`
  - **20.3 品牌色阶生成骨架（HCT tone，路线 A）** `L754`
  - **20.4 首屏防闪烁注入** `L775`
  - **20.5 主题切换（禁用过渡，只改属性）** `L794`
  - **20.6 Style Dictionary 多品牌（完整可跑）** `L814` — ---
- **附：来源** `L847`

### `references/navigation-ia.md` · 导航与信息架构 · Navigation & Information Architecture
_278 行 · 快照 — · 20 节_

- **0. 一句话立场** `L6` — 导航不是「放几个链接」，是「替用户画一张随时能找到自己的地图」。 任何界面在用户眼里只有两个问题：我在这、怎么去那。其余一切（菜单数量、汉堡还是 tab、面包屑、搜索）都是为这两个问题服务。可访问性是这条线的及格线——键盘到不了、读屏念不出
- **1. 导航的四类职责（先分清楚再用形态）** `L12` — 关键判断：一个产品的导航混乱，90% 不是「链接太少/太多」，而是四类职责混在同一根线上（把 footer 链接塞进主导航、把上下文链接做成主导航项）。先给每根线定性，再选形态。
- **2. 形态决策矩阵（什么时候用什么）** `L25` — 响应式降级路径（与 responsive-layout.md 对齐）：<768 → 汉堡或底部 tab（≤5 项）；768–1023 → 顶部导航 / 图标条；≥1024 → 常驻侧栏 / 双层。折叠侧栏 64px、展开 208–240px
- **3. 项数铁律（数量是有科学依据的，不是审美）** `L40` — - 米勒法则（Miller's Law）：工作记忆容量约 7±2；导航项按 5–9 分组是舒适上限。超过就靠视觉分组 / 二级折叠，不要硬排一行。
- **4. 信息架构地基（深度 vs 广度）** `L51` — - 3-click 规则是迷思：NN/g 反复实证——用户不在乎点击次数，只在乎每一步是否知道「点下去会得到什么」（信息气味，information scent）。把树压到 3 层但每层气味稀薄，比 5 层但气味浓更糟。
- **5. 面包屑（Breadcrumb）** `L61` — 位置纪律：面包屑第一项通常是首页/全站名；当前页项禁用 href 且 aria-current="page"；移动端空间不够可省略，但不能用面包屑替代主导航的可达性。responsive-layout.md 已述窄屏表格纪律，面包屑同理——
- **6. 标签页 Tabs（ARIA 的正确打开方式）** `L73` — - Tabs ≠ 导航：了一个最常见的职责错配——用 ARIA role="tab" 做整站主导航是错误。Tabs 表示「同一内容区内的并列视图」，切换不应改变页面 URL/上下文；跨页面的跳转用链接 + 导航 landmark。
- **7. 移动端导航降级** `L82` — - 底部 tab ≤5 项：Apple HIG 与 Material 共识；图标 + 文字标签（icon-only 在底部 tab 上可，但需 aria-label）。
- **8. 当前位置指示（"You are here"）** `L91` — - 必须有激活态：当前导航项用颜色 + 字重 + 图标 + 左侧指示条至少两项组合，永不只靠颜色（WCAG 1.4.1）。
- **9. 可访问性导航（及格线，不是加分项）** `L100` — 地标纪律：一个页面最多一个 banner(<header)、一个 contentinfo(<footer)、一个 main；导航用 nav 且多 nav 各带 aria-label。读屏用户靠 landmark 跳转，「裸」div 导航等于
- **10. 搜索与导航协同** `L120` — - 搜索是导航的备份，不是替身：WCAG 2.4.5 要求「多种找路方式」，导航 + 搜索二者至少并存；纯靠搜索 = 用户先猜关键词。
- **11. 反模式 20 条** `L130` — 1. 全局主导航塞进 9+ 项还不分组
- **12. 自检 20 项** `L155` — 1. [ ] 主导航项 ≤9 且做了视觉分组？
- **13. 可抄代码** `L180` — html
  - **13.1 Skip link + 语义导航骨架** `L182`
  - **13.2 响应式导航（桌面侧栏 / 移动抽屉）** `L213`
  - **13.3 ARIA Tabs 键盘处理（手动激活）** `L225`
  - **13.4 面包屑（位置型，末级非链接）** `L246`
  - **13.5 搜索框 + combobox 联想（APG pattern 节选）** `L257` — ---
- **14. 与其他参考的接线** `L269` — - 项数/分组 → 本节 §3、§4（米勒 7±2、深度≤3）

### `references/overlays-modality.md` · 叠加层与模态性：判型、焦点契约、顶层栈与非模态消隐
_926 行 · 快照 2026-11-11 · 55 节_

- **0. 一句话立场** `L10` — 模态不是一层半透明黑色遮罩，是一份「外部还能不能被操作」的交互契约。 一个界面可以没有遮罩却是模态（代码阻止了外部交互），也可以有遮罩却不是模态（外部仍可点、Tab 仍能走出去）。把模态当成视觉效果来做，就会同时踩中四条独立规范：APG 焦
- **1. 四问判型决策树：inert / 焦点 / 触发 / 退出** `L18` — 先答四问，不要先看设计稿长什么样：
- **2. 三条最重要裁决** `L40` — W3C APG 逐字："A dialog is a window overlaid on either the primary window or another dialog window. Windows under a modal d
  - **裁决一 · 模态性由 inert 定义，不由遮罩定义；aria-modal 是「声明」不是「实现」** `L42` — W3C APG 逐字："A dialog is a window overlaid on either the primary window or another dialog window. Windows under a modal d
  - **裁决二 · Popover API 永远非模态；它与 <dialog 是两套机制，不是彼此的轻量替代** `L50` — MDN 逐字："Popovers created using the Popover API are always non-modal. If you want to create a modal popover, a <dialog el
  - **裁决三 · 「浮层不挡焦点」是 WCAG 2.2 新增的 AA 硬要求，模态天然通过、伪模态最危险** `L58` — SC 2.4.11 Focus Not Obscured (Minimum)（Level AA）逐字："When a user interface component receives keyboard focus, the compone
- **3. APG 对话框契约逐字条文：初始焦点、Tab 循环、Escape、关闭后归位** `L68` — W3C APG《Dialog (Modal) Pattern》Keyboard Interaction 逐字（这是实现验收清单，不是建议）：
  - **3.1 初始焦点的四种情形（APG Note 1 逐字要点，按内容选，不是一律聚焦第一个按钮）** `L79` — 1. 内容含列表 / 表格 / 多段语义结构 → 给开头静态元素 tabindex="-1" 并聚焦它，this makes it easier for assistive technology users to read the cont
  - **3.2 关闭后焦点归位（APG Note 2 逐字）** `L90` — When a dialog closes, focus returns to the element that invoked the dialog unless either:
  - **3.3 语义清单（APG WAI-ARIA Roles, States, and Properties）** `L98` — - 容器 role="dialog"；操作该 dialog 所需的全部元素必须是该容器的后代。
  - **3.4 关于 aria-hidden 的历史包袱** `L106` — APG Note 逐字："The aria-modal property introduced by ARIA 1.1 replaces aria-hidden for informing assistive technologies th
- **4. aria-modal="true" 双条件与误标后果** `L112` — APG 逐字（两处：Dialog Modal Pattern 与 Alert Dialog Pattern 措辞完全一致）：
- **5. 原生 <dialog 的浏览器代劳清单：showModal / show / open / closedby** `L134` — MDN 逐字："The HTML <dialog element is used to create both modal and non-modal dialog boxes." 三种打开方式对应三种交互契约：
  - **5.1 closedby 三值（MDN 逐字）** `L146` — closedby 区分三类关闭动作："A light dismiss user action, in which the <dialog is closed when the user clicks or taps outside it"、
  - **5.2 其余必须记住的逐字点** `L160` — - 多个模态层："If multiple modal dialogs are open, pressing the Esc key should close only the last shown dialog. When using <d
- **6. Popover API 三态：always non-modal 与 auto · hint · manual 双栈** `L171` — MDN："Popovers created using the Popover API are always non-modal." 同一页把术语分清楚："This content can take several different na
  - **6.1 逐字定调** `L173` — MDN："Popovers created using the Popover API are always non-modal." 同一页把术语分清楚："This content can take several different na
  - **6.2 三态契约（MDN Using 逐字）** `L177` — 逐字注意："Note also that popover="hint" falls back to popover="manual" in unsupporting browsers." —— 用 hint 必须做能力检测与降级，降级后「多
  - **6.3 双栈六条交互规则（MDN 逐字）** `L187` — The browser maintains two independent stacks of open popovers: an auto stack for auto popovers, and a hint stack for hin
  - **6.4 焦点与 ARIA（最容易与 dialog 混淆的一节）** `L199` — MDN 逐字："When a relationship is established between a popover and its control (invoker) via the popovertarget attribute, 
  - **6.5 声明式与命令式 API 速查** `L208` — HTML：popover（auto / hint / manual）、popovertarget（指向 id）、popovertargetaction（hide / show / toggle，缺省 toggle）、interestfor（
- **7. top layer、inert、::backdrop 与 z-index 的分界** `L219` — - top layer 是独立绘制层，不是更大的 z-index。MDN 逐字：<dialog "being removed from / added to the top layer and the accessibility tree"
- **8. WCAG 2.2 四条款矩阵：谁管叠加层的哪一段** `L229` — 配套但不在本文件主线的：SC 2.4.12 Focus Not Obscured (Enhanced)（AAA，"none of the component receiving focus should be obscured"）、SC 2
- **9. SC 1.4.13 三条件：Dismissible / Hoverable / Persistent 逐字与可执行判定** `L244` — 《Understanding SC 1.4.13 Content on Hover or Focus》（Level AA）规范性条文逐字：
  - **9.1 范围裁决：模态明确不适用** `L264` — W3C Additional Notes 逐字："Modal dialogs are out of scope for this criterion because they must take keyboard focus and thu
  - **9.2 三条的可执行判定（工程约定，验收时逐条给证据）** `L270` — - Dismissible：在不移动鼠标、不移动键盘焦点的前提下能关掉。W3C Intent 逐字给了标准做法："such as pressing the Esc key"；并给两项豁免 "The additional content co
  - **9.3 tooltip 的正确形态（APG Tooltip Pattern）** `L276` — APG 逐字："A tooltip is a popup that displays information related to an element when the element receives keyboard focus or
- **10. 浮层遮挡裁决：2.4.11 的四类官方判词、两条例外、通过手段与 F110** `L290` — When a user interface component receives keyboard focus, the component is not entirely hidden due to author-created cont
  - **10.1 条文与两条 Note 逐字** `L292` — When a user interface component receives keyboard focus, the component is not entirely hidden due to author-created cont
  - **10.2 四类叠加层的官方裁决表** `L302`
  - **10.3 Note 2 的三条合法出路（W3C 逐字示例）** `L312` — keyboard actions that may allow the item with focus to be revealed include: using the Escape key to dismiss the obscurin
  - **10.4 通过手段（官方与工程分列）** `L318` — - 官方充分技术 C43："Using CSS scroll-padding to un-obscure content"；官方 Failure F110："due to a sticky footer or header complete
- **11. SC 2.1.2 No Keyboard Trap：焦点循环允许的前提是「退出可知、可达」** `L329` — 条文（Level A）逐字：
- **12. SC 3.2.1 On Focus：focus 不得触发 change of context，hover 触发也不等于可以抢焦点** `L349` — 条文（Level A）逐字："When any user interface component receives focus, it does not initiate a change of context."
- **13. 关闭契约矩阵：closedby 三值与七条退出路径** `L367` — 关闭状态归位表（工程约定，逐项都要复位，缺一项就是「关了但没关干净」）：
- **14. 层叠与嵌套：一次一个、双栈、Escape 只关最后一层** `L395` — - Apple HIG 逐字："Let people dismiss a modal view before presenting another one. Allowing multiple modal views to be visib
- **15. 组件族谱判型表（12 类；先判型再选实现）** `L405` — 一条速记：要不要模态，只取决于「用户此刻是否必须处理完才能回到原任务」；Apple HIG 逐字 "Present content modally only when there's a clear benefit. A modal exp
- **16. 平台与设计系统口径（原文 vs 工程约定分列）** `L426` — 定义："Modality is a design technique that presents content in a separate, dedicated mode that prevents interaction with th
  - **16.1 Apple HIG Modality（逐字）** `L428` — 定义："Modality is a design technique that presents content in a separate, dedicated mode that prevents interaction with th
  - **16.2 Radix Primitives Dialog（逐字）** `L434` — Features 逐字："Supports modal and non-modal modes." / "Focus is automatically trapped within modal." / "Manages screen rea
  - **16.3 Material 3 / Open UI（口径限制）** `L443` — M3 components/dialogs/overview 与 components/bottom-sheets/overview 本轮均返回 200，但内容为 JS 动态渲染，未取得可逐字核验的尺寸 / 时长 / 行为数值，因此本文件不
  - **16.4 GitHub API 实测 10 库（2026-11-11）** `L447` — 口径纪律：NOASSERTION ≠ 无许可、未检出 SPDX ≠ 未授权；ariakit/ariakit 与 openui/open-ui 的具体许可须到仓库 LICENSE 文件逐字核验，本表只记录 API 返回的字段，不做推断。★ 与
- **17. 12 场景决策速查** `L466` — 1. 删除确认：role="alertdialog" + 模态 + aria-describedby 指向后果说明；初始焦点落「取消」（APG 最不破坏性动作）；Esc / 取消 / 确认三条路径都归位焦点。
- **18. 20 反模式（每条都给出违反的契约）** `L483` — 1. 用 position: fixed + z-index: 9999 + 半透明遮罩冒充 inert 层：没有 top layer、Tab 跑到背景 → §2 裁决二 / §7。
- **19. 20 项自检（交付前逐条给证据）** `L508` — - [ ] 四问答完并写进组件 API（inert / 焦点 / 触发 / 退出），没有「先画遮罩再补逻辑」？
- **20. 5 段可抄代码（§20.1–§20.3 为 Python 实跑）** `L533` — 把 §1 四问 + §4 双条件 + §2 裁决三编译成可执行断言。输入是组件声明，输出是应走的契约与违规项。
  - **20.1 模态性判型器（Python，实跑 PASS）** `L535` — 把 §1 四问 + §4 双条件 + §2 裁决三编译成可执行断言。输入是组件声明，输出是应走的契约与违规项。
  - **20.2 SC 1.4.13 三条件校验器（Python，实跑 PASS）** `L643`
  - **20.3 SC 2.4.11 遮挡裁决器（Python，实跑 PASS）** `L704`
  - **20.4 原生 HTML / CSS 契约骨架（可抄）** `L776` — 提醒：closedby="none" 时 Esc / 点外部都不关，必须靠表单里的「取消」按钮；若要拦数据丢失，用 cancel 事件 preventDefault() + 确认，不要全局屏蔽 Esc。<dialog 上加 tabindex
  - **20.5 自定义实现的关闭契约状态机（TypeScript，可抄）** `L816` — 这是工程约定骨架，不是规范实现。原生 showModal() 已代劳 inert / top layer / Escape / 隐式 aria-modal，能用原生就不要自己写；这段只用于必须自定义（如跨框架 portal、非 HTML 渲
- **21. 来源与引用（含置信度）** `L868` — 引用纪律：逐字英文只在本文件出现一次，SKILL.md / README 的转述不得升格为条文；popover 术语的「上位概念 vs 具体 API」差异（§6.1）在转述时必须保留，否则会把「always non-modal」误读成「所有
- **22. 取源限制（公开记录，不臆造）** `L891` — 1. M3 两页为 JS 动态渲染：components/dialogs/overview 与 components/bottom-sheets/overview 均 200，但无可逐字核验的尺寸 / 时长 / 交互数值，故本文件不含任何 
- **23. 与既有资产边界矩阵** `L907` — ---
- **24. 接线** `L924` — 接线：SKILL.md 资产表 / 意图路由 / 第 5 步 / 第 41 条自检 · mindmap INTENTS · regression NEWQUERIES · knowledge-map 支线 AE · memory/alias

### `references/patterns.md` · 元素设计模式图鉴 — Patterns（深度蒸馏）
_135 行 · 快照 2026-10-29 · 14 节_

- **导航栏 Navbar** `L7` — 构型谱系（选 1 种，不混用）：
- **首屏 Hero** `L25` — 构型谱系：
- **功能特性区 Features** `L41` — 构型谱系：3 列网格（最常用）｜2×2 大卡｜左右交替图文｜密集列表（每行 icon+标题+一句话）。
- **CTA 区块** `L49` — 构型谱系：通栏色块（强调色底+白字居中）｜描边卡片（浅底+边框+左右布局）｜全宽渐变（每页 ≤1 处）。
- **页脚 Footer** `L57` — 构型谱系：4 列链接 + 底条（产品/资源/公司/法务）｜精简单行（logo+少量链接+版权，作品集）｜大字标语式（品牌宣言压底）｜站点地图式（SaaS 大站）。
- **定价表 Pricing** `L65` — 构型谱系：3 档横排（推荐档抬高/描边强调）｜2 档对照+企业档横条｜月/年切换（年付标 -20% 类折扣）。
- **登录/注册 Auth** `L73` — 构型谱系：居中卡片（≤400px，logo+标题+表单+社交登录+切换链接）｜左品牌右表单分屏（品牌侧放图/标语）｜全屏极简（只有表单）。
- **仪表盘 Dashboard** `L81` — 构型谱系：侧边导航 F + 顶栏 + 内容区（默认）｜顶部导航 + 卡片网格（轻量工具）｜三栏（列表+详情+属性面板，管理类）。
- **卡片 Card** `L89` — 构型谱系：竖版图文（封面 16:9 + 标题 + 摘要）｜横版列表行（缩略图 48–64px + 双行文字）｜数据卡（数值+标签+趋势）｜可交互卡（hover 抬升 2px + 阴影加深）。
- **表单 Form** `L97` — 完整规则（标签对齐决策、字段定宽、校验时机、错误文案模板、中文特有字段、布局梯度、可访问性清单）→ form-table.md §1–§11。此处只给构型与速查。
- **数据表格 Data Table** `L108` — 完整规则（行高计算、列对齐、列宽、固定列、批量操作、空态、可访问性）→ form-table.md §12–§15。
- **移动端底部导航 Tab Bar** `L119` — 关键参数：高度 56–64px + 安全区内嵌；3–5 项，图标 24px + 10–11px 标签；当前项用强调色，其余灰；点击目标 ≥44×44px。
- **落地页版式骨架（整页组装）** `L126` — 标准顺序（SaaS，可裁剪）：导航(A) → Hero(A/B) → 社会证明 logo 墙 → Features(3 列) → 用法演示/截图 → 定价(3 档) → 常见问题(手风琴) → CTA(通栏) → Footer(4 列)。
- **反模式速查（任何元素通用）** `L133` — 纯灰 #808080 大面积使用｜字号不用阶梯｜间距非 4/8 倍数｜同页两种圆角语言｜标题靠彩色而不是字号字重分层｜动效无反馈/引导/个性用途｜一行放不下还想塞｜对比度 <4.5:1 的正文。

### `references/performance-design.md` · 性能与设计的关系（Performance × Design）
_843 行 · 快照 2026-11-01 · 75 节_

- **1. 为什么性能是设计约束：加载速度就是设计决策** `L13` — 字节不等于字节。一个 200KB 的脚本和一个 200KB 的图片，下载时间相同，但成本完全不同：
  - **1.1 三条硬因果** `L15`
  - **1.2 一个必须纠正的直觉** `L23` — 字节不等于字节。一个 200KB 的脚本和一个 200KB 的图片，下载时间相同，但成本完全不同：
  - **1.3 设计师该在什么时候介入** `L34` — 性能是唯一一个"越早决定越便宜"的设计维度：改一张首屏图的构图，在设计阶段是 10 分钟；在上线后发现 LCP 4.2s，是重做首屏。
- **2. 指标体系：先背下这七个数** `L46` — 判定口径（官方，别记错）：
  - **2.1 Core Web Vitals（三项，官方核心）** `L48` — 判定口径（官方，别记错）：
  - **2.2 辅助指标（不是核心，但诊断时离不开）** `L62` — TBT / TTFB / FCP 之所以不是核心指标：官方理由是"不可在真实环境测量，且不直接反映以用户为中心的产出"。
  - **2.3 Lighthouse 性能分怎么算（Lighthouse 10 权重）** `L73` — 评分色带：0–49 红（Poor）/ 50–89 橙（Needs Improvement）/ 90–100 绿（Good）。
- **3. LCP：把 2.5 秒拆成四段（这是最有用的一张表）** `L94` — LCP 可无损拆成四个不重叠、无间隙的子部分，四段之和即 LCP：
  - **3.1 设计侧的 LCP 决策（最常翻车的五处）** `L107` — 1. 首屏主视觉选什么，直接决定 LCP 上限
  - **3.2 一个反直觉的坑** `L118` — 单独优化某一段，时间会转移到另一段。例：把首屏图压小 300KB（load duration 变短），但主 JS 还没执行完，浏览器没空渲染 → 时间跑到 render delay，LCP 不变。
- **4. INP：交互延迟的三段与"设计侧预算"** `L126` — 关键限定：INP 只测到"下一帧被绘制"，不测交互的最终结果（网络请求、异步更新）。所以"点了有反应"和"点了数据到了"是两件事，前者是 INP，后者是 §5 反馈设计。
  - **4.1 三段定义（官方）** `L128` — 关键限定：INP 只测到"下一帧被绘制"，不测交互的最终结果（网络请求、异步更新）。所以"点了有反应"和"点了数据到了"是两件事，前者是 INP，后者是 §5 反馈设计。
  - **4.2 计分口径（容易记错的细节）** `L138` — - 只统计 click / tap / 键盘三类交互。hover、滚动、缩放不计入 INP。
  - **4.3 长任务 50ms：RAIL 与 INP 的分工** `L146` — - RAIL：用户输入应在 50ms 内处理完，以保证 100ms 内有可见响应（人手感的上限）。
  - **4.4 设计侧能直接改善 INP 的四件事** `L154` — 1. 减少同屏可交互元素数量：一个页面 300 个按钮，事件委托与命中测试都变贵。
- **5. CLS：公式、五个位移源、设计侧防抖清单** `L163` — layout shift score = impact fraction × distance fraction
  - **5.1 官方公式** `L165` — - impact fraction：不稳定元素在前后两帧中可见区域的并集 ÷ 视口面积（变化前后的位置都算）。
  - **5.2 什么算位移（判定表）** `L184`
  - **5.3 五个位移源 + 设计侧对策** `L193` — hadRecentInput 的 500ms 是"免责窗口"，不是"允许跳"。用户点了按钮，界面在 400ms 后把下面内容顶下去，虽然不计分，但观感极差。
  - **5.4 设计侧的 CLS 五条铁律** `L205` — 1. 稿子上的每一个图片框，都要标比例（16:9 / 4:3 / 1:1）。没标比例 = 上线必抖。
- **6. 性能预算：给每个页面类型一个数字** `L215` — 关键路径资源 < 170KB（压缩/最小化后）、TTI < 5s（慢速 3G + 中位移动设备）。
  - **6.1 官方基线（可直接引用）** `L217` — 关键路径资源 < 170KB（压缩/最小化后）、TTI < 5s（慢速 3G + 中位移动设备）。
  - **6.2 分页面类型的预算表（建议值，需按项目校准）** `L223` — 预算的用法（这是关键）：预算不是给开发看的数字，是设计评审的否决权。
  - **6.3 预算怎么落进流程** `L238` — 超预算时官方给的三选一：优化现有资产 / 删掉现有功能 / 不加这个功能。没有第四选项"先上再说"。
- **7. 图片：设计师最直接的性能杠杆** `L251` — 三条硬结论（官方）：
  - **7.1 格式选择矩阵** `L253` — 三条硬结论（官方）：
  - **7.2 尺寸数学（这一节能省掉一半流量）** `L270` — 核心事实：浏览器会下载整张图，然后缩放到显示尺寸。你写 width: 400px 不会让浏览器只下载 400px 宽的图。
  - **7.3 响应式图片五条规则** `L286` — 1. srcset 用 w 描述符 + sizes 给布局宽度；sizes 写错等于白做（浏览器按 sizes 算需要多少像素）。
  - **7.4 LCP 图三规则（与 §3 呼应）** `L305` — 1. fetchpriority="high"，且全页最多 1–2 张。
  - **7.5 质量参数（量级估计，需按图校准）** `L311` — 这三个区间是起点不是结论。做法：同一张图导出三档，在目标显示尺寸下（不是 100% 放大）肉眼比对，取第一个"看不出差别"的档。
- **8. 字体：最容易被设计师低估的成本** `L324` — - 字体未到时浏览器通常延迟文本渲染 → 拖 FCP，常拖 LCP。
  - **8.1 字体为什么贵** `L326` — - 字体未到时浏览器通常延迟文本渲染 → 拖 FCP，常拖 LCP。
  - **8.2 font-display 五档（官方数值）** `L332` — 默认行为（不写时）：Chromium/Firefox 阻塞文本渲染最长 3s；Safari 无限期阻塞。这就是"某些手机上首屏一片空白"的常见原因。
  - **8.3 体积四招（按收益排序）** `L346` — 1. 子集化（最大收益）：unicode-range 声明可用字符范围，浏览器按需下载。工具：subfont、glyphhanger；Google Fonts 支持 text= 参数。中文站必做：只含首屏常用字的子集常在 30–80KB 量
  - **8.4 加载三纪律** `L353` — 1. @font-face 声明内联进 <head（不是外部 CSS），让浏览器尽早发现。但不要内联字体文件本身（会延迟 HTML 交付）。
  - **8.5 用 size-adjust 消灭字体抖动（CLS）** `L364` — 思路：把回退字体的度量调成目标字体的度量，让交换前后占位一致。
  - **8.6 字体数量纪律（与 brand-identity.md 一致）** `L391` — - ≤ 2 族、≤ 3 字重（设计侧）；≤ 2 个字体文件（性能侧）。
- **9. JavaScript：设计师看不见但逃不掉的那部分** `L399` — 评审时的提问模板：「这个效果需要引入多少 KB？有没有 0KB 的 CSS 实现？」——这一问能挡掉一半的性能债。
  - **9.1 三条数量级** `L401`
  - **9.2 设计决策如何变成 JS** `L410` — 评审时的提问模板：「这个效果需要引入多少 KB？有没有 0KB 的 CSS 实现？」——这一问能挡掉一半的性能债。
  - **9.3 代码分割与第三方脚本** `L423` — - 路由级分割是默认动作：只加载当前页需要的 JS。
- **10. 视觉手法的性能价格表（本轮核心）** `L431` — 怎么用：设计评审时逐个效果对照。价格是机制判断 + 量级估计，不是精确基准；星级越高越该找替代方案。
- **11. 渲染性能：帧预算与图层内存（可算的数）** `L465` — 这 16.67ms 要同时装下：事件处理 + JS + 样式计算 + 布局 + 绘制 + 合成。所以留给 JS 的时间实际只有 ~10ms 量级。
  - **11.1 帧预算** `L467` — 这 16.67ms 要同时装下：事件处理 + JS + 样式计算 + 布局 + 绘制 + 合成。所以留给 JS 的时间实际只有 ~10ms 量级。
  - **11.2 只动 transform 与 opacity** `L477` — 展开动画的正确写法（不碰 height）：
  - **11.3 图层内存：will-change 的真实代价** `L494` — will-change: transform 会让元素提升为独立合成层，内存按 宽 × 高 × 4 字节（RGBA）计：
  - **11.4 三个高频性能反模式（代码级）** `L511` — ---
- **12. 设计决策分级：什么时候可以"花"性能** `L521` — 不是所有页面都该为速度牺牲表现力。先判页面类型，再判可花的额度。
  - **12.1 三档** `L525`
  - **12.2 C 档的四条硬约束（否则就是"自我感动的设计"）** `L533` — 1. 首屏仍要 2.5s：氛围放在首屏之后（滚动第二屏再放视频/3D），不要拿 LCP 换。
  - **12.3 一句可复用的立场** `L540` — 性能预算不是"不能做好看"，是"必须选择在哪里好看"。
- **13. 弱网与低端设备：降级不是可选功能** `L547` — css
  - **13.1 三层降级** `L549` — css
  - **13.2 弱网下的设计对策（不是技术对策）** `L571`
  - **13.3 一条常被忽略的规则** `L581` — 首屏之外的图片一律 loading="lazy"，但"首屏"的定义是视口内，不是"页面顶部"。
- **14. 微信小程序：另一套物理规律** `L589` — 1. 分包加载（官方称"优化启动耗时效果最明显的手段"）：按功能/使用频率拆包，按需加载。
  - **14.1 官方硬数值** `L591`
  - **14.2 五条官方优化手段（按收益排序）** `L600` — 1. 分包加载（官方称"优化启动耗时效果最明显的手段"）：按功能/使用频率拆包，按需加载。
  - **14.3 设计侧最该记的三条** `L608` — 1. 图片不要进包，走 CDN。官方明确：包内图片/字体"难以进一步被压缩"，影响远大于代码。包内只放小图标。
  - **14.4 小程序性能自检（5 条）** `L618` — - [ ] 主包 ≤ 2MB？有没有把只在分包用的组件写进全局 usingComponents？
- **15. 度量与验收：看哪个数、在哪看** `L628` — ① 现场 p75 达标？
  - **15.1 工具分工** `L630`
  - **15.2 验收顺序（别搞反）** `L642` — "本地 Lighthouse 100 分"不是验收通过。官方明确：实验室测量不能替代现场测量。
  - **15.3 性能预算进 CI 的三行配置（示意）** `L654` — ---
- **16. 反模式清单（20 条，逐条对照）** `L674` — 1. 首屏用背景视频，且 poster 是 2MB 的 PNG。
- **17. 交付自检（18 项，全过才算过关）** `L699` — 首屏与 LCP
- **18. 可抄代码** `L731` — html
  - **18.1 首屏 LCP 图（最优组合）** `L733`
  - **18.2 折叠线以下图片（防 CLS + 懒加载）** `L752`
  - **18.3 字体（子集 + 度量对齐 + 性能优先）** `L760`
  - **18.4 只动合成器属性的入场动画** `L783`
  - **18.5 用 IntersectionObserver 替代滚动回调** `L799`
  - **18.6 省流与慢网降级** `L811` — ---
- **19. 数据来源** `L827` — - web.dev · Web Vitals：LCP ≤2.5s / INP ≤200ms / CLS ≤0.1、75 百分位、移动桌面分段、现场优先、TBT 作为 INP 代理

### `references/portfolios.md` · 作品集 — Portfolios
_194 行 · 快照 2026-10-29 · 8 节_

- **用法** `L5` — 这是审美校准素材：当 agent 需要判断「什么是好的界面」时，参考这些一线从业者的作品构成方式；也用于给用户推荐可对标的作品集风格。
- **Founders & Makers (17)** `L9` — - Emil Kowalski — Creator of Sonner, Vaul, and animations.
- **Design (41)** `L29` — - Rauno Freiberg — Author of Interaction Guidelines at Vercel.
- **Development (30)** `L73` — - Sarah Drasner — Engineering leader and web animation author.
- **Creative Development (13)** `L106` — - Jhey Tompkins — Creative developer building playful CSS experiments.
- **Design Engineering (55)** `L122` — - Arlan Marat — Design engineer from Waymo and Yandex.
- **Studios (4)** `L180` — - Unlimited Studio — Independent studio crafting bespoke digital identities.
- **Other (6)** `L187` — - Krutik Raut — Creative portfolio of Krutik - Designer and Developer who makes pixels behave

### `references/presentation-design.md` · 演示文稿与幻灯片版式（Presentation Design）
_1129 行 · 快照 2026-11-05 · 90 节_

- **目录** `L10` — 1. 尺寸与比例
- **1. 尺寸与比例** `L33` — - PowerPoint 2013+ 默认 16:9（13.333×7.5 英寸）
  - **1.0 速查表** `L35`
  - **1.1 16:9 是事实标准** `L47` — - PowerPoint 2013+ 默认 16:9（13.333×7.5 英寸）
  - **1.2 何时用 4:3** `L54`
  - **1.3 混合比例的坑** `L63` — - PowerPoint 不支持同一文件内不同比例的幻灯片——所有幻灯片必须共享同一尺寸
  - **1.4 分辨率与导出** `L69` — ---
- **2. 安全区与边距** `L81` — PowerPoint 无传统页边距（不像 Word），用以下方式模拟：
  - **2.0 速查表** `L83`
  - **2.1 为什么需要安全区** `L91`
  - **2.2 边距实操** `L100` — PowerPoint 无传统页边距（不像 Word），用以下方式模拟：
  - **2.3 版心推荐值（16:9 / 1920×1080）** `L108` — ---
- **3. 字号体系与可读性** `L122` — 最小字号：24pt（现场演示）/ 18pt（无障碍底线）/ 14pt（仅阅读型讲义）
  - **3.0 核心铁律** `L124` — 最小字号：24pt（现场演示）/ 18pt（无障碍底线）/ 14pt（仅阅读型讲义）
  - **3.1 字号阶梯（现场演示型）** `L129`
  - **3.2 字号阶梯（阅读型讲义 / Slidedoc）** `L141` — 阅读型演示文稿不是"放大的瞬间"，是"缩小的文档"。字号可以更小，但层次要更清晰。
  - **3.3 字号阶梯（海报型 / 社媒分享）** `L151`
  - **3.4 字体选择** `L159`
  - **3.5 字体使用禁忌** `L168` — - ❌ 禁止 Comic Sans（"会丧失可信度"）
  - **3.6 可读性验证方法（Nancy Duarte 法）** `L180` — 测量显示器对角线英寸数 → 后退相同数值的英尺数 → 检查是否清晰
  - **3.7 字号一致性规则** `L190` — - 同一层级文字全篇字号一致：所有标题同一字号，所有正文同一字号
- **4. 文字密度限制** `L199` — 中文字符宽度约为英文单词的 1/2 到 1/3，但信息密度更高。调整规则：
  - **4.0 速查表** `L201`
  - **4.1 哪条规则该用** `L211`
  - **4.2 中文文字密度** `L221` — 中文字符宽度约为英文单词的 1/2 到 1/3，但信息密度更高。调整规则：
  - **4.3 项目符号（Bullet Points）使用纪律** `L231` — - ✅ 仅用于：规格说明、流程步骤、并列要点
  - **4.4 一页一信息原则** `L238` — 每张幻灯片传达一个核心信息。
- **5. 母版与占位符** `L246` — 1. 视图 → 幻灯片母版
  - **5.0 母版是什么** `L248`
  - **5.1 必备版式清单（6–8 种上限）** `L256`
  - **5.2 母版设置步骤（PowerPoint）** `L269` — 1. 视图 → 幻灯片母版
  - **5.3 占位符规则** `L282` — - ✅ 始终用占位符而非手动文本框——占位符保证阅读顺序（无障碍）
  - **5.4 logo 放置** `L290` — ---
- **6. 动画与转场** `L301` — 1. 同一演示文稿全篇统一 1 种转场——不要每页不同
  - **6.0 定义区分** `L303`
  - **6.1 动画四类** `L311`
  - **6.2 转场三档** `L320`
  - **6.3 动画与转场铁律** `L328` — 1. 同一演示文稿全篇统一 1 种转场——不要每页不同
  - **6.4 何时应完全避免动画** `L338` — Lumen Learning / Public Speaking 教材的立场：
  - **6.5 Morph（变体）使用指南** `L346` — ---
- **7. 投影对比度与配色** `L358` — bash
  - **7.0 对比度阈值** `L360`
  - **7.1 投影 vs 屏幕的差异** `L368`
  - **7.2 安全配色策略** `L377`
  - **7.3 禁止的配色** `L386`
  - **7.4 投影对比度自检** `L395` — ---
- **8. 图表在幻灯片中的规则** `L409` — 一张幻灯片一个图表。两个图表 = 拆两页。
  - **8.0 核心原则** `L411` — 一张幻灯片一个图表。两个图表 = 拆两页。
  - **8.1 图表字号** `L415`
  - **8.2 图表在幻灯片中的尺寸** `L425`
  - **8.3 图表颜色** `L433` — - 使用 3–4 种区分色（色盲安全）
- **9. 可访问性** `L442` — 1. 用内置版式（不用手动文本框）→ 保证阅读顺序
  - **9.0 WCAG 对演示文稿的要求** `L444`
  - **9.1 可访问性实操清单** `L457` — 1. 用内置版式（不用手动文本框）→ 保证阅读顺序
  - **9.2 闪烁与光敏性** `L470` — ---
- **10. 远程与线上演示** `L481` — ---
  - **10.0 线上演示的差异** `L483`
  - **10.1 线上演示字号调整** `L493`
  - **10.2 线上演示工具适配** `L501` — ---
- **11. 中文演示场景** `L512` — - 全角标点（，。、；：""''）
  - **11.0 中文字号调整** `L514`
  - **11.1 中文字体推荐** `L523`
  - **11.2 中文标点与排版** `L531` — - 全角标点（，。、；：""''）
  - **11.3 中文演示密度** `L539` — ---
- **12. 版式构图法则** `L550` — - 用 2 条水平 + 2 条垂直假想线将幻灯片分为 9 个区域
  - **12.1 三分法则** `L552` — - 用 2 条水平 + 2 条垂直假想线将幻灯片分为 9 个区域
  - **12.2 Z 模式阅读** `L559` — - 在从左到右的语言环境中：
  - **12.3 留白规则** `L569` — - 留白 = 呼吸空间 → 吸引注意力到焦点
  - **12.4 视觉引导** `L576` — - 所有人物和动物的朝向应面向幻灯片内部，最好朝向主焦点
  - **12.5 一致性规则** `L582` — - 全篇重复使用：相同颜色、字体、图片风格、布局
- **13. 演示节奏与信息流** `L590` — Mayer (2001) 研究表明：分裂注意力影响信息保留能力。
  - **13.0 切换节奏** `L592`
  - **13.1 演讲-幻灯片节奏** `L601` — Mayer (2001) 研究表明：分裂注意力影响信息保留能力。
  - **13.2 引用语规则** `L615` — - ✅ 可以使用，但需满足：简短、清晰、少量使用
  - **13.3 信息结构（倒金字塔）** `L621` — ---
- **14. 工具与框架** `L631` — ---
  - **14.1 桌面工具** `L633`
  - **14.2 代码驱动框架** `L642`
  - **14.3 设计辅助工具** `L652`
  - **14.4 检查工具** `L661` — ---
- **15. 12 场景速查** `L672` — ---
- **16. 20 条反模式** `L691` — ---
- **17. 18 项自检** `L718` — ---
- **18. 可抄代码** `L743` — html
  - **18.1 reveal.js 基础配置** `L745`
  - **18.2 PowerPoint VBA 批量设置字号** `L800`
  - **18.3 对比度检查（Python）** `L840`
  - **18.4 Slidev 基础配置（Markdown 驱动）** `L897`
  - **18.5 CSS 幻灯片安全区模拟（通用）** `L970`
  - **18.6 Python-pptx 生成幻灯片模板** `L1045` — ---

### `references/resources.md` · 设计资源 — Resources
_225 行 · 快照 2026-10-29 · 5 节_

- **用法** `L5` — - Components：找可复用 UI 组件库与设计系统参考
- **Type & Colour (14)** `L14` — - Fontshare（免费） — High-quality professional fonts free for commercial use.
- **Components (128)** `L31` — - ForgeUI（免费+付费） — Animated React and Tailwind components and templates.
- **Motion & 3D (26)** `L162` — - Three.js（免费） — JavaScript 3D library rendering WebGL scenes.
- **Icons (33)** `L191` — - Lucide（免费） — Community-maintained Feather Icons fork with thousands of glyphs.

### `references/responsive-layout.md` · 响应式与断点体系 · Responsive Layout
_726 行 · 快照 2026-11-01 · 55 节_

- **0. 先定策略，再谈数值** `L8` — 绝大多数"响应式做不好"不是断点值选错，而是顺序错了：先抄一套断点，再往里塞布局，于是每个断点都在打补丁。
- **1. 视口断点 vs 容器断点：先选对工具** `L22` — 判断规则（照做）：
- **2. 六大体系断点精确值对照** `L55` — 同一份设计换到不同技术栈就"断错位"，原因就是各家默认值不一样。下表全部为官方默认值，可直接抄。
  - **2.1 Ant Design（中文中后台事实标准）** `L59` — - 栅格 24 栏，gutter 可为 {xs:8, sm:16, md:24} 分断点给值。
  - **2.2 Material UI（React 生态默认）** `L75` — - down(key) 是开区间：down('md') = [0, 900px)，内部用 step: 5 生成 max-width: 899.95px。这就是为什么不要自己手写 max-width: 899px——差 1px 会漏掉 899
  - **2.3 Tailwind CSS v4（默认 rem，可换算）** `L88` — - sm: 不是"小屏"，是"从 sm 断点起"。给手机写样式要用不带前缀的类。这是 Tailwind 最高频的误用。
  - **2.4 Bootstrap 5.3（断点 + 版心一起看）** `L103` — 这张表的第二列比第一列更有用：它给出了一套经过验证的「版心宽度阶梯」——视口变宽时，内容区不是无限拉伸，而是跳到下一个固定版心。自己做站时直接抄这一列。
  - **2.5 IBM Carbon 2x Grid（列数会变的那一派）** `L116` — - 基础单位是 8px mini unit，列宽/行高/间距/内外边距都是它的倍数。
  - **2.6 Material 3（dp，跨 Android/Web）** `L131` — - 只有 Medium 允许"低密度内容"用两栏；高信息密度在 Medium 用两栏会降低可用性。
  - **2.7 一页对照速查** `L145` — 读法：六个体系在同一语义档上最大差 96px（平板竖：768 vs 672 vs 600）。所以"抄哪家"不重要，一套用到底才重要。混用会出现"某个宽度下两套规则同时生效"的双断点 bug。
- **3. 断点该定在哪：内容断，不是设备断** `L160` — 1. 在浏览器里把窗口从 320px 连续拖到 1920px，不要跳着看。
  - **3.1 定断点的唯一正确方法** `L162` — 1. 在浏览器里把窗口从 320px 连续拖到 1920px，不要跳着看。
  - **3.2 建议默认（无特殊理由时直接用这套）** `L175` — 只有 3 档也能做出好响应式：< 768 单栏 / 768–1199 双栏 / ≥1200 三栏 + 固定侧栏。断点数量不是质量指标，每档的变化是否说得清才是。
  - **3.3 移动优先还是桌面优先** `L188` — 中后台可以正大光明用桌面优先，但必须同时满足：① 明确声明"移动端仅支持查看，不支持编辑"；② 320px 下仍不出现横向滚动（WCAG 1.4.10 不看你是不是中后台）。做不到就退回移动优先。
- **4. 跨断点做什么：五个动词** `L202` — M3 的框架最实用——跨断点时只有五种合法动作，每种都要说得出为什么。这比"这里改成两栏"具体得多。
- **5. 栅格与版心：三个必须给的数值** `L226` — 24 栏的理由：能被 2/3/4/6/8/12 整除，中文中后台四等分（6 栏）、三等分（8 栏）、二等分（12 栏）都落在整数栏上。12 栏分不出 5 等分（2.4 栏）。做五列布局时 24 栏更省事。
  - **5.1 栏数** `L228` — 24 栏的理由：能被 2/3/4/6/8/12 整除，中文中后台四等分（6 栏）、三等分（8 栏）、二等分（12 栏）都落在整数栏上。12 栏分不出 5 等分（2.4 栏）。做五列布局时 24 栏更省事。
  - **5.2 Gutter 与 Column 谁固定** `L239` — 铁律：Gutter 固定，Column 流体。
  - **5.3 版心（container max-width）** `L247` — 直接抄 Bootstrap 阶梯，或按内容定：
- **6. 流式排版：clamp() 的正确用法** `L263` — css
  - **6.1 公式** `L265` — - 解析规则：clamp(MIN, VAL, MAX) = max(MIN, min(VAL, MAX))。若 MIN MAX，MIN 胜出（不报错，静默取 MIN）——手滑写反了会得到一个永远不变的字号。
  - **6.2 无障碍硬要求（MDN 明确）** `L276` — 用 clamp() 控制字号时，最大值必须是相对单位，且不小于最小值的 2 倍。
  - **6.3 中文流式排版的三个额外约束** `L289` — 1. 行高不跟着字号线性缩。中文行高在小字号需要更大比例：14px 用 1.7，18px 用 1.6，32px+ 用 1.4。写成 line-height: clamp(1.4, 1.8 - 0.01vw, 1.75) 意义不大——按字号档
  - **6.4 字号阶梯在各断点的取值（建议）** `L295` — 只允许 5–6 档。每多一档，团队就多一个"这个标题该用 26 还是 28"的争论。
- **7. 视口单位：100vh 是个陷阱** `L310` — 关键事实：vh 当前等同于 lvh，也就是说 height: 100vh 在手机上是"地址栏收起时的高度"。地址栏一展开，底部内容被遮住 —— 这是移动端 H5 最常见的 bug。
- **8. 响应式图片：三条规则 + 一个防抖** `L336` — html
  - **8.1 分辨率切换（同一图，不同大小）** `L338` — 规则（全部来自 MDN，逐条都是硬要求）：
  - **8.2 固定尺寸、多倍屏（logo / 头像 / 图标）** `L357` — 用 x 描述符时不写 sizes。1x 可省略。
  - **8.3 艺术指导（不同构图，不只是不同大小）** `L365` — - 必须保留最后的 <img src alt 作为兜底。
  - **8.4 防布局偏移（CLS）** `L379` — - 永远写 width / height 属性。它们只用来确定宽高比，不必等于实际渲染尺寸。
- **9. 表格在窄屏的降级（移动端表格 / 手机表格 / 表格变卡片）：四种策略** `L388` — 表格是响应式最难的一环，因为它天然是二维的。四种策略各有明确适用条件，选错就白做。
  - **9.1 策略对照** `L392`
  - **9.2 决策规则（按顺序问）** `L401` — 1. 用户在小屏上需要"横向比较同一字段的多行值"吗？（比价、对账、看谁最高）→ 是 → A（横滚 + 粘性首列），不要卡片化。
  - **9.3 WCAG 1.4.10 的例外边界（常被误读）** `L410` — 原文允许「需要二维布局才能使用或表达含义的部分」例外，明确举例包含 data tables（但不含单独单元格）。但有三个边界：
  - **9.4 可抄骨架** `L420` — - 横滚容器要有可见提示（右侧渐隐遮罩或"← 左右滑动 →"），否则用户不知道右边还有内容。
- **10. 表单在窄屏** `L442` — - 粘底提交栏：position: sticky; bottom: 0 + padding-bottom: env(safe-area-inset-bottom)。移动端长表单没有粘底按钮，用户会滚到顶部找"提交"。
- **11. 导航降级：一条标准路径** `L458` — - 底部 tab 只放 ≤5 项，超过就用"更多"。M3 与 iOS 都是这个上限。
- **12. 中后台适配（中文场景专用）** `L473` — Ant Design 布局规范给了明确口径，直接采用：
- **13. 触控与鼠标：两套输入不能共用一套假设** `L504` — 照做：
- **14. 调试与验收** `L530` — 320 / 375 / 414 / 768 / 1024 / 1280 / 1366 / 1440 / 1920
  - **14.1 必测宽度（8 档）** `L532` — 320 / 375 / 414 / 768 / 1024 / 1280 / 1366 / 1440 / 1920
  - **14.2 每档检查 6 件事** `L538` — 1. 有没有横向滚动条（document.documentElement.scrollWidth clientWidth）→ 有就是 bug，除非是 §9 允许的表格容器。
  - **14.3 缩放进阶测试（无障碍必做）** `L547` — - 200% 缩放（Cmd/Ctrl + + 到 200%）：文字是否可读、是否截断（WCAG 1.4.4）。
  - **14.4 一条命令自查横向溢出** `L553` — ---
- **15. 反模式 20 条** `L565` — 1. 先抄断点再设计布局（顺序反了）。
- **16. 自检 15 项（有响应式要求时逐条过）** `L590` — 1. 断点数量 ≤5，且每个断点都能说出一句"这个宽度下什么变了"？
- **17. 可抄代码** `L610` — css
  - **17.1 媒体查询骨架（移动优先）** `L612`
  - **17.2 容器查询卡片（同一组件两种宽度）** `L624`
  - **17.3 流式字号（无障碍合规）** `L639`
  - **17.4 响应式表格（横滚 + 粘性首列 + 提示）** `L651`
  - **17.5 安全区底部操作栏** `L670`
  - **17.6 只在真 hover 设备上做悬停效果** `L681` — ---
- **18. 与其他资产的分工** `L696` — ---
- **19. 数据来源** `L711` — - Ant Design Grid（24 栅格与 xs→xxxl 精确值）：https://ant.design/components/grid

### `references/shape-elevation.md` · 形状与深度系统（Shape & Elevation）
_819 行 · 快照 2026-11-08 · 40 节_

- **1 · 为什么单列形状与深度系统** `L17` — 圆角 阴影 高度 材质 形状 elevation 是和色彩、排印并列的基础支柱，但此前 37 份参考里零独立文件；缺口用 dpsearch.py 与词频统计判定为结构性空白而非覆盖不足。
- **2 · 五层模型：先判层，再谈审美** `L31` — 需求里出现「圆角 阴影 高度 材质 形状 elevation」时先定位是哪一层坏了；层叠与边界问题往往在 L5/L3，换圆角半径根本修不了。
- **3 · 裁决一：elevation 是语义 z-height，不是可直接抄写的阴影值** `L47` — M3 官方 elevation 原文与 elevation.css 的单长度 box-shadow 存在误读风险；把高度 token 当 CSS 阴影抄进项目会产出无效声明。
- **4 · M3 Elevation 六级精确表与组件映射** `L78` — M3 component elevation 官方表给出 6 级高度 level0–level5 / dp：0 / 1 / 3 / 6 / 8 / 12；这是层级顺序不是阴影参数。
- **5 · 裁决二：阴影不能充当 WCAG 1.4.11 的 3:1 识别边界** `L99` — WCAG 2.2 SC 1.4.11 非文本对比度要求组件边界对相邻色至少 3:1；本轮用 WCAG 相对亮度公式实跑证明常用半透明阴影只到 1.1–1.3:1，不能算边界。
- **6 · 非文本 3:1 的正确落点（边界 / 焦点 / 状态）** `L125` — 输入框 按钮 开关 边界线 焦点框 阴影 对比度 3:1 的合规信号必须是独立元素；阴影只做叠加氛围，不承担识别责任。
- **7 · box-shadow 正式语法（MDN 逐条核验）** `L144` — box-shadow 需要 2/3/4 个 <length：offset-x offset-y [blur-radius [spread-radius]]；多阴影逗号分隔且第一个在最上，不占布局空间，跟随圆角。
- **8 · 七体系阴影 token 精确对照（源码 / 官方文档实测）** `L167` — 真实说法：「Tailwind shadow-md 默认值到底是多少」「Ant Design 圆角和阴影默认值抄哪」——下表把 Tailwind v4 / MUI / Ant Design 5 / TDesign / Arco / Carbo
  - **8.1 Tailwind CSS v4（box-shadow 官方文档逐字）** `L171` — v4 把这些值放在 --shadow- 自定义属性里，可用 shadow-(<custom-property) 直接接自己的变量——这是把深度 token 化的最低成本路径。注意 shadow-2xl 的 alpha 跳到 0.25，跨档不
  - **8.2 MUI（packages/mui-material/src/styles/shadows.js 源码实测）** `L186` — 共 25 档（shadows[0] = 'none'，其后 24 档）。三个固定 alpha 对应物理分解：umbra（本影，最紧最暗 0.20）、penumbra（半影 0.14）、ambient（环境光 0.12）。这解释了"为什么专业
  - **8.3 Ant Design 5（customize-theme 官方表逐字）** `L198` — 同为三层，alpha 分别 0.08 / 0.12 / 0.05，比 MUI 更淡。注意 spread 一负一正（-4px / 8px）：第三层用正 spread 做大范围柔光，这是"淡但不糊"的关键。
  - **8.4 TDesign（Tencent/tdesign-common/style/web/theme/light.less 源码实测）** `L207` — TDesign 只有 3 档，且档位越高 alpha 反而越淡（5%→4%）——靠更大的 blur / spread 拉开距离感，而不是把阴影加黑。这是与 MUI/Tailwind 不同的思路，直接混用两套会打架。官方设计 token 页原
  - **8.5 Arco Design（官方 token 页）** `L217` — 阴影 token 名为 shadow-special、shadow1-center、shadow2-center、shadow3-center（"center" 表示无 y 偏移的四周扩散型）。取源限制：本轮抓取返回的是变量名与分类，未取得
  - **8.6 Carbon（不用阴影表达层级）** `L221` — Carbon Layering 明确用 neutral gray palette 的 layered colors 表达 depth / spatial association，而非投影：light themes 在 White ↔ Gra
  - **8.7 M3（语义高度 + 已废弃的 surface tint）** `L225` — 见 §3 §4。M3 现代表达是"语义 level + 表面色角色"，Surface tint color is deprecated.。
  - **8.8 横向结论** `L229` — 没有一套是"通用正确"的。选型先定语言（§19），再从这一套里取完整值；把 Tailwind 的 shadow-sm 和 TDesign 的 --td-shadow-3 混在同一页面，等于两套光源模型打架。
- **9 · 三层阴影为什么够：物理分解与克制原则** `L245` — 三层阴影 umbra penumbra ambient 对应一个光源的三种遮挡；阴影应当 subtle，看得清就说明太重——这是 impeccable/spatial-design.md 的原文立场。
- **10 · 裁决三：圆角是几何契约，不是装饰常数** `L259` — border-radius 正式语法是 <length-percentage[0,∞]{1,4} [ / <length-percentage[0,∞]{1,4} ]?；百分比水平轴参照 width、垂直轴参照 height，负值无效。
- **11 · Corner overlap：半径按比例缩减的规范公式** `L275` — 圆角重叠 corner overlap 的规范处理是 f = min(Li / Si)，f < 1 时所有角半径乘 f 等比缩减；实跑验证 100×40 写 30px 只生效 20px。
- **12 · 嵌套同心圆角 r = R − p 与失效条件** `L303` — 嵌套圆角 同心圆角 concentric radius 的规则是内圆角 r = R − p；r ≤ 0 时公式失效，不能硬套负数。
- **13 · 七体系圆角 token 精确对照与 M3 Expressive 更新** `L329` — 真实说法：「定一套圆角 token 该有几档」「形状尺度怎么定」——圆角 token 对照：M3 4/8/12/16/28、TDesign 2/3/6/9/12/999、Ant 2/4/6/8、Arco 0/2/4/8；M3 Express
  - **13.1 精确值（官方原文 / 源码实测）** `L333` — 观察：国内体系（Ant 6 / TDesign 3 / Arco 4）的默认圆角明显小于 M3（medium 12 / large 16）。这不是"谁更现代"，是信息密度不同：中后台表格、表单密集，大圆角会吞掉可用空间并让相邻控件看起来松散
  - **13.2 M3 Expressive（2025-05）更新要点** `L347` — - 新增 35 个 shapes 与 shape morphing（形状在状态间平滑变形）。
- **14 · corner-shape 与 squircle：实验特性，不进生产** `L358` — corner-shape 是 MDN 标记为 Experimental 的属性，依赖 border-radius；没有有效 border-radius 或解析为 0 时完全不生效。
- **15 · 表面层级：不用阴影也能表达深度（Carbon 与暗色重排）** `L376` — 表面层级 surface layering 的第二条路线是用中性灰色阶交替，而非投影；亮色 White ↔ Gray 10 交替、暗色每加一层变浅一个 step。
- **16 · 材质与玻璃：Apple HIG Materials / Liquid Glass 的分层边界** `L392` — 材质 毛玻璃 Liquid Glass 只用于 controls / navigation 的 functional layer，不要用于 content layer；clear 变体在明亮背景上建议加 35% 暗色 dimming lay
- **17 · 玻璃拟态的合成开销与降级顺序** `L410` — 玻璃拟态的真实代价在每帧对背景区域重采样；降级顺序是「减层数与半径 → 加暗色遮罩 → 换实色表面」，不是只去掉透明度。
- **18 · z-index 语义刻度与 stacking context** `L426` — z-index 不该写魔法数；用 dropdown → sticky → modal-backdrop → modal → toast → tooltip 的语义刻度，并检查父级 stacking context。
- **19 · 深度语言三选一：阴影 / 表面色 / 材质** `L450` — 深度语言 阴影 表面色 材质 必须三选一做主导；混用三套等于给界面三套互相矛盾的光源与物理规则。
- **20 · 场景速查（12）** `L466` — ---
- **21 · 反模式（20）** `L485` — 1. 把阴影当 3:1 边界——白底白卡只加 rgba(0,0,0,.1)，实测 1.248:1，验收必挂。
- **22 · 自检（20）** `L510` — 1. 项目里所有 box-shadow 都至少含 2 个 <length 吗？
- **23 · 可抄代码（6 段）** `L535` — css
  - **23.1 CSS · 形状与深度 token 系统（可直接落项目）** `L537`
  - **23.2 Python · 阴影 alpha → WCAG 对比度计算器（实跑 PASS）** `L592` — 实跑输出：
  - **23.3 Python · corner overlap 与同心圆角校验器（实跑 PASS）** `L644` — 实跑输出：
  - **23.4 Python · 深度系统静态扫描器（实跑 PASS）** `L679` — 实跑输出：bad issues: 4（单长度 / elevation token / 负半径 / 魔法 z-index）· good issues: 0 · self-test PASS。
  - **23.5 CSS · 亮暗双主题的同 level 表达（不照搬阴影）** `L734`
  - **23.6 CSS · 材质层的渐进增强与可访问性降级** `L757` — ---
- **24 · 取源与限制（公开记录）** `L782` — 本轮 shape elevation 取源均标注了可核验位置与不可核验处；以下限制不臆造、不补齐，供后续轮次继续深挖。

### `references/tools.md` · 制作工具 — Tools
_182 行 · 快照 2026-10-29 · 7 节_

- **用法** `L5` — - Development：前端/开发工具
- **Development (40)** `L13` — - SVGOMG（免费） — Web GUI to optimize and clean SVG files.
- **Capture & Media (33)** `L56` — - Squoosh — Browser image compression with visual comparisons.
- **Design & Canvas (17)** `L92` — - Vessa — Publish brand guidelines as live pages.
- **Productivity & Desktop (24)** `L112` — - Butterfly — Team building the Pond Linux operating system.
- **AI & Agents (38)** `L139` — - Dray（免费） — Unified desktop workspace managing coding agents.
- **Other (1)** `L180` — - ASCII Magic — Free ASCII art generator and image & video effects studio: ASCII, pixel art, voxel, mosaic, halftone,…

### `references/typography-system.md` · 字体排印系统（Typography System）
_588 行 · 快照 2026-11-07 · 30 节_

- **1 · 为什么单列字体排印系统** `L11` — 字体排印是和色彩科学并列的基础设计支柱，但此前本知识库没有独立文件：字体知识散落在 performance-design.md（19 行，讲加载）、brand-identity.md（13 行，讲人格）、visual-style-taxon
- **2 · 排印决策的六层模型（先判层，再谈审美）** `L25` — 需求里出现「字体 / 字号 / 行距 / 排版」时，先定位是哪一层出问题，不要一上来换字体。可访问性、对比度、表单与验收问题往往落在第 2/3 层，换一款字体根本修不了。
- **3 · 字体选型：覆盖 / 回退 / 授权三个前置，而不是「挑好看的」** `L42` — 选型的可访问性、加载性能与合规验收都从这三个前置开始；「好不好看」是三关全过之后才允许问的第四个问题。缺字、锁死缩放、授权不清，都会让界面在特定用户或分发场景下直接失效。
- **4 · 字号阶梯与相对单位（px 不可访问裁决）** `L54` — 「正文用多大字号」「排版很挤该调哪里」先落到这一层：字号是可访问性与验收问题，用户在浏览器里改默认字号、改到 200%，界面必须还能读、不裁切、不重叠，表单与按钮不能丢功能。这一层出错，后面所有排印细节都没有意义。
- **5 · 行高、行长与段落节奏（可计算，不靠感觉）** `L67` — 行高与行长决定长文可读性，也是对比度、可访问性与验收里最常被跳过的一组数值；三段式节奏（行内 / 段间 / 块间）必须分开定，不能一个 line-height 打天下。
- **6 · WCAG 2.2 三关硬数值（1.4.4 / 1.4.8 / 1.4.12）** `L80` — 字体排印在 WCAG 2.2 里有三条独立准则（Resize Text / Visual Presentation / Text Spacing）；把字号放大不等于过关，三条各有自己的门槛与例外，混成一句「字号够大就行」会漏掉文本间距与行宽
- **7 · 文本间距覆盖验收（注入式实测五步）** `L98` — 这条是 1.4.12 的可执行脚本：把四项间距一次性注入页面，检查按钮、卡片与输入框是否裁切、重叠、丢功能。不改其他属性是条文硬要求，注入时别顺手改 font-size 或 padding。
- **8 · 200% 缩放与容器弹性（按钮 / 输入框 / 卡片）** `L114` — 200% 文本缩放与 1.4.12 间距覆盖是两次独立测试：一个改字号，一个改间距，两者都会让固定高度的表单与按钮失效。只测其中一次等于没验收。
- **9 · Variable Fonts 与五个注册轴** `L126` — 可变字体把「一款字重一个文件」变成连续轴，能同时解决加载体积与 CLS：但轴用错会破坏对比度与视觉层级，且必须遵守「高层 CSS 属性优先」。
- **10 · 数字特性与 tabular-nums（表格 / 时钟 / 频繁变化数值）** `L139` — 数字是排印里最容易被忽略的布局稳定性与对比度问题：比例数字让表格列歪、让计时器每跳一秒抖一次；这不是审美，是缺陷。
- **11 · 高位属性优先，低位 API 兜底** `L163` — OpenType 特性的可访问性与验收风险在于「写错层级」：低位 API 会绕过继承与级联，导致同一段文字在不同组件里表现不一致，且难以被用户样式覆盖。
- **12 · font-family 逐字符回退算法（加载 / 缺字 / 验收）** `L174` — font-family 的回退不是「找第一款已安装字体」，而是逐字符匹配；这条机制决定了 CJK 混排、缺字 tofu 与字体加载量的全部行为，也是 CLS 与验收的常见盲区。
- **13 · unicode-range 子集化与 CJK 分片（性能 / CLS / 验收）** `L186` — 「中文字体太大」「字库太大」的正解是 CJK 分片，不是缩字号：字体子集化直接决定加载体积与 LCP/CLS，也是 CJK 站点最有效的性能手段；但「分片粒度」与「下载触发条件」写错会让优化完全失效。
- **14 · font-display 时间线与五档选择（性能 / CLS / 验收）** `L199` — 字体加载策略决定 FOIT/FOUT 与 CLS，是排印与性能的交界；五档不是「哪个更好」，是「哪个能接受字体不出现」。
- **15 · size-adjust / font-size-adjust 度量对齐（FOUT 不跳版）** `L220` — FOUT 的 CLS 根因不是「换字体」，是两款字体的度量不同；把度量对齐后，swap 才能既保品牌又保布局稳定，这是可访问性与验收里最划算的一处工程修复。
- **16 · 中文排版（W3C clreq 原文核验）** `L232` — 中文排版的区域/locale 差异大于简繁差异；把视觉排版需求写进文本存储层、或按码位处理光标，都会在 CJK 与 emoji 场景下出错。以下四条均取自 W3C《Requirements for Chinese Text Layout》原
- **17 · M3 type scale 与 token 化（可复现，不抄二手数值表）** `L244` — M3 提供的是角色结构 + 行高比率 + 命名约定，不是一张可以照抄的 15 行数值表；把它落成 token 时，角色与比率可复现，精确数值必须回官方动态页或源码复核。
- **18 · 字体授权（OFL 1.1）：能做与不能做** `L258` — 授权不合规会让整个产品无法分发；这一层先于审美，且逐字体检查而不是看仓库级 license。以下取自 SIL OFL 1.1 官方英文原文（Preamble + PERMISSION & CONDITIONS 五条件）。
- **19 · 工具链与 GitHub API 实测数据（2026-11-07）** `L281` — 凡涉及 star / 许可 / 更新时间一律用 GitHub REST API 实测，不凭记忆写数字；NOASSERTION 不等于「无许可」，只代表 API 未自动识别，需进仓库读许可文件。
- **20 · 场景速查（12）** `L303` — ---
- **21 · 反模式（20）** `L322` — 1. 正文 font-size: 14px 写死 → 用户改不了默认字号，MDN 判为 not accessible（§4）。
- **22 · 自检（20）** `L347` — - [ ] 正文字号是 rem 而非 px，且能说清 MDN「Defining font sizes in px is not accessible」的理由？
- **23 · 可抄代码（6 段）** `L372` — css
  - **23.1 CSS · rem 字号阶梯与两档行高（可抄）** `L374`
  - **23.2 CSS · @font-face 三件套（font-display / unicode-range / size-adjust）** `L422`
  - **23.3 CSS · WCAG 2.2 SC 1.4.12 文本间距覆盖验收书签** `L454`
  - **23.4 CSS · 可变字体：高层属性优先 + custom 轴兜底** `L474`
  - **23.5 Python · 排印静态扫描 lint（含自测用例）** `L498`
  - **23.6 CSS · 中文混排与字素丛友好的输入层** `L549` — ---
- **24 · 取源与限制（公开记录）** `L575` — - 已逐条联网核验（官方原文）：W3C WCAG 2.2 Understanding SC 1.4.12（四项数值、Exception、Note 1/2、Applicability、Author/User Responsibility）；M

### `references/ux-writing.md` · 内容设计与 UX 文案 — UX Writing & Content Design（深度蒸馏）
_818 行 · 快照 2026-11-05 · 74 节_

- **一、总则：文字是界面的一部分，不是装饰** `L10` — 界面文字的唯一目标是帮用户高效完成任务。不是展示文采，不是表现幽默，不是"写得短"。判断标准只有一条：用户读完之后知道该干什么吗？
  - **1.1 三级文案尺寸（NN/g 2025-05 定义）** `L14` — 关键：microcopy 占界面文字的 80% 以上，但它不能独自构成完整体验。三层互相嵌套：long 里用 short 和 micro 来分段，short 里用 micro 做标题和按钮。
  - **1.2 五条不可商量原则** `L24`
  - **1.3 扫描行为数据（设计文案的数据基础）** `L34` — 推论：标题和按钮的关键词放前 2 个词。不是"Learn more about our new features"，是"New features — learn more"。
- **二、按钮与操作文案（UI Copy）** `L49` — 中文按钮2–4 字最佳，动词开头，不加"请"字。
  - **2.1 按钮文案规则** `L51`
  - **2.2 主次按钮文案配对** `L63`
  - **2.3 中文按钮文案（B 端特有）** `L73` — 中文按钮2–4 字最佳，动词开头，不加"请"字。
  - **2.4 省略号规则（…）** `L88` — 注意：中文省略号是 ……（6 点），英文是 …（3 点 U+2026）。不要用三个句点 ...。
- **三、错误文案（最高频的文案翻车点）** `L100` — 每条错误文案必须包含三层，缺一不可：
  - **3.1 错误文案结构（NN/g 三层）** `L102` — 每条错误文案必须包含三层，缺一不可：
  - **3.2 禁用词表** `L118`
  - **3.3 错误文案位置与时机** `L132`
  - **3.4 中文错误文案模板** `L145` — 优设 B 端句式：
  - **3.5 错误文案字数** `L165` — ---
- **四、空态文案（Empty State Copy）** `L176` — - 禁用俏皮话（NN/g + Apple HIG）：空态是暂时的，别让用户每次都看同一个笑话
  - **4.1 空态文案五件套** `L178`
  - **4.2 五种空态（区分文案策略）** `L188`
  - **4.3 空态文案禁令** `L198` — - 禁用俏皮话（NN/g + Apple HIG）：空态是暂时的，别让用户每次都看同一个笑话
- **五、语气与语调（Tone of Voice）** `L207` — 语气不是"什么调子"，是四个正交轴上的位置：
  - **5.1 四维度模型（NN/g）** `L209` — 语气不是"什么调子"，是四个正交轴上的位置：
  - **5.2 场景 × 语气矩阵** `L225`
  - **5.3 语调校准方法（NN/g 三步）** `L238` — 1. 定品牌基线：在四维度上标出品牌默认位置（如：Casual + Serious + Respectful + Matter-of-fact）
  - **5.4 禁用语气** `L244` — ---
- **六、表单文案** `L257` — ---
  - **6.1 标签（Label）** `L259`
  - **6.2 占位符 vs 标签** `L270`
  - **6.3 帮助文案（Helper Text）** `L280`
  - **6.4 设置项文案（Apple HIG + GOV.UK）** `L290` — ---
- **七、对话框与通知文案** `L301` — ---
  - **7.1 对话框（Dialog / Modal）** `L303`
  - **7.2 Toast / Message / Snackbar** `L314`
  - **7.3 Notification（右上角通知）** `L325`
  - **7.4 Tooltip** `L335` — ---
- **八、引导与 Onboarding 文案** `L346` — - 禁用功能清单：不列"功能 1/2/3"，用户不关心你的功能列表
  - **8.1 Onboarding 文案原则** `L348`
  - **8.2 Onboarding 文案结构** `L358`
  - **8.3 Onboarding 禁令** `L367` — - 禁用功能清单：不列"功能 1/2/3"，用户不关心你的功能列表
- **九、导航与信息架构文案** `L376` — ---
  - **9.1 导航菜单标签** `L378`
  - **9.2 标签页（Tab）标签** `L388`
  - **9.3 面包屑** `L396` — ---
- **十、术语管理与一致性** `L406` — 同一产品里把"项目"叫成"项目""工程""workspace""空间"——用户不知道这些是不是同一个东西。术语表是文案一致性的基础设施。
  - **10.1 为什么需要术语表** `L408` — 同一产品里把"项目"叫成"项目""工程""workspace""空间"——用户不知道这些是不是同一个东西。术语表是文案一致性的基础设施。
  - **10.2 术语表结构** `L412`
  - **10.3 一致性规则** `L422` — ---
- **十一、大小写与标点** `L434` — 为什么 sentence case：
  - **11.1 大小写（英文）** `L436` — 为什么 sentence case：
  - **11.2 中文标点（优设 B 端规范）** `L450`
  - **11.3 句末标点** `L463` — ---
- **十二、数字、日期与单位** `L479` — ---
  - **12.1 数字** `L481`
  - **12.2 日期与时间** `L492`
  - **12.3 文件大小** `L503` — ---
- **十三、国际化文案注意事项** `L513` — 设计含义（v20 修正，冲突时以 i18n-localization.md §2 为准）：上表是段落/中长文案的经验膨胀率，不能套到按钮、标签、tab、导航等 microcopy 上。W3C 转引 IBM 官方表：英文 ≤10 字符平均膨胀
  - **13.1 文案膨胀** `L515` — 设计含义（v20 修正，冲突时以 i18n-localization.md §2 为准）：上表是段落/中长文案的经验膨胀率，不能套到按钮、标签、tab、导航等 microcopy 上。W3C 转引 IBM 官方表：英文 ≤10 字符平均膨胀
  - **13.2 国际化禁忌** `L526` — ---
- **十四、可访问性与文案** `L538` — ---
  - **14.1 aria-label 与可见文案** `L540`
  - **14.2 读屏测试** `L549`
  - **14.3 文案可读性** `L559` — ---
- **十五、内容设计系统化** `L571` — 像设计 token 一样，把文案做成可复用的变量：
  - **15.1 文案 token（Content Tokens）** `L573` — 像设计 token 一样，把文案做成可复用的变量：
  - **15.2 文案评审清单（快速 PR 检查）** `L597` — ---
- **十六、12 场景速查** `L612` — ---
- **十七、20 条反模式** `L631` — ---
- **十八、18 项自检清单** `L658` — ---
- **十九、可抄代码** `L683` — html
  - **19.1 错误文案模板（中文）** `L685`
  - **19.2 对话框文案模板** `L707`
  - **19.3 空态文案模板** `L720`
  - **19.4 文案 Token 系统（JSON）** `L732`
  - **19.5 aria-live 错误播报** `L787`
  - **19.6 链接文案检查脚本** `L799` — ---

### `references/visual-hierarchy-gestalt.md` · 视觉层级与格式塔组织律（Visual Hierarchy & Gestalt / Attention & Cognitive Load）
_670 行 · 快照 2026-11-08 · 34 节_

- **1 · 为什么单列视觉层级与格式塔** `L19` — 圆角、阴影、字号、色彩都已有独立资产，唯独「用户先看哪、看完往哪走、走完累不累」始终散在边角。缺口用 dpsearch.py 与全域词频统计判定为结构性空白而非覆盖不足。
- **2 · 三层模型：先判层，再谈放大加粗** `L31` — 任何「重点不突出 / 信息太乱 / 用户找不到」的问题，先判落在哪一层，不要一上来就改字号。
- **3 · 裁决一：F 型是默认行为，不是设计目标** `L45` — 来源：NN/g F-Shaped Pattern of Reading on the Web: Misunderstood, But Still Relevant (Even on Mobile)，Kara Pernice，2017-11-
- **4 · 扫描模式全表：F 只是其中一种** `L67` — NN/g 2017 原文命名/描述的模式（逐项核对，未标"命名"的是描述性表述）：
- **5 · 裁决二：四条 WCAG 准则构成的顺序契约** `L87` — 视觉层级若只存在于渲染结果里，对读屏与键盘用户就不存在。以下四条均取自 W3C WAI《Understanding WCAG 2.2》原文。
  - **5.1 SC 1.3.2 Meaningful Sequence（Level A）** `L91` — "When the sequence in which content is presented affects its meaning, a correct reading sequence can be programmatically
  - **5.2 SC 2.4.3 Focus Order（Level A）** `L101` — "If a web page can be navigated sequentially and the navigation sequences affect meaning or operation, focusable compone
  - **5.3 SC 2.4.6 Headings and Labels（Level AA）** `L111` — "Headings and labels describe topic or purpose."
  - **5.4 SC 2.4.10 Section Headings（Level AAA）** `L117` — "Section headings are used to organize the content."
  - **5.5 四条准则的分工表** `L123` — ---
- **6 · 三顺序一致性验收：DOM / 焦点 / 标题树** `L134` — 核心检查：同一个页面，把三份「顺序」分别导出，看是否指向同一个故事。
- **7 · 格式塔 12 条组织律全表（IxDF 逐条核对）** `L155` — 来源：Interaction Design Foundation《The Gestalt Principles》（页面标注 updated 2026）。原文："Gestalt" is German for "unified whole"；由
- **8 · 组织律里可验收的四个部分** `L180` — 格式塔常被讲成"看图说话"，但其中四条能落成可检查的构型规则。以下比值是本知识库的工程约定（便于评审时有一致口径），不是实验测得的感知常数，不要当研究结论引用。
- **9 · 前注意属性：为什么"单特征差异"才会 pop-out** `L201` — 来源：Wikipedia《Feature integration theory》，Anne Treisman 与 Garry Gelade 1980，原始论文 "A feature-integration theory of attenti
- **10 · 图形/背景与多稳态：不要做歧义层级** `L221` — IxDF 把 Figure/Ground 与 Multistability 分列，并明确指出二者常被混淆："In most cases, background and foreground are stable, but in some c
- **11 · 裁决三：认知负荷分三类，7±2 不是菜单上限** `L231` — 来源：Laws of UX《Cognitive Load》与《Miller's Law》逐字页 + Wikipedia《Cognitiveload》。
- **12 · Hick–Hyman Law：决策时间的公式与失效条件** `L251` — 定义（Laws of UX 逐字）："The time it takes to make a decision increases with the number and complexity of choices." 起源：William
- **13 · Fitts's Law：目标尺寸与距离的三种写法** `L273` — 定义（Laws of UX 逐字）："The time to acquire a target is a function of the distance to and size of the target." 起源：Paul Fitts 
- **14 · 工作记忆、chunking 与渐进披露** `L295` — - 工作记忆（Laws of UX 逐字）："A cognitive system that temporarily holds and manipulates information needed to complete tasks."；
- **15 · 序列位置效应与 Von Restorff：位置与差异如何改变记忆** `L304` — 来源：Wikipedia《Serialpositioneffect》《VonRestorffeffect》+ Laws of UX 同名条目。
- **16 · Laws of UX 中注意力/负荷相关的 12 条速查** `L316` — 站点首页共列 31 条。以下 12 条与 L2/L3 直接相关，定义均为首页逐字，未做二次演绎；未在本轮逐页核验的条目只收录首页那一句定义，不补造出处与年份。
- **17 · 从内容到视觉的六步构建流程** `L339` — 顺序不可颠倒——多数"层级乱"是跳过了前 3 步直接做第 4 步。
- **18 · 三关度量与验收** `L354` — 不生产玄学评分，只做三道可复现的检查；任何一道不过，回到 §2 对应层修。
- **19 · 与既有资产的边界矩阵** `L368` — ---
- **20 · 场景速查（12）** `L384` — ---
- **21 · 反模式（20）** `L403` — 1. 把 F 型当版式模板主动"设计"，而不是当作缺引导的诊断信号。
- **22 · 自检（20）** `L428` — 1. 说过"F 型是默认扫描而非设计目标"，并能引用 NN/g 那句 default pattern 原文？
- **23 · 可抄代码（5 段，3 段 Python 已实跑）** `L453` — 只用于方案 A/B 的相对比较；a、b 是占位常数，真实秒数需实测标定。
  - **23.1 Python · Hick / Fitts 相对成本计算器（实跑 PASS）** `L455` — 只用于方案 A/B 的相对比较；a、b 是占位常数，真实秒数需实测标定。
  - **23.2 Python · 三顺序静态扫描器（实跑 PASS）** `L494` — 对一段 HTML 检查标题跳级、正 tabindex、CSS order / row-reverse / position: absolute 造成的视觉顺序搬移，输出可直接贴进评审记录。
  - **23.3 Python · 邻近性间距比校验器（实跑 PASS）** `L565` — 1.5 是 §8 声明的工程约定，改成一个常量便于团队按自己设计系统调整，不伪装成感知实验结论。
  - **23.4 CSS · 层级信号 token（不靠"一路放大加粗"）** `L590`
  - **23.5 HTML · C27 正例与 F1 反例对照** `L620` — ---
- **24 · 取源与限制（公开记录）** `L647` — 本轮深蒸馏的官方/权威原文（逐字引用均已在前文标注出处）：

### `references/visual-style-taxonomy.md` · 视觉风格谱系与设计运动（Visual Style Taxonomy）
_317 行 · 快照 2026-11-07 · 40 节_

- **0. 什么时候读这份文件** `L7` — - 用户说"做成 Linear / Vercel / 某站那种感觉""这个风格叫什么""帮我定个视觉调性""想要高级感 / 复古感 / 科技感 / 温暖感"。
- **1. 为什么需要风格谱系（核心立场）** `L15` — 1. "高级感""复古感"是结果不是方法。 追问一句：它具体是哪几组信号？说不出信号的形容词，不能作为设计指令。
- **2. 风格识别四维信号（拆任何风格都用这四把尺）** `L24` — 拿到一个参考图 / 一个站点 / 一个形容词，逐维标注，不要整体感受。四把尺：
  - **2.1 Typography（字）** `L28` — - 字族：衬线（权威 / 传统 / 编辑）· 无衬线（中性 / 现代 / 科技）· 等宽（技术 / 复古终端 / 代码感）。
  - **2.2 Color（色）** `L34` — - 色相范围：单色相（克制，如 Vercel 近黑白）· 撞色（张扬，如 Neo-brutalism）· 全谱（玩趣，如 Memphis）。
  - **2.3 Shape & Material（形与材质）** `L40` — - 圆角档：0（硬 / 工业 / 原始）· 4（微圆 / 严谨）· 8（中性）· 16（友好）· 全圆（亲和 / 可爱）。一次只主导一档。
  - **2.4 Motion & Space（动效与空间）** `L46` — - 动效密度：静态（极简 / 编辑）· 克制（轻 hover / 淡入，现代 SaaS）· 活泼（弹性 / 交错，年轻产品）。
- **3. 主流动派谱系（编年 + 视觉签名 + 何时用 / 不用 + 代表）** `L55` — 每条给：起源年份与关键人物、四维签名、代表、何时用、何时不用。年份与人物以权威史料为准（Swiss 1950s / Müller-Brockmann；Bauhaus 1919 / Gropius；Memphis 1981 / Sottsas
  - **3.1 Swiss / International Typographic Style（瑞士国际主义，1950s）** `L61` — - 签名：数学网格、无衬线（Helvetica / Akzidenz-Grotesk）、不对称构图、左对齐、大字号标题、摄影替代插画、留白即结构。
  - **3.2 Bauhaus（1919–1933，Walter Gropius）** `L66` — - 签名：几何基本形（圆 / 方 / 三角）、三原色 + 黑白、无衬线、形式跟随功能、红黄蓝撞色。
  - **3.3 Brutalism（网页野兽派，2014+）** `L70` — - 签名：近乎原始 HTML、系统默认字体、高对比单色、无圆角无阴影、露出结构、故意"未抛光"。
  - **3.3b Neo-brutalism（新野兽派，2020+）** `L74` — - 签名：硬黑描边（2–3px）、硬投影（offset 实色块）、高饱和撞色、故意粗糙、大圆角但硬边。
  - **3.4 Memphis（1981，Ettore Sottsass）** `L78` — - 签名：几何碎形、撞色块、黑白条纹 / 波点图案、玩趣、无统一网格。
  - **3.5 Skeuomorphism（拟物，2007–2013，iOS 6 峰值）** `L82` — - 签名：材质仿真、高光、内阴影、真实纹理（皮革 / 木纹）、强投影。
  - **3.6 Flat Design（扁平，2013+，iOS 7 / Windows 8 Metro 引爆）** `L86` — - 签名：纯色块、无阴影无渐变、简单几何图标、二维。
  - **3.7 Material Design（2014，Google）** `L90` — - 签名：8dp 栅格、elevation（z 轴阴影分层）、涟漪反馈、浮动按钮、系统化的动效曲线（见 motion-system.md）。
  - **3.8 Neumorphism / Soft UI（新拟态，2019–2020，Plyuto 引爆 / Kelley 造词 / Malewicz 定型）** `L94` — - 签名：同源双色背景 + 单光源一对方向相反的内阴影，大圆角，元素像"从背景浮起 / 按下去"。可访问性 / 表单红线：低对比违背非文本 3:1，绝不做主操作按钮或表单输入。
  - **3.9 Glassmorphism（玻璃拟态，2020+，Malewicz 命名）** `L98` — - 签名：半透明表面 + 背景模糊（backdrop-filter）+ 1px 高光描边 + 轻投影 + 饱和背景图。可访问性 / 对比度红线：文字 ≥4.5:1、正文密集区禁用、低端机须测 backdrop-filter 成本（详见本节）
  - **3.10 Minimalism（极简，长青）** `L102` — - 签名：极致留白（40–60%）、极少元素、无装饰、单一强调色、克制的字重。
  - **3.11 Maximalism（极繁，周期）** `L106` — - 签名：满版、撞色层叠、多字体混排、强图案。
  - **3.12 Y2K / Frutiger Aero（2004–2013，近年回流）** `L110` — - 签名：气泡、高光水珠、玻璃质感、天空蓝 + 银白、圆润、乐观未来感；Frutiger Aero 是"玻璃 + 自然 + 气泡"子型。
  - **3.13 Vaporwave / Retro-futurism（2010s，亚文化）** `L114` — - 签名：粉紫青渐变、网格地平线、故障（glitch）、罗马雕塑 / 日文假名、复古 3D。
  - **3.14 Cyberpunk / Dark tech（暗色科技）** `L118` — - 签名：暗底、霓虹（青 / 品红 / 绿）、扫描线、等宽字体、发光描边。
  - **3.15 Bento grid（便当盒栅格，2022+，Apple / Linear 推动）** `L122` — - 签名：圆角卡片网格、内容块化、每格一信息、留白内嵌。
  - **3.16 Claymorphism（黏土拟态，2022+）** `L126` — - 签名：圆润如充气、双软阴影（内暗外亮）、高光点、糖果色。
  - **3.17 Corporate / Enterprise（企业中性，长青基线）** `L130` — - 签名：中性蓝 / 灰、规整栅格、低饱和、信息密集但有序、弱投影。
- **4. 风格匹配决策（给定"A 感觉"，怎么拆成信号）** `L136` — 四步：截三屏（首屏 / 列表 / 详情）→ 逐维标注（按 §2 四维表填，而不是"好看"）→ 抽公共信号（多个参考的交集才是真需求）→ 落成 token（圆角档 / 阴影档 / 色板基调 / 字号阶 / 字重对比 / 间距基调 / 动效密度
  - **4.1 用户给参考图 / 站点（最常见、最可靠）** `L138` — 四步：截三屏（首屏 / 列表 / 详情）→ 逐维标注（按 §2 四维表填，而不是"好看"）→ 抽公共信号（多个参考的交集才是真需求）→ 落成 token（圆角档 / 阴影档 / 色板基调 / 字号阶 / 字重对比 / 间距基调 / 动效密度
  - **4.2 用户给形容词（"高级 / 复古 / 科技 / 温暖"）** `L141` — 把词翻成信号，避免空转：
  - **4.3 风格 vs 品牌（不替个性）** `L150` — 先用 brand-identity.md §3 定三词定位与反义词；风格只是"把个性翻译成视觉语言"的若干候选之一。若风格与个性冲突（如"温暖亲子"却套"硬黑边野兽派"），回退到个性，风格让步。
  - **4.4 与第 4 步 L2 衔接** `L153` — design-md-format.md §3 品牌 DNA 是长期资产；本文件是竞品 / 潮流风格的速配。匹配顺序：先 DNA（长期）→ 再本文件（临时 / 参考）。
- **5. 混搭的纪律（什么能混、什么冲突）** `L158` — 1. 安全混搭：材质层（轻投影 / 玻璃）可叠任意色系；栅格严格度独立于色系；圆角档与色系独立。
- **6. 趋势生命周期（何时该上、何时已过）** `L168` — 1. 趋势曲线：引爆（Dribbble / Beh开发者奖）→ 主流采纳 → 过载（一键模板化）→ 反噬（回到克制）。纯视觉潮流通常 12–24 个月走完前两段。
- **7. 中文 / 出海场景的风格注意** `L178` — 1. 中文界面：中文笔画密度远高于拉丁字母，极简留白要更克制（别为了"高级"把中文压到 12px）；字重与字距调整见 chinese-design.md（禁伪粗 / 伪斜、行高 ≥1.6）。衬线中文（宋体类）在屏幕小字号下易发虚，屏幕优先用
- **8. 把风格转成 token（与 design-tokens.md 对接）** `L186` — 1. 风格 → token 映射表（一次只定一套）：
- **9. 12 场景速查** `L204` — 1. 用户说"做成 Linear 那种感觉" → §4.1 拆：暗色可选 / 克制无衬线 / 轻投影 / Bento 卡片 / 极克制动效。
- **10. 20 反模式** `L221` — 1. 直接把"极简 / 高级 / 科技感"当设计指令，不拆信号。
- **11. 20 自检（交付前逐条过）** `L246` — 1. 用户的需求（参考图 / 形容词）被拆成了 §2 四维信号，不是停在"感觉"？
- **12. 可抄代码 / 清单** `L271` — 风格速查卡（标注参考站用）：
- **13. 取源与权威边界** `L310` — - 权威史料与立场：Interaction Design Foundation（Design History：Bauhaus 1919–1933 / De Stijl 1917–1931 / Swiss style / Skeuomorph

### `memory/design-log.md` · 设计记忆（自我成长档案）
_688 行 · 快照 — · 38 节_

- **当前画像（规则层，命中 ≥2 次的稳定偏好）** `L6` — （暂无——随使用积累）
- **匹配与反馈日志（追加层，只增不改）** `L11`
- **YYYY-MM-DD · 需求一句话** `L14` — - 需求：载体/调性/明暗
- **2026-10-28 · 开发者工具深色落地页（自测）** `L21` — - 需求：落地页 / 深色 / 开发者工具；调性默认 极简+专业+冷静
- **2026-10-29 · 元素级精准匹配升级（v3）** `L27` — - 需求：导航栏等元素提示词应返回设计图本体而非设计网站链接
- **2026-10-29 · v4 系统化与中文场景补齐（每日升级 #1）** `L33` — - 需求：每日深蒸馏 Design-related websites.txt + 补充设计站/GitHub 仓库，产出知识路线与资料，自动推 GitHub 并更新 README
- **2026-10-30 · 动效系统 + 记忆树与检索（每日升级 #2）** `L46` — - 需求：每日深蒸馏（本轮按用户补充要求：记忆树、快捷搜索查询、自我进化、自动推送）
- **2026-10-31 · 数据可视化规范（每日升级 #3）** `L61` — - 需求：每日深蒸馏（记忆树 / 快捷检索 / 自我进化 / 自动推送 + 更新 README）
- **2026-10-31 · 表单与表格规范（每日升级 #4）** `L79` — - 需求：每日深蒸馏（记忆树 / 快捷检索 / 自我进化 / 自动推送 + 更新 README）
- **2026-11-01 · 可访问性实操（每日升级 #5）** `L98` — - 需求：每日深蒸馏（记忆树 / 快捷检索 / 自我进化 / 全局安装 / 自动推送 + 更新 README）
- **2026-11-01 · 反馈与状态设计 + 检索层别名映射（每日升级 #6）** `L123` — - 需求：每日深蒸馏（记忆树 / 快捷检索 / 别名映射 / 自我进化 / 全局安装 / 自动推送 + 更新 README）
- **2026-11-01 · 响应式与断点体系（每日升级 #7）** `L147` — - 需求：每日深蒸馏 + 自我进化；本轮取上一轮候选第 1 位（响应式与断点），原知识仅 design-md-format.md 两行"要写断点值"与一句"能响应式"
- **2026-11-01 · 版式与网格（每日升级 #8）** `L169` — - 需求：每日深蒸馏 + 自我进化；本轮取上一轮候选第 1 位（版式与网格/Editorial），原知识仅有 design-md-format.md 两行"要写断点值"与一句"版式要克制"
- **2026-11-01 · 品牌视觉与 Logo 逻辑（每日升级 #9）** `L205` — - 主题：品牌视觉与 Logo 逻辑（上轮候选第 1 位；原知识仅 design-md-format.md 的 54 品牌 DNA 速查，缺"从零定一套视觉识别"的方法、几何规则、色阶生成算法）
- **2026-11-01 · 暗色模式体系（每日升级 #10）** `L243` — 补记：本轮当时只写入了自动化 memory，遗漏 design-log，此处按原始记录补入（不改动既有内容）。
- **2026-11-01 · 性能与设计的关系（每日升级 #11）** `L261` — - 主题：性能与设计的关系（上轮候选第 1 位；原知识仅 knowledge-map.md L3 一句"CWV 三阈值"）
- **2026-11-01 · 设计交付与协作（每日升级 #12）** `L296` — - 主题：设计交付与协作（上轮候选第 1 位；原知识里"走查"零命中、"设计交付"只有 8 条散落在 editorial/accessibility/design-md 的边角）
- **2026-11-05 · 内容设计与 UX 文案体系（每日升级 #13）** `L330` — - 主题：内容设计与 UX 文案（上轮候选第 2 位；候选第 1 位「多品牌/多主题 token 架构」已在 #12 前完成，multi-brand-theming.md 已存在；原知识只有 form-table.md 的 12 条错误模板
- **2026-11-05 · 演示文稿与幻灯片版式（每日升级 #14）** `L358` — - 需求：每日深蒸馏设计知识，本轮主题为演示文稿与幻灯片版式（上轮候选第 1 位）
- **2026-11-05 · 动效进阶：编排、状态机与共享元素转场（每日升级 #15）** `L372` — - 需求：每日深蒸馏设计知识，本轮主题取上轮候选第 1 位「动效进阶（编排与状态机）」——motion-system.md 只覆盖单动效的曲线与时长，多元素编排、列表增删、共享元素转场、动画状态机与中断策略完全空白
- **2026-11-05 · 国际化与本地化设计：i18n / L10n / RTL（每日升级 #16）** `L395` — - 需求：每日深蒸馏设计知识，本轮主题取上轮候选第 1 位「国际化与本地化设计」。先用 dpsearch.py "国际化 本地化 RTL 多语言" 与 grep 确认缺口：现有知识几乎只在 ux-writing.md §13 的 24 行文
- **2026-11-05 · 设计系统文档写作：组件文档页 / 信息架构 / 版本化 / 治理（每日升级 #17）** `L413` — - 需求：每日深蒸馏设计知识，本轮主题取 #16 候选第 1 位「设计系统文档写作」。缺口判定：dpsearch.py "设计系统文档 文档信息架构 组件文档 版本化" + grep → 文档站点 / 组件文档 / 版本化 / 贡献指南 /
- **2026-11-06 · AI / 生成式设计工具链：工作流、提示词、质量验收与合规边界（每日升级 #18）** `L439` — - 需求：延续每日升级协议，第 18 轮只深挖一个主题。候选来自 #17 待挖项；dpsearch.py "AI 生成 设计 提示词 版权 内容标识" 的 8 条命中全落在 ux-writing / knowledge-map / desi
- **2026-11-06 · 设计伦理与包容性：欺骗性设计、隐私同意 UI、成瘾机制与认知无障碍（每日升级 #19）** `L457` — - 需求：延续每日升级协议，第 19 轮只深挖一个主题。dpsearch.py "设计伦理 dark patterns 成瘾设计 隐私 UI 包容性设计 诱导 默认勾选 一键关闭 取消订阅" 命中 8 条但最高只落在 knowledge-m
- **2026-11-07 · 组件 API 设计与组合模式：状态所有权、渲染所有权、契约可演进（每日升级 #20）** `L478` — - 需求：延续每日升级协议，第 20 轮只深挖一个主题。缺口判定用 dpsearch.py "组件 API 设计 组合模式 props 语义 受控 非受控" 与 dpsearch.py "组合 配置 compound component 插
- **2026-11-07 · 设计度量与用户研究：可用性指标、研究方法与统计验收（每日升级 #21）** `L502` — - 需求：延续每日升级协议，第 21 轮只深挖一个主题。缺口判定用 dpsearch.py "设计度量 用户研究 SUS 样本量 A/B 测试 可用性测试 任务成功率 HEART" 与 dpsearch.py "HEART 框架 问卷设计 
- **2026-11-07 · 图标设计系统（Iconography，每日升级 #22）** `L524` — - 需求：延续每日升级协议，第 22 轮只深挖一个主题。缺口判定用 dpsearch.py "图标设计 图标系统 图标网格 图标可访问性 图标字体 spinner" 与 grep -ric "图标网格\keyline\aria-hidden
- **2026-11-07 · 导航与信息架构（Navigation & IA，每日升级 #23）** `L538` — - 需求：延续每日升级协议，第 23 轮只深挖一个主题。缺口判定用 dpsearch.py "导航 导航栏 菜单 面包屑 tabs 信息架构 汉堡 skip link" 与 grep -ric "导航栏\面包屑\skip link\aria
- **2026-11-07 · 设计评审与反馈（Design Critique & Feedback，每日升级 #24）** `L551` — - 需求：延续每日升级协议，第 24 轮只深挖一个主题。缺口判定用 dpsearch.py "评审 critique 反馈 设计走查" 与 grep -ric "评审\critique\反馈"：命中分散在 handoff-collabora
- **2026-11-07 · 每日升级 #25：色彩科学（Color Science）** `L564` — - 升级：新增 references/color-science.md（22 节 / ~620 行）；SKILL.md 接线（资产表 + 意图路由 + 第5步色彩指针 + 第6步色彩科学关 #33）+ v29 基线；buildreadme 
- **2026-11-07 · 每日升级 #26：视觉风格谱系与设计运动（Visual Style Taxonomy）** `L571` — - 本轮性质：续跑 + 收口。定时触发时发现上一轮（#26 / v29→v30）已完成「蒸馏 + 4 处接线」但未收口：references/visual-style-taxonomy.md（312 行 / 13 节）为 untracked
- **2026-11-07 · 每日升级 #27：字体排印系统（Typography System）** `L589` — - 本轮性质：v30→v31 新增基础支柱域。触发时基线干净（HEAD 5246fb3，v30 / 36 参考 / 175 路由 / 34 自检 / 188 别名 / 24 支线 / 132 自测），候选清单首位是「docs-as-code
- **2026-11-08 · 每日升级 #28：形状与深度系统（Shape & Elevation）** `L604` — - 本轮性质：v31→v32 补齐第三根基础支柱域。触发时基线干净（HEAD 945572f、v31 / 37 参考 / 850,837 字符 / 180 路由 / 35 自检 / 198 别名 / 25 支线 / 136 自测）。用 dp
- **2026-11-08 · 每日升级 #29：视觉层级与格式塔组织律 / 注意力与认知负荷（Visual Hierarchy & Gestalt）** `L619` — - 本轮性质：v32→v33 补齐第四根基础支柱域。触发时基线干净（HEAD 005226f、v32 / 38 参考 / 890,649 字符 / 185 路由 / 36 自检 / 204 别名组 / 26 支线 / 140 自测 / 17
- **2026-11-09 · 每日升级 #30：内容可发现性与可扫读性（Content Findability / Search UX / Scannability）** `L633` — - 本轮性质：v33→v34 补齐「内容链路」域，并按 #26 判例先交付在途轮次。触发时工作区不是干净基线：HEAD 740f27e（v33 / 39 参考 / 935,332 字符 / 190 路由 / 37 自检 / 212 别名组 
- **2026-11-10 · 每日升级 #31：直接操纵与指针交互（Direct Manipulation / Pointer, Gesture & Drag-and-Drop）** `L647` — - 本轮性质：v34→v35 补齐「交互执行端」域。触发时工作区是干净基线：HEAD cddf02b（v34 / 40 参考 / 1,004,258 字符 / 195 路由 / 38 自检 / 218 别名组 / 28 支线 · 148 自
- **2026-11-11 · 每日升级 #32：对话式与生成式界面（Conversational & Generative UI / AI 产品交互）** `L661` — - 本轮性质：v35→v36 补齐「AI 产品交互链路」域。触发时工作区是干净基线：HEAD 77c2f40（v35 / 41 参考 / 1,072,753 字符 / 200 路由 / 39 自检 / 224 别名组 / 29 支线 · 1
- **2026-11-11 · 每日升级 #33：叠加层与模态性（Overlays & Modality / Dialog / Popover / Top Layer）** `L675` — - 本轮性质：v36→v37 补齐「层的交互契约」域，并按 #26 判例先交付在途轮次。触发时工作区不是干净基线：HEAD 7d3bdbc（v36 / 42 参考 / 1,114,212 字符 / 205 路由 / 40 自检 / 230 

## 三、主题索引（章节标题 → 位置）

- **0. 30 秒速查** → `references/form-table.md` L8
- **0. 一句话立场** → `references/iconography.md` L6 · `references/navigation-ia.md` L6 · `references/overlays-modality.md` L10
- **0. 一句话立场与三条裁决** → `references/conversational-generative-ui.md` L10
- **0. 与既有资产的分层（先判该读哪份）** → `references/ai-design-toolchain.md` L9 · `references/component-api-design.md` L9 · `references/design-ethics-inclusion.md` L9 · `references/design-measurement-research.md` L9
- **0. 与既有资产的分层（先判读哪一份，别读错）** → `references/design-system-docs.md` L7
- **0. 什么时候读这份文件** → `references/visual-style-taxonomy.md` L7
- **0. 先分清：本文件补什么** → `references/design-critique.md` L10
- **0. 先定策略，再谈数值** → `references/responsive-layout.md` L8
- **0. 四条总原则（AntV 官方，可直接引用）** → `references/dataviz.md` L8
- **1 · 为什么单列「内容可发现性」** → `references/content-findability.md` L19
- **1 · 为什么单列「直接操纵与指针交互」** → `references/direct-manipulation.md` L19
- **1 · 为什么单列字体排印系统** → `references/typography-system.md` L11
- **1 · 为什么单列形状与深度系统** → `references/shape-elevation.md` L17
- **1 · 为什么单列色彩科学** → `references/color-science.md` L9
- **1 · 为什么单列视觉层级与格式塔** → `references/visual-hierarchy-gestalt.md` L19
- **1. 一页速查：交付链的六个关卡** → `references/handoff-collaboration.md` L9
- **1. 一页速查：品牌视觉从零到交付** → `references/brand-identity.md` L8
- **1. 三条不可商量的原则（先给立场，不和稀泥）** → `references/design-ethics-inclusion.md` L27
- **1. 两种评审，别混在一场会** → `references/design-critique.md` L23
- **1. 为什么性能是设计约束：加载速度就是设计决策** → `references/performance-design.md` L13
- **1. 为什么这是结构性空白（缺口实测）** → `references/conversational-generative-ui.md` L24
- **1. 为什么需要风格谱系（核心立场）** → `references/visual-style-taxonomy.md` L15
- **1. 何时用图标 / 文字 / 两者（决策树）** → `references/iconography.md` L12
- **1. 先决定：该不该做暗色（含反面证据）** → `references/dark-mode.md` L13
- **1. 先判关系，再选图形（FT Visual Vocabulary 九类）** → `references/dataviz.md` L21
- **1. 先给立场：度量三步法 + 三层判层** → `references/design-measurement-research.md` L23
- **1. 决策三问：先判该不该动** → `references/motion-system.md` L10
- **1. 分工与决策树：单动效、编排、状态机三层** → `references/motion-orchestration.md` L11
- **1. 判层：AI 在设计流程的五个位置，以及哪些活不该交出去** → `references/ai-design-toolchain.md` L25
- **1. 判层：先分清你要写的是哪一种设计系统文档（Diátaxis 四象限）** → `references/design-system-docs.md` L20
- **1. 四问判型决策树：inert / 焦点 / 触发 / 退出** → `references/overlays-modality.md` L18
- **1. 导航的四类职责（先分清楚再用形态）** → `references/navigation-ia.md` L12
- **1. 尺寸与比例** → `references/presentation-design.md` L33
- **1. 组件 API 设计：三份所有权与三条不可商量的原则（先给立场，不和稀泥）** → `references/component-api-design.md` L25
- **1. 表单（Form）的五个零件：标签·控件·帮助·错误·动作** → `references/form-table.md` L39
- **1. 视口断点 vs 容器断点：先选对工具** → `references/responsive-layout.md` L22
- **10 · MDN PointerEvent 工程契约：设备、事件、捕获、取消** → `references/direct-manipulation.md` L207
- **10 · 图形/背景与多稳态：不要做歧义层级** → `references/visual-hierarchy-gestalt.md` L221
- **10 · 数字特性与 tabular-nums（表格 / 时钟 / 频繁变化数值）** → `references/typography-system.md` L139
- **10 · 色彩无障碍 beyond 1.4.11** → `references/color-science.md` L194
- **10 · 裁决三：圆角是几何契约，不是装饰常数** → `references/shape-elevation.md` L259
- **10 · 裁决二：链接目的的 WCAG 契约族（五条准则）** → `references/content-findability.md` L198
- **10. 20 反模式** → `references/visual-style-taxonomy.md` L221
- **10. AI 功能界面：微软人机交互 18 条准则（HAX G1–G18）** → `references/ai-design-toolchain.md` L300
- **10. Hybrid UI 混合界面与 RICH 范式（WIMP 不是唯一解）** → `references/conversational-generative-ui.md` L282
- **10. 中断与取消：可中断性的工程定义** → `references/motion-orchestration.md` L509
- **10. 反模式清单（逐条给改法）** → `references/dataviz.md` L289
- **10. 可用性测试：moderated / unmoderated 与出声思考** → `references/design-measurement-research.md` L194
- **10. 可访问性（Accessibility）⚠️ 高频翻车点** → `references/iconography.md` L140
- **10. 品牌色双主题：M3 官方 tone 映射表（亮色/暗色精确值，可直接抄进 token）** → `references/brand-identity.md` L300
- **10. 布局梯度：按内容量选，不按审美选** → `references/form-table.md` L259
- **10. 搜索与导航协同** → `references/navigation-ia.md` L120
- **10. 文档版本化（Docusaurus 3.10.2 官方规则 + SemVer 对接）** → `references/design-system-docs.md` L360
- **10. 暗色专属的无障碍陷阱** → `references/dark-mode.md` L436
- **10. 浮层遮挡裁决：2.4.11 的四类官方判词、两条例外、通过手段与 F110** → `references/overlays-modality.md` L290
- **10. 组件契约的最小字段集（API surface，可直接当评审表）** → `references/component-api-design.md` L353
- **10. 自检 20 项（评审前 / 中 / 后）** → `references/design-critique.md` L184
- **10. 表单在窄屏** → `references/responsive-layout.md` L442
- **10. 视觉手法的性能价格表（本轮核心）** → `references/performance-design.md` L431
- **10. 设计走查（design QA）：三遍法 + 9 字段文档** → `references/handoff-collaboration.md` L359
- **10. 远程与线上演示** → `references/presentation-design.md` L481
- **10. 验收清单（10 条，交付前逐条过）** → `references/motion-system.md` L298
- **10. 默认勾选、概括授权、搭售与商业信息：同份规章的另外三条** → `references/design-ethics-inclusion.md` L261
- **11 · Corner overlap：半径按比例缩减的规范公式** → `references/shape-elevation.md` L275
- **11 · touch-action 全值表、形式语法与三条工程陷阱** → `references/direct-manipulation.md` L233
- **11 · 可扫读性：79% / 16% 与 124% 的原文口径** → `references/content-findability.md` L220
- **11 · 工程实现（落地要点）** → `references/color-science.md` L204
- **11 · 裁决三：认知负荷分三类，7±2 不是菜单上限** → `references/visual-hierarchy-gestalt.md` L231
- **11 · 高位属性优先，低位 API 兜底** → `references/typography-system.md` L163
- **11. 20 自检（交付前逐条过）** → `references/visual-style-taxonomy.md` L246
- **11. AI 味验收：AI Slop Test 与 8 维 DO/DON'T** → `references/ai-design-toolchain.md` L350
- **11. Changelog：Keep a Changelog 1.1.0 的七条指导原则与六类变更** → `references/design-system-docs.md` L404
- **11. SC 2.1.2 No Keyboard Trap：焦点循环允许的前提是「退出可知、可达」** → `references/overlays-modality.md` L329
- **11. WAAPI 精确参数表（KeyframeEffect / Element.animate）** → `references/motion-orchestration.md` L561
- **11. 中文演示场景** → `references/presentation-design.md` L512
- **11. 动画（Animation）** → `references/iconography.md` L157
- **11. 卡片分类与树测试（信息架构验证，最被低估的两招）** → `references/design-measurement-research.md` L211
- **11. 反模式 20 条** → `references/navigation-ia.md` L130
- **11. 反模式（命中即扣分）** → `references/motion-system.md` L313
- **11. 可抄模板（4 段）** → `references/design-critique.md` L214
- **11. 品牌色的边界：图表 / 大屏 / 印刷 / 多品牌** → `references/brand-identity.md` L342
- **11. 回调契约：onChange 到底承诺了什么** → `references/component-api-design.md` L384
- **11. 场景速查（12 个高频问题 → 直接答案）** → `references/dark-mode.md` L451
- **11. 实现选型（GitHub API 实测 2026-10-31）** → `references/dataviz.md` L325
- **11. 导航降级：一条标准路径** → `references/responsive-layout.md` L458
- **11. 未成年人防沉迷：国务院令第 766 号第 42–45 条逐条落成设计动作** → `references/design-ethics-inclusion.md` L276
- **11. 渲染性能：帧预算与图层内存（可算的数）** → `references/performance-design.md` L465
- **11. 缺陷分级与发布门禁** → `references/handoff-collaboration.md` L423
- **11. 表单可访问性：可执行清单** → `references/form-table.md` L294
- **11. 裁决三：AI 答错了要高效纠错（HAX G9）——四档恢复链，不是重新生成按钮** → `references/conversational-generative-ui.md` L302
- **12 · HTML Drag and Drop API：七事件、DataTransfer 与 drop target 规则** → `references/direct-manipulation.md` L267
- **12 · Hick–Hyman Law：决策时间的公式与失效条件** → `references/visual-hierarchy-gestalt.md` L251
- **12 · font-family 逐字符回退算法（加载 / 缺字 / 验收）** → `references/typography-system.md` L174
- **12 · nano-content：前 11 个字符决定要不要读下去** → `references/content-findability.md` L245
- **12 · 场景速查（12）** → `references/color-science.md` L234
- **12 · 嵌套同心圆角 r = R − p 与失效条件** → `references/shape-elevation.md` L303
- **12. AI 生成界面的 12 类固有缺陷 → 接回既有专项** → `references/ai-design-toolchain.md` L386
- **12. CSS 入场/退场状态机：@starting-style 四件套** → `references/motion-orchestration.md` L585
- **12. SC 3.2.1 On Focus：focus 不得触发 change of context，hover 触发也不等于可以抢焦点** → `references/overlays-modality.md` L349
- **12. stop / regenerate / setMessages 与状态边界播报一次（含清空队列）** → `references/conversational-generative-ui.md` L337
- **12. 上线自检（22 项，逐条打勾）** → `references/dark-mode.md` L470
- **12. 中后台适配（中文场景专用）** → `references/responsive-layout.md` L473
- **12. 可抄代码 / 清单** → `references/visual-style-taxonomy.md` L271
- **12. 命名与交付清单（Naming & Delivery Checklist）** → `references/iconography.md` L167
- **12. 字体系统：品牌字体与系统栈** → `references/brand-identity.md` L374
- **12. 成瘾设计：机制清单与「可关闭」红线** → `references/design-ethics-inclusion.md` L294
- **12. 接线** → `references/design-critique.md` L255
- **12. 无障碍不是 props 的附属品：键盘契约在 API 层怎么落** → `references/component-api-design.md` L399
- **12. 版式构图法则** → `references/presentation-design.md` L550
- **12. 版本与变更管理** → `references/handoff-collaboration.md` L442
- **12. 素材与出处** → `references/motion-system.md` L326
- **12. 自检 12 项（图表交付前逐条过）** → `references/dataviz.md` L349
- **12. 自检 20 项** → `references/navigation-ia.md` L155
- **12. 表格结构：五层 + 行高密度** → `references/form-table.md` L309
- **12. 设计决策分级：什么时候可以"花"性能** → `references/performance-design.md` L521
- **12. 迁移文档：MAJOR 必带，且必须能被机器校验** → `references/design-system-docs.md` L461
- **12. 问卷与访谈设计：偏差规避（数据垃圾进、垃圾出）** → `references/design-measurement-research.md` L227
- **13 · Fitts's Law：目标尺寸与距离的三种写法** → `references/visual-hierarchy-gestalt.md` L273
- **13 · unicode-range 子集化与 CJK 分片（性能 / CLS / 验收）** → `references/typography-system.md` L186
- **13 · 「Learn More」的三种改法与信息气味的重合** → `references/content-findability.md` L272
- **13 · 七体系圆角 token 精确对照与 M3 Expressive 更新** → `references/shape-elevation.md` L329
- **13 · 反模式（20）** → `references/color-science.md` L251
- **13 · 键盘拖放契约：dnd-kit 的逐字键盘参数** → `references/direct-manipulation.md` L297
- **13. A/B 测试统计：显著≠值得上线** → `references/design-measurement-research.md` L244
- **13. AI 设计工具链五层地图与选型（GitHub REST API 实测 2026-11-06）** → `references/ai-design-toolchain.md` L407
- **13. Token 交付管线：从设计变量到代码** → `references/handoff-collaboration.md` L502
- **13. Token 文档自动生成：DTCG 2025.10 把 $description 明确定位成文档源** → `references/design-system-docs.md` L480
- **13. 关闭契约矩阵：closedby 三值与七条退出路径** → `references/overlays-modality.md` L367
- **13. 列设计：决定表格好不好用的 80%** → `references/form-table.md` L346
- **13. 反模式（20 条，看到就是错）** → `references/dark-mode.md` L510
- **13. 取源与权威边界** → `references/visual-style-taxonomy.md` L310
- **13. 可抄代码** → `references/navigation-ia.md` L180
- **13. 图形语言：图标网格三体系 + 插画五参数** → `references/brand-identity.md` L404
- **13. 库选型矩阵（Library Matrix · GitHub API 实测）** → `references/iconography.md` L179
- **13. 弱网与低端设备：降级不是可选功能** → `references/performance-design.md` L547
- **13. 欧盟 DSA 第 25 条与 FTC 2022：两套执法口径，别混成一句** → `references/design-ethics-inclusion.md` L319
- **13. 演示节奏与信息流** → `references/presentation-design.md` L590
- **13. 状态归位表：每个动作后哪些状态必须复位** → `references/conversational-generative-ui.md` L358
- **13. 状态暴露：别把 9 态做成 9 个布尔 props** → `references/component-api-design.md` L422
- **13. 素材与出处** → `references/dataviz.md` L366
- **13. 编排层编排的无障碍降级（WCAG 2.3.3 / 2.2.2 / prefers-reduced-motion）** → `references/motion-orchestration.md` L646
- **13. 触控与鼠标：两套输入不能共用一套假设** → `references/responsive-layout.md` L504
- **14 · corner-shape 与 squircle：实验特性，不进生产** → `references/shape-elevation.md` L358
- **14 · font-display 时间线与五档选择（性能 / CLS / 验收）** → `references/typography-system.md` L199
- **14 · 工作记忆、chunking 与渐进披露** → `references/visual-hierarchy-gestalt.md` L295
- **14 · 自检（20）** → `references/color-science.md` L276
- **14 · 裁决三：阅读等级的合规门槛是「九年学校教育」** → `references/content-findability.md` L288
- **14 · 读屏指令、live region 播报与中文 announcements** → `references/direct-manipulation.md` L326
- **14. API 版本化：组件特有的破坏性判级（改默认值 = MAJOR 的延伸）** → `references/component-api-design.md` L435
- **14. 与其他参考的接线** → `references/navigation-ia.md` L269
- **14. 与既有参考的接线（Wiring）** → `references/iconography.md` L200
- **14. 代码即文档：Storybook Autodocs / MDX / Doc Blocks 精确配置** → `references/design-system-docs.md` L538
- **14. 分析数据：事件、漏斗、留存、同期群** → `references/design-measurement-research.md` L270
- **14. 包容性设计地基：不是「无障碍的补充」，是另一种起点** → `references/design-ethics-inclusion.md` L354
- **14. 可抄代码（4 段）** → `references/dark-mode.md` L535
- **14. 品牌声音与文案语气（NN/g 四维）** → `references/brand-identity.md` L443
- **14. 回归防线：让"改 A 崩 B"在合并前被发现** → `references/handoff-collaboration.md` L580
- **14. 层叠与嵌套：一次一个、双栈、Escape 只关最后一层** → `references/overlays-modality.md` L395
- **14. 工具与框架** → `references/presentation-design.md` L631
- **14. 微信小程序：另一套物理规律** → `references/performance-design.md` L589
- **14. 性能：100ms 响应窗口、读写分离与快照开销** → `references/motion-orchestration.md` L680
- **14. 流式渲染工程：增量 Markdown、未闭合块、节流、自动滚动纪律** → `references/conversational-generative-ui.md` L378
- **14. 生成 → 代码：衔接层与三个陷阱** → `references/ai-design-toolchain.md` L442
- **14. 表格规模化：分页、固定、批量、空态** → `references/form-table.md` L389
- **14. 调试与验收** → `references/responsive-layout.md` L530
- **15 · signifier 与两类反馈：NN/g 的可发现性裁决** → `references/direct-manipulation.md` L373
- **15 · size-adjust / font-size-adjust 度量对齐（FOUT 不跳版）** → `references/typography-system.md` L220
- **15 · 三条可读性公式、精确系数与「不可换算」** → `references/content-findability.md` L310
- **15 · 可抄代码（6 段）** → `references/color-science.md` L301
- **15 · 序列位置效应与 Von Restorff：位置与差异如何改变记忆** → `references/visual-hierarchy-gestalt.md` L304
- **15 · 表面层级：不用阴影也能表达深度（Carbon 与暗色重排）** → `references/shape-elevation.md` L376
- **15. 12 场景速查** → `references/presentation-design.md` L672
- **15. 12 场景（Scenarios）** → `references/iconography.md` L213
- **15. Inclusive Design Principles 七原则（逐条 + 设计动作）** → `references/design-ethics-inclusion.md` L375
- **15. L1 输入与发送：Enter / Shift+Enter、禁用提交、队列、中文场景** → `references/conversational-generative-ui.md` L391
- **15. Prompt 版本化、eval 与 SemVer** → `references/ai-design-toolchain.md` L458
- **15. Storybook argTypes：把 API 契约变成机器可读、可在 CI 校验的东西** → `references/component-api-design.md` L458
- **15. 协作节奏：每次交接都要有可验收的产出** → `references/handoff-collaboration.md` L622
- **15. 参考来源** → `references/dark-mode.md` L642
- **15. 反模式 20 条** → `references/responsive-layout.md` L565
- **15. 度量与验收：看哪个数、在哪看** → `references/performance-design.md` L628
- **15. 组件族谱判型表（12 类；先判型再选实现）** → `references/overlays-modality.md` L405
- **15. 表格可访问性与中文细节** → `references/form-table.md` L429
- **15. 设计稿 ↔ 文档 ↔ 代码：Figma Code Connect 与命名一致性** → `references/design-system-docs.md` L599
- **15. 证据分级与混合方法（别把噪声当信号）** → `references/design-measurement-research.md` L281
- **15. 资产交付清单与文件格式** → `references/brand-identity.md` L469
- **15. 跨框架实现矩阵与选型决策** → `references/motion-orchestration.md` L709
- **16 · Laws of UX 中注意力/负荷相关的 12 条速查** → `references/visual-hierarchy-gestalt.md` L316
- **16 · 中文可读性：音节公式失效，改用可解释的代理指标** → `references/content-findability.md` L346
- **16 · 中文排版（W3C clreq 原文核验）** → `references/typography-system.md` L232
- **16 · 取源与限制（公开记录）** → `references/color-science.md` L392
- **16 · 材质与玻璃：Apple HIG Materials / Liquid Glass 的分层边界** → `references/shape-elevation.md` L392
- **16 · 触屏拖放的硬性前提：1cm×1cm、几毫秒、约 100ms** → `references/direct-manipulation.md` L393
- **16. 20 反模式（Anti-patterns）** → `references/iconography.md` L230
- **16. 20 条反模式** → `references/presentation-design.md` L691
- **16. W3C COGA 八个目标：认知无障碍的可验收问句** → `references/design-ethics-inclusion.md` L393
- **16. 不确定性与披露：把"可能错"设计出来** → `references/ai-design-toolchain.md` L472
- **16. 中文/本土交付现实** → `references/handoff-collaboration.md` L661
- **16. 反模式清单（20 条，逐条对照）** → `references/performance-design.md` L674
- **16. 反模式清单（逐条给改法）** → `references/form-table.md` L452
- **16. 品牌一致性的十条检查（交付前逐条过）** → `references/brand-identity.md` L506
- **16. 场景速查（16 条，直接取结论）** → `references/motion-orchestration.md` L738
- **16. 平台与设计系统口径（原文 vs 工程约定分列）** → `references/overlays-modality.md` L426
- **16. 来源、引用与置信度呈现（与 HAX 18 条的边界）** → `references/conversational-generative-ui.md` L405
- **16. 研究运营与研究库（Research Ops / Repository）** → `references/design-measurement-research.md` L298
- **16. 类型即文档：TypeScript 契约的四条底线** → `references/component-api-design.md` L490
- **16. 自检 15 项（有响应式要求时逐条过）** → `references/responsive-layout.md` L590
- **16. 贡献与治理：GOV.UK 的准入标准（含可量化阈值）** → `references/design-system-docs.md` L622
- **17 · M3 type scale 与 token 化（可复现，不抄二手数值表）** → `references/typography-system.md` L244
- **17 · 从内容到视觉的六步构建流程** → `references/visual-hierarchy-gestalt.md` L339
- **17 · 玻璃拟态的合成开销与降级顺序** → `references/shape-elevation.md` L410
- **17 · 简明语言：Plain Writing Act 与四份官方指南** → `references/content-findability.md` L365
- **17 · 阈值与时序决策表** → `references/direct-manipulation.md` L417
- **17. 12 个高频场景速查** → `references/conversational-generative-ui.md` L417
- **17. 12 场景决策速查** → `references/overlays-modality.md` L466
- **17. 16 场景决策矩阵（先查表，再动手）** → `references/component-api-design.md` L501
- **17. 18 项自检** → `references/presentation-design.md` L718
- **17. 20 自检（Self-checks）** → `references/iconography.md` L255
- **17. 交付自检（18 项，全过才算过关）** → `references/performance-design.md` L699
- **17. 交付自检（表单 10 + 表格 10）** → `references/form-table.md` L475
- **17. 反模式（20 条，命中即扣分）** → `references/motion-orchestration.md` L761
- **17. 可抄代码** → `references/responsive-layout.md` L610
- **17. 合规达 ≠ 包容：两套判据的正交关系** → `references/design-ethics-inclusion.md` L418
- **17. 商标与授权合规（不做这步，前面全白做）** → `references/brand-identity.md` L521
- **17. 工具矩阵（注明：本轮 star/许可未实测）** → `references/design-measurement-research.md` L308
- **17. 度量：交付质量的六个指标** → `references/handoff-collaboration.md` L710
- **17. 文档新鲜度与漂移：可测指标 + 本技能自身的防漂移机制（自举）** → `references/design-system-docs.md` L650
- **17. 隐私、输入与组织边界** → `references/ai-design-toolchain.md` L483
- **18 · L4 死胡同治理：零结果与 404** → `references/content-findability.md` L379
- **18 · z-index 语义刻度与 stacking context** → `references/shape-elevation.md` L426
- **18 · 三关度量与验收** → `references/visual-hierarchy-gestalt.md` L354
- **18 · 决策一图流** → `references/direct-manipulation.md` L439
- **18 · 字体授权（OFL 1.1）：能做与不能做** → `references/typography-system.md` L258
- **18. 12 场景速查** → `references/ai-design-toolchain.md` L493
- **18. 20 反模式（每条都给出违反的契约）** → `references/overlays-modality.md` L483
- **18. 20 条反模式（逐条可判 FAIL）** → `references/component-api-design.md` L524
- **18. 与其他资产的分工** → `references/responsive-layout.md` L696
- **18. 决策矩阵：什么场景套哪套** → `references/design-ethics-inclusion.md` L431
- **18. 出处** → `references/form-table.md` L503
- **18. 十二场景速查（设计系统文档写作）** → `references/design-system-docs.md` L684
- **18. 反模式 20 条** → `references/conversational-generative-ui.md` L436 · `references/handoff-collaboration.md` L730
- **18. 可抄代码** → `references/brand-identity.md` L557 · `references/performance-design.md` L731 · `references/presentation-design.md` L743
- **18. 可抄代码（Copy-paste）** → `references/iconography.md` L280
- **18. 场景决策矩阵（12 场景：凭问题选度量方案）** → `references/design-measurement-research.md` L327
- **18. 自检清单（20 条，动效编排交付前逐条过）** → `references/motion-orchestration.md` L786
- **19 · 与既有资产的边界矩阵** → `references/visual-hierarchy-gestalt.md` L368
- **19 · 多条路径与当前所在指示的落地清单** → `references/content-findability.md` L398
- **19 · 工具链与 GitHub API 实测数据（2026-11-07）** → `references/typography-system.md` L281
- **19 · 替代路径矩阵：四种输入各自满足哪条 SC** → `references/direct-manipulation.md` L472
- **19 · 深度语言三选一：阴影 / 表面色 / 材质** → `references/shape-elevation.md` L450
- **19. 20 条反模式** → `references/ai-design-toolchain.md` L512
- **19. 20 条反模式（研究者与设计师都容易犯）** → `references/design-measurement-research.md` L346
- **19. 20 项自检（交付前逐条给证据）** → `references/overlays-modality.md` L508
- **19. 22 项上线自检（组件 API 关）** → `references/component-api-design.md` L549
- **19. 二十条反模式（写了等于没写）** → `references/design-system-docs.md` L703
- **19. 反模式 20 条** → `references/brand-identity.md` L625
- **19. 反模式 20 条：反操纵红线与合规验收判据（每条都能判 FAIL）** → `references/design-ethics-inclusion.md` L450
- **19. 取源与验证（Sources & Verification）** → `references/iconography.md` L333
- **19. 可抄代码（8 段）** → `references/motion-orchestration.md` L811
- **19. 数据来源** → `references/performance-design.md` L827 · `references/responsive-layout.md` L711
- **19. 自检 20 项（交付前逐条打勾）** → `references/handoff-collaboration.md` L755
- **19. 自检 20 项（交付前逐条过）** → `references/conversational-generative-ui.md` L461
- **2 · 三层模型：先判层，再谈放大加粗** → `references/visual-hierarchy-gestalt.md` L31
- **2 · 五层模型：先判层，再谈审美** → `references/shape-elevation.md` L31
- **2 · 四层链路模型：先判哪一层断，再谈改文案** → `references/content-findability.md` L31
- **2 · 四段链路模型：先判哪一段断，再谈改动画** → `references/direct-manipulation.md` L31
- **2 · 排印决策的六层模型（先判层，再谈审美）** → `references/typography-system.md` L25
- **2 · 色彩模型谱系（先认坐标，再谈配色）** → `references/color-science.md` L21
- **2. 三条最重要裁决** → `references/overlays-modality.md` L40
- **2. 五段链路判层模型（L1 发得出 → L5 收得回）** → `references/conversational-generative-ui.md` L43
- **2. 交付的本质：交付决策，不是交付图** → `references/handoff-collaboration.md` L26
- **2. 六大体系断点精确值对照** → `references/responsive-layout.md` L55
- **2. 分类体系裁决：别再照抄旧教程的那一套（暗黑模式 / dark patterns 现行 18 类）** → `references/design-ethics-inclusion.md` L37
- **2. 动效缓动曲线（easing）：语义决定曲线，不是审美决定** → `references/motion-system.md` L30
- **2. 受控 / 非受控：唯一真相源（React 官方定义 + Radix 上游源码）** → `references/component-api-design.md` L42
- **2. 可用性的定义：ISO 9241-11 三指标（一切度量的根）** → `references/design-measurement-research.md` L41
- **2. 合规地基（一）：中国 AI 生成内容标识，是法定义务不是设计建议** → `references/ai-design-toolchain.md` L50
- **2. 品牌视觉的四层结构（别从 logo 开始）** → `references/brand-identity.md` L25
- **2. 图标网格系统（Grid & Keylines）** → `references/iconography.md` L25
- **2. 图表选型决策树（30 秒版）** → `references/dataviz.md` L43
- **2. 安全区与边距** → `references/presentation-design.md` L81
- **2. 形态决策矩阵（什么时候用什么）** → `references/navigation-ia.md` L25
- **2. 指标体系：先背下这七个数** → `references/performance-design.md` L46
- **2. 标签：位置三选一，别混用** → `references/form-table.md` L55
- **2. 组件文档页九段式：GOV.UK 逐节拆解（最经得起检验的模板）** → `references/design-system-docs.md` L54
- **2. 编排的四种时间结构与总时长公式** → `references/motion-orchestration.md` L31
- **2. 表面层级：暗色的核心是"重排"，不是"反相"** → `references/dark-mode.md` L58
- **2. 评审前的三个前提（NN/g 原文三主题，必做）** → `references/design-critique.md` L36
- **2. 风格识别四维信号（拆任何风格都用这四把尺）** → `references/visual-style-taxonomy.md` L24
- **20 · 可发现性的度量：tree testing 与 findability** → `references/content-findability.md` L415
- **20 · 场景速查（12）** → `references/shape-elevation.md` L466 · `references/typography-system.md` L303 · `references/visual-hierarchy-gestalt.md` L384
- **20 · 库生态实测与选型** → `references/direct-manipulation.md` L488
- **20. 20 项自检（交付一份研究方案 / 看一份数据报告时逐条过）** → `references/design-measurement-research.md` L371
- **20. 5 段可抄代码（§20.1–§20.3 为 Python 实跑）** → `references/overlays-modality.md` L533
- **20. AI 关 20 项自检（第 6 步新增，逐条可判 PASS/FAIL）** → `references/ai-design-toolchain.md` L537
- **20. 上线自检 22 项** → `references/design-ethics-inclusion.md` L475
- **20. 二十项自检（组件文档上线前逐条打勾）** → `references/design-system-docs.md` L728
- **20. 可抄代码 5 段（3 段 Python 实跑，输出为本轮实测）** → `references/conversational-generative-ui.md` L486
- **20. 可抄代码（3 段 Python 已实跑，含双用例断言）** → `references/component-api-design.md` L576
- **20. 四个可抄模板** → `references/handoff-collaboration.md` L780
- **20. 素材与出处（本轮实测 / 官方原文）** → `references/motion-orchestration.md` L1005
- **20. 自检 18 项（交付前逐条打勾）** → `references/brand-identity.md` L650
- **2026-10-28 · 开发者工具深色落地页（自测）** → `memory/design-log.md` L21
- **2026-10-29 · v4 系统化与中文场景补齐（每日升级 #1）** → `memory/design-log.md` L33
- **2026-10-29 · 元素级精准匹配升级（v3）** → `memory/design-log.md` L27
- **2026-10-30 · 动效系统 + 记忆树与检索（每日升级 #2）** → `memory/design-log.md` L46
- **2026-10-31 · 数据可视化规范（每日升级 #3）** → `memory/design-log.md` L61
- **2026-10-31 · 表单与表格规范（每日升级 #4）** → `memory/design-log.md` L79
- **2026-11-01 · 反馈与状态设计 + 检索层别名映射（每日升级 #6）** → `memory/design-log.md` L123
- **2026-11-01 · 可访问性实操（每日升级 #5）** → `memory/design-log.md` L98
- **2026-11-01 · 品牌视觉与 Logo 逻辑（每日升级 #9）** → `memory/design-log.md` L205
- **2026-11-01 · 响应式与断点体系（每日升级 #7）** → `memory/design-log.md` L147
- **2026-11-01 · 性能与设计的关系（每日升级 #11）** → `memory/design-log.md` L261
- **2026-11-01 · 暗色模式体系（每日升级 #10）** → `memory/design-log.md` L243
- **2026-11-01 · 版式与网格（每日升级 #8）** → `memory/design-log.md` L169
- **2026-11-01 · 设计交付与协作（每日升级 #12）** → `memory/design-log.md` L296
- **2026-11-05 · 内容设计与 UX 文案体系（每日升级 #13）** → `memory/design-log.md` L330
- **2026-11-05 · 动效进阶：编排、状态机与共享元素转场（每日升级 #15）** → `memory/design-log.md` L372
- **2026-11-05 · 国际化与本地化设计：i18n / L10n / RTL（每日升级 #16）** → `memory/design-log.md` L395
- **2026-11-05 · 演示文稿与幻灯片版式（每日升级 #14）** → `memory/design-log.md` L358
- **2026-11-05 · 设计系统文档写作：组件文档页 / 信息架构 / 版本化 / 治理（每日升级 #17）** → `memory/design-log.md` L413
- **2026-11-06 · AI / 生成式设计工具链：工作流、提示词、质量验收与合规边界（每日升级 #18）** → `memory/design-log.md` L439
- **2026-11-06 · 设计伦理与包容性：欺骗性设计、隐私同意 UI、成瘾机制与认知无障碍（每日升级 #19）** → `memory/design-log.md` L457
- **2026-11-07 · 图标设计系统（Iconography，每日升级 #22）** → `memory/design-log.md` L524
- **2026-11-07 · 导航与信息架构（Navigation & IA，每日升级 #23）** → `memory/design-log.md` L538
- **2026-11-07 · 每日升级 #25：色彩科学（Color Science）** → `memory/design-log.md` L564
- **2026-11-07 · 每日升级 #26：视觉风格谱系与设计运动（Visual Style Taxonomy）** → `memory/design-log.md` L571
- **2026-11-07 · 每日升级 #27：字体排印系统（Typography System）** → `memory/design-log.md` L589
- **2026-11-07 · 组件 API 设计与组合模式：状态所有权、渲染所有权、契约可演进（每日升级 #20）** → `memory/design-log.md` L478
- **2026-11-07 · 设计度量与用户研究：可用性指标、研究方法与统计验收（每日升级 #21）** → `memory/design-log.md` L502
- **2026-11-07 · 设计评审与反馈（Design Critique & Feedback，每日升级 #24）** → `memory/design-log.md` L551
- **2026-11-08 · 每日升级 #28：形状与深度系统（Shape & Elevation）** → `memory/design-log.md` L604
- **2026-11-08 · 每日升级 #29：视觉层级与格式塔组织律 / 注意力与认知负荷（Visual Hierarchy & Gestalt）** → `memory/design-log.md` L619
- **2026-11-09 · 每日升级 #30：内容可发现性与可扫读性（Content Findability / Search UX / Scannability）** → `memory/design-log.md` L633
- **2026-11-10 · 每日升级 #31：直接操纵与指针交互（Direct Manipulation / Pointer, Gesture & Drag-and-Drop）** → `memory/design-log.md` L647
- **2026-11-11 · 每日升级 #32：对话式与生成式界面（Conversational & Generative UI / AI 产品交互）** → `memory/design-log.md` L661
- **2026-11-11 · 每日升级 #33：叠加层与模态性（Overlays & Modality / Dialog / Popover / Top Layer）** → `memory/design-log.md` L675
- **21 · 与既有资产的边界矩阵** → `references/direct-manipulation.md` L509
- **21 · 六步构建流程** → `references/content-findability.md` L439
- **21 · 反模式（20）** → `references/shape-elevation.md` L485 · `references/typography-system.md` L322 · `references/visual-hierarchy-gestalt.md` L403
- **21. 6 段可抄代码** → `references/ai-design-toolchain.md` L562
- **21. GitHub API 实测仓库（2026-11-11 经 GitHub API）** → `references/conversational-generative-ui.md` L666
- **21. 六段可抄代码（文档团队直接拿去用）** → `references/design-system-docs.md` L753
- **21. 取源清单与 GitHub API 实测（2026-11-07 快照）** → `references/component-api-design.md` L856
- **21. 可抄代码（4 段 Python，已实跑）** → `references/design-measurement-research.md` L396
- **21. 可抄代码（4 段，3 段 Python 已实跑）** → `references/design-ethics-inclusion.md` L509
- **21. 数据来源** → `references/brand-identity.md` L673
- **21. 来源与引用（含置信度）** → `references/overlays-modality.md` L868
- **22 · 与既有资产的边界矩阵** → `references/content-findability.md` L450
- **22 · 场景速查（12）** → `references/direct-manipulation.md` L526
- **22 · 自检（20）** → `references/shape-elevation.md` L510 · `references/typography-system.md` L347 · `references/visual-hierarchy-gestalt.md` L428
- **22. 与其他资产的边界（避免重复与抢路由）** → `references/conversational-generative-ui.md` L684
- **22. 取源限制与不臆造声明（本轮公开记录）** → `references/component-api-design.md` L903
- **22. 取源限制（公开记录，不臆造）** → `references/overlays-modality.md` L891
- **22. 数据来源与取源纪律** → `references/design-ethics-inclusion.md` L728
- **22. 数据来源（全部官方原文 / 上游源码 / API 实测）** → `references/ai-design-toolchain.md` L761
- **22. 来源与取源限制（公开记录）** → `references/design-measurement-research.md` L480
- **22. 来源（2026-11-05 取源，全部官方原文 / 上游源码 / API 实测）** → `references/design-system-docs.md` L899
- **23 · 反模式（20）** → `references/direct-manipulation.md` L545
- **23 · 可抄代码（5 段，3 段 Python 已实跑）** → `references/visual-hierarchy-gestalt.md` L453
- **23 · 可抄代码（6 段）** → `references/shape-elevation.md` L535 · `references/typography-system.md` L372
- **23 · 场景速查（12）** → `references/content-findability.md` L467
- **23. 与既有资产的最短接线（防止知识孤岛）** → `references/design-measurement-research.md` L499
- **23. 与既有资产边界矩阵** → `references/overlays-modality.md` L907
- **23. 取源限制（公开记录，不臆造）** → `references/conversational-generative-ui.md` L702
- **23. 本轮让哪类问题不再含糊** → `references/design-ethics-inclusion.md` L788
- **24 · 反模式（20）** → `references/content-findability.md` L484
- **24 · 取源与限制（公开记录）** → `references/shape-elevation.md` L782 · `references/typography-system.md` L575 · `references/visual-hierarchy-gestalt.md` L647
- **24 · 自检（20）** → `references/direct-manipulation.md` L570
- **24. 接线** → `references/overlays-modality.md` L924
- **24. 数据来源清单** → `references/conversational-generative-ui.md` L715
- **25 · 可抄代码（5 段；§25.1–§25.3 为 Python，本轮已实跑 PASS）** → `references/direct-manipulation.md` L595
- **25 · 自检（20）** → `references/content-findability.md` L509
- **25. 术语与口径速记** → `references/conversational-generative-ui.md` L732
- **26 · 取源与限制（公开记录）** → `references/direct-manipulation.md` L863
- **26 · 可抄代码（5 段；§26.1–§26.3 为 Python，本轮已实跑 PASS）** → `references/content-findability.md` L534
- **27 · 取源与限制（公开记录）** → `references/content-findability.md` L908
- **3 · 字体选型：覆盖 / 回退 / 授权三个前置，而不是「挑好看的」** → `references/typography-system.md` L42
- **3 · 感知均匀性：HSL 为什么撒谎** → `references/color-science.md` L37
- **3 · 裁决一：F 型是默认行为，不是设计目标** → `references/visual-hierarchy-gestalt.md` L45
- **3 · 裁决一：SC 2.4.5 是「至少两条路」，不是「有个搜索就行」** → `references/content-findability.md` L46
- **3 · 裁决一：SC 2.5.7 要的是「单指针无拖动」，不是「键盘也能拖」** → `references/direct-manipulation.md` L46
- **3 · 裁决一：elevation 是语义 z-height，不是可直接抄写的阴影值** → `references/shape-elevation.md` L47
- **3. APG 对话框契约逐字条文：初始焦点、Tab 循环、Escape、关闭后归位** → `references/overlays-modality.md` L68
- **3. EDPB Guidelines 03/2022 v2.0：六类机制（官方 PDF 74 页，一手）** → `references/design-ethics-inclusion.md` L70
- **3. LCP：把 2.5 秒拆成四段（这是最有用的一张表）** → `references/performance-design.md` L94
- **3. 主流动派谱系（编年 + 视觉签名 + 何时用 / 不用 + 代表）** → `references/visual-style-taxonomy.md` L55
- **3. 五问验收 + 组件页字段清单（能打分才算规范）** → `references/design-system-docs.md` L106
- **3. 交付物清单：spec sheet 的 9 个字段** → `references/handoff-collaboration.md` L50
- **3. 交错编排 stagger：variants 传播与多框架实现** → `references/motion-orchestration.md` L72
- **3. 从三个词到视觉：定位翻译表** → `references/brand-identity.md` L47
- **3. 任务级指标：成功率、任务时间、错误率（最容易落地的三类）** → `references/design-measurement-research.md` L55
- **3. 动效时长：按距离和面积取，不按心情取** → `references/motion-system.md` L69
- **3. 合规地基（二）：中 / 欧 / 美三法域矩阵（出海产品必读）** → `references/ai-design-toolchain.md` L93
- **3. 图表色板：三类用途（分类 / 顺序 / 发散），不许混用** → `references/dataviz.md` L76
- **3. 字号体系与可读性** → `references/presentation-design.md` L122
- **3. 字段宽度：按内容长度定宽（最被忽视的一条）** → `references/form-table.md` L86
- **3. 描边与笔画（Stroke）** → `references/iconography.md` L44
- **3. 文字：暗色下不能用纯白（暗色对比度与文字层级）** → `references/dark-mode.md` L141
- **3. 断点该定在哪：内容断，不是设备断** → `references/responsive-layout.md` L160
- **3. 状态提升与派生状态（别把 state 复制两份）** → `references/component-api-design.md` L122
- **3. 给出反馈的七条铁律** → `references/design-critique.md` L46
- **3. 裁决一：流式文本不是状态消息，状态边界才播报（SC 4.1.3 逐字）** → `references/conversational-generative-ui.md` L59
- **3. 项数铁律（数量是有科学依据的，不是审美）** → `references/navigation-ia.md` L40
- **4 · G219 的四类无拖动替代与两步验收** → `references/direct-manipulation.md` L64
- **4 · M3 Elevation 六级精确表与组件映射** → `references/shape-elevation.md` L78
- **4 · 伽马（gamma）：为什么不能直接对 sRGB 插值** → `references/color-science.md` L49
- **4 · 字号阶梯与相对单位（px 不可访问裁决）** → `references/typography-system.md` L54
- **4 · 扫描模式全表：F 只是其中一种** → `references/visual-hierarchy-gestalt.md` L67
- **4 · 搜索入口的可发现性：位置、形态、宽度** → `references/content-findability.md` L66
- **4. ARIA23 role=log 与隐性 aria-live=polite / aria-atomic=false** → `references/conversational-generative-ui.md` L92
- **4. CPPA §7004：把「对称选择」写成可测量的步数（本轮最硬的规则）** → `references/design-ethics-inclusion.md` L94
- **4. FLIP：共享元素位移的通用算法（First · Last · Invert · Play）** → `references/motion-orchestration.md` L151
- **4. INP：交互延迟的三段与"设计侧预算"** → `references/performance-design.md` L126
- **4. SUS 系统可用性量表（10 题 · 0–100 · 基准 68 · 曲线分级）** → `references/design-measurement-research.md` L77
- **4. aria-modal="true" 双条件与误标后果** → `references/overlays-modality.md` L112
- **4. 信息架构地基（深度 vs 广度）** → `references/navigation-ia.md` L51
- **4. 信息架构：目录、命名、链接、检索（文档写作的四条地基）** → `references/design-system-docs.md` L140
- **4. 场景速查表（直接取值，不用再算）** → `references/motion-system.md` L101
- **4. 坐标轴铁律（含 G2 精确数值）** → `references/dataviz.md` L152
- **4. 尺寸阶梯（Sizing Scale）** → `references/iconography.md` L67
- **4. 接收反馈的四步（别辩护）** → `references/design-critique.md` L63
- **4. 控件尺寸与内边距（三体系精确值）** → `references/form-table.md` L110
- **4. 文字密度限制** → `references/presentation-design.md` L199
- **4. 标志类型学：七型与选择决策** → `references/brand-identity.md` L78
- **4. 标注规则：标例外，不标全量** → `references/handoff-collaboration.md` L79
- **4. 组合 vs 继承：多个「洞」怎么开（React + Vue 对照）** → `references/component-api-design.md` L133
- **4. 裁决一：提示词写得再细，也不构成作者身份（本轮最重要的一条）** → `references/ai-design-toolchain.md` L115
- **4. 跨断点做什么：五个动词** → `references/responsive-layout.md` L202
- **4. 边框与分隔线：暗色下不可依赖** → `references/dark-mode.md` L183
- **4. 风格匹配决策（给定"A 感觉"，怎么拆成信号）** → `references/visual-style-taxonomy.md` L136
- **5 · OKLab / OKLCH：公式与用法** → `references/color-science.md` L59
- **5 · 搜索框的标签契约：placeholder 不是 label** → `references/content-findability.md` L87
- **5 · 行高、行长与段落节奏（可计算，不靠感觉）** → `references/typography-system.md` L67
- **5 · 裁决二：四条 WCAG 准则构成的顺序契约** → `references/visual-hierarchy-gestalt.md` L87
- **5 · 裁决二：路径手势、拖动、指针取消是三条不同的准则** → `references/direct-manipulation.md` L85
- **5 · 裁决二：阴影不能充当 WCAG 1.4.11 的 3:1 识别边界** → `references/shape-elevation.md` L99
- **5. CLS：公式、五个位移源、设计侧防抖清单** → `references/performance-design.md` L163
- **5. CPPA §7003：可读性、无障碍与「显著链接」的具体要求** → `references/design-ethics-inclusion.md` L149
- **5. UMUX / UMUX-Lite（4 题 / 2 题 · 与 SUS 强相关）** → `references/design-measurement-research.md` L112
- **5. 五种「换元素」API 的完整对照（选型先看这个，别看 star）** → `references/component-api-design.md` L158
- **5. 列表增删与重排：四种操作的动画策略** → `references/motion-orchestration.md` L209
- **5. 原生 <dialog 的浏览器代劳清单：showModal / show / open / closedby** → `references/overlays-modality.md` L134
- **5. 图例、标签、注释** → `references/dataviz.md` L184
- **5. 图标与文字间距（Icon–Text Spacing）** → `references/iconography.md` L84
- **5. 必填与可选：只标少数派** → `references/form-table.md` L140
- **5. 怎么开一场评审（议程 / RACI / 远程异步）** → `references/design-critique.md` L72
- **5. 文档写作规范：Google 三条参考层级 + 可直接执行的清单** → `references/design-system-docs.md` L157
- **5. 栅格与版心：三个必须给的数值** → `references/responsive-layout.md` L226
- **5. 标志几何构造：网格 / 基形 / 笔画 / 光学修正** → `references/brand-identity.md` L123
- **5. 母版与占位符** → `references/presentation-design.md` L246
- **5. 混搭的纪律（什么能混、什么冲突）** → `references/visual-style-taxonomy.md` L158
- **5. 状态矩阵：9 态，别画 2ⁿ** → `references/handoff-collaboration.md` L142
- **5. 编排：多个元素一起动时的顺序** → `references/motion-system.md` L131
- **5. 聊天界面播报工程契约：chatbot 流式输出的状态边界（空容器、aria-busy、aria-relevant、assertive 双播）** → `references/conversational-generative-ui.md` L118
- **5. 裁决二：Content Credentials / 打了 AI 标 ≠ 版权清晰 ≠ 内容为真** → `references/ai-design-toolchain.md` L153
- **5. 阴影与高度：两派做法与正确用法** → `references/dark-mode.md` L203
- **5. 面包屑（Breadcrumb）** → `references/navigation-ia.md` L61
- **6 · APG combobox 契约：自动补全不是「弹个下拉」** → `references/content-findability.md` L99
- **6 · SC 2.5.2 与 G210：取消是硬要求，撤销不是可选项** → `references/direct-manipulation.md` L108
- **6 · WCAG 2.2 三关硬数值（1.4.4 / 1.4.8 / 1.4.12）** → `references/typography-system.md` L80
- **6 · 三顺序一致性验收：DOM / 焦点 / 标题树** → `references/visual-hierarchy-gestalt.md` L134
- **6 · 对比度：两套算法，不是只有 WCAG 2.x** → `references/color-science.md` L104
- **6 · 非文本 3:1 的正确落点（边界 / 焦点 / 状态）** → `references/shape-elevation.md` L125
- **6. AI 素材的来源与授权链** → `references/ai-design-toolchain.md` L194
- **6. Popover API 三态：always non-modal 与 auto · hint · manual 双栈** → `references/overlays-modality.md` L171
- **6. SEQ 单题易用度 + SUPR-Q 标准百分等级 + NPS** → `references/design-measurement-research.md` L123
- **6. 「自定义组件必须开放扩展」四条硬规则（Radix + Ariakit 共识）** → `references/component-api-design.md` L240
- **6. 中文数字与单位（中文项目必做）** → `references/dataviz.md` L204
- **6. 共享元素转场 A：View Transitions 完整机制** → `references/motion-orchestration.md` L271
- **6. 动画与转场** → `references/presentation-design.md` L301
- **6. 同意 UI 的 PASS/FAIL 构型表（可直接拿去评审）** → `references/design-ethics-inclusion.md` L163
- **6. 命名四套：图层 / 组件 / 变体 / token** → `references/handoff-collaboration.md` L176
- **6. 品牌色与语义色：降饱和，不是反相** → `references/dark-mode.md` L230
- **6. 填充 / 描边 / 双色（Fill · Stroke · Duotone）** → `references/iconography.md` L93
- **6. 性能预算：给每个页面类型一个数字** → `references/performance-design.md` L215
- **6. 标志清space（安全边距）三口径** → `references/brand-identity.md` L163
- **6. 标签页 Tabs（ARIA 的正确打开方式）** → `references/navigation-ia.md` L73
- **6. 校验时机：三档，各有明确适用** → `references/form-table.md` L154
- **6. 流式排版：clamp() 的正确用法** → `references/responsive-layout.md` L263
- **6. 物理感：什么时候用弹簧，什么时候用曲线** → `references/motion-system.md` L141
- **6. 示例代码的可抄性：五条硬规则（写错就没人用）** → `references/design-system-docs.md` L188
- **6. 裁决二：生成式界面 streamUI 是组件白名单里的路由，不是任意组件** → `references/conversational-generative-ui.md` L137
- **6. 评判框架（把"好不好"变成可讨论的尺子）** → `references/design-critique.md` L90
- **6. 趋势生命周期（何时该上、何时已过）** → `references/visual-style-taxonomy.md` L168
- **7 · box-shadow 正式语法（MDN 逐条核验）** → `references/shape-elevation.md` L144
- **7 · 拖放的完整状态机：从 down-event 到可撤销** → `references/direct-manipulation.md` L126
- **7 · 文本间距覆盖验收（注入式实测五步）** → `references/typography-system.md` L98
- **7 · 格式塔 12 条组织律全表（IxDF 逐条核对）** → `references/visual-hierarchy-gestalt.md` L155
- **7 · 联想、筛选与结果：第一次查询基本就是决战** → `references/content-findability.md` L130
- **7 · 色盲：三型 + Okabe–Ito 8 色** → `references/color-science.md` L143
- **7. AI SDK RSC experimental 与生产推荐路径（口径不张冠李戴）** → `references/conversational-generative-ui.md` L182
- **7. DESIGN.md：把"风格一致性"变成 AI 可读的契约** → `references/ai-design-toolchain.md` L219
- **7. HEART 框架（Google 五指标 + 三层落地法）** → `references/design-measurement-research.md` L141
- **7. props 合并优先级：一张能判 PASS/FAIL 的算子表** → `references/component-api-design.md` L274
- **7. top layer、inert、::backdrop 与 z-index 的分界** → `references/overlays-modality.md` L219
- **7. 中国《个人信息保护法》五条 UI 底线（官方全文逐字）** → `references/design-ethics-inclusion.md` L184
- **7. 中文 / 出海场景的风格注意** → `references/visual-style-taxonomy.md` L178
- **7. 仪表盘布局** → `references/dataviz.md` L223
- **7. 光学对齐与修正（Optical Alignment）** → `references/iconography.md` L107
- **7. 共享元素转场 B：layoutId 与 Motion 布局动画** → `references/motion-orchestration.md` L383
- **7. 反模式 15 条** → `references/design-critique.md` L128
- **7. 图像、插画、图标** → `references/dark-mode.md` L273
- **7. 图片：设计师最直接的性能杠杆** → `references/performance-design.md` L251
- **7. 完整填充范例：一个可直接复制的组件文档页（Button 精简版）** → `references/design-system-docs.md` L202
- **7. 实现：可直接抄的四段代码** → `references/motion-system.md` L155
- **7. 投影对比度与配色** → `references/presentation-design.md` L358
- **7. 最小尺寸与响应式标志四档（多小算太小 / 缩小到什么时候换版）** → `references/brand-identity.md` L198
- **7. 移动端导航降级** → `references/navigation-ia.md` L82
- **7. 组件 API 与设计稿 1:1 对齐** → `references/handoff-collaboration.md` L224
- **7. 视口单位：100vh 是个陷阱** → `references/responsive-layout.md` L310
- **7. 错误文案：模板化，禁止「输入有误」** → `references/form-table.md` L173
- **8 · 200% 缩放与容器弹性（按钮 / 输入框 / 卡片）** → `references/typography-system.md` L114
- **8 · 七体系阴影 token 精确对照（源码 / 官方文档实测）** → `references/shape-elevation.md` L167
- **8 · 决策一图流：从入口到死胡同** → `references/content-findability.md` L151
- **8 · 组织律里可验收的四个部分** → `references/visual-hierarchy-gestalt.md` L180
- **8 · 色板生成科学：四条可复现路线（选一不许混）** → `references/color-science.md` L162
- **8 · 裁决三：目标尺寸三套口径，24×24 是 AA 下限不是设计值** → `references/direct-manipulation.md` L143
- **8. WCAG 2.2 四条款矩阵：谁管叠加层的哪一段** → `references/overlays-modality.md` L229
- **8. useChat 四态状态机与 message.parts（parts 不是 content）** → `references/conversational-generative-ui.md` L207
- **8. 中国《互联网广告管理办法》第 10 条：一键关闭的量化红线** → `references/design-ethics-inclusion.md` L200
- **8. 决策记录（ADR / critique notes）** → `references/design-critique.md` L148
- **8. 品牌色：主色怎么定（不是"选个好看的颜色"）** → `references/brand-identity.md` L229
- **8. 响应式图片：三条规则 + 一个防抖** → `references/responsive-layout.md` L336
- **8. 图表动效（与 motion-system.md 的关系）** → `references/dataviz.md` L242
- **8. 图表在幻灯片中的规则** → `references/presentation-design.md` L409
- **8. 复合组件 / Compound Components 与状态共享** → `references/component-api-design.md` L295
- **8. 字体：最容易被设计师低估的成本** → `references/performance-design.md` L324
- **8. 帮助文字、占位符、前缀后缀** → `references/form-table.md` L203
- **8. 当前位置指示（"You are here"）** → `references/navigation-ia.md` L91
- **8. 性能与降级** → `references/motion-system.md` L238
- **8. 把风格转成 token（与 design-tokens.md 对接）** → `references/visual-style-taxonomy.md` L186
- **8. 提示词工程：把设计 brief 变成可复用、可评估的 prompt** → `references/ai-design-toolchain.md` L237
- **8. 样本量：定性「发现」与定量「下结论」是两回事** → `references/design-measurement-research.md` L157
- **8. 活文档四件套：研究 / 已知问题 / 近期变更 / 帮助改进（证据与反馈闭环）** → `references/design-system-docs.md` L293
- **8. 状态与交互反馈在暗色下的差异** → `references/dark-mode.md` L302
- **8. 状态图标（State Icons）** → `references/iconography.md` L116
- **8. 跨文档转场（MPA）与导航方向类型** → `references/motion-orchestration.md` L418
- **8. 验收标准的写法：Given / When / Then** → `references/handoff-collaboration.md` L259
- **9 · Variable Fonts 与五个注册轴** → `references/typography-system.md` L126
- **9 · W3C Pointer Events Level 3 的规范性因果链：pointercancel 什么时候必然触发** → `references/direct-manipulation.md` L179
- **9 · 三层阴影为什么够：物理分解与克制原则** → `references/shape-elevation.md` L245
- **9 · 信息气味：一个相对量，不是一个形容词** → `references/content-findability.md` L173
- **9 · 前注意属性：为什么"单特征差异"才会 pop-out** → `references/visual-hierarchy-gestalt.md` L201
- **9 · 渐变与插值：在 OKLab 空间做** → `references/color-science.md` L175
- **9. 12 场景速查** → `references/visual-style-taxonomy.md` L204
- **9. AG-UI 对话状态机：RunStarted / RunError / TextMessageStart 与 messageId 归属** → `references/conversational-generative-ui.md` L240
- **9. AI 辅助设计的工作流（可直接落地的 8 步）** → `references/ai-design-toolchain.md` L285
- **9. JavaScript：设计师看不见但逃不掉的那部分** → `references/performance-design.md` L399
- **9. SC 1.4.13 三条件：Dismissible / Hoverable / Persistent 逐字与可执行判定** → `references/overlays-modality.md` L244
- **9. ref 与命令式 API：React 19 反陈旧裁决（本轮第二重要的裁决）** → `references/component-api-design.md` L308
- **9. 中文场景与小程序** → `references/motion-system.md` L285
- **9. 交付格式（Delivery Formats）** → `references/iconography.md` L126
- **9. 切换实现：四端与防闪白** → `references/dark-mode.md` L318
- **9. 动画状态机：四态/六态模型与 XState** → `references/motion-orchestration.md` L452
- **9. 可访问性** → `references/presentation-design.md` L442
- **9. 可访问性导航（及格线，不是加分项）** → `references/navigation-ia.md` L100
- **9. 可访问性（图表最容易漏的一节）** → `references/dataviz.md` L265
- **9. 工具** → `references/design-critique.md` L174
- **9. 控件选择矩阵（含中文特有字段）** → `references/form-table.md` L228
- **9. 研究方法全景：先定 2×2 再选工具** → `references/design-measurement-research.md` L176
- **9. 组件文档状态与成熟度（USWDS 生命周期 + Carbon semver 对照）** → `references/design-system-docs.md` L311
- **9. 自动续费：2025 年修正后的现行规则，以及一条必须纠正的过期口径** → `references/design-ethics-inclusion.md` L221
- **9. 色阶生成三条路线（选一条，别混）** → `references/brand-identity.md` L253
- **9. 表格在窄屏的降级（移动端表格 / 手机表格 / 表格变卡片）：四种策略** → `references/responsive-layout.md` L388
- **9. 设计评审（critique）：30 分钟，2 正 1 改** → `references/handoff-collaboration.md` L300
- **AI & Agents (38)** → `references/tools.md` L139
- **CTA 区块** → `references/patterns.md` L49
- **Capture & Media (33)** → `references/tools.md` L56
- **Components (128)** → `references/resources.md` L31
- **Creative Development (13)** → `references/portfolios.md` L106
- **Design & Canvas (17)** → `references/tools.md` L92
- **Design (41)** → `references/portfolios.md` L29
- **Design Engineering (55)** → `references/portfolios.md` L122
- **Development (30)** → `references/portfolios.md` L73
- **Development (40)** → `references/tools.md` L13
- **Founders & Makers (17)** → `references/portfolios.md` L9
- **Galleries (103)** → `references/inspiration.md` L9
- **Icons (33)** → `references/resources.md` L191
- **L0 · 视觉感知：先治"看不出来"** → `references/knowledge-map.md` L23
- **L1 · 界面语汇：从"感觉"到"构型"** → `references/knowledge-map.md` L50
- **L2 · 系统秩序：从"页面"到"系统"** → `references/knowledge-map.md` L75
- **L3 · 工程落地：从"稿"到"跑起来"** → `references/knowledge-map.md` L102
- **L4 · 判断与品味：在冲突约束下取舍** → `references/knowledge-map.md` L129
- **Motion & 3D (26)** → `references/resources.md` L162
- **Other (1)** → `references/inspiration.md` L151 · `references/tools.md` L180
- **Other (6)** → `references/portfolios.md` L187
- **Productivity & Desktop (24)** → `references/tools.md` L112
- **Reading (33)** → `references/inspiration.md` L115
- **Studios (4)** → `references/portfolios.md` L180
- **Type & Colour (14)** → `references/resources.md` L14
- **YYYY-MM-DD · 需求一句话** → `memory/design-log.md` L14
- **§0 一页速查（赶时间只看这里）** → `references/editorial-layout.md` L18
- **§1 先判载体：五类产出的本质差异** → `references/editorial-layout.md` L38
- **§1 先定判定口径：无障碍验收按哪套标准（否则后面全是空谈）** → `references/accessibility.md` L9
- **§1 反馈的五个层级与选择决策** → `references/feedback-states.md` L10
- **§10 动态内容播报：aria-live 用对了才有用** → `references/accessibility.md` L393
- **§10 可访问性与合规** → `references/feedback-states.md` L389
- **§10 海报（Poster）** → `references/editorial-layout.md` L314
- **§11 中文场景与弱网** → `references/feedback-states.md` L429
- **§11 图片、图标、图表的替代文本** → `references/accessibility.md` L418
- **§11 长图（Long Image / 信息长图）** → `references/editorial-layout.md` L368
- **§12 不靠颜色单独传达（1.4.1）** → `references/accessibility.md` L448
- **§12 反模式（逐条对照，命中即改）** → `references/feedback-states.md` L440
- **§12 社媒图（各平台尺寸表）** → `references/editorial-layout.md` L398
- **§13 上线自检（15 条，全部可判定）** → `references/feedback-states.md` L465
- **§13 印刷交付（设计做完不等于能印）** → `references/editorial-layout.md` L445
- **§13 用户偏好媒体查询（三条，别只做第一条）** → `references/accessibility.md` L491
- **§14 CSS 实现（可抄）** → `references/editorial-layout.md` L476
- **§14 可抄代码** → `references/feedback-states.md` L485
- **§14 读屏实测：不做实测等于没做** → `references/accessibility.md` L517
- **§15 中文版式专项（避头尾 / 标点 / 竖排）** → `references/editorial-layout.md` L579
- **§15 工具与库（2026-11-01 GitHub API 实测）** → `references/feedback-states.md` L573
- **§15 自动化工具的边界（别把它当验收）** → `references/accessibility.md` L548
- **§16 中文场景：法规、国标、适老化（国外规范不管的部分）** → `references/accessibility.md` L577
- **§16 工具链（star / 许可实测 2026-11-01）** → `references/editorial-layout.md` L598
- **§17 上线前自检：25 条（按可判定性排序）** → `references/accessibility.md` L607
- **§17 反模式（20 条，逐条对照）** → `references/editorial-layout.md` L621
- **§18 反模式 18 条（评审时逐条对照）** → `references/accessibility.md` L644
- **§18 自检（18 项，交付前逐条过）** → `references/editorial-layout.md` L646
- **§19 三个常见争议，本技能给立场** → `references/accessibility.md` L667
- **§19 三套可抄模板** → `references/editorial-layout.md` L676
- **§2 对比度：四个阈值、一条铁律、一个中文陷阱** → `references/accessibility.md` L38
- **§2 时间阈值（唯一的权威刻度）** → `references/feedback-states.md` L46
- **§2 网格类型与选择** → `references/editorial-layout.md` L54
- **§20 与其他文件的分工** → `references/editorial-layout.md` L756
- **§3 Toast / Snackbar / Message（轻提示）** → `references/feedback-states.md` L75
- **§3 栏数、gutter 与基线网格** → `references/editorial-layout.md` L74
- **§3 焦点可见：三层标准叠着用** → `references/accessibility.md` L89
- **§4 加载与进度** → `references/feedback-states.md` L126
- **§4 版心与页边距（版心宽度 / 页边距比例）** → `references/editorial-layout.md` L108
- **§4 键盘：顺序、陷阱、返回** → `references/accessibility.md` L164
- **§5 字号模数与层级（字号阶梯）** → `references/editorial-layout.md` L161
- **§5 焦点不被遮挡（2.4.11）：粘性栏的账要还** → `references/accessibility.md` L221
- **§5 空态 / 空状态（五种"空"）** → `references/feedback-states.md` L177
- **§6 目标尺寸：24 是底线，44 是好用，48/60 是适老** → `references/accessibility.md` L241
- **§6 行长与行距（最影响"读得下去"的两项）** → `references/editorial-layout.md` L191
- **§6 错误状态的分级** → `references/feedback-states.md` L230
- **§7 弹窗、确认与破坏性操作** → `references/feedback-states.md` L281
- **§7 拖动必须有替代（2.5.7）** → `references/accessibility.md` L273
- **§7 段落细节与断行（工艺层，差一点就差很多）** → `references/editorial-layout.md` L236
- **§8 五态数据模型（工程落地）** → `references/feedback-states.md` L333
- **§8 视觉动线与焦点** → `references/editorial-layout.md` L270
- **§8 语义与 ARIA：原生优先，ARIA 是补丁不是方案** → `references/accessibility.md` L290
- **§9 十个高频场景速查** → `references/feedback-states.md` L372
- **§9 留白与密度（留白占比）** → `references/editorial-layout.md` L296
- **§9 表单无障碍：只补 form-table.md 没说的** → `references/accessibility.md` L330
- **一、DESIGN.md 是什么，为什么值得作为交付物** → `references/design-md-format.md` L10
- **一、三层架构（唯一正确的组织方式）** → `references/design-tokens.md` L9
- **一、中文排版：为什么不是"英文换字"** → `references/chinese-design.md` L10
- **一、判层：国际化与本地化 i18n / L10n / 翻译 / 多语言 / RTL 不是同一件事** → `references/i18n-localization.md` L11
- **一、判据：什么时候真的需要多品牌架构** → `references/multi-brand-theming.md` L11
- **一、总则：文字是界面的一部分，不是装饰** → `references/ux-writing.md` L10
- **七、ICU MessageFormat：禁拼接字符串、单句完整翻译、select / plural / selectordinal** → `references/i18n-localization.md` L431
- **七、与本技能其他文件的衔接** → `references/design-md-format.md` L182
- **七、对话框与通知文案** → `references/ux-writing.md` L301
- **七、运行时切换 vs 构建期编译** → `references/multi-brand-theming.md` L305
- **三、54 品牌 DNA 速查** → `references/design-md-format.md` L44
- **三、lang 与 dir：BCP 47 语言声明、RTL 方向、WCAG 3.1.1 / 3.1.2** → `references/i18n-localization.md` L124
- **三、三大体系对比（选哪套取决于产品语境）** → `references/design-tokens.md` L112
- **三、中文产品形态的四个特征（影响设计决策）** → `references/chinese-design.md` L167
- **三、四层架构：在原有三层上加一层"品牌输入"** → `references/multi-brand-theming.md` L52
- **三、错误文案（最高频的文案翻车点）** → `references/ux-writing.md` L100
- **三十一条专题支线（可与主线并行）** → `references/knowledge-map.md` L154
- **九、四套真实主题矩阵对照（可直接抄结构）** → `references/multi-brand-theming.md` L353
- **九、导航与信息架构文案** → `references/ux-writing.md` L376
- **九、日期 / 时间 / 日历 / 时区格式（Node 实测）** → `references/i18n-localization.md` L564
- **二、Ant Design 数值体系（中文语境最完整的一套）** → `references/design-tokens.md` L26
- **二、中文设计生态地图（平台怎么用、哪里有坑）** → `references/chinese-design.md` L121
- **二、主题不是"换色"，是四个正交轴** → `references/multi-brand-theming.md` L28
- **二、九章骨架（照此结构写，不增不减）** → `references/design-md-format.md` L26
- **二、按钮与操作文案（UI Copy）** → `references/ux-writing.md` L49
- **二、文案膨胀 text expansion / 翻译后按钮被截断 / 字数变长：翻译后文字变长、按钮放不下，+40% 不是安全值** → `references/i18n-localization.md` L44
- **二十、20 项自检（出海交付前逐条过）** → `references/i18n-localization.md` L863
- **二十、可抄代码（6 段）** → `references/multi-brand-theming.md` L664
- **二十一、6 段可抄代码** → `references/i18n-localization.md` L888
- **二十二、数据来源（官方原文 + API 实测）** → `references/i18n-localization.md` L1024
- **五、RTL 镜像规则：该镜像与不该镜像清单（Material Design Bidirectionality 官方）** → `references/i18n-localization.md` L298
- **五、Token 输出格式（三种落地形态）** → `references/design-tokens.md` L156
- **五、何时把 DESIGN.md 作为交付物** → `references/design-md-format.md` L153
- **五、品牌色护栏：把"客户给什么用什么"变成"算过才用"** → `references/multi-brand-theming.md` L174
- **五、语气与语调（Tone of Voice）** → `references/ux-writing.md` L207
- **仪表盘 Dashboard** → `references/patterns.md` L81
- **元素覆盖矩阵** → `references/component-libraries.md` L5
- **全景：五级台阶与对应产出** → `references/knowledge-map.md` L9
- **八、Intl API 全表与本机实测（Node v22.22.2）** → `references/i18n-localization.md` L502
- **八、多品牌同页共存（最容易被忽略的场景）** → `references/multi-brand-theming.md` L333
- **八、引导与 Onboarding 文案** → `references/ux-writing.md` L346
- **六、主题矩阵的落地：选择器与层叠策略** → `references/multi-brand-theming.md` L240
- **六、写 DESIGN.md 的四条纪律** → `references/design-md-format.md` L173
- **六、复数 plural：CLDR 六类、ICU 复数规则、不同语言复数形式（Node 实测）** → `references/i18n-localization.md` L365
- **六、常见错误（逐条对照）** → `references/design-tokens.md` L218
- **六、表单文案** → `references/ux-writing.md` L257
- **功能特性区 Features** → `references/patterns.md` L41
- **匹配与反馈日志（追加层，只增不改）** → `memory/design-log.md` L11
- **十、数字 / 货币 / 单位 / 千分位格式（Node 实测）** → `references/i18n-localization.md` L593
- **十、术语管理与一致性** → `references/ux-writing.md` L406
- **十、语义层分叉的边界：什么时候允许"每个品牌一套 L2"** → `references/multi-brand-theming.md` L381
- **十一、列表 / 相对时间 / DisplayNames / 排序 Collator / 中文分词 Segmenter（Node 实测）** → `references/i18n-localization.md` L622
- **十一、大小写与标点** → `references/ux-writing.md` L434
- **十一、配置文件结构：DTCG 多品牌写法** → `references/multi-brand-theming.md` L410
- **十七、12 个场景速查** → `references/multi-brand-theming.md` L597
- **十七、20 条反模式** → `references/ux-writing.md` L631
- **十七、框架与工程落地：React / Vue / Next / MUI RTL、字体、能力检测** → `references/i18n-localization.md` L788
- **十三、品牌注入管线：从客户填表到 CSS 生效** → `references/multi-brand-theming.md` L509
- **十三、国际化文案注意事项** → `references/ux-writing.md` L513
- **十三、语言协商 locale negotiation 与回退策略** → `references/i18n-localization.md` L692
- **十九、18 项自检（多品牌/多主题关）** → `references/multi-brand-theming.md` L641
- **十九、20 条反模式** → `references/i18n-localization.md` L838
- **十九、可抄代码** → `references/ux-writing.md` L683
- **十二、Figma 侧：变量模式必须与代码轴一一对应** → `references/multi-brand-theming.md` L495
- **十二、姓名 / 地址 / 称呼：不要 first name + last name（W3C《Personal names around the world》）** → `references/i18n-localization.md` L645
- **十二、数字、日期与单位** → `references/ux-writing.md` L479
- **十五、内容设计系统化** → `references/ux-writing.md` L571
- **十五、性能成本：变量数量与切换代价** → `references/multi-brand-theming.md` L561
- **十五、文化适配：颜色、图标、图像、示例数据与数字字形** → `references/i18n-localization.md` L755
- **十八、12 个场景速查** → `references/i18n-localization.md` L819
- **十八、18 项自检清单** → `references/ux-writing.md` L658
- **十八、20 条反模式** → `references/multi-brand-theming.md` L616
- **十六、12 场景速查** → `references/ux-writing.md` L612
- **十六、治理：品牌准入与变更管理** → `references/multi-brand-theming.md` L582
- **十六、给译者的交付规格：字符预算、变量说明、截图与术语表（与 handoff-collaboration.md 衔接）** → `references/i18n-localization.md` L768
- **十四、伪本地化 pseudolocalization / 伪翻译 / 伪 locale（Microsoft Learn 官方）** → `references/i18n-localization.md` L707
- **十四、可访问性与文案** → `references/ux-writing.md` L538
- **十四、防闪烁：多品牌特有的 FOUC** → `references/multi-brand-theming.md` L539
- **卡片 Card** → `references/patterns.md` L89
- **参考来源（本文件数值的出处）** → `references/accessibility.md` L680
- **反模式速查（任何元素通用）** → `references/patterns.md` L133
- **四、CSS logical properties：逻辑属性 inline / block、start / end 与 RTL 自动镜像** → `references/i18n-localization.md` L237
- **四、中文排版自检清单（交付前逐条过）** → `references/chinese-design.md` L182
- **四、中文设计系统矩阵（GitHub 验证 · 2026-10-29）** → `references/design-tokens.md` L133
- **四、从 1 个品牌色算出整套色阶：四条路线与精确参数** → `references/multi-brand-theming.md` L76
- **四、空态文案（Empty State Copy）** → `references/ux-writing.md` L176
- **四、项目类型 → 风格推荐（选风格先看场景）** → `references/design-md-format.md` L135
- **学习节奏（可持续，不靠意志力）** → `references/knowledge-map.md` L412
- **定价表 Pricing** → `references/patterns.md` L65
- **导航栏 Navbar** → `references/patterns.md` L7
- **工作流：接到任何设计任务时按此执行** → `SKILL.md` L116
- **当前画像（规则层，命中 ≥2 次的稳定偏好）** → `memory/design-log.md` L6
- **数据来源** → `references/handoff-collaboration.md` L837
- **数据表格 Data Table** → `references/patterns.md` L108
- **用法** → `references/inspiration.md` L5 · `references/portfolios.md` L5 · `references/resources.md` L5 · `references/tools.md` L5
- **登录/注册 Auth** → `references/patterns.md` L73
- **目录** → `references/presentation-design.md` L10
- **移动端底部导航 Tab Bar** → `references/patterns.md` L119
- **组件库选型规则** → `references/component-libraries.md` L24
- **维护协议** → `references/component-libraries.md` L34
- **能力自测（162 条，做到 ≥110 条即达 L2+）** → `references/knowledge-map.md` L543
- **自我成长机制（用得越多越准）** → `SKILL.md` L941
- **自我进化机制（知识保鲜）** → `SKILL.md` L954
- **落地页版式骨架（整页组装）** → `references/patterns.md` L126
- **表单 Form** → `references/patterns.md` L97
- **边界与习惯** → `SKILL.md` L977
- **附：来源** → `references/multi-brand-theming.md` L847
- **页脚 Footer** → `references/patterns.md` L57
- **首屏 Hero** → `references/patterns.md` L25

## 四、接线体检（自我进化的自检项）

✅ 所有 references 均已在 SKILL.md 接线。

> 每次升级新增参考文件后，必须同步在 SKILL.md 资产表 + 意图路由里加一行，否则等于没写。
