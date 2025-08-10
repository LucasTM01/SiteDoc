from __future__ import annotations

from datetime import time
from typing import Optional

from sqlmodel import SQLModel, Field


class Availability(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    doctor_id: int = Field(foreign_key="doctor.id")
    weekday: int = Field(description="0=Monday .. 6=Sunday")
    start_time: time
    end_time: time