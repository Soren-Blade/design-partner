#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""trim_audit.py — 季度裁剪判据的可执行形式（v74）。

背景：「删除 6 个月未被路由命中的资产」在本库不可执行——库龄 < 6 个月，
且 62/62 资产都在 SKILL.md §4 有路由行。本脚本把判据换成三条可测事实：

  R 未路由   : SKILL.md 第 4 节没有 `references/<file>` 引用行
  I 零入度   : 其它资产 / 附录 / 夹具 / SKILL 都不提这个文件名（含自身目录外）
  G 无夹具   : tests/golden/*.md 从没引用它

裁剪候选 = 未路由 或（零入度 且 无夹具）。按字符数升序处理：最小的先死，
代价最低；内容等重的先用合并、不用删除。

用法：
  python scripts/trim_audit.py            # 人类可读表 + 汇总
  python scripts/trim_audit.py --json     # 机器可读
  python scripts/trim_audit.py --fail-on-unrouted   # CI：有未路由资产则退出 1
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)


def read(p):
    with open(p, encoding='utf-8') as f:
        return f.read()


def main():
    golden = sorted(glob.glob('tests/golden/*.md'))
    golden_text = '\n'.join(read(p) for p in golden)
    appendix_text = '\n'.join(read(p) for p in sorted(glob.glob('references/appendix/*.md')))
    skill = read('SKILL.md')

    assets = sorted(glob.glob('references/*.md'))
    rows = []
    for path in assets:
        name = os.path.basename(path)
        body = read(path)
        others = '\n'.join(read(p) for p in assets if p != path) + '\n' + appendix_text + '\n' + golden_text
        routed = bool(re.search(r'references/' + re.escape(name), skill))
        indeg = len(re.findall(re.escape(name), others))
        in_golden = name in golden_text
        rows.append({
            'asset': name,
            'chars': len(body),
            'lines': body.count('\n') + 1,
            'routed': routed,
            'indeg': indeg,
            'golden': in_golden,
        })

    for r in rows:
        r['candidate'] = (not r['routed']) or (r['indeg'] == 0 and not r['golden'])

    total = sum(r['chars'] for r in rows)
    cands = sorted([r for r in rows if r['candidate']], key=lambda r: r['chars'])
    if '--json' in sys.argv:
        print(json.dumps({'assets': len(rows), 'chars': total, 'rows': rows,
                          'candidates': [c['asset'] for c in cands]}, ensure_ascii=False, indent=1))
    else:
        print(f'资产 {len(rows)} 份 · 合计 {total:,} 字符 · 候选 {len(cands)} 份')
        print(f'{"资产":<38}{"字符":>8}{"行":>6}  R I  G')
        for r in rows:
            flag = '是' if r['candidate'] else '  '
            print(f'{flag}{r["asset"]:<38}{r["chars"]:>8}{r["lines"]:>6}  '
                  f'{"✓" if r["routed"] else "✗"} {"0" if r["indeg"] == 0 else str(r["indeg"]):>2}  {"✓" if r["golden"] else "-"}')
        print('\n裁剪候选（最小先死）：')
        for c in cands:
            why = []
            if not c['routed']:
                why.append('未路由')
            if c['indeg'] == 0:
                why.append('零入度')
            if not c['golden']:
                why.append('无夹具')
            print(f'  - {c["asset"]}  {c["chars"]} 字符  [{" / ".join(why)}]')
        if not cands:
            print('  （无：所有资产都被路由且至少被引用一次——本轮无可裁剪项）')

    if '--fail-on-unrouted' in sys.argv:
        unrouted = [r['asset'] for r in rows if not r['routed']]
        if unrouted:
            print('FAIL 未路由资产：' + ', '.join(unrouted))
            return 1
        print('PASS 所有资产均有 SKILL 路由行')
    return 0


if __name__ == '__main__':
    sys.exit(main())
