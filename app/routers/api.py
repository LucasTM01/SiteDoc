from __future__ import annotations

from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.auth.dependencies import get_current_user
from app.db.session import get_session
from app.models.appointment import Appointment
from app.schemas.appointment import AppointmentCheck, AppointmentCreate
from app.services.scheduling import validate_scheduling_rules

router = APIRouter(prefix="/api", tags=["api"])


@router.get("/availability/{doctor_id}")
def api_availability(doctor_id: int, date: str, session: Session = Depends(get_session), _user=Depends(get_current_user)):
    target = datetime.fromisoformat(date)
    # Very simplified: return hourly slots 08-17 that pass validation
    slots: list[dict] = []
    for hour in range(8, 18):
        start_dt = target.replace(hour=hour, minute=0, second=0, microsecond=0)
        end_dt = start_dt + timedelta(minutes=30)
        ok, error = validate_scheduling_rules(doctor_id, start_dt, end_dt, session)
        if ok:
            slots.append({"start": start_dt.isoformat(), "end": end_dt.isoformat()})
    return {"slots": slots}


@router.post("/appointments/check-conflict")
def check_conflict(payload: AppointmentCheck, session: Session = Depends(get_session), _user=Depends(get_current_user)):
    ok, error = validate_scheduling_rules(payload.doctor_id, payload.start_datetime, payload.end_datetime, session)
    return {"ok": ok, "error": error}


@router.post("/appointments/create")
def create_appointment(payload: AppointmentCreate, session: Session = Depends(get_session), _user=Depends(get_current_user)):
    ok, error = validate_scheduling_rules(payload.doctor_id, payload.start_datetime, payload.end_datetime, session)
    if not ok:
        raise HTTPException(status_code=400, detail=error or "Inválido")
    appt = Appointment(**payload.model_dump())
    session.add(appt)
    session.commit()
    session.refresh(appt)
    return {"id": appt.id}