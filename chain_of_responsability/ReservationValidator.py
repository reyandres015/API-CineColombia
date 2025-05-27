from fastapi import HTTPException
from chain_of_responsability.Validator import Validator
from db.reservation_db import aplicar_descuento, exists_reservation, get_precio_reserva, guardar_reserva, update_precio
from models.common import APIResponse
from visitor.reservation.ReservaBase import Reserva, ReservaEstandar


class ReservationValidator(Validator):
    def validar(self, solicitud):
        if not exists_reservation(solicitud.reservation_id):
            raise HTTPException(
                status_code=404,
                detail=dict(APIResponse(
                    code=404,
                    status="error",
                    message="Reserva no encontrada o no disponible",
                    data=None
                ))
            )


class ReservationValidatorCreate(Validator):
    def validar(self, solicitud):
        precio = get_precio_reserva(solicitud.reservation_id)
        response = guardar_reserva(solicitud, precio)
        if not response:
            raise HTTPException(
                status_code=400,
                detail=dict(APIResponse(
                    code=400,
                    status="error",
                    message="No se pudo guardar la reserva: función no encontrada, no disponible o sin asientos suficientes",
                    data=None
                ))
            )
        return response


class ReservationValidatorPromotions(Validator):
    def validar(self, solicitud):
        precio = get_precio_reserva(solicitud.reservation_id)
        reserva = ReservaEstandar(precio_base=precio)
        descuento = aplicar_descuento(reserva, solicitud.codigo)
        if not descuento:
            raise HTTPException(
                status_code=404,
                detail=dict(APIResponse(
                    code=404,
                    status="error",
                    message="Código promocional no encontrado o inválido",
                    data=None
                ))
            )
        return descuento


class ReservationValidatorUpdatePrice(Validator):
    def validar(self, solicitud, precio):
        if not precio:
            raise HTTPException(
                status_code=404,
                detail=dict(APIResponse(
                    code=404,
                    status="error",
                    message="Función no encontrada",
                    data=None
                ))
            )
        precio = update_precio(solicitud, precio)
        if not precio:
            raise HTTPException(
                status_code=500,
                detail=dict(APIResponse(
                    code=500,
                    status="error",
                    message="Error al actualizar el precio de la reserva",
                    data=None
                ))
            )
        return precio
