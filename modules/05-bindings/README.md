# Module 5: Bindings 🔗
> Connect your application to external systems with ease using Dapr Bindings

```text
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║                        MODULE 5: DAPR BINDINGS                            ║
║                                                                           ║
║  Objectives:                                                              ║
║  - Trigger code from external events (Input Bindings)                     ║
║  - Call external resources (Output Bindings)                               ║
║  - Decouple infrastructure from application logic                        ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

## Architecture Diagram

```text
    ┌──────────────────────┐           ┌──────────────────────┐
    │   External System    │           │   External System    │
    │  (Kafka, Cron, S3)   │           │ (Twilio, SendGrid)   │
    └──────────┬───────────┘           └──────────▲───────────┘
               │                                  │
      (1) Input Event                    (4) Output Call
               │                                  │
    ┌──────────▼───────────┐           ┌──────────┴───────────┐
    │     Dapr Sidecar     │           │     Dapr Sidecar     │
    └──────────┬───────────┘           └──────────▲───────────┘
               │                                  │
      (2) HTTP/gRPC Post                 (3) HTTP/gRPC Post
               │                                  │
    ┌──────────▼───────────┐           ┌──────────┴───────────┐
    │   Python App (SDK)   │           │   Python App (SDK)   │
    └──────────────────────┘           └──────────────────────┘
```

## 1. Input Bindings
Input bindings trigger your application when an event occurs in an external resource.

### Example: Cron Binding
Configuration (`cron.yaml`):
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: scheduled-task
spec:
  type: bindings.cron
  version: v1
  metadata:
    - name: schedule
      value: "@every 1m"
```

Python Implementation:
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/scheduled-task', methods=['POST'])
def handle_cron():
    print("Executing scheduled task every minute!")
    return jsonify(success=True), 200

if __name__ == "__main__":
    app.run(port=5000)
```

## 2. Output Bindings
Output bindings allow you to invoke external resources without knowing their implementation details.

### Example: HTTP Output Binding
Configuration (`http-binding.yaml`):
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: external-api
spec:
  type: bindings.http
  version: v1
  metadata:
    - name: url
      value: "https://api.example.com/data"
```

Python Implementation (SDK):
```python
from dapr.clients import DaprClient

def call_external_api():
    with DaprClient() as client:
        # Invoke the output binding
        resp = client.invoke_binding(
            binding_name='external-api',
            operation='create',
            binding_data='{"message": "Hello from Dapr"}'
        )
        print(f"Response: {resp.data}")

if __name__ == "__main__":
    call_external_api()
```

## Summary of Patterns
1. **Separation of Concerns**: Your Python code doesn't need to know how to talk to Kafka, SQS, or Twilio.
2. **Portability**: Change the binding component YAML to switch providers without changing Python code.
3. **Triggered Execution**: Effortlessly build event-driven systems.
