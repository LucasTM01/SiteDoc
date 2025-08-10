from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session

from app.auth.dependencies import get_current_user
from app.db.session import get_session
from app.models.appointment import Appointment, AppointmentStatus
from app.services.scheduling import validate_scheduling_rules
from app.templates import templates

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.get("/new", response_class=HTMLResponse)
def new_appointment_modal(request: Request, _user=Depends(get_current_user)):
    return templates.TemplateResponse("appointments/new_modal.html", {"request": request})


@router.post("/cancel/{appointment_id}")
def cancel_appointment(appointment_id: int, reason: str = Form(""), session: Session = Depends(get_session), _user=Depends(get_current_user)):
    appt = session.get(Appointment, appointment_id)
    if not appt:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    appt.status = AppointmentStatus.CANCELLED
    if reason:
        appt.notes = (appt.notes or "") + f"\nCancelado: {reason}"
    session.add(appt)
    session.commit()
    return RedirectResponse(f"/calendar/{appt.doctor_id}?mode=day&d={appt.start_datetime.date().isoformat()}", status_code=302)


@router.post("/reschedule/{appointment_id}")
def reschedule_appointment(
    appointment_id: int,
    start_datetime: datetime = Form(...),
    end_datetime: datetime = Form(...),
    session: Session = Depends(get_session),
    _user=Depends(get_current_user),
):
    appt = session.get(Appointment, appointment_id)
    if not appt:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    ok, error = validate_scheduling_rules(appt.doctor_id, start_datetime, end_datetime, session)
    if not ok:
        raise HTTPException(status_code=400, detail=error)
    appt.start_datetime = start_datetime
    appt.end_datetime = end_datetime
    session.add(appt)
    session.commit()
    return RedirectResponse(f"/calendar/{appt.doctor_id}?mode=day&d={appt.start_datetime.date().isoformat()}", status_code=302)