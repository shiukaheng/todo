# Todo

DAG-based task management with real-time updates.

## Components

### Backend (`/backend`)

FastAPI server with Neo4j graph database.

**Features:**
- Task CRUD with DAG dependencies
- Real-time updates via SSE
- Automatic cycle detection

**Run locally:**
```bash
cd backend
pip install -e .
NEO4J_URL=bolt://localhost:7687 NEO4J_USER=neo4j NEO4J_PASSWORD=password uvicorn app.main:app --reload
```

**Docker:**
```bash
docker build -t todo-api .
docker run -p 8000:8000 -e NEO4J_URL=bolt://host.docker.internal:7687 -e NEO4J_PASSWORD=password todo-api
```

**Environment variables:**
| Variable | Default | Description |
|----------|---------|-------------|
| `NEO4J_URL` | `bolt://localhost:7687` | Neo4j connection URL |
| `NEO4J_USER` | `neo4j` | Neo4j username |
| `NEO4J_PASSWORD` | - | Neo4j password |

### Client (`/client`)

TypeScript client library for the API.

**Install:**
```bash
npm install github:shiukaheng/todo
```

**Usage:**
```typescript
import { DefaultApi, Configuration, subscribeToTasks } from 'todo-client';

// REST API
const api = new DefaultApi(new Configuration({ basePath: 'http://localhost:8000' }));
const tasks = await api.listTasksApiTasksGet();

// Real-time updates via SSE
const unsubscribe = subscribeToTasks(
  (data) => console.log(data.tasks),
  { baseUrl: 'http://localhost:8000' }
);
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks` | List all tasks |
| POST | `/api/tasks` | Create task |
| GET | `/api/tasks/{id}` | Get task |
| PUT | `/api/tasks/{id}` | Update task |
| DELETE | `/api/tasks/{id}` | Delete task |
| POST | `/api/tasks/{id}/link/{target}` | Add dependency |
| DELETE | `/api/tasks/{id}/link/{target}` | Remove dependency |
| GET | `/api/tasks/subscribe` | SSE subscription |
| GET | `/health` | Health check |

## Related

- [todo-gui](https://github.com/shiukaheng/todo-gui) - Graph visualization frontend
- [todo-docker-compose](https://github.com/shiukaheng/todo-docker-compose) - Full stack deployment
