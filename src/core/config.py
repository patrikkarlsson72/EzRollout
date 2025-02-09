import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    TENANT_ID: str = os.getenv("TENANT_ID")
    CLIENT_ID: str = os.getenv("CLIENT_ID")
    CLIENT_SECRET: str = os.getenv("CLIENT_SECRET")
    SCOPE: str = "https://graph.microsoft.com/.default"
    TOKEN_URL: str = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"

settings = Settings() 