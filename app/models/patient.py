from __future__ import annotations

from datetime import date
from typing import Optional

from sqlmodel import SQLModel, Field


class Patient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    birthdate: date
    document: str
    phone: str
    email: str
    notes: str | None = None