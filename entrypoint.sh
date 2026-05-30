#!/bin/bash
set -e

echo "==> Running database migrations..."
python manage.py migrate --noinput

echo "==> Checking if initial data needs to be loaded..."
USER_COUNT=$(python manage.py shell -c "
from accounts.models import User
print(User.objects.count())
" 2>/dev/null || echo "0")

if [ "$USER_COUNT" = "0" ]; then
    echo "==> Loading initial data (users, modules, quizzes, simulations, badges)..."
    python manage.py loaddata fixtures/initial_data.json
    echo "==> Initial data loaded successfully."
else
    echo "==> Database already has data ($USER_COUNT users), skipping fixture load."
fi

echo "==> Starting gunicorn..."
exec gunicorn phishing_platform.wsgi:application \
    --bind 0.0.0.0:80 \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
