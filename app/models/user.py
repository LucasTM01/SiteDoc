from __future__ import annotations

from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    MEDICO = "MEDICO"
    RECEPCAO = "RECEPCAO"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(index=True, unique=True)
    role: UserRole = Field(default=UserRole.RECEPCAO)
    hashed_password: str
    is_active: bool = Field(default=True)