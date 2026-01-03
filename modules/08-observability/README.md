# Module 8: Observability & Resiliency 📊🛡️
> Build robust, transparent, and self-healing distributed systems

```text
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║               MODULE 8: OBSERVABILITY & RESILIENCY                        ║
║                                                                           ║
║  Features:                                                                ║
║  - Distributed Tracing (W3C Trace Context)                                ║
║  - Metrics (Prometheus/Grafana)                                           ║
║  - Retries, Timeouts, and Circuit Breakers                                ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

## Resiliency Diagram: Circuit Breaker

```text
       Normal Flow                Circuit Open (Failing)
    ┌───────────────┐           ┌───────────────┐
    │  Python App   │           │  Python App   │
    └───────┬───────┘           └───────┬───────┘
            │                           │
    ┌───────▼───────┐           ┌───────▼───────┐
    │ Dapr Sidecar  │           │ Dapr Sidecar  │ (Fail Fast!)
    │[Resiliency Pol]           │[Circuit Open] ──┐
    └───────┬───────┘           └───────┬───────┘ │
            │                           │         │ (Reject)
    ┌───────▼───────┐           ┌───────▼───────┐ │
    │ Target Service│           │ Broken Service│ <┘
    │    (Down)     │           │    (Down)     │
    └───────────────┘           └───────────────┘
```

## 1. Resiliency Policies
Configuration (`resiliency.yaml`):

```yaml
apiVersion: dapr.io/v1alpha1
kind: Resiliency
metadata:
  name: myresiliency
spec:
  policies:
    retries:
      retryApi:
        policy: constant
        duration: 5s
        maxRetries: 3
    circuitBreakers:
      cbApi:
        maxRequests: 1
        timeout: 30s
        trip: consecutiveFailures >= 5
  targets:
    apps:
      target-app:
        retry: retryApi
        circuitBreaker: cbApi
```

## 2. Observability: Tracing
Dapr automatically injects trace headers.

```python
from dapr.clients import DaprClient
import logging

logging.basicConfig(level=logging.INFO)

def make_call_with_tracing():
    # Dapr handles the propagation of Traceparent headers automatically
    with DaprClient() as client:
        client.invoke_method('order-service', 'process', data='{}')
        logging.info("Method invoked. Check Zipkin/Jaeger for trace.")
```

## 3. Metrics
Dapr exposes a Prometheus endpoint at `:9090` by default.

Key metrics for Python devs:
- `dapr_runtime_service_invocation_req_count`: Total requests made.
- `dapr_runtime_service_invocation_req_latency`: Response times.
- `dapr_component_operation_latencies`: Performance of state stores/pub-sub.

## Summary
- **Zero-code Tracing**: You get a graph of your whole microservice architecture without changing Python code.
- **Fail-Safe**: Protect your Python app from cascading failures using Retries and Circuit Breakers.
