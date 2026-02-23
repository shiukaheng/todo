"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.BatchOperationToJSON = BatchOperationToJSON;
const NodeType_1 = require("./NodeType");
const StepData_1 = require("./StepData");
/**
 * Convert a BatchOperation to JSON for the API.
 * Handles camelCase -> snake_case conversion.
 */
function BatchOperationToJSON(value) {
    if (value == null) {
        return value;
    }
    const base = { op: value.op };
    switch (value.op) {
        case 'create_node': {
            const v = value;
            return {
                ...base,
                id: v.id,
                text: v.text,
                completed: v.completed,
                node_type: v.nodeType != null ? (0, NodeType_1.NodeTypeToJSON)(v.nodeType) : undefined,
                due: v.due,
                depends: v.depends,
                blocks: v.blocks,
            };
        }
        case 'update_node': {
            const v = value;
            return {
                ...base,
                id: v.id,
                text: v.text,
                completed: v.completed,
                node_type: v.nodeType !== undefined ? (v.nodeType != null ? (0, NodeType_1.NodeTypeToJSON)(v.nodeType) : null) : undefined,
                due: v.due,
            };
        }
        case 'delete_node':
            return { ...base, id: value.id };
        case 'rename_node':
            return { ...base, id: value.id, new_id: value.newId };
        case 'link':
            return { ...base, from_id: value.fromId, to_id: value.toId };
        case 'unlink':
            return { ...base, from_id: value.fromId, to_id: value.toId };
        case 'create_plan': {
            const v = value;
            return {
                ...base,
                id: v.id,
                text: v.text,
                steps: v.steps != null ? v.steps.map(StepData_1.StepDataToJSON) : undefined,
            };
        }
        case 'update_plan': {
            const v = value;
            return {
                ...base,
                id: v.id,
                text: v.text,
                steps: v.steps != null ? v.steps.map(StepData_1.StepDataToJSON) : v.steps,
            };
        }
        case 'delete_plan':
            return { ...base, id: value.id };
        case 'rename_plan':
            return { ...base, id: value.id, new_id: value.newId };
        default:
            return { ...base, ...value };
    }
}
