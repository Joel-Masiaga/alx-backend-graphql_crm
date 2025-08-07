import os
import requests
from datetime import datetime, timedelta

# GraphQL endpoint
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"

# The GraphQL query
QUERY = """
query GetPendingOrders($orderDate: Date!) {
  orders(orderDate_Gte: $orderDate) {
    id
    customer {
      email
    }
  }
}
"""

def send_reminders():
    """
    Queries the GraphQL endpoint for orders within the last 7 days and logs reminders.
    """
    last_week = (datetime.now() - timedelta(days=7)).date()
    variables = {"orderDate": last_week.isoformat()}

    try:
        response = requests.post(GRAPHQL_ENDPOINT, json={'query': QUERY, 'variables': variables})
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json().get('data', {})
        orders = data.get('orders', [])

        log_file_path = "/tmp/order_reminders_log.txt"

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

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to GraphQL endpoint: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    send_reminders()