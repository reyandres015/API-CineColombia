from fastapi import APIRouter

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
