#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
design-partner 记忆树生成器

扫描 SKILL.md / references/*.md / memory/*.md，产出两样东西：
  1) memory/index.json —— 机器索引（文件 → 章节 → 摘要 + 行号），供 dp_search.py 检索
  2) memory/tree.md     —— 人/agent 可读的知识树 + 意图路由 + 主题索引 + 接线体检

为什么需要它：
    技能资产到 11 份、上千行后，"知识在哪个文件哪一节"本身成了问题。
    没有索引时 agent 只能整份读，浪费上下文；有了索引可以先定位再精读。

用法:
    python scripts/mindmap.py              # 重建索引与树
    python scripts/mindmap.py --check      # 只做接线体检（SKILL.md 是否收录所有资产）
"""
import json
import re
import sys
import time
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "references"
MEM = ROOT / "memory"
SKILL = ROOT / "SKILL.md"

H2 = re.compile(r"^(#{2,3})\s+(.+?)\s*$", re.M)
FENCE = re.compile(r"```.*?```", re.S)
LINK = re.compile(r"\[([^\]]+)\]\([^)]+\)")
EMPH = re.compile(r"[*_`>|]")

# 意图 → 该去哪儿（保持与 SKILL.md 第 1 步的路由一致，树里做快捷方式）
INTENTS = [
    ("从零做视觉", "第 5 步原则 + patterns.md 取构型 + design-tokens.md 取数值"),
    ("改进现有设计", "按第 5 步逐条诊断；动效问题查 motion-system.md §10 验收清单"),
    ("要灵感 / 参考", "patterns.md（元素级）→ inspiration.md（风格级）→ portfolios.md（校准）"),
    ("要设计规范 / 系统", "design-tokens.md（三层 token）→ design-md-format.md（九章骨架）"),
    ("对标某品牌", "design-md-format.md §3 品牌 DNA + design-tokens.md 取精确值"),
    ("中文项目", "chinese-design.md（排版/生态）→ motion-system.md §9（小程序）"),
    ("动效 / 微交互 / 动画", "motion-system.md：§2 曲线 · §3 时长 · §4 场景表 · §7 代码 · §10 验收"),
    ("滚动动画 / 页面转场", "motion-system.md §7.3 View Transitions · §7.4 scroll-driven"),
    ("无障碍 / reduced-motion", "motion-system.md §8.1 三档降级"),
    ("提示 / toast / 弹窗 / 确认", "feedback-states.md：§1 层级决策 · §3 toast 数值 · §7 确认与破坏性操作"),
    ("加载 / 骨架屏 / 进度", "feedback-states.md：§2 时间阈值 · §4 加载与进度 · §14.2 骨架代码"),
    ("空状态 / 无数据 / 失败空", "feedback-states.md §5（五种空 + 五件套结构 + 文案公式）"),
    ("错误页 / 报错文案 / 重试", "feedback-states.md §6（五级错误 + 404/500 规则 + 三段式文案）"),
    ("找工具 / 资产", "tools.md（工具）· resources.md（图标/字体/3D）· component-libraries.md（代码）"),
    ("想提升自己 / 学习路径", "knowledge-map.md L0→L4 + 20 条自测"),
    ("AI 生成设计 / AIGC 工作流", "ai-design-toolchain.md §1 五层人工闸门 · §9 八步工作流 · §13 选型三问"),
    ("AI 内容标识 / 合规 / 版权 / 提示词 / AI 味验收", "ai-design-toolchain.md §2 标识 · §4 USCO 裁决 · §8 提示词 · §11 AI Slop Test · §20 自检"),
    ("设计伦理 / 欺骗性设计 / 隐私同意 / 自动续费 / 一键关闭", "design-ethics-inclusion.md §1 三条立场 · §2 现行 18 类 · §4 对称选择 · §8 一键关闭 · §9 反陈旧裁决 · §21 脚本"),
    ("包容性设计 / 认知无障碍 / 未成年人 / 成瘾设计", "design-ethics-inclusion.md §11 令第 766 号 · §12 成瘾四红线 · §14 三原则 · §15 七原则 · §16 COGA 八目标 · §17 四象限"),
    ("组件 API / props 契约 / 受控非受控 / 组合 / 插槽 / asChild / 换元素", "component-api-design.md §1 三份所有权 · §2 受控契约 · §5 五种换元素 API · §7 合并优先级 · §8 compound components"),
    ("ref 转发 / React 19 forwardRef / 复合组件键盘 / roving tabindex / 组件发版 SemVer / argTypes", "component-api-design.md §9 反陈旧裁决 · §12 APG 键盘契约 · §14 API SemVer 六冻结面 · §15 Storybook argTypes · §20 脚本"),
    ("设计度量 / 用户研究 / 可用性测试 / SUS / 样本量 / HEART / A-B 测试", "design-measurement-research.md §0 分层导语 · §1 度量三步法 · §3 任务级指标 · §4 SUS/UMUX · §5 问卷量表 · §7 样本量 · §11 A/B 统计"),
    ("满意度怎么量化 / 改版有没有效 / 要不要上线 A-B / 该做多少人的研究", "design-measurement-research.md §21 四段可抄代码（问题暴露率·比例样本量·SUS 计分·A/B z 检验）· §23 接线与其他资产"),
    ("不确定知识在哪", "python scripts/dp_search.py \"关键词\""),
]


def clean(text: str) -> str:
    text = FENCE.sub(" ", text)
    text = LINK.sub(r"\1", text)
    text = EMPH.sub("", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def slug(title: str) -> str:
    s = re.sub(r"[^\w\u4e00-\u9fff]+", "-", title).strip("-")
    return s.lower() or "section"


def load_aliases() -> list:
    """读 memory/aliases.json → [(规范词, [别名...])]，供树中展示与检索扩展。"""
    p = MEM / "aliases.json"
    if not p.exists():
        return []
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return []
    rows = []
    for g in data.get("groups", []):
        c, a = g.get("canonical"), g.get("aliases", [])
        if c:
            rows.append((c, a))
    return rows


def snapshot(text: str) -> str:
    m = re.search(r"快照\s*(\d{4}-\d{2}-\d{2})", text[:2000])
    if m:
        return m.group(1)
    m = re.search(r"(\d{4}-\d{2}-\d{2})\s*经?\s*GitHub\s*API", text[:2000])
    return m.group(1) if m else "—"


def mask_fences(text: str) -> str:
    """把 ``` 代码块里的内容抹成空格（保留换行与字符位置）。

    否则代码块里的 `## 标题` 会被当成真章节：例如变更日志模板里的
    `## [2.0.0] - 2026-11-01` 会变成一条假章节，污染索引与检索排序。
    抹成等长空格是为了让 match 的 start/end 仍能直接索引原文。
    """
    def repl(m):
        return re.sub(r"[^\n]", " ", m.group(0))
    return FENCE.sub(repl, text)


def parse_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    title = path.stem
    for line in lines[:15]:
        if line.startswith("# "):
            title = line[2:].strip()
            break

    sections = []
    # 标题只在代码块之外识别；正文仍从原文切，行号与内容都不受影响
    matches = list(H2.finditer(mask_fences(text)))
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end]
        # 若本节下面紧接子标题（body 只有空行），摘要要往下找：
        # 否则 §3 这类"只有子节、没有导语"的章节在索引里摘要为空，检索命中后片段也是空白。
        level = len(m.group(1))
        eff_end = end
        if not body.strip():
            for j in range(i + 1, len(matches)):
                if len(matches[j].group(1)) <= level:
                    eff_end = matches[j].start()
                    break
            else:
                eff_end = len(text)
        summary = ""
        for raw in text[start:eff_end].splitlines():
            s = raw.strip()
            if not s or s.startswith("|") or s.startswith("<!--") or s.startswith("#"):
                continue
            summary = clean(s)[:120]
            if summary:
                break
        line_no = text[: m.start()].count("\n") + 1
        sections.append({
            "id": slug(m.group(2)),
            "level": level,
            "title": clean(m.group(2)),
            "summary": summary,
            "line": line_no,
            "chars": len(body),
        })

    rel = path.relative_to(ROOT).as_posix()
    return {
        "path": rel,
        "title": clean(title),
        "snapshot": snapshot(text),
        "lines": len(lines),
        "chars": len(text),
        "sections": sections,
    }


def collect() -> list:
    files = []
    targets = [SKILL] + sorted(REF.glob("*.md")) + sorted(MEM.glob("*.md"))
    for p in targets:
        if p.exists() and p.name != "tree.md":
            files.append(parse_file(p))
    return files


def wiring_check(files: list) -> dict:
    """接线体检：SKILL.md 是否引用了每个资产；磁盘上是否有 SKILL.md 提到但不存在的文件。"""
    skill_text = SKILL.read_text(encoding="utf-8") if SKILL.exists() else ""
    referenced = set(re.findall(r"references/([\w\-.]+\.md)", skill_text))
    on_disk = {p.name for p in REF.glob("*.md")}
    return {
        "未接线": sorted(on_disk - referenced),      # 写了但没在 SKILL.md 里路由 → 等于没写
        "已失联": sorted(referenced - on_disk),      # SKILL.md 指向不存在的文件
    }


def build_tree(files: list, check: dict) -> str:
    today = time.strftime("%Y-%m-%d %H:%M")
    total_sections = sum(len(f["sections"]) for f in files)
    total_chars = sum(f["chars"] for f in files)

    out = [
        "# 记忆树 · Knowledge Tree",
        "",
        f"> 自动生成于 {today} ｜ {len(files)} 个文件 · {total_sections} 个章节 · {total_chars:,} 字符",
        "> 由 `scripts/mindmap.py` 重建，**不要手改**（手改会被下次覆盖；要改就改源文件或脚本）。",
        "",
        "## 怎么用（三条命令）",
        "",
        "```bash",
        "python scripts/dp_search.py \"缓动曲线\"      # 关键词检索：命中章节 + 行号 + 摘要",
        "python scripts/dp_search.py --topic          # 列出所有主题（章节标题一览）",
        "python scripts/mindmap.py                    # 资产变更后重建本树与 index.json",
        "```",
        "",
        "**检索纪律**：先用 `dp_search` 定位到「文件 §章节」，再只读那一段。不要整份读 references——十几份文件全读一遍会吃掉大量上下文，而命中往往只在一节。",
        "",
        "## 一、意图 → 位置（快捷路由）",
        "",
        "| 用户这么说 | 去哪儿 |",
        "|---|---|",
    ]
    for intent, where in INTENTS:
        out.append(f"| {intent} | {where} |")

    # 别名映射：检索层专用，只提升召回，不改上面的路由优先级
    alias_rows = load_aliases()
    if alias_rows:
        out += [
            "",
            "## 一·B、别名映射（检索层，不改路由优先级）",
            "",
            "> 用户在说法上不会统一：说「弹窗」还是 dialog、说「转圈」还是 loading。"
            "`memory/aliases.json` 把这些说法归到同一个规范词，`dp_search.py` 检索时以 **0.45 权重**追加召回——"
            "**只影响召回，不影响上表的意图路由顺序**。",
            "",
            "| 规范词 | 别名 / 俗称 / 中英对应 |",
            "|---|---|",
        ]
        for canonical, aliases in alias_rows:
            out.append(f"| **{canonical}** | {' · '.join(aliases)} |")
        out.append("")
        out.append("新增别名改 `memory/aliases.json`；`dp_search.py \"词\" --no-alias` 可关闭扩展做对比。")

    out += ["", "## 二、知识树（按文件）", ""]
    for f in files:
        out.append(f"### `{f['path']}` · {f['title']}")
        out.append(f"_{f['lines']} 行 · 快照 {f['snapshot']} · {len(f['sections'])} 节_")
        out.append("")
        for s in f["sections"]:
            indent = "  " * (s["level"] - 2)
            summary = f" — {s['summary']}" if s["summary"] else ""
            out.append(f"{indent}- **{s['title']}** `L{s['line']}`{summary}")
        out.append("")

    out += ["## 三、主题索引（章节标题 → 位置）", ""]
    idx = {}
    for f in files:
        for s in f["sections"]:
            if s["level"] == 2:
                idx.setdefault(s["title"], []).append(f"`{f['path']}` L{s['line']}")
    for title in sorted(idx):
        out.append(f"- **{title}** → {' · '.join(idx[title])}")

    out += ["", "## 四、接线体检（自我进化的自检项）", ""]
    if check["未接线"]:
        out.append("⚠️ **未接线**（在 references 里但 SKILL.md 没路由 → agent 不会在正确时机读到）：")
        for n in check["未接线"]:
            out.append(f"- `references/{n}`")
    else:
        out.append("✅ 所有 references 均已在 SKILL.md 接线。")
    if check["已失联"]:
        out.append("")
        out.append("❌ **已失联**（SKILL.md 指向但文件不存在）：")
        for n in check["已失联"]:
            out.append(f"- `references/{n}`")
    out += [
        "",
        "> 每次升级新增参考文件后，必须同步在 SKILL.md 资产表 + 意图路由里加一行，否则等于没写。",
        "",
    ]
    return "\n".join(out)


def main():
    files = collect()
    check = wiring_check(files)
    # 检索索引剔除变更日志：design-log.md 是流水账，关键词密度极高，
    # 会让「表单」「表格」这类查询的前 3 条全是日志而不是知识章节。
    # 树里仍保留它（人可读），只是不参与 dp_search 排序。
    # SKILL.md 常驻上下文（技能激活即全量可见），而它的「工作流」是 500+ 行的巨型章节，
    # 放进索引会吞掉任何多词查询（例：查「商标注册」时 §工作流 因正文词频高排第一，
    # 真正的 §17 反而被压到第二）。检索层的职责是定位 references/ 与 memory/ 里的知识，
    # 所以这两类不进索引——树里仍保留，方便人看。
    NOT_SEARCHABLE = {"memory/design-log.md", "SKILL.md"}
    searchable = [
        {**f, "sections": []} if f["path"] in NOT_SEARCHABLE else f for f in files
    ]
    index = {
        "generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "files": searchable,
        "wiring": check,
    }
    MEM.mkdir(parents=True, exist_ok=True)
    (MEM / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8"
    )

    if "--check" in sys.argv:
        print(f"文件 {len(files)} · 章节 {sum(len(f['sections']) for f in files)}")
        print("未接线:", check["未接线"] or "无")
        print("已失联:", check["已失联"] or "无")
        return

    (MEM / "tree.md").write_text(build_tree(files, check), encoding="utf-8")
    print(f"[完成] {len(files)} 文件 / {sum(len(f['sections']) for f in files)} 章节")
    print("  memory/index.json")
    print("  memory/tree.md")
    if check["未接线"]:
        print("  ⚠️ 未接线:", ", ".join(check["未接线"]))


if __name__ == "__main__":
    main()
