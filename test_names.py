import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

for m in ['models/gemini-2.0-flash-001', 'models/gemini-1.5-flash-latest', 'models/gemini-1.5-flash']:
    try:
        print(f"Probando {m}...")
        model = genai.GenerativeModel(m)
        response = model.generate_content("Responde solo OK")
        print(f"✅ Éxito con {m}: {response.text}")
        break
    except Exception as e:
        print(f"❌ Falló {m}: {e}")
