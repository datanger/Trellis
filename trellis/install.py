"""Install only eight entry skills; keep pinned upstream repos out of discovery."""
import sys
import shutil
import subprocess
import tempfile
from pathlib import Path
from .registry import ROOT, ENTRIES, TrellisError, validate
from .engine import atomic


def install(host, scope, project, offline=False, replace=False, home=None):
    validate()
    home=Path(home or Path.home()).resolve(); project=Path(project).resolve()
    if scope=='project' and not project.is_dir():raise TrellisError('Project path must exist')
    version=(ROOT/'VERSION').read_text().strip()
    hosts=['codex','claude'] if host=='both' else [host]
    toolkit=(home/'.trellis'/'toolkits'/version if scope=='user' else project/'.trellis'/'toolkit'/version)
    dirs={h:(home if scope=='user' else project)/('.agents' if h=='codex' else '.claude')/'skills' for h in hosts}
    # Preflight existing entries to avoid replacing unrelated user skills.
    for d in dirs.values():
        for n in ENTRIES:
            f=d/('trellis-'+n)/'SKILL.md'
            if f.exists() and 'Trellis managed installation' not in f.read_text(encoding='utf-8'):
                raise TrellisError('Existing unrelated skill: '+str(f))
            if f.exists() and not replace:
                content=f.read_text(encoding='utf-8')
                if str(toolkit) not in content:raise TrellisError('Existing Trellis installation uses a different toolkit; use --replace explicitly')
    toolkit.parent.mkdir(parents=True,exist_ok=True)
    # Prepare runtime atomically; reuse exact toolkit if already installed, not partial installs.
    if not toolkit.exists():
        with tempfile.TemporaryDirectory(prefix='.trellis-install-',dir=toolkit.parent) as temp:
            stage=Path(temp)/version; stage.mkdir()
            for name in ('trellis','registry','skills','docs'):
                shutil.copytree(ROOT/name,stage/name,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
            for name in ('trellis.py','VERSION','README.md','README.en.md','LICENSE','NOTICE.md'):
                if (ROOT/name).exists():shutil.copy2(ROOT/name,stage/name)
            if (ROOT/'upstream').exists():shutil.copytree(ROOT/'upstream',stage/'upstream',symlinks=True)
            if not offline:
                r=subprocess.run([sys.executable,str(stage/'trellis.py'),'deps','sync'],check=False)
                if r.returncode:raise TrellisError('Pinned upstream download failed; no entry skills installed. Use --offline only for wrapper development.')
            stage.rename(toolkit)
    elif not offline:
        r=subprocess.run([sys.executable,str(toolkit/'trellis.py'),'deps','sync'],check=False)
        if r.returncode:raise TrellisError('Pinned upstream validation/download failed')
    installed=[]
    for h,d in dirs.items():
        for n in ENTRIES:
            name='trellis-'+n; src=toolkit/'skills'/name/'SKILL.md'
            text=src.read_text(encoding='utf-8').replace('@TRELLIS_TOOLKIT@',str(toolkit)).replace('@TRELLIS_PYTHON@',sys.executable)
            dest=d/name/'SKILL.md'; atomic(dest,text);installed.append(str(dest))
    return {'version':version,'toolkit':str(toolkit),'installed':installed,'dependency_mode':'offline (wrappers only if cache missing)' if offline else 'pinned checkout','restart':'Start a fresh Codex/Claude Code session.'}
