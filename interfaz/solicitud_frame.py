import tkinter as tk
from tkinter import ttk, messagebox
from modelos.cliente import Cliente

class FrameSolicitud(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.lista_empresas = master.lista_empresas
        self._crear_componentes()

    def _crear_componentes(self):
        tk.Label(self, text="Solicitud de Atención", font=("Arial", 16)).pack(pady=10)

        tk.Label(self, text="Empresa:").pack()
        self.combo_empresa = ttk.Combobox(self, state="readonly")
        self.combo_empresa.pack()
        self.combo_empresa.bind("<<ComboboxSelected>>", self.cargar_puntos)

        tk.Label(self, text="Punto de atención:").pack()
        self.combo_punto = ttk.Combobox(self, state="readonly")
        self.combo_punto.pack()
        self.combo_punto.bind("<<ComboboxSelected>>", self.cargar_transacciones)

        tk.Label(self, text="DPI del cliente:").pack()
        self.entry_dpi = tk.Entry(self)
        self.entry_dpi.pack()

        tk.Label(self, text="Nombre del cliente:").pack()
        self.entry_nombre = tk.Entry(self)
        self.entry_nombre.pack()

        # Área scrollable para transacciones
        frame_scroll = tk.Frame(self)
        frame_scroll.pack(pady=10, fill="both", expand=True)

        self.canvas = tk.Canvas(frame_scroll, height=200)
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_scroll, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.inner_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.transacciones_widgets = []

        btn_enviar = tk.Button(self, text="Solicitar Atención", command=self.enviar_solicitud)
        btn_enviar.pack(pady=10)

        self.label_resultado = tk.Label(self, text="", font=("Arial", 12), fg="blue", wraplength=500, justify="center")
        self.label_resultado.pack()

        self.cargar_empresas()

    def cargar_empresas(self):
        empresas = self.lista_empresas.recorrer()
        self.combo_empresa["values"] = [e.nombre for e in empresas]
        self.empresas_dict = {e.nombre: e for e in empresas}

    def cargar_puntos(self, event=None):
        nombre_empresa = self.combo_empresa.get()
        empresa = self.empresas_dict.get(nombre_empresa)
        if empresa:
            puntos = empresa.puntos.recorrer()
            self.combo_punto["values"] = [p.nombre for p in puntos]
            self.puntos_dict = {p.nombre: p for p in puntos}
            self.combo_punto.set("")

    def cargar_transacciones(self, event=None):
        for widget in self.inner_frame.winfo_children():
            widget.destroy()
        self.transacciones_widgets.clear()

        nombre_empresa = self.combo_empresa.get()
        empresa = self.empresas_dict.get(nombre_empresa)
        if not empresa:
            return

        transacciones = empresa.transacciones.recorrer()

        for t in transacciones:
            var = tk.IntVar()
            chk = tk.Checkbutton(self.inner_frame, text=t.nombre, variable=var)
            chk.grid(sticky="w", padx=5, pady=2)

            entry = tk.Entry(self.inner_frame, width=5)
            entry.grid(row=self.inner_frame.grid_size()[1] - 1, column=1, padx=5)

            self.transacciones_widgets.append((t, var, entry))

    def enviar_solicitud(self):
        nombre = self.entry_nombre.get().strip()
        dpi = self.entry_dpi.get().strip()
        punto_nombre = self.combo_punto.get()
        punto = self.puntos_dict.get(punto_nombre)

        if not nombre or not dpi or not punto:
            messagebox.showerror("Error", "Completa todos los campos")
            return

        cliente = Cliente(dpi, nombre)
        total = 0

        for trans, var, entry in self.transacciones_widgets:
            if var.get():
                try:
                    cantidad = int(entry.get())
                    cliente.agregar_transaccion(trans, cantidad)
                    total += trans.tiempo * cantidad
                except ValueError:
                    messagebox.showerror("Error", f"Cantidad inválida para '{trans.nombre}'")
                    return

        if total == 0:
            messagebox.showwarning("Advertencia", "Debe seleccionar al menos una transacción.")
            return

        cliente.tiempo_espera = punto.cola_espera.tamano() * total
        punto.agregar_cliente(cliente)

        self.label_resultado.config(
            text=f"Solicitud registrada\nTiempo estimado: {cliente.tiempo_espera} min"
        )
