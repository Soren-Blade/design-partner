# design-partner · 设计伙伴

**把模糊的想法，变成有品味、可执行的设计决策。** 它不是一本规范手册，而是一条判断流程：
先问清约束，再并置三个方向，然后带着代价选一个，最后用证据自检。

`当前版本 {{VERSION}}` · 本页由 `scripts/build_readme.py` 生成于 {{DATE}} · 生成器与 `CHANGELOG.md` 同源

---

## 它做什么，不做什么

| 做 | 不做 |
|---|---|
| 从一句模糊需求里问出真正约束（最多 3 个问题，给选项） | 一上来给 8 套配色让你挑 |
| 对同一 brief 给**保守 / 主流 / 进取**三案，并说明各自代价 | 只给「最佳实践」一句话 |
| 按比例、节奏、层级、材料、克制、一致性六维给审美判断 | 用「高级感」「大气」当结论 |
| 用 5 秒测试、盲评、大众锚检验是否只是自我感觉良好 | 用合规清单代替好看 |
| 把每次真实反馈记进 `memory/journal.jsonl`，够了才升级为规则 | 把「待观察」写成「已完成」 |

## 30 秒开始

```bash
python scripts/dp_search.py "续费弹窗怎么写得不像骗人"   # 关键词 → 命中文件 §章节 + 行号
python scripts/dp_search.py --topic                    # 看全部主题
python scripts/mindmap.py                              # 资产变了才需要：重建索引与记忆树
python scripts/memory.py stats                         # 记忆里到底有多少条真实反馈
```

在 DeepSeek Harness 里直接说需求即可（如「做一个 SaaS 定价页」「这张海报不好看，改」），
技能会被自动载入；`SKILL.md` 是判断流程，`references/` 是按需读的 1–3 份资产。

## 一次完整的判断长什么样

```
你：做个面向独立开发者的 API 监控落地页
它：问 3 个问题（谁在什么场景打开？最怕什么？要极简还是浓烈？）→ 缺省：极简、浅色、专业
    给三案：A 保守（文档站气质，信任优先）/ B 主流（Linear 式暗色+渐变，转化优先）/ C 进取（监控墙即首屏，证据优先）
    裁决：选 B；代价＝更贵的前端动效与更弱的「朴素可信」；证据＝同类产品首屏 5 秒测试通过率
    改选 A 的条件：客户是金融/政企，采购先看合规与稳定
    自检：5 秒内能否说出「这是监控」？缩小到 320px 后主按钮还在首屏？暗色下状态色对比度过 4.5:1？
```

## 资产一览（{{REF_COUNT}} 份，按需读）

{{ASSET_TABLE}}

## 记忆与成长

- 反馈日志：`memory/journal.jsonl`，{{JOURNAL_ROWS}} 条记录，其中 {{JOURNAL_REAL}} 条带真实用户反馈
- 用户画像：`memory/profile.md`（{{PROFILE_STATE}}）；规则只在同一偏好出现 ≥2 次后晋升
- 历史：`CHANGELOG.md`（每轮一行摘要）；取源口径：`SOURCES.md`
- 成长协议：一进一出（新增 N 字符必须删掉 N 字符）、`SKILL.md` ≤ 500 行、单份资产 ≤ 1,200 行、
  每轮必须写下「被推翻的旧判断」；`scripts/audit.py` 是发布门禁

## 目录

```
SKILL.md           判断流程（≤500 行）：总纲 → 五问 → 判层 → 三案裁决 → 路由 → 自检 → 记忆 → 成长
references/        资产库：判断品味 / 视觉基础 / 版式系统 / 界面交互 / 领域商业 / 合规与索引
memory/            profile.md + journal.jsonl（长期记忆）；索引与树是本地生成物，不入库
scripts/           dp_search / mindmap / memory / audit / build_readme / regression
tests/golden/      10 条基准 brief + 评分 rubric（防回退）
CHANGELOG.md       逐版变更（只追加一行摘要）
SOURCES.md         每轮取源与「未验证」标记的纪律
```

## 视觉与内容边界

- 不臆造资源、库、数值：引用不给 URL 视为未验证，写进 `SOURCES.md` 的「未验证」区
- 不把法条当设计值、不把设计值当法条：口径冲突先查 `references/numeric-truth.md`
- 中文优先；中英混排、行高、标点按 `typography-system.md` + `chinese-design.md` 的同一套口径

## License

代码（`scripts/`、`tests/`）MIT；文本与资产（`SKILL.md`、`references/`、`memory/` 模板）CC BY 4.0，
转载注明来源。商用前请自行核对所引第三方规范的授权。

## 反馈

发现说错、过时、自相矛盾：直接开 issue，附「哪一句 / 哪份文件 / 反例」。
每一条带反例的反馈都会进 `journal.jsonl`，而不是只改一句话。
