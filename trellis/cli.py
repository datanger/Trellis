"""Optional deterministic utilities; host agent owns execution."""
import argparse
import json
import sys
from .registry import TrellisError, validate, catalog, SOURCES, ROOT
from . import deps, requirements
from .install import install

def main(argv=None):
    p=argparse.ArgumentParser(description='Trellis — Grow with structure.')
    p.add_argument('--project',default='.')
    sub=p.add_subparsers(dest='command',required=True)
    for name in ('version','validate','coverage','bootstrap','requirements-check'):sub.add_parser(name)
    c=sub.add_parser('catalog');c.add_argument('entry')
    c=sub.add_parser('install');c.add_argument('--host',choices=['codex','claude','both'],default='both');c.add_argument('--scope',choices=['user','project'],default='user');c.add_argument('--target');c.add_argument('--offline',action='store_true');c.add_argument('--replace',action='store_true')
    c=sub.add_parser('deps');c.add_argument('action',choices=['sync','doctor','resolve']);c.add_argument('key',nargs='?')
    c=sub.add_parser('migrate-requirements');c.add_argument('--apply',action='store_true')
    a=p.parse_args(argv); cmd=a.command
    try:
        if cmd=='version':out={'version':(ROOT/'VERSION').read_text().strip()}
        elif cmd=='validate':out=validate()
        elif cmd=='coverage':out={'summary':validate(),'sources':SOURCES}
        elif cmd=='catalog':out=catalog(a.entry)
        elif cmd=='install':out=install(a.host,a.scope,a.target or a.project,a.offline,a.replace)
        elif cmd=='deps':out=deps.sync() if a.action=='sync' else deps.doctor() if a.action=='doctor' else deps.resolve(a.key)
        elif cmd=='bootstrap':out=requirements.bootstrap(a.project)
        elif cmd=='requirements-check':out=requirements.check(a.project)
        else:out=requirements.migrate(a.project,a.apply)
        print(json.dumps(out,ensure_ascii=False,indent=2))
        return 2 if out.get('ok') is False or out.get('ready') is False else 0
    except (TrellisError,OSError,ValueError,KeyError,TypeError) as e:
        print(json.dumps({'status':'blocked','error':str(e)},ensure_ascii=False),file=sys.stderr);return 2
