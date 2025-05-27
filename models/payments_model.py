from datetime import datetime
from typing import Literal
from pydantic import BaseModel

from models.common import FlexibleModel, MongoIdModel


class Payment(MongoIdModel):
    """
    Representa un pago en el sistema.

    Atributos:
        reservation_id (FlexibleModel): Identificador de la reserva asociada al pago.
        amount (float): Monto del pago realizado.
        method (Literal["Debit Card", "PSE", "Cash"]): Método de pago utilizado.
        status (Literal["Pending", "Completed", "Failed"]): Estado actual del pago.
        created_at (datetime): Fecha y hora en que se realizó el pago.

    """
    reservation_id: FlexibleModel
    amount: float
    method: Literal["Debit Card", "PSE", "Cash"]
    status: Literal["Pending", "Completed", "Failed"]
    created_at: datetime


class PaymentCreate(BaseModel):
    """
    PaymentCreate es un modelo Pydantic que representa los datos requeridos para crear un nuevo pago.
    Atributos:
        reservation_id (str): El identificador único de la reserva asociada al pago.
        amount (float): El monto a pagar.
        method (Literal["Debit Card", "PSE", "Cash"]): El método de pago utilizado. Debe ser uno de "Debit Card", "PSE" o "Cash".
    """

    reservation_id: str
    amount: float
    method: Literal["Debit Card", "PSE", "Cash"]
