"""Generate navigation, preserving project and daily source pages."""
from pathlib import Path
from urllib.parse import quote
from datetime import date
import json
import os
from validate import check
ROOT = Path(__file__).resolve().parent.parent

def link(label, target, parent):
    label = str(label).replace('|', '\\|').replace('[', '\\[').replace(']', '\\]').replace('\n', ' ')
    target = target.resolve()
    url = quote(os.path.relpath(target, parent)) if target.is_relative_to(ROOT) else target.as_uri()
    return f'[{label}]({url})'

def refresh():
    errors, warnings = check(ROOT)
    if errors: raise SystemExit('\n'.join(errors))
    for x in warnings: print('WARNING:', x)
    mem = ROOT/'memory'; nav = mem/'导航'; diary = mem/'日记'
    nav.mkdir(parents=True, exist_ok=True); diary.mkdir(parents=True, exist_ok=True)
    projects = json.loads((ROOT/'index/projects.json').read_text())['projects']
    lines = ['# 项目目录', '', '由 tools/refresh.py 生成；核验状态由维护者填写。', '', '| 项目 | 当前知识入口 | 核验状态 |', '|---|---|---|']
    pending = ['# 待复核知识', '']
    for p in projects:
        target = p.get('currentKnowledgeTarget')
        label = link(p['name'], ROOT/target, nav) if target else p['id']
        lines.append(f"| {label} | {'已登记' if target else '未登记'} | {p['knowledgeTargetStatus']} |")
        if p['knowledgeTargetStatus'] != 'verified': pending.append(f"- {p['id']}：权威入口待核验。")
    (nav/'项目目录.md').write_text('\n'.join(lines)+'\n')
    (nav/'待复核知识.md').write_text('\n'.join(pending)+'\n')
    years = {}
    for p in sorted(diary.glob('*/*/*.md')):
        try: day = date.fromisoformat(p.stem)
        except ValueError: continue
        if p.parent.name != f'{day.month:02}' or p.parent.parent.name != str(day.year): continue
        years.setdefault(p.parent.parent, {}).setdefault(p.parent, []).append(p)
    rl = ['# 日记', '', '由 tools/refresh.py 生成。', '']
    for year, months in sorted(years.items(), reverse=True):
        yi = year/f'{year.name}年日记.md'; yl = [f'# {year.name}年日记', '', link('全部日记', diary/'日记.md', year), '']
        for month, entries in sorted(months.items(), reverse=True):
            mi = month/f'{year.name}年{month.name}月日记.md'
            ml = [f'# {year.name}年{month.name}月日记', '', link('返回年份', yi, month), '']
            ml.extend('- '+link(p.stem, p, month) for p in reversed(entries))
            mi.write_text('\n'.join(ml)+'\n'); yl.append('- '+link(month.name+'月', mi, year))
        yi.write_text('\n'.join(yl)+'\n'); rl.append('- '+link(year.name+'年', yi, diary))
    (diary/'日记.md').write_text('\n'.join(rl)+'\n')
    print('Navigation refreshed.')
if __name__ == '__main__': refresh()
