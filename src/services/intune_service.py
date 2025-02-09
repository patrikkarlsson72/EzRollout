import requests
from ..core.auth import get_access_token
from ..utils.mock_data import generate_mock_devices, get_mock_deployment_analysis
from datetime import datetime
import os

class IntuneService:
    def __init__(self, demo_mode=False):
        self.demo_mode = demo_mode or os.getenv("DEMO_MODE", "false").lower() == "true"
        self._mock_devices = generate_mock_devices() if self.demo_mode else None

    def get_device_status(self):
        if self.demo_mode:
            return self._mock_devices

        access_token = get_access_token()
        if not access_token:
            return {"error": "Failed to authenticate"}
        
        headers = {"Authorization": f"Bearer {access_token}"}
        url = "https://graph.microsoft.com/v1.0/deviceManagement/managedDevices"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json().get("value", [])
        return {"error": "Failed to fetch device status", "details": response.text}

    def analyze_deployment(self, devices=None):
        if self.demo_mode:
            return get_mock_deployment_analysis(self._mock_devices)

        if "error" in (devices or {}):
            return devices
        
        devices = devices or self.get_device_status()
        total_devices = len(devices)
        successful_deployments = sum(1 for device in devices if device.get("complianceState") == "compliant")
        success_rate = (successful_deployments / total_devices) * 100 if total_devices > 0 else 0
        
        return {
            "total_devices": total_devices,
            "successful_deployments": successful_deployments,
            "success_rate": success_rate,
            "timestamp": datetime.now().isoformat()
        } 