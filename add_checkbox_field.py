import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('AIRTABLE_TOKEN')
BASE_ID = os.getenv('AIRTABLE_BASE_ID')

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def create_checkbox_field(table_id):
    url = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables/{table_id}/fields"
    payload = {
        "name": "Asistió",
        "type": "checkbox",
        "options": {
            "icon": "check",
            "color": "greenBright"
        }
    }
    r = requests.post(url, headers=headers, json=payload)
    return r

try:
    # 1. Buscar el ID de la tabla 'Asistencia'
    print("🔍 Buscando el ID de la tabla 'Asistencia'...")
    url_metadata = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables"
    r_meta = requests.get(url_metadata, headers=headers)
    
    if r_meta.status_code == 200:
        tables = r_meta.json().get('tables', [])
        target_table = next((t for t in tables if t.get('name') == 'Asistencia'), None)
        
        if target_table:
            table_id = target_table.get('id')
            print(f"✅ Hoja encontrada (ID: {table_id}). Intentando crear el checkbox...")
            
            # 2. Crear el campo checkbox
            r_field = create_checkbox_field(table_id)
            if r_field.status_code == 200:
                print("✨ ¡Columna 'Asistió' (Checkbox) creada con éxito!")
            else:
                print(f"❌ Error al crear columna: {r_field.status_code} - {r_field.text}")
        else:
            print("⚠️ No encontré ninguna hoja llamada 'Asistencia'. Por favor, créala manualmente primero.")
    else:
        print(f"❌ Error al leer metadata: {r_meta.status_code} - {r_meta.text}")

except Exception as e:
    print(f"Error: {e}")
