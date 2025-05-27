from typing import Literal
from pydantic import BaseModel

from models.common import MongoIdModel


class Room(MongoIdModel):
    """
    Clase que representa una habitación en el sistema.

    Atributos:
        numero (int): Número identificador de la habitación.
        capacidad (int): Capacidad máxima de personas que puede alojar la habitación.
        status (Literal["Disponible", "No Disponible"]): Estado actual de la habitación, puede ser "Disponible" o "No Disponible". Por defecto es "Disponible".
    """
    numero: int
    capacidad: int
    status: Literal["Disponible", "No Disponible"] = "Disponible"


class RoomCreate(BaseModel):
    """
    Modelo de datos para la creación de una habitación.

    Atributos:
        numero (int): Número identificador de la habitación.
        capacidad (int): Capacidad máxima de personas que puede alojar la habitación.
    """
    numero: int
    capacidad: int
