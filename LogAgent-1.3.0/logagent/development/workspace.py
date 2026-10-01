import json, difflib, subprocess
from pathlib import Path
from datetime import datetime, timezone
class WorkspaceManager:
    ALLOWED_EXT={'.py','.js','.ts','.tsx','.json','.yaml','.yml','.md','.html','.css','.ps1','.psm1','.sql','.toml','.txt','.recipe'}
    def __init__(self, root):
        self.root=Path(root).resolve(); self.root.mkdir(parents=True,exist_ok=True); self.history=self.root/'history'; self.history.mkdir(exist_ok=True)
    def _safe(self, rel):
        p=(self.root/rel).resolve()
        if self.root not in p.parents and p != self.root: raise ValueError('Path outside development workspace')
        return p
    def tree(self, rel='.'):
        base=self._safe(rel); return [str(p.relative_to(self.root)) for p in sorted(base.rglob('*')) if p.is_file() and p.suffix.lower() in self.ALLOWED_EXT]
    def read(self, rel):
        p=self._safe(rel)
        if p.stat().st_size > 2_000_000: raise ValueError('File too large')
        return p.read_text(encoding='utf-8')
    def diff(self, rel, proposed): return ''.join(difflib.unified_diff(self.read(rel).splitlines(True),proposed.splitlines(True),fromfile=rel,tofile=rel+'.proposed'))
    def apply(self, rel, content, reason='chatgpt'):
        p=self._safe(rel); p.parent.mkdir(parents=True,exist_ok=True); old=p.read_text(encoding='utf-8') if p.exists() else ''
        stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'); backup=self.history/f'{stamp}_{Path(rel).name}.before'; backup.write_text(old,encoding='utf-8'); p.write_text(content,encoding='utf-8')
        return {'path':rel,'backup':str(backup.relative_to(self.root)),'changed':old!=content,'reason':reason}
    def run_tests(self, command):
        if not command.strip().startswith(('pytest','python -m pytest')): raise ValueError('Only allow-listed pytest commands are permitted')
        return subprocess.run(command,shell=True,cwd=self.root,capture_output=True,text=True,timeout=600)
    def history_list(self): return [str(p.relative_to(self.root)) for p in sorted(self.history.glob('*'))]
