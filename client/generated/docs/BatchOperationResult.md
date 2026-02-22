
# BatchOperationResult

Result of a single operation in a batch.

## Properties

Name | Type
------------ | -------------
`op` | string
`success` | boolean
`message` | string

## Example

```typescript
import type { BatchOperationResult } from ''

// TODO: Update the object below with actual values
const example = {
  "op": null,
  "success": null,
  "message": null,
} satisfies BatchOperationResult

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as BatchOperationResult
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


