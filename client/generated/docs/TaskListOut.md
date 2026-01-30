
# TaskListOut

Task list response.

## Properties

Name | Type
------------ | -------------
`tasks` | [Array&lt;EnrichedTaskOut&gt;](EnrichedTaskOut.md)
`hasCycles` | boolean

## Example

```typescript
import type { TaskListOut } from ''

// TODO: Update the object below with actual values
const example = {
  "tasks": null,
  "hasCycles": null,
} satisfies TaskListOut

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as TaskListOut
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


