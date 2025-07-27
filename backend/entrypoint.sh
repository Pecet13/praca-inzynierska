#!/bin/bash

if true 
then
    echo
fi

python3 manage.py migrate
python3 manage.py loaddata example_data/*.json
python3 manage.py update_rankings

exec "$@"