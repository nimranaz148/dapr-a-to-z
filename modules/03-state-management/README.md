# Module 3: State Management 🗄️

> Learn how to store and retrieve application state using Dapr's state management building block

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║                    MODULE 3: STATE MANAGEMENT                            ║
║                                                                           ║
║  Goals:                                                                   ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ║
║  • Understand Dapr state management concepts                             ║
║  • Learn CRUD operations on state                                        ║
║  • Master state consistency and concurrency patterns                    ║
║  • Use transactions for atomic operations                               ║
║  • Configure different state stores                                      ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

## Table of Contents

1. [What is State Management?](#what-is-state-management)
2. [State Management Architecture](#state-management-architecture)
3. [Supported State Stores](#supported-state-stores)
4. [Basic State Operations](#basic-state-operations)
5. [Advanced Features](#advanced-features)
6. [Transactions](#transactions)
7. [Configuration](#configuration)
8. [Exercises](#exercises)

---

## What is State Management?

State management in Dapr allows your application to store, retrieve, and delete key-value pairs without being tied to a specific storage backend.

### Why Use Dapr for State?

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    Without Dapr State Management                         │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────┐         ┌─────────────┐         ┌─────────────┐        │
│  │   Service   │         │   Service   │         │   Service   │        │
│  │     A       │         │     B       │         │     C       │        │
│  └──────┬──────┘         └──────┬──────┘         └──────┬──────┘        │
│         │                       │                       │              │
│         │  Redis Library        │  Redis Library       │  Redis       │
│         ├───────────────────────┼───────────────────────► Library      │
│         │                       │                       │              │
│         ▼                       ▼                       ▼              │
│  ┌─────────────┐         ┌─────────────┐         ┌─────────────┐        │
│  │ Redis SDK   │         │ Redis SDK   │         │ Redis SDK   │        │
│  │ - Connection│         │ - Connection│         │ - Connection│       │
│  │ - Retry     │         │ - Retry     │         │ - Retry     │       │
│  │ - Serial    │         │ - Serial    │         │ - Serial    │       │
│  └──────┬──────┘         └──────┬──────┘         └──────┬──────┘        │
│         │                       │                       │              │
│         └───────────────────────┼───────────────────────┘              │
│                                 │                                      │
│                                 ▼                                      │
│                         ┌─────────────┐                               │
│                         │   Redis     │                               │
│                         └─────────────┘                               │
│                                                                          │
║  Problem: Vendor lock-in, repeated code, hard to switch stores         ║
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

```
┌──────────────────────────────────────────────────────────────────────────┐
│                      With Dapr State Management                         │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────┐         ┌─────────────┐         ┌─────────────┐        │
│  │   Service   │         │   Service   │         │   Service   │        │
│  │     A       │         │     B       │         │     C       │        │
│  └──────┬──────┘         └──────┬──────┘         └──────┬──────┘        │
│         │                       │                       │              │
│         │ Dapr Client           │ Dapr Client           │ Dapr Client   │
│         │ save_state()          │ save_state()          │ save_state()  │
│         ├───────────────────────┼───────────────────────┼              │
│         ▼                       ▼                       ▼              │
│  ┌─────────────┐         ┌─────────────┐         ┌─────────────┐        │
│  │ Dapr Sidecar│         │ Dapr Sidecar│         │ Dapr Sidecar│        │
│  └──────┬──────┘         └──────┬──────┘         └──────┬──────┘        │
│         │                       │                       │              │
│         └───────────────────────┼───────────────────────┘              │
│                                 │                                      │
│                         ┌───────▼────────┐                            │
│                         │  Dapr Runtime  │                            │
│                         │  (Abstraction) │                            │
│                         └───────┬────────┘                            │
│                                 │                                      │
│                    ┌────────────┼────────────┐                         │
│                    │            │            │                         │
│              ┌─────▼────┐  ┌────▼────┐  ┌────▼────┐                    │
│              │  Redis   │  │PostgreSQL│  │  Azure  │                  │
│              └──────────┘  │  Cosmos   │  └─────────┘                  │
│                            └──────────┘                               │
│                                                                          │
║  Benefit: Switch stores with config change, no code change!            ║
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## State Management Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    State Management Request Flow                        │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                        Your Application                           │   │
│  │  ┌─────────────────────────────────────────────────────────┐    │   │
│  │  │  dapr.save_state(store_name="mystore", key="user:1")   │    │   │
│  │  └─────────────────────────────────────────────────────────┘    │   │
│  └───────────────────────────────┬───────────────────────────────────┘   │
│                                  │ gRPC/HTTP                          │
│                                  ▼                                      │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                         Dapr Sidecar                             │   │
│  │  ┌─────────────────────────────────────────────────────────┐  │   │
│  │  │  State Store Component (mystore)                         │  │   │
│  │  │  - Applies ETag check                                    │  │   │
│  │  │  - Applies TTL                                           │  │   │
│  │  │  - Serializes/Deserializes                               │  │   │
│  │  │  - Handles retry logic                                    │  │   │
│  │  └─────────────────────────────────────────────────────────┘  │   │
│  └────────────────────────────────────────┬────────────────────────┘   │
│                                           │                             │
│                                           ▼                             │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                      State Store Backend                         │   │
│  │                    (Redis, PostgreSQL, etc.)                     │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Supported State Stores

Dapr supports a wide variety of state stores:

```
╔══════════════════════════════════════════════════════════════════════════╗
║                      Supported State Stores                              ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  ┌─────────────────────────────────────────────────────────────────┐    ║
║  │  IN-MEMORY                                                       │    ║
║  │  • In-Memory (Redis)                                             │    ║
║  │  • Memcached                                                      │    ║
║  └─────────────────────────────────────────────────────────────────┘    ║
║                                                                          ║
║  ┌─────────────────────────────────────────────────────────────────┐    ║
║  │  SQL DATABASES                                                    │    ║
║  │  • PostgreSQL                                                    │    ║
║  │  • MySQL                                                         │    ║
║  │  • SQL Server                                                    │    ║
║  │  • MariaDB                                                       │    ║
║  └─────────────────────────────────────────────────────────────────┘    ║
║                                                                          ║
║  ┌─────────────────────────────────────────────────────────────────┐    ║
║  │  NOSQL DATABASES                                                  │    ║
║  │  • Redis                                                         │    ║
║  │  • MongoDB                                                       │    ║
║  │  • Cassandra                                                     │    ║
║  │  • ScyllaDB                                                      │    ║
║  └─────────────────────────────────────────────────────────────────┘    ║
║                                                                          ║
║  ┌─────────────────────────────────────────────────────────────────┐    ║
║  │  CLOUD NATIVE                                                    │    ║
║  │  • Azure Cosmos DB                                               │    ║
║  │  • Azure Table Storage                                           │    ║
║  │  • AWS DynamoDB                                                  │    ║
║  │  • Google Cloud Datastore                                       │    ║
║  │  • GCP Firestore                                                 │    ║
║  └─────────────────────────────────────────────────────────────────┘    ║
║                                                                          ║
║  ┌─────────────────────────────────────────────────────────────────┐    ║
║  │  OTHERS                                                          │    ║
║  │  • Aerospike                                                     │    ║
║  │  • Couchbase                                                     │    ║
║  │  • etcd                                                          │    ║
║  │  • HashiCorp Consul                                             │    ║
║  └─────────────────────────────────────────────────────────────────┘    ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
```

---

## Basic State Operations

### Setup

First, create a Redis component configuration:

```yaml
# .dapr/components/statestore.yaml
apiVersion: dapr.io/v1
kind: Component
metadata:
  name: statestore
  namespace: default
spec:
  type: state.redis
  version: v1
  initTimeout: 1m
  metadata:
  - name: redisHost
    value: localhost:6379
  - name: redisPassword
    value: ""
  - name: enableTLS
    value: "false"
  - name: failover
    value: "false"
```

### 1. Save State

```python
from dapr.clients import DaprClient
import json

# Simple string value
with DaprClient() as dapr:
    dapr.save_state(
        store_name="statestore",
        key="user:1:name",
        value="Alice"
    )

# JSON object
user_data = {
    "name": "Alice",
    "email": "alice@example.com",
    "age": 30
}
dapr.save_state(
    store_name="statestore",
    key="user:1",
    value=json.dumps(user_data)
)
```

### 2. Get State

```python
from dapr.clients import DaprClient

with DaprClient() as dapr:
    # Get state
    state = dapr.get_state(store_name="statestore", key="user:1:name")

    if state.data:
        print(f"Name: {state.json()}")
    else:
        print("State not found")
```

### 3. Delete State

```python
from dapr.clients import DaprClient

with DaprClient() as dapr:
    dapr.delete_state(store_name="statestore", key="user:1")
```

### 4. Bulk Operations

```python
from dapr.clients import DaprClient

with DaprClient() as dapr:
    # Save multiple states
    states = [
        ("user:1", json.dumps({"name": "Alice", "age": 30})),
        ("user:2", json.dumps({"name": "Bob", "age": 25})),
        ("user:3", json.dumps({"name": "Charlie", "age": 35})),
    ]

    for key, value in states:
        dapr.save_state(store_name="statestore", key=key, value=value)

    # Get multiple states
    keys = ["user:1", "user:2", "user:3"]
    items = dapr.get_bulk_state(store_name="statestore", keys=keys)

    for item in items:
        print(f"{item.key}: {item.json()}")

    # Delete multiple states
    for key in keys:
        dapr.delete_state(store_name="statestore", key=key)
```

---

## Advanced Features

### 1. ETags (Optimistic Concurrency)

ETags prevent concurrent modifications from overwriting each other:

```
┌──────────────────────────────────────────────────────────────────────────┐
│                     Optimistic Concurrency with ETags                    │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Client A                               Client B                          │
│     │                                      │                             │
│     │ GET user:1 (ETag: v1)                │                             │
│     ├─────────────────────────────────────►│                             │
│     │                                      │                             │
│     │ {balance: 100, ETag: v1}             │                             │
│     ◄─────────────────────────────────────┤                             │
│     │                                      │                             │
│     │ balance += 50                        │                             │
│     │                                      │ GET user:1 (ETag: v1)        │
│     │                                      ├────────────────────────────►│
│     │                                      │                             │
│     │                                      │ {balance: 100, ETag: v1}     │
│     │                                      ◄────────────────────────────┤
│     │                                      │                             │
│     │ PUT user:1 (ETag: v1, balance: 150)   │ balance += 20               │
│     ├─────────────────────────────────────►│                             │
│     │ ◄─ SUCCESS                           │                             │
│     │ (New ETag: v2)                       │                             │
│     │                                      │ PUT user:1 (ETag: v1,       │
│     │                                      │       balance: 120)          │
│     │                                      ├────────────────────────────►│
│     │                                      │ ◄─ CONFLICT (ETag mismatch)│
│     │                                      │                             │
║  Client B must fetch new state and retry                           ║
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

```python
from dapr.clients import DaprClient
from dapr.clients.grpc._state import StateItem
import json

with DaprClient() as dapr:
    # Get current state
    state = dapr.get_state(store_name="statestore", key="account:1")
    account = json.loads(state.json())
    current_etag = state.etag

    print(f"Current: {account}, ETag: {current_etag}")

    # Modify with optimistic concurrency
    account["balance"] += 50

    try:
        dapr.save_state(
            store_name="statestore",
            key="account:1",
            value=json.dumps(account),
            etag=current_etag  # Use the ETag we got
        )
        print("Update successful!")
    except Exception as e:
        print(f"Conflict! Someone else modified the state. Error: {e}")
```

### 2. TTL (Time to Live)

Automatically expire state after a specified time:

```python
from dapr.clients import DaprClient
from dapr.clients.grpc._state import StateItem, StateOptions
from datetime import timedelta
import json

with DaprClient() as dapr:
    # Save state with TTL of 1 hour
    options = StateOptions(
        metadata={
            "ttlInSeconds": "3600"  # 1 hour
        }
    )

    dapr.save_state(
        store_name="statestore",
        key="session:abc123",
        value=json.dumps({"user_id": "1", "expires_at": "1h"}),
        state_options=options
    )

    print("State saved with 1 hour TTL")
```

### 3. State Metadata

Additional metadata that can be attached to state:

```python
from dapr.clients import DaprClient
from dapr.clients.grpc._state import StateOptions

with DaprClient() as dapr:
    options = StateOptions(
        metadata={
            "ttlInSeconds": "3600",
            "secondaryIndex": "user_id:123",
            "createdBy": "serviceA",
            "contentType": "application/json"
        }
    )

    dapr.save_state(
        store_name="statestore",
        key="document:456",
        value="document content",
        state_options=options
    )
```

### 4. Consistency Levels

Dapr supports different consistency models:

```
┌──────────────────────────────────────────────────────────────────────────┐
│                      State Consistency Levels                             │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
║  STRONG                   EVENTUAL                   CABOA               ║
║  ┌─────────┐              ┌─────────┐              ┌─────────┐          ║
║  │   All   │              │   Any   │              │   Quorum│          ║
║  │  nodes  │              │  node   │              │  nodes  │          ║
║  │   sync  │              │  write  │              │   sync  │          ║
║  └────┬────┘              └────┬────┘              └────┬────┘          ║
║       │                        │                        │                ║
║       ▼                        ▼                        ▼                ║
║   ┌─────────┐              ┌─────────┐              ┌─────────┐         ║
║   │ 100%    │              │ Fast    │              │ Balanced│         ║
║   │ Accurate│              │ No sync │              │  sync   │         ║
║   │  Slow   │              │         │              │         │         ║
║   └─────────┘              └─────────┘              └─────────┘         ║
║                                                                          ║
║  • STRONG:  Wait for all replicas to acknowledge                         ║
║  • EVENTUAL: Write succeeds without waiting for replicas                 ║
║  • CABOA: Converge Aggressive Bounded Availability                       ║
║                                                                          ║
└──────────────────────────────────────────────────────────────────────────┘
```

```python
from dapr.clients import DaprClient
from dapr.clients.grpc._state import StateOptions, Consistency

with DaprClient() as dapr:
    options = StateOptions(
        consistency=Consistency.STRONG  # STRONG, EVENTUAL, or CABOA
    )

    dapr.save_state(
        store_name="statestore",
        key="critical:data",
        value="important_data",
        state_options=options
    )
```

---

## Transactions

Transactions allow you to perform multiple state operations atomically.

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    Transaction Flow                                      │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Application                                                     │    │
│  │  ┌─────────────────────────────────────────────────────────┐    │    │
│  │  │  START TRANSACTION                                        │    │    │
│  │  │    Operation 1: Save A                                   │    │    │
║  │  │    Operation 2: Save B                                   │    │    ║
║  │  │    Operation 3: Delete C                                 │    │    ║
║  │  │  COMMIT TRANSACTION                                      │    │    ║
│  │  └─────────────────────────────────────────────────────────┘    │    │
│  └────────────────────────────────────────┬────────────────────────┘    │
│                                           │                             │
│                                           ▼                             │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Dapr Sidecar                                                    │    │
│  │  ┌─────────────────────────────────────────────────────────┐    │    │
│  │  │  If all operations succeed:                              │    │    │
│  │  │    Apply all changes to state store                       │    │    │
│  │  │  If any operation fails:                                 │    │    │
║  │  │    Rollback ALL changes (no partial state)               │    │    ║
│  │  └─────────────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

### Transaction Example

```python
from dapr.clients import DaprClient
from dapr.clients.grpc._state import StateItem, TransactionOperationType
import json

def transfer_money(from_account: str, to_account: str, amount: float):
    with DaprClient() as dapr:
        # Get current balances
        from_state = dapr.get_state(store_name="statestore", key=f"account:{from_account}")
        to_state = dapr.get_state(store_name="statestore", key=f"account:{to_account}")

        from_balance = json.loads(from_state.json())["balance"] if from_state.data else 0
        to_balance = json.loads(to_state.json())["balance"] if to_state.data else 0

        if from_balance < amount:
            raise ValueError("Insufficient funds")

        # Create transaction operations
        operations = [
            TransactionOperationType(
                operation_type="upsert",
                request=StateItem(
                    key=f"account:{from_account}",
                    value=json.dumps({"balance": from_balance - amount}),
                    etag=from_state.etag
                )
            ),
            TransactionOperationType(
                operation_type="upsert",
                request=StateItem(
                    key=f"account:{to_account}",
                    value=json.dumps({"balance": to_balance + amount}),
                    etag=to_state.etag
                )
            )
        ]

        # Execute transaction atomically
        dapr.execute_transaction(store_name="statestore", operations=operations)

        print(f"Transferred {amount} from {from_account} to {to_account}")

# Usage
transfer_money("123", "456", 100)
```

---

## Complete Example: Shopping Cart

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from dapr.clients import DaprClient
import json

app = FastAPI(title="Shopping Cart Service")

class CartItem(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int

class Cart(BaseModel):
    items: List[CartItem]

@app.get("/cart/{user_id}")
def get_cart(user_id: str):
    with DaprClient() as dapr:
        state = dapr.get_state(store_name="statestore", key=f"cart:{user_id}")

        if not state.data:
            return Cart(items=[])

        return Cart(items=json.loads(state.json()))

@app.post("/cart/{user_id}/add")
def add_to_cart(user_id: str, item: CartItem):
    with DaprClient() as dapr:
        # Get existing cart
        state = dapr.get_state(store_name="statestore", key=f"cart:{user_id}")
        cart = json.loads(state.json()) if state.data else []

        # Check if item already exists
        for cart_item in cart:
            if cart_item["product_id"] == item.product_id:
                cart_item["quantity"] += item.quantity
                break
        else:
            cart.append(item.model_dump())

        # Save with 24 hour TTL
        from dapr.clients.grpc._state import StateOptions
        options = StateOptions(metadata={"ttlInSeconds": "86400"})

        dapr.save_state(
            store_name="statestore",
            key=f"cart:{user_id}",
            value=json.dumps(cart),
            state_options=options
        )

        return {"message": "Item added", "cart": cart}

@app.delete("/cart/{user_id}")
def clear_cart(user_id: str):
    with DaprClient() as dapr:
        dapr.delete_state(store_name="statestore", key=f"cart:{user_id}")
        return {"message": "Cart cleared"}

@app.post("/cart/{user_id}/checkout")
def checkout(user_id: str):
    with DaprClient() as dapr:
        # Get cart
        state = dapr.get_state(store_name="statestore", key=f"cart:{user_id}")

        if not state.data:
            raise HTTPException(status_code=404, detail="Cart is empty")

        cart = json.loads(state.json())
        total = sum(item["price"] * item["quantity"] for item in cart)

        # Create order using transaction
        from dapr.clients.grpc._state import TransactionOperationType, StateItem

        operations = [
            TransactionOperationType(
                operation_type="upsert",
                request=StateItem(
                    key=f"order:{user_id}:{hash(json.dumps(cart))}",
                    value=json.dumps({
                        "user_id": user_id,
                        "items": cart,
                        "total": total,
                        "status": "pending"
                    })
                )
            ),
            TransactionOperationType(
                operation_type="delete",
                request=StateItem(key=f"cart:{user_id}")
            )
        ]

        dapr.execute_transaction(store_name="statestore", operations=operations)

        return {"message": "Order placed", "order_id": f"order:{user_id}", "total": total}
```

---

## Configuration

### Redis State Store

```yaml
# .dapr/components/redis-state.yaml
apiVersion: dapr.io/v1
kind: Component
metadata:
  name: statestore
  namespace: default
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: localhost:6379
  - name: redisPassword
    value: ""
  - name: enableTLS
    value: "false"
  - name: keyPrefix
    value: none  # Options: none, appid, name
  - name: failover
    value: "false"
  - name: maxRetries
    value: "3"
  - name: maxRetryBackoff
    value: "2000ms"
```

### PostgreSQL State Store

```yaml
# .dapr/components/postgres-state.yaml
apiVersion: dapr.io/v1
kind: Component
metadata:
  name: statestore
  namespace: default
spec:
  type: state.postgresql
  version: v1
  metadata:
  - name: connectionString
    secretKeyRef:
      name: postgres-connection
      key: connection-string
  - name: tablePrefix
    value: dapr_
  - name: cleanupIntervalInSeconds
    value: "3600"
  - name: maxIdleConns
    value: "10"
  - name: maxOpenConns
    value: "100"
```

### Azure Cosmos DB State Store

```yaml
# .dapr/components/cosmos-state.yaml
apiVersion: dapr.io/v1
kind: Component
metadata:
  name: statestore
  namespace: default
spec:
  type: state.azure.cosmosdb
  version: v1
  metadata:
  - name: url
    secretKeyRef:
      name: cosmos-db-url
      key: url
  - name: masterKey
    secretKeyRef:
      name: cosmos-db-master-key
      key: masterKey
  - name: database
    value: "dapr-state"
  - name: collection
    value: "state"
```

---

## Exercises

### Exercise 1: Todo List with State
1. Create a Todo service using Dapr state
2. Implement endpoints:
   - Create todo
   - List todos
   - Update todo
   - Delete todo
   - Mark todo as complete
3. Use ETags for safe updates

### Exercise 2: Leaderboard
1. Create a game leaderboard service
2. Store player scores with TTL of 24 hours
3. Implement:
   - Add score
   - Get top 10 players
   - Get player rank
4. Use transactions for score updates

### Exercise 3: Switch State Stores
1. Build a service using Redis state store
2. Change the component to use PostgreSQL
3. Verify no code changes are needed

---

## Summary

In this module, you learned:

- Dapr state management architecture
- Basic CRUD operations
- ETags for optimistic concurrency
- TTL for expiring state
- Transactions for atomic operations
- Multiple state store options

### Next Steps

Continue to [Module 4: Pub/Sub](../04-pubsub/README.md) to learn about event-driven architecture.
