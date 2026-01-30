# Todo Client Library

A TypeScript client library for the DAG Todo API. This library provides a fully typed interface for managing tasks with DAG (Directed Acyclic Graph) dependencies and real-time updates via Server-Sent Events (SSE).

## Installation

Install directly from GitHub:

```bash
# Install from GitHub
npm install github:shiukaheng/todo

# Or install from a specific branch or commit
npm install github:shiukaheng/todo#main
npm install github:shiukaheng/todo#v1.0.0

# For private repositories, ensure you're authenticated with GitHub
# GitHub will use your SSH key or personal access token automatically
```

The package will automatically build when installed (via the `prepare` script).

## Quick Start

```typescript
import { DefaultApi, Configuration, subscribeToTasks } from 'todo-client';

// Initialize the API client
const api = new DefaultApi(new Configuration({ 
  basePath: 'http://localhost:8000/api' 
}));

// Create a task
const newTask = await api.addTaskApiTasksPost({
  taskCreate: {
    text: 'Complete project documentation',
    completed: false
  }
});

// List all tasks
const tasks = await api.listTasksApiTasksGet();
console.log(tasks.tasks);

// Subscribe to real-time updates
const unsubscribe = subscribeToTasks((data) => {
  console.log('Tasks updated:', data.tasks);
});
```

## HTTP API Endpoints

### List Tasks

```
GET /api/tasks
```

**Response:** `200 OK`

```json
{
  "tasks": {
    "task-uuid-1": {
      "id": "task-uuid-1",
      "text": "Task description",
      "completed": false,
      "inferred": false,
      "due": 1738569600,
      "created_at": 1738396800,
      "updated_at": 1738396800,
      "calculated_completed": false,
      "calculated_due": 1738569600,
      "deps_clear": true,
      "parents": [],
      "children": ["task-uuid-2"]
    }
  },
  "dependencies": {
    "dep-uuid": {
      "id": "dep-uuid",
      "from_id": "task-uuid-1",
      "to_id": "task-uuid-2"
    }
  },
  "has_cycles": false
}
```

**Schema:**
- `tasks`: Object mapping task IDs to `TaskOut` objects
- `dependencies`: Object mapping dependency IDs to `DependencyOut` objects
- `has_cycles`: Boolean indicating if circular dependencies exist

### Subscribe to Task Updates (SSE)

```
GET /api/tasks/subscribe
```

**Response:** `200 OK` (Server-Sent Events stream)

**Event Types:**

**`init`** - Initial task list sent when connection is established:
```
event: init
data: {"tasks": {...}, "dependencies": {...}, "has_cycles": false}
```

**`update`** - Task list sent whenever tasks are modified:
```
event: update
data: {"tasks": {...}, "dependencies": {...}, "has_cycles": false}
```

Both events contain the complete `TaskListOut` schema with all current tasks and dependencies.

## API Reference

### Configuration

Create a configured API client instance:

```typescript
import { DefaultApi, Configuration } from 'todo-client';

const config = new Configuration({
  basePath: 'http://localhost:8000/api',
  // Optional: add custom headers, middleware, etc.
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN'
  }
});

const api = new DefaultApi(config);
```

### Task Management

#### Create a Task

```typescript
const task = await api.addTaskApiTasksPost({
  taskCreate: {
    text: 'Task description',
    completed: false,
    inferred: false,
    due: '2026-02-15T10:00:00Z',  // Optional ISO date string
    note: 'Additional notes'       // Optional
  }
});
```

#### List All Tasks

```typescript
const taskList = await api.listTasksApiTasksGet();

// Access tasks and metadata
console.log(taskList.tasks);        // Array of TaskOut objects
console.log(taskList.dependencies); // Array of DependencyOut objects
```

#### Update a Task

```typescript
await api.setTaskApiTasksTaskIdPatch({
  taskId: 'task-uuid',
  taskUpdate: {
    text: 'Updated task text',
    completed: true,
    due: '2026-03-01T12:00:00Z'
  }
});
```

#### Rename a Task

```typescript
await api.renameTaskApiTasksTaskIdRenamePost({
  taskId: 'task-uuid',
  renameRequest: {
    newText: 'New task name'
  }
});
```

#### Delete a Task

```typescript
const result = await api.removeTaskApiTasksTaskIdDelete({
  taskId: 'task-uuid'
});

console.log(result.success); // true/false
console.log(result.message); // Status message
```

### Dependency Management

#### Link Tasks (Create Dependency)

```typescript
await api.linkTasksApiLinksPost({
  linkRequest: {
    fromId: 'parent-task-uuid',
    toId: 'child-task-uuid'
  }
});
```

#### Unlink Tasks (Remove Dependency)

```typescript
await api.unlinkTasksApiLinksDelete({
  linkRequest: {
    fromId: 'parent-task-uuid',
    toId: 'child-task-uuid'
  }
});
```

### Real-Time Updates

Subscribe to task updates via Server-Sent Events:

```typescript
import { subscribeToTasks } from 'todo-client';

const unsubscribe = subscribeToTasks(
  // Callback function for updates
  (data) => {
    console.log('Current tasks:', data.tasks);
    console.log('Dependencies:', data.dependencies);
  },
  // Optional configuration
  {
    baseUrl: 'http://localhost:8000',
    onError: (err) => {
      console.error('SSE connection error:', err);
    }
  }
);

// Later, when you want to stop listening:
unsubscribe();
```

The subscription will receive:
- **init**: Initial task list when connection is established
- **update**: Task list updates whenever tasks change

## Type Definitions

### TaskOut

```typescript
interface TaskOut {
  id: string;                  // Unique task identifier
  text: string;                // Task description
  completed: boolean;          // Completion status
  inferred: boolean;           // Whether task was inferred from text
  depth: number;               // Depth in DAG hierarchy
  due?: string | null;         // Due date (ISO string)
  note?: string | null;        // Additional notes
  createdAt: string;           // Creation timestamp
  updatedAt: string;           // Last update timestamp
}
```

### TaskCreate

```typescript
interface TaskCreate {
  text?: string | null;        // Task description
  completed?: boolean;         // Completion status (default: false)
  inferred?: boolean;          // Inferred flag (default: false)
  due?: string | null;         // Due date (ISO string)
  note?: string | null;        // Additional notes
}
```

### TaskUpdate

```typescript
interface TaskUpdate {
  text?: string | null;        // Updated description
  completed?: boolean;         // Updated completion status
  due?: string | null;         // Updated due date
  note?: string | null;        // Updated notes
}
```

### DependencyOut

```typescript
interface DependencyOut {
  fromId: string;              // Parent task ID
  toId: string;                // Child task ID
  createdAt: string;           // Creation timestamp
}
```

## Error Handling

The API throws errors for failed requests. Wrap calls in try-catch blocks:

```typescript
try {
  const task = await api.addTaskApiTasksPost({
    taskCreate: { text: 'New task' }
  });
} catch (error) {
  if (error instanceof Response) {
    const errorData = await error.json();
    console.error('API Error:', errorData);
  } else {
    console.error('Network Error:', error);
  }
}
```

## Development

### Generate Client Code

The client is generated from the OpenAPI specification:

```bash
npm run generate
```

This runs the generation script that creates the API client from [openapi.json](openapi.json).

### Build

Compile TypeScript to JavaScript:

```bash
npm run build
```

Output is placed in the `dist/` directory.

## Advanced Usage

### Custom Request Options

Pass custom fetch options to any API call:

```typescript
const tasks = await api.listTasksApiTasksGet({
  headers: {
    'X-Custom-Header': 'value'
  },
  signal: abortController.signal  // For cancellation
});
```

### Batch Operations

Perform multiple operations efficiently:

```typescript
// Create multiple tasks
const taskPromises = ['Task 1', 'Task 2', 'Task 3'].map(text =>
  api.addTaskApiTasksPost({
    taskCreate: { text }
  })
);

const createdTasks = await Promise.all(taskPromises);

// Link them in a chain
for (let i = 0; i < createdTasks.length - 1; i++) {
  await api.linkTasksApiLinksPost({
    linkRequest: {
      fromId: createdTasks[i].id,
      toId: createdTasks[i + 1].id
    }
  });
}
```

## License

MIT
