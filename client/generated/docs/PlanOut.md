
# PlanOut

Plan response.

## Properties

Name | Type
------------ | -------------
`id` | string
`text` | string
`createdAt` | number
`updatedAt` | number
`steps` | [Array&lt;StepData&gt;](StepData.md)

## Example

```typescript
import type { PlanOut } from ''

// TODO: Update the object below with actual values
const example = {
  "id": null,
  "text": null,
  "createdAt": null,
  "updatedAt": null,
  "steps": null,
} satisfies PlanOut

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as PlanOut
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


