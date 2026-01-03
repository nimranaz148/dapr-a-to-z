from dapr.clients import DaprClient

def fetch_secrets():
    with DaprClient() as client:
        # 1. Single secret
        secret = client.get_secret(
            store_name="localsecrets",
            key="db-password"
        )
        print(f"Secret fetched: {list(secret.secret.keys())}")

        # 2. Bulk secrets
        all_secrets = client.get_bulk_secret(store_name="localsecrets")
        print("Bulk secrets fetched.")

if __name__ == "__main__":
    fetch_secrets()
