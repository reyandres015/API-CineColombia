from dependencies.database import db_client
from bson import ObjectId


def guardar_reserva(solicitud, precio):
    # Guardar la reserva en la base de datos
    new_reservation = {
        "function_id": ObjectId(solicitud.function_id),
        "precio": precio * solicitud.cantidad_personas,
        "cantidad_personas": solicitud.cantidad_personas,
        "status": "En Proceso"
    }
    result = db_client.local.reservations.insert_one(new_reservation)
    return result.inserted_id
