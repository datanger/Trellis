"""Fetch exact upstream commits into an isolated, non-discoverable directory.

Only git fetch/checkout is performed; no upstream hooks/installers are executed.
"""
import os
import subprocess
import tempfile
import shutil
from pathlib import Path
from .registry import LOCK, SOURCES, ROOT, TrellisError, validate


def git(args,cwd=None):
    env=dict(os.environ,GIT_TERMINAL_PROMPT='0',GIT_CONFIG_NOSYSTEM='1')
    # A user's global aliases/hooks must not execute during a dependency checkout.
    result=subprocess.run(['git','-c','core.hooksPath=/dev/null','-c','protocol.file.allow=never',*args],cwd=cwd,env=env,capture_output=True,text=True,timeout=240)
    if result.returncode:
        raise TrellisError('git '+ ' '.join(args[:2])+' failed: '+result.stderr.strip()[-2000:])
    return result.stdout.strip()


def dep_root():
    return ROOT/'upstream'


def checkout_ok(path, provider):
    obj=LOCK[provider]
    if not (path/'.git').exists():
        raise TrellisError(f'{provider}: missing pinned checkout; run deps sync')
    if git(['rev-parse','HEAD'],path)!=obj['commit']:
        raise TrellisError(f'{provider}: checkout differs from lock; reinstall exact version')
    if git(['status','--porcelain','--untracked-files=no'],path):
        raise TrellisError(f'{provider}: modified tracked upstream files')
    return path


def inventory(path, provider):
    actual=set(git(['ls-tree','-r','--name-only','HEAD'],path).splitlines())
    registered={v['path'] for v in SOURCES.values() if v['provider']==provider}
    expected_skills=set(LOCK[provider]['skill_files'])
    found_skills={s for s in actual if s.endswith('/SKILL.md') or s=='SKILL.md'}
    missing=sorted(registered-actual)
    added=sorted(found_skills-expected_skills)
    removed=sorted(expected_skills-found_skills)
    if missing or added or removed:
        raise TrellisError(f'{provider}: inventory mismatch; missing={missing}, new skills={added}, removed={removed}')
    # Files in registry must be ordinary, contained paths, not external symlinks.
    for filename in registered:
        f=path/filename
        if not f.is_file() or not f.resolve().is_relative_to(path.resolve()):
            raise TrellisError(f'{provider}: missing or unsafe source path {filename}')
    return {'commit':LOCK[provider]['commit'],'skills':len(found_skills),'registered_files':len(registered)}


def sync():
    validate()
    target=dep_root(); target.mkdir(parents=True,exist_ok=True)
    out={}
    for provider,obj in LOCK.items():
        dest=target/provider
        if dest.exists():
            out[provider]=inventory(checkout_ok(dest,provider),provider); continue
        # fetch the exact commit; fail closed if unavailable, never fall back to HEAD.
        with tempfile.TemporaryDirectory(prefix='.download-',dir=target) as tmp:
            path=Path(tmp)/provider; path.mkdir()
            git(['init','-q'],path)
            git(['remote','add','origin',obj['url']],path)
            git(['fetch','--depth','1','origin',obj['commit']],path)
            git(['checkout','--detach','--quiet','FETCH_HEAD'],path)
            out[provider]=inventory(checkout_ok(path,provider),provider)
            path.rename(dest)
    return out


def doctor():
    out={}; ok=True
    for provider in LOCK:
        try:
            out[provider]={'status':'ready',**inventory(checkout_ok(dep_root()/provider,provider),provider)}
        except (TrellisError, OSError, subprocess.SubprocessError) as e:
            out[provider]={'status':'blocked','reason':str(e)}; ok=False
    return {'ready':ok,'providers':out,'tools':{k:shutil.which(k) for k in ['git','python3','node','npm','uv','specify','codex','claude','gh']}}


def resolve(key):
    if key not in SOURCES:
        raise TrellisError('Unknown source: '+key)
    obj=SOURCES[key]; p=obj['provider']; root=checkout_ok(dep_root()/p,p)
    f=root/obj['path']
    if not f.is_file() or not f.resolve().is_relative_to(root.resolve()):
        raise TrellisError('Missing or unsafe upstream resource: '+str(f))
    return {**obj,'key':key,'file':str(f),'repository_root':str(root),'commit':LOCK[p]['commit']}
