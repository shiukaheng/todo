/**
 * SSE subscription wrappers for real-time updates.
 * Use these alongside the generated OpenAPI client.
 *
 * OpenAPI doesn't spec SSE, so these are manual.
 */

import { NodeListOut, NodeListOutFromJSON, AppState, AppStateFromJSON } from './generated';

export type TaskSubscriber = (data: NodeListOut) => void;
export type StateSubscriber = (data: AppState) => void;

/**
 * Subscribe to application state updates (tasks + dependencies + plans).
 * This is the recommended subscription for full app state.
 */
export function subscribeToState(
  onUpdate: StateSubscriber,
  options?: {
    baseUrl?: string;
    onError?: (err: Event) => void;
  }
): () => void {
  const baseUrl = options?.baseUrl ?? '';
  const es = new EventSource(`${baseUrl}/api/state/subscribe`);

  const handler = (e: MessageEvent) => {
    try {
      const raw = JSON.parse(e.data);
      onUpdate(AppStateFromJSON(raw));
    } catch (err) {
      console.error('Failed to parse SSE data:', err);
    }
  };

  es.addEventListener('init', handler);
  es.addEventListener('update', handler);
  es.onerror = options?.onError ?? (() => console.error('SSE connection error'));

  return () => es.close();
}

/**
 * Subscribe to task updates only (deprecated - use subscribeToState instead).
 * @deprecated Use subscribeToState for full application state including plans.
 */
export function subscribeToTasks(
  onUpdate: TaskSubscriber,
  options?: {
    baseUrl?: string;
    onError?: (err: Event) => void;
  }
): () => void {
  const baseUrl = options?.baseUrl ?? '';
  const es = new EventSource(`${baseUrl}/api/tasks/subscribe`);

  const handler = (e: MessageEvent) => {
    try {
      const raw = JSON.parse(e.data);
      onUpdate(NodeListOutFromJSON(raw));
    } catch (err) {
      console.error('Failed to parse SSE data:', err);
    }
  };

  es.addEventListener('init', handler);
  es.addEventListener('update', handler);
  es.onerror = options?.onError ?? (() => console.error('SSE connection error'));

  return () => es.close();
}
