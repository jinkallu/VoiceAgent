# Azure Container Apps: Frontend + Backend Setup

## Overview
This project deploys a **frontend (React)** and **backend (FastAPI)** using Docker containers to **Azure Container Apps**. It uses a user-assigned managed identity with subscription-level access and follows a secure, environment-driven configuration.

---

## Architecture

```
[React Frontend (Docker + Nginx)] --> [FastAPI Backend (Docker + Uvicorn)]
        |                                        |
        |------> Azure Container Apps <----------|
```

---

## Components

### Frontend
- **Built with**: React (Node.js)
- **Served via**: Nginx
- **Dockerfile (frontend):**
```Dockerfile
FROM node:16 AS frontend
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install --legacy-peer-deps
COPY frontend/ ./
RUN npm run build

FROM nginx:alpine
WORKDIR /app
COPY --from=frontend /app/frontend/build /app/frontend/build
COPY ./nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```
- **Nginx Config:** Ensures SPA routing:
```nginx
location / {
  try_files $uri $uri/ /index.html;
}
```

### Backend
- **Built with**: Python 3.12, FastAPI
- **Served via**: Uvicorn
- **Dockerfile (backend):**
```Dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ /app
WORKDIR /app
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Environment Configuration

### .env frontend
```env
REACT_APP_API_URL=https://admin-app.redwave-be3cee76.eastus2.azurecontainerapps.io/api
```

### React 
const API_BASE_URL = process.env.REACT_APP_API_URL;

### .env backend
```env
ALLOWED_CLOUD_ORIGIN=https://admin-app-frontend.<your-region>.azurecontainerapps.io
```

### FastAPI CORS Setup
```python
from fastapi.middleware.cors import CORSMiddleware

origins = [
    os.environ.get("ALLOWED_CLOUD_ORIGIN")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Azure Setup

### Managed Identity
- Created a **User-Defined Managed Identity**
- Assigned **"Owner"** role at **subscription** level:
  - Allows creation of resource groups
  - Allows role assignments

### Access Issues & Fixes
- If CORS errors occur when **Ingress is limited to Environment**, check that `ALLOWED_CLOUD_ORIGIN` matches the **internal app DNS**.
- When **Ingress is set to Public**, CORS issues do not appear.

### CORS Error Example
```
Access to fetch at '<API_URL>' from origin '<FRONTEND_URL>' has been blocked by CORS policy
```
- Confirm correct env var
- Confirm that origin is registered in `allow_origins`

### Fll .env backend
```
AZURE_SUBSCRIPTION_ID=c5ad8acd-d3b5-4357-beae-caeff17c2d82
PRODUCTS_BLOB_CONTAINER=pdf
AZURE_ADMIN_ID_PRINCIPAL_ID=c6d2421e-2e5e-44b5-9af8-e648ef254724
AZURE_ADMIN_RESOURCE_GROUP=admin
AZURE_ADMIN_CONTAINER_NAME=admin
AZURE_ADMIN_BLOB_NAME=users.json
PRODUCT_DATA_FILE_NAME=data.json
PRODUCTS_BLOB_CONTAINER=pdf
MAPPING_BLOB=mapping.json
ASSISTANT_IMG_NAME=assistant
ASSISTANT_IMG_TAG=latest
ASSISTANT_IMG_LOCATION=eastus 2
ADMIN_ACR_NAME=adminsu0cw
ADMIN_IMG_NAME=admin
ADMIN_IMG_TAG=latest
ADMIN_FRONTEND_IMG_NAME=admin_frontend
ADMIN_FRONTEND_IMG_TAG=latest
ADMIN_IMG_LOCATION=eastus 2
TTS_IMG_NAME=tts
TTS_IMG_TAG=main
STT_IMG_NAME=stt
STT_IMG_TAG=main
DEFAULT_PRODUCT_CONTAINER=sample-prd
LOG_CONTAINER=applog
ALLOWED_LOCAL_ORIGIN=http://localhost:3000
ALLOWED_CLOUD_ORIGIN=https://admin-app-frontend.redwave-be3cee76.eastus2.azurecontainerapps.io
BASE_API_URL=https://admin-app.redwave-be3cee76.eastus2.azurecontainerapps.io
DEFAULT_PRODUCT_DATA_PATH=./sample_prd/data.json
GODADDY_BASE_URL=https://api.godaddy.com
GODADDY_KEY=
GODADDY_SECRET=
EMAIL_SECRET_ID=
EMAIL_SECRET_VALUE=
EMAIL_CLIENT_ID=
### for agent app
OPENAI_4O_MINI_ENDPOINT=https://cog-s2kzrdow3y3rq.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-08-01-preview
OPENAI_4O_MINI_KEY=
OPENAI_4O_ENDPOINT=https://ai-jineshks5663ai187603290877.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2025-01-01-preview
OPENAI_4O_KEY=
```

### build in ACR frontend
```
az acr build --registry adminsu0cw --image admin_frontend:latest --file Dockerfile.frontend .
```
### Build docker frontend

```
docker build -f .\Dockerfile.frontend -t admin_frontend .
docker tag admin_frontend:latest adminsu0cw.azurecr.io/admin_frontend:latest
az acr login --name adminsu0cw
docker push adminsu0cw.azurecr.io/admin_frontend:latest
```
### build in ACR backend
```
az acr build --registry adminsu0cw --image admin:latest --file Dockerfile.backend .
```
### Build docker backend

```
docker build -f .\Dockerfile.backend -t admin .
docker tag admin:latest adminsu0cw.azurecr.io/admin:latest
az acr login --name adminsu0cw
docker push adminsu0cw.azurecr.io/admin:latest
```

# 📧 Send Emails with Microsoft Graph API using Python

This project demonstrates how to send emails from a **Microsoft 365 shared or user mailbox** using Python and the **Microsoft Graph API** via **Client Credentials Flow** — without user interaction.

---

## ✅ What Works

- Created and registered an app **`PythonGraphEmail`** in Azure Portal under **App registrations**
- Configured **API permissions**:
  - `Mail.Send` (**Application**) — Required admin consent ✅
- Granted **SendAs** permission to the app for the mailbox (user or shared)
- Used **MSAL** to acquire access token
- Successfully sent email via `https://graph.microsoft.com/v1.0/users/{sender}/sendMail`

---

## 📦 Requirements

Install dependencies:

```bash
pip install msal requests python-dotenv
```

### 🔐 Environment Configuration
Create a .env file in your project root with the following:

```
EMAIL_CLIENT_ID=your-app-client-id
EMAIL_SECRET_VALUE=your-client-secret
AZURE_TENANT_ID=your-tenant-id
```
### Ensure you have the Mail.Send (Application) permission granted via admin consent
### If it did not work

```
Add-RecipientPermission -Identity "noreply@tralpine.com" -Trustee "PythonGraphEmail" -AccessRights SendAs
```
---

## Notes
- Use Azure Portal or CLI to assign roles to the managed identity.
- To debug identity issues, retrieve the identity's `principal_id` and confirm it is listed in the role assignment.

---

## Next Steps
- Add logging for CORS headers in backend.
- Add health probes to container apps.
- Optional: Use Azure Key Vault to manage environment secrets securely.

