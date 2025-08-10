from __future__ import annotations

from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select

from app.auth.dependencies import get_current_user
from app.db.session import get_session
from app.models.appointment import Appointment, AppointmentStatus
from app.models.doctor import Doctor
from app.templates import templates

router = APIRouter(prefix="/calendar", tags=["calendar"])


@router.get("/{doctor_id}", response_class=HTMLResponse)
def calendar_view(
    request: Request,
    doctor_id: int,
    mode: str = Query("day", pattern="^(day|week|month)$"),
    d: str | None = None,
    session: Session = Depends(get_session),
    _user=Depends(get_current_user),
):
    today = date.fromisoformat(d) if d else date.today()
    doctor = session.get(Doctor, doctor_id)
    appts = session.exec(select(Appointment).where((Appointment.doctor_id == doctor_id))).all()
    return templates.TemplateResponse(
        "calendar/view.html",
        {
            "request": request,
            "doctor": doctor,
            "mode": mode,
            "today": today,
            "appointments": appts,
        },
    )