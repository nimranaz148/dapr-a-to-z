# Module 6: Virtual Actors 🎭
> State, behavior, and location transparency for massively parallel applications

```text
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║                     MODULE 6: DAPR VIRTUAL ACTORS                         ║
║                                                                           ║
║  Key Concepts:                                                            ║
║  - Encapsulating State & Behavior                                         ║
║  - Single-threaded concurrency model                                      ║
║  - Automatic distribution and placement                                    ║
║  - Turn-based access                                                      ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

## Actor Model Diagram

```text
               ┌─────────────────────────────────┐
               │         Dapr Placement          │
               │            Service              │
               └───────────────┬─────────────────┘
                               │ (Where is Actor 1?)
      ┌────────────────────────▼────────────────────────┐
      │                  Dapr Sidecar                   │
      └──────┬─────────────────┬─────────────────┬──────┘
             │                 │                 │
      ┌──────▼──────┐   ┌──────▼──────┐   ┌──────▼──────┐
      │  Actor ID 1 │   │  Actor ID 2 │   │  Actor ID 3 │
      │  [State]    │   │  [State]    │   │  [State]    │
      │  [Methods]  │   │  [Methods]  │   │  [Methods]  │
      └─────────────┘   └─────────────┘   └─────────────┘
             Python Actor Service (Process A)
```

## 1. Defining an Actor Interface
Actors communicate through strictly defined interfaces.

```python
from dapr.actors import ActorInterface, actormethod

class ISmartDevice(ActorInterface):
    @actormethod(name='SetStatus')
    async def set_status(self, status: dict) -> None:
        ...

    @actormethod(name='GetStatus')
    async def get_status(self) -> dict:
        ...
```

## 2. Implementing the Actor
Dapr handles the lifecycle (activation/deactivation) and state persistence.

```python
from dapr.actors import Actor
from .interface import ISmartDevice

class SmartDevice(Actor, ISmartDevice):
    def __init__(self, ctx, actor_id):
        super(SmartDevice, self).__init__(ctx, actor_id)

    async def set_status(self, status: dict) -> None:
        # Save state automatically
        await self._state_manager.set_state('status', status)
        await self._state_manager.save_state()

    async def get_status(self) -> dict:
        return await self._state_manager.get_state('status')
```

## 3. Invoking an Actor
Clients can call actors from anywhere in the cluster by ID.

```python
from dapr.actors.client import ActorProxy
from .interface import ISmartDevice

async def main():
    # Create proxy for actor with ID 'thermostat-01'
    proxy = ActorProxy.create('SmartDevice', ActorId('thermostat-01'), ISmartDevice)

    # Call method
    await proxy.SetStatus({'temp': 22})
    status = await proxy.GetStatus()
    print(f'Status: {status}')
```

## Important Features
1. **Timers**: Actors can schedule periodic work.
2. **Reminders**: Durable schedules that persist even if the actor is deactivated or the process restarts.
3. **Automatic Garbage Collection**: Idle actors are removed from memory to save resources.
