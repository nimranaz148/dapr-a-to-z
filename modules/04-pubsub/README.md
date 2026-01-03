# Module 4: Pub/Sub Messaging 📨

> Learn event-driven architecture using Dapr's publish/subscribe pattern

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║                    MODULE 4: PUB/SUB MESSAGING                            ║
║                                                                           ║
║  Goals:                                                                   ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ║
║  • Understand pub/sub patterns and event-driven architecture             ║
║  • Learn to publish and subscribe to events                              ║
║  • Configure message brokers (Redis, Kafka, RabbitMQ)                    ║
║  • Handle dead-letter queues and retry policies                          ║
║  • Implement complex routing patterns                                    ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

## Table of Contents

1. [What is Pub/Sub?](#what-is-pubsub)
2. [Event-Driven Architecture](#event-driven-architecture)
3. [Supported Message Brokers](#supported-message-brokers)
4. [Publishing Events](#publishing-events)
5. [Subscribing to Events](#subscribing-to-events)
6. [Message Routing](#message-routing)
7. [Dead Letter Queues](#dead-letter-queues)
8. [Exercises](#exercises)

---

## What is Pub/Sub?

Publish/Subscribe (Pub/Sub) is a messaging pattern where senders (publishers) send messages to topics, and receivers (subscribers) receive messages from topics. Publishers and subscribers are decoupled.

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    Traditional vs Pub/Sub Communication                 │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  TRADITIONAL (Point-to-Point)                           PUB/SUB          │
│                                                                          │
│  ┌──────┐         ┌──────┐         ┌──────┐      ┌──────┐              │
│  │ App A│◄───────►│ App B│◄───────►│ App C│      │ App A│              │
│  └──────┘         └──────┘         └──────┘       └──┬───┘              │
│                                                        │               │
║  Tightly coupled                             ┌─────────▼─────────┐    ║
║  Hard to scale                            │   Message Broker  │    ║
║  Point-to-point calls                     │   (Topic)         │    ║
║                                            │                   │    ║
║                                            └───┬─────┬─────┬───┘    ║
║  Benefits of Pub/Sub:                     │     │     │         ║
║  • Decoupled services                     │     │     │         ║
║  • Scalable (add consumers easily)       ▼     ▼     ▼         ║
║  • Flexible routing                    ┌──────┐ ┌──────┐ ┌──────┐ ║
║  • Better resilience                  │App B │ │App C │ │App D │ ║
║                                         └──────┘ └──────┘ └──────┘ ║
║                                            Subscribers                ║
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Event-Driven Architecture

```
╔══════════════════════════════════════════════════════════════════════════╗
║                    Event-Driven Architecture Flow                        ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  ┌─────────────────────────────────────────────────────────────────┐    ║
║  │                         Publishers                             │    ║
║  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │    ║
║  │  │   Order     │  │   Payment   │  │    User     │           │    ║
║  │  │  Service    │  │  Service    │  │   Service   │           │    ║
║  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘           │    ║
║  │         │                 │                 │                  │    ║
║  │         │ Event           │ Event           │ Event            │    ║
║  │         │                 │                 │                  │    ║
║  └─────────┼─────────────────┼─────────────────┼──────────────────┘    ║
║            │                 │                 │                      ║
║            └─────────────────┼─────────────────┘                      ║
║                              │                                        ║
║                    ┌─────────▼────────────────┐                        ║
║                    │    Dapr Message Broker   │                        ║
║                    │                          │                        ║
║                    │  Topic: order.created    │                        ║
║                    │  Topic: payment.done     │                        ║
║                    │  Topic: user.registered  │                        ║
║                    └──────────┬───────────────┘                        ║
║                               │                                        ║
║          ┌────────────────────┼────────────────────┐                  ║
║          ▼                    ▼                    ▼                  ║
║   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐              ║
║   │   Email     │    │  Inventory  │    │ Analytics   │              ║
║   │  Service    │    │  Service    │    │  Service    │              ║
║   └─────────────┘    └─────────────┘    └─────────────┘              ║
║      Subscribers          Subscribers          Subscribers            ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
```

---

## Supported Message Brokers

```
╔══════════════════════════════════════════════════════════════════════════╗
║                    Supported Message Brokers                              ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  ┌─────────────────────────────────────────────────────────────────┐    ║
║  │  OPEN SOURCE                                                     │    ║
║  │  • Redis Streams (Lightweight, built-in pub/sub)                 │    ║
║  │  • Apache Kafka (High throughput, distributed)                   │    ║
║  │  • RabbitMQ (Flexible, AMQP protocol)                            │    ║
║  │  • NATS (Fast, lightweight)                                      │    ║
║  │  • MQTT (IoT focused, lightweight protocol)                      │    ║
║  └─────────────────────────────────────────────────────────────────┘    ║
║                                                                          ║
║  ┌─────────────────────────────────────────────────────────────────┐    ║
║  │  CLOUD NATIVE                                                    │    ║
║  │  • AWS SNS/SQS                                                   │    ║
║  │  • Azure Service Bus                                             │    ║
║  │  • Azure Event Grid                                              │    ║
║  │  • Google Cloud Pub/Sub                                          │    ║
║  └─────────────────────────────────────────────────────────────────┘    ║
║                                                                          ║
║  ┌─────────────────────────────────────────────────────────────────┐    ║
║  │  SPECIALIZED                                                     │    ║
║  │  • Apache Pulsar (Multi-tenancy, geo-replication)               │    ║
║  │  • JetStream (NATS persistence layer)                            │    ║
║  │  • Solace (Enterprise messaging)                                 │    ║
║  └─────────────────────────────────────────────────────────────────┘    ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
```

---

## Configuration

### Redis Pub/Sub Component

```yaml
# .dapr/components/redis-pubsub.yaml
apiVersion: dapr.io/v1
kind: Component
metadata:
  name: pubsub
  namespace: default
spec:
  type: pubsub.redis
  version: v1
  metadata:
  - name: redisHost
    value: localhost:6379
  - name: redisPassword
    value: ""
  - name: enableTLS
    value: "false"
  # Consumer settings
  - name: consumerID
    value: "myConsumer"
  # Redelivery settings
  - name: maxLenApprox
    value: "1000000"
scopes:
- order-service
- notification-service
```

### Kafka Pub/Sub Component

```yaml
# .dapr/components/kafka-pubsub.yaml
apiVersion: dapr.io/v1
kind: Component
metadata:
  name: pubsub
  namespace: default
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "localhost:9092"
  - name: consumerGroup
    value: "group1"
  - name: authRequired
    value: "false"
  - name: saslUsername
    value: ""
  - name: saslPassword
    value: ""
  - name: allowAutoTopicCreation
    value: "true"
  - name: maxMessageBytes
    value: "1024"
```

### RabbitMQ Pub/Sub Component

```yaml
# .dapr/components/rabbitmq-pubsub.yaml
apiVersion: dapr.io/v1
kind: Component
metadata:
  name: pubsub
  namespace: default
spec:
  type: pubsub.rabbitmq
  version: v1
  metadata:
  - name: host
    value: "amqp://guest:guest@localhost:5672"
  - name: durable
    value: "true"
  - name: deletedWhenUnused
    value: "false"
  - name: autoAck
    value: "false"
  - name: reconnectWait
    value: "0"
  - name: deliveryMode
    value: "0"
```

---

## Publishing Events

### Simple Publish

```python
from dapr.clients import DaprClient
import json

def publish_order_created(order: dict):
    with DaprClient() as dapr:
        dapr.publish_event(
            pubsub_name="pubsub",
            topic_name="order.created",
            data=json.dumps(order),
            data_content_type="application/json"
        )
        print(f"Published order: {order}")

# Usage
order = {
    "order_id": "ORD-001",
    "customer_id": "CUST-123",
    "items": ["product-1", "product-2"],
    "total": 99.99
}
publish_order_created(order)
```

### Publishing with Metadata

```python
from dapr.clients import DaprClient
import json

def publish_with_metadata(topic: str, data: dict, metadata: dict = None):
    with DaprClient() as dapr:
        dapr.publish_event(
            pubsub_name="pubsub",
            topic_name=topic,
            data=json.dumps(data),
            metadata=metadata or {
                "partitionKey": "user-123",  # For Kafka partitioning
                "messageId": "msg-001",
                "correlationId": "req-456"
            }
        )
```

### Bulk Publish (Kafka)

```python
from dapr.clients import DaprClient
import json

def bulk_publish(topic: str, messages: list):
    with DaprClient() as dapr:
        entries = []
        for i, msg in enumerate(messages):
            entry = dapr.BulkPublishMessageEntry(
                entry_id=str(i),
                event=json.dumps(msg),
                content_type="application/json"
            )
            entries.append(entry)

        response = dapr.bulk_publish_event(
            pubsub_name="pubsub",
            topic_name=topic,
            messages=entries
        )

        print(f"Published: {response.published_entries_count}")
        if response.failed_entries:
            print(f"Failed: {len(response.failed_entries)}")
```

---

## Subscribing to Events

### Subscription via Declarative Component

```yaml
# .dapr/components/order-subscription.yaml
apiVersion: dapr.io/v1
kind: Subscription
metadata:
  name: order-created-subscription
  namespace: default
spec:
  topic: order.created
  route: /orders/create
  pubsubname: pubsub
  scopes:
  - notification-service
  - inventory-service
```

### Subscription via Code (Programmatic)

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dapr.ext.fastapi import DaprApp
import json

app = FastAPI()
dapr_app = DaprApp(app)

# Method 1: Using DaprApp decorator
@dapr_app.subscribe(pubsub="pubsub", topic="order.created")
def order_created_handler(event_data: dict):
    order = event_data["data"]
    print(f"Received order: {order}")
    # Process order...
    return {"status": "success"}

# Method 2: Manual subscription endpoint
@app.post("/orders/create")
async def handle_order_event(request: Request):
    event = await request.json()
    print(f"Raw event: {event}")

    # CloudEvents format
    data = event.get("data", {})
    order = json.loads(data) if isinstance(data, str) else data

    print(f"Processing order: {order}")

    # Your business logic here

    return JSONResponse(
        status_code=200,
        content={"status": "processed", "order_id": order.get("order_id")}
    )

# Method 3: Multiple subscriptions
@app.post("/orders/updated")
async def handle_order_updated(request: Request):
    event = await request.json()
    order = json.loads(event["data"])
    print(f"Order updated: {order['order_id']}")
    return {"status": "processed"}

@app.post("/orders/deleted")
async def handle_order_deleted(request: Request):
    event = await request.json()
    order_id = json.loads(event["data"]).get("order_id")
    print(f"Order deleted: {order_id}")
    return {"status": "processed"}
```

### Complete Subscriber Example

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from dapr.ext.fastapi import DaprApp
from dapr.clients import DaprClient
import json
import logging

app = FastAPI(title="Order Processing Service")
dapr_app = DaprApp(app)
logger = logging.getLogger(__name__)

class OrderProcessor:
    def __init__(self):
        self.dapr = DaprClient()

    def process_order(self, order: dict) -> dict:
        """Process an incoming order"""
        logger.info(f"Processing order: {order['order_id']}")

        # Validate order
        if not order.get("items"):
            raise ValueError("Order has no items")

        # Calculate total
        total = sum(item.get("price", 0) * item.get("quantity", 0)
                    for item in order["items"])

        # Update order with calculated total
        order["total"] = total
        order["status"] = "processed"

        # Save to state
        self.dapr.save_state(
            store_name="statestore",
            key=f"order:{order['order_id']}",
            value=json.dumps(order)
        )

        # Publish order processed event
        self.dapr.publish_event(
            pubsub_name="pubsub",
            topic_name="order.processed",
            data=json.dumps(order)
        )

        return order

processor = OrderProcessor()

@dapr_app.subscribe(pubsub="pubsub", topic="order.created")
async def order_created_subscription(request: Request):
    """Handle order.created events"""
    try:
        event = await request.json()
        data = event.get("data", {})

        # Parse data (might be string or dict)
        order = json.loads(data) if isinstance(data, str) else data

        # Process the order
        result = processor.process_order(order)

        logger.info(f"Order {order['order_id']} processed successfully")

        return JSONResponse(
            status_code=200,
            content={"status": "success", "order": result}
        )

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": str(e)}
        )
    except Exception as e:
        logger.error(f"Processing error: {e}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": "Internal error"}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## Message Routing

### Content-Based Routing

Route messages based on their content using Dapr's routing feature:

```yaml
# .dapr/components/pubsub.yaml
apiVersion: dapr.io/v1
kind: Component
metadata:
  name: pubsub
  namespace: default
spec:
  type: pubsub.redis
  version: v1
  metadata:
  - name: redisHost
    value: localhost:6379
```

```yaml
# .dapr/components/order-routes.yaml
apiVersion: dapr.io/v1
kind: Subscription
metadata:
  name: order-routing-subscription
  namespace: default
spec:
  topic: orders
  route: orders
  pubsubname: pubsub
  rules:
  - match: 'event.type == "order.created"'
    path: /orders/created
  - match: 'event.type == "order.updated"'
    path: /orders/updated
  - match: 'event.type == "order.canceled"'
    path: /orders/canceled
```

### Handler for Routed Messages

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import json

app = FastAPI()

@app.post("/orders/created")
async def handle_order_created(request: Request):
    event = await request.json()
    data = json.loads(event["data"])
    print(f"Order created: {data['order_id']}")
    return {"status": "created"}

@app.post("/orders/updated")
async def handle_order_updated(request: Request):
    event = await request.json()
    data = json.loads(event["data"])
    print(f"Order updated: {data['order_id']}")
    return {"status": "updated"}

@app.post("/orders/canceled")
async def handle_order_canceled(request: Request):
    event = await request.json()
    data = json.loads(event["data"])
    print(f"Order canceled: {data['order_id']}")
    return {"status": "canceled"}
```

### Multi-Topic Subscriber

```python
from dapr.ext.fastapi import DaprApp
from fastapi import FastAPI
import json

app = FastAPI()
dapr_app = DaprApp(app)

@dapr_app.subscribe(pubsub="pubsub", topic="users.created")
def user_created(event_data: dict):
    user = json.loads(event_data["data"])
    print(f"New user: {user['email']}")
    # Send welcome email...

@dapr_app.subscribe(pubsub="pubsub", topic="users.deleted")
def user_deleted(event_data: dict):
    user = json.loads(event_data["data"])
    print(f"User deleted: {user['email']}")
    # Clean up user data...

@dapr_app.subscribe(pubsub="pubsub", topic="payments.completed")
def payment_completed(event_data: dict):
    payment = json.loads(event_data["data"])
    print(f"Payment completed: ${payment['amount']}")
    # Update order status...
```

---

## Dead Letter Queues

Dead Letter Queues (DLQ) store messages that couldn't be processed after multiple retries.

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    Dead Letter Queue Flow                                │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Publisher                                                       │    │
│  │         ┌─────────────────────────────────────────────┐         │    │
│  │         │  Event                                      │         │    │
│  │         └──────────────────┬──────────────────────────┘         │    │
│  └────────────────────────────┼────────────────────────────────────┘    │
│                               ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Message Broker                                                  │    │
│  │  ┌─────────────────────────────────────────────────────────┐   │    │
│  │  │  Topic: orders                                           │   │    │
│  │  │                                                           │   │    │
│  │  │  ┌───────────────────────────────────────────────────┐  │   │    │
│  │  │  │  Consumer Group: order-processor                  │  │   │    │
│  │  │  │                                                   │  │   │    │
│  │  │  │  ┌─────────┐    ┌─────────┐    ┌─────────┐      │  │   │    │
│  │  │  │  │ Message │ ─► │ Message │ ─► │ Message │ ──?  │  │   │    │
│  │  │  │  │   1     │    │   2     │    │   3     │      │  │   │    │
│  │  │  │  │ Success │    │ Success │    │ Failed  │      │  │   │    │
│  │  │  │  └─────────┘    └─────────┘    └────┬────┘      │  │   │    │
│  │  │  │                                      │           │  │   │    │
│  │  │  │    Retry 1 ─────────────────────────┘           │  │   │    │
│  │  │  │         │                                       │  │   │    │
│  │  │  │         ▼                                       │  │   │    │
│  │  │  │    Retry 2 ──────────────────────────X           │  │   │    │
│  │  │  │                                          │       │  │   │    │
│  │  │  │                                          ▼       │  │   │    │
│  │  │  │                              ┌───────────────┐  │  │   │    │
│  │  │  │                              │ Dead Letter   │  │  │   │    │
║  │  │  └──────────────────────────────►   Queue       │◄─┘  │   │    ║
║  │  │                                └───────────────┘      │   │    ║
║  │  └───────────────────────────────────────────────────┘   │    ║
│  │                                                           │    │
│  │  ┌─────────────────────────────────────────────────────┐  │    │
│  │  │  Topic: orders-dlq                                  │  │    │
│  │  │  (Failed messages for manual inspection/retry)      │  │    │
│  │  └─────────────────────────────────────────────────────┘  │    │
│  └───────────────────────────────────────────────────────────┘    │
│                                 │                                     │
│                                 ▼                                     │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │  DLQ Consumer (Manual inspection and reprocessing)               │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

### DLQ Configuration

```yaml
# .dapr/components/pubsub-with-dlq.yaml
apiVersion: dapr.io/v1
kind: Component
metadata:
  name: pubsub
  namespace: default
spec:
  type: pubsub.redis
  version: v1
  metadata:
  - name: redisHost
    value: localhost:6379
  # DLQ Settings
  - name: consumerID
    value: "order-processor"
  - name: maxDeliveryAttempts
    value: "3"
  - name: processingTimeout
    value: "60s"
  - name: autoAck
    value: "false"
scopes:
- order-processor
```

### DLQ Handler

```python
from fastapi import FastAPI, Request
from dapr.ext.fastapi import DaprApp
import json
import logging

app = FastAPI()
dapr_app = DaprApp(app)
logger = logging.getLogger(__name__)

# Handler with error simulation for DLQ demo
@dapr_app.subscribe(pubsub="pubsub", topic="orders")
async def process_order(request: Request):
    try:
        event = await request.json()
        data = json.loads(event["data"])

        # Simulate processing failure for certain orders
        if data.get("order_id", "").endswith("FAIL"):
            raise ValueError("Simulated processing failure")

        logger.info(f"Processed order: {data['order_id']}")
        return {"status": "success"}

    except Exception as e:
        logger.error(f"Failed to process order: {e}")
        # This will cause message to go to DLQ after retries
        raise

# DLQ Consumer - processes failed messages
@app.post("/dlq/orders")
async def process_dlq_message(request: Request):
    """Endpoint to manually process messages from DLQ"""
    event = await request.json()
    data = json.loads(event["data"])

    logger.warning(f"Processing DLQ message: {data}")

    # Manual inspection and handling
    # Could fix issues and republish, or log for investigation

    return {"status": "dlq_handled"}

# Manual DLQ reader
@app.get("/dlq/orders")
async def list_dlq_messages():
    """List messages in DLQ for inspection"""
    from dapr.clients import DaprClient

    with DaprClient() as dapr:
        # Read from DLQ topic
        try:
            # This is pseudo-code - actual implementation depends on broker
            messages = dapr.get_state(
                store_name="statestore",
                key="dlq:orders"
            )
            return {"messages": messages.json()}
        except:
            return {"messages": []}
```

---

## Complete Example: E-commerce Event Flow

```
╔══════════════════════════════════════════════════════════════════════════╗
║                    E-commerce Event Flow                                 ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  ┌─────────────────────────────────────────────────────────────────┐    ║
║  │  User Places Order                                              │    ║
║  └──────────────────────────┬──────────────────────────────────────┘    ║
║                             │                                           ║
║                             ▼                                           ║
║  ┌─────────────────────────────────────────────────────────────────┐    ║
║  │  Order Service                                                  │    ║
║  │  ┌─────────────────────────────────────────────────────────┐    │    ║
║  │  │  1. Create order record                                  │    │    ║
║  │  │  2. Publish order.created event                          │    │    ║
║  │  └─────────────────────────────────────────────────────────┘    │    ║
║  └──────────────────────────┬──────────────────────────────────────┘    ║
║                             │                                           ║
║                             ▼                                           ║
║  ┌─────────────────────────────────────────────────────────────────┐    ║
║  │  Message Broker (Topic: order.created)                          │    ║
║  └──────────┬────────────────────────────┬──────────────────────────┘    ║
║             │                            │                               ║
║    ┌────────▼─────────┐         ┌────────▼─────────┐                   ║
║    │ Inventory Svc    │         │ Payment Svc      │                   ║
║    │ ┌──────────────┐ │         │ ┌──────────────┐ │                   ║
║    │ │ Reserve      │ │         │ │ Process      │ │                   ║
║    │ │ Inventory    │ │         │ │ Payment      │ │                   ║
║    │ └──────┬───────┘ │         │ └──────┬───────┘ │                   ║
║    │        │          │         │        │          │                   ║
║    │        ▼          │         │        ▼          │                   ║
║    │   Publish        │         │   Publish         │                   ║
║    │   inventory.     │         │   payment.        │                   ║
║    │   reserved       │         │   completed       │                   ║
║    └──────────────────┘         └───────────────────┘                   ║
║             │                            │                               ║
║             └────────┬───────────────────┘                               ║
║                      ▼                                                 ║
║  ┌─────────────────────────────────────────────────────────────────┐    ║
║  │  Message Broker (Topics: inventory.reserved, payment.completed)   │    ║
║  └──────────────────────────┬──────────────────────────────────────┘    ║
║                             │                                           ║
║                    ┌────────▼────────┐                                  ║
║                    │ Order Svc       │                                  ║
║                    │ ┌──────────────┐ │                                  ║
║                    │ │ Confirm      │ │                                  ║
║                    │ │ Order        │ │                                  ║
║                    │ └──────┬───────┘ │                                  ║
║                    │        │          │                                  ║
║                    │        ▼          │                                  ║
║                    │   Publish         │                                  ║
║                    │   order.          │                                  ║
║                    │   confirmed       │                                  ║
║                    └────────┬──────────┘                                  ║
║                             │                                            ║
║                    ┌────────▼────────┐                                  ║
║                    │ Email Svc       │                                  ║
║                    │ ┌──────────────┐ │                                  ║
║                    │ │ Send         │ │                                  ║
║                    │ │ Confirmation  │ │                                  ║
║                    │ │ Email        │ │                                  ║
║                    │ └──────────────┘ │                                  ║
║                    └──────────────────┘                                  ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
```

### Complete Order Flow Implementation

**Order Service (Publisher)**

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from dapr.clients import DaprClient
import json
import uuid

app = FastAPI(title="Order Service")

class OrderItem(BaseModel):
    product_id: str
    quantity: int
    price: float

class CreateOrderRequest(BaseModel):
    customer_id: str
    items: List[OrderItem]

class Order(BaseModel):
    order_id: str
    customer_id: str
    items: List[OrderItem]
    total: float
    status: str = "pending"

@app.post("/orders")
def create_order(request: CreateOrderRequest):
    order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
    total = sum(item.price * item.quantity for item in request.items)

    order = Order(
        order_id=order_id,
        customer_id=request.customer_id,
        items=request.items,
        total=total,
        status="pending"
    )

    # Save to state
    with DaprClient() as dapr:
        dapr.save_state(
            store_name="statestore",
            key=f"order:{order_id}",
            value=json.dumps(order.model_dump())
        )

        # Publish order.created event
        dapr.publish_event(
            pubsub_name="pubsub",
            topic_name="order.created",
            data=json.dumps(order.model_dump()),
            metadata={"messageId": order_id}
        )

    return order

@app.get("/orders/{order_id}")
def get_order(order_id: str):
    with DaprClient() as dapr:
        state = dapr.get_state(store_name="statestore", key=f"order:{order_id}")

        if not state.data:
            raise HTTPException(status_code=404, detail="Order not found")

        return json.loads(state.json())
```

**Inventory Service (Subscriber)**

```python
from fastapi import FastAPI, Request
from dapr.ext.fastapi import DaprApp
from dapr.clients import DaprClient
import json

app = FastAPI(title="Inventory Service")
dapr_app = DaprApp(app)

@dapr_app.subscribe(pubsub="pubsub", topic="order.created")
async def handle_order_created(request: Request):
    event = await request.json()
    order = json.loads(event["data"])

    print(f"Reserving inventory for order: {order['order_id']}")

    with DaprClient() as dapr:
        # Process each item
        for item in order["items"]:
            # Get current inventory
            key = f"inventory:{item['product_id']}"
            state = dapr.get_state(store_name="statestore", key=key)
            current_stock = int(state.json()) if state.data else 100

            # Reserve stock
            if current_stock >= item["quantity"]:
                new_stock = current_stock - item["quantity"]
                dapr.save_state(store_name="statestore", key=key, value=str(new_stock))
            else:
                # Publish inventory.failed event
                dapr.publish_event(
                    pubsub_name="pubsub",
                    topic_name="inventory.failed",
                    data=json.dumps({
                        "order_id": order["order_id"],
                        "product_id": item["product_id"],
                        "reason": "Insufficient stock"
                    })
                )
                return {"status": "failed"}

        # Publish inventory.reserved event
        dapr.publish_event(
            pubsub_name="pubsub",
            topic_name="inventory.reserved",
            data=json.dumps({"order_id": order["order_id"]})
        )

    return {"status": "reserved"}
```

**Payment Service (Subscriber)**

```python
from fastapi import FastAPI, Request
from dapr.ext.fastapi import DaprApp
from dapr.clients import DaprClient
import json
import random

app = FastAPI(title="Payment Service")
dapr_app = DaprApp(app)

@dapr_app.subscribe(pubsub="pubsub", topic="inventory.reserved")
async def handle_inventory_reserved(request: Request):
    event = await request.json()
    order_id = event["data"]["order_id"]

    print(f"Processing payment for order: {order_id}")

    with DaprClient() as dapr:
        # Get order details
        state = dapr.get_state(store_name="statestore", key=f"order:{order_id}")
        order = json.loads(state.json())

        # Process payment (simulated)
        success = random.random() > 0.1  # 90% success rate

        if success:
            # Update order status
            order["status"] = "paid"
            dapr.save_state(
                store_name="statestore",
                key=f"order:{order_id}",
                value=json.dumps(order)
            )

            # Publish payment.completed event
            dapr.publish_event(
                pubsub_name="pubsub",
                topic_name="payment.completed",
                data=json.dumps({"order_id": order_id})
            )

            return {"status": "paid"}
        else:
            # Publish payment.failed event
            dapr.publish_event(
                pubsub_name="pubsub",
                topic_name="payment.failed",
                data=json.dumps({"order_id": order_id})
            )
            return {"status": "failed"}
```

**Notification Service (Subscriber)**

```python
from fastapi import FastAPI, Request
from dapr.ext.fastapi import DaprApp
from dapr.clients import DaprClient
import json

app = FastAPI(title="Notification Service")
dapr_app = DaprApp(app)

@dapr_app.subscribe(pubsub="pubsub", topic="payment.completed")
async def handle_payment_completed(request: Request):
    event = await request.json()
    order_id = event["data"]["order_id"]

    with DaprClient() as dapr:
        # Get order details
        state = dapr.get_state(store_name="statestore", key=f"order:{order_id}")
        order = json.loads(state.json())

        print(f"Sending confirmation email for order: {order_id}")
        print(f"Customer: {order['customer_id']}")
        print(f"Total: ${order['total']}")

        # Here you would send an actual email

        # Publish order.confirmed event
        dapr.publish_event(
            pubsub_name="pubsub",
            topic_name="order.confirmed",
            data=json.dumps(order)
        )

    return {"status": "notified"}
```

---

## Exercises

### Exercise 1: Chat Application
1. Create a chat service using pub/sub
2. Implement:
   - Publish messages to a `chat.messages` topic
   - Subscribe to messages and display them
   - Support multiple chat rooms (topics)

### Exercise 2: Notification System
1. Create a notification service that:
   - Subscribes to multiple event types
   - Routes events to appropriate channels (email, SMS, push)
   - Implements content-based routing

### Exercise 3: Saga Pattern
1. Implement a saga pattern using pub/sub:
   - Order → Inventory → Payment → Shipping
   - Compensating actions if any step fails

---

## Summary

In this module, you learned:

- Event-driven architecture with pub/sub
- Publishing events with Dapr
- Subscribing to events
- Message routing strategies
- Dead letter queues
- Complete e-commerce event flow

### Next Steps

Continue to [Module 5: Bindings](../05-bindings/README.md) to learn about input and output bindings.
