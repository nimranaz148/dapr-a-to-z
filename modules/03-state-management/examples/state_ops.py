from dapr.clients import DaprClient
from dapr.clients.grpc._state import StateItem, StateOptions

def manage_state():
    with DaprClient() as client:
        # 1. Individual Save
        client.save_state(
            store_name="statestore",
            key="user_1",
            value='{"name": "Alice"}',
            metadata={"ttlInSeconds": "3600"}
        )

        # 2. Bulk Get
        items = client.get_bulk_state(
            store_name="statestore",
            keys=["user_1", "user_2"]
        ).items
        for item in items:
            print(f"Key: {item.key}, Data: {item.data}")

        # 3. Transactional Update
        client.execute_state_transaction(
            store_name="statestore",
            operations=[
                StateItem(key="user_1", value='{"name": "Alice Updated"}', action="upsert"),
                StateItem(key="user_2", value='{"name": "Bob"}', action="upsert")
            ]
        )

if __name__ == "__main__":
    manage_state()
