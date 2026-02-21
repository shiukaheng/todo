/* tslint:disable */
/* eslint-disable */
import { mapValues } from '../runtime';
import type { BatchOperationResult } from './BatchOperationResult';
import {
    BatchOperationResultFromJSON,
    BatchOperationResultToJSON,
} from './BatchOperationResult';

/**
 * Response for a batch operation.
 * @export
 * @interface BatchResponse
 */
export interface BatchResponse {
    /**
     *
     * @type {boolean}
     * @memberof BatchResponse
     */
    success: boolean;
    /**
     *
     * @type {Array<BatchOperationResult>}
     * @memberof BatchResponse
     */
    results: Array<BatchOperationResult>;
    /**
     *
     * @type {string}
     * @memberof BatchResponse
     */
    message?: string | null;
}

export function instanceOfBatchResponse(value: object): value is BatchResponse {
    if (!('success' in value) || value['success'] === undefined) return false;
    if (!('results' in value) || value['results'] === undefined) return false;
    return true;
}

export function BatchResponseFromJSON(json: any): BatchResponse {
    return BatchResponseFromJSONTyped(json, false);
}

export function BatchResponseFromJSONTyped(json: any, ignoreDiscriminator: boolean): BatchResponse {
    if (json == null) {
        return json;
    }
    return {
        'success': json['success'],
        'results': ((json['results'] as Array<any>).map(BatchOperationResultFromJSON)),
        'message': json['message'] == null ? undefined : json['message'],
    };
}

export function BatchResponseToJSON(json: any): BatchResponse {
    return BatchResponseToJSONTyped(json, false);
}

export function BatchResponseToJSONTyped(value?: BatchResponse | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        'success': value['success'],
        'results': ((value['results'] as Array<any>).map(BatchOperationResultToJSON)),
        'message': value['message'],
    };
}
