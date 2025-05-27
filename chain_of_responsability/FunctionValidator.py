from fastapi import HTTPException

from db.functions_db import exists_funcion, update_function_seats
from chain_of_responsability.Validator import Validator
from models.common import APIResponse


class FunctionValidatorExists(Validator):
    def validar(self, solicitud):
        if not exists_funcion(solicitud.function_id, solicitud.cantidad_personas):
            raise HTTPException(
                status_code=404,
                detail=dict(APIResponse(
                    code=404,
                    status="error",
                    message="Función no encontrada, no disponible o sin asientos suficientes",
                    data=None
                ))
            )


class FunctionValidatorUpdate(Validator):
    def validar(self, solicitud, resultado=None):
        if not update_function_seats(solicitud.function_id, solicitud.cantidad_personas):
            raise HTTPException(
                status_code=500,
                detail=dict(APIResponse(
                    code=500,
                    status="error",
                    message="Error al actualizar las sillas disponibles en la función",
                    data=None
                ))
            )
        # Al final, retorna el resultado original (el ID de la reserva)
        return resultado
