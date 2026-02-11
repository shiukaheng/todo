
# AppState

Complete application state (graph + plans).

## Properties

Name | Type
------------ | -------------
`tasks` | [{ [key: string]: NodeOut; }](NodeOut.md)
`dependencies` | [{ [key: string]: DependencyOut; }](DependencyOut.md)
`hasCycles` | boolean
`plans` | [{ [key: string]: PlanOut; }](PlanOut.md)

## Example

```typescript
import type { AppState } from ''

// TODO: Update the object below with actual values
const example = {
  "tasks": null,
  "dependencies": null,
  "hasCycles": null,
  "plans": null,
} satisfies AppState

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as AppState
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


