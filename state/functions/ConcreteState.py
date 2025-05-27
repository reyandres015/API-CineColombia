from state.functions.FunctionState import FunctionState
from fastapi import HTTPException


class EnVentaState(FunctionState):
    """
    Estado concreto que representa una función en venta dentro del patrón State.
    En este estado, es posible iniciar, finalizar o cancelar la función.
    Cada acción genera un cambio de estado en el contexto de la función."""

    def start(self, context):
        print("Iniciando función...")
        context.state = EnCursoState()

    def finish(self, context):
        raise HTTPException(
            status_code=400,
            detail="No se puede finalizar una función que aún no ha comenzado."
        )

    def cancel(self, context):
        print("Cancelando función...")
        context.state = CanceladaState()


class EnCursoState(FunctionState):
    """
    Estado concreto que representa una función en curso dentro del patrón State.
    En este estado, es posible iniciar, finalizar o cancelar la función.
    Cada acción genera un cambio de estado en el contexto de la función.
    """

    def start(self, context):
        raise HTTPException(
            status_code=400,
            detail="No se puede iniciar una función que ya está en curso."
        )

    def finish(self, context):
        print("Finalizando función...")
        context.state = FinalizadaState()

    def cancel(self, context):
        raise HTTPException(
            status_code=400,
            detail="No se puede cancelar una función en curso."
        )


class FinalizadaState(FunctionState):
    """
    Estado concreto que representa una función finalizada dentro del patrón State.
    En este estado, no es posible iniciar, finalizar ni cancelar la función.
    Cada intento de realizar estas acciones genera una excepción HTTP con un mensaje descriptivo.
    """

    def start(self, context):
        raise HTTPException(
            status_code=400,
            detail="La función ya ha finalizado."
        )

    def finish(self, context):
        raise HTTPException(
            status_code=400,
            detail="La función ya ha finalizado."
        )

    def cancel(self, context):
        raise HTTPException(
            status_code=400,
            detail="No se puede cancelar una función finalizada."
        )


class CanceladaState(FunctionState):
    """
    Estado concreto que representa una función cancelada dentro del patrón State.
    En este estado, no es posible iniciar, finalizar ni volver a cancelar la función.
    Cada intento de realizar estas acciones genera una excepción HTTP con un mensaje descriptivo.
    """

    def start(self, context):
        raise HTTPException(
            status_code=400,
            detail="No se puede iniciar una función cancelada."
        )

    def finish(self, context):
        raise HTTPException(
            status_code=400,
            detail="No se puede finalizar una función cancelada."
        )

    def cancel(self, context):
        raise HTTPException(
            status_code=400,
            detail="La función ya está cancelada."
        )
