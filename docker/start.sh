#!/bin/sh

SERVER_ADDRESS=${SERVER_ADDRESS:-0.0.0.0:8080}
HOST=$(echo $SERVER_ADDRESS | cut -d':' -f1)
PORT=$(echo $SERVER_ADDRESS | cut -d':' -f2)

alembic upgrade head

exec uvicorn src.main:app --host $HOST --port $PORT --workers 4