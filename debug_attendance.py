import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('AIRTABLE_TOKEN')
BASE_ID = os.getenv('AIRTABLE_BASE_ID')

# Buscamos un ID de jugadora real
url_jugadoras = f"https://api.airtable.com/v0/{BASE_ID}/{os.getenv('AIRTABLE_TABLE_NAME')}?maxRecords=1"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

try:
    print("🔍 Obteniendo ID de prueba...")
    res_j = requests.get(url_jugadoras, headers=headers)
    record_id = res_j.json().get('records', [{}])[0].get('id')
    
    if record_id:
        print(f"✅ ID: {record_id}. Probando guardado completo...")
        url_asistencia = f"https://api.airtable.com/v0/{BASE_ID}/Asistencia"
        payload = {
            "records": [{
                "fields": {
                    "Fecha Registro": f"Test Equipo - 2026-03-08",
                    "Deportista": [record_id],
                    "Fecha": "2026-03-08",
                    "Asistió": True,
                    "Equipo": "Test Equipo"
                }
            }]
        }
        res_a = requests.post(url_asistencia, headers=headers, json=payload)
        print("Status Airtable:", res_a.status_code)
        print("Error Detallado:", res_a.text)
    else:
        print("❌ No hay jugadoras.")
except Exception as e:
    print("Error:", e)
