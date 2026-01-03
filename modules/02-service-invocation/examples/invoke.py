import asyncio
from dapr.clients import DaprClient

async def invoke_service():
    async with DaprClient() as client:
        # Full parameter usage
        resp = await client.invoke_method(
            app_id='target-service',
            method_name='hello',
            data='{"message": "Hello from Caller"}',
            http_verb='POST',
            data_content_type='application/json',
            metadata={'x-custom-header': 'dapr-master'}
        )
        print(f"Service Response: {resp.data.decode('utf-8')}")

if __name__ == '__main__':
    asyncio.run(invoke_service())
