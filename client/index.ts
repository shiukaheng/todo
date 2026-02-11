/**
 * Re-export everything for convenience.
 *
 * Usage:
 *   import { DefaultApi, Configuration, subscribeToState } from 'todo-client';
 *
 *   const api = new DefaultApi(new Configuration({ basePath: '/api' }));
 *   const state = await api.getStateApiStateGet();
 *
 *   const unsub = subscribeToState((data) => console.log(data.tasks, data.plans));
 */

export * from './generated';
export { subscribeToState, subscribeToTasks } from './sse';
