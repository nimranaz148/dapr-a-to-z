from dapr.clients import DaprClient

def hello_dapr():
    with DaprClient() as client:
        # Check if sidecar is healthy
        print("Checking Dapr sidecar health...")
        # In a real scenario, we might just try a small operation
        try:
            client.get_metadata()
            print("Successfully connected to Dapr!")
        except Exception as e:
            print(f"Could not connect to Dapr: {e}")

if __name__ == "__main__":
    hello_dapr()
