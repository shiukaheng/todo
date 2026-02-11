
# PlanCreate

Create a plan with steps.

## Properties

Name | Type
------------ | -------------
`id` | string
`text` | string
`steps` | [Array&lt;StepData&gt;](StepData.md)

## Example

```typescript
import type { PlanCreate } from ''

// TODO: Update the object below with actual values
const example = {
  "id": null,
  "text": null,
  "steps": null,
} satisfies PlanCreate

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as PlanCreate
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


