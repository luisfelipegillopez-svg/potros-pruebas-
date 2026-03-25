import os
import requests
from dotenv import load_dotenv

load_dotenv()
url = f"https://api.airtable.com/v0/{os.getenv('AIRTABLE_BASE_ID')}/{os.getenv('AIRTABLE_TABLE_NAME')}?maxRecords=1"
headers = {"Authorization": f"Bearer {os.getenv('AIRTABLE_TOKEN')}"}

try:
    r = requests.get(url, headers=headers)
    fields = r.json().get('records', [{}])[0].get('fields', {})
    print("Columnas detectadas en Airtable:")
    for key in fields.keys():
        print(f"- {key}")
except Exception as e:
    print(f"Error: {e}")
