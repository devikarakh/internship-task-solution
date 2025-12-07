Internship Task

This repository contains a FastAPI starter project for backend internship candidates. The goal is to evaluate debugging skills, API design, and MySQL integration.

Scenario

You have inherited a partially built service that supports user registration, login, and storing arbitrary records. Some features are intentionally incomplete or incorrect to mimic real maintenance work. Use the tasks document to guide your contributions.

Prerequisites

Python 3.10+
MySQL 8+ running locally (or in Docker)
Recommended: virtual environment tool such as venv or pipenv
Setup

Clone the repository and install dependencies:
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
Provision a MySQL database (using Docker):
docker run --name internship-mysql -e MYSQL_ROOT_PASSWORD=secret \
  -e MYSQL_DATABASE=internship_task -e MYSQL_USER=intern -e MYSQL_PASSWORD=intern \
  -p 3306:3306 -d mysql:8
Configure the database URL (optional if you used the Docker command above):
export DATABASE_URL="mysql+pymysql://intern:intern@localhost:3306/internship_task"
Apply migrations (the models auto-create tables on startup, but you can also run this script to verify):
python - <<'PY'
from app.database import Base, engine
import app.models

Base.metadata.create_all(bind=engine)
print("Database tables created")
PY
Start the API server:
uvicorn app.main:app --reload
Open the interactive docs at http://127.0.0.1:8000/docs to explore the available routes.
Project structure

app/
  crud.py        # Data access helpers (includes a deliberate auth bug)
  database.py    # SQLAlchemy engine and session configuration
  main.py        # FastAPI routes
  models.py      # ORM models
  schemas.py     # Pydantic schemas
What to work on

Consult tasks.txt for the internship exercises detailing bugs to fix and features to add.