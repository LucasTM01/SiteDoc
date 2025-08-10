from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel


class AppointmentCreate(BaseModel):
    doctor_id: int
    patient_id: int
    start_datetime: datetime
    end_datetime: datetime
    notes: str | None = None


class AppointmentCheck(BaseModel):
    doctor_id: int
    start_datetime: datetime
    end_datetime: datetime