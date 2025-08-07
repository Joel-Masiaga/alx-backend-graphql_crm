from datetime import datetime
import requests

def log_crm_heartbeat():
    """
    Logs a heartbeat message and optionally checks the GraphQL endpoint.
    """
    log_file_path = "/tmp/crm_heartbeat_log.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Optional: Check GraphQL endpoint
    try:
        response = requests.post("http://localhost:8000/graphql", json={'query': '{ hello }'})
        if response.status_code == 200:
            status = "and GraphQL is responsive"
        else:
            status = f"but GraphQL returned status code {response.status_code}"
    except requests.exceptions.RequestException as e:
        status = f"but GraphQL check failed: {e}"

    message = f"{timestamp} - CRM is alive {status}\n"
    with open(log_file_path, "a") as f:
        f.write(message)