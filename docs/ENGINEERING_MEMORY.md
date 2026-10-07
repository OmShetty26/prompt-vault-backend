# `docs/ENGINEERING_MEMORY.md`

## Alembic
- **Problem:** Modify existing PostgreSQL schema safely.
- **Approach:** Model change → migration → inspect → upgrade.
- **Key concept:** Models = desired; DB = actual; migration = transformation.
- **Biggest mistake:** Assuming model edits modify an existing DB.
- **Tradeoff:** Extra process gives reproducible schema history.

## User Ownership
- **Problem:** Associate prompts with users.
- **Approach:** `Prompt.user_id → User.id`.
- **Key concept:** One User can own many Prompts; `user_id` is not unique.
- **Biggest mistake:** Initially treating `user_id` as if it should be unique.
- **Tradeoff:** Ownership adds query constraints everywhere.

## Registration
- **Problem:** Create accounts without storing passwords.
- **Approach:** Pydantic validation + Argon2 hash + safe response model.
- **Key concept:** Username identifies; password proves identity.
- **Biggest mistake:** Duplicating validation already handled by Pydantic.
- **Tradeoff:** Frontend may duplicate rules for UX, backend stays authoritative.

## JWT Authentication
- **Problem:** Authenticate subsequent requests.
- **Approach:** Password verification → JWT → HttpOnly cookie.
- **Key concept:** JWT = credential; cookie = transport/storage mechanism.
- **Biggest mistake to avoid:** Returning ORM User without a safe response model.
- **Tradeoff:** Stateless simplicity vs immediate token revocation.

## `/auth/me`
- **Problem:** Frontend loses in-memory user state after refresh.
- **Approach:** Validate cookie and return safe current-user data.
- **Key concept:** Backend reconstructs authenticated identity.
- **Biggest mistake:** Confusing it with credential modification.
- **Tradeoff:** Adds one startup request.

## Authorization
- **Problem:** Logged-in users must not access other users' prompts.
- **Approach:** Scope every prompt query to `current_user.id`.
- **Key concept:** Authentication = who; authorization = allowed to access what.
- **Biggest mistake:** Filtering only by `prompt_id`.
- **Tradeoff:** Slightly more query logic for required security.