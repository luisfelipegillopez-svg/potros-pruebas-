import json
import os
import requests
import re
import concurrent.futures
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# ==========================================
# CONFIGURACIÓN BÓVEDA
# ==========================================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY: genai.configure(api_key=GEMINI_API_KEY)

AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN")
AIRTABLE_BASE_ID = "appczH8CG08DHek22"
MASTER_PIN = os.getenv("MASTER_PIN", "Fg050522")

SAFETY_SETTINGS = {c: HarmBlockThreshold.BLOCK_NONE for c in [
    HarmCategory.HARM_CATEGORY_HARASSMENT, 
    HarmCategory.HARM_CATEGORY_HATE_SPEECH, 
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, 
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT
]}

def sanitize_html(html_string):
    if not html_string: return ""
    clean = re.sub(r'<script.*?>.*?</script>', '', html_string, flags=re.DOTALL | re.IGNORECASE)
    clean = re.sub(r'\s+on\w+\s*=\s*(["\']).*?\1', '', clean, flags=re.IGNORECASE)
    clean = re.sub(r'href\s*=\s*(["\'])javascript:.*?\1', '', clean, flags=re.IGNORECASE)
    return clean

def airtable_request(table_name, method='GET', data=None):
    if not AIRTABLE_TOKEN or not AIRTABLE_BASE_ID: return []
    encoded_name = table_name.replace(' ', '%20')
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{encoded_name}"
    headers = {"Authorization": f"Bearer {AIRTABLE_TOKEN}", "Content-Type": "application/json"}
    try:
        if method == 'GET':
            all_records = []
            offset = None
            while True:
                params = {"offset": offset} if offset else {}
                r = requests.get(url, headers=headers, params=params, timeout=15)
                if r.status_code != 200: break
                resp = r.json()
                all_records.extend(resp.get('records', []))
                offset = resp.get('offset')
                if not offset: break
            return all_records
        elif method == 'POST':
            r = requests.post(url, headers=headers, json=data, timeout=15)
            return r.json().get('records', [{}])[0] if r.status_code == 200 else r.json()
        elif method == 'PATCH':
            r = requests.patch(url, headers=headers, json=data, timeout=15)
            return r.json()
        elif method == 'DELETE':
            requests.delete(f"{url}/{data}", headers=headers, timeout=15)
            return {"success": True}
    except Exception as e:
        return {"error": str(e)}
    return []

@app.route('/')
def index(): return render_template('index.html')

@app.route('/api/login/staff', methods=['POST'])
def login_staff():
    pin_sent = str(request.json.get('pin', '')).strip()
    if pin_sent == MASTER_PIN: 
        return jsonify({"success": True, "role": "superadmin", "data": {"name": "Súper Admin", "teams": "Todas"}})
    
    staff_records = airtable_request("Staff")
    for r in staff_records:
        if str(r['fields'].get('PIN', '')).strip() == pin_sent:
            status = str(r['fields'].get('Estado', 'pendiente')).lower()
            if 'pendiente' in status:
                return jsonify({"success": False, "error": "pendiente"})
            return jsonify({
                "success": True, 
                "role": status, 
                "data": {"id": r['id'], "name": r['fields'].get('Nombre', ''), "teams": r['fields'].get('Categorías Asignadas', '')}
            })
    return jsonify({"success": False, "error": "incorrecto"}), 401

@app.route('/api/login/parent', methods=['POST'])
def login_parent():
    dni_sent = str(request.json.get('dni', '')).strip()
    if len(dni_sent) < 5: return jsonify({"success": False}), 400
    athletes = airtable_request("Jugadoras")
    for r in athletes:
        athlete_dni = str(r['fields'].get('Documento de identidad') or "")
        if dni_sent in athlete_dni and athlete_dni != "":
            return jsonify({"success": True, "athlete_id": r['id']})
    return jsonify({"success": False}), 404

@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        def f(t): return airtable_request(t)
        tables = ["Jugadoras", "Planes Cancha", "Planes Fisicos", "Staff", "Asistencia", "Evaluaciones Físicas"]
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            res = list(executor.map(f, tables))
        
        def validate(data): return data if isinstance(data, list) else []
        def safe_link(record, field): 
            val = record['fields'].get(field)
            return val[0] if isinstance(val, list) and len(val) > 0 else None

        athletes_raw = validate(res[0])
        plans_raw = validate(res[1])
        phys_raw = validate(res[2])
        staff_raw = validate(res[3])
        att_raw = validate(res[4])
        eval_raw = validate(res[5])

        return jsonify({
            "athletes": [{"id": r['id'], "name": r['fields'].get('Nombre completo', 'Sin Nombre'), "category": r['fields'].get('Categoría', 'General'), "height": r['fields'].get('Estatura (cm)', 0), "wingspan": r['fields'].get('Envergadura (cm)', 0), "notes": r['fields'].get('Notas de perfil', ''), "dni": "", "year": r['fields'].get('Año de nacimiento', '')} for r in athletes_raw],
            "sessionPlans": [{"id": r['id'], "date": r['fields'].get('Fecha', ''), "cat": r['fields'].get('Categoría', ''), "day": r['fields'].get('Día', ''), "dur": r['fields'].get('Duración', 0), "players": r['fields'].get('Jugadoras', 0), "method": r['fields'].get('Método', ''), "obj": r['fields'].get('Objetivo', ''), "sessionHTML": r['fields'].get('Contenido HTML', '')} for r in plans_raw],
            "physicalPlans": [{"id": r['id'], "date": r['fields'].get('Fecha', ''), "category": r['fields'].get('Equipo', ''), "duration": r['fields'].get('Duración', ''), "days": r['fields'].get('Días/Sem', ''), "material": r['fields'].get('Material', ''), "focus": r['fields'].get('Enfoque', ''), "mainHTML": r['fields'].get('Contenido HTML', '')} for r in phys_raw],
            "registeredCoaches": [{"id": r['id'], "name": r['fields'].get('Nombre', ''), "pin": str(r['fields'].get('PIN', '')), "status": r['fields'].get('Estado', 'pendiente'), "teams": r['fields'].get('Categorías Asignadas', '')} for r in staff_raw],
            "attendance": [{"id": r['id'], "jugadora_id": safe_link(r, 'Deportista'), "fecha": r['fields'].get('Fecha'), "asistio": r['fields'].get('Asistió', False), "equipo": r['fields'].get('Equipo')} for r in att_raw],
            "evaluations": [{"id": r['id'], "jugadora_id": safe_link(r, 'Deportista'), "fecha": r['fields'].get('Fecha de la toma de datos', ''), "sj": r['fields'].get('SJ (Squat Jump) (number)', 0), "cmj": r['fields'].get('CMJ (Countermovement Jump)', 0), "weight": r['fields'].get('Peso (kg)', 0)} for r in eval_raw]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/save/staff', methods=['POST'])
def save_staff():
    d = request.json
    f = {"Nombre": d['name'], "PIN": int(d['pin']), "Estado": d.get('status', 'pendiente'), "Categorías Asignadas": d.get('teams', '')}
    return jsonify(airtable_request("Staff", "POST", {"records": [{"fields": f}]}))

@app.route('/api/save/cancha', methods=['POST'])
def save_cancha():
    d = request.json
    f = {"Fecha": d['date'], "Categoría": d['cat'], "Día": d['day'], "Duración": int(d.get('dur', 0)), "Jugadoras": int(d.get('players', 0)), "Método": d.get('method', ''), "Objetivo": d['obj'], "Contenido HTML": sanitize_html(d['sessionHTML'])}
    return jsonify(airtable_request("Planes Cancha", "POST", {"records": [{"fields": f}]}))

@app.route('/api/save/fisica', methods=['POST'])
def save_fisica():
    d = request.json
    f = {"Fecha": d['date'], "Equipo": d['category'], "Duración": str(d['duration']), "Días/Sem": str(d['days']), "Material": d['material'], "Enfoque": d['focus'], "Contenido HTML": sanitize_html(d['mainHTML'])}
    return jsonify(airtable_request("Planes Fisicos", "POST", {"records": [{"fields": f}]}))

@app.route('/api/ai/cancha', methods=['POST'])
def generate_cancha():
    try:
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        mission = "Eres Entrenador Nacional Élite. Generar planificación técnica en TABLA HTML. PROHIBIDO incluir calentamientos o retroalimentación. Empieza directamente con <table>."
        response = model.generate_content(f"{mission}\n\n{request.json['prompt']}", safety_settings=SAFETY_SETTINGS, generation_config={"temperature": 0.2})
        text = response.text.replace('```html', '').replace('```', '').strip()
        match = re.search(r'(<table|<h[1-3])', text, re.IGNORECASE)
        return jsonify({"html": text[match.start():] if match else text})
    except: return jsonify({"error": "IA ocupada"}), 500

@app.route('/api/ai/fisica', methods=['POST'])
def generate_fisica():
    try:
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        mission = "Preparador Físico Voleibol Élite. Tabla HTML sin explicaciones."
        response = model.generate_content(f"{mission}\n\n{request.json['prompt']}", safety_settings=SAFETY_SETTINGS)
        text = response.text.replace('```html', '').replace('```', '').strip()
        match = re.search(r'<table.*?>.*?</table>', text, re.DOTALL | re.IGNORECASE)
        return jsonify({"html": match.group(0) if match else text})
    except: return jsonify({"error": "IA ocupada"}), 500

@app.route('/api/athletes/create', methods=['POST'])
def create_athlete():
    d = request.json
    f = {"Nombre completo": d['name'], "Categoría": d['category'], "Documento de identidad": int(d['dni']), "Estatura (cm)": float(d['height']), "Envergadura (cm)": float(d['wingspan']), "Notas de perfil": d['notes'], "Año de nacimiento": int(d['year'])}
    return jsonify(airtable_request("Jugadoras", "POST", {"records": [{"fields": f}]}))

@app.route('/api/athletes/update', methods=['POST'])
def update_athlete():
    d = request.json
    f = {"Nombre completo": d['name'], "Categoría": d['category'], "Documento de identidad": int(d['dni']), "Estatura (cm)": float(d['height']), "Envergadura (cm)": float(d['wingspan']), "Notas de perfil": d['notes'], "Año de nacimiento": int(d['year'])}
    return jsonify(airtable_request("Jugadoras", "PATCH", {"records": [{"id": d['id'], "fields": f}]}))

@app.route('/api/attendance/save', methods=['POST'])
def save_attendance():
    d = request.json
    records, category = d.get('records', []), d.get('category', 'General')
    for i in range(0, len(records), 10):
        batch = records[i:i+10]
        airtable_payload = {"records": [{"fields": {"Fecha Registro": f"{category} - {r['fecha']}", "Deportista": [r['jugadora_id']], "Fecha": r['fecha'], "Asistió": True, "Equipo": category}} for r in batch]}
        airtable_request("Asistencia", "POST", airtable_payload)
    return jsonify({"success": True})

@app.route('/api/staff/update', methods=['POST'])
def update_staff():
    d = request.json
    fields = {}
    if 'status' in d: fields["Estado"] = d['status']
    if 'name' in d: fields["Nombre"] = d['name']
    if 'pin' in d: fields["PIN"] = int(d['pin'])
    return jsonify(airtable_request("Staff", "PATCH", {"records": [{"id": d['id'], "fields": fields}]}))

@app.route('/api/evaluations/save', methods=['POST'])
def save_evaluation():
    f = {"Jugadora": [request.json['jugadora_id']], "Fecha de la toma de datos": request.json['fecha'], "SJ (Squat Jump) (number)": float(request.json['sj']), "CMJ (Countermovement Jump)": float(request.json['cmj']), "Peso (kg)": float(request.json['weight'])}
    return jsonify(airtable_request("Evaluaciones Físicas", "POST", {"records": [{"fields": f}]}))

@app.route('/api/delete/<path:table>/<id>', methods=['DELETE'])
def delete_record(table, id):
    airtable_request(table, "DELETE", id)
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
