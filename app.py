"""Punto de entrada de Software FJ."""

from infrastructure.event_logger import EventLogger
from application.system_manager import SystemManager
from ui.main_window import SoftwareFJWindow


def main():
    """Prepara los componentes principales e inicia la interfaz gráfica."""
    # La interfaz no crea ni conoce directamente los detalles del logger:
    # el gestor recibe esa dependencia y la comparte con las operaciones.
    logger = EventLogger()
    manager = SystemManager(logger)

    # Se cargan servicios de ejemplo para que el sistema pueda utilizarse
    # desde el primer inicio, sin necesitar una base de datos.
    manager.load_default_services()

    # La ventana solo presenta los datos y delega las reglas al gestor.
    window = SoftwareFJWindow(manager)
    window.run()


if __name__ == "__main__":
    main()
