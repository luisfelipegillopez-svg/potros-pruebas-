import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('AIRTABLE_TOKEN')
BASE_ID = os.getenv('AIRTABLE_BASE_ID')
ATTENDANCE_TABLE_ID = "tblRhG58qUAXxpnxv"
PRIMARY_FIELD_ID = "fldUC8WDC2MXAtHRW"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

try:
    print(f"✏️ Renombrando la columna primaria (ID: {PRIMARY_FIELD_ID})...")
    url = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables/{ATTENDANCE_TABLE_ID}/fields/{PRIMARY_FIELD_ID}"
    payload = {
        "name": "Fecha Registro"
    }
    r = requests.patch(url, headers=headers, json=payload)
    
    if r.status_code == 200:
        print("✅ Columna primaria renombrada a 'Fecha Registro'.")
    else:
        print(f"❌ Error al renombrar: {r.text}")

except Exception as e:
    print(f"Error técnico: {e}")
