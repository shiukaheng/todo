/* tslint:disable */
/* eslint-disable */
import { mapValues } from '../runtime';

/**
 * Discriminated union of display batch operations.
 * The `op` field determines the operation type.
 * @export
 */
export type DisplayBatchOperation =
    | CreateViewOp
    | DeleteViewOp
    | UpdatePositionsOp
    | RemovePositionsOp
    | SetWhitelistOp
    | SetBlacklistOp;

export interface CreateViewOp {
    op: 'create_view';
    id: string;
}

export interface DeleteViewOp {
    op: 'delete_view';
    id: string;
}

export interface UpdatePositionsOp {
    op: 'update_positions';
    viewId: string;
    positions: { [key: string]: Array<number> };
}

export interface RemovePositionsOp {
    op: 'remove_positions';
    viewId: string;
    nodeIds: Array<string>;
}

export interface SetWhitelistOp {
    op: 'set_whitelist';
    viewId: string;
    nodeIds: Array<string>;
}

export interface SetBlacklistOp {
    op: 'set_blacklist';
    viewId: string;
    nodeIds: Array<string>;
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
        case 'create_view':
            return { ...base, id: (value as CreateViewOp).id };
        case 'delete_view':
            return { ...base, id: (value as DeleteViewOp).id };
        case 'update_positions': {
            const v = value as UpdatePositionsOp;
            return { ...base, view_id: v.viewId, positions: v.positions };
        }
        case 'remove_positions': {
            const v = value as RemovePositionsOp;
            return { ...base, view_id: v.viewId, node_ids: v.nodeIds };
        }
        case 'set_whitelist': {
            const v = value as SetWhitelistOp;
            return { ...base, view_id: v.viewId, node_ids: v.nodeIds };
        }
        case 'set_blacklist': {
            const v = value as SetBlacklistOp;
            return { ...base, view_id: v.viewId, node_ids: v.nodeIds };
        }
        default:
            return { ...base, ...(value as any) };
    }
}
