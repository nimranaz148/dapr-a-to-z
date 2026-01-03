from fastapi import FastAPI, Body
from dapr.clients import DaprClient
import uvicorn
import uuid

app = FastAPI(title="Dapr Master Application")

STATE_STORE = "statestore"
PUBSUB_NAME = "pubsub"
TOPIC_NAME = "orders"

@app.post("/order")
async def create_order(order_data: dict = Body(...)):
    order_id = str(uuid.uuid4())
    order_data['id'] = order_id

    with DaprClient() as client:
        # 1. State Management: Store order
        client.save_state(STATE_STORE, order_id, str(order_data))

        # 2. Pub/Sub: Publish order created event
        client.publish_event(
            pubsub_name=PUBSUB_NAME,
            topic_name=TOPIC_NAME,
            data=order_data,
            data_content_type='application/json'
        )

    return {"message": "Order created", "order_id": order_id}

@app.get("/order/{order_id}")
async def get_order(order_id: str):
    with DaprClient() as client:
        result = client.get_state(STATE_STORE, order_id)
        if not result.data:
            return {"error": "Order not found"}
        return {"order": result.data.decode('utf-8')}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
