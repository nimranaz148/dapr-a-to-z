# Module 2: Service Invocation Deep Dive 📞

This module demonstrates how to perform service-to-service communication with all available Python SDK parameters.

## Client-Side Code (`caller.py`)

```python
import asyncio
from dapr.clients import DaprClient

async def run():
    async with DaprClient() as client:
        # 1. Basic POST request
        print("--- Basic POST ---")
        resp = await client.invoke_method(
            app_id='target-app',
            method_name='hello',
            data='{"name": "Dapr Master"}',
            http_verb='POST'
        )
        print(f"Response: {resp.data.decode('utf-8')}")

        # 2. GET request with Metadata (Headers)
        print("\n--- GET with Headers ---")
        resp = await client.invoke_method(
            app_id='target-app',
            method_name='get-info',
            http_verb='GET',
            metadata={'x-user-id': 'dev-001'} # This becomes an HTTP header
        )
        print(f"Response: {resp.data.decode('utf-8')}")

        # 3. Invocation with custom Content-Type
        print("\n--- Custom Content-Type ---")
        resp = await client.invoke_method(
            app_id='target-app',
            method_name='xml-endpoint',
            data='<root>data</root>',
            http_verb='POST',
            data_content_type='application/xml'
        )
        print(f"Status: {resp.status_code}")

if __name__ == '__main__':
    asyncio.run(run())
```

## Detailed Parameter Explanation

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `app_id` | `str` | The unique ID of the target application (defined in Dapr). |
| `method_name` | `str` | The route or method to call on the target application. |
| `data` | `bytes/str` | The payload. Can be JSON, XML, or binary data. |
| `http_verb` | `str` | Standard HTTP methods: `GET`, `POST`, `PUT`, `DELETE`. |
| `metadata` | `dict` | Key-value pairs translated to HTTP headers or gRPC metadata. |
| `data_content_type`| `str` | Specifies the MIME type of the `data`. |

## Key Methods in `DaprClient`:
- `invoke_method()`: Main entry point for service invocation.
- `invoke_method_async()`: The asynchronous version (as shown above).

## Resiliency in Invocation
By default, Dapr handles retries. You can override this using a `Resiliency` component as discussed in Module 8.
