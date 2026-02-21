/* tslint:disable */
/* eslint-disable */
import { mapValues } from '../runtime';
import type { BatchOperation } from './BatchOperation';
import {
    BatchOperationToJSON,
} from './BatchOperation';

/**
 * Batch of operations to execute atomically.
 * @export
 * @interface BatchRequest
 */
export interface BatchRequest {
    /**
     *
     * @type {Array<BatchOperation>}
     * @memberof BatchRequest
     */
    operations: Array<BatchOperation>;
}

export function instanceOfBatchRequest(value: object): value is BatchRequest {
    if (!('operations' in value) || value['operations'] === undefined) return false;
    return true;
}

export function BatchRequestFromJSON(json: any): BatchRequest {
    return BatchRequestFromJSONTyped(json, false);
}

export function BatchRequestFromJSONTyped(json: any, ignoreDiscriminator: boolean): BatchRequest {
    if (json == null) {
        return json;
    }
    return {
        'operations': json['operations'],
    };
}

export function BatchRequestToJSON(json: any): BatchRequest {
    return BatchRequestToJSONTyped(json, false);
}

export function BatchRequestToJSONTyped(value?: BatchRequest | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        'operations': (value['operations'] as Array<any>).map(BatchOperationToJSON),
    };
}
