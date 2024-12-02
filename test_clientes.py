import requests
import json
from datetime import datetime
import time
import pytz

mexico_tz = pytz.timezone("America/Mexico_City")

endpoints = {
    "Login": {
        "url": "https://financlick.somee.com/api/Usuario/login",
        "method": "POST",
        "data": {"usuario": "davidf", "contrasenia": "password123"}
    },
    "CrearClienteFisica": {
        "url": "https://financlick.somee.com/api/Cliente",
        "method": "POST",
        "data": {
            "idCliente": 0,
            "regimenFiscal": "FISICA",
            "idEmpresa": 0,
            "estatus": 0,
            "datosClienteFisicas": [
                {
                    "idClienteFisica": 0,
                    "idPersona": 0,
                    "idCliente": 0,
                    "idPersonaNavigation": {
                        "nombre": "Juan Prueba",
                        "apellidoPaterno": "Ramirez",
                        "apellidoMaterno": "Rosas",
                        "fechaNacimiento": "1980-01-01",
                        "paisNacimiento": "México",
                        "estadoNacimiento": "CDMX",
                        "genero": "M",
                        "rfc": "PEJL800101ABC",
                        "curp": "PEJL800101HDFLRN02",
                        "claveElector": "ABC123456",
                        "nacionalidad": "Mexicana",
                        "estadoCivil": "Soltero",
                        "calle": "Av. Siempre Viva",
                        "numExterior": "123",
                        "colonia": "Centro",
                        "codigoPostal": "01000",
                        "paisResidencia": "México",
                        "estadoResidencia": "CDMX",
                        "ciudadResidencia": "Ciudad de México",
                        "email": "juan.perez@example.com",
                        "telefono": "5555555555"
                    }
                }
            ],
            "datosClienteMorals": []
        }
    },
    "EliminarCliente": {
        "url_template": "https://financlick.somee.com/api/Cliente/{}",
        "method": "DELETE"
    },
    "CrearClienteMoral": {
        "url": "https://financlick.somee.com/api/Cliente",
        "method": "POST",
        "data": {
            "idCliente": 0,
            "regimenFiscal": "MORAL",
            "idEmpresa": 0,
            "estatus": 0,
            "datosClienteFisicas": [],
            "datosClienteMorals": [
                {
                    "idClienteMoral": 0,
                    "idPersonaMoral": 0,
                    "nombreRepLegal": "Carlos Gómez",
                    "rfcrepLegal": "GZMC800101ABC",
                    "idCliente": 0,
                    "idPersonaMoralNavigation": {
                        "razonSocial": "Empresa XYZ S.A. de C.V.",
                        "razonComercial": "XYZ Comercial",
                        "fechaConstitucion": "2000-05-15",
                        "rfc": "XYZ800101ABC",
                        "nacionalidad": "Mexicana",
                        "paisRegistro": "México",
                        "estadoRegistro": "Jalisco",
                        "ciudadRegistro": "Guadalajara",
                        "numEscritura": "12345",
                        "fechaRppc": "2000-06-01",
                        "nombreNotario": "Lic. Juan Pérez",
                        "numNotario": "27",
                        "folioMercantil": "67890",
                        "calle": "Av. Industrias",
                        "numExterior": "500",
                        "colonia": "Parque Industrial",
                        "codigoPostal": "44100",
                        "paisResidencia": "México",
                        "estadoResidencia": "Jalisco",
                        "ciudadResidencia": "Guadalajara"
                    }
                }
            ]
        }
    }
}

def ejecutar_pruebas():
    resultados = []
    token = None

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

    headers = {"Authorization": f"Bearer {token}"} if token else {}

    try:
        crear_fisica_response = requests.post(
            endpoints["CrearClienteFisica"]["url"],
            json=endpoints["CrearClienteFisica"]["data"],
            headers=headers,
            timeout=10
        )
        timestamp = datetime.now(mexico_tz).isoformat()
        id_cliente_fisica = crear_fisica_response.json().get("idCliente", 0)

        resultados.append({
            "endpoint": "CrearClienteFisica",
            "url": endpoints["CrearClienteFisica"]["url"],
            "status_code": crear_fisica_response.status_code,
            "response": crear_fisica_response.json(),
            "timestamp": timestamp,
        })

        eliminar_fisica_url = endpoints["EliminarCliente"]["url_template"].format(id_cliente_fisica)
        eliminar_fisica_response = requests.delete(eliminar_fisica_url, headers=headers, timeout=10)

        resultados.append({
            "endpoint": "EliminarClienteFisica",
            "url": eliminar_fisica_url,
            "status_code": eliminar_fisica_response.status_code,
            "response": eliminar_fisica_response.json() if eliminar_fisica_response.content else {},
            "timestamp": datetime.now(mexico_tz).isoformat(),
        })
    except Exception as e:
        resultados.append({
            "endpoint": "CrearClienteFisica/EliminarClienteFisica",
            "error": str(e),
            "timestamp": datetime.now(mexico_tz).isoformat(),
        })

    try:
        crear_moral_response = requests.post(
            endpoints["CrearClienteMoral"]["url"],
            json=endpoints["CrearClienteMoral"]["data"],
            headers=headers,
            timeout=10
        )
        timestamp = datetime.now(mexico_tz).isoformat()
        id_cliente_moral = crear_moral_response.json().get("idCliente", 0)

        resultados.append({
            "endpoint": "CrearClienteMoral",
            "url": endpoints["CrearClienteMoral"]["url"],
            "status_code": crear_moral_response.status_code,
            "response": crear_moral_response.json(),
            "timestamp": timestamp,
        })

        eliminar_moral_url = endpoints["EliminarCliente"]["url_template"].format(id_cliente_moral)
        eliminar_moral_response = requests.delete(eliminar_moral_url, headers=headers, timeout=10)

        resultados.append({
            "endpoint": "EliminarClienteMoral",
            "url": eliminar_moral_url,
            "status_code": eliminar_moral_response.status_code,
            "response": eliminar_moral_response.json() if eliminar_moral_response.content else {},
            "timestamp": datetime.now(mexico_tz).isoformat(),
        })
    except Exception as e:
        resultados.append({
            "endpoint": "CrearClienteMoral/EliminarClienteMoral",
            "error": str(e),
            "timestamp": datetime.now(mexico_tz).isoformat(),
        })

    with open("log_clientes.json", "a") as log_file:
        for resultado in resultados:
            log_file.write(json.dumps(resultado, ensure_ascii=False) + "\n")

    print("Pruebas ejecutadas y resultados guardados en 'log_clientes.json'.")

if __name__ == "__main__":
    print("Ejecutando pruebas cada 1 minuto.")
    while True:
        ejecutar_pruebas()
        time.sleep(60)
