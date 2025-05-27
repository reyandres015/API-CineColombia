from fastapi import HTTPException
from dependencies.database import db_client
from bson import ObjectId


def get_precio_function(function_id):
    # Obtener el precio de la función por su ID
    function = db_client.local.functions.find_one(
        {"_id": ObjectId(function_id)},
        {"precio": 1}
    )
    if not function:
        raise HTTPException(
            status_code=404,
            detail="Función no encontrada"
        )

    return function.get("precio", 0)


def exists_funcion(function_id, cantidad_personas):
    # Verificar que la función existe, está en venta y tiene suficientes sillas disponibles
    return db_client.local.functions.find_one(
        {
            "_id": ObjectId(function_id),
            "status": "En Venta",
            "sillas_disponibles": {"$gte": cantidad_personas}
        },
        {"_id": 1}
    ) is not None


def update_function_seats(function_id, cantidad_personas):
    # Actualizar la cantidad de sillas disponibles en la función
    return db_client.local.functions.update_one(
        {"_id": ObjectId(function_id)},
        {"$inc": {"sillas_disponibles": -cantidad_personas}}
    ) is not None
