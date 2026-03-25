import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('AIRTABLE_TOKEN')
BASE_ID = os.getenv('AIRTABLE_BASE_ID')
ATTENDANCE_TABLE_ID = "tblRhG58qUAXxpnxv"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

try:
    print("🏟️ Creando columna 'Equipo' en la tabla de Asistencia...")
    url = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables/{ATTENDANCE_TABLE_ID}/fields"
    payload = {
        "name": "Equipo",
        "type": "singleLineText"
    }
    r = requests.post(url, headers=headers, json=payload)
    
    if r.status_code == 200:
        print("✅ Columna 'Equipo' creada con éxito.")
    else:
        print(f"❌ Error: {r.text}")

except Exception as e:
    print(f"Error técnico: {e}")
