#!/bin/bash
# Generate TypeScript client from OpenAPI spec
# Requires: npm install -g @openapitools/openapi-generator-cli

set -e

API_URL="${1:-http://localhost:8000}"

echo "Fetching OpenAPI spec from $API_URL..."
curl -s "$API_URL/openapi.json" > openapi.json

echo "Generating TypeScript client..."
npx @openapitools/openapi-generator-cli generate \
  -i openapi.json \
  -g typescript-fetch \
  -o generated \
  --additional-properties=supportsES6=true,typescriptThreePlus=true

echo "Done. Client generated in ./generated/"
