import asyncio
from dapr.actors import ActorId
from dapr.actors.client import ActorProxy
# Note: This assumes the SmartDevice interface from Module 6
# from .interface import ISmartDevice

async def main():
    # Demonstrating how to use a proxy to call an actor
    # In a real app, 'ISmartDevice' would be imported
    # proxy = ActorProxy.create('SmartDevice', ActorId('1'), ISmartDevice)
    # await proxy.SetStatus({'power': 'on'})
    print("Actor invocation example ready. See interface.py in Module 6.")

if __name__ == "__main__":
    asyncio.run(main())
