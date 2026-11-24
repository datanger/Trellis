import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from trellis.engine import Project
from trellis.registry import ENTRIES, LOCK, SOURCES, COVERAGE, ROUTES, TrellisError, compose, validate
from trellis.install import install
from trellis import deps


class RegistryTests(unittest.TestCase):
    def test_all_entries_and_pinned_inventory(self):
        result=validate()
        self.assertEqual(result['entries'],8)
        self.assertEqual(result['providers'],5)
        self.assertEqual(result['skill_files'],61)
        self.assertEqual(result['unmapped_registered_resources'],0)
        self.assertEqual(set(SOURCES),set(COVERAGE))
        self.assertEqual(set(ENTRIES),{'init','requirements','design','contract','dev','accept','audit','simpler'})
        for provider,meta in LOCK.items(): self.assertEqual(len(meta['commit']),40)

    def test_same_entry_routes_differ(self):
        a=compose('trellis-audit',['audit.docs-consistency']); b=compose('audit',['audit.bugs'])
        self.assertNotEqual(a['steps'],b['steps'])
        self.assertTrue(all(not x['mutates'] for x in a['steps']+b['steps']))
        d=compose('simpler',['simpler.docs','simpler.code'])
        self.assertEqual([s['gate'] for s in d['steps'] if s['kind']=='gate'],['cleanup','cleanup'])

    def test_reject_wrong_entry_and_duplicate(self):
        with self.assertRaises(TrellisError):compose('audit',['dev.bug'])
        with self.assertRaises(TrellisError):compose('audit',['audit.bugs','audit.bugs'])

    def test_progressive_preserves_separate_gates(self):
        w=compose('contract',['contract.progressive'])
        self.assertEqual(w['requires'],['design'])
        self.assertEqual([s['gate'] for s in w['steps'] if s['kind']=='gate'],['contract','skeleton','plan'])
        self.assertEqual(compose('dev',['dev.implement'])['requires'],['plan'])

    def test_split_contract_compose_keeps_prerequisite(self):
        w=compose('contract',['contract.interfaces','contract.skeleton','contract.integrate'])
        self.assertEqual(w['requires'],['design'])
        self.assertEqual([s['gate'] for s in w['steps'] if s['kind']=='gate'],['contract','skeleton','plan'])

    def test_native_paths_and_modes(self):
        self.assertIn('audit.archify-pr-attach',ROUTES)
        self.assertIn('dev.ponytail-off',ROUTES)
        self.assertIn('init.cap-workflow-overlays',ROUTES)
        self.assertIn('audit.band-import',ROUTES)
        self.assertEqual(ROUTES['dev.ponytail-off']['steps'][0]['providers'],[])


class ProjectTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)
        self.git('init','-q');self.git('config','user.name','Trellis Test');self.git('config','user.email','test@example.invalid')
        self.write('src.py','def value():\n    return 1\n');self.write('test_value.py','from src import value\nassert value() == 1\n');self.write('design.md','Design v1\n');self.write('contract.md','Contract v1\n');self.write('skeleton.md','Public signatures\n');self.write('plan.md','Plan v1\n')
        self.write('accept.json',json.dumps({'commands':[[sys.executable,'-B','test_value.py']], 'protect':['src.py','test_value.py','design.md']}))
        self.write('.gitignore','__pycache__/\n.trellis/\n'); self.commit()
        self.p=Project(self.root); self.ctx=self.p.locked(create=True);self.ctx.__enter__();self.p.bootstrap();self.commit()
        self.fake=patch('trellis.deps.resolve',side_effect=lambda k:{'key':k,'file':'unit-test-mocked-provider'});self.fake.start()

    def tearDown(self):
        self.fake.stop();self.ctx.__exit__(None,None,None);self.tmp.cleanup()

    def write(self,path,content):
        p=self.root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content,encoding='utf-8');return p

    def git(self,*args):return subprocess.run(['git',*args],cwd=self.root,check=True,capture_output=True,text=True).stdout
    def commit(self):self.git('add','.');self.git('commit','-qm','snapshot')

    def approve(self,scope,stage,files,run=None):
        g=self.p.propose(scope,stage,files,'test review packet',run=run)
        self.p.decide(g['id'],g['token'],'human-test','approve');return g['id']

    def make_baseline(self):
        r=self.p.test([sys.executable,'-B','test_value.py']);self.assertEqual(r['exit_code'],0)
        files=['src.py','test_value.py','design.md','accept.json']
        g=self.approve('module','acceptance',files+[r['receipt']]);return self.p.baseline('module',g,[r['receipt']],files,'accept.json')

    def test_original_append_modify_and_dedup(self):
        r=self.p.raw_add('支持 PDF\n不要更改源文件','chat:1');r2=self.p.raw_add('支持 PDF\n不要更改源文件','chat:1');self.assertEqual(r,r2)
        q=self.p.raw_add('改为 Word','chat:2','modify',[r['id']]); self.assertNotEqual(q['id'],r['id'])
        text=(self.root/'docs/requirements/raw-requirements.md').read_text();self.assertIn('> 支持 PDF\n> 不要更改源文件',text);self.assertIn('> 改为 Word',text)
        self.assertEqual(len(self.p.state['raw']),2)

    def test_functional_ids_and_approval(self):
        r=self.p.raw_add('Upload','chat:1'); f=self.p.functional_upsert('File','Upload', [r['id']],'valid file',derived=True)
        self.assertEqual(f['id'],'F01-001'); self.assertEqual(f['status'],'proposed')
        g=self.approve(f['id'],'requirements',['docs/requirements/functional-requirements.md'])
        self.assertEqual(self.p.confirm_functional(f['id'],g)['status'],'confirmed');self.assertTrue(self.p.gate_current(self.p.state['gates'][g]))
        updated=self.p.functional_upsert('File','Upload PDF',[r['id']],'pdf accepted',fid=f['id']);self.assertEqual(updated['id'],f['id']);self.assertEqual(updated['status'],'proposed')
        self.assertFalse(self.p.gate_current(self.p.state['gates'][g]))

    def test_invalid_raw_mapping(self):
        with self.assertRaises(TrellisError):self.p.functional_upsert('File','Upload',['R-9999'],'works')
        with self.assertRaises(TrellisError):self.p.raw_add('Delete','chat','delete')

    def test_generated_views_not_overwritten(self):
        self.write('docs/requirements/raw-requirements.md','human edit')
        with self.assertRaises(TrellisError):self.p.raw_add('New','chat')
        self.assertEqual((self.root/'docs/requirements/raw-requirements.md').read_text(),'human edit')

    def test_gate_detects_changed_artifact_and_token(self):
        g=self.p.propose('module','design',['design.md'],'review')
        with self.assertRaises(TrellisError):self.p.decide(g['id'],'wrong','human','approve')
        self.write('design.md','Changed after review')
        with self.assertRaises(TrellisError):self.p.decide(g['id'],g['token'],'human','approve')

    def test_requirements_precondition(self):
        with self.assertRaises(TrellisError):self.p.start('design',['design.solution'],'design','module')
        self.approve('module','requirements',['design.md']); r=self.p.start('design',['design.solution'],'design','module');self.assertEqual(r['status'],'active')
        self.write('design.md','new version')
        with self.assertRaises(TrellisError):self.p.preflight(r['id'])

    def test_gate_step_blocks_and_resumes(self):
        r=self.p.start('dev',['dev.bug'],'fix bug','module',['src.py','test_value.py']);rid=r['id'];self.p.complete(rid,['design.md'])
        self.assertEqual(self.p.next(rid)['current']['kind'],'gate')
        with self.assertRaises(TrellisError):self.p.complete(rid,['design.md'])
        wrong=self.approve('module','change',['design.md'])
        with self.assertRaises(TrellisError):self.p.complete(rid,gate_id=wrong)
        g=self.approve('module','change',['design.md'],run=rid);self.p.complete(rid,gate_id=g)
        self.assertTrue(self.p.next(rid)['current']['id'].endswith('/red'))
        # state can be resumed by a fresh Project instance
        other=Project(self.root);other.state=json.loads(other.statefile.read_text());self.assertEqual(other.next(rid)['current'],self.p.next(rid)['current'])

    def test_scope_check(self):
        r=self.p.start('dev',['dev.bug'],'fix','module',['src.py']);self.write('contract.md','unauthorized edit')
        with self.assertRaisesRegex(TrellisError,'Out-of-scope'):self.p.preflight(r['id'])

    def test_missing_provider_blocks(self):
        r=self.p.start('audit',['audit.bugs'],'检查bug','module'); self.fake.stop()
        try:
            with self.assertRaisesRegex(TrellisError,'missing pinned checkout'):self.p.preflight(r['id'])
        finally:self.fake.start()

    def test_test_exit_code_and_stale_receipt(self):
        a=self.p.start('accept',['accept.test'],'run tests','module');rid=a['id'];self.p.complete(rid,['test_value.py'])
        bad=self.p.test([sys.executable,'-c','raise SystemExit(7)']);self.assertEqual(bad['exit_code'],7)
        with self.assertRaises(TrellisError):self.p.complete(rid,[bad['receipt']],receipt=bad['receipt'])
        good=self.p.test([sys.executable,'-B','test_value.py']);self.assertEqual(good['exit_code'],0)
        self.write('src.py','def value(): return 2\n')
        with self.assertRaisesRegex(TrellisError,'stale'):self.p.complete(rid,[good['receipt']],receipt=good['receipt'])

    def test_pass_and_persistent_completion(self):
        r=self.p.start('accept',['accept.test'],'test','module');rid=r['id'];self.p.complete(rid,['test_value.py'])
        good=self.p.test([sys.executable,'-B','test_value.py']);d=self.p.complete(rid,[good['receipt']],receipt=good['receipt']);self.assertEqual(d['status'],'done');self.assertNotIn('initial_files',self.p.run(rid))

    def test_baseline_detects_code_docs_and_test_edits(self):
        b=self.make_baseline();self.assertEqual(b['commit'],self.p.head());self.assertTrue(self.p.guard()['ok'])
        for f in ['src.py','design.md','test_value.py']:
            old=(self.root/f).read_text();self.write(f,old+'\n# drift\n');self.assertFalse(self.p.guard()['ok']);self.assertIn(f,[x['path'] for x in self.p.guard()['changed']]);self.write(f,old)
        self.assertTrue(self.p.guard()['ok'])

    def test_baseline_requires_every_approved_command(self):
        r=self.p.test([sys.executable,'-c','pass']); files=['src.py','test_value.py','design.md','accept.json'];g=self.approve('module','acceptance',files+[r['receipt']])
        with self.assertRaisesRegex(TrellisError,'Missing approved acceptance commands'):self.p.baseline('module',g,[r['receipt']],files,'accept.json')

    def test_authorized_change_still_needs_reaccept(self):
        self.make_baseline();r=self.p.start('dev',['dev.bug'],'fix','module',['src.py']);rid=r['id']
        g=self.approve('module','change',['src.py','plan.md']);self.p.authorize_change(rid,g,['src.py'])
        self.write('src.py','def value():\n    return 1  # changed implementation\n');self.p.preflight(rid);self.assertFalse(self.p.guard()['ok'])
        self.commit();b=self.make_baseline();self.assertTrue(self.p.guard()['ok']);self.assertEqual(len(self.p.state['baseline_history']),1)

    def test_receipt_log_tamper_detected(self):
        r=self.p.test([sys.executable,'-B','test_value.py']);self.write(r['log'],'changed log')
        with self.assertRaisesRegex(TrellisError,'changed local test log'):self.p.read_receipt(r['receipt'])

    def test_path_escape(self):
        with self.assertRaises(TrellisError):self.p.path('../outside')
        with self.assertRaises(TrellisError):self.p.path('/tmp/outside')


class InstallerTests(unittest.TestCase):
    def test_offline_install_both_hosts_and_eight_entries(self):
        with tempfile.TemporaryDirectory() as d:
            home=Path(d);out=install('both','user',home,offline=True,home=home)
            self.assertEqual(len(out['installed']),16)
            for path in (home/'.agents/skills',home/'.claude/skills'):
                self.assertEqual(len(list(path.glob('*/SKILL.md'))),8)
                for f in path.glob('*/SKILL.md'):
                    self.assertNotIn('@TRELLIS_TOOLKIT@',f.read_text());self.assertIn(str(home/'.trellis/toolkits/0.1.0'),f.read_text())
            r=subprocess.run([sys.executable,str(Path(out['toolkit'])/'trellis.py'),'validate'],check=True,capture_output=True,text=True);self.assertEqual(json.loads(r.stdout)['entries'],8)

    def test_project_scope_and_no_overwrite_user_skill(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);install('codex','project',p,offline=True,home=p)
            self.assertTrue((p/'.agents/skills/trellis-init/SKILL.md').exists())
            f=p/'.claude/skills/trellis-init/SKILL.md';f.parent.mkdir(parents=True);f.write_text('unrelated')
            with self.assertRaises(TrellisError):install('claude','project',p,offline=True,home=p)
            self.assertEqual(f.read_text(),'unrelated')

    def test_source_inventory_drift_blocks(self):
        provider='superpowers';files=LOCK[provider]['skill_files'];all_paths={v['path'] for v in SOURCES.values() if v['provider']==provider}
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)
            for x in all_paths:
                f=path/x;f.parent.mkdir(parents=True,exist_ok=True);f.write_text('test fixture')
            with patch('trellis.deps.git',return_value='\n'.join(all_paths)):
                self.assertEqual(deps.inventory(path,provider)['skills'],len(files))
            with patch('trellis.deps.git',return_value='\n'.join(all_paths|{'skills/new/SKILL.md'})):
                with self.assertRaisesRegex(TrellisError,'new skills'):deps.inventory(path,provider)


if __name__=='__main__':unittest.main()
