# CLAUDE.md

## Project Overview

Slate EV Truck API — a FastAPI REST API serving specifications, features, and pricing data for the Slate EV truck. Data is imported from CSV into SQLite on first startup. The API is consumed by fan sites and documentation portals. Deployed via Netlify (docs) and Railway/Render (API).

## Workflow

- **Small changes** (single file, typo, bug fix): implement directly
- **Multi-file changes or new patterns** (3+ files, new subsystem, unfamiliar area): use `/design` to research the codebase and propose an approach before implementing — wait for approval before writing code
- Always run `/gates` before finishing any task

## Quick Reference

| Aspect          | Value                               |
|-----------------|-------------------------------------|
| Language        | Python 3.11                         |
| Framework       | FastAPI 0.104                       |
| ORM             | SQLAlchemy 2.0                      |
| Validation      | Pydantic 2.5                        |
| Database        | SQLite (file-based)                 |
| Package manager | pip                                 |
| Test framework  | pytest                              |
| Run server      | `uvicorn main:app --reload`         |
| Run tests       | `python -m pytest`                  |
| Security scan   | `bash scripts/security-check.sh`    |
| **All checks**  | **`/gates`**                        |

## Development Commands

```bash
# Development
uvicorn main:app --reload

# Quality gates (run before every commit)
python -m pytest && bash scripts/security-check.sh

# Individual checks
python -m pytest tests/test_architecture.py -v   # Architecture guardrails
bash scripts/security-check.sh                    # Security scan
bash scripts/security-check.sh --strict           # Security scan (fail on warnings)
```

## Architecture

### Directory Map

```text
app/
├── api/
│   └── endpoints.py     # All FastAPI route definitions
├── core/
│   └── config.py         # Pydantic settings (env vars, paths)
├── db/
│   └── session.py        # SQLAlchemy engine, SessionLocal, Base, get_db
├── models/
│   └── vehicle.py        # SQLAlchemy ORM models (Vehicle, Feature, etc.)
├── schemas/
│   └── vehicle.py        # Pydantic response schemas
└── services/
    └── csv_import.py     # CSV-to-database import logic
data/
└── slate.csv             # Source data (committed)
main.py                   # FastAPI app creation, startup event, router mounting
```

### Starting Points

| Task                    | Start Here              | Why                                   |
|-------------------------|-------------------------|---------------------------------------|
| Add/change endpoints    | `app/api/endpoints.py`  | All routes live here                  |
| Change data models      | `app/models/vehicle.py` | ORM models; schemas must match        |
| Change API responses    | `app/schemas/vehicle.py`| Pydantic schemas control serialization|
| Database configuration  | `app/db/session.py`     | Engine, session factory, Base         |
| App startup / mounting  | `main.py`               | Router inclusion, startup event       |

## Code Conventions

### Database Access

**Rule:** Only `app/db/session.py` creates the database engine. All other modules get sessions via the `get_db()` dependency.
**Bug it prevents:** Direct engine creation bypasses connection management and makes testing impossible.

```python
# WRONG — in any file other than app/db/session.py
from sqlalchemy import create_engine
engine = create_engine("sqlite:///my.db")

# CORRECT — in endpoints, services, etc.
from app.db.session import get_db
def my_endpoint(db: Session = Depends(get_db)):
    ...
```

### Import Order

**Rule:** stdlib → third-party → local (`app.`). No circular imports.

### No Dangerous Functions

**Rule:** Never use `eval()`, `exec()`, `os.system()`, or `os.popen()` in application code.
**Bug it prevents:** Code injection from untrusted input.

### SQL Safety

**Rule:** Never build SQL with f-strings or `%` formatting. Use SQLAlchemy ORM methods or parameterized queries.
**Bug it prevents:** SQL injection.

## Architecture Decisions

These choices are intentional. Do not suggest alternatives unless explicitly asked.

- **SQLite over PostgreSQL**: Single-user fan API; file-based DB simplifies deployment
- **SQLAlchemy ORM over raw SQL**: Type safety, relationship management, migration support
- **Pydantic v2 over v1**: Performance and strict mode validation
- **CSV import on startup over migration seeds**: Data comes from a single canonical CSV

## Data Integrity Rules

- **Never cap results with array slicing** (no `[:20]` or `.slice(0, 100)`) unless it's a deliberate, documented parameter. If 50 items were collected, all 50 must be returned.
- **Per-item error handling in loops is mandatory.** A single outer try/catch means one bad item kills processing for everything after it.

## Environment Variables

| Variable         | Required | Purpose                          |
|------------------|----------|----------------------------------|
| `SQLITE_DB_PATH` | No       | Override default DB path         |
| `DATABASE_URL`   | No       | Alternative DB connection string |

## Debug Playbook

### If tests fail

- Run `python -m pytest tests/test_architecture.py -v` to see which architectural rule was violated
- Check the test output for the specific file and line number

### If the server won't start

- Check that `data/slate.csv` exists (required for first-run data import)
- Check that no other process is using port 8000

### If security-check.sh reports findings

- Run `bash scripts/security-check.sh` to see warnings
- Each finding includes the file, line number, and pattern matched
- Fix the pattern or add to the allowlist if it's a false positive
