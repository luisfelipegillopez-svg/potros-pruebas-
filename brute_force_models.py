import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
print("Disponibles:", available)

for m in available:
    try:
        print(f"Probando {m}...")
        model = genai.GenerativeModel(m)
        response = model.generate_content("Responde OK")
        print(f"✅ ÉXITO CON {m}!")
        break
    except Exception as e:
        print(f"❌ FALLÓ {m}")
