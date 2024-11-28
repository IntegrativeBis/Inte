import requests
from PYTHON.PRIVATE import api_keymaps 

# Reemplaza con tu clave de API
# Define los puntos de origen y destino
origen = 'Chihuahua, Mexico'
destino = 'Juarez, Mexico'

# Construye la URL de la solicitud
url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origen}&destination={destino}&key={api_keymaps}"

# Realiza la solicitud a la API
response = requests.get(url)
directions = response.json()

# Verifica si la solicitud fue exitosa
if directions['status'] == 'OK':
    # Extrae las instrucciones paso a paso
    routes = directions['routes'][0]['legs'][0]['steps']
    for step in routes:
        print(step['html_instructions'])
else:
    print("Error:", directions['status'])
