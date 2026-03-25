import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('AIRTABLE_TOKEN')
BASE_ID = os.getenv('AIRTABLE_BASE_ID')

# Probamos con el ID de una jugadora real (Samanta Mosquera - rec...)
# Primero buscamos una jugadora para tener un ID válido
url_jugadoras = f"https://api.airtable.com/v0/{BASE_ID}/{os.getenv('AIRTABLE_TABLE_NAME')}?maxRecords=1"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

try:
    print("🔍 Obteniendo un ID de jugadora válido...")
    res_j = requests.get(url_jugadoras, headers=headers)
    record_id = res_j.json().get('records', [{}])[0].get('id')
    
    if record_id:
        print(f"✅ ID encontrado: {record_id}. Intentando guardar asistencia...")
        url_asistencia = f"https://api.airtable.com/v0/{BASE_ID}/Asistencia"
        payload = {
            "records": [{
                "fields": {
                    "Jugadora": [record_id],
                    "Fecha": "2026-03-08",
                    "Asistió": True
                }
            }]
        }
        res_a = requests.post(url_asistencia, headers=headers, json=payload)
        print("Resultado Airtable:", res_a.status_code)
        print("Mensaje:", res_a.text)
    else:
        print("❌ No se encontró ninguna jugadora en la base.")

except Exception as e:
    print(f"Error técnico: {e}")
