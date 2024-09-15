#!/bin/sh

alembic upgrade head

exec uvicorn src.main:app --host 0.0.0.0 --port 8080 --workers 4