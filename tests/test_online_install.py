"""Exercise the real bootstrap against a local archive; no network or user files."""
import io
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / 'VERSION').read_text().strip()


class OnlineInstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='trellis-online-test-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.home = self.root / 'home'; self.home.mkdir()
        self.bin = self.root / 'bin'; self.bin.mkdir()
        self.archive = self.root / 'source.tar.gz'
        self.log = self.root / 'curl.log'
        self.env = dict(os.environ, HOME=str(self.home), PYTHON=sys.executable,
                        PATH=str(self.bin) + os.pathsep + os.environ['PATH'],
                        TRELLIS_TEST_ARCHIVE=str(self.archive), TRELLIS_TEST_LOG=str(self.log),
                        TMPDIR=str(self.root))
        # The curl substitute records the exact URL, honors -o and can inject failure.
        fake = self.bin / 'curl'
        fake.write_text('''#!/usr/bin/env bash
set -euo pipefail
printf '%s\\n' "$@" > "$TRELLIS_TEST_LOG"
if [[ "${TRELLIS_TEST_FAIL:-0}" == 1 ]]; then exit 22; fi
while (($#)); do
  if [[ "$1" == -o ]]; then cp "$TRELLIS_TEST_ARCHIVE" "$2"; exit 0; fi
  shift
done
exit 2
''')
        fake.chmod(0o755)
        self.make_archive()

    def make_archive(self, version=VERSION, valid=True):
        with tarfile.open(self.archive, 'w:gz') as archive:
            if valid:
                for name in ('install.sh', 'trellis.py', 'trellis', 'skills', 'registry', 'docs', 'templates'):
                    archive.add(ROOT / name, arcname='Trellis-fixture/' + name,
                                filter=lambda item: None if '__pycache__' in item.name else item)
            data = (version + '\n').encode()
            entry = tarfile.TarInfo('Trellis-fixture/VERSION'); entry.size = len(data)
            archive.addfile(entry, io.BytesIO(data))

    def run_install(self, *args, **extra_env):
        return subprocess.run(['bash', str(ROOT / 'install-online.sh'), *args],
                              cwd=self.root, env=dict(self.env, **extra_env),
                              capture_output=True, text=True, timeout=30)

    def test_both_hosts(self):
        r = self.run_install('--host', 'both', '--offline')
        self.assertEqual(r.returncode, 0, r.stderr)
        for host in ('.agents', '.claude'):
            files = list((self.home / host / 'skills').glob('trellis-*/SKILL.md'))
            self.assertEqual(len(files), 8)
            self.assertIn(str(self.home / '.trellis' / 'toolkits' / VERSION), files[0].read_text())
        self.assertIn('/tar.gz/refs/heads/main', self.log.read_text())
        self.assertFalse(list(self.root.glob('tmp.*')))

    def test_pinned_relative_project(self):
        project = self.root / 'project with spaces'; project.mkdir()
        r = self.run_install('--version', 'v' + VERSION, '--host', 'claude', '--scope', 'project',
                             '--target', project.name, '--offline')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('/tar.gz/refs/tags/v' + VERSION, self.log.read_text())
        self.assertTrue((project / '.claude/skills/trellis-init/SKILL.md').is_file())
        self.assertFalse((self.home / '.claude').exists())

    def test_upgrade(self):
        entry = self.home / '.agents/skills/trellis-init/SKILL.md'
        entry.parent.mkdir(parents=True); entry.write_text('Trellis managed installation old toolkit')
        r = self.run_install('--host', 'codex', '--offline', '--replace')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotIn('old toolkit', entry.read_text())

    def test_download_failure(self):
        r = self.run_install('--host', 'both', '--offline', TRELLIS_TEST_FAIL='1')
        self.assertNotEqual(r.returncode, 0)
        self.assertFalse((self.home / '.agents').exists())
        self.assertFalse(list(self.root.glob('tmp.*')))

    def test_invalid_version(self):
        r = self.run_install('--version', '../main')
        self.assertNotEqual(r.returncode, 0)
        self.assertFalse(self.log.exists())

    def test_version_mismatch(self):
        r = self.run_install('--version', 'v99.99.99', '--offline')
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('does not match', r.stderr)
        self.assertFalse((self.home / '.agents').exists())

    def test_missing_archive_files(self):
        self.make_archive(valid=False)
        r = self.run_install('--offline')
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('Invalid Trellis archive', r.stderr)

    def test_help_does_not_download(self):
        r = self.run_install('--help')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertFalse(self.log.exists())


if __name__ == '__main__':
    unittest.main()
