from celery import shared_task
import requests
from datetime import datetime

@shared_task
def generate_crm_report():
    """
    Generates a weekly CRM report using a GraphQL query and logs it.
    """
    graphql_endpoint = "http://localhost:8000/graphql"
    log_file_path = "/tmp/crm_report_log.txt"

    query = """
    query {
      customers {
        id
      }
      orders {
        totalAmount
      }
    }
    """

    try:
        response = requests.post(graphql_endpoint, json={'query': query})
        response.raise_for_status()
        data = response.json().get('data', {})

        num_customers = len(data.get('customers', []))
        orders = data.get('orders', [])
        num_orders = len(orders)
        total_revenue = sum(order.get('totalAmount', 0) for order in orders)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report_message = (
            f"{timestamp} - Report: {num_customers} customers, "
            f"{num_orders} orders, {total_revenue} revenue."
        )

        with open(log_file_path, "a") as f:
            f.write(report_message + "\n")

    except requests.exceptions.RequestException as e:
        with open(log_file_path, "a") as f:
            f.write(f"{datetime.now()} - Error generating report: {e}\n")