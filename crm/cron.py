from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    """
    Logs a heartbeat message and checks the GraphQL endpoint using gql.
    """
    log_file_path = "/tmp/crm_heartbeat_log.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=False)

    query = gql("{ hello }")

    try:
        result = client.execute(query)
        hello_message = result.get("hello", "No response")
        status = f"and GraphQL says: {hello_message}"
    except Exception as e:
        status = f"but GraphQL check failed: {e}"

    message = f"{timestamp} - CRM is alive {status}\n"
    with open(log_file_path, "a") as f:
        f.write(message)

def update_low_stock():
    """
    Executes the UpdateLowStockProducts mutation via GraphQL
    and logs updated product names and stock levels.
    """
    log_file_path = "/tmp/low_stock_updates_log.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=False)

    mutation = gql("""
        mutation {
            updateLowStockProducts {
                updatedProducts {
                    name
                    stock
                }
                message
            }
        }
    """)

    try:
        result = client.execute(mutation)
        updates = result.get("updateLowStockProducts", {})
        products = updates.get("updatedProducts", [])
        message = updates.get("message", "No message")

        with open(log_file_path, "a") as f:
            f.write(f"{timestamp} - {message}\n")
            for p in products:
                f.write(f"{timestamp} - Restocked {p['name']} to {p['stock']}\n")

    except Exception as e:
        with open(log_file_path, "a") as f:
            f.write(f"{timestamp} - Error: {e}\n")
