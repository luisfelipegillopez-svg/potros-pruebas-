import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('AIRTABLE_TOKEN')

# Consultar todas las bases accesibles por el token
url = "https://api.airtable.com/v0/meta/bases"
headers = {"Authorization": f"Bearer {TOKEN}"}

try:
    print("🔍 Consultando bases accesibles...")
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        bases = r.json().get('bases', [])
        if not bases:
            print("❌ El token funciona pero NO tiene acceso a ninguna base. Revisa la configuración de 'Access' en Airtable.")
        for b in bases:
            base_id = b.get('id')
            base_name = b.get('name')
            print(f"\n📂 BASE: {base_name} (ID: {base_id})")
            
            # Consultar tablas de cada base
            t_url = f"https://api.airtable.com/v0/meta/bases/{base_id}/tables"
            tr = requests.get(t_url, headers=headers)
            if tr.status_code == 200:
                tables = tr.json().get('tables', [])
                for t in tables:
                    print(f"   - TABLA: {t.get('name')}")
            else:
                print(f"   ⚠️ No se pudieron leer las tablas de esta base.")
    else:
        print(f"❌ Error de Token: {r.status_code} - {r.text}")
except Exception as e:
    print(f"Error: {e}")
