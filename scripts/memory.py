#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""design-partner 用户层记忆工具：记录用户信号、统计、晋升候选与校验。

只记录、不推断：没有真实反馈就记 none，绝不替用户编偏好。
子命令：add / stats / promote / apply / validate，详见 `python scripts/memory.py -h`；add 示例：
退出码：0 成功；1 校验失败、参数错误或用户取消。
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import date, datetime
from difflib import SequenceMatcher
from pathlib import Path

SIGNALS = ("explicit_preference", "correction", "accept", "none", "process")
REAL_SIGNALS = ("explicit_preference", "correction", "accept")
JOURNAL_FIELDS = ("date", "task", "carrier", "user_quote", "signal_type",
                  "decision", "outcome", "closed_at", "evidence_ref")
DOMAIN_KEYWORDS = {
    "布局": ("布局", "栅格", "网格", "版式", "响应式", "断点", "留白", "间距", "对齐", "层级", "首屏", "滚动", "页面结构"),
    "字体排印": ("字体", "字号", "行高", "排印", "字距", "中英混排", "标点", "可变字体", "字重", "行长"),
    "色彩": ("色彩", "配色", "色板", "对比度", "暗色", "深色", "渐变", "主题色", "颜色"),
    "动效": ("动效", "动画", "过渡", "缓动", "微交互", "滚动动画", "帧率"),
    "组件": ("组件", "表单", "表格", "按钮", "输入", "弹窗", "对话框", "下拉", "导航", "菜单", "标签页", "图标", "播放器", "上传", "选择器"),
    "内容": ("文案", "写作", "语气", "空状态", "通知", "邮件", "本地化", "国际", "翻译", "错误信息", "引导"),
    "合规": ("合规", "无障碍", "隐私", "同意", "授权", "发票", "定价", "税", "许可", "cookie"),
    "流程": ("流程", "评审", "交接", "度量", "研究", "规范", "维护", "发布", "升级"),
}

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
REF_RE = re.compile(
    r"^(?P<file>design-log\.md|archive/design-log-v51\.md|journal\.jsonl):"
    r"(?P<a>\d+)(?:-(?P<b>\d+))?$")


def say(text=""):
    print(text)


def die(message):
    print("错误：" + message, file=sys.stderr)
    return 1


def default_root():
    return Path(__file__).resolve().parent.parent


def journal_path(root):
    return Path(root) / "memory" / "journal.jsonl"


def profile_path(root):
    return Path(root) / "memory" / "profile.md"


def load_journal(root):
    """逐行读取 journal，返回 [(行号, 记录), ...]；格式错误抛 ValueError。"""
    path = journal_path(root)
    if not path.exists():
        raise ValueError("找不到 " + str(path))
    rows = []
    with path.open(encoding="utf-8") as handle:
        for number, line in enumerate(handle, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError("journal 第 %d 行不是合法 JSON：%s" % (number, exc))
            if not isinstance(rec, dict):
                raise ValueError("journal 第 %d 行不是对象" % number)
            rows.append((number, rec))
    return rows


def guess_domain(*texts):
    blob = " ".join(t for t in texts if t)
    best, hits = "未分类", 0
    for domain, words in DOMAIN_KEYWORDS.items():
        count = sum(1 for word in words if word in blob)
        if count > hits:
            best, hits = domain, count
    return best


def normalize_decision(text):
    return re.sub(r"[\s，。；、：！？,.;:!?（）()\[\]「」【】\"'“”‘’—\-]+", "", text or "").lower()


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio() >= 0.7


def check_date(value, where):
    if value is None:
        return None
    if not isinstance(value, str) or not DATE_RE.match(value):
        return "%s 日期格式应为 YYYY-MM-DD" % where
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return "%s 不是有效日期：%s" % (where, value)
    return None


def resolve_range(root, ref):
    """校验 evidence_ref 指向的文件与行号是否存在，返回错误文本或 None。"""
    match = REF_RE.match(ref or "")
    if not match:
        return "evidence_ref 格式应为 journal.jsonl:N 或 design-log.md:A-B：" + str(ref)
    name, start, end = match.group("file"), int(match.group("a")), int(match.group("b") or match.group("a"))
    if start < 1 or end < start:
        return "evidence_ref 行号不合法：" + ref
    memory = Path(root) / "memory"
    candidates = [memory / name]
    if name == "design-log.md":
        candidates.append(memory / "archive" / "design-log-v51.md")
    target = next((p for p in candidates if p.exists()), None)
    if target is None:
        return "evidence_ref 指向的文件不存在：" + ref
    total = sum(1 for _ in target.open(encoding="utf-8"))
    if end > total:
        return "evidence_ref 超出文件行数（%d 行）：%s" % (total, ref)
    return None


def command_add(root, args):
    task = (args.task or "").strip()
    decision = (args.decision or "").strip()
    if not task:
        return die("--task 不能为空")
    if args.signal not in SIGNALS:
        return die("--signal 只能是：" + " / ".join(SIGNALS))
    if not decision:
        return die("--decision 不能为空（没有决策就记 none，不要编）")
    quote = args.quote.strip() if args.quote else None
    if args.signal == "none" and quote:
        return die("signal=none 表示没有真实反馈，不应带 --quote")
    if args.signal in ("explicit_preference", "correction") and not quote:
        return die("signal=%s 必须带 --quote（用户原话或转述）" % args.signal)
    day = args.date or date.today().isoformat()
    err = check_date(day, "--date")
    if err:
        return die(err)
    rows = load_journal(root) if journal_path(root).exists() else []
    rec = {
        "date": day,
        "task": task,
        "carrier": (args.carrier or "（未记录）").strip(),
        "user_quote": quote,
        "signal_type": args.signal,
        "decision": decision,
        "outcome": (args.outcome or "待观察").strip(),
        "closed_at": None,
        "evidence_ref": "journal.jsonl:%d" % (len(rows) + 1),
    }
    with journal_path(root).open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(rec, ensure_ascii=False) + "\n")
    say("已追加 journal 第 %d 条：%s" % (len(rows) + 1, json.dumps(rec, ensure_ascii=False)))
    return 0


def command_stats(root, args):
    rows = load_journal(root)
    signals = Counter(rec.get("signal_type") for _, rec in rows)
    domains = Counter(guess_domain(rec.get("task"), rec.get("decision")) for _, rec in rows)
    real = sum(signals.get(sig, 0) for sig in REAL_SIGNALS)
    unclosed = sum(1 for _, rec in rows if not rec.get("closed_at"))
    say("总条数：%d" % len(rows))
    say("signal_type 分布：")
    for sig in SIGNALS:
        say("  %-20s %d" % (sig, signals.get(sig, 0)))
    say("真实信号数（explicit_preference + correction + accept）：%d" % real)
    say("未闭环数（closed_at 为空）：%d" % unclosed)
    say("域分布：")
    for domain, count in domains.most_common():
        say("  %-8s %d" % (domain, count))
    if real == 0:
        say("提示：还没有真实用户信号，profile.md 应保持空状态。")
    return 0


def command_promote(root, args):
    rows = load_journal(root)
    buckets = defaultdict(list)
    for number, rec in rows:
        if rec.get("signal_type") not in ("explicit_preference", "correction"):
            continue
        domain = guess_domain(rec.get("task"), rec.get("decision"))
        placed = False
        for candidate in buckets[domain]:
            if similar(normalize_decision(rec.get("decision")), candidate["key"]):
                candidate["items"].append((number, rec))
                candidate["key"] = normalize_decision(rec.get("decision"))
                placed = True
                break
        if not placed:
            buckets[domain].append({"key": normalize_decision(rec.get("decision")),
                                    "items": [(number, rec)]})
    candidates = []
    for domain, group in buckets.items():
        for candidate in group:
            if len(candidate["items"]) >= 2:
                candidates.append((domain, candidate["items"]))
    if not candidates:
        say("没有候选：需要同一域下同一决策至少有 2 条 explicit_preference / correction。")
        return 0
    for index, (domain, items) in enumerate(candidates, 1):
        rule = max((rec.get("decision") or "" for _, rec in items), key=len)
        numbers = [str(number) for number, _ in items]
        say("候选 %d/%d" % (index, len(candidates)))
        say("  域：%s" % domain)
        say("  规则草案：%s" % rule)
        say("  证据（%d 条）：" % len(items))
        for number, rec in items:
            say("    - journal.jsonl:%d  %s  %s" % (number, rec.get("date"), rec.get("task")))
        say("  应用：python scripts/memory.py apply --rule \"%s\" --domain %s --evidence %s"
            % (rule, domain, ",".join(numbers)))
        say()
    return 0


def split_profile(text):
    """把 profile 拆成 (标题前, 「当前规则」正文, 之后的文本)。"""
    marker = "## 当前规则"
    start = text.find(marker)
    if start < 0:
        return text, "", ""
    head = text[:start]
    body_start = start + len(marker)
    tail_start = text.find("\n## ", body_start)
    if tail_start < 0:
        return head, text[body_start:], ""
    return head, text[body_start:tail_start], text[tail_start:]


def parse_rules(section):
    rules = []
    for line in section.splitlines():
        line = line.strip()
        if not line.startswith("|") or set(line) <= set("|- "):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != 6 or cells[0] == "rule":
            continue
        rules.append({
            "rule": cells[0], "domain": cells[1], "first_seen": cells[2],
            "confirmations": cells[3], "evidence_refs": cells[4], "status": cells[5],
        })
    return rules


def render_section(rules):
    if not rules:
        return ("\n\n**空。** 没有规则达到晋升条件。\n\n")
    lines = ["", "| rule | domain | first_seen | confirmations | evidence_refs | status |",
             "| --- | --- | --- | --- | --- | --- |"]
    for rule in rules:
        safe = rule["rule"].replace("|", "／")
        lines.append("| %s | %s | %s | %s | %s | %s |" % (
            safe, rule["domain"], rule["first_seen"], rule["confirmations"],
            rule["evidence_refs"], rule["status"]))
    lines.append("")
    return "\n".join(lines) + "\n"


def command_apply(root, args):
    rule = re.sub(r"\s+", " ", (args.rule or "")).strip()
    domain = (args.domain or "").strip()
    if not rule:
        return die("--rule 不能为空")
    if not domain:
        return die("--domain 不能为空")
    try:
        numbers = [int(part) for part in args.evidence.replace("，", ",").split(",") if part.strip()]
    except ValueError:
        return die("--evidence 应形如 3,7")
    if not numbers:
        return die("--evidence 不能为空")
    rows = load_journal(root)
    by_number = dict(rows)
    picked = []
    for number in numbers:
        if number not in by_number:
            return die("evidence journal.jsonl:%d 不存在" % number)
        if by_number[number].get("signal_type") not in REAL_SIGNALS:
            return die("journal.jsonl:%d 不是真实信号，不能作为证据" % number)
        picked.append((number, by_number[number]))
    picked.sort(key=lambda item: item[1].get("date") or "")
    refs = ",".join("journal.jsonl:%d" % number for number, _ in picked)
    profile = profile_path(root)
    text = profile.read_text(encoding="utf-8") if profile.exists() else "# 用户画像\n"
    head, section, tail = split_profile(text)
    if not head and not tail:
        return die("profile.md 缺少「## 当前规则」章节")
    rules = parse_rules(section)
    if any(item["rule"] == rule for item in rules):
        return die("规则已存在：" + rule)
    if not args.yes:
        if not sys.stdin.isatty():
            return die("写入 profile 需要显式确认：请在终端运行，或确认后加 --yes。")
        answer = input("确认把该规则写入 profile.md？[y/N] ").strip().lower()
        if answer not in ("y", "yes"):
            say("已取消，未写入。")
            return 1
    rules.append({
        "rule": rule, "domain": domain,
        "first_seen": "journal.jsonl:%d" % picked[0][0],
        "confirmations": str(len(picked)), "evidence_refs": refs, "status": "active",
    })
    profile.write_text(head + "## 当前规则" + render_section(rules) + tail, encoding="utf-8")
    say("已写入 profile.md：%s（证据 %s）" % (rule, refs))
    return 0


def command_validate(root, args):
    problems = []
    try:
        rows = load_journal(root)
    except ValueError as exc:
        return die(str(exc))
    seen_dates = []
    for number, rec in rows:
        where = "journal 第 %d 行" % number
        missing = [field for field in JOURNAL_FIELDS if field not in rec]
        if missing:
            problems.append("%s 缺字段：%s" % (where, ",".join(missing)))
        if not str(rec.get("task") or "").strip():
            problems.append("%s task 为空" % where)
        if rec.get("signal_type") not in SIGNALS:
            problems.append("%s signal_type 非法：%s" % (where, rec.get("signal_type")))
        err = check_date(rec.get("date"), where)
        if err:
            problems.append(err)
        else:
            seen_dates.append(rec["date"])
        quote = rec.get("user_quote")
        if quote is not None and not isinstance(quote, str):
            problems.append("%s user_quote 应为字符串或 null" % where)
        if rec.get("signal_type") == "none" and quote:
            problems.append("%s signal=none 却带 user_quote" % where)
        err = check_date(rec.get("closed_at"), where + " closed_at")
        if err:
            problems.append(err)
        err = resolve_range(root, rec.get("evidence_ref"))
        if err:
            problems.append("%s %s" % (where, err))
    profile = profile_path(root)
    if not profile.exists():
        problems.append("缺少 memory/profile.md")
    else:
        text = profile.read_text(encoding="utf-8")
        if len(text.splitlines()) > 80:
            problems.append("profile.md 超过 80 行（当前 %d 行）" % len(text.splitlines()))
        _, section, _ = split_profile(text)
        for rule in parse_rules(section):
            numbers = []
            for ref in rule["evidence_refs"].split(","):
                match = re.match(r"^journal\.jsonl:(\d+)$", ref.strip())
                if not match:
                    problems.append("profile 规则「%s」证据格式错误：%s" % (rule["rule"], ref))
                    continue
                number = int(match.group(1))
                numbers.append(number)
                if number not in dict(rows):
                    problems.append("profile 规则「%s」引用了不存在的 journal.jsonl:%d"
                                    % (rule["rule"], number))
                elif dict(rows)[number].get("signal_type") not in REAL_SIGNALS:
                    problems.append("profile 规则「%s」引用的 journal.jsonl:%d 不是真实信号"
                                    % (rule["rule"], number))
            if rule["confirmations"] != str(len(numbers)):
                problems.append("profile 规则「%s」confirmations=%s 与证据数 %d 不符"
                                % (rule["rule"], rule["confirmations"], len(numbers)))
            if rule["status"] not in ("active", "weakened", "retired"):
                problems.append("profile 规则「%s」status 非法：%s" % (rule["rule"], rule["status"]))
    if problems:
        say("validate: 失败，共 %d 个问题" % len(problems))
        for problem in problems:
            say("  - " + problem)
        return 1
    say("validate: 通过（journal %d 行，日期 %s → %s，profile 规则 %d 条）"
        % (len(rows), min(seen_dates or ["-"]), max(seen_dates or ["-"]),
           len(parse_rules(split_profile(profile.read_text(encoding="utf-8"))[1]))))
    return 0


def build_parser():
    parser = argparse.ArgumentParser(
        prog="memory.py",
        description="design-partner 用户层记忆工具：采集 journal、统计、晋升候选与校验。",
        epilog="典型顺序：add 记录 → stats 看总量 → promote 找候选 → apply 经确认写 profile → validate。")
    parser.add_argument("--root", default=str(default_root()),
                        help="仓库根目录，默认为脚本上级目录")
    sub = parser.add_subparsers(dest="command", metavar="命令")

    add = sub.add_parser("add", help="追加一条 journal 记录")
    add.add_argument("--task", required=True, help="任务名，不能为空")
    add.add_argument("--signal", default="none", choices=SIGNALS, help="signal_type 取值")
    add.add_argument("--quote", help="用户原话；explicit_preference / correction 必填")
    add.add_argument("--decision", required=True, help="用户要什么或本轮决定")
    add.add_argument("--date", help="日期 YYYY-MM-DD，默认今天")
    add.add_argument("--carrier", help="本轮落地的工件，默认「（未记录）」")
    add.add_argument("--outcome", default="待观察", help="效果，默认「待观察」")
    add.set_defaults(func=command_add)

    stats = sub.add_parser("stats", help="统计条数、signal 分布、未闭环与域分布")
    stats.set_defaults(func=command_stats)

    promote = sub.add_parser("promote", help="扫描 journal，输出 ≥2 条证据的画像候选（不写入）")
    promote.set_defaults(func=command_promote)

    apply_cmd = sub.add_parser("apply", help="经显式确认后把规则写入 profile.md")
    apply_cmd.add_argument("--rule", required=True, help="规则一句话")
    apply_cmd.add_argument("--domain", required=True, help="域：布局 / 字体排印 / 色彩 / …")
    apply_cmd.add_argument("--evidence", required=True, help="journal 行号，如 3,7")
    apply_cmd.add_argument("--yes", action="store_true", help="跳过交互确认（仅在已确认后使用）")
    apply_cmd.set_defaults(func=command_apply)

    check = sub.add_parser("validate", help="校验 journal JSON、字段、日期与 profile 引用")
    check.set_defaults(func=command_validate)
    return parser


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "func", None):
        parser.print_help()
        return 1
    try:
        return args.func(Path(args.root).resolve(), args)
    except ValueError as exc:
        return die(str(exc))
    except FileNotFoundError as exc:
        return die("找不到文件：%s" % exc)


if __name__ == "__main__":
    sys.exit(main())
