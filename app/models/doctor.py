from __future__ import annotations

from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class Doctor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    specialty: str
    crm: str
    clinic_name: str