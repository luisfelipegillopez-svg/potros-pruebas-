import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('AIRTABLE_TOKEN')
BASE_ID = os.getenv('AIRTABLE_BASE_ID')
PLAYERS_TABLE_ID = os.getenv('AIRTABLE_TABLE_NAME') # tblbJtUTX4lFcQY5x

url = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables"
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Definición de la nueva tabla de Asistencia
payload = {
    "name": "Asistencia",
    "description": "Registro diario de asistencia de las jugadoras",
    "fields": [
        {
            "name": "Jugadora",
            "type": "multipleRecordLinks",
            "options": {
                "linkedTableId": PLAYERS_TABLE_ID
            }
        },
        {
            "name": "Fecha",
            "type": "date",
            "options": { "format": "YYYY-MM-DD" }
        },
        {
            "name": "Asistió",
            "type": "checkbox",
            "options": { "icon": "check", "color": "greenBright" }
        }
    ]
}

try:
    print("🚀 Intentando crear la hoja de Asistencia en Airtable...")
    r = requests.post(url, headers=headers, json=payload)
    if r.status_code == 200:
        print("✅ ¡Hoja 'Asistencia' creada con éxito!")
    else:
        print(f"❌ No se pudo crear automáticamente: {r.status_code} - {r.text}")
        print("\n💡 Probablemente falte el permiso 'schema.bases:write' en tu token.")
except Exception as e:
    print(f"Error: {e}")
