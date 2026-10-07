# `docs/ADRS.md`

## ADR-001 — Use PostgreSQL + SQLAlchemy

**Status:** Accepted

**Context:** PromptVault needs relational users, prompts, ownership, and future vector search.

**Decision:** Use PostgreSQL with SQLAlchemy ORM.

**Why:** Strong relational constraints, production relevance, future `pgvector` support.

**Alternatives:** SQLite; raw SQL.

**Tradeoff:** More setup than SQLite.

---

## ADR-002 — Use Alembic for Schema Evolution

**Status:** Accepted

**Context:** Existing database tables must change safely over time.

**Decision:** Manage schema changes with versioned Alembic migrations.

**Why:** Explicit, reproducible upgrade history.

**Alternative:** `Base.metadata.create_all()`.

**Tradeoff:** Every meaningful schema change requires a migration.

---

## ADR-003 — User Owns Many Prompts

**Status:** Accepted

**Context:** Users must only access their own prompts.

**Decision:** `Prompt.user_id` is a foreign key to `User.id`.

**Why:** Represents ownership directly and enables database integrity.

**Tradeoff:** Existing ownerless prompts required staged migration handling.

---

## ADR-004 — Use Argon2 Password Hashing

**Status:** Accepted

**Context:** Plaintext passwords must never be stored.

**Decision:** Use `pwdlib` with its recommended Argon2 password hashing.

**Why:** Secure modern password hashing with salt/verification handled by the library.

**Alternative:** Manual hashing or weaker algorithms.

**Tradeoff:** Hashing is deliberately computationally expensive.

---

## ADR-005 — JWT in HttpOnly Cookie

**Status:** Accepted

**Context:** Authentication must persist across browser requests and refreshes.

**Decision:** Issue short-lived JWTs containing `sub=user.id` and store them in an HttpOnly cookie.

**Why:** Simple stateless authentication; browser manages credential transport; JS cannot directly read the token.

**Alternatives:** Bearer token stored in JavaScript; server sessions.

**Tradeoff:** Cookie auth requires CSRF awareness and logout does not inherently revoke copied JWTs.

---

## ADR-006 — No JWT Revocation Initially

**Status:** Accepted

**Context:** Immediate revocation requires additional server-side state.

**Decision:** Logout deletes the browser cookie; no denylist/session registry.

**Why:** 30-minute tokens and PromptVault's security needs do not justify extra complexity.

**Alternative:** Revocation table/Redis/session store.

**Tradeoff:** A copied JWT remains usable until expiry.

---

## ADR-007 — Centralize Authentication in `get_current_user`

**Status:** Accepted

**Context:** Protected routes otherwise duplicate cookie/JWT/user lookup logic.

**Decision:** Use a reusable FastAPI dependency returning the authenticated User.

**Why:** Centralizes authentication and exposes `current_user.id` to routes.

**Tradeoff:** Protected routes depend on FastAPI's dependency system.

---

## ADR-008 — Scope Prompt Queries by Ownership

**Status:** Accepted

**Context:** Authentication alone does not stop cross-user resource access.

**Decision:** Prompt queries include both prompt ID and current user ID.

**Why:** Enforces resource-level authorization.

**Alternative:** Fetch by ID and check ownership afterward.

**Tradeoff:** Every resource operation requires ownership context.

---

## ADR-009 — Return 404 for Inaccessible Prompts

**Status:** Accepted

**Context:** Returning 403 could reveal another user's prompt exists.

**Decision:** Ownership-scoped queries return 404 when no matching prompt exists.

**Why:** Avoids leaking resource existence.

**Tradeoff:** Client cannot distinguish nonexistent vs other-user resource.

---

## ADR-010 — Keep Secrets Outside Git

**Status:** Accepted

**Context:** JWT secrets and future production credentials must remain private.

**Decision:** Use environment variables; ignore `.env`; commit `.env.example`.

**Why:** Keeps secrets out of source control and supports environment-specific configuration.

**Tradeoff:** Runtime environments must supply configuration.