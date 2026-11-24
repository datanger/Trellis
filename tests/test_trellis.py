import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from trellis.registry import ENTRIES, LOCK, SOURCES, FAMILIES, HINTS, TrellisError, catalog, validate
from trellis.install import install
from trellis.requirements import RAW, FUNC, bootstrap, check, migrate
from trellis import deps

class RegistryTests(unittest.TestCase):
    def test_inventory(self):
        v=validate()
        self.assertEqual((v['entries'],v['providers'],v['registered_resources'],v['skill_files'],v['capability_families']),(8,5,136,61,91))
        self.assertEqual(v['unmapped_registered_resources'],0)
        self.assertEqual(set().union(*(set(catalog(e)['families']) for e in ENTRIES)),set(FAMILIES))
    def test_hints_different(self):
        h=catalog('audit')['task_hints']
        self.assertNotEqual(h['audit.docs-consistency']['capabilities'],h['audit.bugs']['capabilities'])
        s=catalog('simpler')['task_hints']
        self.assertNotEqual(s['simpler.docs']['capabilities'],s['simpler.code']['capabilities'])
        self.assertTrue(all('steps' not in h for h in HINTS.values()))
    def test_native_modes(self):
        for h in ['audit.archify-pr-attach','audit.band-import','dev.ponytail-off','simpler.archify-story-video']:
            self.assertIn(h,HINTS)
    def test_unknown_entry(self):
        with self.assertRaises(TrellisError):catalog('unknown')
    def test_missing_provider(self):
        with tempfile.TemporaryDirectory() as d, patch('trellis.deps.dep_root',return_value=Path(d)):
            self.assertFalse(deps.doctor()['ready'])
            with self.assertRaises(TrellisError):deps.resolve(next(iter(SOURCES)))

class RequirementsTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
    def tearDown(self):self.tmp.cleanup()
    def test_bootstrap_preserve(self):
        bootstrap(self.root);p=self.root/RAW;p.write_text('user owned content')
        self.assertEqual(bootstrap(self.root)['created'],[]);self.assertEqual(p.read_text(),'user owned content')
        self.assertFalse((self.root/'.trellis').exists())
    def write_raw(self,rows):
        bootstrap(self.root);(self.root/RAW).write_text('# 原始需求\n| 序号 | 需求描述 |\n|---|---|\n'+rows+'\n')
    def test_valid_markdown_edit_and_delete(self):
        self.write_raw('| R-0001 | 原始需求（2026-11-24） |\n| R-0002 | ~~删除的需求~~ (2026-11-24) |')
        self.assertTrue(check(self.root)['ok'])
        p=self.root/RAW;p.write_text(p.read_text().replace('原始需求（','更新需求（'))
        self.assertTrue(check(self.root)['ok'])
    def test_operation_only(self):
        self.write_raw('| R-0001 | `$trellis-init`（2026-11-24） |');self.assertFalse(check(self.root)['ok'])
    def test_duplicate_and_bad_date(self):
        self.write_raw('| R-0001 | x（2026-99-24） |\n| R-0001 | y（2026-11-24） |');self.assertEqual(len(check(self.root)['errors']),2)
    def test_invalid_links(self):
        self.write_raw('| R-0001 | ~~x~~（2026-11-24） |')
        (self.root/FUNC).write_text('| F01-001 | y | R-0001 | test | 已确认 |\n| F01-002 | y | R-0099 | test | 待确认 |')
        self.assertEqual(len(check(self.root)['errors']),2)
    def legacy(self):
        bootstrap(self.root);(self.root/'.trellis').mkdir();state={'schema':1,'raw':[{'id':'R-0001','text':'$trellis-init','time':'2026-11-23T00:00:00','operation':'add','supersedes':[]},{'id':'R-0002','text':'旧需求','time':'2026-11-23T00:00:00','operation':'add','supersedes':[]},{'id':'R-0003','text':'新需求','time':'2026-11-24T00:00:00','operation':'modify','supersedes':['R-0002']}],'functional':{'F01-001':{'category':'业务','text':'功能','raw_ids':['R-0003'],'acceptance':'test','status':'confirmed'}},'categories':{'业务':'F01'},'views':{r:hashlib.sha256((self.root/r).read_bytes()).hexdigest() for r in (RAW,FUNC)}}
        (self.root/'.trellis/state.json').write_text(json.dumps(state));return state
    def test_migration(self):
        self.legacy();preview=migrate(self.root);self.assertEqual(preview['omitted_operation_ids'],['R-0001']);self.assertEqual(preview['highest_legacy_id'],3);self.assertNotIn('R-0003',(self.root/RAW).read_text());self.assertIn('~~旧需求~~（2026-11-24）',preview['raw_preview']);migrate(self.root,True)
        self.assertTrue(check(self.root)['ok']);self.assertTrue((self.root/'.trellis/v0.1-backup/state.json').exists());self.assertFalse((self.root/'.trellis/state.json').exists())
    def test_migration_refuses_modified_docs(self):
        self.legacy();(self.root/RAW).write_text('manual edit')
        with self.assertRaises(TrellisError):migrate(self.root,True)
        self.assertEqual((self.root/RAW).read_text(),'manual edit')
    def test_bootstrap_legacy_guard(self):
        self.legacy()
        with self.assertRaises(TrellisError):bootstrap(self.root)

class InstallTests(unittest.TestCase):
    def test_both_layouts(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);r=install('both','user',root,offline=True,home=root)
            self.assertEqual(len(r['installed']),16)
            for path in r['installed']:
                self.assertIn('Trellis managed installation',Path(path).read_text());self.assertNotIn('@TRELLIS_TOOLKIT@',Path(path).read_text())
            self.assertTrue((Path(r['toolkit'])/'templates/raw-requirements.md').exists());self.assertFalse((Path(r['toolkit'])/'trellis/engine.py').exists())
    def test_project_scope(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);r=install('codex','project',root,offline=True,home=root)
            self.assertEqual(len(r['installed']),8);self.assertTrue((root/'.agents/skills/trellis-init/SKILL.md').is_file())
    def test_upgrade_explicit(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);f=root/'.agents/skills/trellis-init/SKILL.md';f.parent.mkdir(parents=True);f.write_text('Trellis managed installation old toolkit')
            with self.assertRaises(TrellisError):install('codex','user',root,offline=True,home=root)
            install('codex','user',root,offline=True,replace=True,home=root);self.assertNotIn('old toolkit',f.read_text())
    def test_unrelated_skill_preserved(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);f=root/'.agents/skills/trellis-init/SKILL.md';f.parent.mkdir(parents=True);f.write_text('not managed')
            with self.assertRaises(TrellisError):install('codex','user',root,offline=True,replace=True,home=root)
            self.assertEqual(f.read_text(),'not managed')

if __name__=='__main__':unittest.main()
