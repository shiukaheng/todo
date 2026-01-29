# DAG Todo API - Maintenance & Usage Guide

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                      FastAPI                            │
│  ┌──────────────┐  ┌──────────────┐   ┌──────────────┐  │
│  │ routes.py    │  │ models.py    │   │ sse.py       │  │
│  │ (endpoints)  │  │ (Pydantic)   │   │ (publisher)  │  │
│  └──────┬───────┘  └──────────────┘   └──────┬───────┘  │
│         │                                    │          │
│  ┌──────▼────────────────────────────────────▼───────┐  │
│  │                  core/services.py                 │  │
│  │            (business logic, Cypher queries)       │  │
│  └──────────────────────┬────────────────────────────┘  │
│                         │                               │
│  ┌──────────────────────▼────────────────────────────┐  │
│  │                  core/db.py                       │  │
│  │               (Neo4j driver)                      │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

**Data flow:**
1. Request → `routes.py` → validates with `models.py`
2. Route calls `services.py` functions with Neo4j transaction
3. On mutations, `sse.py` broadcasts to all subscribers

---

## Schema Changes

Neo4j is schemaless—you can add/remove properties freely. The "schema" lives in code:

### Where schema is defined

| File | What to change |
|------|----------------|
| `backend/app/core/services.py` | `Task` dataclass, `_ENRICHMENT` Cypher fragment |
| `backend/app/models.py` | Pydantic models (`TaskOut`, `TaskCreate`, `TaskUpdate`) |

### Adding a new field

Example: adding a `priority` field (int, 1-5).

**Step 1: Update dataclass** (`backend/app/core/services.py`)

```python
@dataclass
class Task:
    id: str
    text: str = ""
    completed: bool = False
    inferred: bool = False
    priority: int = 3          # ← add here
    due: int | None = None
    created_at: int | None = None
    updated_at: int | None = None
```

**Step 2: Update `_node_to_task`** (`backend/app/core/services.py`)

```python
def _node_to_task(node) -> Task:
    d = dict(node)
    return Task(
        ...
        priority=d.get("priority", 3),  # ← add here with default
        ...
    )
```

**Step 3: Update Pydantic models** (`backend/app/models.py`)

```python
class TaskOut(BaseModel):
    ...
    priority: int
    ...

class TaskCreate(TaskBase):
    ...
    priority: int = 3
    ...

class TaskUpdate(BaseModel):
    ...
    priority: int | None = None
    ...
```

**Step 4: Update `add_task` and `update_task`** (`backend/app/core/services.py`)

```python
def add_task(tx, id: str, ..., priority: int = 3, ...):
    props = {
        ...
        "priority": priority,
        ...
    }
```

**Step 5: Update route handlers** (`backend/app/api/routes.py`)

Pass the new field through in `add_task` and `set_task`.

### Adding a computed property

Computed properties are calculated in the `_ENRICHMENT` Cypher fragment. Example: adding `blocked_by_count`.

**Step 1: Update `_ENRICHMENT`** (`backend/app/core/services.py`)

```cypher
...
RETURN t,
       direct_deps,
       size(all_deps) AS blocked_by_count,   -- ← add here
       ...
```

**Step 2: Update `EnrichedTask` dataclass**

```python
@dataclass
class EnrichedTask:
    ...
    blocked_by_count: int = 0
```

**Step 3: Update `_record_to_enriched`**

```python
def _record_to_enriched(record, skip_calculated: bool = False) -> EnrichedTask:
    return EnrichedTask(
        ...
        blocked_by_count=record.get("blocked_by_count", 0),
    )
```

**Step 4: Update `EnrichedTaskOut`** (`backend/app/models.py`)

```python
class EnrichedTaskOut(BaseModel):
    ...
    blocked_by_count: int
```

### Migrations

For existing data, you may need to backfill. Run a Cypher query directly:

```cypher
// Set default priority for existing tasks
MATCH (t:Task) WHERE t.priority IS NULL SET t.priority = 3
```

Or via the Neo4j browser at `http://localhost:7474`.

---

## Client Usage

### Generated TypeScript Client (Recommended)

The REST client is **codegenned** from OpenAPI. SSE requires a small manual wrapper (OpenAPI doesn't spec SSE).

```
client/
├── generate.sh      # Run this to regenerate
├── generated/       # ← Codegenned REST client (don't edit)
├── sse.ts           # ← Manual SSE wrapper
└── index.ts         # Re-exports both
```

**Generate the client:**

```bash
cd client

# Ensure backend is running
npm install -g @openapitools/openapi-generator-cli
./generate.sh http://localhost:8000
```

**Use in your frontend:**

```typescript
import {
  DefaultApi,
  Configuration,
  subscribeToTasks,
  type TaskListOut,
} from './client';

// REST client (codegenned)
const api = new DefaultApi(new Configuration({ basePath: '' }));

// List tasks
const { tasks, has_cycles } = await api.listTasksApiTasksGet();

// Add task
await api.addTaskApiTasksPost({
  taskCreate: { id: 'my-task', text: 'Do something' }
});

// Update task
await api.setTaskApiTasksTaskIdPatch({
  taskId: 'my-task',
  taskUpdate: { completed: true }
});

// Link/unlink
await api.linkTasksApiLinksPost({
  linkRequest: { from_id: 'a', to_id: 'b' }
});
await api.unlinkTasksApiLinksDelete({
  linkRequest: { from_id: 'a', to_id: 'b' }
});

// SSE subscription (manual wrapper, uses generated types)
const unsubscribe = subscribeToTasks((data: TaskListOut) => {
  console.log('Tasks updated:', data.tasks);
});

// Later: unsubscribe();
```

### SSE Events

The `/api/tasks/subscribe` endpoint streams:

| Event | When | Payload |
|-------|------|---------|
| `init` | On connect | Full `TaskListOut` |
| `update` | After any mutation | Full `TaskListOut` |

The SSE wrapper in `client/sse.ts` handles both events identically—your callback just receives the latest state.

### Regenerating After Schema Changes

When you change the backend schema:

1. Update backend (`services.py`, `models.py`)
2. Restart backend
3. Run `./generate.sh` in `client/`
4. TypeScript will show you what broke in your frontend

---

## Development Workflow

### Running locally

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

### Testing changes

```bash
# Health check
curl http://localhost:8000/health

# List tasks
curl http://localhost:8000/api/tasks | jq .

# Test SSE (Ctrl+C to stop)
curl -N http://localhost:8000/api/tasks/subscribe
```

### Adding a new endpoint

1. Add Pydantic model in `backend/app/models.py` (if needed)
2. Add service function in `backend/app/core/services.py`
3. Add route in `backend/app/api/routes.py`
4. Call `await publisher.broadcast()` after mutations
5. Regenerate client: `cd client && ./generate.sh`

---

## Checklist: Schema Change

- [ ] Update `Task` dataclass in `backend/app/core/services.py`
- [ ] Update `_node_to_task()` with default value
- [ ] Update `add_task()` / `update_task()` to accept new field
- [ ] Update Pydantic models in `backend/app/models.py`
- [ ] Update route handlers in `backend/app/api/routes.py` if needed
- [ ] Backfill existing data if needed (Cypher migration)
- [ ] Restart backend
- [ ] **Regenerate client:** `cd client && ./generate.sh`
- [ ] Fix frontend type errors (TypeScript will guide you)
- [ ] Test: add task with new field
- [ ] Test: list tasks shows new field
- [ ] Test: SSE includes new field

---

## Troubleshooting

**SSE not receiving updates:**
- Check that mutations call `await publisher.broadcast()`
- Verify CORS allows the SSE endpoint

**"Task not found" on link:**
- Both task IDs must exist before linking

**"Would create cycle":**
- The link would create a circular dependency—this is prevented

**Schema mismatch errors:**
- Check that Pydantic models match the dataclass
- Check that `_node_to_task` has defaults for all fields
