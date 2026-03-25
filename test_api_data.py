import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_api():
    print("--- 🧪 INICIANDO PRUEBAS DE FUEGO ---")
    
    # 1. Test Registro Staff
    staff_data = {
        "name": "Coach de Prueba",
        "pin": 9999,
        "status": "pendiente",
        "teams": "Infantil A1"
    }
    r1 = requests.post(f"{BASE_URL}/api/save/staff", json=staff_data)
    print(f"1. Registro Staff: {'✅ ÉXITO' if r1.status_code == 200 and 'id' in r1.text else '❌ FALLÓ'}")
    if r1.status_code != 200 or 'id' not in r1.text: print(f"   Error: {r1.text}")

    # 2. Test Guardado Cancha
    cancha_data = {
        "date": "2026-03-11",
        "cat": "Infantil A1",
        "day": "Miércoles",
        "dur": 30,
        "players": 12,
        "method": "Global",
        "obj": "Prueba Técnica",
        "sessionHTML": "<table><tr><td>Ejercicio de prueba</td></tr></table>"
    }
    r2 = requests.post(f"{BASE_URL}/api/save/cancha", json=cancha_data)
    print(f"2. Guardado Cancha: {'✅ ÉXITO' if r2.status_code == 200 and 'id' in r2.text else '❌ FALLÓ'}")
    if r2.status_code != 200 or 'id' not in r2.text: print(f"   Error: {r2.text}")

    # 3. Test Guardado Física
    fisica_data = {
        "date": "2026-03-11",
        "category": "Mayores",
        "duration": "60",
        "days": "3",
        "material": "Balones",
        "focus": "Salto",
        "mainHTML": "<table><tr><td>Fuerza</td></tr></table>"
    }
    r3 = requests.post(f"{BASE_URL}/api/save/fisica", json=fisica_data)
    print(f"3. Guardado Física: {'✅ ÉXITO' if r3.status_code == 200 and 'id' in r3.text else '❌ FALLÓ'}")
    if r3.status_code != 200 or 'id' not in r3.text: print(f"   Error: {r3.text}")

if __name__ == "__main__":
    test_api()
