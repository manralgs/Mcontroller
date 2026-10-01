import json, tempfile
from pathlib import Path
from logagent.munki import RecipeManager

def test_validate_save_saveas_pull_push():
    with tempfile.TemporaryDirectory() as td:
        m=RecipeManager(td); r={'Identifier':'com.example.Test','Input':{'NAME':'Test'}}
        assert m.validate(r)==[]; m.save('Test.recipe',r); m.save_as('Test.recipe','Test-copy.recipe',r)
        pulled=m.pull(str(Path(td)/'Test.recipe')); assert pulled['Identifier']=='com.example.Test'
        dest=Path(td)/'out'/'Test.recipe'; m.push('Test.recipe',dest); assert dest.exists(); assert list((Path(td)/'history').glob('*.jsonl'))
