import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from trellis.registry import ROOT, ENTRIES, LOCK, SOURCES, FAMILIES, HINTS, TrellisError, catalog, validate
from trellis.install import install
from trellis.requirements import RAW, FUNC, bootstrap, check, migrate
from trellis import deps

class RegistryTests(unittest.TestCase):
    def test_inventory(self):
        v=validate()
        self.assertEqual((v['entries'],v['providers'],v['registered_resources'],v['skill_files'],v['capability_families']),(8,5,136,61,91))
        self.assertEqual(v['unmapped_registered_resources'],0)
        self.assertEqual(v['workflow_files'],8)
        self.assertEqual(set().union(*(set(catalog(e)['families']) for e in ENTRIES)),set(FAMILIES))
    def test_hints_different(self):
        h=catalog('audit')['task_hints']
        self.assertNotEqual(h['audit.docs-consistency']['capabilities'],h['audit.bugs']['capabilities'])
        s=catalog('simpler')['task_hints']
        self.assertNotEqual(s['simpler.docs']['capabilities'],s['simpler.code']['capabilities'])
        self.assertTrue(all('steps' not in h for h in HINTS.values()))
    def test_entry_workflows(self):
        for entry in ENTRIES:
            path=Path(catalog(entry)['workflow']);self.assertTrue(path.is_file());self.assertIn('## Other registered capabilities',path.read_text());self.assertIn('workflows.md',path.with_name('SKILL.md').read_text())
    def test_existing_plan_uses_real_ponytail(self):
        text=(ROOT/'skills/trellis-dev/workflows.md').read_text();section=text.split('## Execute an existing plan',1)[1].split('## Plan new work',1)[0]
        for key in ['superpowers:skills/executing-plans/SKILL.md','ponytail:skills/ponytail/SKILL.md','agent-skills:skills/incremental-implementation/SKILL.md','superpowers:skills/test-driven-development/SKILL.md','superpowers:skills/verification-before-completion/SKILL.md']:
            self.assertIn(key,section);self.assertIn(key,SOURCES)
        self.assertIn('Required before writing',section);self.assertIn('do not regenerate a plan',section)
        self.assertIn('dev.execute-plan',catalog('dev')['task_hints'])
    def test_contract_design_stops_before_implementation(self):
        text=(ROOT/'skills/trellis-contract/workflows.md').read_text();section=text.split('## Design or review interfaces',1)[1].split('## Create a public code skeleton',1)[0]
        self.assertIn('agent-skills:skills/api-and-interface-design/SKILL.md',section);self.assertIn('do not create skeleton or business code',section)
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
        bootstrap(self.root);(self.root/RAW).write_text('# 原始需求\n\n'+rows+'\n')
    def write_func(self,rows):
        bootstrap(self.root);(self.root/FUNC).write_text('# 需求拆解\n\n'+rows+'\n')
    def test_valid_markdown_edit_and_delete(self):
        self.write_raw('1. 原始需求（2026-11-24）\n2. ~~删除的需求~~ (2026-11-24)')
        self.write_func('## 输入\n\n1. 读取文件（2026-11-24）\n2. ~~旧格式~~（2026-11-24）\n\n## 输出\n\n1. 输出结果（2026-11-24）')
        self.assertTrue(check(self.root)['ok']);self.assertEqual(check(self.root)['functional'],3)
        p=self.root/RAW;p.write_text(p.read_text().replace('原始需求（','更新需求（'))
        self.assertTrue(check(self.root)['ok'])
    def test_operation_only(self):
        self.write_raw('1. `$trellis-init`（2026-11-24）\n2. /plan（2026-11-24）');self.assertFalse(check(self.root)['ok'])
    def test_numbering_and_bad_date(self):
        self.write_raw('1. x（2026-99-24）\n1. y（2026-11-24）');self.assertEqual(len(check(self.root)['errors']),2)
        self.write_raw('1. x（2026-11-24）\n3. y（2026-11-24）');self.assertFalse(check(self.root)['ok'])
    def test_functional_category_restart(self):
        self.write_func('## A\n1. x（2026-11-24）\n## B\n2. y（2026-11-24）');self.assertFalse(check(self.root)['ok'])
        self.write_func('1. x（2026-11-24）');self.assertFalse(check(self.root)['ok'])
    def test_reject_tables_bullets_and_metadata(self):
        for value in ['| R-0001 | x（2026-11-24） |','- x（2026-11-24）','1. x','1. ~~x（2026-11-24）','1. x（2026-11-24)']:
            self.write_raw(value);self.assertFalse(check(self.root)['ok'],value)
    def legacy(self):
        bootstrap(self.root);(self.root/'.trellis').mkdir();state={'schema':1,'raw':[{'id':'R-0001','text':'$trellis-init','time':'2026-11-23T00:00:00','operation':'add','supersedes':[]},{'id':'R-0002','text':'旧需求','time':'2026-11-23T00:00:00','operation':'add','supersedes':[]},{'id':'R-0003','text':'新需求','time':'2026-11-24T00:00:00','operation':'modify','supersedes':['R-0002']}],'functional':{'F01-001':{'category':'业务','text':'功能','raw_ids':['R-0003'],'acceptance':'test','status':'confirmed','time':'2026-11-24T00:00:00'},'F01-002':{'category':'业务','text':'提案','raw_ids':['R-0003'],'acceptance':'test2','status':'proposed'}},'categories':{'业务':'F01'},'views':{r:hashlib.sha256((self.root/r).read_bytes()).hexdigest() for r in (RAW,FUNC)}}
        (self.root/'.trellis/state.json').write_text(json.dumps(state));return state
    def test_migration(self):
        self.legacy();preview=migrate(self.root);self.assertEqual(preview['omitted_operations'],['R-0001']);self.assertEqual(preview['pending_functional'],['F01-002']);self.assertIn('1. ~~旧需求~~（2026-11-24）',preview['raw_preview']);self.assertIn('2. 新需求（2026-11-24）',preview['raw_preview']);self.assertNotIn('提案',preview['functional_preview']);self.assertFalse((self.root/'.trellis/v0.1-backup').exists());migrate(self.root,True)
        self.assertTrue(check(self.root)['ok']);self.assertTrue((self.root/'.trellis/v0.1-backup/state.json').exists());self.assertFalse((self.root/'.trellis/state.json').exists())
    def test_table_migration(self):
        self.write_raw('| 序号 | 需求描述 |\n|---|---|\n| R-0001 | 读取文件（2026-11-24） |\n| R-0002 | ~~旧格式~~（2026-11-24） |')
        self.write_func('## F01 业务\n\n| 编号 | 功能点 | 原始来源 | 验收条件 | 状态 |\n|---|---|---|---|---|\n| F01-001 | 读取文件 | R-0001 | 验收细节 | 已确认 |\n| F01-002 | 待议 | R-0001 | test | 待确认（AI推导） |\n| F01-003 | 旧功能 | R-0002 | test | 已取消 |\n\n## F02 输出\n\n| F02-001 | 输出结果 | R-0001 | test | 已确认 |')
        preview=migrate(self.root);self.assertEqual(preview['pending_functional'],['F01-002']);self.assertIn('F01-001',preview['dates_assigned']);self.assertIn('## 业务',preview['functional_preview']);self.assertIn('2. ~~旧功能~~',preview['functional_preview']);self.assertIn('## 输出\n\n1. 输出结果',preview['functional_preview']);self.assertEqual(preview['legacy_functional_metadata'][0]['acceptance'],'验收细节')
        old=(self.root/FUNC).read_text();migrate(self.root,True);self.assertTrue(check(self.root)['ok']);self.assertEqual((self.root/'.trellis/requirements-list-backup/functional-requirements.md').read_text(),old);self.assertFalse(migrate(self.root,True)['applied'])
    def test_bullet_migration(self):
        self.write_raw('- A（2026-11-24）\n- ~~B~~（2026-11-24）');self.write_func('## 分类一\n- A（2026-11-24）\n## 分类二\n- B（2026-11-24）')
        migrate(self.root,True);self.assertTrue(check(self.root)['ok']);self.assertIn('## 分类二\n\n1. B', (self.root/FUNC).read_text())
    def test_migration_refuses_modified_docs(self):
        self.legacy();(self.root/RAW).write_text('manual edit')
        with self.assertRaises(TrellisError):migrate(self.root,True)
        self.assertEqual((self.root/RAW).read_text(),'manual edit')
    def test_migration_refuses_unknown_content(self):
        self.write_raw('Unknown user-owned content')
        with self.assertRaises(TrellisError):migrate(self.root,True)
        self.assertIn('Unknown user-owned content',(self.root/RAW).read_text());self.assertFalse((self.root/'.trellis').exists())
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
            self.assertTrue((Path(r['toolkit'])/'templates/raw-requirements.md').exists());
            for entry in ENTRIES:self.assertTrue((Path(r['toolkit'])/'skills'/('trellis-'+entry)/'workflows.md').exists());
            self.assertFalse((Path(r['toolkit'])/'trellis/engine.py').exists())
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
