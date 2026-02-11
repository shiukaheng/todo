
# PlanUpdate

Update a plan (text and/or steps).

## Properties

Name | Type
------------ | -------------
`text` | string
`steps` | [Array&lt;StepData&gt;](StepData.md)

## Example

```typescript
import type { PlanUpdate } from ''

// TODO: Update the object below with actual values
const example = {
  "text": null,
  "steps": null,
} satisfies PlanUpdate

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as PlanUpdate
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


