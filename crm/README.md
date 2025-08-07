# CRM Celery Setup

This document outlines the steps to set up and run Celery for scheduled tasks in the CRM application.

### Prerequisites

- **Redis**: You need a running Redis instance. The configuration assumes Redis is running on `localhost:6379`.
- **Dependencies**: Ensure all required packages are installed.

### Installation

1.  **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

2.  **Run migrations**:
    ```bash
    python manage.py migrate
    ```

### Running the Celery Components

You need to run a Celery worker and a Celery Beat scheduler. It's recommended to run these in separate terminal windows.

1.  **Start the Celery worker**:
    This process executes the tasks.

    ```bash
    celery -A crm worker -l info
    ```

2.  **Start the Celery Beat scheduler**:
    This process sends the tasks to the worker according to the defined schedules in `CELERY_BEAT_SCHEDULE`.
    ```bash
    celery -A crm beat -l info
    ```

### Verification

- After the scheduled time (Monday at 6:00 AM), check the log file:
  ```bash
  tail -f /tmp/crm_report_log.txt
  ```
  You should see a new log entry confirming the report was generated.
