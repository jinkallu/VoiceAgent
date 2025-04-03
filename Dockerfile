# Stage 1: Build the frontend (Node.js)
# docker build -t admin .
# docker run -p 3000:3000 -p 8000:8000 admin
# docker tag admin:latest adminsu0cw.azurecr.io/admin:latest
# docker push adminsu0cw.azurecr.io/admin:latest

FROM node:16 AS frontend

WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm install --legacy-peer-deps

COPY frontend/ ./
RUN npm run build

# Stage 2: Build the FastAPI backend (Python)
FROM python:3.9-slim AS final

WORKDIR /app/backend

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./

# Install Nginx and dependencies
RUN apt-get update && \
    apt-get install -y nginx && \
    rm -rf /var/lib/apt/lists/*

# Set up the frontend in the final image
WORKDIR /app
COPY --from=frontend /app/frontend/build /app/frontend/build

# Copy Nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Expose ports
EXPOSE 3000
EXPOSE 8000

# Copy start script and make it executable
COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
