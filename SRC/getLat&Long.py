from geopy.geocoders import Nominatim

# Inicializa el geocodificador Nominatim
geolocator = Nominatim(user_agent="PriceSeeker")
# Dirección que deseas geocodificar
direccion = "Hospital Infantil de Especialidades de Chihuahua"
# Geocodificar la dirección
geodireccion = geolocator.geocode(direccion)
# Extraer las coordenadas (latitud y longitud)
if geodireccion:
    coordenada = (geodireccion.latitude, geodireccion.longitude)
    print(coordenada)
else:
    print("No se pudo obtener la geocodificación")
    
    
    
"""
df= pd.DataFrame({'direcc':
            ['2094 Valentine Avenue,Bronx,NY,10457',
             '1123 East Tremont Avenue,Bronx,NY,10460',
             '412 Macon Street,Brooklyn,NY,11233','Calle del Universo, 3, Valladolid',
             '302 Juan de Montoro, Aguascalientes']})

import time
start=time.time()
df['location'] = df['direcc'].apply(geocode)
df['coordenadas'] = df['location'].apply(lambda x: (x.latitude, x.longitude))
end = time.time()
elapsed = end-start
print(df)
print(str(elapsed)+"segundos")
direccion="Hospital Infantil de Especialidades de Chihuahua"
geodireccion= direccion.apply(geocode)
cordenada=geodireccion.apply(lambda x: (x.latitude, x.longitude))
print(cordenada)
from geopy.geocoders import Nominatim
"""