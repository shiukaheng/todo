
# NodeListOut

Node list response.

## Properties

Name | Type
------------ | -------------
`tasks` | [{ [key: string]: NodeOut; }](NodeOut.md)
`dependencies` | [{ [key: string]: DependencyOut; }](DependencyOut.md)
`hasCycles` | boolean

## Example

```typescript
import type { NodeListOut } from ''

// TODO: Update the object below with actual values
const example = {
  "tasks": null,
  "dependencies": null,
  "hasCycles": null,
} satisfies NodeListOut

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as NodeListOut
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


