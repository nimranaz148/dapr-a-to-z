from dapr.clients import DaprClient

def publish_messages():
    with DaprClient() as client:
        for i in range(5):
            message = {"id": i, "content": f"Message number {i}"}

            # Full parameters
            client.publish_event(
                pubsub_name="pubsub",
                topic_name="orders",
                data=message,
                data_content_type="application/json",
                metadata={"ttlInSeconds": "60"}
            )
            print(f"Published item {i}")

if __name__ == "__main__":
    publish_messages()
