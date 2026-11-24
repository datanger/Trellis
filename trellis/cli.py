"""Command-line interface used by the eight agent skills and human reviewers."""
import argparse
import json
import sys
from pathlib import Path
from .registry import TrellisError, validate, catalog, compose, COVERAGE, SOURCES, ROOT
from .engine import Project
from . import deps
from .install import install


def make_parser():
    p=argparse.ArgumentParser(description='Trellis — Grow with structure.')
    p.add_argument('--project',default='.',help='Target project root (before subcommand)')
    sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('version');sub.add_parser('validate');sub.add_parser('coverage')
    c=sub.add_parser('catalog');c.add_argument('entry')
    c=sub.add_parser('compose');c.add_argument('entry');c.add_argument('--route',action='append',required=True)
    c=sub.add_parser('install');c.add_argument('--host',choices=['codex','claude','both'],default='both');c.add_argument('--scope',choices=['user','project'],default='user');c.add_argument('--target',default=None,help='Project root for project scope');c.add_argument('--offline',action='store_true');c.add_argument('--replace',action='store_true')
    c=sub.add_parser('deps');c.add_argument('action',choices=['sync','doctor','resolve']);c.add_argument('key',nargs='?')
    sub.add_parser('bootstrap');sub.add_parser('status');sub.add_parser('guard')
    c=sub.add_parser('raw-add');g=c.add_mutually_exclusive_group(required=True);g.add_argument('--text');g.add_argument('--text-file');c.add_argument('--source',required=True);c.add_argument('--operation',choices=['add','modify','delete','clarify'],default='add');c.add_argument('--supersedes',action='append',default=[])
    c=sub.add_parser('functional-upsert');c.add_argument('--category',required=True);c.add_argument('--text',required=True);c.add_argument('--raw',action='append',required=True);c.add_argument('--acceptance',required=True);c.add_argument('--id');c.add_argument('--derived',action='store_true')
    c=sub.add_parser('confirm-functional');c.add_argument('--id',required=True);c.add_argument('--gate',required=True);c.add_argument('--cancel',action='store_true')
    c=sub.add_parser('start');c.add_argument('entry');c.add_argument('--route',action='append',required=True);c.add_argument('--request',required=True);c.add_argument('--scope',required=True);c.add_argument('--allow',action='append',default=[])
    for name in ('next','preflight','cancel-run'):
        c=sub.add_parser(name);c.add_argument('run')
    c=sub.add_parser('complete');c.add_argument('run');c.add_argument('--evidence',action='append',default=[]);c.add_argument('--gate');c.add_argument('--receipt')
    c=sub.add_parser('propose');c.add_argument('--scope',required=True);c.add_argument('--stage',required=True);c.add_argument('--file',action='append',required=True);c.add_argument('--summary',required=True);c.add_argument('--run')
    c=sub.add_parser('decide');c.add_argument('gate');c.add_argument('--token',required=True);c.add_argument('--by',required=True);c.add_argument('--decision',choices=['approve','reject'],required=True);c.add_argument('--reason',default='')
    c=sub.add_parser('authorize-change');c.add_argument('run');c.add_argument('--gate',required=True);c.add_argument('--file',action='append',required=True)
    c=sub.add_parser('test');c.add_argument('--timeout',type=int,default=300);c.add_argument('argv',nargs=argparse.REMAINDER)
    c=sub.add_parser('baseline');c.add_argument('--scope',required=True);c.add_argument('--gate',required=True);c.add_argument('--receipt',action='append',required=True);c.add_argument('--file',action='append',required=True);c.add_argument('--policy',required=True)
    c=sub.add_parser('policy');c.add_argument('simplification',choices=['lite','full','ultra','off'])
    return p


def main(argv=None):
    a=make_parser().parse_args(argv); cmd=a.command
    try:
        if cmd=='version':out={'version':(ROOT/'VERSION').read_text().strip()}
        elif cmd=='validate':out=validate()
        elif cmd=='coverage':out={'summary':validate(),'coverage':COVERAGE}
        elif cmd=='catalog':out=catalog(a.entry)
        elif cmd=='compose':out=compose(a.entry,a.route)
        elif cmd=='install':out=install(a.host,a.scope,a.target or a.project,a.offline,a.replace)
        elif cmd=='deps':
            out=deps.sync() if a.action=='sync' else deps.doctor() if a.action=='doctor' else deps.resolve(a.key)
            if a.action=='doctor' and not out['ready']:
                print(json.dumps(out,ensure_ascii=False,indent=2));return 2
        else:
            p=Project(a.project)
            with p.locked(create=cmd in ('bootstrap','start')):
                if cmd=='bootstrap':out=p.bootstrap()
                elif cmd=='status':out=p.status()
                elif cmd=='guard':out=p.guard()
                elif cmd=='raw-add':out=p.raw_add(a.text if a.text is not None else Path(a.text_file).read_text(encoding='utf-8'),a.source,a.operation,a.supersedes)
                elif cmd=='functional-upsert':out=p.functional_upsert(a.category,a.text,a.raw,a.acceptance,a.derived,a.id)
                elif cmd=='confirm-functional':out=p.confirm_functional(a.id,a.gate,a.cancel)
                elif cmd=='start':
                    # Start may create metadata, never rewrite existing project files by default.
                    out=p.start(a.entry,a.route,a.request,a.scope,a.allow)
                elif cmd=='next':out=p.next(a.run)
                elif cmd=='preflight':out=p.preflight(a.run)
                elif cmd=='cancel-run':
                    r=p.run(a.run);r['status']='cancelled';r.pop('initial_files',None);p.event('run-cancelled',run=a.run);p.save();out=p.next(a.run)
                elif cmd=='complete':out=p.complete(a.run,a.evidence,a.gate,a.receipt)
                elif cmd=='propose':out=p.propose(a.scope,a.stage,a.file,a.summary,a.run)
                elif cmd=='decide':out=p.decide(a.gate,a.token,a.by,a.decision,a.reason)
                elif cmd=='authorize-change':out=p.authorize_change(a.run,a.gate,a.file)
                elif cmd=='test':out=p.test(a.argv[1:] if a.argv and a.argv[0]=='--' else a.argv,a.timeout)
                elif cmd=='baseline':out=p.baseline(a.scope,a.gate,a.receipt,a.file,a.policy)
                elif cmd=='policy':p.state['policy']['simplification']=a.simplification;p.save();out=p.state['policy']
                else:raise TrellisError('Unimplemented command')
        print(json.dumps(out,ensure_ascii=False,indent=2))
        if cmd=='guard' and not out['ok']:return 3
        if cmd=='test' and out['exit_code']!=0:return 1
        return 0
    except (TrellisError,OSError,ValueError,KeyError,TypeError) as e:
        print(json.dumps({'status':'blocked','error':str(e)},ensure_ascii=False),file=sys.stderr);return 2
