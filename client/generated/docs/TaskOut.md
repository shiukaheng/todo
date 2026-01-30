
# TaskOut

Task response.

## Properties

Name | Type
------------ | -------------
`id` | string
`text` | string
`completed` | boolean
`inferred` | boolean
`due` | number
`createdAt` | number
`updatedAt` | number

## Example

```typescript
import type { TaskOut } from ''

// TODO: Update the object below with actual values
const example = {
  "id": null,
  "text": null,
  "completed": null,
  "inferred": null,
  "due": null,
  "createdAt": null,
  "updatedAt": null,
} satisfies TaskOut

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as TaskOut
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


