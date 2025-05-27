from dependencies.database import db_client
from bson import ObjectId

from visitor.reservation.ReservaBase import Reserva
from visitor.reservation.VisitorReserva import PromoPorcentajeVisitor


def exists_reservation(reservation_id):
    # Verificar que la reservacion existe.
    return db_client.local.reservations.find_one(
        {
            "_id": ObjectId(reservation_id),
            "status": "En Proceso"
        },
        {"_id": 1}
    ) is not None


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


def get_precio_reserva(reservation_id):
    # Obtener el precio de la reserva por su ID
    reservation = db_client.local.reservations.find_one(
        {"_id": ObjectId(reservation_id)},
        {"precio": 1}
    )
    if not reservation:
        return None
    return reservation.get("precio", 0)


def update_precio(reservation_id, precio):
    # Actualizar el precio de la reserva en la base de datos
    db_client.local.reservations.update_one(
        {"_id": ObjectId(reservation_id)},
        {"$set": {"precio": precio}}
    )
    return precio


def aplicar_descuento(reserva: Reserva, codigo: str):
    promo = db_client.local.promotion_codes.find_one(
        {"code": codigo.upper()}, {"_id": 0, "descuento": 1}
    )

    if not promo:
        return False
    

    visitante = PromoPorcentajeVisitor(promo["descuento"])
    return reserva.aceptar(visitante)
