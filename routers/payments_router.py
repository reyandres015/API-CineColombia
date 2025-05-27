from fastapi import APIRouter
from datetime import datetime
from bson import ObjectId

from dependencies.database import db_client
from models.common import APIResponse
from models.payments_model import PaymentCreate


router = APIRouter()


# Crear un nuevo pago
@router.post("/create")
def create_payment(payment_data: PaymentCreate):
    """
    Endpoint para crear un nuevo pago.

    Este endpoint valida que la reservación asociada exista, crea un nuevo documento de pago en la base de datos,
    y actualiza el estado de la reservación a "Completed" si el pago se realiza correctamente.

    Args:
        payment_data (PaymentCreate): Objeto con los datos necesarios para crear el pago.

    Returns:
        APIResponse: Respuesta con el ID del pago creado o un mensaje de error.
    """
    # Validar que la reservación exista
    reservation = db_client.local.reservations.find_one(
        {"_id": ObjectId(payment_data.reservation_id)}, {"_id": 1}
    )
    if not reservation:
        raise APIResponse(
            code=404,
            status="error",
            message="Reservación no encontrada"
        )

    # Crear el documento de pago
    new_payment = {
        "reservation_id": ObjectId(payment_data.reservation_id),
        "amount": payment_data.amount,
        "method": payment_data.method,
        "status": "Completed",  # El estado inicial del pago es "Completed"
        "created_at": datetime.now()
    }

    # Insertar el pago en la base de datos
    result = db_client.local.payments.insert_one(new_payment)
    if not result.acknowledged:
        raise APIResponse(
            code=500,
            status="error",
            message="Error al crear el pago"
        )

    # Actualizar el estado de la reservación asociada al pago
    db_client.local.reservations.update_one(
        {"_id": ObjectId(payment_data.reservation_id)},
        {"$set": {"status": "Completed"}}
    )

    # Retornar respuesta exitosa con el ID del pago creado
    return APIResponse(
        code=201,
        status="success",
        message="Pago creado exitosamente",
        data={"payment_id": str(result.inserted_id)}
    )
