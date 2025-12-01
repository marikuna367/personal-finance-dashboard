from fastapi import FastAPI
from .db import init_db
from .routers import auth, finances

app = FastAPI(title="Personal Finance Dashboard API")

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(auth.router)
app.include_router(finances.router)

@app.get('/')
def root():
    return {"ok": True, "message": "Personal Finance API"}
