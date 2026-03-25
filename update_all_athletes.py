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

# Datos completos de las 17 jugadoras
raw_data = """Samanta Mosquera	2012	55	56		31,22	33,92	32,88	-0,058283292	38,98	162	170	8	215	2.54	2.48
Anthonella Tejada	2012	51	53	34,807	30,15	27,17	28,75	0,058152374	31,21			0	217	2.48	2.46
Alisson Arbelaez	2012	47	50	35,216	29,17	28,31	26,66	-0,058283292	30,84	170	166	-4	210	2.41	2.37
Nicol Jaramillo	2012	60	60	32,581	31,3	31,26	31,78	0,016634677	32,59	165	172	7	216	2.49	2.48
Sara Vergara	2012	56	57	33,038	33,3	28,96	27,1	-0,064226519	28,95	163	160	-3	206	2.35	2.33
Luciana Zea	2011	76	79	25,107	22,71	24,05	21,24	-0,116839917	24,11	182	188	6	236	2.60	2.57
Maria José Barrera	2012	65	65	35,763	33,56	30,84	32,33	0,048313878	35,67	181	186	5	238	2.74	2.70
Sofia Sanchez	2012	47	50	29,922	28,35	21,17	22,48	0,061880019	27,99	162	162	0	210	2.38	2.33
Juanita Arango	2012	45	45	34,285	31,15	31,27	32,72	0,046370323	35,71	148	153	5	190	2.26	2.23
Mariangel Cano	2011	60	60		32,03	31,07	30,26	-0,026070164	33,58	167	165	-2	212	2.46	2.42
Maria Jose Salazar	2011	55	55		36,41	32,92	32,62	-0,009113001	38,6	173	171	-2	222	2.61	2.55
Violeta Tabares	2012	49	53	40,604	37,51	35,13	35,41	0,007970396	38,24	164	163	-1	206	2.44	2.41
Salome Franco	2011	60	61	35,103	31,16			#DIV/0!				0	217		
Julieta Garcia	2011		54	30,394		26,76	28,52	0,065769806	30,72	169	175	6	223	2.54	2.52
MICHELLE JAUREGUI	2012		61	40,854		34	35,6	0,047058824	41,53	174	173	-1	221	2.63	2.57
Maria Jose Perez	2013		56			31,32	29,05	-0,07247765	33,55	162	167	5	205	2.39	2.34
Luciana Guevara	2013		62			28,33	28,91	0,020472997	28,55	173	176	3	222	2.51	2.51"""

def get_all_records():
    r = requests.get(url, headers=headers)
    return r.json().get('records', []) if r.status_code == 200 else []

print("🔍 Sincronizando datos técnicos de las 17 jugadoras...")
records = get_all_records()

for line in raw_data.strip().split('\n'):
    p = line.split('\t')
    name = p[0].strip()
    record = next((r for r in records if r['fields'].get('Nombre completo') == name), None)
    
    if record:
        def clean(val): 
            try: return val.replace(',', '.').strip() or "0"
            except: return "0"

        # Formato de tabla para la web
        technical_html = f"""
        <table class='w-full text-[10px] mt-4 border-collapse'>
            <tr class='border-b border-white/10'><td class='py-1 opacity-60'>Peso</td><td class='text-right font-bold'>{p[2] or p[3]} kg</td></tr>
            <tr class='border-b border-white/10'><td class='py-1 opacity-60'>SJ (Salto)</td><td class='text-right font-bold'>{clean(p[6])} cm</td></tr>
            <tr class='border-b border-white/10'><td class='py-1 opacity-60'>CMJ (Salto)</td><td class='text-right font-bold'>{clean(p[7])} cm</td></tr>
            <tr class='border-b border-white/10'><td class='py-1 opacity-60'>Salto Libre</td><td class='text-right font-bold'>{clean(p[9])} cm</td></tr>
            <tr class='border-b border-white/10'><td class='py-1 opacity-60'>Alcance Remate</td><td class='text-right font-bold'>{p[14] if len(p)>14 else '-'} m</td></tr>
            <tr><td class='py-1 opacity-60'>Alcance Bloqueo</td><td class='text-right font-bold'>{p[15] if len(p)>15 else '-'} m</td></tr>
        </table>"""

        payload = {
            "fields": {
                "Estatura (cm)": float(clean(p[10])) if len(p)>10 else 0,
                "Envergadura (cm)": float(clean(p[11])) if len(p)>11 else 0,
                "Notas de perfil": technical_html
            }
        }
        requests.patch(f"{url}/{record['id']}", headers=headers, json=payload)
        print(f"✅ {name} actualizada.")
    time.sleep(0.1)

print("\n✨ ¡Base de datos técnica completada!")
