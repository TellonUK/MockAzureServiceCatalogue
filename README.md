# Azure Service Catalog Clone

A FastAPI + HTMX clone of AWS Service Catalog with Azure services.

## Features

- JWT Authentication (guest/guest)
- Service catalog with Azure service cards
- YAML configuration upload
- Fake deployment progress simulation
- Corporate Azure-styled UI

## Setup

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Run the application:
```bash
cd backend/app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

3. Access the application at http://localhost:8000

## Login

- Username: `guest`
- Password: `guest`

## Structure

```
ServiceCatPy/
├── backend/
│   ├── app/
│   │   ├── main.py       # FastAPI application
│   │   ├── auth.py       # JWT authentication
│   │   └── data.py       # Azure services data
│   ├── secrets.py        # JWT secrets (gitignored)
│   └── requirements.txt
├── frontend/
│   ├── static/css/
│   │   └── style.css     # Corporate styling
│   └── templates/
│       ├── login.html    # Login page
│       ├── catalog.html  # Service catalog
│       └── deployment.html # Deployment progress
└── .gitignore
```