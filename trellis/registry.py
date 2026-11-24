"""Capability inventory and semantic routing hints, not a workflow engine."""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
LOCK = json.loads((ROOT/'registry/dependencies.lock.json').read_text())
REGISTRY = json.loads((ROOT/'registry/capabilities.json').read_text())
ENTRIES = REGISTRY['entries']
SOURCES = REGISTRY['sources']
FAMILIES = REGISTRY['families']
HINTS = REGISTRY['task_hints']

class TrellisError(Exception):
    pass


def validate():
    errors = []
    if len(ENTRIES)!=8 or len(LOCK)!=5: errors.append('Expected eight entries and five providers')
    for provider,obj in LOCK.items():
        if not re.fullmatch('[a-f0-9]{40}',obj['commit']): errors.append('Unpinned '+provider)
        actual={v['path'] for v in SOURCES.values() if v['provider']==provider and v['path'].endswith('/SKILL.md')}
        if actual!=set(obj['skill_files']): errors.append('Inventory mismatch '+provider)
    for key,obj in SOURCES.items():
        family=FAMILIES.get(obj['capability'],{})
        if key!=obj['provider']+':'+obj['path'] or obj['provider'] not in LOCK or obj['entry'] not in ENTRIES or obj['primary']!=family.get('primary') or obj['primary'] not in SOURCES:
            errors.append('Unmapped '+key)
    for key,family in FAMILIES.items():
        if SOURCES.get(family['primary'],{}).get('capability')!=key or any(x not in SOURCES for x in family['complements']): errors.append('Invalid family '+key)
    for key,hint in HINTS.items():
        if hint['entry'] not in ENTRIES or any(x not in FAMILIES for x in hint['capabilities']): errors.append('Invalid hint '+key)
    if errors: raise TrellisError('\n'.join(errors))
    return {'entries':len(ENTRIES),'providers':len(LOCK),'registered_resources':len(SOURCES),'skill_files':sum(len(v['skill_files']) for v in LOCK.values()),'capability_families':len(FAMILIES),'task_hints':len(HINTS),'unmapped_registered_resources':0,'note':'Structural mapping; live host execution not proven.'}


def catalog(entry):
    entry=entry.removeprefix('trellis-')
    if entry not in ENTRIES: raise TrellisError('Unknown entry '+entry)
    keys={v['capability'] for v in SOURCES.values() if v['entry']==entry}
    hints={k:v for k,v in HINTS.items() if v['entry']==entry}
    keys.update(c for h in hints.values() for c in h['capabilities'])
    return {'entry':entry,'families':{k:{**FAMILIES[k],'resources':{s:{'summary':v['summary'],'mode':v['mode'],'disposition':v['disposition']} for s,v in SOURCES.items() if v['capability']==k}} for k in sorted(keys)},'task_hints':hints}
