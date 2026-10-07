# `docs/ARCHITECTURE.md`

## Stack
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic
- pwdlib / Argon2
- PyJWT

## File Responsibilities

```text
main.py
→ routes and request orchestration

models.py
→ SQLAlchemy ORM models

schemas.py
→ Pydantic API schemas

database.py
→ engine/session/get_db

security.py
→ password hashing, verification and JWT creation

config.py
→ environment configuration

alembic/
→ schema migrations
```

## Data Model

```text
User
├── id PK
├── username UNIQUE NOT NULL
└── password_hash NOT NULL

User 1 ─────< Prompt

Prompt
├── id PK
├── title
├── category
├── content
├── is_pinned
├── last_opened_at
└── user_id FK → User.id
```

Each Prompt belongs to one User.

## Authentication

Registration:

```text
username/password
→ validate
→ hash password
→ store User
```

Login:

```text
username/password
→ verify password
→ JWT(sub=user.id, exp)
→ HttpOnly cookie
```

Current user:

```text
cookie
→ verify JWT
→ read sub
→ query User
→ return User ORM object
```

`GET /auth/me` returns safe current-user information.

Logout deletes the authentication cookie.

## Authorization

All prompt endpoints require authentication.

Lists:

```text
Prompt.user_id == current_user.id
```

Single-resource queries:

```text
Prompt.id == requested_id
AND
Prompt.user_id == current_user.id
```

New prompts receive:

```python
user_id=current_user.id
```

The frontend never chooses prompt ownership.

## Database Changes

Schema changes use:

```text
change SQLAlchemy model
→ alembic revision --autogenerate
→ inspect migration
→ alembic upgrade head
→ verify PostgreSQL
```

Alembic, not `create_all()`, owns ongoing schema evolution.

## Configuration

Secrets such as JWT signing keys live in environment variables.

```text
.env
→ local real values, ignored

.env.example
→ required-variable template, committed
```