/* tslint:disable */
/* eslint-disable */
import { mapValues } from '../runtime';
import type { NodeType } from './NodeType';
import {
    NodeTypeToJSON,
} from './NodeType';
import type { StepData } from './StepData';
import {
    StepDataToJSON,
} from './StepData';

/**
 * Discriminated union of batch operations.
 * The `op` field determines the operation type.
 * @export
 */
export type BatchOperation =
    | CreateNodeOp
    | UpdateNodeOp
    | DeleteNodeOp
    | RenameNodeOp
    | LinkOp
    | UnlinkOp
    | CreatePlanOp
    | UpdatePlanOp
    | DeletePlanOp
    | RenamePlanOp;

export interface CreateNodeOp {
    op: 'create_node';
    id: string;
    text?: string | null;
    completed?: boolean;
    nodeType?: NodeType;
    due?: number | null;
    depends?: Array<string> | null;
    blocks?: Array<string> | null;
}

export interface UpdateNodeOp {
    op: 'update_node';
    id: string;
    text?: string | null;
    completed?: boolean | null;
    nodeType?: NodeType | null;
    due?: number | null;
}

export interface DeleteNodeOp {
    op: 'delete_node';
    id: string;
}

export interface RenameNodeOp {
    op: 'rename_node';
    id: string;
    newId: string;
}

export interface LinkOp {
    op: 'link';
    fromId: string;
    toId: string;
}

export interface UnlinkOp {
    op: 'unlink';
    fromId: string;
    toId: string;
}

export interface CreatePlanOp {
    op: 'create_plan';
    id: string;
    text?: string | null;
    steps?: Array<StepData>;
}

export interface UpdatePlanOp {
    op: 'update_plan';
    id: string;
    text?: string | null;
    steps?: Array<StepData> | null;
}

export interface DeletePlanOp {
    op: 'delete_plan';
    id: string;
}

export interface RenamePlanOp {
    op: 'rename_plan';
    id: string;
    newId: string;
}

/**
 * Convert a BatchOperation to JSON for the API.
 * Handles camelCase -> snake_case conversion.
 */
export function BatchOperationToJSON(value: BatchOperation): any {
    if (value == null) {
        return value;
    }

    const base: any = { op: value.op };

    switch (value.op) {
        case 'create_node': {
            const v = value as CreateNodeOp;
            return {
                ...base,
                id: v.id,
                text: v.text,
                completed: v.completed,
                node_type: v.nodeType != null ? NodeTypeToJSON(v.nodeType) : undefined,
                due: v.due,
                depends: v.depends,
                blocks: v.blocks,
            };
        }
        case 'update_node': {
            const v = value as UpdateNodeOp;
            return {
                ...base,
                id: v.id,
                text: v.text,
                completed: v.completed,
                node_type: v.nodeType !== undefined ? (v.nodeType != null ? NodeTypeToJSON(v.nodeType) : null) : undefined,
                due: v.due,
            };
        }
        case 'delete_node':
            return { ...base, id: (value as DeleteNodeOp).id };
        case 'rename_node':
            return { ...base, id: (value as RenameNodeOp).id, new_id: (value as RenameNodeOp).newId };
        case 'link':
            return { ...base, from_id: (value as LinkOp).fromId, to_id: (value as LinkOp).toId };
        case 'unlink':
            return { ...base, from_id: (value as UnlinkOp).fromId, to_id: (value as UnlinkOp).toId };
        case 'create_plan': {
            const v = value as CreatePlanOp;
            return {
                ...base,
                id: v.id,
                text: v.text,
                steps: v.steps != null ? (v.steps as Array<any>).map(StepDataToJSON) : undefined,
            };
        }
        case 'update_plan': {
            const v = value as UpdatePlanOp;
            return {
                ...base,
                id: v.id,
                text: v.text,
                steps: v.steps != null ? (v.steps as Array<any>).map(StepDataToJSON) : v.steps,
            };
        }
        case 'delete_plan':
            return { ...base, id: (value as DeletePlanOp).id };
        case 'rename_plan':
            return { ...base, id: (value as RenamePlanOp).id, new_id: (value as RenamePlanOp).newId };
        default:
            return { ...base, ...(value as any) };
    }
}
