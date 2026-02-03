
# TaskCreate

Task creation request.

## Properties

Name | Type
------------ | -------------
`text` | string
`completed` | boolean
`inferred` | boolean
`due` | number
`id` | string
`depends` | Array&lt;string&gt;
`blocks` | Array&lt;string&gt;

## Example

```typescript
import type { TaskCreate } from ''

// TODO: Update the object below with actual values
const example = {
  "text": null,
  "completed": null,
  "inferred": null,
  "due": null,
  "id": null,
  "depends": null,
  "blocks": null,
} satisfies TaskCreate

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as TaskCreate
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


