from fastapi import APIRouter

from dependencies.database import db_client
from models.common import APIResponse
from models.room_model import RoomCreate


router = APIRouter()

# Crear sala


@router.post("/create")
def create_room(room_data: RoomCreate):
    """
    Endpoint para crear una nueva sala de cine.

    Este endpoint recibe los datos de la sala, crea el documento correspondiente y lo inserta en la base de datos.
    Si la inserción falla, retorna un error.

    Args:
        room_data (RoomCreate): Objeto con los datos de la sala a crear.

    Returns:
        APIResponse: Respuesta con el ID de la sala creada o un mensaje de error.
    """
    new_room = {
        "numero": room_data.numero,
        "capacidad": room_data.capacidad,
        "status": "Disponible"  # Estado por defecto
    }

    # Insertar en la base de datos
    result = db_client.local.rooms.insert_one(new_room)

    if not result.acknowledged:
        raise APIResponse(
            code=500,
            status="error",
            message="Failed to create room",
            data=None
        )

    return APIResponse(
        code=201,
        status="success",
        message="Room created successfully",
        data={"id": str(result.inserted_id)}
    )
