from fastapi import APIRouter, Response, Query
from fastapi.responses import FileResponse
from ..services.intune_service import IntuneService
import pandas as pd
import os
from pathlib import Path
from datetime import datetime

router = APIRouter()
# Skapa en instans av IntuneService med demo_mode
intune_service = IntuneService(demo_mode=True)  # Eller låt den läsa från .env genom att inte skicka in något argument

# Skapa en reports-mapp om den inte finns
REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(exist_ok=True)

@router.get("/device-status")
async def get_device_status():
    return intune_service.get_device_status()

@router.get("/analyze-deployment")
async def analyze_deployment():
    devices = intune_service.get_device_status()
    return intune_service.analyze_deployment(devices)

@router.get("/generate-report")
async def generate_report(app_id: str = None, app_name: str = None):
    if not (app_id or app_name):
        return {"error": "Must specify either app_id or app_name"}

    devices = await search_applications(app_id, app_name)
    
    if not isinstance(devices, list) or len(devices) == 0:
        return {"error": "No devices found with specified application"}

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    app_identifier = app_id if app_id else "".join(c for c in app_name if c.isalnum())
    filename = f"app_deployment_report_{app_identifier}_{timestamp}.xlsx"
    file_path = REPORTS_DIR / filename
    
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        deployment_data = []
        target_app = None
        
        for device in devices:
            for app in device['installedApplications']:
                if (app_id and app['id'] == app_id) or (app_name and app_name.lower() in app['name'].lower()):
                    target_app = app
                    deployment_data.append({
                        # App-specifik information
                        'Application Name': app['displayName'],
                        'Version': app['version'],
                        'Short Version': app['shortVersion'],
                        'Publisher': app['publisher'],
                        'Application Key': app['applicationKey'],
                        'Install State': app['installState'],
                        
                        # Enhetsinformation
                        'Device Name': device['deviceName'],
                        'User': device['userDisplayName'],
                        'Department': device['department'],
                        'Platform': device['platform'],
                        'OS Version': device['osVersion'],
                        'Last Check-in': device['lastSyncDateTime']
                    })
                    break
        
        if deployment_data:
            df = pd.DataFrame(deployment_data)
            # Bara en flik: 'Deployment Status'
            df.to_excel(writer, sheet_name='Deployment Status', index=False)
    
    return {
        "message": "Application deployment report created successfully", 
        "file": str(file_path),
        "application": target_app['displayName'] if target_app else "Unknown"
    }

@router.get("/download-report")
async def download_report():
    try:
        # Uppdaterat filnamnsmönster för att matcha nya rapporten
        files = list(REPORTS_DIR.glob("app_deployment_report_*.xlsx"))
        if not files:
            return {"error": "No report available"}
        
        latest_file = max(files, key=lambda x: x.stat().st_mtime)
        return FileResponse(
            path=latest_file,
            filename=latest_file.name,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        return {"error": f"Error accessing report: {str(e)}"}

@router.get("/search-applications")
async def search_applications(app_id: str = None, app_name: str = None):
    devices = intune_service.get_device_status()
    if not isinstance(devices, list):
        return []
    
    filtered_devices = []
    for device in devices:
        apps = device.get('installedApplications', [])
        if app_id:
            if any(app['id'] == app_id for app in apps):
                filtered_devices.append(device)
        elif app_name:
            if any(app_name.lower() in app['name'].lower() for app in apps):
                filtered_devices.append(device)
    
    return filtered_devices 