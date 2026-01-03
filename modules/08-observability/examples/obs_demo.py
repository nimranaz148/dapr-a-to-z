import logging
from dapr.clients import DaprClient

logging.basicConfig(level=logging.INFO)

def check_observability():
    with DaprClient() as client:
        # Dapr automatically propagates W3C trace headers if present in incoming request
        # or initiates a new trace if not.
        logging.info("Starting Dapr operation...")
        client.invoke_method('inventory', 'check', data='{}')
        logging.info("Operation logged. Metadata available in zipkin/jaeger.")

if __name__ == "__main__":
    check_observability()
