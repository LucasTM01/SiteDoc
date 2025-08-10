# MVP - Gestão de Agenda Médica (estilo Doctoralia)

Stack: FastAPI + SQLModel (SQLite), Jinja2 + HTMX, Tailwind via CDN, sessão por cookies, pytest.

## Rodando localmente

Requisitos: Python 3.11+

```bash
pip install -r requirements.txt
export SECRET_KEY=super-secret-demo-key
python -m app.db.seed
uvicorn app.main:app --reload
```

Acesse: http://localhost:8000

## Docker

```bash
docker-compose up --build
```

## Seeds e logins demo
- admin: admin@demo.com / Admin123!
- recepção: recepcao@demo.com / Recep123!
- médico: med1@demo.com / Med123!

Rodar seed manualmente:
```bash
python -m app.db.seed
```

## Testes
```bash
pytest -q
```

## Estrutura
```
app/
  main.py
  deps.py
  models/
  routers/
  services/
  templates/
  static/
  auth/
  db/
```

## Critérios atendidos
- CRUD Pacientes/Médicos/Agendas
- Calendário dia/semana/mês por médico
- Agendamento sem conflito e com validações
- API JSON para HTMX
- Conteinerização com seed automático
- Testes básicos passando
