import requests
from .config import settings

def get_access_token():
    data = {
        "grant_type": "client_credentials",
        "client_id": settings.CLIENT_ID,
        "client_secret": settings.CLIENT_SECRET,
        "scope": settings.SCOPE
    }
    response = requests.post(settings.TOKEN_URL, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    return None 