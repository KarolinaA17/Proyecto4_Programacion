"""Coordina los registros y las operaciones del sistema."""

from domain.clients import Client
from domain.services import (
    RoomBookingService, EquipmentRentalService, TechnicalConsultingService
)
from domain.reservations import Reservation
from infrastructure.exceptions import DuplicateRecordError, InvalidReservationError


class SystemManager:
    """Mantiene las listas en memoria y conecta los objetos del dominio.

    La interfaz llama a este gestor en vez de modificar directamente las
    colecciones; así las comprobaciones y el registro de eventos quedan en un
    único lugar.
    """

    def __init__(self, logger):
        self.logger = logger
        self.clients = []
        self.services = []
        self.reservations = []

    def register_client(self, full_name, email, phone):
        """Valida y agrega un cliente a la lista interna."""
        try:
            # El constructor del dominio valida y normaliza los datos.
            client = Client(full_name, email, phone)
            # El correo se guarda en minúsculas en Client, por lo que la
            # comparación no distingue mayúsculas de minúsculas.
            if any(item.email == client.email for item in self.clients):
                raise DuplicateRecordError("Ya existe un cliente con ese correo.")
        except Exception as error:
            self.logger.error("Falló el registro de cliente", error)
            raise
        else:
            self.clients.append(client)
            self.logger.info(f"Cliente registrado: {client.entity_id} - {client.email}")
            return client
        finally:
            # El registro de cierre ayuda a seguir cada intento de operación.
            self.logger.info("Finalizó el intento de registro de cliente.")

    def add_service(self, service):
        """Agrega un servicio después de comprobar que no esté duplicado."""
        try:
            # Los nombres se comparan ignorando diferencias de mayúsculas.
            if any(item.name.lower() == service.name.lower() for item in self.services):
                raise DuplicateRecordError("Ya existe un servicio con ese nombre.")
        except Exception as error:
            self.logger.error("Falló el registro de servicio", error)
            raise
        else:
            self.services.append(service)
            self.logger.info(f"Servicio agregado: {service.entity_id} - {service.name}")
            return service

    def create_reservation(self, client_id, service_id, duration):
        """Busca los objetos relacionados y crea una reserva."""
        try:
            # Se usan referencias a los objetos ya registrados, no copias de
            # sus datos, para que la reserva mantenga la relación completa.
            client = self.find_client(client_id)
            service = self.find_service(service_id)
            reservation = Reservation(client, service, duration)
        except Exception as error:
            self.logger.error("No se pudo crear la reserva", error)
            raise
        else:
            self.reservations.append(reservation)
            self.logger.info(f"Reserva creada: {reservation.entity_id}")
            return reservation

    def find_client(self, client_id):
        """Busca un cliente por su identificador."""
        # Las listas son pequeñas y se mantienen en memoria; una búsqueda
        # secuencial es suficiente para este alcance académico.
        for client in self.clients:
            if client.entity_id == client_id:
                return client
        raise InvalidReservationError("No se encontró el cliente seleccionado.")

    def find_service(self, service_id):
        """Busca un servicio por su identificador."""
        for service in self.services:
            if service.entity_id == service_id:
                return service
        raise InvalidReservationError("No se encontró el servicio seleccionado.")

    def confirm_reservation(self, reservation_id):
        """Localiza y confirma una reserva."""
        try:
            reservation = self.find_reservation(reservation_id)
            reservation.confirm()
        except Exception as error:
            self.logger.error("No se pudo confirmar la reserva", error)
            raise
        else:
            self.logger.info(f"Reserva confirmada: {reservation_id}")
            return reservation

    def cancel_reservation(self, reservation_id):
        """Localiza y cancela una reserva."""
        try:
            reservation = self.find_reservation(reservation_id)
            reservation.cancel()
        except Exception as error:
            self.logger.error("No se pudo cancelar la reserva", error)
            raise
        else:
            self.logger.info(f"Reserva cancelada: {reservation_id}")
            return reservation

    def process_reservation(self, reservation_id, tax_rate=0.19, discount=0):
        """Procesa el cálculo de una reserva y registra cualquier excepción."""
        try:
            reservation = self.find_reservation(reservation_id)
            amount = reservation.process(tax_rate, discount)
        except Exception as error:
            self.logger.error("Error durante el procesamiento de la reserva", error)
            raise
        else:
            self.logger.info(f"Reserva procesada: {reservation_id} - ${amount:.2f}")
            return amount

    def find_reservation(self, reservation_id):
        """Busca una reserva por su identificador."""
        for reservation in self.reservations:
            if reservation.entity_id == reservation_id:
                return reservation
        raise InvalidReservationError("No se encontró la reserva indicada.")

    def load_default_services(self):
        """Registra servicios iniciales para facilitar la primera ejecución."""
        # Evita duplicar el catálogo cuando se llama más de una vez.
        if self.services:
            return

        # Cada instancia representa una variante concreta del servicio base
        # y define sus propias reglas de duración y descripción.
        defaults = [
            RoomBookingService("Sala Ejecutiva", "Sala equipada para reuniones", 45000, 12),
            EquipmentRentalService("Alquiler de portátil", "Equipo para trabajo y presentaciones", 18000, "Portátil", 8),
            TechnicalConsultingService("Asesoría de software", "Acompañamiento en soluciones digitales", 70000, "Desarrollo de software"),
        ]
        for service in defaults:
            self.add_service(service)
