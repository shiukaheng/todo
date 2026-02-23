"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.DisplayBatchOperationToJSON = DisplayBatchOperationToJSON;
/**
 * Convert a DisplayBatchOperation to JSON for the API.
 * Handles camelCase -> snake_case conversion.
 */
function DisplayBatchOperationToJSON(value) {
    if (value == null) {
        return value;
    }
    const base = { op: value.op };
    switch (value.op) {
        case 'update_view': {
            const v = value;
            const result = { ...base, view_id: v.viewId };
            if (v.positions !== undefined)
                result.positions = v.positions;
            if (v.whitelist !== undefined)
                result.whitelist = v.whitelist;
            if (v.blacklist !== undefined)
                result.blacklist = v.blacklist;
            return result;
        }
        case 'delete_view':
            return { ...base, id: value.id };
        default:
            return { ...base, ...value };
    }
}
