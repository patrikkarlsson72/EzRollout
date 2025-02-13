# EzRollout

A tool for monitoring and managing application deployments via Microsoft Intune.

## Features
- Search applications by ID or name
- View detailed deployment status
- Generate deployment reports
- Monitor installation success rates
- Track device compliance

## Tech Stack
- Python
- FastAPI
- Microsoft Graph API
- SQLite
- Pandas
- OpenPyXL
- GPT-4 API
- Streamlit

## Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in your credentials
4. Run the API: `uvicorn main:app --reload`
5. Run the dashboard: `streamlit run dashboard.py`

## Project Structure 