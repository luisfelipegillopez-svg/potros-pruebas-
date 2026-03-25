import requests
import json

url = "http://127.0.0.1:5000/api/ai/generate"
data = {
    "prompt": "MICRO-CICLO: Lunes. Objetivo: Prueba. Métodos: Analíticos. Cat: Infantil. Duración: 60 min. Jugadoras: 12.",
    "system_instruction": "Eres Entrenador Nacional de Voleibol de Élite. Diseña una planificación técnica avanzada. Crea una tabla HTML para cada día. Estructura: <div class='day-table'><h2>🏐 DÍA: [NOMBRE]</h2><table style='width:100%; border-collapse:collapse; margin-bottom:20px;' border='1'><thead><tr style='background:#1e1b4b; color:white;'><th>EJERCICIO</th><th>MÉTODO</th><th>DESCRIPCIÓN Y PASOS</th><th>TIPS DE ÉLITE</th></tr></thead><tbody>[Filas con <tr><td>...</td>]</tbody></table></div>"
}
try:
    response = requests.post(url, json=data)
    print("Status Code:", response.status_code)
    print("Response:", response.text)
except Exception as e:
    print("Error:", e)
