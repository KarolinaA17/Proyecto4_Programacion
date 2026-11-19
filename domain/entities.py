"""Definición de la entidad general del sistema."""

from abc import ABC, abstractmethod
from datetime import datetime
from uuid import uuid4


class BaseEntity(ABC):
    """Base abstracta de los objetos identificables del dominio.

    Las clases concretas heredan el identificador y la fecha de creación, y
    deben implementar get_summary para definir cómo se muestran.
    """

    def __init__(self):
        # Se toma un prefijo de UUID para que el identificador sea fácil de
        # mostrar; al acortarlo, una colisión es posible aunque poco probable
        # para el volumen de registros esperado en esta aplicación.
        self._entity_id = str(uuid4())[:8].upper()
        self._created_at = datetime.now()

    @property
    def entity_id(self):
        """Permite consultar el identificador sin modificarlo directamente."""
        return self._entity_id

    @property
    def created_at(self):
        """Devuelve la fecha de creación de la entidad."""
        return self._created_at

    @abstractmethod
    def get_summary(self):
        """Obliga a las clases hijas a definir un resumen propio."""
        raise NotImplementedError
