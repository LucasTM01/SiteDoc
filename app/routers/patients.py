from __future__ import annotations

from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Form, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session, select

from app.auth.dependencies import get_current_user
from app.db.session import get_session
from app.models.patient import Patient
from app.templates import templates

router = APIRouter(prefix="/patients", tags=["patients"])


@router.get("/", response_class=HTMLResponse)
def list_patients(
    request: Request,
    q: Optional[str] = Query(None),
    session: Session = Depends(get_session),
    _user=Depends(get_current_user),
):
    query = select(Patient)
    if q:
        like = f"%{q}%"
        query = query.where(Patient.name.ilike(like))
    patients = session.exec(query.order_by(Patient.name)).all()
    return templates.TemplateResponse("patients/list.html", {"request": request, "patients": patients, "q": q or ""})


@router.get("/{patient_id}", response_class=HTMLResponse)
def view_patient(
    request: Request,
    patient_id: int,
    session: Session = Depends(get_session),
    _user=Depends(get_current_user),
):
    patient = session.get(Patient, patient_id)
    return templates.TemplateResponse("patients/detail.html", {"request": request, "patient": patient})


@router.post("/new")
def create_patient(
    name: str = Form(...),
    birthdate: date = Form(...),
    document: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    notes: str = Form("") ,
    session: Session = Depends(get_session),
    _user=Depends(get_current_user),
):
    p = Patient(name=name, birthdate=birthdate, document=document, phone=phone, email=email, notes=notes or None)
    session.add(p)
    session.commit()
    return RedirectResponse(f"/patients/{p.id}", status_code=302)