# DefaultApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**addTaskApiTasksPost**](DefaultApi.md#addtaskapitaskspost) | **POST** /api/tasks | Add Task |
| [**createPlanApiPlansPost**](DefaultApi.md#createplanapiplanspost) | **POST** /api/plans | Create Plan |
| [**deletePlanApiPlansPlanIdDelete**](DefaultApi.md#deleteplanapiplansplaniddelete) | **DELETE** /api/plans/{plan_id} | Delete Plan |
| [**getPlanApiPlansPlanIdGet**](DefaultApi.md#getplanapiplansplanidget) | **GET** /api/plans/{plan_id} | Get Plan |
| [**getStateApiStateGet**](DefaultApi.md#getstateapistateget) | **GET** /api/state | Get State |
| [**getTaskApiTasksTaskIdGet**](DefaultApi.md#gettaskapitaskstaskidget) | **GET** /api/tasks/{task_id} | Get Task |
| [**healthHealthGet**](DefaultApi.md#healthhealthget) | **GET** /health | Health |
| [**initDbApiInitPost**](DefaultApi.md#initdbapiinitpost) | **POST** /api/init | Init Db |
| [**linkTasksApiLinksPost**](DefaultApi.md#linktasksapilinkspost) | **POST** /api/links | Link Tasks |
| [**listPlansApiPlansGet**](DefaultApi.md#listplansapiplansget) | **GET** /api/plans | List Plans |
| [**listTasksApiTasksGet**](DefaultApi.md#listtasksapitasksget) | **GET** /api/tasks | List Tasks |
| [**removeTaskApiTasksTaskIdDelete**](DefaultApi.md#removetaskapitaskstaskiddelete) | **DELETE** /api/tasks/{task_id} | Remove Task |
| [**renameTaskApiTasksTaskIdRenamePost**](DefaultApi.md#renametaskapitaskstaskidrenamepost) | **POST** /api/tasks/{task_id}/rename | Rename Task |
| [**setTaskApiTasksTaskIdPatch**](DefaultApi.md#settaskapitaskstaskidpatch) | **PATCH** /api/tasks/{task_id} | Set Task |
| [**subscribeStateApiStateSubscribeGet**](DefaultApi.md#subscribestateapistatesubscribeget) | **GET** /api/state/subscribe | Subscribe State |
| [**subscribeTasksApiTasksSubscribeGet**](DefaultApi.md#subscribetasksapitaskssubscribeget) | **GET** /api/tasks/subscribe | Subscribe Tasks |
| [**unlinkTasksApiLinksDelete**](DefaultApi.md#unlinktasksapilinksdelete) | **DELETE** /api/links | Unlink Tasks |
| [**updatePlanApiPlansPlanIdPatch**](DefaultApi.md#updateplanapiplansplanidpatch) | **PATCH** /api/plans/{plan_id} | Update Plan |



## addTaskApiTasksPost

> NodeOut addTaskApiTasksPost(nodeCreate)

Add Task

Create a new task.

### Example

```ts
import {
  Configuration,
  DefaultApi,
} from '';
import type { AddTaskApiTasksPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DefaultApi();

  const body = {
    // NodeCreate
    nodeCreate: ...,
  } satisfies AddTaskApiTasksPostRequest;

  try {
    const data = await api.addTaskApiTasksPost(body);
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
| **nodeCreate** | [NodeCreate](NodeCreate.md) |  | |

### Return type

[**NodeOut**](NodeOut.md)

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


## createPlanApiPlansPost

> PlanOut createPlanApiPlansPost(planCreate)

Create Plan

Create a new plan.

### Example

```ts
import {
  Configuration,
  DefaultApi,
} from '';
import type { CreatePlanApiPlansPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DefaultApi();

  const body = {
    // PlanCreate
    planCreate: ...,
  } satisfies CreatePlanApiPlansPostRequest;

  try {
    const data = await api.createPlanApiPlansPost(body);
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
| **planCreate** | [PlanCreate](PlanCreate.md) |  | |

### Return type

[**PlanOut**](PlanOut.md)

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


## deletePlanApiPlansPlanIdDelete

> OperationResult deletePlanApiPlansPlanIdDelete(planId)

Delete Plan

Delete a plan.

### Example

```ts
import {
  Configuration,
  DefaultApi,
} from '';
import type { DeletePlanApiPlansPlanIdDeleteRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DefaultApi();

  const body = {
    // string
    planId: planId_example,
  } satisfies DeletePlanApiPlansPlanIdDeleteRequest;

  try {
    const data = await api.deletePlanApiPlansPlanIdDelete(body);
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


## linkTasksApiLinksPost

> DependencyOut linkTasksApiLinksPost(linkRequest)

Link Tasks

Create a dependency: from_id depends on to_id.

### Example

```ts
import {
  Configuration,
  DefaultApi,
} from '';
import type { LinkTasksApiLinksPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DefaultApi();

  const body = {
    // LinkRequest
    linkRequest: ...,
  } satisfies LinkTasksApiLinksPostRequest;

  try {
    const data = await api.linkTasksApiLinksPost(body);
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
| **linkRequest** | [LinkRequest](LinkRequest.md) |  | |

### Return type

[**DependencyOut**](DependencyOut.md)

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


## removeTaskApiTasksTaskIdDelete

> OperationResult removeTaskApiTasksTaskIdDelete(taskId)

Remove Task

Delete a task and its edges.

### Example

```ts
import {
  Configuration,
  DefaultApi,
} from '';
import type { RemoveTaskApiTasksTaskIdDeleteRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DefaultApi();

  const body = {
    // string
    taskId: taskId_example,
  } satisfies RemoveTaskApiTasksTaskIdDeleteRequest;

  try {
    const data = await api.removeTaskApiTasksTaskIdDelete(body);
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
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## renameTaskApiTasksTaskIdRenamePost

> OperationResult renameTaskApiTasksTaskIdRenamePost(taskId, renameRequest)

Rename Task

Rename a task (change its ID).

### Example

```ts
import {
  Configuration,
  DefaultApi,
} from '';
import type { RenameTaskApiTasksTaskIdRenamePostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DefaultApi();

  const body = {
    // string
    taskId: taskId_example,
    // RenameRequest
    renameRequest: ...,
  } satisfies RenameTaskApiTasksTaskIdRenamePostRequest;

  try {
    const data = await api.renameTaskApiTasksTaskIdRenamePost(body);
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
| **renameRequest** | [RenameRequest](RenameRequest.md) |  | |

### Return type

[**OperationResult**](OperationResult.md)

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


## setTaskApiTasksTaskIdPatch

> OperationResult setTaskApiTasksTaskIdPatch(taskId, nodeUpdate)

Set Task

Update a task\&#39;s properties.

### Example

```ts
import {
  Configuration,
  DefaultApi,
} from '';
import type { SetTaskApiTasksTaskIdPatchRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DefaultApi();

  const body = {
    // string
    taskId: taskId_example,
    // NodeUpdate
    nodeUpdate: ...,
  } satisfies SetTaskApiTasksTaskIdPatchRequest;

  try {
    const data = await api.setTaskApiTasksTaskIdPatch(body);
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
| **nodeUpdate** | [NodeUpdate](NodeUpdate.md) |  | |

### Return type

[**OperationResult**](OperationResult.md)

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


## unlinkTasksApiLinksDelete

> OperationResult unlinkTasksApiLinksDelete(linkRequest)

Unlink Tasks

Remove a dependency.

### Example

```ts
import {
  Configuration,
  DefaultApi,
} from '';
import type { UnlinkTasksApiLinksDeleteRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DefaultApi();

  const body = {
    // LinkRequest
    linkRequest: ...,
  } satisfies UnlinkTasksApiLinksDeleteRequest;

  try {
    const data = await api.unlinkTasksApiLinksDelete(body);
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
| **linkRequest** | [LinkRequest](LinkRequest.md) |  | |

### Return type

[**OperationResult**](OperationResult.md)

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


## updatePlanApiPlansPlanIdPatch

> PlanOut updatePlanApiPlansPlanIdPatch(planId, planUpdate)

Update Plan

Update a plan\&#39;s properties.

### Example

```ts
import {
  Configuration,
  DefaultApi,
} from '';
import type { UpdatePlanApiPlansPlanIdPatchRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DefaultApi();

  const body = {
    // string
    planId: planId_example,
    // PlanUpdate
    planUpdate: ...,
  } satisfies UpdatePlanApiPlansPlanIdPatchRequest;

  try {
    const data = await api.updatePlanApiPlansPlanIdPatch(body);
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
| **planUpdate** | [PlanUpdate](PlanUpdate.md) |  | |

### Return type

[**PlanOut**](PlanOut.md)

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

