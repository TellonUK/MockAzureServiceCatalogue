from fastapi import FastAPI, HTTPException, Depends, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import timedelta
import asyncio
import json
from auth import authenticate_user, create_access_token, verify_token
from data import AZURE_SERVICES

app = FastAPI()

app.mount("/static", StaticFiles(directory="../../frontend/static"), name="static")
app.mount("/icons", StaticFiles(directory="../icons"), name="icons")
templates = Jinja2Templates(directory="../../frontend/templates")

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = authenticate_user(username, password)
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    
    access_token = create_access_token(data={"sub": user["username"]})
    response = RedirectResponse(url="/catalog", status_code=302)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response

@app.get("/catalog", response_class=HTMLResponse)
async def catalog(request: Request):
    token = request.cookies.get("access_token")
    if not token or not verify_token(token):
        return RedirectResponse(url="/")
    return templates.TemplateResponse("catalog.html", {"request": request, "services": AZURE_SERVICES})

@app.post("/deploy/{service_id}")
async def deploy_service(service_id: str, request: Request, config_file: UploadFile = File(...)):
    token = request.cookies.get("access_token")
    if not token or not verify_token(token):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    service = next((s for s in AZURE_SERVICES if s["id"] == service_id), None)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    config_content = await config_file.read()
    return templates.TemplateResponse("deployment.html", {
        "request": request, 
        "service": service,
        "config": config_content.decode()
    })