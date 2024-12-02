import requests
import json
from datetime import datetime
import time
import pytz

# Endpoints para las pruebas
endpoints = {
    "Login": {
        "url": "https://financlick.somee.com/api/Usuario/login",
        "method": "POST",
        "data": {"usuario": "davidf", "contrasenia": "password123"}
    },
    "Amortizaciones": {
        "url": "https://financlick.somee.com/api/Credito/Amortizaciones/1",
        "method": "GET"
    }
}

# Zona horaria de México
mexico_tz = pytz.timezone("America/Mexico_City")


def ejecutar_pruebas():
    resultados = []
    token = None

    # **Paso 1: Login**
    try:
        login_response = requests.post(endpoints["Login"]["url"], json=endpoints["Login"]["data"], timeout=10)
        timestamp = datetime.now(mexico_tz).isoformat()

        if login_response.status_code == 200:
            login_data = login_response.json()
            token = login_data.get("token")

        resultados.append({
            "endpoint": "Login",
            "url": endpoints["Login"]["url"],
            "status_code": login_response.status_code,
            "response": login_response.json(),
            "timestamp": timestamp,
        })
    except Exception as e:
        resultados.append({
            "endpoint": "Login",
            "url": endpoints["Login"]["url"],
            "error": str(e),
            "timestamp": datetime.now(mexico_tz).isoformat(),
        })

    # **Paso 2: Amortizaciones**
    if token:
        try:
            headers = {"Authorization": f"Bearer {token}"}
            amortizaciones_response = requests.get(endpoints["Amortizaciones"]["url"], headers=headers, timeout=10)
            timestamp = datetime.now(mexico_tz).isoformat()

            resultados.append({
                "endpoint": "Amortizaciones",
                "url": endpoints["Amortizaciones"]["url"],
                "status_code": amortizaciones_response.status_code,
                "response": amortizaciones_response.json(),
                "timestamp": timestamp,
            })
        except Exception as e:
            resultados.append({
                "endpoint": "Amortizaciones",
                "url": endpoints["Amortizaciones"]["url"],
                "error": str(e),
                "timestamp": datetime.now(mexico_tz).isoformat(),
            })
    else:
        resultados.append({
            "endpoint": "Amortizaciones",
            "url": endpoints["Amortizaciones"]["url"],
            "error": "No se pudo obtener el token del login.",
            "timestamp": datetime.now(mexico_tz).isoformat(),
        })

    # Guardar los resultados en un archivo log
    with open("log_amortizaciones.json", "a") as log_file:
        for resultado in resultados:
            log_file.write(json.dumps(resultado, ensure_ascii=False) + "\n")

    print("Pruebas ejecutadas y resultados guardados en 'log_financlick.json'.")


if __name__ == "__main__":
    print("Ejecutando pruebas cada 5 minutos.")
    while True:
        ejecutar_pruebas()
        print("Esperando 5 minuto antes de la próxima ejecución...")
        time.sleep(60)
