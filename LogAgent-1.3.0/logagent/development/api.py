import os
from flask import Blueprint, request, jsonify
from .workspace import WorkspaceManager
from .chatgpt import ask

def create_blueprint(root):
    bp=Blueprint("development",__name__,url_prefix="/api/development")
    ws=WorkspaceManager(root)
    @bp.get("/tree")
    def tree(): return jsonify(ws.tree(request.args.get("path",".")))
    @bp.get("/file")
    def file(): return jsonify({"path":request.args["path"],"content":ws.read(request.args["path"])})
    @bp.post("/diff")
    def diff():
        b=request.get_json(force=True); return jsonify({"diff":ws.diff(b["path"],b["content"])})
    @bp.post("/apply")
    def apply():
        b=request.get_json(force=True); return jsonify(ws.apply(b["path"],b["content"],b.get("reason","chatgpt")))
    @bp.post("/test")
    def test():
        b=request.get_json(force=True); r=ws.run_tests(b.get("command","pytest -q")); return jsonify({"returncode":r.returncode,"stdout":r.stdout,"stderr":r.stderr,"passed":r.returncode==0})
    @bp.post("/chat")
    def chat():
        b=request.get_json(force=True); context=""
        if b.get("path") and b.get("content"): context=f"Current file: {b['path']}\n```\n{b['content'][:200000]}\n```"
        return jsonify(ask(b["message"],context))
    @bp.get("/history")
    def history(): return jsonify(ws.history_list())
    @bp.get("/config")
    def config(): return jsonify({"configured":bool(os.environ.get("OPENAI_API_KEY")),"model":os.environ.get("OPENAI_MODEL","gpt-5.6")})
    return bp
