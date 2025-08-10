from __future__ import annotations

from datetime import datetime, time
from typing import Iterable

from sqlmodel import Session, select

from app.models.appointment import Appointment, AppointmentStatus
from app.models.availability import Availability


def times_overlap(start_a: datetime, end_a: datetime, start_b: datetime, end_b: datetime) -> bool:
    return start_a < end_b and end_a > start_b


def is_within_availability(doctor_id: int, start_dt: datetime, end_dt: datetime, session: Session) -> bool:
    weekday = start_dt.weekday()
    if start_dt.date() != end_dt.date():
        return False
    avails = session.exec(
        select(Availability).where(
            (Availability.doctor_id == doctor_id) & (Availability.weekday == weekday)
        )
    ).all()
    if not avails:
        return False
    start_t, end_t = start_dt.time(), end_dt.time()
    for a in avails:
        if a.start_time <= start_t and end_t <= a.end_time:
            return True
    return False


def has_conflict(doctor_id: int, start_dt: datetime, end_dt: datetime, session: Session) -> bool:
    appointments = session.exec(
        select(Appointment).where(
            (Appointment.doctor_id == doctor_id)
            & (Appointment.status != AppointmentStatus.CANCELLED)
        )
    ).all()
    for appt in appointments:
        if times_overlap(start_dt, end_dt, appt.start_datetime, appt.end_datetime):
            return True
    return False


def validate_scheduling_rules(doctor_id: int, start_dt: datetime, end_dt: datetime, session: Session) -> tuple[bool, str | None]:
    if end_dt <= start_dt:
        return False, "Horário final deve ser após o inicial"
    if not is_within_availability(doctor_id, start_dt, end_dt, session):
        return False, "Fora do horário de atendimento"
    if has_conflict(doctor_id, start_dt, end_dt, session):
        return False, "Conflito de agenda (overbooking)"
    return True, None