"""Servicios disponibles y sus cálculos particulares."""

from abc import abstractmethod
from domain.entities import BaseEntity
from infrastructure.exceptions import InvalidServiceDataError, ServiceUnavailableError


class BaseService(BaseEntity):
    """Base abstracta con datos y reglas compartidas por todos los servicios.

    Las clases hijas deben validar la duración, calcular el precio y describir
    las particularidades de su servicio.
    """

    def __init__(self, name, description, hourly_rate):
        super().__init__()

        if not isinstance(name, str) or not name.strip():
            raise InvalidServiceDataError("El servicio necesita un nombre.")
        if not isinstance(hourly_rate, (int, float)) or hourly_rate <= 0:
            raise InvalidServiceDataError("La tarifa debe ser un número mayor que cero.")

        self.name = name.strip()
        self.description = description.strip()
        self.hourly_rate = float(hourly_rate)
        self.is_available = True

    def _calculate_final_price(self, subtotal, tax_rate=0, discount=0):
        """Aplica impuestos y descuento a un subtotal previamente calculado."""
        if not 0 <= tax_rate <= 1:
            raise InvalidServiceDataError("El impuesto debe estar entre 0 y 1.")
        if not 0 <= discount <= 1:
            raise InvalidServiceDataError("El descuento debe estar entre 0 y 1.")

        # Primero se descuenta el subtotal y luego se aplica el impuesto al
        # resultado; las tasas se expresan como fracciones (0.19 = 19 %).
        discounted_total = subtotal * (1 - discount)
        return round(discounted_total * (1 + tax_rate), 2)

    def check_availability(self):
        """Evita reservar servicios que se encuentren deshabilitados."""
        if not self.is_available:
            raise ServiceUnavailableError(f"El servicio '{self.name}' no está disponible.")

    @abstractmethod
    def calculate_cost(self, duration, tax_rate=0, discount=0):
        """Cada servicio implementa su propia fórmula de cobro."""
        raise NotImplementedError

    @abstractmethod
    def validate_parameters(self, duration):
        """Cada servicio valida los parámetros que necesita."""
        raise NotImplementedError

    @abstractmethod
    def describe_service(self):
        """Devuelve una descripción específica del servicio."""
        raise NotImplementedError

    def get_summary(self):
        """Resumen general utilizado en la interfaz."""
        return f"{self.name} | ${self.hourly_rate:,.0f} por hora"


class RoomBookingService(BaseService):
    """Servicio de alquiler de salas por hora."""

    def __init__(self, name, description, hourly_rate, room_capacity):
        super().__init__(name, description, hourly_rate)
        if not isinstance(room_capacity, int) or room_capacity <= 0:
            raise InvalidServiceDataError("La capacidad de la sala debe ser un entero positivo.")
        self.room_capacity = room_capacity

    def validate_parameters(self, duration):
        """Valida la duración solicitada para la sala."""
        # La validación se reutiliza al crear la reserva y al calcular el
        # precio, para que ambos caminos apliquen las mismas reglas.
        if not isinstance(duration, (int, float)) or duration <= 0 or duration > 12:
            raise InvalidServiceDataError("La duración de la sala debe ser mayor que 0 y máximo 12 horas.")
        self.check_availability()

    def calculate_cost(self, duration, tax_rate=0, discount=0):
        """Calcula el alquiler de la sala según las horas reservadas."""
        self.validate_parameters(duration)
        return self._calculate_final_price(self.hourly_rate * duration, tax_rate, discount)

    def describe_service(self):
        """Describe las características de la sala."""
        return f"{self.description}. Capacidad máxima: {self.room_capacity} personas."


class EquipmentRentalService(BaseService):
    """Servicio de alquiler de equipos tecnológicos."""

    def __init__(self, name, description, hourly_rate, equipment_name, available_units):
        super().__init__(name, description, hourly_rate)
        if not isinstance(available_units, int) or available_units < 1:
            raise InvalidServiceDataError("La cantidad de equipos debe ser un entero positivo.")
        self.equipment_name = equipment_name.strip()
        self.available_units = available_units

    def validate_parameters(self, duration):
        """Comprueba la duración y la disponibilidad del equipo."""
        if not isinstance(duration, (int, float)) or duration <= 0 or duration > 24:
            raise InvalidServiceDataError("La duración del alquiler debe estar entre 0 y 24 horas.")
        self.check_availability()

    def calculate_cost(self, duration, tax_rate=0, discount=0):
        """Calcula el costo del alquiler del equipo."""
        self.validate_parameters(duration)
        return self._calculate_final_price(self.hourly_rate * duration, tax_rate, discount)

    def describe_service(self):
        """Muestra el tipo de equipo y las unidades disponibles."""
        return f"{self.description}. Equipo: {self.equipment_name}. Unidades: {self.available_units}."


class TechnicalConsultingService(BaseService):
    """Servicio de asesoría especializada."""

    def __init__(self, name, description, hourly_rate, specialty):
        super().__init__(name, description, hourly_rate)
        if not isinstance(specialty, str) or not specialty.strip():
            raise InvalidServiceDataError("La especialidad de la asesoría es obligatoria.")
        self.specialty = specialty.strip()

    def validate_parameters(self, duration):
        """Las asesorías se programan en bloques de una a ocho horas."""
        if not isinstance(duration, (int, float)) or duration < 1 or duration > 8:
            raise InvalidServiceDataError("La asesoría debe durar entre 1 y 8 horas.")
        self.check_availability()

    def calculate_cost(self, duration, tax_rate=0, discount=0):
        """Calcula el valor de la asesoría especializada."""
        self.validate_parameters(duration)
        return self._calculate_final_price(self.hourly_rate * duration, tax_rate, discount)

    def describe_service(self):
        """Devuelve la especialidad que cubre la asesoría."""
        return f"{self.description}. Especialidad: {self.specialty}."
