
# EnrichedTaskOut

Enriched task response with computed properties.

## Properties

Name | Type
------------ | -------------
`task` | [TaskOut](TaskOut.md)
`directDeps` | Array&lt;string&gt;
`calculatedCompleted` | boolean
`calculatedDue` | number
`depsClear` | boolean

## Example

```typescript
import type { EnrichedTaskOut } from ''

// TODO: Update the object below with actual values
const example = {
  "task": null,
  "directDeps": null,
  "calculatedCompleted": null,
  "calculatedDue": null,
  "depsClear": null,
} satisfies EnrichedTaskOut

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as EnrichedTaskOut
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


