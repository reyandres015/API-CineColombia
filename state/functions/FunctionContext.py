from state.functions.FunctionState import FunctionState


class FunctionContext:
    """
    Clase FunctionContext

    Esta clase actúa como el contexto para el patrón de diseño State, permitiendo cambiar el comportamiento de un objeto cuando su estado interno cambia.

    Atributos:
        state (FunctionState): El estado actual del contexto, que define el comportamiento de las operaciones.

    Métodos:
        start(): Llama al método start del estado actual, pasando el contexto.
        finish(): Llama al método finish del estado actual, pasando el contexto.
        cancel(): Llama al método cancel del estado actual, pasando el contexto.
    """

    def __init__(self, state: FunctionState):
        self.state = state

    def start(self):
        self.state.start(self)

    def finish(self):
        self.state.finish(self)

    def cancel(self):
        self.state.cancel(self)
