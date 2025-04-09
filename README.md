# Praca-inzynierska

## Setup na drugim komputerze

frontend
.env
```
VITE_API_URL="http://localhost:8000"
```

backend
.env
```
DB_NAME = inz_db
DB_USER = ...
DB_PASSWORD = "..."
DB_HOST = localhost
DB_PORT = 5432
```

db
```
sudo service postgresql status
sudo service postgresql start
sudo -u postgres psql
create user ... with password '...';
CREATE DATABASE inz_db OWNER ...;
GRANT ALL PRIVILEGES ON DATABASE inz_db TO ...;
\q
python3 manage.py makemigrations
python3 manage.py migrate
```