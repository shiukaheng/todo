"use strict";
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
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __exportStar = (this && this.__exportStar) || function(m, exports) {
    for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports, p)) __createBinding(exports, m, p);
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.subscribeToTasks = exports.subscribeToDisplay = exports.subscribeToState = void 0;
__exportStar(require("./generated"), exports);
var sse_1 = require("./sse");
Object.defineProperty(exports, "subscribeToState", { enumerable: true, get: function () { return sse_1.subscribeToState; } });
Object.defineProperty(exports, "subscribeToDisplay", { enumerable: true, get: function () { return sse_1.subscribeToDisplay; } });
Object.defineProperty(exports, "subscribeToTasks", { enumerable: true, get: function () { return sse_1.subscribeToTasks; } });
