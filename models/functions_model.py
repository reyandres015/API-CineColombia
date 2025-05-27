from pydantic import BaseModel
from typing import Literal
from datetime import datetime, date, time

from models.common import FlexibleModel, MongoIdModel


class Function(MongoIdModel):
    """
    Representa una función (proyección) de una película en un cine.

    Atributos:
        pelicula_id (FlexibleModel): ID de la película asociada a la función.
        sala_id (FlexibleModel): ID de la sala donde se proyecta la función.
        fecha (datetime): Fecha y hora de la función.
        precio (float): Precio de la entrada para la función.
        sillas_disponibles (int): Cantidad de sillas disponibles para la función.
        status (Literal): Estado de la función. Puede ser:
            - "En Venta": Entradas disponibles para la venta.
            - "Vendido": Entradas agotadas.
            - "En Función": La función está en curso.
            - "Finalizada": La función ha terminado.
    """
    pelicula_id: FlexibleModel
    sala_id: FlexibleModel
    fecha: datetime
    precio: float

    sillas_disponibles: int
    status: Literal["En Venta", "Vendido", "En Función",
                    "Finalizada"] = "En Venta"  # Default status is 'En Venta'


class FunctionCreate(BaseModel):
    """
    Modelo para la creación de una nueva función de cine.

    Atributos:
        pelicula_id (str): ID de la película a proyectar.
        sala_id (str): ID de la sala donde se realizará la función.
        fecha (date): Fecha de la función.
        hora (time): Hora de la función.
        precio (float): Precio de la entrada.
    """
    pelicula_id: str
    sala_id: str
    fecha: date
    hora: time
    precio: float
