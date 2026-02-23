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
export { subscribeToState, subscribeToDisplay, subscribeToTasks } from './sse';

// Backward-compatible aliases for generated discriminated-union types.
// The OpenAPI generator names these OperationsInner / OperationsInner1.
export type { OperationsInner as BatchOperation } from './generated';
export type { OperationsInner1 as DisplayBatchOperation } from './generated';
