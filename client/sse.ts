/**
 * SSE subscription wrapper for task updates.
 * Use this alongside the generated OpenAPI client.
 *
 * OpenAPI doesn't spec SSE, so this is manual.
 */

import type { TaskListOut } from './generated';

export type TaskSubscriber = (data: TaskListOut) => void;

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
      onUpdate(JSON.parse(e.data));
    } catch (err) {
      console.error('Failed to parse SSE data:', err);
    }
  };

  es.addEventListener('init', handler);
  es.addEventListener('update', handler);
  es.onerror = options?.onError ?? (() => console.error('SSE connection error'));

  return () => es.close();
}
