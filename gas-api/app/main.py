from fastapi import FastAPI, Query, HTTPException
from app.services.bencina_service import fetch_all_stations
from app.utils.geo_utils import calculate_distance
from app.models.schemas import SearchResponse

app = FastAPI(
    title="Bencina Finder API",
    description="API para búsqueda de estaciones de combustible según cercanía, precio y servicios."
)

@app.get("/api/stations/search", response_model=SearchResponse)
async def search_stations(
    lat: float = Query(..., description="Latitud de la ubicación actual"),
    lng: float = Query(..., description="Longitud de la ubicación actual"),
    # Validación estricta mediante regex para aceptar solo los tipos solicitados
    product: str = Query(..., pattern="^(93|95|97|diesel|kerosene)$", description="Producto: 93, 95, 97, diesel, kerosene"),
    nearest: bool = Query(False, description="Filtro para la estación más cercana"),
    store: bool = Query(False, description="Filtro para estaciones con tienda"),
    cheapest: bool = Query(False, description="Filtro para el menor precio")
):
    # 1. Obtención de datos masivos desde la API de Integración
    stations_list = fetch_all_stations()
    
    if not stations_list:
        return SearchResponse(
            success=False, 
            message="No se pudo obtener información de la fuente de datos externa."
        )

    # 2. Normalización del producto solicitado
    product_map = {
        "93": "Gasolina 93",
        "95": "Gasolina 95",
        "97": "Gasolina 97",
        "diesel": "Diesel",
        "kerosene": "Kerosene"
    }
    
    search_term = product_map[product]
    candidates = []

    # 3. Procesamiento y Filtrado
    for s in stations_list:
        # Filtro de Tienda
        if store:
            tienda_info = s.get("Tienda") or {}
            if not tienda_info.get("NombreTienda"):
                continue

        # Obtención de Precios del producto específico solicitado
        prices = s.get("Prices", [])
        p_info = next((p for p in prices if p.get("Producto") == search_term), None)
        
        if not p_info or not p_info.get("Precio"):
            continue

        try:
            price_val = int(p_info.get("Precio"))
            s_lat = float(s.get("Latitud"))
            s_lng = float(s.get("Longitud"))
            
            # Cálculo de distancia
            dist = calculate_distance(lat, lng, s_lat, s_lng)
            
            candidates.append({
                "raw": s,
                "dist": round(dist, 2),
                "price": price_val
            })
        except (ValueError, TypeError):
            continue

    if not candidates:
        raise HTTPException(
            status_code=404, 
            detail="No se encontraron estaciones para los criterios seleccionados."
        )

    # 4. Lógica de Ordenamiento
    if cheapest:
        candidates.sort(key=lambda x: (x["price"], x["dist"]))
    else:
        candidates.sort(key=lambda x: x["dist"])

    # 5. Construcción de la Respuesta Dinámica
    winner = candidates[0]
    s_data = winner["raw"]
    
    # Mapeo final de campos
    final_station_data = {
        "id": str(s_data.get("CodEs")),
        "compania": str(s_data.get("Compania")).upper(),
        "direccion": str(s_data.get("Direccion")).title(),
        "comuna": str(s_data.get("Comuna")),
        "region": str(s_data.get("Region")).upper(),
        "latitud": float(s_data.get("Latitud")),
        "longitud": float(s_data.get("Longitud")),
        "distancia(lineal)": winner["dist"],
        # El campo de precio ahora es dinámico según la búsqueda
        f"precio_{product}": winner["price"],
        "tienda": {
            "codigo": s_data.get("Tienda", {}).get("CodigoTienda"),
            "nombre": s_data.get("Tienda", {}).get("NombreTienda"),
            "tipo": s_data.get("Tienda", {}).get("Tipo")
        },
        "tiene_tienda": True if s_data.get("Tienda", {}).get("NombreTienda") else False
    }

    return SearchResponse(
        success=True,
        data=final_station_data,
        message=None
    )