#!/bin/bash

set -euo pipefail

if [ ! -f .env ] 
then
    cp .env.example .env
    NEW_KEY=$(python3 -c 'import re; from django.core.management.utils import get_random_secret_key;
print(re.escape(get_random_secret_key()))')
    sed -i "s/^SECRET_KEY=.*$/SECRET_KEY=${NEW_KEY}/" .env
fi

python3 manage.py migrate --noinput

DATA_LOADED=$(python3 -c 'import os; os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings");
import django; django.setup(); from api.models import Product; print(Product.objects.exists())')

if [ ! "$DATA_LOADED" ] 
then
    python3 manage.py loaddata example_data/*.json
fi

python3 manage.py collectstatic --noinput
python3 manage.py update_rankings

exec "$@"