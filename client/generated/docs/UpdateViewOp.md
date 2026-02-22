
# UpdateViewOp

Upsert a view. Creates if not exists, replaces provided fields.

## Properties

Name | Type
------------ | -------------
`op` | string
`viewId` | string
`whitelist` | Array&lt;string&gt;
`blacklist` | Array&lt;string&gt;

## Example

```typescript
import type { UpdateViewOp } from ''

// TODO: Update the object below with actual values
const example = {
  "op": null,
  "viewId": null,
  "whitelist": null,
  "blacklist": null,
} satisfies UpdateViewOp

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as UpdateViewOp
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


