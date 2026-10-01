import os
try:
    from openai import OpenAI
except ImportError:
    OpenAI=None
SYSTEM = """You are the LogAgent development assistant. Work only within the supplied project workspace. Propose changes as complete file contents or precise patches. Never claim a change was applied unless the host explicitly applies it. Prefer tests before modifications. Do not expose secrets."""
def ask(message, context=""):
    if OpenAI is None: raise RuntimeError("Install the official openai Python package")
    if not os.environ.get("OPENAI_API_KEY"): raise RuntimeError("OPENAI_API_KEY is not configured on the server")
    client=OpenAI()
    r=client.responses.create(model=os.environ.get("OPENAI_MODEL","gpt-5.6"),instructions=SYSTEM,input=(context+"\n\nUser request:\n"+message) if context else message)
    return {"id":r.id,"model":r.model,"text":r.output_text}
