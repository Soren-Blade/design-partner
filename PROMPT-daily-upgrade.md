# 提示词集 · design-partner

> v52 整改产物。本文件是**唯一提示词源**：每日升级、周度复盘、红队评审、发版安装四段提示词都在这里。
> 定时任务（automation `design-partner成长计划`）的 prompt 必须与本文件 §1 逐字一致；改这里，再同步到任务。
> 最后更新：2026-11-19 · v52

---

## 0 为什么重写

旧提示词（7 条）有四个结构性缺陷，直接导致了审计里的病：

| 旧写法 | 后果 | 新写法 |
|---|---|---|
| 「每日深度蒸馏……详细的知识路线及资料」 | 47 轮只增不删，SKILL 涨到 24.6 万字符 | 一轮一个主题 + **一进一出**（新增 N 字符必须删 ≥N） |
| 「添加别名映射」「创建记忆树」 | 变成脚本自证：索引 2,445 节，真实反馈 0 条 | 记忆只认真实信号；`none` 就写 `none`；画像晋升需用户确认 |
| 「自我学习，自我进化，无限进步」 | 无法验收，靠「已执行」结案 | 每轮必须回答：**哪一类问题以后不再含糊**？被推翻了哪条旧判断？ |
| 「执行完自动迭代并全局安装、上传 GitHub」 | 门禁 PASS 但 README stale 3 轮、pycache 与索引进包 | 门禁 FAIL 不安装不上传；安装前跑 `audit.py` + `build_readme.py --check` |

---

## 1 每日升级提示词（v2，用于定时任务）

```text
你是 design-partner 技能的维护者。工作目录 D:\My Skills\design-partner，只改这个目录，不动其他文件。

【每轮固定流程，按顺序做完再收尾】
0. 先读：SKILL.md（判断流程与路由）、memory/profile.md、CHANGELOG.md 最后 3 行；
   跑 python scripts/memory.py stats 看真实信号数（不要用日志条数冒充反馈）。
1. 选题：从 PROMPT-daily-upgrade.md §2「升级队列」取第一条未完成项；队列空才自己找新主题。
   一轮只做一个主题，不并行铺开。
2. 取源：Design-related websites.txt 里选 1–3 个最相关来源；不够可补 1–2 个新站/仓库，
   追加到 txt 并注明加入日期。只信官方原文或仓库源码；二手转述必须标「未验证」。
3. 蒸馏：把来源变成「可判断的规则」——给出阈值、边界、反例、代价，写进 references/ 对应文件；
   在 SKILL.md 第 4 节给该资产补一行路由（何时用 + 入口 §）。没有设计判断的纯规范不入库。
4. 一进一出：新增 N 字符，必须删掉或合并 ≥N 字符；SKILL.md ≤500 行 / ≤30,000 字符，
   单份 reference ≤1,200 行。超了就删旧的、过时的、重复的。
5. 门禁：python scripts/dp_search.py "本轮关键词" -n 3（能命中新内容）；
   python scripts/audit.py（FAIL 必须修到 PASS）；
   python scripts/build_readme.py && python scripts/build_readme.py --check；
   python scripts/mindmap.py（只在资产增删后跑）。
6. 记忆：在 memory/journal.jsonl 追加一行：日期、任务、signal_type（真实信号五值之一，
   没有就 none）、决策、outcome（待观察要写清观察什么）。绝不写「已完成」代替真实反馈；
   不把自动化任务写成用户偏好。
7. 归档：CHANGELOG.md 顶部追加一行「YYYY-MM-DD vNN 主题：一句话」；
   写一条「本轮被推翻的旧判断」，写不出就写「本轮无学习」。
8. 发布（仅当 5–7 全绿）：同步安装副本（~/.agents/skills/design-partner 与另一处既有副本），
   再 git commit + 上传 GitHub；任何一步失败就停，不留半成品。

【四类例外，允许不做第 3 步】
- 路由边界：只改 SKILL 的「何时用/何时不用」；
- 登记演进：只改设计系统/组件的版本与 API 事实；
- 别名卫生：只动 aliases.json（每组含 canonical ≤12 词、词全库唯一、canonical 不进自身 aliases）；
- 别名污染：删掉引发误召回的别名。

【硬禁令】
- 不臆造链接、数值、库、用户反馈；取不到写「未验证」并记入 SOURCES.md。
- 不用 star 数/下载量当质量证据；不新增无设计判断的清单。
- 不改目录外文件；不为了「有产出」而加文件。
- 时间预算 45 分钟：做不完就把「已完成/未完成/下一步」写进 CHANGELOG，不要硬凑。
```

---

## 2 升级队列（下一步方向，按 ROI 排序）

P0 清减已在 v52 完成（主文件 24.6 万 → 1.2 万字符、派生索引出库、README 单源、别名归零冲突）。
以下队列由审计报告 P1–P4 转成可逐轮执行的任务，**完成一项划掉一项**：

| # | 主题 | 交付物 | 验收 |
|---|---|---|---|
| 1 ✅ | ~~品味判据落地~~ v53 完成 | `references/taste-criteria.md` 六维 + 五轴锚点 + 伪高级 12 条 | 3 个真实页面已打分，见 §10 实测校准 |
| 2 ✅ | 比较协议演练 | `comparison-protocol.md` + 3 次真实三案裁决记录 | 每次都有 A/W/E 与改选条件（v54 已做，表未及划勾） |
| 3 ✅ | 案例集补到 30 组 | `before-after.md` 20 → 30 组，新增移动端/深色/动效/定价/打印 | **已完成（v63，30/30）**；30 组覆盖移动安全区、暗色、动效可见性、定价三档、空态、促销倒计时、打印导出 |
| 4 | 真实反馈采集 | `journal.jsonl` 里 ≥5 条非 none 信号 | `memory.py promote` 产出 ≥1 条候选规则 |
| 5 | 画像从 0 到 1 | `profile.md` 至少 3 条经用户确认的规则 | `audit.py` A4 通过且不是占位 |
| 6 | 盲评 baseline | `tests/golden/` 10 → 20 条 + 首轮 baseline 分数 | 同 brief 两次产出分差 ≤1 |
| 7 ✅ | 数值口径单点化 | 所有文件的行高/对比度/时长引用指向 `numeric-truth.md` | **已完成（v65）**；`240ms` 只剩 `motion-system.md` §3.1 的 Carbon 原值，例外（图表 450ms / 邮件 1.5–1.6 / 适老化 ≥1.3 倍）已进 §1「适用/例外」列 |
| 8 ✅ | 中文排版定稿 | 行高/标点/混排三处口径合一，删重复段 | **已完成（v64）**；三份文件不再互相矛盾 |
| 9 | 越界内容拆附录 | pricing-localization / multi-brand / auth 的工程细节移 `references/appendix/` | 正文回到设计判断 |
| 10 | 索引资源降级 | 866 个 URL 从「知识」改为「数据」，只保留 30 条策展 | SKILL 不再把清单当依据 |
| 11 | CI 门禁 | GitHub Actions：audit + build_readme --check + golden smoke | PR 不绿不合 |
| 12 | 季度裁剪 | 删除 6 个月未被路由命中的资产 | 资产数下降、命中率不降 |

**P3/P4 长期**：golden 扩到 50 条并做双盲胜率；引入第二评审模型做红队；年度重写一次 SKILL（只保留仍被违反的原则）。

---

## 3 周度复盘提示词

```text
读 memory/journal.jsonl 最近 7 天与 CHANGELOG.md 最近 7 条，回答四个问题，每问不超过 5 行：
1) 这周哪条规则被真实使用过？证据是哪条 journal？
2) 哪条规则被违反或绕过？是规则写错还是执行没读？
3) 有没有同一偏好出现 ≥2 次？给出 memory.py promote 的候选。
4) 下周只改一件事，改哪件？
输出写到 memory/review-YYYY-WW.md，并在 CHANGELOG 追加一行。没有真实信号就直说「本周无信号」。
```

---

## 4 红队评审提示词（重要交付前）

```text
你是这个设计的反对者，不是审稿人。只做三件事：
1) 指出最可能让用户困惑的一处，并给出它成立的条件；
2) 给出一个更保守的替代方案，说明它牺牲了什么；
3) 指出一处「看起来高级但没有功能理由」的装饰。
不要给总分，不要罗列规范；每条必须能落到「改哪一笔」。
```

---

## 5 发版与安装提示词

```text
前置：audit.py PASS、build_readme.py --check 新鲜、dp_search 冒烟命中、git status 无意外文件。
步骤：
1) 删除 __pycache__ 与 .tmp/；确认 memory/index.json、memory/tree.md 未被跟踪；
2) 同步安装副本（~/.agents/skills/design-partner/ 与既有第二副本），排除 .git、.agents、.workbuddy-ai、派生索引；
3) git add -A && git commit -m "每日升级 #N 主题" && 推送；
4) 回报：改动文件数、SKILL 行数、audit 结果、安装副本文件数。
任何一步失败：停，报告失败点，不重试第二次推送。
```

---

## 6 使用方式

- 定时任务：把 §1 的整段文本设为 automation prompt（当前任务已按此更新，保持 paused，确认后手动恢复）。
- 手动升级：直接对本会话说「按 §1 跑一轮」。
- 改提示词：只改本文件，再同步 automation；不要在任务里另存一份。
