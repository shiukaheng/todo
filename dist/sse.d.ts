/**
 * SSE subscription wrappers for real-time updates.
 * Use these alongside the generated OpenAPI client.
 *
 * OpenAPI doesn't spec SSE, so these are manual.
 */
import { NodeListOut, AppState, ViewListOut } from './generated';
export type TaskSubscriber = (data: NodeListOut) => void;
export type StateSubscriber = (data: AppState) => void;
export type DisplaySubscriber = (data: ViewListOut) => void;
/**
 * Subscribe to application state updates (tasks + dependencies + plans).
 * This is the recommended subscription for full app state.
 */
export declare function subscribeToState(onUpdate: StateSubscriber, options?: {
    baseUrl?: string;
    onError?: (err: Event) => void;
}): () => void;
/**
 * Subscribe to display layer updates (views with positions/filters).
 */
export declare function subscribeToDisplay(onUpdate: DisplaySubscriber, options?: {
    baseUrl?: string;
    onError?: (err: Event) => void;
}): () => void;
/**
 * Subscribe to task updates only (deprecated - use subscribeToState instead).
 * @deprecated Use subscribeToState for full application state including plans.
 */
export declare function subscribeToTasks(onUpdate: TaskSubscriber, options?: {
    baseUrl?: string;
    onError?: (err: Event) => void;
}): () => void;
