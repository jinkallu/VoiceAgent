#!/bin/bash

# Start Nginx in the foreground
nginx -g 'daemon off;' &

# Start Uvicorn (FastAPI)
cd /app/backend

uvicorn main:app --host 0.0.0.0 --port 8000
