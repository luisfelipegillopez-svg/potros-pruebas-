import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('AIRTABLE_TOKEN')
BASE_ID = os.getenv('AIRTABLE_BASE_ID')
TABLE_ID = os.getenv('AIRTABLE_TABLE_NAME')

url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def get_all_records():
    r = requests.get(url, headers=headers)
    return r.json().get('records', []) if r.status_code == 200 else []

print("🔍 Iniciando actualización de categorías a Infantil A1...")
records = get_all_records()

for rec in records:
    # Solo actualizar si el campo Categoría está vacío
    if not rec['fields'].get('Categoría'):
        payload = {
            "records": [{
                "id": rec['id'],
                "fields": { "Categoría": "Infantil A1" }
            }]
        }
        res = requests.patch(url, headers=headers, json=payload)
        if res.status_code == 200:
            print(f"✅ Jugadora {rec['fields'].get('Nombre completo')} marcada como Infantil A1")
        else:
            print(f"❌ Error al actualizar {rec['fields'].get('Nombre completo')}")
        time.sleep(0.2)

print("\n✨ Categorización completada.")
