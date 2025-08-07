import os
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime, timedelta

# GraphQL endpoint
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"

# GraphQL query
QUERY = gql("""
query GetPendingOrders($orderDate: Date!) {
  orders(orderDate_Gte: $orderDate) {
    id
    customer {
      email
    }
  }
}
""")

def send_reminders():
    last_week = (datetime.now() - timedelta(days=7)).date()
    variables = {"orderDate": last_week.isoformat()}

    transport = RequestsHTTPTransport(url=GRAPHQL_ENDPOINT, verify=True, retries=3)
    client = Client(transport=transport, fetch_schema_from_transport=False)

    log_file_path = "/tmp/orderreminderslog.txt"  # EXACT name

    try:
        result = client.execute(QUERY, variable_values=variables)
        orders = result.get('orders', [])

        with open(log_file_path, "a") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if orders:
                for order in orders:
                    order_id = order.get('id')
                    customer_email = order.get('customer', {}).get('email')
                    log_message = f"{timestamp} - Reminder for Order ID: {order_id}, Customer Email: {customer_email}\n"
                    f.write(log_message)
            else:
                f.write(f"{timestamp} - No pending orders found.\n")

        print("Order reminders processed!")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    send_reminders()
