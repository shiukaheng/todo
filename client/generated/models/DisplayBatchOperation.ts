/* tslint:disable */
/* eslint-disable */
import { mapValues } from '../runtime';

/**
 * Discriminated union of display batch operations.
 * The `op` field determines the operation type.
 * @export
 */
export type DisplayBatchOperation =
    | UpdateViewOp
    | DeleteViewOp;

export interface UpdateViewOp {
    op: 'update_view';
    viewId: string;
    positions?: { [key: string]: Array<number> };
    whitelist?: Array<string>;
    blacklist?: Array<string>;
}

export interface DeleteViewOp {
    op: 'delete_view';
    id: string;
}

/**
 * Convert a DisplayBatchOperation to JSON for the API.
 * Handles camelCase -> snake_case conversion.
 */
export function DisplayBatchOperationToJSON(value: DisplayBatchOperation): any {
    if (value == null) {
        return value;
    }

    const base: any = { op: value.op };

    switch (value.op) {
        case 'update_view': {
            const v = value as UpdateViewOp;
            const result: any = { ...base, view_id: v.viewId };
            if (v.positions !== undefined) result.positions = v.positions;
            if (v.whitelist !== undefined) result.whitelist = v.whitelist;
            if (v.blacklist !== undefined) result.blacklist = v.blacklist;
            return result;
        }
        case 'delete_view':
            return { ...base, id: (value as DeleteViewOp).id };
        default:
            return { ...base, ...(value as any) };
    }
}
