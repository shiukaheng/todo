# DefaultApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**batchOperationsApiBatchPost**](DefaultApi.md#batchoperationsapibatchpost) | **POST** /api/batch | Batch Operations |
| [**displayBatchOperationsApiDisplayBatchPost**](DefaultApi.md#displaybatchoperationsapidisplaybatchpost) | **POST** /api/display/batch | Display Batch Operations |
| [**getPlanApiPlansPlanIdGet**](DefaultApi.md#getplanapiplansplanidget) | **GET** /api/plans/{plan_id} | Get Plan |
| [**getStateApiStateGet**](DefaultApi.md#getstateapistateget) | **GET** /api/state | Get State |
| [**getTaskApiTasksTaskIdGet**](DefaultApi.md#gettaskapitaskstaskidget) | **GET** /api/tasks/{task_id} | Get Task |
| [**getViewApiViewsViewIdGet**](DefaultApi.md#getviewapiviewsviewidget) | **GET** /api/views/{view_id} | Get View |
| [**getViewPositionsApiViewsViewIdPositionsGet**](DefaultApi.md#getviewpositionsapiviewsviewidpositionsget) | **GET** /api/views/{view_id}/positions | Get View Positions |
| [**healthHealthGet**](DefaultApi.md#healthhealthget) | **GET** /health | Health |
| [**initDbApiInitPost**](DefaultApi.md#initdbapiinitpost) | **POST** /api/init | Init Db |
| [**listPlansApiPlansGet**](DefaultApi.md#listplansapiplansget) | **GET** /api/plans | List Plans |
| [**listTasksApiTasksGet**](DefaultApi.md#listtasksapitasksget) | **GET** /api/tasks | List Tasks |
| [**listViewsApiViewsGet**](DefaultApi.md#listviewsapiviewsget) | **GET** /api/views | List Views |
| [**putViewPositionsApiViewsViewIdPositionsPut**](DefaultApi.md#putviewpositionsapiviewsviewidpositionsput) | **PUT** /api/views/{view_id}/positions | Put View Positions |
| [**subscribeDisplayApiDisplaySubscribeGet**](DefaultApi.md#subscribedisplayapidisplaysubscribeget) | **GET** /api/display/subscribe | Subscribe Display |
| [**subscribeStateApiStateSubscribeGet**](DefaultApi.md#subscribestateapistatesubscribeget) | **GET** /api/state/subscribe | Subscribe State |
| [**subscribeTasksApiTasksSubscribeGet**](DefaultApi.md#subscribetasksapitaskssubscribeget) | **GET** /api/tasks/subscribe | Subscribe Tasks |



## batchOperationsApiBatchPost

> BatchResponse batchOperationsApiBatchPost(batchRequest)

Batch Operations

Execute multiple operations atomically in a single transaction.

### Example

```ts
import {
  Configuration,
  DefaultApi,
} from '';
import type { BatchOperationsApiBatchPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DefaultApi();

  const body = {
    // BatchRequest
    batchRequest: ...,
  } satisfies BatchOperationsApiBatchPostRequest;

  try {
    const data = await api.batchOperationsApiBatchPost(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **batchRequest** | [BatchRequest](BatchRequest.md) |  | |

### Return type

[**BatchResponse**](BatchResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## displayBatchOperationsApiDisplayBatchPost

> BatchResponse displayBatchOperationsApiDisplayBatchPost(displayBatchRequest)

Display Batch Operations

Execute multiple display operations atomically in a single transaction.

### Example

```ts
import {
  Configuration,
  DefaultApi,
} from '';
import type { DisplayBatchOperationsApiDisplayBatchPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DefaultApi();

  const body = {
    // DisplayBatchRequest
    displayBatchRequest: ...,
  } satisfies DisplayBatchOperationsApiDisplayBatchPostRequest;

  try {
    const data = await api.displayBatchOperationsApiDisplayBatchPost(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **displayBatchRequest** | [DisplayBatchRequest](DisplayBatchRequest.md) |  | |

### Return type

[**BatchResponse**](BatchResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getPlanApiPlansPlanIdGet

> PlanOut getPlanApiPlansPlanIdGet(planId)

Get Plan

Get a single plan with its steps.

### Example

```ts
import {
  Configuration,
  DefaultApi,
} from '';
import type { GetPlanApiPlansPlanIdGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DefaultApi();

  const body = {
    // string
    planId: planId_example,
  } satisfies GetPlanApiPlansPlanIdGetRequest;

  try {
    const data = await api.getPlanApiPlansPlanIdGet(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **planId** | `string` |  | [Defaults to `undefined`] |

### Return type

[**PlanOut**](PlanOut.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getStateApiStateGet

> AppState getStateApiStateGet()

Get State

Get current complete application state (one-shot).

### Example

```ts
import {
  Configuration,
  DefaultApi,
} from '';
import type { GetStateApiStateGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DefaultApi();

  try {
    const data = await api.getStateApiStateGet();
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**AppState**](AppState.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getTaskApiTasksTaskIdGet

> NodeOut getTaskApiTasksTaskIdGet(taskId)

Get Task

Get a single task with computed properties.

### Example

```ts
import {
  Configuration,
  DefaultApi,
} from '';
import type { GetTaskApiTasksTaskIdGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DefaultApi();

  const body = {
    // string
    taskId: taskId_example,
  } satisfies GetTaskApiTasksTaskIdGetRequest;

  try {
    const data = await api.getTaskApiTasksTaskIdGet(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **taskId** | `string` |  | [Defaults to `undefined`] |

### Return type

[**NodeOut**](NodeOut.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getViewApiViewsViewIdGet

> ViewOut getViewApiViewsViewIdGet(viewId)

Get View

Get a single view.

### Example

```ts
import {
  Configuration,
  DefaultApi,
} from '';
import type { GetViewApiViewsViewIdGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DefaultApi();

  const body = {
    // string
    viewId: viewId_example,
  } satisfies GetViewApiViewsViewIdGetRequest;

  try {
    const data = await api.getViewApiViewsViewIdGet(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **viewId** | `string` |  | [Defaults to `undefined`] |

### Return type

[**ViewOut**](ViewOut.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getViewPositionsApiViewsViewIdPositionsGet

> ViewPositionsOut getViewPositionsApiViewsViewIdPositionsGet(viewId)

Get View Positions

Get positions for a view.

### Example

```ts
import {
  Configuration,
  DefaultApi,
} from '';
import type { GetViewPositionsApiViewsViewIdPositionsGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DefaultApi();

  const body = {
    // string
    viewId: viewId_example,
  } satisfies GetViewPositionsApiViewsViewIdPositionsGetRequest;

  try {
    const data = await api.getViewPositionsApiViewsViewIdPositionsGet(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **viewId** | `string` |  | [Defaults to `undefined`] |

### Return type

[**ViewPositionsOut**](ViewPositionsOut.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## healthHealthGet

> any healthHealthGet()

Health

Health check endpoint.

### Example

```ts
import {
  Configuration,
  DefaultApi,
} from '';
import type { HealthHealthGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DefaultApi();

  try {
    const data = await api.healthHealthGet();
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

This endpoint does not need any parameter.

### Return type

**any**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## initDbApiInitPost

> OperationResult initDbApiInitPost()

Init Db

Initialize the database schema and run migrations.

### Example

```ts
import {
  Configuration,
  DefaultApi,
} from '';
import type { InitDbApiInitPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DefaultApi();

  try {
    const data = await api.initDbApiInitPost();
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**OperationResult**](OperationResult.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## listPlansApiPlansGet

> PlanListOut listPlansApiPlansGet()

List Plans

List all plans with their steps.

### Example

```ts
import {
  Configuration,
  DefaultApi,
} from '';
import type { ListPlansApiPlansGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DefaultApi();

  try {
    const data = await api.listPlansApiPlansGet();
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**PlanListOut**](PlanListOut.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## listTasksApiTasksGet

> NodeListOut listTasksApiTasksGet()

List Tasks

List all tasks with computed properties.

### Example

```ts
import {
  Configuration,
  DefaultApi,
} from '';
import type { ListTasksApiTasksGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DefaultApi();

  try {
    const data = await api.listTasksApiTasksGet();
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**NodeListOut**](NodeListOut.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## listViewsApiViewsGet

> ViewListOut listViewsApiViewsGet()

List Views

List all views.

### Example

```ts
import {
  Configuration,
  DefaultApi,
} from '';
import type { ListViewsApiViewsGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DefaultApi();

  try {
    const data = await api.listViewsApiViewsGet();
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**ViewListOut**](ViewListOut.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## putViewPositionsApiViewsViewIdPositionsPut

> putViewPositionsApiViewsViewIdPositionsPut(viewId, viewPositionsIn)

Put View Positions

Full overwrite of positions for a view. Does NOT trigger display SSE broadcast.

### Example

```ts
import {
  Configuration,
  DefaultApi,
} from '';
import type { PutViewPositionsApiViewsViewIdPositionsPutRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DefaultApi();

  const body = {
    // string
    viewId: viewId_example,
    // ViewPositionsIn
    viewPositionsIn: ...,
  } satisfies PutViewPositionsApiViewsViewIdPositionsPutRequest;

  try {
    const data = await api.putViewPositionsApiViewsViewIdPositionsPut(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **viewId** | `string` |  | [Defaults to `undefined`] |
| **viewPositionsIn** | [ViewPositionsIn](ViewPositionsIn.md) |  | |

### Return type

`void` (Empty response body)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **204** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## subscribeDisplayApiDisplaySubscribeGet

> any subscribeDisplayApiDisplaySubscribeGet()

Subscribe Display

Subscribe to real-time display layer updates via SSE.

### Example

```ts
import {
  Configuration,
  DefaultApi,
} from '';
import type { SubscribeDisplayApiDisplaySubscribeGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DefaultApi();

  try {
    const data = await api.subscribeDisplayApiDisplaySubscribeGet();
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

This endpoint does not need any parameter.

### Return type

**any**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## subscribeStateApiStateSubscribeGet

> any subscribeStateApiStateSubscribeGet()

Subscribe State

Subscribe to real-time state updates via SSE.

### Example

```ts
import {
  Configuration,
  DefaultApi,
} from '';
import type { SubscribeStateApiStateSubscribeGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DefaultApi();

  try {
    const data = await api.subscribeStateApiStateSubscribeGet();
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

This endpoint does not need any parameter.

### Return type

**any**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## subscribeTasksApiTasksSubscribeGet

> any subscribeTasksApiTasksSubscribeGet()

Subscribe Tasks

Subscribe to real-time task updates via SSE (deprecated - use /state/subscribe).

### Example

```ts
import {
  Configuration,
  DefaultApi,
} from '';
import type { SubscribeTasksApiTasksSubscribeGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DefaultApi();

  try {
    const data = await api.subscribeTasksApiTasksSubscribeGet();
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

This endpoint does not need any parameter.

### Return type

**any**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

