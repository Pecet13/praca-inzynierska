#!/bin/bash

set -euo pipefail

NEW_KEY=$(python3 -c 'import re; from django.core.management.utils import get_random_secret_key;
print(re.escape(get_random_secret_key()))')
sed -i "s/example_key/'${NEW_KEY}'/" .env

python3 manage.py migrate --noinput

DATA_LOADED=$(python3 -c 'import os; os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings");
import django; django.setup(); from api.models import Product; print(Product.objects.exists())')

if [ "$DATA_LOADED" = "False" ] 
then
    python3 manage.py loaddata example_data/*.json
fi

python3 manage.py collectstatic --noinput
python3 manage.py update_rankings

exec "$@"