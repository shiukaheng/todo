import type { NodeType } from './NodeType';
import type { StepData } from './StepData';
/**
 * Discriminated union of batch operations.
 * The `op` field determines the operation type.
 * @export
 */
export type BatchOperation = CreateNodeOp | UpdateNodeOp | DeleteNodeOp | RenameNodeOp | LinkOp | UnlinkOp | CreatePlanOp | UpdatePlanOp | DeletePlanOp | RenamePlanOp;
export interface CreateNodeOp {
    op: 'create_node';
    id: string;
    text?: string | null;
    completed?: number | null;
    nodeType?: NodeType;
    due?: number | null;
    depends?: Array<string> | null;
    blocks?: Array<string> | null;
}
export interface UpdateNodeOp {
    op: 'update_node';
    id: string;
    text?: string | null;
    completed?: number | null;
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
export declare function BatchOperationToJSON(value: BatchOperation): any;
