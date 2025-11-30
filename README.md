# README

## Library Management System  
**PostgreSQL + SQLAlchemy + FastAPI + Full CRUD + Tests + Swagger UI**

A clean, production-ready backend API for managing a library (Authors & Books) with:
- PostgreSQL (via Docker)
- SQLAlchemy 2.0+ ORM
- FastAPI (automatic interactive docs)
- Complete CRUD operations
- Professional testing with `pytest`
- In-memory SQLite for fast, isolated tests

---

#### Live Demo
After starting:  
- **Swagger UI**: http://127.0.0.1:8000/docs  
- **ReDoc**: http://127.0.0.1:8000/redoc

---

#### Features
- Full CRUD for `Author` and `Book`
- One-to-Many relationship (Author → Books)
- Automatic OpenAPI documentation (Swagger + ReDoc)
- Dependency injection with `Depends(get_db)`
- Clean separation: `database.py`, `models.py`, `main.py`
- Professional test suite using in-memory SQLite
- Dockerized PostgreSQL (no local install needed)

---

#### Project Structure
```
postgreslib/
├── .venv/                  # (ignored)
├── tests/                  ← Full test suite
│   ├── test_database.py    ← Test DB setup (SQLite in-memory)
│   └── test_main.py        ← All API endpoint tests
├── database.py             ← SQLAlchemy engine & session
├── models.py               ← Author & Book ORM models
├── main.py                 ← FastAPI app with full CRUD
├── docker-compose.yml      ← PostgreSQL container
├── requirements.txt        ← (optional) pin dependencies
├── pytest.ini              ← Fixes test imports
└── README.md               ← This file
```

---

#### Quick Start

##### 1. Clone & Enter Project
```bash
git clone https://github.com/your-username/postgreslib.git
cd postgreslib
```

##### 2. Create Virtual Environment
```bash
python -m venv .venv
.\.venv\Scripts\activate        # Windows
# source .venv/bin/activate     # macOS/Linux
```

##### 3. Install Dependencies
```bash
pip install sqlalchemy psycopg2-binary fastapi uvicorn pydantic pytest httpx
```

##### 4. Start PostgreSQL (Docker)
```bash
docker-compose up -d
```

##### 5. Run the API
```bash
uvicorn main:app --reload
```

→ Open http://127.0.0.1:8000/docs and play with the API!

---

#### Run Tests
```bash
python -m pytest -v
# or just: pytest -v
```

All 10+ tests use an in-memory SQLite database → super fast and safe.  
Tests cover:
- Create, Read, Update, Delete for Authors & Books
- Relationship handling (`author_name` in book responses)
- 404 error handling
- Full isolation (DB resets between tests)

---

#### API Endpoints (Auto-documented)

| Method | Endpoint             | Description                   |
|--------|----------------------|-------------------------------|
| POST   | `/authors/`          | Create author                 |
| GET    | `/authors/`          | List all authors              |
| GET    | `/authors/{id}`      | Get one author                |
| PUT    | `/authors/{id}`      | Update author                 |
| DELETE | `/authors/{id}`      | Delete author                 |
| POST   | `/books/`            | Create book (needs author_id) |
| GET    | `/books/`            | List all books + author name  |
| GET    | `/books/{id}`        | Get one book                  |
| PUT    | `/books/{id}`        | Update book                   |
| DELETE | `/books/{id}`        | Delete book                   |

---

#### Git Workflow
Always:
```bash
git pull origin main
git checkout -b feature/your-feature-name
# ... make changes
git add .
git commit -m "feat: add X / fix: Y"
git push origin HEAD
```
→ Open a Pull Request on GitHub

Use conventional commits: `feat:`, `fix:`, `test:`, `docs:`, `refactor:`, `chore:`

---

#### .gitignore (already set up)
Ignores:
- `.venv/`
- `__pycache__/`
- `.idea/`, `.vscode/`
- logs, OS files

---

