from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime

@shared_task
def generate_crm_report():
    """
    Generates a weekly CRM report using a GraphQL query and logs it.
    """
    log_file_path = "/tmp/crm_report_log.txt"

    # GraphQL query
    query = gql("""
    query {
      customers {
        id
      }
      orders {
        totalAmount
      }
    }
    """)

    # GraphQL client setup
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=False)

    try:
        result = client.execute(query)

        customers = result.get("customers", [])
        orders = result.get("orders", [])

        num_customers = len(customers)
        num_orders = len(orders)
        total_revenue = sum(order.get("totalAmount", 0) for order in orders)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report_message = (
            f"{timestamp} - Report: {num_customers} customers, "
            f"{num_orders} orders, {total_revenue} revenue."
        )

        with open(log_file_path, "a") as f:
            f.write(report_message + "\n")

    except Exception as e:
        with open(log_file_path, "a") as f:
            f.write(f"{datetime.now()} - Error generating report: {e}\n")
