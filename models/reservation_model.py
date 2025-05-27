from typing import Literal
from pydantic import BaseModel

from models.common import FlexibleModel, MongoIdModel


class Reservation(MongoIdModel):
    """
    Representa una reserva realizada por un usuario para una función o evento específico.

    Atributos:
        function_id (FlexibleModel): Referencia a la función o evento reservado.
        pago_id (FlexibleModel): Referencia al pago asociado con la reserva.
        cantidad_personas (int): Número de personas incluidas en la reserva.
        status (Literal["En Proceso", "Confirmada", "Cancelada"]): Estado actual de la reserva.
            Por defecto es "En Proceso".
    """
    function_id: FlexibleModel
    pago_id: FlexibleModel
    cantidad_personas: int
    precio: float

    status: Literal["En Proceso", "Confirmada", "Cancelada"] = "En Proceso"


class ReservationCreate(BaseModel):
    """
    Modelo de datos para la creación de una reserva.

    Atributos:
        function_id (str): Identificador de la función para la cual se realiza la reserva.
        cantidad_personas (int): Número de personas incluidas en la reserva.
    """
    function_id: str
    cantidad_personas: int
