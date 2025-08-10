from datetime import datetime, timedelta

from fastapi.testclient import TestClient

from app.main import app
from app.db.seed import run_seed


client = TestClient(app)


def auth_session(email: str, password: str):
    r = client.post("/login", data={"email": email, "password": password})
    assert r.status_code in (200, 302)


def test_login_and_availability_flow():
    run_seed()
    # login recepcao
    r = client.post("/login", data={"email": "recepcao@demo.com", "password": "Recep123!"})
    assert r.status_code in (200, 302)

    # check conflict for an obvious valid slot (tomorrow 09:00)
    tomorrow = (datetime.now() + timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0)
    payload = {
        "doctor_id": 1,
        "start_datetime": tomorrow.isoformat(),
        "end_datetime": (tomorrow + timedelta(minutes=30)).isoformat(),
    }
    r = client.post("/api/appointments/check-conflict", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "ok" in data