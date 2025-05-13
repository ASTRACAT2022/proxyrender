from fastapi import FastAPI, Response
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import subprocess
import os
from starlette.requests import Request

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def status_page(request: Request):
    # Проверка статуса WireGuard
    try:
        result = subprocess.check_output("wg show", shell=True).decode()
        online = "interface" in result
    except Exception:
        online = False
        result = "WireGuard is not active."
    
    # Получение IP-адреса
    try:
        ip = subprocess.check_output("curl -s https://ipinfo.io/ip", shell=True).decode().strip()
    except:
        ip = "N/A"

    return templates.TemplateResponse("index.html", {
        "request": request,
        "status": "🟢 Активен" if online else "🔴 Отключён",
        "ip": ip,
        "details": result
    })

@app.get("/download")
def download_config():
    return FileResponse("configs/wg0.conf", filename="wg0.conf", media_type='application/octet-stream')