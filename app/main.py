from __future__ import annotations

import os
from pathlib import Path

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles
from sqlmodel import Session

from app.db.session import init_db
from app.templates import templates
from app.auth.dependencies import get_current_user
from app.routers import auth as auth_router
from app.routers import patients as patients_router
from app.routers import doctors as doctors_router
from app.routers import appointments as appointments_router
from app.routers import api as api_router
from app.routers import calendar as calendar_router

app = FastAPI(title="Agenda Médica")

# Sessions
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY, session_cookie="session")

# Static
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/", response_class=HTMLResponse)
def home(request: Request, _user=Depends(get_current_user)):
    return templates.TemplateResponse("home.html", {"request": request})


# Routers
app.include_router(auth_router.router)
app.include_router(patients_router.router)
app.include_router(doctors_router.router)
app.include_router(appointments_router.router)
app.include_router(api_router.router)
app.include_router(calendar_router.router)