from __future__ import annotations

import json
import random
from datetime import date, datetime, timedelta, time
from pathlib import Path

from sqlmodel import Session, select

from app.auth.security import hash_password
from app.db.session import engine, init_db
from app.models.appointment import Appointment, AppointmentStatus
from app.models.availability import Availability
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.user import User, UserRole


def load_fixtures() -> dict:
    fixtures_path = Path(__file__).parents[2] / "fixtures.json"
    with open(fixtures_path, "r", encoding="utf-8") as f:
        return json.load(f)


def seed_users(session: Session) -> None:
    users = [
        ("Admin", "admin@demo.com", UserRole.ADMIN, "Admin123!"),
        ("Recepção", "recepcao@demo.com", UserRole.RECEPCAO, "Recep123!"),
        ("Dr. João", "med1@demo.com", UserRole.MEDICO, "Med123!"),
        ("Dra. Maria", "med2@demo.com", UserRole.MEDICO, "Med123!"),
        ("Dr. Pedro", "med3@demo.com", UserRole.MEDICO, "Med123!"),
        ("Dra. Ana", "med4@demo.com", UserRole.MEDICO, "Med123!"),
        ("Dr. Carlos", "med5@demo.com", UserRole.MEDICO, "Med123!"),
    ]
    for name, email, role, raw in users:
        if not session.exec(select(User).where(User.email == email)).first():
            session.add(User(name=name, email=email, role=role, hashed_password=hash_password(raw)))
    session.commit()


def seed_doctors(session: Session, fixtures: dict) -> list[Doctor]:
    specialties = fixtures["specialties"]
    clinics = fixtures["clinics"]
    doctors: list[Doctor] = []
    user_ids = [u.id for u in session.exec(select(User).where(User.role == UserRole.MEDICO)).all()]
    for i, uid in enumerate(user_ids):
        crm = f"CRM-{1000+i}"
        d = session.exec(select(Doctor).where(Doctor.user_id == uid)).first()
        if not d:
            d = Doctor(user_id=uid, specialty=specialties[i % len(specialties)], crm=crm, clinic_name=clinics[i % len(clinics)])
            session.add(d)
            session.commit()
            session.refresh(d)
        doctors.append(d)
    return doctors


def seed_patients(session: Session, fixtures: dict, count: int = 30) -> list[Patient]:
    first = fixtures["patient_first_names"]
    last = fixtures["patient_last_names"]
    patients: list[Patient] = []
    for i in range(count):
        name = f"{random.choice(first)} {random.choice(last)}"
        email = f"pac{i}@demo.com"
        existing = session.exec(select(Patient).where(Patient.email == email)).first()
        if existing:
            patients.append(existing)
            continue
        p = Patient(
            name=name,
            birthdate=date(1980 + random.randint(0, 30), random.randint(1, 12), random.randint(1, 28)),
            document=f"DOC{i:04d}",
            phone=f"(11) 9{random.randint(1000,9999)}-{random.randint(1000,9999)}",
            email=email,
            notes="",
        )
        session.add(p)
        session.commit()
        session.refresh(p)
        patients.append(p)
    return patients


def seed_availability(session: Session, doctors: list[Doctor]) -> None:
    for d in doctors:
        # Clear old
        for old in session.exec(select(Availability).where(Availability.doctor_id == d.id)).all():
            session.delete(old)
        session.commit()
        # Mon-Fri 08:00-17:00
        for wd in range(0, 5):
            session.add(Availability(doctor_id=d.id, weekday=wd, start_time=time(8, 0), end_time=time(17, 0)))
        session.commit()


def seed_appointments(session: Session, doctors: list[Doctor], patients: list[Patient], approx: int = 50) -> None:
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    times = [time(h, 0) for h in range(8, 17)]
    created = 0
    for _ in range(approx * 2):  # try more to skip conflicts
        d = random.choice(doctors)
        p = random.choice(patients)
        day = start_of_week + timedelta(days=random.randint(0, 4))
        t = random.choice(times)
        start_dt = datetime.combine(day, t)
        end_dt = start_dt + timedelta(minutes=30)
        # conflict check
        conflict = session.exec(
            select(Appointment).where(
                (Appointment.doctor_id == d.id) & (Appointment.status != AppointmentStatus.CANCELLED)
            )
        ).all()
        if any(not (end_dt <= a.start_datetime or start_dt >= a.end_datetime) for a in conflict):
            continue
        session.add(Appointment(doctor_id=d.id, patient_id=p.id, start_datetime=start_dt, end_datetime=end_dt, status=AppointmentStatus.BOOKED))
        created += 1
        if created >= approx:
            break
    session.commit()


def run_seed() -> None:
    init_db()
    fixtures = load_fixtures()
    with Session(engine) as session:
        seed_users(session)
        doctors = seed_doctors(session, fixtures)
        patients = seed_patients(session, fixtures)
        seed_availability(session, doctors)
        seed_appointments(session, doctors, patients)
    print("Seed concluído.")


if __name__ == "__main__":
    run_seed()