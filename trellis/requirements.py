"""Optional Markdown checks and explicit one-time v0.1 migration."""
import json
import re
import hashlib
import shutil
from pathlib import Path
from datetime import date
from .registry import ROOT,TrellisError

RAW='docs/requirements/raw-requirements.md'
FUNC='docs/requirements/functional-requirements.md'
OP_ONLY=re.compile(r'^[`\s]*[$/]?trellis-(?:init|requirements|design|contract|dev|accept|audit|simpler)[`\s]*$')

def cell(text):
    return str(text).replace('&','&amp;').replace('|','&#124;').replace('<','&lt;').replace('>','&gt;').replace('\r','').replace('\n','<br>')

def bootstrap(root):
    root=Path(root).resolve()
    if (root/'.trellis/state.json').exists(): raise TrellisError('Legacy state exists; inspect migrate-requirements first')
    created=[]
    for rel in (RAW,FUNC):
        dest=root/rel
        if not dest.exists():
            dest.parent.mkdir(parents=True,exist_ok=True)
            with dest.open('x',encoding='utf-8') as f:f.write((ROOT/'templates'/dest.name).read_text())
            created.append(rel)
    return {'created':created,'note':'Existing documents preserved.'}

def rows(text):
    for line in text.splitlines():
        if line.lstrip().startswith('|'):
            yield [x.strip() for x in re.split(r'(?<!\\)\|',line.strip()[1:-1])]

def check(root):
    root=Path(root); errors=[]; raw={}; funcs=set()
    for row in rows((root/RAW).read_text()):
        if not row or not re.match(r'^R-',row[0]):continue
        rid=row[0]
        if not re.fullmatch(r'R-\d{3,}',rid) or rid in raw:errors.append('Invalid/duplicate raw ID '+rid)
        if len(row)!=2:errors.append('Expected two raw columns '+rid);continue
        m=re.search(r'[（(](\d{4}-\d{2}-\d{2})[）)]$',row[1]); desc=row[1][:m.start()].strip() if m else row[1]
        try:
            if not m:raise ValueError()
            date.fromisoformat(m.group(1))
        except ValueError:errors.append('Missing/invalid last edit date '+rid)
        if not desc or (OP_ONLY.fullmatch(desc.strip('~ ')) and not desc.startswith('~~')):errors.append('Empty or operation-only raw requirement '+rid)
        if desc.startswith('~~')!=desc.endswith('~~'):errors.append('Unbalanced deletion strike '+rid)
        raw[rid]=desc.startswith('~~') and desc.endswith('~~')
    for row in rows((root/FUNC).read_text()):
        if not row or not re.match(r'^F\d',row[0]):continue
        fid=row[0]
        if not re.fullmatch(r'F\d{2,}-\d{3,}',fid) or fid in funcs:errors.append('Invalid/duplicate functional ID '+fid)
        funcs.add(fid)
        if len(row)!=5:errors.append('Expected five functional columns '+fid);continue
        refs=re.findall(r'R-\d{3,}',row[2])
        if not refs or any(r not in raw for r in refs):errors.append('Missing raw link '+fid)
        if refs and all(raw.get(r,False) for r in refs) and '取消' not in row[4]:errors.append('Only cancelled raw links '+fid)
    return {'ok':not errors,'raw':len(raw),'functional':len(funcs),'errors':errors}

def migrate(root,apply=False):
    root=Path(root).resolve(); legacy=root/'.trellis/state.json'; state=json.loads(legacy.read_text())
    if state.get('schema')!=1:raise TrellisError('Unsupported legacy schema')
    backup=root/'.trellis/v0.1-backup'
    if backup.exists():raise TrellisError('Migration backup already exists; do not repeat')
    for rel in (RAW,FUNC):
        f=root/rel; expected=state.get('views',{}).get(rel)
        if f.exists() and (not expected or hashlib.sha256(f.read_bytes()).hexdigest()!=expected):raise TrellisError('Existing document changed; reconcile manually: '+rel)
    superseded={i:r['time'][:10] for r in state['raw'] for i in r.get('supersedes',[])}
    referenced={r for f in state['functional'].values() for r in f['raw_ids']}
    raw=['# 原始需求','','| 序号 | 需求描述 |','|---|---|']; omitted=[]
    for r in state['raw']:
        rid=r['id']; desc=cell(r['text']); day=superseded.get(rid,r['time'][:10])
        if OP_ONLY.fullmatch(r['text'].strip()) and rid not in referenced:omitted.append(rid);continue
        if rid in superseded or r['operation']=='delete' or OP_ONLY.fullmatch(r['text'].strip()):desc='~~'+desc+'~~'
        raw.append(f'| {rid} | {desc}（{day}） |')
    func=['# 功能需求','']
    for cat,code in state['categories'].items():
        func += [f'## {code} {cat}','','| 编号 | 功能点 | 原始来源 | 验收条件 | 状态 |','|---|---|---|---|---|']
        for fid,f in state['functional'].items():
            if f['category']!=cat:continue
            status={'proposed':'待确认','confirmed':'已确认','cancelled':'已取消'}.get(f['status'],f['status'])
            if f.get('derived') and status=='待确认':status+='（AI推导）'
            func.append('| '+' | '.join(map(cell,[fid,f['text'],', '.join(f['raw_ids']),f['acceptance'],status]))+' |')
        func.append('')
    result={'applied':apply,'omitted_operation_ids':omitted,'highest_legacy_id':max((int(r['id'].split('-')[1]) for r in state['raw']),default=0),'raw_preview':'\n'.join(raw)+'\n','functional_preview':'\n'.join(func)+'\n','note':'Legacy state and evidence retained; review historical links and approvals manually; do not reuse omitted IDs.'}
    if apply:
        backup.mkdir(parents=True)
        for rel in (RAW,FUNC):
            if (root/rel).exists():shutil.copy2(root/rel,backup/Path(rel).name)
        shutil.copy2(legacy,backup/'state.json')
        for rel,key in ((RAW,'raw_preview'),(FUNC,'functional_preview')):
            f=root/rel;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(result[key],encoding='utf-8')
        legacy.rename(backup/'retired-state.json')
    return result
