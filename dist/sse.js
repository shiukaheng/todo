"use strict";
/**
 * SSE subscription wrappers for real-time updates.
 * Use these alongside the generated OpenAPI client.
 *
 * OpenAPI doesn't spec SSE, so these are manual.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.subscribeToState = subscribeToState;
exports.subscribeToDisplay = subscribeToDisplay;
exports.subscribeToTasks = subscribeToTasks;
const generated_1 = require("./generated");
/**
 * Subscribe to application state updates (tasks + dependencies + plans).
 * This is the recommended subscription for full app state.
 */
function subscribeToState(onUpdate, options) {
    const baseUrl = options?.baseUrl ?? '';
    const es = new EventSource(`${baseUrl}/api/state/subscribe`);
    const handler = (e) => {
        try {
            const raw = JSON.parse(e.data);
            onUpdate((0, generated_1.AppStateFromJSON)(raw));
        }
        catch (err) {
            console.error('Failed to parse SSE data:', err);
        }
    };
    es.addEventListener('init', handler);
    es.addEventListener('update', handler);
    es.onerror = options?.onError ?? (() => console.error('SSE connection error'));
    return () => es.close();
}
/**
 * Subscribe to display layer updates (views with positions/filters).
 */
function subscribeToDisplay(onUpdate, options) {
    const baseUrl = options?.baseUrl ?? '';
    const es = new EventSource(`${baseUrl}/api/display/subscribe`);
    const handler = (e) => {
        try {
            const raw = JSON.parse(e.data);
            onUpdate((0, generated_1.ViewListOutFromJSON)(raw));
        }
        catch (err) {
            console.error('Failed to parse display SSE data:', err);
        }
    };
    es.addEventListener('init', handler);
    es.addEventListener('update', handler);
    es.onerror = options?.onError ?? (() => console.error('Display SSE connection error'));
    return () => es.close();
}
/**
 * Subscribe to task updates only (deprecated - use subscribeToState instead).
 * @deprecated Use subscribeToState for full application state including plans.
 */
function subscribeToTasks(onUpdate, options) {
    const baseUrl = options?.baseUrl ?? '';
    const es = new EventSource(`${baseUrl}/api/tasks/subscribe`);
    const handler = (e) => {
        try {
            const raw = JSON.parse(e.data);
            onUpdate((0, generated_1.NodeListOutFromJSON)(raw));
        }
        catch (err) {
            console.error('Failed to parse SSE data:', err);
        }
    };
    es.addEventListener('init', handler);
    es.addEventListener('update', handler);
    es.onerror = options?.onError ?? (() => console.error('SSE connection error'));
    return () => es.close();
}
