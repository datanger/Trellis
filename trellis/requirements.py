"""Human-editable numbered Markdown; explicit, reviewed conversion of old formats."""
import hashlib
import json
import re
import shutil
from datetime import date
from html import unescape
from pathlib import Path
from .registry import ROOT, TrellisError

RAW = 'docs/requirements/raw-requirements.md'
FUNC = 'docs/requirements/functional-requirements.md'
OP_ONLY = re.compile(r'^[`\s]*[$/]?trellis-(?:init|requirements|design|contract|dev|accept|audit|simpler)[`\s]*$|^[`\s]*/plan[`\s]*$')
ITEM = re.compile(r'^(\d+)\.\s+(.+)$')
BULLET = re.compile(r'^(?:[-*+]\s+|\d+[.)]\s+)(.+)$')
STAMP = re.compile(r'(?:（(\d{4}-\d{2}-\d{2})）|\((\d{4}-\d{2}-\d{2})\))$')


def split_date(text):
    text = text.strip()
    m = STAMP.search(text)
    if not m:
        return text, None
    day = m.group(1) or m.group(2)
    try:
        date.fromisoformat(day)
    except ValueError:
        raise TrellisError('Invalid last-edit date: ' + day)
    return text[:m.start()].rstrip(), day


def item_error(text):
    try:
        desc, day = split_date(text)
    except TrellisError as e:
        return str(e)
    if not day:
        return 'Missing last-edit date (YYYY-MM-DD)'
    if desc.startswith('~~') != desc.endswith('~~'):
        return 'Unbalanced deletion strike'
    plain = desc[2:-2].strip() if desc.startswith('~~') and desc.endswith('~~') else desc
    if not plain or OP_ONLY.fullmatch(plain):
        return 'Empty or operation-only requirement'
    return None


def inspect(text, functional=False):
    errors, count, expected, category = [], 0, 1, False
    for lineno, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        if not line or re.fullmatch(r'#\s+.+', line):
            continue
        if functional and re.fullmatch(r'##\s+.+', line):
            expected, category = 1, True
            continue
        m = ITEM.fullmatch(line)
        if not m:
            errors.append(f'Line {lineno}: use an ordered list, not a table, bullet or metadata block')
            continue
        count += 1
        if functional and not category:
            errors.append(f'Line {lineno}: functional item needs a category heading (##)')
        if int(m.group(1)) != expected:
            errors.append(f'Line {lineno}: expected number {expected}')
        expected += 1
        err = item_error(m.group(2))
        if err:
            errors.append(f'Line {lineno}: {err}')
    return count, errors


def bootstrap(root):
    root = Path(root).resolve()
    if (root/'.trellis/state.json').exists():
        raise TrellisError('Legacy state exists; inspect migrate-requirements first')
    created = []
    for rel in (RAW, FUNC):
        dest = root/rel
        if not dest.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
            with dest.open('x', encoding='utf-8') as f:
                f.write((ROOT/'templates'/dest.name).read_text(encoding='utf-8'))
            created.append(rel)
    return {'created': created, 'note': 'Existing documents preserved.'}


def check(root):
    root = Path(root)
    errors, counts = [], []
    for rel, functional in ((RAW, False), (FUNC, True)):
        path = root/rel
        if not path.is_file():
            counts.append(0)
            errors.append('Missing document: ' + rel)
            continue
        count, found = inspect(path.read_text(encoding='utf-8'), functional)
        counts.append(count)
        errors.extend(f'{rel}: {err}' for err in found)
    return {'ok': not errors, 'raw': counts[0], 'functional': counts[1], 'errors': errors}


def table_cells(line):
    return [unescape(s.strip().replace(r'\|', '|').replace('<br>', ' '))
            for s in re.split(r'(?<!\\)\|', line.strip()[1:-1])]


def render(groups, title, functional=False):
    lines = [f'# {title}', '']
    for category, items in groups.items():
        if functional:
            lines.extend([f'## {category}', ''])
        for i, (text, day) in enumerate(items, 1):
            lines.append(f'{i}. {text}（{day}）')
        lines.append('')
    return '\n'.join(lines).rstrip() + '\n'


def add(groups, category, text, stamp, cancelled, report, origin):
    desc, day = split_date(' '.join(str(text).splitlines()))
    day = day or stamp
    if OP_ONLY.fullmatch(desc.strip('~ ')):
        report['omitted_operations'].append(origin)
        return
    if not day:
        day = report['migration_date']
        report['dates_assigned'].append(origin)
    if cancelled and not (desc.startswith('~~') and desc.endswith('~~')):
        desc = '~~' + desc + '~~'
    err = item_error(f'{desc}（{day}）')
    if err:
        raise TrellisError(f'{origin}: {err}')
    groups.setdefault(category, []).append((desc, day))


def from_markdown(text, functional, report):
    """Convert known legacy tables or simple lists; refuse unknown prose/structures."""
    groups, category = {}, None if functional else ''
    table_width = 5 if functional else 2
    for lineno, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        origin = ('functional' if functional else 'raw') + f':{lineno}'
        if not line or re.fullmatch(r'#\s+.+', line):
            continue
        if functional and re.fullmatch(r'##\s+.+', line):
            category = re.sub(r'^F\d+\s+', '', line[3:].strip())
            groups.setdefault(category, [])
            continue
        if line == '按业务分类维护；每项关联原始需求编号。' and functional:
            continue
        if line.startswith('|') and line.endswith('|'):
            row = table_cells(line)
            if len(row) == table_width and (row[0] in ('序号', '编号') or all(re.fullmatch(r':?-+:?', s) for s in row)):
                continue
            if len(row) != table_width or not re.fullmatch(r'F\d+-\d+' if functional else r'R-\d+', row[0]):
                raise TrellisError('Unrecognized legacy table row: ' + origin)
            if category is None:
                raise TrellisError('Functional row outside category: ' + origin)
            if functional:
                status = row[4]
                report['legacy_functional_metadata'].append({'id': row[0], 'category': category, 'description': row[1], 'raw_links': row[2], 'acceptance': row[3], 'status': status})
                if status.startswith('待确认') or status == 'proposed':
                    report['pending_functional'].append(row[0])
                    continue
                if status not in ('已确认', '已取消', 'confirmed', 'cancelled'):
                    raise TrellisError('Unrecognized functional status: ' + status)
                add(groups, category, row[1], None, status in ('已取消', 'cancelled'), report, row[0])
            else:
                add(groups, category, row[1], None, False, report, row[0])
            continue
        m = BULLET.fullmatch(line)
        if not m or category is None:
            raise TrellisError('Unrecognized content; review manually: ' + origin)
        add(groups, category, m.group(1), None, False, report, origin)
    return groups


def from_state(root, state, report):
    if state.get('schema') != 1:
        raise TrellisError('Unsupported legacy schema')
    for rel in (RAW, FUNC):
        f = root/rel
        expected = state.get('views', {}).get(rel)
        if f.exists() and (not expected or hashlib.sha256(f.read_bytes()).hexdigest() != expected):
            raise TrellisError('Existing document changed; reconcile manually: ' + rel)
    raw, functional = {}, {}
    superseded = {i: r['time'][:10] for r in state['raw'] for i in r.get('supersedes', [])}
    for r in state['raw']:
        rid = r['id']
        if r['operation'] == 'delete':
            report['omitted_operations'].append(rid)
            continue
        add(raw, '', r['text'], superseded.get(rid, r['time'][:10]), rid in superseded, report, rid)
    for fid, f in state['functional'].items():
        report['legacy_functional_metadata'].append({'id': fid, **f})
        status = f['status']
        if status == 'proposed':
            report['pending_functional'].append(fid)
            continue
        if status not in ('confirmed', 'cancelled'):
            raise TrellisError('Unrecognized functional status: ' + status)
        add(functional, f['category'], f['text'], f.get('time', '')[:10] or None, status == 'cancelled', report, fid)
    return raw, functional


def migrate(root, apply=False):
    root = Path(root).resolve()
    legacy = root/'.trellis/state.json'
    report = {'migration_date': date.today().isoformat(), 'omitted_operations': [], 'dates_assigned': [],
              'pending_functional': [], 'legacy_functional_metadata': []}
    if legacy.exists():
        raw, functional = from_state(root, json.loads(legacy.read_text(encoding='utf-8')), report)
        backup = root/'.trellis/v0.1-backup'
    else:
        if not (root/RAW).is_file() or not (root/FUNC).is_file():
            raise TrellisError('Both existing requirement documents are needed; do not invent missing content')
        if check(root)['ok']:
            return {'applied': False, 'note': 'Already in numbered-list format; no changes needed.'}
        raw = from_markdown((root/RAW).read_text(encoding='utf-8'), False, report)
        functional = from_markdown((root/FUNC).read_text(encoding='utf-8'), True, report)
        backup = root/'.trellis/requirements-list-backup'
    if backup.exists():
        raise TrellisError('Migration backup already exists; review it before migrating again')
    result = {'applied': apply, 'raw_preview': render(raw, '原始需求'),
              'functional_preview': render(functional, '需求拆解', True), **report,
              'note': 'Review assigned dates, pending proposals and old acceptance criteria before applying. Original documents and legacy metadata are preserved in backup; no old approval is imported.'}
    for key, is_func in (('raw_preview', False), ('functional_preview', True)):
        _, errors = inspect(result[key], is_func)
        if errors:
            raise TrellisError('Migration produced invalid list: ' + '; '.join(errors))
    if apply:
        backup.mkdir(parents=True)
        for rel in (RAW, FUNC):
            if (root/rel).exists():
                shutil.copy2(root/rel, backup/Path(rel).name)
        if legacy.exists():
            shutil.copy2(legacy, backup/'state.json')
        (backup/'migration-report.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        for rel, key in ((RAW, 'raw_preview'), (FUNC, 'functional_preview')):
            f = root/rel
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(result[key], encoding='utf-8')
        if legacy.exists():
            legacy.unlink()
    return result
