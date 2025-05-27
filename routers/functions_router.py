from bson import ObjectId
from fastapi import APIRouter
from dependencies.database import db_client
from datetime import datetime

from models.common import APIResponse
from models.functions_model import FunctionCreate

router = APIRouter()


@router.post("/create")
def create_function(function_data: FunctionCreate):
    """
    Crea una nueva función (proyección) de una película en una sala de cine.

    Proceso:
    1. Verifica que la película exista y obtiene su fecha de estreno.
    2. Verifica que la sala exista y esté disponible.
    3. Combina la fecha y hora proporcionadas en un solo objeto datetime.
    4. Valida que la función no sea antes del estreno de la película.
    5. Valida que la función no sea en el pasado.
    6. Inserta la función en la base de datos.
    """

    # 1. Verificar que la película exista y obtener su fecha de estreno
    pelicula = db_client.local.movies.find_one(
        {
            "_id": ObjectId(function_data.pelicula_id),
        },
        {"_id": 1, "estreno": 1}
    )
    if not pelicula:
        raise APIResponse(
            code=400,
            status="error",
            message="La película no existe",
            data=None
        )

    # 2. Verificar que la sala exista y esté disponible
    sala = db_client.local.rooms.find_one(
        {
            "_id": ObjectId(function_data.sala_id),
            "estado": {"$ne": "No Disponible"}
        },
        {"_id": 1, "capacidad": 1}
    )
    if not sala:
        raise APIResponse(
            code=400,
            status="error",
            message="Sala no encontrada o no disponible",
            data=None
        )

    # 3. Combinar fecha y hora en un solo datetime
    function_datetime = datetime.combine(
        function_data.fecha, function_data.hora)

    # 4. Validar que la función no sea antes del estreno de la película
    if pelicula["estreno"] > function_datetime.replace(tzinfo=None):
        raise APIResponse(
            code=400,
            status="error",
            message="La película aún no se ha estrenado en la fecha seleccionada",
            data=None
        )

    # 5. Validar que la función no sea en el pasado
    if function_datetime.replace(tzinfo=None) < datetime.now():
        raise APIResponse(
            code=400,
            status="error",
            message="La fecha u hora de la función no puede ser anterior a la hora actual en el día de hoy",
            data=None
        )

    # 6. Crear nueva función y guardar en la base de datos
    new_function = {
        "pelicula_id": pelicula["_id"],
        "sala_id": sala["_id"],
        "fecha": function_datetime,
        "precio": function_data.precio,
        "sillas_disponibles": sala["capacidad"],
        "status": "En Venta"
    }

    result = db_client.local.functions.insert_one(new_function)

    if not result.acknowledged:
        raise APIResponse(
            code=500,
            status="error",
            message="Failed to create function",
            data=None
        )

    return APIResponse(
        code=201,
        status="success",
        message="Function created successfully",
        data={"function_id": str(result.inserted_id)}
    )
