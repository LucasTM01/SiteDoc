from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Generator

from sqlmodel import SQLModel, Session, create_engine

DB_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
engine = create_engine(DB_URL, connect_args={"check_same_thread": False} if DB_URL.startswith("sqlite") else {})


def init_db() -> None:
    """Create all tables if not exist."""
    from app.models.user import User  # noqa: F401
    from app.models.doctor import Doctor  # noqa: F401
    from app.models.patient import Patient  # noqa: F401
    from app.models.availability import Availability  # noqa: F401
    from app.models.appointment import Appointment  # noqa: F401

    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session