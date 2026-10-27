"""Create a separate private workspace without Git history or personal data."""
from pathlib import Path
import argparse
import shutil
ROOT = Path(__file__).resolve().parent.parent

def initialize(destination):
    dest = destination.expanduser().resolve()
    if dest == ROOT or dest.is_relative_to(ROOT):
        raise ValueError('destination must be outside the public template repository')
    dest.mkdir(parents=True, exist_ok=False)
    for name in ('README.md', 'LICENSE', 'AGENTS.md', 'Agent 知识库.md', 'index/projects.json', 'index/local-paths.example.json', 'memory/记忆首页.md', '.gitignore'):
        target = dest/name; target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT/name, target)
    for name in ('workflows', 'templates', 'tools', 'docs', 'examples'):
        shutil.copytree(ROOT/name, dest/name, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    for name in ('memory/项目', 'memory/日记', 'memory/决策与经验', 'memory/导航', 'audit', 'archive'):
        (dest/name).mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT/'templates/obsidian', dest/'memory/.obsidian')
    notes = dest/'memory/模板'
    notes.mkdir(parents=True, exist_ok=True)
    for name in ('项目.md', '经验.md'):
        shutil.copyfile(ROOT/'templates'/name, notes/name)
    daily = (ROOT/'templates/日记.md').read_text().replace('# YYYY-MM-DD', '# {{date:YYYY-MM-DD}}')
    (notes/'日记.md').write_text(daily)
    (dest/'memory/附件').mkdir(exist_ok=True)
    (dest/'index/local-paths.json').write_text('[]\n')
    print(f'Private workspace created: {dest}')
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', type=Path, required=True)
    args = parser.parse_args()
    try: initialize(args.destination)
    except (OSError, ValueError) as exc: parser.exit(1, f'Initialization failed: {exc}\n')
