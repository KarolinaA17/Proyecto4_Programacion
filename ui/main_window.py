"""Ventana principal de Software FJ construida con Tkinter."""

import tkinter as tk
from tkinter import ttk, messagebox


class SoftwareFJWindow:
    """Presenta las opciones para administrar clientes, servicios y reservas.

    Los callbacks leen los controles, llaman al SystemManager y muestran el
    resultado. Las reglas de negocio se mantienen fuera de esta clase.
    """

    def __init__(self, manager):
        self.manager = manager
        self.root = tk.Tk()
        self.root.title("Software FJ | Gestión de clientes y reservas")
        self.root.geometry("1080x680")
        self.root.minsize(900, 600)
        self._configure_style()
        self._build_layout()
        self.refresh_all()

    def _configure_style(self):
        """Define colores, fuentes y estilos comunes de los controles."""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#F3F5F8")
        style.configure("TLabel", background="#F3F5F8", foreground="#253247", font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"), foreground="#17365D")
        style.configure("Subtitle.TLabel", font=("Segoe UI", 10), foreground="#66758A")
        style.configure("TButton", font=("Segoe UI", 9, "bold"), padding=7)
        style.configure("Treeview", font=("Segoe UI", 9), rowheight=27)
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

    def _build_layout(self):
        """Construye el encabezado, las pestañas y la barra inferior."""
        header = ttk.Frame(self.root, padding=(22, 18))
        header.pack(fill="x")
        ttk.Label(header, text="SOFTWARE FJ", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text="Sistema integral de gestión de clientes, servicios y reservas",
            style="Subtitle.TLabel"
        ).pack(anchor="w", pady=(3, 0))

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=18, pady=(0, 12))

        self.clients_tab = ttk.Frame(self.notebook, padding=16)
        self.services_tab = ttk.Frame(self.notebook, padding=16)
        self.reservations_tab = ttk.Frame(self.notebook, padding=16)

        self.notebook.add(self.clients_tab, text="Clientes")
        self.notebook.add(self.services_tab, text="Servicios")
        self.notebook.add(self.reservations_tab, text="Reservas")

        self._build_clients_tab()
        self._build_services_tab()
        self._build_reservations_tab()

        footer = ttk.Frame(self.root, padding=(18, 8))
        footer.pack(fill="x")
        ttk.Button(footer, text="Actualizar información", command=self.refresh_all).pack(side="left")
        ttk.Button(footer, text="Ejecutar demostración", command=self.run_demo).pack(side="left", padx=8)
        ttk.Label(footer, text="Los datos se mantienen en memoria durante la ejecución.").pack(side="right")

    def _build_clients_tab(self):
        """Crea el formulario de registro y la tabla de clientes."""
        form = ttk.LabelFrame(self.clients_tab, text="Registrar cliente", padding=12)
        form.pack(fill="x", pady=(0, 14))

        self.name_entry = self._add_field(form, "Nombre completo", 0, 0)
        self.email_entry = self._add_field(form, "Correo electrónico", 0, 2)
        self.phone_entry = self._add_field(form, "Teléfono", 0, 4)
        ttk.Button(form, text="Registrar cliente", command=self.register_client).grid(
            row=0, column=6, padx=(14, 0), pady=5, sticky="se"
        )

        self.clients_tree = self._create_tree(
            self.clients_tab, ("id", "name", "email", "phone"),
            ("ID", "Nombre", "Correo", "Teléfono"), (100, 180, 260, 150)
        )

    def _build_services_tab(self):
        """Muestra los servicios y sus características."""
        ttk.Label(
            self.services_tab,
            text="Servicios disponibles en el catálogo",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", pady=(0, 12))
        self.services_tree = self._create_tree(
            self.services_tab, ("id", "name", "type", "rate", "description"),
            ("ID", "Servicio", "Tipo", "Tarifa por hora", "Descripción"), (90, 170, 160, 130, 350)
        )

    def _build_reservations_tab(self):
        """Crea los controles para registrar y administrar reservas."""
        form = ttk.LabelFrame(self.reservations_tab, text="Crear reserva", padding=12)
        form.pack(fill="x", pady=(0, 14))

        ttk.Label(form, text="Cliente").grid(row=0, column=0, sticky="w")
        self.client_combo = ttk.Combobox(form, state="readonly", width=28)
        self.client_combo.grid(row=1, column=0, padx=(0, 12), pady=5)

        ttk.Label(form, text="Servicio").grid(row=0, column=1, sticky="w")
        self.service_combo = ttk.Combobox(form, state="readonly", width=28)
        self.service_combo.grid(row=1, column=1, padx=(0, 12), pady=5)

        ttk.Label(form, text="Duración (horas)").grid(row=0, column=2, sticky="w")
        self.duration_entry = ttk.Entry(form, width=14)
        self.duration_entry.grid(row=1, column=2, padx=(0, 12), pady=5)

        ttk.Button(form, text="Crear reserva", command=self.create_reservation).grid(
            row=1, column=3, padx=5
        )

        actions = ttk.Frame(self.reservations_tab)
        actions.pack(fill="x", pady=(0, 8))
        ttk.Button(actions, text="Procesar y confirmar", command=self.process_selected).pack(side="left")
        ttk.Button(actions, text="Cancelar reserva", command=self.cancel_selected).pack(side="left", padx=8)

        self.reservations_tree = self._create_tree(
            self.reservations_tab, ("id", "client", "service", "duration", "status", "cost"),
            ("ID", "Cliente", "Servicio", "Horas", "Estado", "Valor"), (90, 160, 170, 70, 110, 130)
        )

    def _add_field(self, parent, label, row, column):
        """Agrega una etiqueta y un campo de texto al formulario."""
        ttk.Label(parent, text=label).grid(row=row, column=column, sticky="w", padx=(0, 8))
        entry = ttk.Entry(parent, width=19)
        entry.grid(row=row, column=column + 1, padx=(0, 12), pady=5)
        return entry

    def _create_tree(self, parent, columns, headings, widths):
        """Crea una tabla reutilizable para mostrar registros."""
        container = ttk.Frame(parent)
        container.pack(fill="both", expand=True)
        tree = ttk.Treeview(container, columns=columns, show="headings")
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        for column, heading, width in zip(columns, headings, widths):
            # El orden de estas tres secuencias debe corresponder para que
            # cada columna tenga su título y ancho adecuados.
            tree.heading(column, text=heading)
            tree.column(column, width=width, minwidth=60, anchor="w")

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        return tree

    def register_client(self):
        """Toma los datos del formulario y solicita el registro al gestor."""
        try:
            # La validación vive en Client/SystemManager; aquí solo se
            # presentan los valores y se comunican errores al usuario.
            client = self.manager.register_client(
                self.name_entry.get(), self.email_entry.get(), self.phone_entry.get()
            )
        except Exception as error:
            messagebox.showerror("No se pudo registrar", str(error))
        else:
            messagebox.showinfo("Registro exitoso", f"Cliente registrado. Código: {client.entity_id}")
            for entry in (self.name_entry, self.email_entry, self.phone_entry):
                entry.delete(0, tk.END)
            self.refresh_all()

    def create_reservation(self):
        """Valida la selección y crea una reserva."""
        try:
            # Los combos muestran "ID | nombre". Se extrae el ID porque es
            # el dato que espera el gestor para localizar cada objeto.
            client_id = self.client_combo.get().split(" | ")[0]
            service_id = self.service_combo.get().split(" | ")[0]
            # Acepta punto o coma decimal, útil para entradas en español.
            duration = float(self.duration_entry.get().replace(",", "."))
            reservation = self.manager.create_reservation(client_id, service_id, duration)
        except (ValueError, IndexError) as error:
            messagebox.showerror("Datos incompletos", "Selecciona un cliente, un servicio e indica una duración válida.")
            self.manager.logger.warning(f"Formulario de reserva incompleto: {error}")
        except Exception as error:
            messagebox.showerror("No se pudo crear la reserva", str(error))
        else:
            messagebox.showinfo("Reserva creada", f"Reserva pendiente: {reservation.entity_id}")
            self.duration_entry.delete(0, tk.END)
            self.refresh_all()

    def _selected_reservation_id(self):
        """Obtiene el identificador de la fila seleccionada."""
        selection = self.reservations_tree.selection()
        if not selection:
            raise ValueError("Selecciona una reserva de la tabla.")
        return self.reservations_tree.item(selection[0], "values")[0]

    def process_selected(self):
        """Procesa la reserva seleccionada y muestra el valor calculado."""
        try:
            reservation_id = self._selected_reservation_id()
            amount = self.manager.process_reservation(reservation_id)
        except Exception as error:
            messagebox.showerror("No se pudo procesar", str(error))
        else:
            messagebox.showinfo("Reserva confirmada", f"Total con impuesto: ${amount:,.2f}")
            self.refresh_all()

    def cancel_selected(self):
        """Cancela la reserva seleccionada."""
        try:
            reservation_id = self._selected_reservation_id()
            self.manager.cancel_reservation(reservation_id)
        except Exception as error:
            messagebox.showerror("No se pudo cancelar", str(error))
        else:
            messagebox.showinfo("Reserva cancelada", "La reserva fue cancelada correctamente.")
            self.refresh_all()

    def refresh_all(self):
        """Actualiza las tablas y las listas desplegables."""
        # Las tablas se reconstruyen a partir del estado actual del gestor;
        # no son la fuente de verdad de los registros.
        self._fill_tree(self.clients_tree, [
            (item.entity_id, item.full_name, item.email, item.phone)
            for item in self.manager.clients
        ])
        self._fill_tree(self.services_tree, [
            (
                item.entity_id,
                item.name,
                item.__class__.__name__,
                f"${item.hourly_rate:,.0f}",
                item.describe_service()
            )
            for item in self.manager.services
        ])
        self._fill_tree(self.reservations_tree, [
            (
                item.entity_id,
                item.client.full_name,
                item.service.name,
                item.duration,
                item.status,
                f"${item.total_cost:,.2f}" if item.total_cost is not None else "Sin calcular"
            )
            for item in self.manager.reservations
        ])

        self.client_combo["values"] = [
            f"{item.entity_id} | {item.full_name}" for item in self.manager.clients
        ]
        self.service_combo["values"] = [
            f"{item.entity_id} | {item.name}" for item in self.manager.services
        ]

    @staticmethod
    def _fill_tree(tree, rows):
        """Limpia una tabla y carga nuevamente sus filas."""
        # Treeview no actualiza automáticamente sus filas cuando cambian las
        # listas del gestor, por eso se eliminan y se insertan de nuevo.
        for row in tree.get_children():
            tree.delete(row)
        for values in rows:
            tree.insert("", "end", values=values)

    def run_demo(self):
        """Ejecuta los escenarios de prueba y presenta un resumen."""
        # La importación local evita cargar el módulo de demostración hasta
        # que el usuario solicite esa funcionalidad.
        from tests.scenarios import run_scenarios

        try:
            report = run_scenarios(self.manager)
        except Exception as error:
            messagebox.showerror("Error en demostración", str(error))
        else:
            messagebox.showinfo("Demostración terminada", report)
            self.refresh_all()

    def run(self):
        """Inicia el ciclo principal de Tkinter."""
        self.root.mainloop()
