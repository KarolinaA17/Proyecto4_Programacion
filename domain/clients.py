"""Modelo y validaciones de los clientes."""

import re
from domain.entities import BaseEntity
from infrastructure.exceptions import InvalidClientDataError


class Client(BaseEntity):
    """Representa a una persona que solicita servicios de Software FJ."""

    def __init__(self, full_name, email, phone):
        super().__init__()

        # Se valida y normaliza cada dato antes de guardarlo. Al ser atributos
        # privados, el resto del programa los consulta mediante propiedades.
        self.__full_name = self._validate_name(full_name)
        self.__email = self._validate_email(email)
        self.__phone = self._validate_phone(phone)

    @staticmethod
    def _validate_name(value):
        """Comprueba que el nombre tenga contenido y caracteres permitidos."""
        if not isinstance(value, str) or len(value.strip()) < 3:
            raise InvalidClientDataError("El nombre debe tener al menos 3 caracteres.")
        if any(char.isdigit() for char in value):
            raise InvalidClientDataError("El nombre no puede contener números.")
        return value.strip().title()

    @staticmethod
    def _validate_email(value):
        """Valida una estructura básica de correo electrónico."""
        if not isinstance(value, str) or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value.strip()):
            raise InvalidClientDataError("El correo electrónico no tiene un formato válido.")
        return value.strip().lower()

    @staticmethod
    def _validate_phone(value):
        """Acepta números telefónicos de 7 a 15 dígitos."""
        # Se permite ingresar separadores (espacios, guiones, paréntesis),
        # pero el valor almacenado conserva únicamente los dígitos.
        digits = re.sub(r"\D", "", str(value))
        if not 7 <= len(digits) <= 15:
            raise InvalidClientDataError("El teléfono debe contener entre 7 y 15 dígitos.")
        return digits

    @property
    def full_name(self):
        """Nombre completo del cliente."""
        return self.__full_name

    @property
    def email(self):
        """Correo electrónico del cliente."""
        return self.__email

    @property
    def phone(self):
        """Teléfono del cliente."""
        return self.__phone

    def get_summary(self):
        """Entrega una descripción breve para listados y reportes."""
        return f"{self.full_name} | {self.email} | {self.phone}"
