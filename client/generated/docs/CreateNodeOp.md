
# CreateNodeOp

Create a node.

## Properties

Name | Type
------------ | -------------
`op` | string
`id` | string
`text` | string
`completed` | number
`nodeType` | [NodeType](NodeType.md)
`due` | number
`depends` | Array&lt;string&gt;
`blocks` | Array&lt;string&gt;

## Example

```typescript
import type { CreateNodeOp } from ''

// TODO: Update the object below with actual values
const example = {
  "op": null,
  "id": null,
  "text": null,
  "completed": null,
  "nodeType": null,
  "due": null,
  "depends": null,
  "blocks": null,
} satisfies CreateNodeOp

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as CreateNodeOp
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


