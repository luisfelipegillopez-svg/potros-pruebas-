import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('AIRTABLE_TOKEN')
BASE_ID = os.getenv('AIRTABLE_BASE_ID')
PLAYERS_TABLE_ID = os.getenv('AIRTABLE_TABLE_NAME')
ATTENDANCE_TABLE_ID = "tblRhG58qUAXxpnxv"
FIELD_TO_DELETE = "fldUC8WDC2MXAtHRW"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

try:
    # 1. Intentar borrar la columna de texto vieja
    print(f"🗑️ Borrando columna de texto (ID: {FIELD_TO_DELETE})...")
    url_delete = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables/{ATTENDANCE_TABLE_ID}/fields/{FIELD_TO_DELETE}"
    r_del = requests.delete(url_delete, headers=headers)
    
    if r_del.status_code == 200:
        print("✅ Columna borrada con éxito.")
    else:
        print(f"⚠️ No se pudo borrar (Status {r_del.status_code}). Quizás es la primaria. Intentaremos crear la nueva directamente.")

    # 2. Crear la columna de Vínculo real 'Deportista'
    print("🔗 Creando columna vinculada 'Deportista'...")
    url_create = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables/{ATTENDANCE_TABLE_ID}/fields"
    payload = {
        "name": "Deportista",
        "type": "multipleRecordLinks",
        "options": {
            "linkedTableId": PLAYERS_TABLE_ID
        }
    }
    r_create = requests.post(url_create, headers=headers, json=payload)
    
    if r_create.status_code == 200:
        print("✨ ¡Columna 'Deportista' (Vínculo) creada con éxito!")
    else:
        print(f"❌ Error al crear vínculo: {r_create.text}")

except Exception as e:
    print(f"Error técnico: {e}")
