/**
 * Re-export everything for convenience.
 *
 * Usage:
 *   import { DefaultApi, Configuration, subscribeToTasks } from './client';
 *
 *   const api = new DefaultApi(new Configuration({ basePath: '/api' }));
 *   const tasks = await api.listTasksApiTasksGet();
 *
 *   const unsub = subscribeToTasks((data) => console.log(data.tasks));
 */

export * from './generated';
export { subscribeToTasks } from './sse';
