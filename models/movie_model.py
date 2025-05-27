from datetime import date
from typing import Literal
from pydantic import BaseModel

from models.common import MongoIdModel


class Movie(MongoIdModel):
    """
    Modelo que representa una película.

    Atributos:
        nombre (str): Nombre de la película.
        genero (str): Género de la película.
        anio (int): Año de lanzamiento de la película.
        director (str): Nombre del director de la película.
        duracion (int): Duración de la película en minutos.
        idioma (str): Idioma principal de la película.
        sinopsis (str): Breve descripción o resumen de la trama de la película.
        status (Literal["Por Estrenar", "Estrenada"]): Estado de la película, puede ser "Por Estrenar" o "Estrenada". Por defecto es "Estrenada".
        estreno (datetime.date): Fecha de estreno de la película en formato ISO 8601 (YYYY-MM-DD).
    """
    nombre: str
    genero: str
    anio: int
    director: str
    duracion: int  # Duración en minutos
    idioma: str
    sinopsis: str
    status: Literal["Por Estrenar", "Estrenada"] = "Estrenada"
    estreno: date  # Fecha de estreno en formato ISO 8601 (YYYY-MM-DD)


class MovieCreate(BaseModel):
    """
    Modelo Pydantic para crear una nueva entrada de película.

    Atributos:
        nombre (str): Nombre de la película.
        genero (str): Género de la película.
        anio (int): Año de lanzamiento de la película.
        director (str): Nombre del director de la película.
        duracion (int): Duración de la película en minutos.
        idioma (str): Idioma principal de la película.
        sinopsis (str): Breve descripción o sinopsis de la película.
        estreno (date): Fecha de estreno en formato ISO 8601 (YYYY-MM-DD).
    """
    nombre: str
    genero: str
    anio: int
    director: str
    duracion: int
    idioma: str
    sinopsis: str
    estreno: date
