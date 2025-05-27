from fastapi import FastAPI
from routers import (
    rooms_router,
    movies_router,
    functions_router,
    reservation_router,
    payments_router,
)

# Instancia principal de la aplicación FastAPI
app = FastAPI(
    title="API Cine Colombia",
    description="Api para gestionar procesos de un cine",
    version="1.0.0"
)

# Incluir routers de cada módulo de la aplicación
# Cada router agrupa los endpoints relacionados con una entidad o proceso del cine

# Endpoints para gestión de salas de cine
app.include_router(
    rooms_router.router,
    prefix="/rooms",
    tags=["Salas"]
)

# Endpoints para gestión de películas
app.include_router(
    movies_router.router,
    prefix="/movies",
    tags=["Peliculas"]
)

# Endpoints para gestión de funciones (proyecciones)
app.include_router(
    functions_router.router,
    prefix="/functions",
    tags=["Funciones"]
)

# Endpoints para gestión de reservas
app.include_router(
    reservation_router.router,
    prefix="/reservations",
    tags=["Reservas"]
)

# Endpoints para gestión de pagos
app.include_router(
    payments_router.router,
    prefix="/payments",
    tags=["Pagos"]
)
