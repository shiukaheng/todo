
# UpdatePlanOp

Update a plan.

## Properties

Name | Type
------------ | -------------
`op` | string
`id` | string
`text` | string
`steps` | [Array&lt;StepData&gt;](StepData.md)

## Example

```typescript
import type { UpdatePlanOp } from ''

// TODO: Update the object below with actual values
const example = {
  "op": null,
  "id": null,
  "text": null,
  "steps": null,
} satisfies UpdatePlanOp

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as UpdatePlanOp
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


