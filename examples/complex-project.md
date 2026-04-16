# Example: building a full-stack task management app

Nexus Cortexia handling a larger project with multiple services,
authentication, and a frontend.

## User prompt

> Build a task management web app with a FastAPI backend, React frontend,
> PostgreSQL database, JWT auth, and real-time updates via WebSockets.

## Phase 1: Decompose

```
Task graph: task management app

Full-stack app with auth, CRUD, and real-time updates.

Wave 1 (3 tasks, parallel)
- [task-1] Project scaffolding and config — trivial
  Set up monorepo: /backend (FastAPI), /frontend (React+Vite), docker-compose
  for PostgreSQL. Environment config with pydantic-settings.
  Acceptance: docker-compose up starts Postgres, backend serves /health.

- [task-2] Database models and migrations — simple
  SQLAlchemy models: User (id, email, password_hash, created_at),
  Task (id, title, description, status, assignee_id, created_at, updated_at).
  Alembic migration.
  Acceptance: migrate creates tables, models match schema.

- [task-3] Auth module — moderate
  JWT auth: register (POST /auth/register), login (POST /auth/login),
  refresh (POST /auth/refresh). Bcrypt password hashing. 15-min access tokens,
  7-day refresh tokens. Dependency injection for protected routes.
  Acceptance: full auth flow works. Expired tokens return 401.

Wave 2 (2 tasks, after wave 1)
- [task-4] Task CRUD API [depends: task-2, task-3] — simple
  GET/POST/PUT/DELETE for /tasks. Filtered by assignee. Pagination.
  Protected by auth middleware.
  Acceptance: all CRUD operations work. Only task owner can modify.

- [task-5] WebSocket real-time updates [depends: task-2, task-3] — moderate
  WebSocket endpoint at /ws. Broadcasts task creation, update, deletion
  to connected clients. Auth via token in connection params.
  Acceptance: creating a task in one browser tab appears in another.

Wave 3 (2 tasks, after wave 2)
- [task-6] React frontend: auth pages [depends: task-3] — simple
  Login and register pages. Token storage in memory (not localStorage).
  Auth context provider. Protected route wrapper.
  Acceptance: can register, login, and access protected pages.

- [task-7] React frontend: task board [depends: task-4, task-5] — moderate
  Kanban board with columns: todo, in-progress, done. Drag-and-drop to
  change status. Real-time updates via WebSocket.
  Acceptance: tasks appear on board, drag changes status, updates are live.

Wave 4 (1 task, after wave 3)
- [task-8] Integration tests and error handling [depends: all] — simple
  Test the full flow: register, login, create task, move task, verify
  WebSocket update. Error handling for edge cases.
  Acceptance: all integration tests pass.

Summary: 8 tasks in 4 waves. 1 trivial, 4 simple, 3 moderate.
Team: architect + implementer + reviewer (3 agents).
Consensus needed for: task-3, task-5, task-7.
```

## Phase 2: Consensus (task-3 example)

**Architect proposes:** Use python-jose for JWT, bcrypt via passlib. Store
refresh tokens in database (not just signed JWTs) so they can be revoked.
Token rotation on refresh: issue new refresh token, invalidate old one.

**Reviewer approves with modification:** also add rate limiting on login
endpoint (5 attempts per minute per IP) using slowapi.

**Implementer approves.**

**Agreement: 0.83 (1.0 + 0.5 + 1.0 / 3). Proceed with rate limiting added.**

## Phase 3: Execute

Wave 1 tasks dispatched in parallel. Each agent gets only its task spec
and the agreed approach. No cross-contamination of context.

Wave 2 agents receive compressed outputs from wave 1:
- Database model interfaces (field names, types, relationships)
- Auth dependency injection function signature
- File paths for imports

Not the full implementations. Just what they need to build against.

## Phase 4: Review

Task-5 review catches a CRITICAL issue: WebSocket connection doesn't validate
the auth token before accepting messages. One retry fixes it with a
connection middleware that verifies the token on connect.

Task-7 review flags a WARN: the drag-and-drop library isn't imported in
package.json. Fixed during retry.

## Token summary

```
Decomposition:     ~1,500 tokens
Consensus (x3):    ~9,000 tokens
Execution (x8):    ~48,000 tokens
Review (x7):       ~10,500 tokens
Retries (x2):      ~8,000 tokens
Total:             ~77,000 tokens
```

A comparable unstructured conversation: 200,000-350,000 tokens, with at
least 2-3 complete rewrites of components that were built on wrong
assumptions. The 30,000 tokens spent on planning and discussion saved an
estimated 150,000+ tokens in avoided rework.
