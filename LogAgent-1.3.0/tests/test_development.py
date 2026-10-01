import tempfile
from pathlib import Path
from logagent.development.workspace import WorkspaceManager

def test_workspace_diff_apply_history():
    with tempfile.TemporaryDirectory() as td:
        w=WorkspaceManager(td); p=Path(td)/'x.py'; p.write_text('a=1\n',encoding='utf-8')
        assert 'x.py' in w.tree(); d=w.diff('x.py','a=2\n'); assert '-a=1' in d and '+a=2' in d
        r=w.apply('x.py','a=2\n'); assert r['changed'] and p.read_text()=='a=2\n'; assert w.history_list()
