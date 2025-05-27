from visitor.reservation.ReservaBase import ReservaEstandar


class PromoPorcentajeVisitor:
    def __init__(self, porcentaje: float):
        self.porcentaje = porcentaje

    def visitar_reserva_estandar(self, reserva: ReservaEstandar):
        return reserva.precio_base * (1 - self.porcentaje / 100)
