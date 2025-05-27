from abc import ABC, abstractmethod

# Clase base para los validadores


class Validator(ABC):
    def __init__(self):
        self._siguiente = None

    def establecer_siguiente(self, validador):
        self._siguiente = validador
        return validador

    def manejar(self, solicitud, resultado=None):
        # Si resultado es None, es el primer validador, así que ejecuta validar normalmente
        if resultado is None:
            resultado = self.validar(solicitud)
        else:
            # Si ya hay un resultado (por ejemplo, un ID), pásalo a los siguientes validadores si lo necesitan
            resultado = self.validar(solicitud, resultado)
        if self._siguiente:
            return self._siguiente.manejar(solicitud, resultado)
        return resultado

    @abstractmethod
    def validar(self, solicitud):
        pass
