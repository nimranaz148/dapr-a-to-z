from dapr.clients import DaprClient

def use_bindings():
    with DaprClient() as client:
        # Output Binding example
        # Operation and data depend on the specific component (e.g., S3, SendGrid)
        try:
            resp = client.invoke_binding(
                binding_name="external-storage",
                operation="create",
                data='{"content": "Dapr Masterclass"}',
                binding_metadata={"fileName": "master.txt"}
            )
            print("Binding invoked successfully")
        except Exception as e:
            print(f"Binding failed: {e}")

if __name__ == "__main__":
    use_bindings()
