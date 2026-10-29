#!/usr/bin/env python3
"""Prune old Vercel deployments to reclaim team deployment storage.

Vercel's free tier counts every deployment artifact toward a team-wide 10 GB cap.
Only the newest few matter; older ones are reachable again by redeploying from git.

Usage:
  python3 scripts/vercel-prune.py                 # dry run, all projects except the-signal, keep 2
  python3 scripts/vercel-prune.py --apply         # actually delete
  python3 scripts/vercel-prune.py --apply --include-live
  python3 scripts/vercel-prune.py --apply --only kmarie-braids-website,stock
  python3 scripts/vercel-prune.py --apply --keep 1
"""
import argparse, json, pathlib, sys, time, urllib.error, urllib.request

ENV_PATH = pathlib.Path('/home/chino/.hermes/profiles/yachty/.env')
PROJECT_JSON = pathlib.Path('/home/chino/thesignal/.vercel/project.json')
# The live site runs its own weekly prune; leave it alone unless --include-live.
LIVE_PROJECTS = {'the-signal'}


def load_token() -> str:
    for line in ENV_PATH.read_text(errors='ignore').split('\n'):
        if line.startswith('VERCEL_TOKEN'):
            return line.split('=', 1)[1].strip().strip('"').strip("'")
    sys.exit('VERCEL_TOKEN not found in profile .env')


def api(path: str, method: str = 'GET', token: str = '', team: str = ''):
    sep = '&' if '?' in path else '?'
    url = f'https://api.vercel.com{path}{sep}teamId={team}'
    req = urllib.request.Request(url, method=method,
                                 headers={'Authorization': f'Bearer {token}',
                                          'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=60) as r:
        body = r.read()
    return json.loads(body) if body else {}


def all_deployments(pid: str, token: str, team: str):
    out, until = [], None
    for _ in range(20):
        q = f'/v6/deployments?projectId={pid}&limit=100'
        if until:
            q += f'&until={until}'
        d = api(q, token=token, team=team)
        batch = d.get('deployments', [])
        out.extend(batch)
        until = (d.get('pagination') or {}).get('next')
        if not until or not batch:
            break
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true', help='actually delete (default is dry run)')
    ap.add_argument('--keep', type=int, default=2, help='newest N deployments to keep per project')
    ap.add_argument('--only', default='', help='comma-separated project names')
    ap.add_argument('--include-live', action='store_true', help='also prune the-signal')
    a = ap.parse_args()

    token = load_token()
    proj = json.loads(PROJECT_JSON.read_text())
    team = proj['orgId']

    only = {s.strip() for s in a.only.split(',') if s.strip()}
    projects = api('/v9/projects?limit=100', token=token, team=team).get('projects', [])
    if only:
        projects = [p for p in projects if p['name'] in only]

    total_deleted = total_kept = 0
    errors = []
    for p in sorted(projects, key=lambda x: x['name']):
        name = p['name']
        if name in LIVE_PROJECTS and not a.include_live:
            print(f'  SKIP  {name:30s} (live site — run with --include-live to prune)')
            continue
        deps = all_deployments(p['id'], token, team)
        if len(deps) <= a.keep:
            print(f'  ok    {name:30s} {len(deps)} deployments — nothing to do')
            continue
        deps.sort(key=lambda d: d.get('created') or 0, reverse=True)
        keep, drop = deps[:a.keep], deps[a.keep:]
        print(f'  prune {name:30s} {len(deps)} -> {len(keep)} (deleting {len(drop)})')
        for d in drop:
            if not a.apply:
                total_deleted += 1
                continue
            try:
                api(f"/v13/deployments/{d['uid']}", method='DELETE', token=token, team=team)
                total_deleted += 1
            except urllib.error.HTTPError as e:
                errors.append(f'{name}/{d.get("uid")}: HTTP {e.code}')
            except Exception as e:
                errors.append(f'{name}/{d.get("uid")}: {type(e).__name__}')
            time.sleep(0.4)
        total_kept += len(keep)

    verb = 'Deleted' if a.apply else 'Would delete'
    print(f'\n{verb} {total_deleted} deployments; kept {total_kept}.')
    if errors:
        print(f'{len(errors)} errors:')
        for e in errors[:20]:
            print('   ', e)


if __name__ == '__main__':
    main()
