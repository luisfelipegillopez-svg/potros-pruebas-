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
    url = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables"
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        tables = r.json().get('tables', [])
        for t in tables:
            if t.get('id') == ATTENDANCE_TABLE_ID:
                print(f"Campos actuales en {t.get('name')}:")
                for f in t.get('fields', []):
                    print(f"- Nombre: {f.get('name')} | ID: {f.get('id')} | Tipo: {f.get('type')}")
    else:
        print(f"Error: {r.text}")
except Exception as e:
    print(f"Error: {e}")
