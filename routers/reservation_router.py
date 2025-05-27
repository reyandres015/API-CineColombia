from bson import ObjectId
from fastapi import APIRouter

from dependencies.database import db_client
from models.common import APIResponse
from models.reservation_model import ReservationCreate


router = APIRouter()

# Crear reserva


@router.post("/create")
def create_reservation(reservation_data: ReservationCreate):
    """
    Endpoint para crear una reserva de asientos para una función de cine.

    Este endpoint valida que la función exista, esté en venta y tenga suficientes sillas disponibles.
    Si la función es válida, crea una nueva reserva y actualiza la cantidad de sillas disponibles en la función.

    Args:
        reservation_data (ReservationCreate): Objeto con los datos necesarios para crear la reserva.

    Returns:
        APIResponse: Respuesta con el ID de la reserva creada o un mensaje de error.
    """
    # Verificar que la función existe, está en venta y tiene suficientes sillas disponibles
    function = db_client.local.functions.find_one(
        {
            "_id": ObjectId(reservation_data.function_id),
            "status": "En Venta",
            "sillas_disponibles": {"$gte": reservation_data.cantidad_personas}
        },
        {"_id": 1}
    )
    if not function:
        raise APIResponse(
            code=404,
            status="error",
            message="Función no encontrada o no disponible",
            data=None
        )

    # Crear la reserva
    new_reservation = {
        "function_id": function["_id"],
        "cantidad_personas": reservation_data.cantidad_personas,
        "status": "En Proceso"
    }

    result = db_client.local.reservations.insert_one(new_reservation)

    if not result.acknowledged:
        raise APIResponse(
            code=500,
            status="error",
            message="Error al crear la reserva",
            data=None
        )

    # Actualizar la función para reducir las sillas disponibles
    db_client.local.functions.update_one(
        {"_id": function["_id"]},
        {"$inc": {"sillas_disponibles": -reservation_data.cantidad_personas}}
    )

    # Retornar el ID de la reserva creada
    return APIResponse(
        code=201,
        status="success",
        message="Reserva creada exitosamente",
        data={"reservation_id": str(result.inserted_id)}
    )
