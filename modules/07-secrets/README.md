# Module 7: Secrets Management 🔐
> Securely access sensitive information without hardcoding credentials

```text
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║                  MODULE 7: DAPR SECRETS MANAGEMENT                        ║
║                                                                           ║
║  Benefits:                                                                ║
║  - Abstract different secret stores (KV, Vault, Local)                    ║
║  - No secrets in source code or CI/CD logs                                ║
║  - Uniform API for developers                                             ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

## Secrets Flow Diagram

```text
   ┌──────────────────────┐
   │    Secret Store      │ <--- (e.g. HashiCorp Vault, Azure KV)
   │  [DB_PASSWORD: ****] │
   └──────────┬───────────┘
              │
        (1) Fetch Secret
              │
   ┌──────────▼───────────┐
   │     Dapr Sidecar     │
   └──────────┬───────────┘
              │
        (2) API Response (JSON)
              │
   ┌──────────▼───────────┐
   │   Python App (SDK)   │
   └──────────────────────┘
```

## 1. Configure Secret Store
Example: Local environment variable store (`secrets.yaml`):

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: env-secrets
spec:
  type: secretstores.local.env
  version: v1
  metadata: []
```

## 2. Retrieve Secrets in Python
Use the Dapr Client to fetch secrets dynamically.

```python
from dapr.clients import DaprClient

def get_db_credentials():
    with DaprClient() as client:
        # Get one secret
        secret = client.get_secret(
            store_name='env-secrets',
            key='DATABASE_URL'
        )
        print(f"Secret: {secret.secret}")

        # Get all secrets from a store
        all_secrets = client.get_bulk_secret(store_name='env-secrets')
        print(f"All Secrets keys: {all_secrets.keys()}")

if __name__ == "__main__":
    get_db_credentials()
```

## 3. Best Practices
1. **Never Log Secrets**: Even if Dapr makes it easy to fetch them, ensure your application logic doesn't print them to console/logs.
2. **Scoping**: Use Dapr's `scopes` metadata to limit which applications can access specific secret stores.
3. **Rotation**: Rely on external store rotation policies; Dapr will fetch the latest version when called.
