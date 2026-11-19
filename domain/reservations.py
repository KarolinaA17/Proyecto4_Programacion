"""Control del ciclo de vida de una reserva."""

from datetime import datetime
from domain.entities import BaseEntity
from infrastructure.exceptions import InvalidReservationError, ReservationProcessingError


class Reservation(BaseEntity):
    """Relaciona un cliente con un servicio y controla su estado."""

    VALID_STATES = ("Pendiente", "Confirmada", "Cancelada")

    def __init__(self, client, service, duration):
        super().__init__()
        if client is None or service is None:
            raise InvalidReservationError("La reserva necesita un cliente y un servicio.")

        # La clase concreta del servicio impone sus propios límites de
        # duración y comprueba su disponibilidad antes de crear la reserva.
        service.validate_parameters(duration)
        self.client = client
        self.service = service
        self.duration = duration
        self.status = "Pendiente"
        self.total_cost = None
        self.processed_at = None

    def confirm(self):
        """Confirma una reserva que todavía está pendiente."""
        if self.status != "Pendiente":
            raise InvalidReservationError("Solo se pueden confirmar reservas pendientes.")
        # La disponibilidad se comprueba de nuevo al confirmar, ya que pudo
        # cambiar desde el momento en que se creó la reserva.
        self.service.check_availability()
        self.status = "Confirmada"
        self.processed_at = datetime.now()

    def cancel(self):
        """Cancela una reserva pendiente o confirmada."""
        if self.status == "Cancelada":
            raise InvalidReservationError("La reserva ya se encuentra cancelada.")
        self.status = "Cancelada"

    def process(self, tax_rate=0.19, discount=0):
        """Calcula el valor y confirma la reserva, registrando fallos de proceso."""
        try:
            if self.status != "Pendiente":
                raise InvalidReservationError("La reserva no está pendiente y no puede procesarse.")
            # El servicio calcula el subtotal según su tarifa; esta reserva
            # entrega los parámetros comunes de impuesto y descuento.
            self.total_cost = self.service.calculate_cost(
                self.duration, tax_rate=tax_rate, discount=discount
            )
        except Exception as error:
            # Se conserva el error original como causa para facilitar su diagnóstico.
            raise ReservationProcessingError("No fue posible procesar la reserva.") from error
        else:
            # Solo se confirma después de que el cálculo terminó sin error.
            self.confirm()
            return self.total_cost
        finally:
            # Este bloque se ejecuta tanto si el proceso termina bien como si falla.
            self.processed_at = datetime.now()

    def get_summary(self):
        """Prepara los datos principales para mostrar una reserva."""
        cost_text = f"${self.total_cost:,.2f}" if self.total_cost is not None else "Pendiente de cálculo"
        return (
            f"{self.entity_id} | {self.client.full_name} | "
            f"{self.service.name} | {self.duration} h | {self.status} | {cost_text}"
        )
