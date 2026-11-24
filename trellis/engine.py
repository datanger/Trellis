"""Small durable workflow engine. No model API, no arbitrary shell execution."""
import contextlib
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import tempfile
import uuid
from pathlib import Path
from .registry import TrellisError, compose, ROUTES, SOURCES


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')


def dump(x):
    return json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+'\n'


def digest(b):
    return hashlib.sha256(b).hexdigest()


def obj_digest(x):
    return digest(dump(x).encode())


def atomic(path, text):
    path.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix='.'+path.name+'.',dir=path.parent)
    try:
        with os.fdopen(fd,'w',encoding='utf-8') as f:
            f.write(text); f.flush(); os.fsync(f.fileno())
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)


def clean_scope(scope):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,79}',scope):
        raise TrellisError('Scope must be a stable ASCII identifier (e.g. F01-001, parser, project)')
    return scope


def markdown_cell(text):
    return str(text).replace('&','&amp;').replace('|','&#124;').replace('<','&lt;').replace('>','&gt;').replace('\n','<br>').replace('\r','')


class Project:
    def __init__(self, root):
        self.root=Path(root).expanduser().resolve()
        if not self.root.is_dir(): raise TrellisError('Project directory does not exist: '+str(root))
        self.dir=self.root/'.trellis'
        if self.dir.is_symlink(): raise TrellisError('.trellis may not be a symlink')
        self.statefile=self.dir/'state.json'
        self.state=None

    @contextlib.contextmanager
    def locked(self, create=False):
        self.dir.mkdir(exist_ok=True)
        lock=self.dir/'lock'
        try: fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
        except FileExistsError: raise TrellisError('Project locked; another Trellis process may be active. Remove stale lock only after verifying it is inactive.')
        try:
            os.write(fd,str(os.getpid()).encode()); os.close(fd)
            if self.statefile.exists():
                self.state=json.loads(self.statefile.read_text(encoding='utf-8'))
                if self.state.get('schema')!=1: raise TrellisError('Unsupported state schema')
            elif create:
                self.state={'schema':1,'raw':[],'functional':{},'categories':{},'gates':{},'runs':{},'baselines':{},'baseline_history':[],'views':{},'events':[],'policy':{'simplification':'full'},'change_grants':{}}
            else: raise TrellisError('Project not initialized: run bootstrap or trellis-init')
            yield self
        finally:
            lock.unlink(missing_ok=True)

    def save(self): atomic(self.statefile,dump(self.state))

    def event(self,kind,**fields):
        self.state['events'].append(dict(time=now(),kind=kind,**fields))

    def path(self,rel):
        p=Path(rel)
        if p.is_absolute() or '..' in p.parts or p==Path('.'):
            raise TrellisError('Expected a contained project-relative file: '+str(rel))
        q=self.root/p
        if not q.resolve().is_relative_to(self.root) or q.is_symlink():
            raise TrellisError('Unsafe path: '+str(rel))
        return q

    def filehash(self,rel,missing=False):
        q=self.path(rel)
        if not q.is_file():
            if missing and not q.exists(): return None
            raise TrellisError('Expected file: '+str(rel))
        return digest(q.read_bytes())

    def snapshot(self,files,missing=False):
        if not files: raise TrellisError('Explicit artifact paths required')
        return {Path(f).as_posix():self.filehash(f,missing=missing) for f in sorted(set(files))}

    def git(self,args,check=True):
        r=subprocess.run(['git',*args],cwd=self.root,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120)
        if check and r.returncode: raise TrellisError('Git failed: '+r.stderr.decode(errors='replace').strip())
        return r

    def head(self):
        r=self.git(['rev-parse','HEAD'],check=False)
        return r.stdout.decode().strip() if r.returncode==0 else None

    def tree_files(self):
        r=self.git(['ls-files','-z','--cached','--others','--exclude-standard'])
        files=[os.fsdecode(f) for f in r.stdout.split(b'\0') if f and not os.fsdecode(f).startswith('.trellis/')]
        # Protect against links to out-of-project files. In-repo symbolic links are represented by the link target string.
        hashes={}
        for f in sorted(set(files)):
            p=self.root/f
            if p.is_symlink(): hashes[f]='symlink:'+os.readlink(p)
            elif p.is_file() and p.resolve().is_relative_to(self.root): hashes[f]=digest(p.read_bytes())
            elif not p.exists(): hashes[f]=None
            else: hashes[f]='non-file'
        return hashes

    def tree_snapshot(self):
        return obj_digest(self.tree_files())

    def clean_code(self):
        return not self.git(['status','--porcelain','-z','--untracked-files=all','--','.',':(exclude).trellis/**']).stdout

    def check_views(self):
        for p, h in self.state['views'].items():
            if self.filehash(p,missing=True)!=h:
                raise TrellisError(f'Generated requirement view changed outside Trellis: {p}. Reconcile/backup before regenerating; no silent overwrite.')

    def render_requirements(self):
        raw_path='docs/requirements/raw-requirements.md'; f_path='docs/requirements/functional-requirements.md'
        self.check_views()
        for name in (raw_path,f_path):
            if name not in self.state['views'] and self.path(name).exists():
                raise TrellisError('Existing requirement document must be migrated explicitly before generation: '+name)
        raw=['# 原始需求 / Raw requirements','', '> 用户原始输入及来源。通过 Trellis 命令追加；不要直接覆盖历史。','']
        superseded={i for r in self.state['raw'] for i in r['supersedes']}
        for r in self.state['raw']:
            raw += [f"## {r['id']}", '',f"- 来源：{markdown_cell(r['source'])}",f"- 时间：{r['time']}",f"- 操作：{r['operation']}",f"- 状态：{'已被后续请求替代' if r['id'] in superseded else '已记录'}",f"- 替代：{', '.join(r['supersedes']) or '—'}",'',*[f'> {line}' for line in r['text'].split('\n')],'']
        func=['# 功能需求 / Functional requirements','','> 按业务分类；每项关联 R 编号。通过 Trellis 命令更新；Git 保存历史。','']
        for cat,code in self.state['categories'].items():
            func.extend([f'## {code} {cat}','','| 编号 | 功能点 | 原始来源 | 验收条件 | 状态 |','|---|---|---|---|---|'])
            for fid,f in self.state['functional'].items():
                if f['category']!=cat: continue
                origin=', '.join(f['raw_ids'])+('（AI推导）' if f['derived'] else '')
                func.append('| '+' | '.join(markdown_cell(x) for x in [fid,f['text'],origin,f['acceptance'],f['status']])+' |')
            func.append('')
        for p,lines in [(raw_path,raw),(f_path,func)]:
            atomic(self.path(p),'\n'.join(lines)+'\n'); self.state['views'][p]=self.filehash(p)

    def bootstrap(self):
        self.render_requirements(); self.event('bootstrap'); self.save()
        return {'state':str(self.statefile),'documents':list(self.state['views'])}

    def raw_add(self,text,source,operation='add',supersedes=()):
        if not text.strip() or not source.strip(): raise TrellisError('Nonempty original text and source required')
        known={r['id'] for r in self.state['raw']}
        if not set(supersedes)<=known: raise TrellisError('Unknown superseded raw ID')
        if operation in ('modify','delete') and not supersedes: raise TrellisError('Specify prior raw IDs for modify/delete')
        for r in self.state['raw']:
            if (r['text'],r['source'],r['operation'],r['supersedes'])==(text,source,operation,list(supersedes)): return r
        self.check_views()
        r={'id':f'R-{len(self.state["raw"])+1:04d}','text':text,'source':source,'operation':operation,'supersedes':list(supersedes),'time':now()}
        self.state['raw'].append(r); self.render_requirements(); self.event('raw-added',id=r['id']); self.save(); return r

    def functional_upsert(self,category,text,raw_ids,acceptance,derived=False,fid=None,status='proposed'):
        if '\n' in category or '\r' in category or not category.strip() or not text.strip() or not acceptance.strip(): raise TrellisError('Category, functional behavior and acceptance criteria required')
        if not raw_ids or not set(raw_ids)<={r['id'] for r in self.state['raw']}: raise TrellisError('Functional point needs valid original IDs')
        self.check_views()
        old=None
        if fid:
            old=self.state['functional'].get(fid)
            if not old: raise TrellisError('Unknown functional ID')
            if old['category']!=category: raise TrellisError('Category is stable; create linked replacement rather than renumbering')
        else:
            code=self.state['categories'].setdefault(category,f'F{len(self.state["categories"])+1:02d}')
            n=1+sum(f['category']==category for f in self.state['functional'].values())
            fid=f'{code}-{n:03d}'
        if status=='confirmed': raise TrellisError('Use confirm-functional after explicit requirements approval')
        if status=='cancelled': raise TrellisError('Use a proposed change followed by confirm-functional --cancel after approval')
        self.state['functional'][fid]={'category':category,'text':text,'raw_ids':list(dict.fromkeys(raw_ids)),'acceptance':acceptance,'derived':bool(derived),'status':'proposed','time':now()}
        self.render_requirements(); self.event('functional-proposed',id=fid,previous=old); self.save(); return {'id':fid,**self.state['functional'][fid]}

    def confirm_functional(self,fid,gate_id,cancel=False):
        f=self.state['functional'].get(fid)
        if not f: raise TrellisError('Unknown functional ID')
        # Gate bound to actual generated functional document and exact scope (or project-wide scope).
        g=self.require_gate(gate_id,stage='requirements')
        if g['scope'] not in (fid,'project') or 'docs/requirements/functional-requirements.md' not in g['files']:
            raise TrellisError('Requirements gate must explicitly cover this functional point and document')
        self.check_views(); f['status']='cancelled' if cancel else 'confirmed'; f['approval']=gate_id
        self.render_requirements()
        # Confirming changes only status metadata in the generated view. Rebind the approved view
        # while keeping the original approval evidence and invalidating downstream gates as appropriate.
        g['confirmed_view']=self.filehash('docs/requirements/functional-requirements.md')
        self.event('functional-confirmed',id=fid,status=f['status'],gate=gate_id)
        for other in self.state['gates'].values():
            if other['stage'] in ('design','contract','skeleton','plan','acceptance') and other['scope'] in (fid,'project') and other['status']=='approved':
                other['status']='superseded'; other['reason']='Functional requirements changed'
        self.save(); return {'id':fid,**f}

    def gate_current(self,g):
        if g['status']!='approved': return False
        for path,h in g['files'].items():
            expected=g.get('confirmed_view',h) if path=='docs/requirements/functional-requirements.md' else h
            if self.filehash(path,missing=True)!=expected:return False
        return True

    def require_gate(self,gate_id,stage=None,scope=None):
        g=self.state['gates'].get(gate_id)
        if not g or (stage and g['stage']!=stage) or (scope and g['scope']!=scope) or not self.gate_current(g):
            raise TrellisError('Approval missing, wrong scope/stage, superseded or stale: '+str(gate_id))
        return g

    def latest_gate(self,scope,stage):
        # Latest proposal wins; never fall back to an earlier approval when newer one is pending/rejected.
        found=[g for g in self.state['gates'].values() if g['scope']==scope and g['stage']==stage]
        if not found: raise TrellisError(f'{scope}: missing {stage} approval')
        return self.require_gate(max(found,key=lambda g:g['sequence'])['id'],stage,scope)

    def propose(self,scope,stage,files,summary,run=None,step=None):
        clean_scope(scope)
        if stage not in ('init','requirements','design','contract','skeleton','plan','acceptance','change','cleanup','evaluation','ui','configuration','external'):
            raise TrellisError('Unknown approval stage')
        if not summary.strip(): raise TrellisError('Proposal summary required')
        snap=self.snapshot(files); gid='G-'+uuid.uuid4().hex[:12]
        if run:
            r=self.run(run); s=self.current(r)
            if not s or s['kind']!='gate' or s['gate']!=stage or r['scope']!=scope or (step and s['id']!=step): raise TrellisError('Gate must match current workflow step and scope')
            step=s['id']
        g={'id':gid,'scope':scope,'stage':stage,'files':snap,'summary':summary,'run':run,'step':step,'sequence':len(self.state['gates'])+1,'status':'pending','created':now()}
        g['token']=obj_digest(g)[:16]
        self.state['gates'][gid]=g; self.event('gate-proposed',id=gid); self.save(); return g

    def decide(self,gid,token,by,decision,reason=''):
        g=self.state['gates'].get(gid)
        if not g or g['status']!='pending' or token!=g['token'] or not by.strip(): raise TrellisError('Invalid pending gate, approval token or approver')
        if self.snapshot(g['files'])!=g['files']:raise TrellisError('Proposal artifacts changed: create a new gate')
        g.update(status='approved' if decision=='approve' else 'rejected',by=by,decided=now(),reason=reason)
        if decision=='approve':
            for other in self.state['gates'].values():
                if other['id']!=gid and other['scope']==g['scope'] and other['stage']==g['stage'] and other['status']=='approved': other['status']='superseded'
        self.event('gate-decided',id=gid,decision=decision,by=by); self.save(); return g

    def start(self,entry,routes,request,scope,allowed=()):
        clean_scope(scope)
        if not request.strip(): raise TrellisError('Original task text is required')
        workflow=compose(entry,routes)
        prereq={s:self.latest_gate(scope,s)['id'] for s in workflow['requires']}
        rid='W-'+uuid.uuid4().hex[:12]
        r=dict(workflow,id=rid,request=request,scope=scope,allowed=list(allowed),prerequisites=prereq,cursor=0,status='active',history=[],created=now(),head=self.head(),initial_files=self.tree_files() if self.head() else None)
        for f in allowed: self.path(f)
        self.state['runs'][rid]=r; self.event('workflow-started',id=rid); self.save(); return self.next(rid)

    def run(self,rid):
        r=self.state['runs'].get(rid)
        if not r: raise TrellisError('Unknown workflow: '+rid)
        return r

    def current(self,r): return r['steps'][r['cursor']] if r['cursor']<len(r['steps']) else None

    def next(self,rid):
        r=self.run(rid); s=self.current(r)
        out={'id':rid,'scope':r['scope'],'request':r['request'],'status':r['status'],'progress':f"{r['cursor']}/{len(r['steps'])}",'allowed':r['allowed'],'current':s,'prerequisites':r['prerequisites']}
        if s:
            out['providers']=[{'key':k,**SOURCES[k]} for k in s['providers']]
            out['pending_gates']=[g for g in self.state['gates'].values() if g.get('run')==rid and g.get('step')==s['id'] and g['status'] in ('pending','approved')]
        return out

    def authorize_change(self,rid,gate_id,files):
        r=self.run(rid); g=self.require_gate(gate_id,stage='change',scope=r['scope'])
        if not files:raise TrellisError('Exact protected paths required')
        if not set(files)<=set(g['files']):raise TrellisError('Approved change gate must include all target files')
        protected={p for b in self.state['baselines'].values() for p in b['files']}
        if not set(files)<=protected:raise TrellisError('Change authorization is only for exact protected files')
        if self.guard()['changed']:raise TrellisError('Restore or reconcile existing baseline changes before approving new ones')
        grant={'gate':gate_id,'files':self.snapshot(files),'scope':r['scope'],'time':now()}
        # Gate hashes are immutable approval evidence. Target bytes may subsequently change;
        # the grant, not a stale gate, is used for editing. New acceptance is still mandatory.
        self.state.setdefault('change_grants',{})[rid]=grant
        self.event('change-authorized',run=rid,gate=gate_id);self.save();return grant

    def scope_violations(self,r):
        if r.get('initial_files') is None or not r['allowed']:return []
        old=r['initial_files']; new=self.tree_files()
        changed={p for p in set(old)|set(new) if old.get(p)!=new.get(p)}
        return sorted(p for p in changed if not any(p==a or p.startswith(a.rstrip('/')+'/') for a in r['allowed']))

    def preflight(self,rid):
        r=self.run(rid); s=self.current(r)
        if r['status']!='active' or not s: raise TrellisError('Workflow not active')
        for stage,gid in r['prerequisites'].items(): self.require_gate(gid,stage,r['scope'])
        if s['mutates'] and r['entry'] in ('dev','simpler','contract') and not r['allowed']:
            raise TrellisError('Mutating work requires explicit allowed paths in start')
        if r['entry'] in ('dev','simpler','contract'):
            violations=self.scope_violations(r)
            if violations:raise TrellisError('Out-of-scope changes: '+str(violations))
            grant=self.state.get('change_grants',{}).get(rid,{})
            permitted=set(grant.get('files',{}))
            violations=[v for v in self.guard()['changed'] if v['path'] not in permitted or v.get('reason')]
            if violations:raise TrellisError("Accepted baseline changed without this run's authorization: "+str(violations))
        from .deps import resolve
        out=self.next(rid)
        out['resolved_providers']=[resolve(k) for k in s['providers']]
        return out

    def complete(self,rid,evidence=(),gate_id=None,receipt=None):
        r=self.run(rid); s=self.current(r)
        if r['status']!='active' or not s: raise TrellisError('No active step')
        self.preflight(rid)
        record={'step':s['id'],'time':now()}
        if s['kind']=='gate':
            g=self.require_gate(gate_id,s['gate'],r['scope'])
            if g.get('run')!=rid or g.get('step')!=s['id']:raise TrellisError('Approval is not bound to this workflow step')
            matching=[x for x in self.state['gates'].values() if x.get('run')==rid and x.get('step')==s['id']]
            if g['sequence']!=max(x['sequence'] for x in matching):raise TrellisError('A newer proposal supersedes this step approval')
            record['gate']=gate_id
        else:
            record['evidence']=self.snapshot(evidence)
            if s['kind']=='verify':
                if not receipt: raise TrellisError('Verification step requires an actual Trellis test receipt')
                rec=self.read_receipt(receipt)
                if rec['exit_code']!=0: raise TrellisError('Verification failed; do not advance')
                if rec['before']!=rec['after'] or rec['after']!=self.tree_snapshot(): raise TrellisError('Test receipt is stale or code changed during test')
                record['receipt']=receipt
        r['history'].append(record); r['cursor']+=1
        if self.current(r) is None:
            r['status']='done'; r['initial_tree']=obj_digest(r.pop('initial_files',None))
        self.event('step-completed',run=rid,step=s['id']); self.save(); return self.next(rid)

    def test(self,argv,timeout=300):
        if not argv or timeout<1 or timeout>86400:raise TrellisError('Explicit test argv and valid timeout required')
        before=self.tree_snapshot(); head=self.head(); tid='T-'+uuid.uuid4().hex[:12]; log=self.dir/'logs'/f'{tid}.log'; log.parent.mkdir(exist_ok=True)
        started=now(); result=None
        with log.open('wb') as out:
            try:
                result=subprocess.run(argv,cwd=self.root,stdout=out,stderr=subprocess.STDOUT,timeout=timeout,check=False)
                code=result.returncode
            except subprocess.TimeoutExpired:
                code=124; out.write(b'\nTrellis: timeout\n')
            except OSError as e:
                code=127; out.write(str(e).encode())
        rec={'id':tid,'argv':argv,'start':started,'end':now(),'exit_code':code,'head':head,'before':before,'after':self.tree_snapshot(),'log':str(log.relative_to(self.root)),'log_hash':digest(log.read_bytes())}
        dest=self.dir/'receipts'/f'{tid}.json'; atomic(dest,dump(rec)); self.event('test-run',id=tid,exit_code=code); self.save()
        return {'receipt':str(dest.relative_to(self.root)),**rec}

    def read_receipt(self,rel):
        q=self.path(rel)
        if q.parent!=self.dir/'receipts':raise TrellisError('Expected Trellis-generated test receipt')
        rec=json.loads(q.read_text(encoding='utf-8'))
        if rec['id']+'.json'!=q.name or not any(e.get('kind')=='test-run' and e.get('id')==rec['id'] and e.get('exit_code')==rec['exit_code'] for e in self.state['events']):raise TrellisError('Receipt not recorded by Trellis test runner')
        if self.filehash(rec['log'],missing=True)!=rec['log_hash']:
            # Local logs are intentionally not committed; imported receipts need preserved evidence for review.
            raise TrellisError('Missing or changed local test log; rerun the approved command')
        return rec

    def baseline(self,scope,gate_id,receipt_paths,files,policy):
        clean_scope(scope); g=self.require_gate(gate_id,'acceptance',scope)
        if not self.head() or not self.clean_code():raise TrellisError('Baseline requires a committed code/docs/test tree; commit reviewed work before final test and approval')
        if not receipt_paths:raise TrellisError('At least one approved actual test receipt required')
        criteria=json.loads(self.path(policy).read_text(encoding='utf-8'))
        commands=criteria.get('commands'); protect=criteria.get('protect')
        if not isinstance(commands,list) or not commands or not all(isinstance(c,list) and c and all(isinstance(a,str) and a for a in c) for c in commands):
            raise TrellisError('Acceptance policy requires nonempty commands (argv arrays)')
        if not isinstance(protect,list) or not protect or not all(isinstance(f,str) for f in protect):raise TrellisError('Acceptance policy requires protected paths')
        if not (set(protect)|{policy})<=set(files):raise TrellisError('Baseline must protect all policy paths and policy itself')
        snap=self.snapshot(files)
        for f,h in snap.items():
            if g['files'].get(f)!=h:raise TrellisError('Protected file not included in acceptance approval: '+f)
        tree=self.tree_snapshot(); head=self.head()
        executed=[]
        for path in receipt_paths:
            if g['files'].get(path)!=self.filehash(path):raise TrellisError('Receipt not included in approval: '+path)
            r=self.read_receipt(path); executed.append(tuple(r['argv']))
            if r['exit_code']!=0 or r['head']!=head or r['before']!=tree or r['after']!=tree:raise TrellisError('Receipt must pass on the same committed, unchanged tree')
        if not {tuple(c) for c in commands}<=set(executed):raise TrellisError('Missing approved acceptance commands; every policy command needs a passing receipt')
        previous=self.state['baselines'].get(scope)
        if previous:
            missing=set(previous['files'])-set(snap)
            if missing:raise TrellisError('Cannot silently drop previously protected files: '+str(sorted(missing)))
            self.state['baseline_history'].append(previous)
        for f in snap:
            if self.git(['ls-files','--error-unmatch','--',f],check=False).returncode:
                raise TrellisError('Protected file is not tracked by Git: '+f)
        b={'scope':scope,'policy':policy,'commit':head,'tree':tree,'files':snap,'approval':gate_id,'receipts':{p:self.filehash(p) for p in receipt_paths},'time':now()}
        self.state['baselines'][scope]=b; self.event('baseline-recorded',scope=scope,commit=head); self.save();return b

    def guard(self):
        changed=[]
        for scope,b in self.state['baselines'].items():
            for f,h in b['files'].items():
                if self.filehash(f,missing=True)!=h: changed.append({'scope':scope,'path':f,'baseline':b['commit']})
            for f,h in b['receipts'].items():
                if self.filehash(f,missing=True)!=h:changed.append({'scope':scope,'path':f,'baseline':b['commit'],'reason':'acceptance evidence changed'})
        return {'ok':not changed,'changed':changed,'baseline_count':len(self.state['baselines'])}

    def status(self):
        return {'raw_count':len(self.state['raw']),'functional':{k:v['status'] for k,v in self.state['functional'].items()},'active_workflows':[self.next(k) for k,v in self.state['runs'].items() if v['status']=='active'],'pending_gates':[g for g in self.state['gates'].values() if g['status']=='pending'],'baselines':{k:v['commit'] for k,v in self.state['baselines'].items()},'guard':self.guard(),'policy':self.state['policy']}
