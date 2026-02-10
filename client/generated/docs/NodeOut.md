
# NodeOut

Node response with calculated fields.

## Properties

Name | Type
------------ | -------------
`id` | string
`text` | string
`nodeType` | [NodeType](NodeType.md)
`completed` | boolean
`due` | number
`createdAt` | number
`updatedAt` | number
`calculatedValue` | boolean
`calculatedDue` | number
`depsClear` | boolean
`isActionable` | boolean
`parents` | Array&lt;string&gt;
`children` | Array&lt;string&gt;

## Example

```typescript
import type { NodeOut } from ''

// TODO: Update the object below with actual values
const example = {
  "id": null,
  "text": null,
  "nodeType": null,
  "completed": null,
  "due": null,
  "createdAt": null,
  "updatedAt": null,
  "calculatedValue": null,
  "calculatedDue": null,
  "depsClear": null,
  "isActionable": null,
  "parents": null,
  "children": null,
} satisfies NodeOut

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as NodeOut
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


