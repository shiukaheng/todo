/**
 * Discriminated union of display batch operations.
 * The `op` field determines the operation type.
 * @export
 */
export type DisplayBatchOperation = UpdateViewOp | DeleteViewOp;
export interface UpdateViewOp {
    op: 'update_view';
    viewId: string;
    positions?: {
        [key: string]: Array<number>;
    };
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
export declare function DisplayBatchOperationToJSON(value: DisplayBatchOperation): any;
