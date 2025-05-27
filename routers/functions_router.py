from fastapi import APIRouter, HTTPException

from db.functions_db import cambiar_estado_function
from models.common import APIResponse
from models.functions_model import FunctionCreate
from template_method.Functions.CreatFuncion import CrearFuncionEstandar

router = APIRouter()


@router.post("/create/")
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

    creator = CrearFuncionEstandar()
    function_id = creator.crear_funcion(function_data)

    return APIResponse(
        code=201,
        status="success",
        message="Function created successfully",
        data={"function_id": function_id}
    )


@router.post("/functions/{function_id}/start")
def start_function(function_id: str):
    """
    Inicia una función específica.

    Args:
        function_id (str): ID de la función a iniciar.

    Returns:
        APIResponse: Respuesta indicando el éxito o error al iniciar la función.
    """
    response = cambiar_estado_function(function_id, "start")
    if not response:
        raise HTTPException(
            status_code=404,
            detail=dict(APIResponse(
                code=404,
                status="error",
                message="No fue posible iniciar la función",
                data=None
            ))
        )

    return APIResponse(
        code=200,
        status="success",
        message=response.get("message", "Function started successfully"),
        data={"function_id": function_id}
    )


@router.post("/functions/{function_id}/cancel")
def cancel_function(function_id: str):
    """
    Cancela una función específica.

    Args:
        function_id (str): ID de la función a cancelar.

    Returns:
        APIResponse: Respuesta indicando el éxito o error al cancelar la función.
    """
    response = cambiar_estado_function(function_id, "cancel")
    if not response:
        raise HTTPException(
            status_code=404,
            detail=dict(APIResponse(
                code=404,
                status="error",
                message="No fue posible cancelar la función",
                data=None
            ))
        )

    return APIResponse(
        code=200,
        status="success",
        message=response.get("message", "Function cancelled successfully"),
        data={"function_id": function_id}
    )


@router.post("/functions/{function_id}/finish")
def finish_function(function_id: str):
    """
    Finaliza una función específica.

    Args:
        function_id (str): ID de la función a finalizar.

    Returns:
        APIResponse: Respuesta indicando el éxito o error al finalizar la función.
    """
    response = cambiar_estado_function(function_id, "finish")
    if not response:
        raise HTTPException(
            status_code=404,
            detail=dict(APIResponse(
                code=404,
                status="error",
                message="No fue posible finalizar la función",
                data=None
            ))
        )

    return APIResponse(
        code=200,
        status="success",
        message=response.get("message", "Function finished successfully"),
        data={"function_id": function_id}
    )
