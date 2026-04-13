import requests
import os
from dotenv import load_dotenv

load_dotenv()

# URL en variable de entorno
API_URL = os.getenv("BENCINA_API_URL")

def fetch_all_stations():
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.copec.cl/"
    }
    try:
        response = requests.get(API_URL, headers=headers, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        return []