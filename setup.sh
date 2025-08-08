#!/bin/bash

set -euo pipefail

cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

docker-compose up --build -d