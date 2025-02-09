import ssl
from fastapi import FastAPI
import requests
import os
import pandas as pd
from openpyxl import Workbook
from datetime import datetime
import schedule
import time
from threading import Thread
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from src.api.routes import router

# Kontrollera att nödvändiga paket är installerade
try:
    import openpyxl
except ImportError:
    os.system("pip install openpyxl")

# Se till att SSL är aktiverat
try:
    ssl.create_default_context()
except AttributeError:
    raise ImportError("SSL-modulen saknas. Se till att din Python-miljö inkluderar SSL-stöd.")

# Skapa FastAPI-instansen
app = FastAPI(title="EzRollout")

# Microsoft Graph API-konfiguration
load_dotenv()
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SCOPE = "https://graph.microsoft.com/.default"
TOKEN_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"

# Lägg till i app-konfigurationen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Funktion för att autentisera med Graph API
def get_access_token():
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": SCOPE
    }
    response = requests.post(TOKEN_URL, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        return None

# Hämta enhetsstatus från Intune
@app.get("/device-status")
def get_device_status():
    access_token = get_access_token()
    if not access_token:
        return {"error": "Misslyckades med att autentisera"}
    
    headers = {"Authorization": f"Bearer {access_token}"}
    url = "https://graph.microsoft.com/v1.0/deviceManagement/managedDevices"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("value", [])
    else:
        return {"error": "Misslyckades med att hämta enhetsstatus", "details": response.text}

# Generera en Excel-rapport
@app.get("/generate-report")
def generate_report():
    devices = get_device_status()
    if "error" in devices:
        return devices
    
    if not isinstance(devices, list) or len(devices) == 0:
        return {"error": "Ingen enhetsdata tillgänglig"}
    
    df = pd.DataFrame(devices)
    file_path = "intune_report.xlsx"
    df.to_excel(file_path, index=False, engine='openpyxl')
    
    return {"message": "Rapport skapad", "file": file_path}

# Endpoint för att ladda ner rapport
@app.get("/download-report")
def download_report():
    file_path = "intune_report.xlsx"
    if os.path.exists(file_path):
        return {"message": "Ladda ner rapport", "url": file_path}
    else:
        return {"error": "Ingen rapport tillgänglig"}

# Grundläggande route
@app.get("/")
async def root():
    return {"message": "Welcome to EzRollout"}

# Ny funktion för att analysera deployment success rate
@app.get("/analyze-deployment")
async def analyze_deployment():
    devices = get_device_status()
    if "error" in devices:
        return devices
    
    total_devices = len(devices)
    successful_deployments = sum(1 for device in devices if device.get("complianceState") == "compliant")
    success_rate = (successful_deployments / total_devices) * 100 if total_devices > 0 else 0
    
    return {
        "total_devices": total_devices,
        "successful_deployments": successful_deployments,
        "success_rate": success_rate,
        "timestamp": datetime.now().isoformat()
    }

# Funktion för automatisk rapportgenerering
def scheduled_report_generation():
    response = requests.get("http://localhost:8000/api/generate-report")
    print(f"Report generated at {datetime.now()}: {response.status_code}")

# Starta schemalagd rapportgenerering
def start_scheduler():
    schedule.every().day.at("00:00").do(scheduled_report_generation)
    while True:
        schedule.run_pending()
        time.sleep(60)

# Starta scheduler i en separat tråd när appen startar
@app.on_event("startup")
async def startup_event():
    Thread(target=start_scheduler, daemon=True).start()

# Inkludera routes
app.include_router(router, prefix="/api")
