"""Pinned upstream inventory, capability mappings, and task workflow templates."""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / 'registry' / (name + '.json')).read_text(encoding='utf-8'))


LOCK = load('dependencies.lock')
SOURCES = load('upstream-capabilities')
CAPABILITIES = load('capability-registry')
ROUTING = load('routing-registry')
ENTRIES = ROUTING['entries']
ROUTES = ROUTING['routes']
COVERAGE = load('coverage')


class TrellisError(Exception):
    """Expected, actionable failure."""


def entry_name(name):
    name = name.removeprefix('trellis-')
    if name not in ENTRIES:
        raise TrellisError('Unknown entry: ' + name)
    return name


def validate():
    errors = []
    if len(ENTRIES) != 8 or len(LOCK) != 5:
        errors.append('Public contract requires exactly eight entries and five providers')
    for key, obj in LOCK.items():
        if not re.fullmatch(r'[a-f0-9]{40}', obj['commit']):
            errors.append(f'Unpinned commit: {key}')
        expected = {v['path'] for v in SOURCES.values() if v['provider'] == key and v['path'].endswith('/SKILL.md')}
        if expected != set(obj['skill_files']):
            errors.append(f'Skill inventory mismatch: {key}')
    if set(SOURCES) != set(COVERAGE):
        errors.append('Upstream coverage entries do not match inventory')
    for key, obj in SOURCES.items():
        if obj['provider'] not in LOCK or key != obj['provider']+':'+obj['path']:
            errors.append('Invalid source: '+key)
        cov = COVERAGE.get(key, {})
        if cov.get('route') not in ROUTES or cov.get('primary') not in SOURCES:
            errors.append('Unmapped source: '+key)
        elif SOURCES[cov['primary']]['capability'] != obj['capability']:
            errors.append('Wrong capability family: '+key)
    for k, route in ROUTES.items():
        if route['entry'] not in ENTRIES or not k.startswith(route['entry']+'.'):
            errors.append('Invalid route entry: '+k)
        seen = set()
        for step in route['steps']:
            if step['id'] in seen:
                errors.append('Duplicate step: '+k+':'+step['id'])
            seen.add(step['id'])
            for p in step['providers']:
                if p not in SOURCES:
                    errors.append('Unknown provider source: '+p)
            if step['kind'] == 'gate' and not step.get('gate'):
                errors.append('Unnamed gate: '+k)
    if errors:
        raise TrellisError('\n'.join(errors))
    return {'entries': len(ENTRIES), 'providers':len(LOCK), 'registered_resources':len(SOURCES),
            'skill_files':sum(len(x['skill_files']) for x in LOCK.values()),
            'capability_families':len(CAPABILITIES['primary']), 'routes':len(ROUTES),
            'unmapped_registered_resources':0, 'note':'Structural inventory mapping only; native execution parity requires host integration tests.'}


def catalog(entry):
    e = entry_name(entry)
    return {k:{'title':v['title'],'examples':v['examples'],'requires':v['requires']} for k,v in ROUTES.items() if v['entry']==e}


def compose(entry, route_ids):
    """Compose selected templates in caller-specified order; never remove gates.

    The host LLM selects routes semantically from catalog, not keyword matching.
    Cross-entry selection must be explicitly redirected in chat before calling.
    """
    e = entry_name(entry)
    if not route_ids:
        raise TrellisError('Select one or more routes from the entry catalog')
    if len(route_ids) != len(set(route_ids)):
        raise TrellisError('Do not repeat routes')
    steps=[]; requires=[]; produced=set()
    for key in route_ids:
        route=ROUTES.get(key)
        if not route or route['entry'] != e:
            raise TrellisError(f'Route {key!r} not in {e}; select/redirect to the appropriate entry')
        for need in route['requires']:
            if need not in produced and need not in requires:
                requires.append(need)
        for s in route['steps']:
            steps.append(dict(s, id=key+'/'+s['id'], route=key))
            if s['kind']=='gate':
                produced.add(s['gate'])
    return {'entry':e,'routes':route_ids,'requires':requires,'steps':steps}
