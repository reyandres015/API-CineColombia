from fastapi import APIRouter
import datetime

from dependencies.database import db_client
from models.common import APIResponse
from models.movie_model import MovieCreate

router = APIRouter()


@router.post("/create")
def create_movie(movie_data: MovieCreate):
    """
    Endpoint para crear una nueva película en la base de datos.

    Este endpoint recibe los datos de una película, determina su estado según la fecha de estreno,
    y la inserta en la base de datos MongoDB. Si la inserción falla, retorna un error.

    Args:
        movie_data (MovieCreate): Objeto con los datos de la película a crear.

    Returns:
        APIResponse: Respuesta con el ID de la película creada o un mensaje de error.
    """
    # Determinar el estado de la película según la fecha de estreno
    status = "Por Estrenar" if movie_data.estreno > datetime.date.today() else "Estrenada"

    # Construir el documento de la nueva película
    new_movie = {
        "nombre": movie_data.nombre,
        "genero": movie_data.genero,
        "anio": movie_data.anio,
        "director": movie_data.director,
        "duracion": movie_data.duracion,
        "idioma": movie_data.idioma,
        "sinopsis": movie_data.sinopsis,
        "status": status,
        # Convertir la fecha de estreno a datetime.datetime para MongoDB
        "estreno": datetime.datetime.combine(movie_data.estreno, datetime.time()),
    }

    # Insertar la película en la base de datos
    result = db_client.local.movies.insert_one(new_movie)

    # Verificar si la inserción fue exitosa
    if not result.acknowledged:
        raise APIResponse(
            code=500,
            status="error",
            message="Failed to create movie",
            data=None
        )

    # Retornar respuesta exitosa con el ID de la película creada
    return APIResponse(
        code=201,
        status="success",
        message="Movie created successfully",
        data={"id": str(result.inserted_id)}
    )
