from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select

from app.auth.dependencies import get_current_user
from app.db.session import get_session
from app.models.doctor import Doctor
from app.models.user import User
from app.templates import templates

router = APIRouter(prefix="/doctors", tags=["doctors"])


@router.get("/", response_class=HTMLResponse)
def list_doctors(request: Request, session: Session = Depends(get_session), _user=Depends(get_current_user)):
    doctors = session.exec(select(Doctor)).all()
    users = {u.id: u for u in session.exec(select(User)).all()}
    return templates.TemplateResponse("doctors/list.html", {"request": request, "doctors": doctors, "users": users})