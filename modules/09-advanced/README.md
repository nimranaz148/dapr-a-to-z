# Module 9: Advanced Patterns & Best Practices 🚀
> Architectural strategies for production-grade Dapr applications

```text
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║                  MODULE 9: ADVANCED DAPR PATTERNS                         ║
║                                                                           ║
║  Topics:                                                                  ║
║  - SAGA Pattern (Distributed Transactions)                                ║
║  - Sidecar Lifecycle Management                                           ║
║  - Secure gRPC communication                                              ║
║  - Production Deployment Strategies                                       ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

## 1. SAGA Pattern with Dapr
Since Dapr doesn't support distributed transactions directly, we use the SAGA pattern (compensating transactions) with Pub/Sub.

```text
    ┌─────────────┐       (1) Success       ┌──────────────┐
    │  Service A  ├────────────────────────►│  Service B   │
    └──────┬──────┘                         └──────┬───────┘
           │                                       │
           │ (2) Failure                           │
           │                                       │
    ┌──────▼──────┐       (3) Compensate    ┌──────▼───────┐
    │  Revert A   │◄────────────────────────┤   Revert B   │
    └─────────────┘                         └──────────────┘
```

## 2. Best Practices for Python
1. **Asyncio Always**: Dapr's Python SDK is built for `asyncio`. Use it to prevent sidecar communication from blocking your main thread.
2. **Lean Sidecars**: Only enable components you actually use to reduce resource footprint.
3. **App-Port Readiness**: Ensure your Python application (Flask/FastAPI/Uvicorn) is fully ready before Dapr starts sending traffic. Use the `DAPR_HTTP_PORT` check.

## 3. Production Readiness Checklist
- [ ] **mTLS**: Enable Mutual TLS for sidecar-to-sidecar communication.
- [ ] **API Token**: Use `DAPR_API_TOKEN` to secure your application's communication with the sidecar.
- [ ] **Resource Limits**: Set CPU/Memory limits for both your container and the Dapr sidecar container.
- [ ] **Health Checks**: Implement `/healthz` endpoints and let Dapr know via `app-health-path`.

## 4. Deployment Pattern: Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: python-app
spec:
  template:
    metadata:
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "python-app"
        dapr.io/app-port: "8000"
        dapr.io/enable-mtls: "true"
...
```

## Future Learning
- Explore **Dapr Workflow** (Alpha) for stateful orchestrations.
- Deep dive into **Pluggable Components**.
- Join the Dapr Discord community.
