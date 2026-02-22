/* tslint:disable */
/* eslint-disable */
import { mapValues } from '../runtime';
import type { DisplayBatchOperation } from './DisplayBatchOperation';
import { DisplayBatchOperationToJSON } from './DisplayBatchOperation';

/**
 * Batch of display operations to execute atomically.
 * @export
 * @interface DisplayBatchRequest
 */
export interface DisplayBatchRequest {
    /**
     * @type {Array<DisplayBatchOperation>}
     * @memberof DisplayBatchRequest
     */
    operations: Array<DisplayBatchOperation>;
}

export function instanceOfDisplayBatchRequest(value: object): value is DisplayBatchRequest {
    if (!('operations' in value) || value['operations'] === undefined) return false;
    return true;
}

export function DisplayBatchRequestFromJSON(json: any): DisplayBatchRequest {
    if (json == null) {
        return json;
    }
    return {
        'operations': json['operations'],
    };
}

export function DisplayBatchRequestToJSON(value?: DisplayBatchRequest | null): any {
    if (value == null) {
        return value;
    }

    return {
        'operations': (value['operations'] as Array<any>).map(DisplayBatchOperationToJSON),
    };
}
