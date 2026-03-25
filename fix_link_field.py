import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('AIRTABLE_TOKEN')
BASE_ID = os.getenv('AIRTABLE_BASE_ID')
PLAYERS_TABLE_ID = os.getenv('AIRTABLE_TABLE_NAME')
ATTENDANCE_TABLE_ID = "tblRhG58qUAXxpnxv"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def get_field_id(table_id, field_name):
    url = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables/{table_id}"
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        fields = r.json().get('fields', [])
        for f in fields:
            if f.get('name') == field_name:
                return f.get('id')
    return None

try:
    print("🔍 Buscando el ID de la columna 'Jugadora'...")
    field_id = get_field_id(ATTENDANCE_TABLE_ID, "Jugadora")
    
    if field_id:
        # Nota: Airtable API no permite borrar columnas fácilmente vía metadatos en tokens personales
        # de forma directa sin el scope preciso. Intentaremos sobreescribirla o crear una nueva con sufijo.
        print(f"✅ Columna encontrada (ID: {field_id}).")
        
        # Intentaremos crear la columna 'Atleta' vinculada si no podemos borrar Jugadora.
        # Es más seguro crear una nueva para no entrar en bucles de error.
        print("🔗 Creando columna de vínculo 'Deportista'...")
        payload = {
            "name": "Deportista",
            "type": "multipleRecordLinks",
            "options": { "linkedTableId": PLAYERS_TABLE_ID }
        }
        r = requests.post(f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables/{ATTENDANCE_TABLE_ID}/fields", headers=headers, json=payload)
        
        if r.status_code == 200:
            print("✨ ¡Nueva columna 'Deportista' creada con éxito!")
        else:
            print(f"❌ Error: {r.text}")
    else:
        print("⚠️ No encontré la columna.")

except Exception as e:
    print(f"Error: {e}")
