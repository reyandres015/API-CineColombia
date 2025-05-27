from fastapi import HTTPException
from chain_of_responsability.Validator import Validator
from db.functions_db import get_precio_function
from db.reservation_db import guardar_reserva
from models.common import APIResponse


class ReservationValidatorCreate(Validator):
    def validar(self, solicitud):
        precio = get_precio_function(solicitud.function_id)
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
