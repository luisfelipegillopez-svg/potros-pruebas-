import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('AIRTABLE_TOKEN')
BASE_ID = os.getenv('AIRTABLE_BASE_ID')
TABLE_ID = os.getenv('AIRTABLE_TABLE_NAME') # Usamos el ID de tabla guardado

url = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables"
headers = {"Authorization": f"Bearer {TOKEN}"}

try:
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        tables = r.json().get('tables', [])
        for t in tables:
            if t.get('id') == TABLE_ID or t.get('name') == TABLE_ID:
                print(f"Campos encontrados en la tabla '{t.get('name')}':")
                for f in t.get('fields', []):
                    print(f"- {f.get('name')} (Tipo: {f.get('type')})")
    else:
        print(f"Error: {r.status_code} - {r.text}")
except Exception as e:
    print(f"Error: {e}")
