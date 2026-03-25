import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("AIRTABLE_TOKEN")
base_id = "appczH8CG08DHek22"
headers = {"Authorization": f"Bearer {token}"}

tables = ["Jugadoras", "Planes Cancha", "Planes Fisicos", "Staff", "Asistencia", "Evaluaciones Físicas"]

url = f"https://api.airtable.com/v0/meta/bases/{base_id}/tables"
r = requests.get(url, headers=headers)

if r.status_code == 200:
    data = r.json()
    for table in data['tables']:
        if table['name'] in tables:
            print(f"\n--- TABLA: {table['name']} ---")
            for field in table['fields']:
                print(f"  * {field['name']} ({field['type']})")
else:
    print("Error:", r.text)
