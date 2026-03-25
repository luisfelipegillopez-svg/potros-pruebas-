import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('AIRTABLE_TOKEN')
BASE_ID = os.getenv('AIRTABLE_BASE_ID')
PLAYERS_TABLE_ID = os.getenv('AIRTABLE_TABLE_NAME') # tblbJtUTX4lFcQY5x
ATTENDANCE_TABLE_ID = "tblRhG58qUAXxpnxv"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

try:
    # 1. Crear campo Jugadora (Link)
    print("🔗 Creando vínculo con la tabla de Jugadoras...")
    payload_link = {
        "name": "Jugadora",
        "type": "multipleRecordLinks",
        "options": { "linkedTableId": PLAYERS_TABLE_ID }
    }
    requests.post(f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables/{ATTENDANCE_TABLE_ID}/fields", headers=headers, json=payload_link)

    # 2. Crear campo Fecha
    print("📅 Creando campo de Fecha...")
    payload_date = {
        "name": "Fecha",
        "type": "date",
        "options": { "format": "YYYY-MM-DD" }
    }
    requests.post(f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables/{ATTENDANCE_TABLE_ID}/fields", headers=headers, json=payload_date)

    print("✨ Estructura de Asistencia completada.")

except Exception as e:
    print(f"Error: {e}")
