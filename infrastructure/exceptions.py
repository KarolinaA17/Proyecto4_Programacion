"""Excepciones propias utilizadas para identificar fallos del sistema."""


class SoftwareFJError(Exception):
    """Error general de la aplicación.

    Permite capturar errores propios del sistema sin confundirlos con errores
    inesperados de Python.
    """


class InvalidClientDataError(SoftwareFJError):
    """Se presenta cuando los datos de un cliente no cumplen las reglas."""


class InvalidServiceDataError(SoftwareFJError):
    """Se presenta cuando un servicio recibe datos incorrectos."""


class ServiceUnavailableError(SoftwareFJError):
    """Indica que el servicio no puede reservarse en ese momento."""


class InvalidReservationError(SoftwareFJError):
    """Indica que una operación sobre una reserva no está permitida."""


class ReservationProcessingError(SoftwareFJError):
    """Agrupa errores que ocurren durante el procesamiento de una reserva."""


class DuplicateRecordError(SoftwareFJError):
    """Evita registrar dos veces el mismo cliente o servicio."""
