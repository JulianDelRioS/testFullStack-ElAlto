# Bencina API 

Este proyecto es una **API REST** robusta desarrollada en **Python** utilizando **FastAPI**. El sistema permite realizar búsquedas inteligentes de estaciones de servicio en Chile, basándose en la ubicación geográfica del usuario y aplicando diversos criterios de filtrado y optimización.

## Cumplimiento de Requisitos

La solución implementada cubre el 100% de los requisitos solicitados en la prueba técnica:

- **Desarrollo:** Implementación completa en Python utilizando FastAPI (Bonus por API REST completa).
- **Casos de Búsqueda:** Se implementaron con éxito los 4 escenarios requeridos:
  1. **Estación más cercana por producto:** Encuentra la estación más cercana a la ubicación dada.
  2. **Estación más cercana con menor precio:** Encuentra la estación más cercana que tenga el menor precio de combustible.
  3. **Estación más cercana con tienda:** Encuentra la estación más cercana que tenga tienda disponible.
  4. **Estación con tienda y menor precio:** Encuentra la estación más cercana que combine ambos beneficios.
- **Estructura de Datos:** Salidas en formato JSON estandarizado con la información exacta requerida (ID, compañía, dirección, coordenadas, precios y detalles de tienda).
- **Manejo de Errores:** Validación estricta de parámetros de entrada mediante Pydantic y respuestas HTTP informativas (404 para búsquedas sin éxito y 422 para errores de formato).

## Tecnologías y Características

- **Framework:** FastAPI (Asíncrono, alto rendimiento y validación nativa).
- **Buenas Prácticas:** Implementación de **Variables de Entorno** (`.env`) mediante `python-dotenv` para la gestión segura de configuraciones, evitando el *hardcoding* de URLs sensibles.
- **Inspección de API:** Los datos se consumen en tiempo real desde el endpoint de integración de Copec, asegurando información veraz, precisa y actualizada.
- **Geolocalización:** Cálculo de distancia lineal entre coordenadas utilizando la fórmula de Haversine en la capa de utilidades.
- **Documentación Automática:** Generación de documentación interactiva mediante Swagger UI y ReDoc.

## Estructura del Proyecto


.
├── app/
│   ├── main.py            # Lógica central de la API y Endpoints
│   ├── services/
│   │   └── bencina_service.py # Consumo de datos externos y headers de seguridad
│   ├── utils/
│   │   └── geo_utils.py       # Utilidades para cálculos geográficos (Haversine)
│   └── models/
│       └── schemas.py         # Modelos de validación (Pydantic)
├── .env                       # Gestión segura de variables de entorno
├── requirements.txt           # Dependencias del proyecto
└── README.md                  # Documentación del sistema



## Instalación y ejecución

1. Clonar el repositorio

2.Entrar al directorio del proyecto:
  cd gas-api

3.Instalar dependencias:
  pip install -r requirements.txt

4.Configurar variables de entorno, crear archivo .env (dentro de la carpeta gas-api) y pegar la variable de entorno:
  BENCINA_API_URL=https://integracion.copec.cl/stations?codEs=-1&company=-1&region=-1&comuna=-1

5.Iniciar el servidor:
  uvicorn app.main:app --reload

6.Probar la API (Documentación Interactiva):
  http://127.0.0.1:8000/docs
