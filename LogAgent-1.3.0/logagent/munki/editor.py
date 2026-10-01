import json, plistlib, copy, shutil
from pathlib import Path
from datetime import datetime, timezone
class RecipeManager:
    def __init__(self, root): self.root=Path(root); self.root.mkdir(parents=True,exist_ok=True); self.history=self.root/'history'; self.history.mkdir(exist_ok=True)
    def parse(self,text):
        data=plistlib.loads(text.encode()) if text.lstrip().startswith('<plist') else json.loads(text)
        if not isinstance(data,dict): raise ValueError('Recipe root must be an object')
        return data
    def validate(self,data):
        errors=[]
        if not isinstance(data,dict): return ['Recipe must be an object']
        if 'Identifier' not in data: errors.append('Missing Identifier')
        if 'Process' not in data and 'Input' not in data: errors.append('Recipe has neither Process nor Input')
        if 'Identifier' in data and not isinstance(data['Identifier'],str): errors.append('Identifier must be a string')
        return errors
    def save(self,name,data,source='editor'):
        errors=self.validate(data)
        if errors: raise ValueError('; '.join(errors))
        path=self.root/name; path.write_text(json.dumps(data,indent=2,sort_keys=True),encoding='utf-8'); self._history(name,data,source); return str(path)
    def save_as(self,source_name,target_name,data): return self.save(target_name,copy.deepcopy(data),'save-as:'+source_name)
    def pull(self,source):
        p=Path(source)
        if not p.exists(): raise FileNotFoundError(source)
        data=self.parse(p.read_text(encoding='utf-8')); self.validate(data); return data
    def push(self,name,destination):
        src=self.root/name
        if not src.exists(): raise FileNotFoundError(str(src))
        dst=Path(destination); dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst); return str(dst)
    def _history(self,name,data,source):
        record={'time':datetime.now(timezone.utc).isoformat(),'source':source,'data':data}
        with (self.history/(name+'.history.jsonl')).open('a',encoding='utf-8') as f: f.write(json.dumps(record)+'\n')
