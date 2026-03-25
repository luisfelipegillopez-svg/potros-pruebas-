import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('AIRTABLE_TOKEN')
BASE_ID = os.getenv('AIRTABLE_BASE_ID')
TABLE_NAME = os.getenv('AIRTABLE_TABLE_NAME')

url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
headers = {"Authorization": f"Bearer {TOKEN}"}

try:
    r = requests.get(url, headers=headers)
    records = r.json().get('records', [])
    print("--- LISTA DE REGISTROS EN AIRTABLE ---")
    for rec in records:
        fields = rec.get('fields', {})
        nombre = fields.get('Nombre completo')
        if not nombre:
            print(f"❌ REGISTRO SIN NOMBRE - ID Airtable: {rec.get('id')}")
        else:
            print(f"✅ {nombre}")
except Exception as e:
    print(f"Error: {e}")
