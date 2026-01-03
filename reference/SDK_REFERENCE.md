# Dapr Python SDK Deep Dive Reference 📚

This guide covers the `DaprClient` methods, their parameters, and advanced usage patterns for every major building block.

---

## 1. State Management Reference

### `save_state`
Saves one or more state items.

```python
client.save_state(
    store_name="statestore",
    key="order-123",
    value="some-data",
    etag="1",                     # Optional: For optimistic concurrency
    options={                     # Optional: StateOptions
        "consistency": "strong",  # "eventual" or "strong"
        "concurrency": "first-write" # "first-write" or "last-write"
    },
    metadata={"ttlInSeconds": "60"} # Optional: TTL or custom component metadata
)
```

### `get_state`
Retrieves state for a specific key.

```python
response = client.get_state(
    store_name="statestore",
    key="order-123",
    consistency="strong",      # Optional: Query consistency
    metadata={"foo": "bar"}    # Optional: Custom metadata
)
# Access data: response.data, response.etag, response.metadata
```

### `delete_state`
```python
client.delete_state(
    store_name="statestore",
    key="order-123",
    etag="1",                  # Optional
    options={"consistency": "strong"}, # Optional
    metadata={}                # Optional
)
```

### `get_bulk_state`
```python
response = client.get_bulk_state(
    store_name="statestore",
    keys=["k1", "k2"],
    parallelism=10,            # Optional: Max parallel requests
    metadata={}
)
for item in response.items:
    print(item.key, item.data)
```

---

## 2. Pub/Sub Reference

### `publish_event`
```python
client.publish_event(
    pubsub_name="messagebus",
    topic_name="new-orders",
    data={"id": 1},            # Data will be serialized based on content_type
    data_content_type="application/json", # Optional
    metadata={                 # Optional: TTL, Raw Payload, etc.
        "ttlInSeconds": "120",
        "rawPayload": "false"
    }
)
```

---

## 3. Service Invocation Reference

### `invoke_method`
```python
client.invoke_method(
    app_id="inventory-service",
    method_name="check-stock",
    data='{"id": "apple"}',    # String or bytes
    http_verb="POST",          # GET, POST, PUT, DELETE, etc.
    data_content_type="application/json",
    metadata={"x-custom-header": "val"} # Passes as request headers
)
```

---

## 4. Bindings Reference

### `invoke_binding`
```python
client.invoke_binding(
    binding_name="storage-bucket",
    operation="create",        # Determined by the component type
    data='file-content',
    binding_metadata={"fileName": "test.txt"} # Binding-specific metadata
)
```

---

## 5. Secrets Reference

### `get_secret`
```python
secret_response = client.get_secret(
    store_name="vault",
    key="db-password",
    metadata={"version": "1"} # Optional: Store-specific metadata
)
# result: secret_response.secret (dict)
```

---

## 6. Configuration Reference (Alpha)

### `get_configuration`
```python
response = client.get_configuration(
    store_name="config-store",
    keys=["app-settings"],
    metadata={}
)
```

---

## 7. Configuration for `DaprClient`
You can initialize the client with custom settings:

```python
from dapr.clients import DaprClient

# Connect to a remote sidecar or specific ports
client = DaprClient(address='localhost:50001')
```

---

## 8. Common Data Types
- **Etag**: A string used for concurrency control.
- **StateOptions**: Controls consistency and concurrency.
- **DaprClientResponse**: Wrapper for responses containing `.data`, `.headers`, `.metadata`.
