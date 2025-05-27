class FunctionState:
    """
    Clase base abstracta para representar el estado de una función en un contexto determinado.

    Métodos:
        start(context): Inicia la función en el contexto dado. Debe ser implementado por las subclases.
        finish(context): Finaliza la función en el contexto dado. Debe ser implementado por las subclases.
        cancel(context): Cancela la función en el contexto dado. Debe ser implementado por las subclases.
    """

    def start(self, context):
        raise NotImplementedError

    def finish(self, context):
        raise NotImplementedError

    def cancel(self, context):
        raise NotImplementedError
