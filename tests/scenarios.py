"""Escenarios para comprobar operaciones correctas e incorrectas."""

from domain.services import RoomBookingService


def run_scenarios(manager):
    """Ejecuta operaciones demostrativas y devuelve un resumen legible.

    Recibe el gestor existente para que los resultados puedan verse en la
    ventana y en el log. La demostración modifica sus datos en memoria.
    """
    results = []

    def record(label, action, expected_error=False):
        # Cada escenario se aísla para que un fallo no detenga los siguientes.
        # Los errores esperados se informan como resultados satisfactorios.
        try:
            action()
        except Exception as error:
            manager.logger.error(f"Escenario: {label}", error)
            if expected_error:
                results.append(f"OK - {label}: error controlado ({type(error).__name__})")
            else:
                results.append(f"FALLO - {label}: {error}")
        else:
            if expected_error:
                results.append(f"FALLO - {label}: se esperaba una excepción")
            else:
                results.append(f"OK - {label}")

    # 1. Registro de cliente válido.
    record("Registro de cliente válido",
           lambda: manager.register_client("Laura Méndez", "laura.demo@correo.com", "3001234567"))

    # 2. Correo inválido.
    record("Registro con correo inválido",
           lambda: manager.register_client("Pedro Ruiz", "correo-no-valido", "3101234567"), True)

    # 3. Teléfono inválido.
    record("Registro con teléfono inválido",
           lambda: manager.register_client("Ana Torres", "ana.demo@correo.com", "123"), True)

    # 4. Cliente duplicado.
    record("Registro de correo duplicado",
           lambda: manager.register_client("Laura Méndez", "laura.demo@correo.com", "3001234567"), True)

    # 5. Creación de un servicio adicional.
    record("Creación de servicio de sala",
           lambda: manager.add_service(RoomBookingService("Sala de capacitación", "Sala para talleres", 52000, 20)))

    # 6. Servicio con tarifa incorrecta.
    record("Creación de servicio con tarifa inválida",
           lambda: RoomBookingService("Sala inválida", "Prueba", -100, 10), True)

    # 7. Crear reserva válida.
    # Se buscan datos concretos creados por los primeros escenarios y el
    # primer servicio del catálogo para preparar las acciones posteriores.
    demo_client = next(item for item in manager.clients if item.email == "laura.demo@correo.com")
    demo_service = manager.services[0]
    created_reservation = {}

    def create_valid_reservation():
        created_reservation["item"] = manager.create_reservation(
            demo_client.entity_id, demo_service.entity_id, 2
        )

    record("Creación de reserva válida", create_valid_reservation)

    # 8. Procesar reserva.
    if "item" in created_reservation:
        record("Procesamiento y confirmación de reserva",
               lambda: manager.process_reservation(created_reservation["item"].entity_id))

    # 9. Intentar confirmar otra vez una reserva ya confirmada.
    if "item" in created_reservation:
        record("Confirmación repetida de reserva",
               lambda: manager.confirm_reservation(created_reservation["item"].entity_id), True)

    # 10. Crear reserva con duración inválida.
    record("Reserva con duración negativa",
           lambda: manager.create_reservation(demo_client.entity_id, demo_service.entity_id, -3), True)

    # 11. Cancelar una reserva pendiente.
    pending_reservation = {}

    def create_pending_reservation():
        pending_reservation["item"] = manager.create_reservation(
            demo_client.entity_id, demo_service.entity_id, 1
        )

    record("Creación de segunda reserva", create_pending_reservation)
    if "item" in pending_reservation:
        record("Cancelación de reserva pendiente",
               lambda: manager.cancel_reservation(pending_reservation["item"].entity_id))

    # 12. Intentar procesar una reserva inexistente.
    record("Procesamiento de identificador inexistente",
           lambda: manager.process_reservation("NO-EXISTE"), True)

    manager.logger.info("Finalizó la demostración de escenarios.")
    return "Resultados de la demostración:\n\n" + "\n".join(results)
