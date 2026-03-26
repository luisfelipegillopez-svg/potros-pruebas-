import os
import google.generativeai as genai
from dotenv import load_dotenv
import json

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

print(f"Clave detectada: {GEMINI_API_KEY[:10]}...")

prompt = "MICRO-CICLO: Lunes. Objetivo: Prueba. Métodos: Analíticos. Cat: Infantil. Duración: 60 min. Jugadoras: 12."
system_instruction = "Eres Entrenador de Voleibol. Responde SOLO JSON con clave 'html' conteniendo una tabla HTML."

try:
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    response = model.generate_content(f"{system_instruction}\n\n{prompt}")
    print("--- RESPUESTA CRUDA ---")
    print(response.text)
    print("--- FIN RESPUESTA ---")
    
    text = response.text
    if "{" in text and "}" in text:
        start = text.find("{")
        end = text.rfind("}") + 1
        json_str = text[start:end]
        data = json.loads(json_str)
        print("✅ EL JSON ES VÁLIDO")
    else:
        print("❌ NO SE ENCONTRÓ JSON")
except Exception as e:
    print(f"❌ ERROR DETECTADO: {str(e)}")
