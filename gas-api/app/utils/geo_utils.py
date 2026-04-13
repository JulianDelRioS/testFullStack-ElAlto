import math

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calcula la distancia en kilómetros entre dos coordenadas (Latitud/Longitud)
    usando la fórmula de Haversine.
    """
    R = 6371.0  # Radio de la Tierra en kilómetros

    # Convertir coordenadas de grados a radianes
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)

    # Aplicar fórmula de Haversine
    a = math.sin(d_lat / 2)**2 + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(d_lon / 2)**2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance