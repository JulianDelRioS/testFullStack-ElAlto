from pydantic import BaseModel, Field
from typing import Optional, List, Any

class TiendaSchema(BaseModel):
    codigo: Optional[str] = None
    nombre: Optional[str] = None
    tipo: Optional[str] = None

class StationData(BaseModel):
    id: str
    compania: str
    direccion: str
    comuna: str
    region: str
    latitud: float
    longitud: float
    distancia_lineal: float = Field(..., alias="distancia(lineal)") 
    precios93: int
    tienda: Optional[TiendaSchema]
    tiene_tienda: bool

    class Config:
        # Esto permite que Pydantic acepte el nombre con paréntesis
        populate_by_name = True

class SearchResponse(BaseModel):
    success: bool
    data: Optional[StationData] = None
    message: Optional[str] = None