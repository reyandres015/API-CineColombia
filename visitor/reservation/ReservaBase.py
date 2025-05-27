class Reserva:
    def __init__(self, precio_base: float):
        self.precio_base = precio_base

    def aceptar(self, visitante):
        raise NotImplementedError


class ReservaEstandar(Reserva):
    def aceptar(self, visitante):
        return visitante.visitar_reserva_estandar(self)
