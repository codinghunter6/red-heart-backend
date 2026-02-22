# Red Heart Backend (FastAPI)

Copy `.env.example` to `.env` and set your variables.

```bash
cd red-heart-backend
copy .env.example .env   # Windows
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API: http://localhost:8000  
Docs: http://localhost:8000/docs

## Project structure

```
red-heart-backend/
├── app/
│   ├── main.py           # FastAPI app, CORS, lifespan
│   ├── config.py         # Settings (from .env)
│   ├── core/             # Database, security, Redis
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   └── api/v1/           # API routes (endpoints, router)
├── celery_app.py         # Celery app (broker: Redis)
├── requirements.txt
├── .env.example
└── README.md
```
