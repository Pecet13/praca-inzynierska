# Praca-inzynierska

## PL: System opinii porównawczych

Do uruchomienia systemu wymagany jest Docker.

Pierwsze uruchomienie (z budową obrazów) w tle
```
chmod +x setup.sh
./setup.sh
```

Kolejne uruchomienia (bez budowania obrazów) w tle
```
docker compose up -d
```

Stop/start kontenerów
```
docker compose stop
docker compose start
```

Testy
```
docker exec -it praca-inzynierska-backend-1 ./manage.py test
```

Usunięcie kontenerów i sieci
```
docker compose down
```

Usunięcie kontenerów i sieci razem z wolumenami
```
docker compose down --volumes
```


## EN: Comparative review system

Docker is required to run the system.

First run (with image building) in the background
```
chmod +x setup.sh
./setup.sh
```

Next runs (without image building) in the background
```
docker compose up -d
```

Stop/start containers
```
docker compose stop
docker compose start
```

Tests
```
docker exec -it praca-inzynierska-backend-1 ./manage.py test
```

Delete containers and network
```
docker compose down
```

Delete containers and network with volumes
```
docker compose down --volumes
```