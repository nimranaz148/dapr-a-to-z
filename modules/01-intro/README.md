# Module 1: Introduction to Dapr with Python 🐍

> Getting started with Dapr - Understanding the basics and setting up your development environment

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║                     MODULE 1: INTRODUCTION TO DAPR                        ║
║                                                                           ║
║  Goals:                                                                   ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ║
║  • Understand what Dapr is and why it matters                            ║
║  • Learn the sidecar architecture pattern                                 ║
║  • Set up Dapr with Python and uv                                         ║
║  • Run your first Dapr application                                       ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

## Table of Contents

1. [What is Dapr?](#what-is-dapr)
2. [Dapr Architecture](#dapr-architecture)
3. [Installation](#installation)
4. [Your First Dapr Application](#your-first-dapr-application)
5. [Key Concepts](#key-concepts)
6. [Exercises](#exercises)

---

## What is Dapr?

**Dapr (Distributed Application Runtime)** is a portable, event-driven runtime that makes it easy for developers to build resilient microservices. It provides common distributed application capabilities as building blocks, accessed via a simple HTTP or gRPC API.

### Key Characteristics

```
┌──────────────────────────────────────────────────────────────────────────┐
│                          Dapr Core Characteristics                       │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐    │
│  │  LANGUAGE AGNOSTIC                                                 │    │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐                   │    │
│  │  │Python│ │ Java │ │ Go   │ │NodeJS│ │ C#   │                   │    │
│  │  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘                   │    │
│  │        All use the same Dapr APIs via HTTP/gRPC                    │    │
│  └──────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐    │
│  │  PLATFORM AGNOSTIC                                                 │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │    │
│  │  │  Kubernetes  │  │   Docker     │  │     VM       │           │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘           │    │
│  │  ┌──────────────┐  ┌──────────────┐                             │    │
│  │  │   Edge IoT   │  │   Bare Metal │                             │    │
│  │  └──────────────┘  └──────────────┘                             │    │
│  └──────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐    │
│  │  CLOUD AGNOSTIC                                                     │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │    │
│  │  │    Azure     │  │     AWS      │  │     GCP      │           │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘           │    │
│  │  ┌──────────────┐  ┌──────────────┐                             │    │
│  │  │  Alibaba     │  │   On-Prem    │                             │    │
│  │  └──────────────┘  └──────────────┘                             │    │
│  └──────────────────────────────────────────────────────────────────┘    │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

### The Problem Dapr Solves

Without Dapr, building microservices requires dealing with:

```
┌──────────────────────────────────────────────────────────────────────────┐
│                     Without Dapr - The Challenge                         │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Service A ──┐                                                          │
│              │  ┌─────────────────────────────────────────┐            │
│  Service B ──┼──► Implement Service Discovery Yourself?     │            │
│              │  └─────────────────────────────────────────┘            │
│  Service C ──┤                                                          │
│              │  ┌─────────────────────────────────────────┐            │
│  Service D ──┼──► Implement Retry/Timeout/Circuit Breaker? │            │
│              │  └─────────────────────────────────────────┘            │
│  Service E ──┤                                                          │
│              │  ┌─────────────────────────────────────────┐            │
│  Service F ──┼──► Implement State Store?                   │            │
│              │  └─────────────────────────────────────────┘            │
│              │                                                          │
│              │  ┌─────────────────────────────────────────┐            │
│              └──► Implement Pub/Sub?                      │            │
│                 └─────────────────────────────────────────┘            │
│                                                                          │
│  Result: Repeated boilerplate code, vendor lock-in, high complexity      │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

With Dapr:

```
┌──────────────────────────────────────────────────────────────────────────┐
│                      With Dapr - The Solution                           │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────┐      ┌─────────┐      ┌─────────┐      ┌─────────┐        │
│  │Service A│      │Service B│      │Service C│      │Service D│        │
│  └────┬────┘      └────┬────┘      └────┬────┘      └────┬────┘        │
│       │                │                │                │              │
│       └────────────────┼────────────────┼────────────────┘              │
│                        │                │                               │
│                    ┌───┴────────────────┴───┐                            │
│                    │     Dapr Sidecars      │                            │
│                    │   (All Capabilities)   │                            │
│                    └─────────┬──────────────┘                            │
│                              │                                           │
│                    ┌─────────▼──────────────┐                            │
│                    │   Shared Infrastructure│                            │
│                    │   (Redis, Kafka, etc.) │                            │
│                    └────────────────────────┘                            │
│                                                                          │
│  Result: Focus on business logic, no vendor lock-in, simpler code        │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Dapr Architecture

### The Sidecar Pattern

```
┌──────────────────────────────────────────────────────────────────────────┐
│                      Dapr Sidecar Architecture                           │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   Application Container                        Sidecar Container         │
│   ┌─────────────────────────────────────┐      ┌─────────────────────┐  │
│   │                                     │      │                     │  │
│   │   ┌─────────────────────────────┐  │      │   ┌───────────────┐  │  │
│   │   │    Your Python Service      │  │      │   │   Dapr       │  │  │
│   │   │    (Business Logic)         │  │      │   │  Runtime      │  │  │
│   │   │                             │  │◄────►│   │  (Go)         │  │  │
│   │   │  @app.post("/process")      │  │      │   │               │  │  │
│   │   │  def process():             │  │      │   │  Building     │  │  │
│   │   │      # Business code here   │  │      │   │  Blocks:      │  │  │
│   │   │      pass                   │  │      │   │               │  │
│   │   └─────────────────────────────┘  │      │   │  • State      │  │  │
│   │                                     │      │   │  • Pub/Sub    │  │  │
│   │   ┌─────────────────────────────┐  │      │   │  • Bindings   │  │  │
│   │   │    Dapr Client (Python)     │  │      │   │  • Actors     │  │  │
│   │   │    ────────────────────     │  │      │   │  • Secrets    │  │  │
│   │   │    dapr.save_state(...)     │  │      │   │  • etc.       │  │  │
│   │   │    dapr.publish_event(...)  │  │      │   └───────────────┘  │  │
│   │   └─────────────────────────────┘  │      │                     │  │
│   │                                     │      │                     │  │
│   └─────────────────────────────────────┘      └─────────────────────┘  │
│           │                                          │                  │
│           │              HTTP/gRPC Port              │                  │
│           └──────────────────────────────────────────┘                  │
│                        (localhost:3500)                                 │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

### Communication Flow

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    Dapr Communication Flow                              │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. App → Dapr (Sidecar)                                                 │
│     ┌─────────────┐         ┌─────────────────┐                         │
│     │   Python    │ ──────► │   Dapr Sidecar  │                         │
│     │   App       │  HTTP   │  HTTP: 3500     │                         │
│     │   FastAPI   │         │  gRPC: 50001    │                         │
│     └─────────────┘         └────────┬────────┘                         │
│                                       │                                  │
│  2. Dapr → Infrastructure                                       │
│                                       │                                  │
│                                  ┌────▼─────┐ ┌─────────┐               │
│                                  │   Redis  │ │  Kafka  │               │
│                                  │   Store  │ │ Broker  │               │
│                                  └──────────┘ └─────────┘               │
│                                                                          │
│  3. Infrastructure → Dapr → App (for pubsub, bindings, etc.)            │
│                                       │                                  │
│                                  ┌────▼─────────────┐                   │
│                                  │   Dapr Sidecar   │                   │
│                                  │  (receives event)│                   │
│                                  └────────┬─────────┘                   │
│                                           │                              │
│                                  ┌────────▼─────────┐                   │
│                                  │   Python App     │                   │
│                                  │  (HTTP callback) │                   │
│                                  └──────────────────┘                   │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Installation

### Step 1: Install Dapr CLI

```bash
# Linux/Mac
curl -fsSL https://raw.githubusercontent.com/dapr/cli/master/install/install.sh | /bin/bash

# Windows (PowerShell)
powershell -Command "iex -OutFile install.ps1 (Invoke-WebRequest -Uri https://raw.githubusercontent.com/dapr/cli/master/install/install.ps1).Content"

# Verify installation
dapr --version
```

### Step 2: Initialize Dapr

```bash
# Initialize Dapr (downloads Docker images, sets up dev environment)
dapr init

# Verify Dapr is running
dapr --version
```

Output:
```
CLI version: 1.13.0
Runtime version: 1.13.0
```

### Step 3: Install uv (Package Manager)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify installation
uv --version
```

### Step 4: Install Dapr Python SDK

```bash
# Navigate to tutorial directory
cd dapr-python-tutorial

# Install dependencies using uv
uv sync

# Or add to existing project
uv add dapr
```

### Verify Installation

```bash
# Test Dapr installation
dapr --version

# Test Python SDK
python -c "import dapr.clients; print('Dapr SDK installed successfully!')"
```

---

## Your First Dapr Application

### Hello World Example

Create a file `hello_world.py`:

```python
from dapr.clients import DaprClient

def main():
    with DaprClient() as dapr:
        # Save state
        dapr.save_state(
            store_name="statestore",
            key="greeting",
            value="Hello from Dapr!"
        )

        # Retrieve state
        state = dapr.get_state(store_name="statestore", key="greeting")

        print(f"Retrieved state: {state.json()}")

        # Delete state
        dapr.delete_state(store_name="statestore", key="greeting")

        print("State deleted successfully!")

if __name__ == "__main__":
    main()
```

### Running with Dapr

```bash
# Start Dapr with Redis (default state store)
docker run -d -p 6379:6379 redis

# Run the app with Dapr sidecar
dapr run --app-id hello-world \
         --dapr-http-port 3500 \
         -- python hello_world.py
```

Output:
```
== APP == Retrieved state: Hello from Dapr!
== APP == State deleted successfully!
```

### Using FastAPI with Dapr

```python
from fastapi import FastAPI
from pydantic import BaseModel
from dapr.clients import DaprClient

app = FastAPI()

class Greeting(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"message": "Hello from Dapr + FastAPI!"}

@app.post("/save")
def save_greeting(greeting: Greeting):
    with DaprClient() as dapr:
        dapr.save_state(
            store_name="statestore",
            key="greeting",
            value=greeting.message
        )
    return {"status": "saved", "message": greeting.message}

@app.get("/greeting")
def get_greeting():
    with DaprClient() as dapr:
        state = dapr.get_state(store_name="statestore", key="greeting")
    return {"greeting": state.json()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Run it:

```bash
dapr run --app-id fastapi-app \
         --dapr-http-port 3500 \
         --app-protocol http \
         -- uvicorn hello_fastapi:app --host 0.0.0.0 --port 8000
```

---

## Key Concepts

### 1. Building Blocks

Dapr provides the following building blocks:

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        Dapr Building Blocks                              │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Service Invocation  │  State Management  │  Pub/Sub Messaging  │    │
│  │                     │                   │                     │    │
│  │  Call other         │  Store and        │  Publish and        │    │
│  │  services securely  │  retrieve state   │  subscribe to       │    │
│  │  with retry,        │  with            │  events             │    │
│  │  timeout, auth      │  consistency      │                     │    │
│  └────────────────────┴───────────────────┴─────────────────────┘    │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Input/Output Bindings  │  Distributed Tracing  │  Actors        │    │
│  │                          │                      │               │    │
│  │  Interface with          │  Observe service      │  Stateful     │    │
│  │  external systems        │  calls and            │  objects      │    │
│  │  (cron, HTTP, Kafka)     │  events               │               │    │
│  └──────────────────────────┴──────────────────────┴───────────────┘    │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Secrets Management  │  Configuration  │  Virtual Actors         │    │
│  │                      │                │                         │    │
│  │  Secure access to    │  External      │  Concurrent stateful    │    │
│  │  secrets             │  configuration │  objects                │    │
│  │  (Vault, AWS, Azure) │  stores        │                         │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

### 2. Components

Components are how Dapr connects to external infrastructure:

```yaml
# Example: Redis state store component
apiVersion: dapr.io/v1
kind: Component
metadata:
  name: statestore
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: localhost:6379
  - name: redisPassword
    value: ""
```

### 3. App ID

Every Dapr-enabled application has a unique `app-id`:

```bash
dapr run --app-id my-service python app.py
```

This ID is used for:
- Service discovery
- Actor identity
- Component association
- Tracing and metrics

---

## Dapr CLI Commands

```
╔══════════════════════════════════════════════════════════════════════════╗
║                      Common Dapr CLI Commands                           ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  dapr init                    Initialize Dapr (first time setup)        ║
║  dapr run --app-id NAME cmd  Run application with Dapr sidecar          ║
║  dapr stop --app-id NAME      Stop Dapr application                     ║
║  dapr list                    List running Dapr applications            ║
║  dapr status                  Show Dapr runtime status                  ║
║  dapr uninstall               Remove Dapr from system                   ║
║                                                                          ║
║  dapr dashboard               Launch Dapr dashboard UI                  ║
║  dapr mtls                   Manage mutual TLS settings                ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
```

---

## Complete Example: Counter Service

Create `counter.py`:

```python
from fastapi import FastAPI
from dapr.clients import DaprClient
from pydantic import BaseModel

app = FastAPI(title="Counter Service", version="1.0.0")

class CounterResponse(BaseModel):
    value: int
    message: str

@app.post("/increment")
def increment_counter(amount: int = 1):
    with DaprClient() as dapr:
        # Get current value
        state = dapr.get_state(store_name="statestore", key="counter")
        current_value = int(state.json()) if state.data else 0

        # Increment
        new_value = current_value + amount

        # Save new value
        dapr.save_state(
            store_name="statestore",
            key="counter",
            value=str(new_value)
        )

        return CounterResponse(
            value=new_value,
            message=f"Counter incremented by {amount}"
        )

@app.post("/reset")
def reset_counter():
    with DaprClient() as dapr:
        dapr.delete_state(store_name="statestore", key="counter")
        return CounterResponse(value=0, message="Counter reset")

@app.get("/counter")
def get_counter():
    with DaprClient() as dapr:
        state = dapr.get_state(store_name="statestore", key="counter")
        value = int(state.json()) if state.data else 0
        return CounterResponse(value=value, message=f"Current counter value")
```

Run it:

```bash
# First, start Redis
docker run -d -p 6379:6379 redis

# Run with Dapr
dapr run --app-id counter \
         --dapr-http-port 3500 \
         -- uvicorn counter:app --host 0.0.0.0 --port 8000
```

Test it:

```bash
# Increment counter
curl -X POST http://localhost:8000/increment
curl -X POST http://localhost:8000/increment?amount=5

# Get current value
curl http://localhost:8000/counter

# Reset counter
curl -X POST http://localhost:8000/reset
```

---

## Dapr Configuration

Create `.dapr/config.yaml`:

```yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: appconfig
spec:
  tracing:
    samplingRate: "1"
    zipkin:
      endpointAddress: "http://localhost:9411/api/v2/spans"
  metrics:
    enabled: true
  featureFlags:
    - name: MyFeature
      enabled: true
```

Use the configuration:

```bash
dapr run --app-id myapp \
         --config .dapr/config.yaml \
         -- python app.py
```

---

## Exercises

### Exercise 1: Hello Dapr
1. Create a Python script that saves your name to state
2. Retrieve and display the name
3. Delete the state and confirm deletion

### Exercise 2: Temperature Tracker
1. Create a service that stores temperature readings
2. Add endpoints to:
   - Save a temperature reading
   - Get the latest temperature
   - Get temperature history (use multiple keys)
3. Run it with Dapr and test all endpoints

### Exercise 3: Configuration
1. Create a Dapr configuration file that enables tracing
2. Run an app with this configuration
3. Use the Dapr dashboard to see traces

---

## Summary

In this module, you learned:

- What Dapr is and why it's useful
- How the sidecar architecture works
- How to install Dapr and the Python SDK
- How to run your first Dapr application
- Key Dapr concepts: building blocks, components, and app-id

### Next Steps

Continue to [Module 2: Service Invocation](../02-service-invocation/README.md) to learn how to call other services using Dapr.

---

## Additional Resources

- [Dapr Official Documentation](https://docs.dapr.io/)
- [Dapr Python SDK](https://github.com/dapr/python-sdk)
- [Dapr Concepts](https://docs.dapr.io/concepts/)
- [Dapr Samples](https://github.com/dapr/samples)
