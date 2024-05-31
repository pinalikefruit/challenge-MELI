import requests

# Hacer una solicitud HTTPS con validación del certificado SSL
response = requests.get('https://62433a7fd126926d0c5d296b.mockapi.io/api/v1/usuarios', verify=True)

# Manejar errores de verificación de certificados
try:
    response.raise_for_status()
    print("Solicitud exitosa, datos obtenidos:")
    print(response.json())
except requests.exceptions.SSLError as e:
    print(f"Error de SSL: {e}")
except requests.exceptions.HTTPError as e:
    print(f"Error HTTP: {e}")
