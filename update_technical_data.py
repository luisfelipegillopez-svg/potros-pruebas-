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

# Datos tabulados proporcionados por el usuario
raw_data = """Samanta Mosquera	2012	55	56		31,22	33,92	32,88	-0,058283292	38,98	162	170	8	215	2.54	2.48
Anthonella Tejada	2012	51	53	34,807	30,15	27,17	28,75	0,058152374	31,21			0	217	2.48	2.46
Alisson Arbelaez	2012	47	50	35,216	29,17	28,31	26,66	-0,058283292	30,84	170	166	-4	210	2.41	2.37
Nicol Jaramillo	2012	60	60	32,581	31,3	31,26	31,78	0,016634677	32,59	165	172	7	216	2.49	2.48
Sara Vergara	2012	56	57	33,038	33,3	28,96	27,1	-0,064226519	28,95	163	160	-3	206	2.35	2.33
Luciana Zea	2011	76	79	25,107	22,71	24,05	21,24	-0,116839917	24,11	182	188	6	236	2.60	2.57
Maria José Barrera	2012	65	65	35,763	33,56	30,84	32,33	0,048313878	35,67	181	186	5	238	2.74	2.70
Sofia Sanchez	2012	47	50	29,922	28,35	21,17	22,48	0,061880019	27,99	162	162	0	210	2.38	2.33"""

def get_all_records():
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.json().get('records', [])
    return []

print("🔍 Buscando jugadoras en Airtable para actualizar...")
records = get_all_records()

for line in raw_data.strip().split('\n'):
    p = line.split('\t')
    name = p[0].strip()
    
    # Buscar el ID del registro por nombre
    record = next((r for r in records if r['fields'].get('Nombre completo') == name), None)
    
    if record:
        record_id = record['id']
        
        # Limpieza de valores numéricos (cambiar coma por punto)
        def clean_num(val):
            try: return float(val.replace(',', '.')) if val.strip() else 0
            except: return 0

        # Construir el bloque de notas con todos los datos técnicos
        notas = f"""📊 FICHA TÉCNICA ÉLITE:
- Peso: {p[2]} kg
- SJ (Squat Jump): {p[6]} cm
- CMJ (Countermovement Jump): {p[7]} cm
- Salto Libre: {p[9]} cm
- Alcance 1 mano: {p[13]} cm
- Alcance Remate: {p[14]} m
- Alcance Bloqueo: {p[15]} m"""

        payload = {
            "fields": {
                "Estatura (cm)": clean_num(p[10]),
                "Envergadura (cm)": clean_num(p[11]),
                "Notas de perfil": notas
            }
        }
        
        update_url = f"{url}/{record_id}"
        res = requests.patch(update_url, headers=headers, json=payload)
        if res.status_code == 200:
            print(f"✅ Datos técnicos actualizados para: {name}")
        else:
            print(f"❌ Error al actualizar {name}: {res.text}")
    else:
        print(f"⚠️ No se encontró a {name} en Airtable.")
    
    time.sleep(0.2)

print("\n✨ ¡Fichas técnicas completadas en la nube!")
