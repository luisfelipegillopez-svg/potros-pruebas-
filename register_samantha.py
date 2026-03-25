import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('AIRTABLE_TOKEN')
BASE_ID = os.getenv('AIRTABLE_BASE_ID')
TABLE_ID = os.getenv('AIRTABLE_TABLE_NAME')

url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

# Construcción de la ficha técnica profesional
technical_html = """
<table class='w-full text-[10px] mt-4 border-collapse'>
    <tr class='border-b border-white/10'><td class='py-1 opacity-60'>Peso</td><td class='text-right font-bold'>57 kg</td></tr>
    <tr class='border-b border-white/10'><td class='py-1 opacity-60'>SJ (Salto)</td><td class='text-right font-bold'>31.79 cm</td></tr>
    <tr class='border-b border-white/10'><td class='py-1 opacity-60'>CMJ (Salto)</td><td class='text-right font-bold'>28.41 cm</td></tr>
    <tr class='border-b border-white/10'><td class='py-1 opacity-60'>Salto Libre</td><td class='text-right font-bold'>23.89 cm</td></tr>
    <tr class='border-b border-white/10'><td class='py-1 opacity-60'>Fecha Test</td><td class='text-right font-bold'>13/02/2026</td></tr>
</table>"""

payload = {
    "records": [{
        "fields": {
            "Nombre completo": "Samantha Echeverry Vanegas",
            "Categoría": "Infantil A2",
            "Año de nacimiento": 2012,
            "Estatura (cm)": 0,
            "Envergadura (cm)": 0,
            "Notas de perfil": technical_html
        }
    }]
}

res = requests.post(url, headers=headers, json=payload)
if res.status_code == 200:
    print("✅ Samantha Echeverry registrada con éxito en Infantil A2")
else:
    print(f"❌ Error: {res.text}")
