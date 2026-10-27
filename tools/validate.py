"""Validate index structure and file availability; not factual accuracy."""
from pathlib import Path
import json
ROOT = Path(__file__).resolve().parent.parent

def check(root=ROOT):
    errors, warnings = [], []
    try:
        data = json.loads((root/'index/projects.json').read_text())
        if not isinstance(data, dict) or data.get('schemaVersion') != 2 or not isinstance(data.get('projects'), list):
            raise ValueError('expected schemaVersion=2 and projects list')
        policy = data.get('routingPolicy')
        if not isinstance(policy, str) or not (root/policy).is_file():
            errors.append('routingPolicy file missing')
        ids = set()
        for p in data['projects']:
            if not isinstance(p, dict):
                errors.append('project must be an object'); continue
            pid = p.get('id')
            if not isinstance(pid, str) or not pid or pid in ids:
                errors.append('id must be nonempty and unique'); continue
            ids.add(pid)
            if not isinstance(p.get('name'), str) or not p['name']:
                errors.append(f'{pid}: name required')
            aliases = p.get('aliases', [])
            if not isinstance(aliases, list) or any(not isinstance(x, str) for x in aliases):
                errors.append(f'{pid}: aliases must be strings')
            status = p.get('knowledgeTargetStatus')
            if status not in ('verified', 'unverified'):
                errors.append(f'{pid}: invalid knowledgeTargetStatus')
            target = p.get('currentKnowledgeTarget')
            if not (isinstance(target, str) and target and (root/target).is_file()):
                (errors if status == 'verified' else warnings).append(f'{pid}: knowledge target missing')
        local = root/'index/local-paths.json'
        if local.exists():
            paths = json.loads(local.read_text())
            if not isinstance(paths, list):
                raise ValueError('local-paths must be a list')
            mapped = set()
            for item in paths:
                if not isinstance(item, dict):
                    errors.append('path mapping must be an object'); continue
                pid, path = item.get('id'), item.get('localPath')
                if not isinstance(pid, str) or pid not in ids or pid in mapped:
                    errors.append('mapping id unknown or duplicate')
                if isinstance(pid, str): mapped.add(pid)
                if not isinstance(path, str) or not Path(path).is_absolute():
                    errors.append('localPath must be absolute')
                elif not Path(path).is_dir():
                    warnings.append(f'{pid}: local directory missing')
    except (OSError, ValueError, TypeError) as exc:
        errors.append(str(exc))
    return errors, warnings

if __name__ == '__main__':
    errors, warnings = check()
    for x in warnings: print('WARNING:', x)
    for x in errors: print('ERROR:', x)
    print(f'{len(errors)} error(s), {len(warnings)} warning(s)')
    raise SystemExit(bool(errors))
