"""Configuración central del registro de eventos y errores."""

import logging
from pathlib import Path


class EventLogger:
    """Escribe los eventos del programa en un archivo de texto.

    Si no se indica una ruta, el archivo queda dentro de logs/ en la raíz del
    proyecto. La clase ofrece métodos pequeños para que las otras capas no
    dependan directamente de la configuración de logging.
    """

    def __init__(self, file_path=None):
        # La carpeta se crea automáticamente si todavía no existe.
        default_path = Path(__file__).resolve().parent.parent / "logs" / "software_fj.log"
        self.file_path = Path(file_path) if file_path else default_path
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        self._logger = logging.getLogger("SoftwareFJ")
        self._logger.setLevel(logging.INFO)
        self._logger.propagate = False

        # Se evita agregar varios manejadores si se crea más de una instancia.
        # De otro modo, cada evento podría escribirse varias veces en el mismo
        # archivo durante una única ejecución.
        if not self._logger.handlers:
            handler = logging.FileHandler(self.file_path, encoding="utf-8")
            handler.setFormatter(logging.Formatter(
                "%(asctime)s | %(levelname)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            ))
            self._logger.addHandler(handler)

    def info(self, message):
        """Registra una operación normal."""
        self._logger.info(message)

    def warning(self, message):
        """Registra una situación que requiere atención."""
        self._logger.warning(message)

    def error(self, message, exception=None):
        """Registra el mensaje y, si existe, la información de la excepción."""
        if exception:
            self._logger.exception("%s: %s", message, exception)
        else:
            self._logger.error(message)
