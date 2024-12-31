# Overview

Refreshed python API for the Records mobile application (formerly known as Genesus). 

## Develop Locally

1. fastapi dev main.py

## Docker

1. Build: `docker build -t records-api .`
2. Run: `docker run -e MONGODB_URI=$MONGODB_URI records-api`