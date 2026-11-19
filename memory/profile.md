# 用户画像（规则层）

> 本文件只放被 ≥2 条证据支持、且经用户确认的规则。

## 字段

| 字段 | 含义 | 取值 |
| --- | --- | --- |
| rule | 一条可执行的设计规则 | 一句话，写清触发条件与动作 |
| domain | 所属域 | 布局 / 字体排印 / 色彩 / 动效 / 组件 / 内容 / 合规 / 流程 |
| first_seen | 首次出现的证据 | journal.jsonl:N |
| confirmations | 独立证据条数 | 整数，≥2 |
| evidence_refs | 支持该规则的证据行 | journal.jsonl:3,7 |
| status | 状态 | active / weakened / retired |

## 当前规则

**空。** 截至 2026-11-19，没有一条规则满足晋升条件。

原因：`memory/journal.jsonl` 的 49 条记录里，0 条来自真实用户的偏好陈述——43 条反馈字段为「无真实用户反馈（自动化任务）」，3 条是任务收尾或流程指令（process），其余记录无反馈字段。没有任何一条偏好出现过 ≥2 次独立证据，因此这里不写推测性内容。

晋升条件（三条同时满足才可写入）：

1. 同一 domain 下同一决策出现 ≥2 条独立证据（signal_type 为 explicit_preference 或 correction）；
2. 证据来自不同任务或日期，不是同一次会话里的重复记录；
3. 用户在会话中明确确认过（复述、点头，或写进项目的 DESIGN.md）。

## 如何晋升（5 步）

1. **记**：任务收尾时执行
   `python scripts/memory.py add --task "..." --signal explicit_preference --quote "用户原话" --decision "用户要什么"`
   没有真实反馈就记 `--signal none`；宁可空，不编。
2. **筛**：`python scripts/memory.py promote` 扫描 journal，输出「同域、决策等价、≥2 条证据」的候选。候选只是候选，不改任何文件。
3. **核**：回到 evidence_ref 指向的原文读上下文，排除巧合、单次场景和反讽；证据不足就停在候选。
4. **确认**：把规则复述给用户，得到明确确认。未确认不写。
5. **入册**：`python scripts/memory.py apply --rule "..." --domain 布局 --evidence 3,7`，交互输入 `y` 后写入本文件，status 记为 active。

## 季度重写

每季度最后一周做一次，把规则压到能一次读完的长度：

- 逐条复查 confirmations 与 status：新证据不足则降为 weakened；被用户明确否定的标 retired，保留一行原因；
- 合并同域近义规则，删掉「只描述偏好、没有设计动作」的条目；
- 重算 evidence_refs（journal 只追加不删，行号稳定），active 控制在 20 条以内；
- 文末记一行 `> 2026-Q4 重写：active N 条，retired M 条`；
- 改完跑 `python scripts/memory.py validate` 确认引用仍然可解析。

## 与采集协议的关系

journal 是原始记录（只追加），profile 是结论（可重写）。两者不一致时以 journal 为准。不要在 profile 里写「用户可能喜欢……」——没有证据的推测只配留在会话里，不配进文件。
