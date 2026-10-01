from pathlib import Path
from flask import Blueprint, request, jsonify
from .editor import RecipeManager

def create_blueprint(root):
    bp=Blueprint('munki',__name__,url_prefix='/api/munki'); mgr=RecipeManager(root)
    @bp.get('/recipes')
    def recipes(): return jsonify(sorted(p.name for p in Path(root).glob('*.recipe')))
    @bp.post('/validate')
    def validate():
        data=request.get_json(force=True); errors=mgr.validate(data); return jsonify({'valid':not errors,'errors':errors})
    @bp.post('/save')
    def save():
        b=request.get_json(force=True); return jsonify({'path':mgr.save(b['name'],b['recipe'])})
    @bp.post('/save-as')
    def save_as():
        b=request.get_json(force=True); return jsonify({'path':mgr.save_as(b['source'],b['name'],b['recipe'])})
    @bp.post('/pull')
    def pull():
        b=request.get_json(force=True); return jsonify({'recipe':mgr.pull(b['source'])})
    @bp.post('/push')
    def push():
        b=request.get_json(force=True); return jsonify({'path':mgr.push(b['name'],b['destination'])})
    return bp
