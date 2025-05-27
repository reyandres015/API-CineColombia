from fastapi import APIRouter

from chain_of_responsability.ReservationValidator import ReservationValidatorCreate
from chain_of_responsability.FunctionValidator import FunctionValidatorExists, FunctionValidatorUpdate
from models.common import APIResponse
from models.reservation_model import ReservationCreate


router = APIRouter()

# Crear reserva


@router.post("/create/")
def create_reservation(solicitud: ReservationCreate):
    """
    Endpoint para crear una reserva de asientos para una función de cine.

    Valida que la función exista, esté en venta y tenga suficientes sillas disponibles.
    Si la función es válida, crea una nueva reserva y actualiza la cantidad de sillas disponibles en la función.

    Args:
        reservation_data (ReservationCreate): Objeto con los datos necesarios para crear la reserva.

    Returns:
        APIResponse: Respuesta con el ID de la reserva creada o un mensaje de error.
    """

    # Verificar que la función exista.
    validador = FunctionValidatorExists()
    # Crear reservación y actualizar cantidad de sillas disponibles en la función.
    validador.establecer_siguiente(ReservationValidatorCreate()) \
             .establecer_siguiente(FunctionValidatorUpdate())

    response = validador.manejar(solicitud)

    return APIResponse(
        code=201,
        status="success",
        message="Reserva creada exitosamente",
        data={"reservation_id": str(response)}
    )
