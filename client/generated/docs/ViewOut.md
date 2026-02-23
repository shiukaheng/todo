
# ViewOut

View response.

## Properties

Name | Type
------------ | -------------
`id` | string
`positions` | { [key: string]: any; }
`whitelist` | Array&lt;string&gt;
`blacklist` | Array&lt;string&gt;
`createdAt` | number
`updatedAt` | number

## Example

```typescript
import type { ViewOut } from ''

// TODO: Update the object below with actual values
const example = {
  "id": null,
  "positions": null,
  "whitelist": null,
  "blacklist": null,
  "createdAt": null,
  "updatedAt": null,
} satisfies ViewOut

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ViewOut
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


