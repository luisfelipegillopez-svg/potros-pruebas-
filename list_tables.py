import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('AIRTABLE_TOKEN')
BASE_ID = os.getenv('AIRTABLE_BASE_ID')

# Consultar esquema de la base
url = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables"
headers = {"Authorization": f"Bearer {TOKEN}"}

try:
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        tables = r.json().get('tables', [])
        print("Tablas encontradas en esta base:")
        for t in tables:
            print(f"- {t.get('name')} (ID: {t.get('id')})")
    else:
        print(f"Error al consultar: {r.status_code} - {r.text}")
except Exception as e:
    print(f"Error: {e}")
