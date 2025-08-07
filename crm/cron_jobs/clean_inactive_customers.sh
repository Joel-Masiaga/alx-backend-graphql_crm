#!/bin/bash

cd /alx_backend_graphql_crm/crm/cron_jobs > 

# Execute the Django management command to delete inactive customers and log the output to a temporary file
DELETED_COUNT=$(python manage.py shell -c "
from datetime import timedelta
from django.utils import timezone
from crm.models import Customer, Order

one_year_ago = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.filter(order__isnull=True) | Customer.objects.filter(order__order_date__lt=one_year_ago).distinct()

deleted_count = 0
for customer in inactive_customers:
    if not Order.objects.filter(customer=customer).exists() or Order.objects.filter(customer=customer).latest('order_date').order_date < one_year_ago:
        customer.delete()
        deleted_count += 1

print(f'Successfully deleted {deleted_count} inactive customers.')
")

# Log the result with a timestamp
echo "$(date +'%Y-%m-%d %H:%M:%S') - $DELETED_COUNT" >> /tmp/customer_cleanup_log.txt