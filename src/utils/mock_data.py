from datetime import datetime, timedelta
import random

def generate_mock_devices(num_devices=50):
    compliance_states = ["compliant", "noncompliant", "unknown"]
    os_versions = ["Windows 11", "Windows 10", "macOS 13", "macOS 12"]
    departments = ["IT", "HR", "Sales", "Marketing", "Engineering", "Finance"]
    models = ["Surface Laptop 4", "MacBook Pro 16", "ThinkPad X1", "Dell XPS 13", "HP EliteBook"]
    sku_families = ["Windows 10 Enterprise", "Windows 11 Enterprise", "macOS Enterprise"]
    
    # Uppdatera med olika installationsstatusar
    install_states = ["Installed", "Failed", "Installing", "Uninstall Failed", "Error"]
    # Vikta sannolikheten för olika statusar (70% success, 30% andra statusar)
    install_weights = [0.7, 0.15, 0.05, 0.05, 0.05]
    
    applications = [
        {
            "id": "12345",
            "name": "Microsoft Office 365",
            "displayName": "Microsoft 365 Apps for Enterprise",
            "version": "16.0.14931.20118",
            "publisher": "Microsoft Corporation",
            "shortVersion": "16.0",
            "installState": random.choices(install_states, weights=install_weights)[0],
            "applicationKey": "O365ProPlus",
        },
        {
            "id": "12346",
            "name": "Microsoft Teams",
            "displayName": "Microsoft Teams",
            "version": "1.6.00.12335",
            "publisher": "Microsoft Corporation",
            "shortVersion": "1.6",
            "installState": random.choices(install_states, weights=install_weights)[0],
            "applicationKey": "MSTeams",
        },
        {
            "id": "12347",
            "name": "Adobe Acrobat Reader DC",
            "displayName": "Adobe Acrobat Reader DC",
            "version": "23.003.20201",
            "publisher": "Adobe Inc.",
            "shortVersion": "23.0",
            "installState": random.choices(install_states, weights=install_weights)[0],
            "applicationKey": "AdobeReader",
        },
        {
            "id": "12348",
            "name": "Adobe Creative Cloud",
            "displayName": "Adobe Creative Cloud",
            "version": "5.9.0.373",
            "publisher": "Adobe Inc.",
            "shortVersion": "5.9",
            "installState": random.choices(install_states, weights=install_weights)[0],
            "applicationKey": "CreativeCloud",
        },
        {
            "id": "12349",
            "name": "Google Chrome",
            "displayName": "Google Chrome",
            "version": "114.0.5735.199",
            "publisher": "Google LLC",
            "shortVersion": "114.0",
            "installState": random.choices(install_states, weights=install_weights)[0],
            "applicationKey": "Chrome",
        },
        {
            "id": "12350",
            "name": "Mozilla Firefox",
            "displayName": "Mozilla Firefox",
            "version": "115.0.2",
            "publisher": "Mozilla Corporation",
            "shortVersion": "115.0",
            "installState": random.choices(install_states, weights=install_weights)[0],
            "applicationKey": "Firefox",
        },
        {
            "id": "12351",
            "name": "Zoom Client",
            "displayName": "Zoom Client for Meetings",
            "version": "5.15.5.12494",
            "publisher": "Zoom Video Communications, Inc.",
            "shortVersion": "5.15",
            "installState": random.choices(install_states, weights=install_weights)[0],
            "applicationKey": "ZoomClient",
        },
        {
            "id": "12352",
            "name": "Slack",
            "displayName": "Slack",
            "version": "4.33.73",
            "publisher": "Slack Technologies, Inc.",
            "shortVersion": "4.33",
            "installState": random.choices(install_states, weights=install_weights)[0],
            "applicationKey": "Slack",
        }
    ]
    
    mock_devices = []
    for i in range(num_devices):
        # Generera ett realistiskt serienummer
        serial = f"SN{random.randint(100000, 999999)}"
        
        # Generera användarinformation
        user_id = f"user{i:03d}"
        
        # För varje enhet, skapa en kopia av applications-listan och ge varje app en slumpmässig status
        device_apps = []
        for app in random.sample(applications, random.randint(4, 8)):
            app_copy = app.copy()
            app_copy["installState"] = random.choices(install_states, weights=install_weights)[0]
            device_apps.append(app_copy)
        
        device = {
            "id": f"device_{i}",
            "deviceName": f"DEVICE-{i:03d}",
            "osVersion": random.choice(os_versions),
            "lastSyncDateTime": (datetime.now() - timedelta(hours=random.randint(1, 72))).isoformat(),
            "complianceState": random.choice(compliance_states),
            "managementAgent": "MDM",
            "operatingSystem": "Windows" if "Windows" in os_versions[i % len(os_versions)] else "macOS",
            "installedApplications": device_apps,
            "userDisplayName": f"User {user_id}",
            "mailNickname": f"{user_id}",
            "department": random.choice(departments),
            "model": random.choice(models),
            "serialNumber": serial,
            "skuFamily": random.choice(sku_families),
            "platform": "Windows" if "Windows" in os_versions[i % len(os_versions)] else "macOS",
            "osDescription": f"Microsoft Windows 10 Enterprise" if "Windows" in os_versions[i % len(os_versions)] else "macOS Ventura",
            "userPrincipalName": f"{user_id}@company.com",
        }
        mock_devices.append(device)
    
    return mock_devices

def get_mock_deployment_analysis(devices):
    total_devices = len(devices)
    successful_deployments = sum(1 for device in devices if device.get("complianceState") == "compliant")
    success_rate = (successful_deployments / total_devices) * 100 if total_devices > 0 else 0
    
    return {
        "total_devices": total_devices,
        "successful_deployments": successful_deployments,
        "success_rate": success_rate,
        "timestamp": datetime.now().isoformat()
    } 