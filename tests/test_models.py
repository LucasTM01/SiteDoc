from datetime import datetime, date, time

from app.models.user import User, UserRole
from app.models.appointment import Appointment, AppointmentStatus
from app.models.patient import Patient
from app.models.doctor import Doctor


def test_user_role_enum():
    assert UserRole.ADMIN.value == "ADMIN"


def test_appointment_status_enum():
    assert AppointmentStatus.BOOKED.value == "BOOKED"


def test_models_can_init():
    u = User(name="Test", email="t@example.com", role=UserRole.ADMIN, hashed_password="x")
    p = Patient(name="P", birthdate=date.today(), document="D", phone="1", email="e@example.com")
    d = Doctor(user_id=1, specialty="Cardio", crm="CRM-1", clinic_name="Clin")
    a = Appointment(doctor_id=1, patient_id=1, start_datetime=datetime.now(), end_datetime=datetime.now())
    assert u.name and p.name and d.specialty and a.doctor_id == 1