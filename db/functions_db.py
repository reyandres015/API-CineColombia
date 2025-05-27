from fastapi import HTTPException
from dependencies.database import db_client
from bson import ObjectId

from state.functions.FunctionContext import FunctionContext
from state.functions.ConcreteState import CanceladaState, EnCursoState, EnVentaState, FinalizadaState
import re


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


def cambiar_estado_function(function_id, accion):
    """
    Cambia el estado de una función de cine según la acción indicada.

    Args:
        function_id (str): ID de la función.
        accion (str): Acción a realizar: 'start', 'finish', 'cancel'.

    Returns:
        dict: Mensaje con el nuevo estado.
    """
    # Obtener la función desde la base de datos
    function_data = db_client.local.functions.find_one(
        {"_id": ObjectId(function_id)}, {"status": 1})
    if not function_data:
        raise HTTPException(status_code=404, detail="Función no encontrada")

    # Mapear el estado actual a la clase correspondiente
    state_mapping = {
        "En Venta": EnVentaState(),
        "En Curso": EnCursoState(),
        "Finalizada": FinalizadaState(),
        "Cancelada": CanceladaState()
    }

    current_state = state_mapping.get(function_data["status"])
    if not current_state:
        raise HTTPException(status_code=400, detail="Estado inválido")

    # Crear el contexto y ejecutar la acción
    context = FunctionContext(current_state)
    if accion == "start":
        context.start()
    elif accion == "finish":
        context.finish()
    elif accion == "cancel":
        context.cancel()
    else:
        raise HTTPException(status_code=400, detail="Acción inválida")

    # Obtener el nombre del nuevo estado y separarlo
    new_status = type(context.state).__name__.replace("State", "")
    new_status = re.sub(r'([a-z])([A-Z])', r'\1 \2', new_status)

    db_client.local.functions.update_one(
        {"_id": ObjectId(function_id)},
        {"$set": {"status": new_status}}
    )

    return {"message": f"Función {function_id} {accion}ada. Nuevo estado: {new_status}"}
