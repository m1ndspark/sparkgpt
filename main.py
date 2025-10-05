from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/healthz", response_class=PlainTextResponse)
def healthz():
    return "ok"
