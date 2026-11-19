# Software FJ

Sistema de escritorio para gestionar clientes, servicios y reservas. Proyecto académico desarrollado en Python con programación orientada a objetos y Tkinter.

## Requisitos

- Python 3.10 o superior.
- Tkinter (normalmente viene incluido con Python).
- No requiere instalar paquetes externos.
- No utiliza bases de datos.

## Ejecución

Desde la carpeta principal del proyecto:

```bash
python app.py
```

En algunos equipos Windows también puede utilizarse:

```bash
py app.py
```

## Organización

```text
Software_FJ/
├── app.py
├── application/
│   └── system_manager.py
├── domain/
│   ├── entities.py
│   ├── clients.py
│   ├── services.py
│   └── reservations.py
├── infrastructure/
│   ├── exceptions.py
│   └── event_logger.py
├── ui/
│   └── main_window.py
├── tests/
│   └── scenarios.py
└── logs/
```

## Responsabilidad de los módulos

- `domain`: contiene las entidades y reglas del negocio.
- `application`: coordina las operaciones y mantiene las listas en memoria.
- `infrastructure`: define las excepciones y el registro de eventos.
- `ui`: contiene exclusivamente la interfaz gráfica.
- `tests`: ejecuta escenarios de demostración.
- `app.py`: conecta los componentes e inicia el programa.

## Funcionalidades

1. Registrar clientes con validación de nombre, correo y teléfono.
2. Consultar el catálogo de servicios.
3. Crear reservas asociadas a un cliente y un servicio.
4. Calcular costos con impuestos y descuentos.
5. Confirmar y cancelar reservas.
6. Registrar eventos y errores en `logs/software_fj.log`.
7. Ejecutar escenarios correctos e incorrectos desde el botón de demostración.

## Conceptos de programación orientada a objetos

- **Abstracción:** `BaseEntity` y `BaseService` definen contratos comunes.
- **Herencia:** `Client`, los tres servicios especializados y `Reservation` reutilizan la entidad base cuando corresponde.
- **Encapsulación:** los datos personales del cliente se almacenan en atributos privados y se consultan mediante propiedades.
- **Polimorfismo:** cada servicio implementa su propia descripción, validación y cálculo.
- **Excepciones:** se utilizan excepciones personalizadas y bloques de control para evitar que un error esperado cierre la aplicación.

## Almacenamiento

Los clientes, servicios y reservas se conservan en listas mientras la aplicación está abierta. No se guardan como información permanente. El único archivo que se genera para escritura es el registro de eventos y errores.

## Nota para la sustentación

La demostración ejecuta escenarios de prueba sobre el gestor en memoria. Para observarlos, abre la aplicación y selecciona **Ejecutar demostración**. Los detalles técnicos quedan registrados en el archivo de log.
