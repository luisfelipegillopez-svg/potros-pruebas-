import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('AIRTABLE_TOKEN')
BASE_ID = os.getenv('AIRTABLE_BASE_ID')
TABLE_ID = os.getenv('AIRTABLE_TABLE_NAME')

url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}"
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

raw_data = """Samanta Mosquera	2012
Anthonella Tejada	2012
Alisson Arbelaez	2012
Nicol Jaramillo	2012
Sara Vergara	2012
Luciana Zea	2011
Maria José Barrera	2012
Sofia Sanchez	2012
Juanita Arango	2012
Mariangel Cano	2011
Maria Jose Salazar	2011
Violeta Tabares	2012
Salome Franco	2011
Julieta Garcia	2011
MICHELLE JAUREGUI	2012
Maria Jose Perez	2013
Luciana Guevara	2013"""

print("🚀 Iniciando carga profesional a Airtable...")

for line in raw_data.split('\n'):
    parts = line.split('\t')
    if len(parts) >= 2:
        name = parts[0].strip()
        year = parts[1].strip()
        
        payload = {
            "records": [
                {
                    "fields": {
                        "Nombre completo": name,
                        "Año de nacimiento": int(year) if year.isdigit() else year
                    }
                }
            ]
        }
        
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"✅ Añadida con éxito: {name}")
        else:
            print(f"❌ Error con {name}: {response.text}")
        
        time.sleep(0.2)

print("\n✨ Carga completa. Las jugadoras ya están en tu nube de Airtable.")
