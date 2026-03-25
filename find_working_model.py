import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

models_to_test = [
    'gemini-2.0-flash-exp',
    'gemini-1.5-flash',
    'gemini-1.5-flash-latest',
    'gemini-pro'
]

print("🚀 Iniciando test de modelos...")

for model_name in models_to_test:
    try:
        print(f"Probando {model_name}...")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hola, responde solo 'OK'")
        if response.text:
            print(f"✅ ¡ÉXITO! El modelo '{model_name}' funciona perfectamente.")
            # Guardamos el ganador en un archivo temporal para que el servidor lo lea
            with open('winner_model.txt', 'w') as f:
                f.write(model_name)
            break
    except Exception as e:
        print(f"❌ Falló {model_name}: {e}")

print("\nFin del test.")
