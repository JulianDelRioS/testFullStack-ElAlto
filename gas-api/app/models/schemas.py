from pydantic import BaseModel, Field
from typing import Optional, Any

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
    # El alias permite que el JSON use el nombre con paréntesis pero el código use guion bajo
    distancia_lineal: float = Field(..., alias="distancia(lineal)")
    tienda: Optional[TiendaSchema]
    tiene_tienda: bool

    class Config:
        populate_by_name = True
        
        extra = "allow" 

class SearchResponse(BaseModel):
    success: bool
    data: Optional[StationData] = None
    message: Optional[str] = None