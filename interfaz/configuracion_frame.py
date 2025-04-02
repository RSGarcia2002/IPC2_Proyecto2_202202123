import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from lector_xml import LectorXML
from estructuras.lista_simple import ListaSimple
from modelos.empresa import Empresa
from modelos.punto_atencion import PuntoAtencion
from modelos.escritorio import Escritorio
from modelos.transaccion import Transaccion

class FrameConfiguracion(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.lista_empresas = master.lista_empresas if hasattr(master, 'lista_empresas') else ListaSimple()
        master.lista_empresas = self.lista_empresas
        self._crear_componentes()

    def _crear_componentes(self):
        tk.Label(self, text="Configuración del Sistema", font=("Arial", 16)).pack(pady=10)

        btn_config = tk.Button(self, text="Cargar archivo de configuración (.xml)", width=40, command=self.cargar_config)
        btn_config.pack(pady=5)

        btn_inicial = tk.Button(self, text="Cargar archivo de inicio (.xml)", width=40, command=self.cargar_inicial)
        btn_inicial.pack(pady=5)

        btn_limpiar = tk.Button(self, text="Limpiar Sistema", width=40, command=self.limpiar_sistema, bg="#d9534f", fg="white")
        btn_limpiar.pack(pady=5)

        # --- Crear Empresa Manual ---
        frame_empresa = tk.LabelFrame(self, text="Crear Empresa Manualmente", padx=10, pady=10)
        frame_empresa.pack(pady=10, fill="x")

        tk.Label(frame_empresa, text="ID:").grid(row=0, column=0, sticky="e")
        self.entry_id = tk.Entry(frame_empresa)
        self.entry_id.grid(row=0, column=1, sticky="w")

        tk.Label(frame_empresa, text="Nombre:").grid(row=1, column=0, sticky="e")
        self.entry_nombre = tk.Entry(frame_empresa)
        self.entry_nombre.grid(row=1, column=1, sticky="w")

        tk.Label(frame_empresa, text="Abreviatura:").grid(row=2, column=0, sticky="e")
        self.entry_abrev = tk.Entry(frame_empresa)
        self.entry_abrev.grid(row=2, column=1, sticky="w")

        btn_crear = tk.Button(frame_empresa, text="Crear Empresa", command=self.crear_empresa)
        btn_crear.grid(row=3, column=0, columnspan=2, pady=5)

        # --- Crear Punto de Atención ---
        frame_punto = tk.LabelFrame(self, text="Crear Punto de Atención Manualmente", padx=10, pady=10)
        frame_punto.pack(pady=10, fill="x")

        tk.Label(frame_punto, text="Empresa:").grid(row=0, column=0, sticky="e")
        self.combo_empresa = ttk.Combobox(frame_punto, state="readonly", width=30)
        self.combo_empresa.grid(row=0, column=1, sticky="w")

        tk.Label(frame_punto, text="ID Punto:").grid(row=1, column=0, sticky="e")
        self.entry_id_punto = tk.Entry(frame_punto)
        self.entry_id_punto.grid(row=1, column=1, sticky="w")

        tk.Label(frame_punto, text="Nombre:").grid(row=2, column=0, sticky="e")
        self.entry_nombre_punto = tk.Entry(frame_punto)
        self.entry_nombre_punto.grid(row=2, column=1, sticky="w")

        tk.Label(frame_punto, text="Dirección:").grid(row=3, column=0, sticky="e")
        self.entry_direccion_punto = tk.Entry(frame_punto)
        self.entry_direccion_punto.grid(row=3, column=1, sticky="w")

        btn_punto = tk.Button(frame_punto, text="Crear Punto", command=self.crear_punto)
        btn_punto.grid(row=4, column=0, columnspan=2, pady=5)

        # --- Crear Escritorio Manualmente ---
        frame_escritorio = tk.LabelFrame(self, text="Crear Escritorio Manualmente", padx=10, pady=10)
        frame_escritorio.pack(pady=10, fill="x")

        tk.Label(frame_escritorio, text="Empresa:").grid(row=0, column=0, sticky="e")
        self.combo_empresa_esc = ttk.Combobox(frame_escritorio, state="readonly", width=30)
        self.combo_empresa_esc.grid(row=0, column=1, sticky="w")
        self.combo_empresa_esc.bind("<<ComboboxSelected>>", self.actualizar_puntos_escritorio)

        tk.Label(frame_escritorio, text="Punto:").grid(row=1, column=0, sticky="e")
        self.combo_punto_esc = ttk.Combobox(frame_escritorio, state="readonly", width=30)
        self.combo_punto_esc.grid(row=1, column=1, sticky="w")

        tk.Label(frame_escritorio, text="ID Escritorio:").grid(row=2, column=0, sticky="e")
        self.entry_id_esc = tk.Entry(frame_escritorio)
        self.entry_id_esc.grid(row=2, column=1, sticky="w")

        tk.Label(frame_escritorio, text="Identificación:").grid(row=3, column=0, sticky="e")
        self.entry_ident_esc = tk.Entry(frame_escritorio)
        self.entry_ident_esc.grid(row=3, column=1, sticky="w")

        tk.Label(frame_escritorio, text="Encargado:").grid(row=4, column=0, sticky="e")
        self.entry_encargado_esc = tk.Entry(frame_escritorio)
        self.entry_encargado_esc.grid(row=4, column=1, sticky="w")

        btn_crear_esc = tk.Button(frame_escritorio, text="Crear Escritorio", command=self.crear_escritorio)
        btn_crear_esc.grid(row=5, column=0, columnspan=2, pady=5)

        # --- Crear Transacción Manualmente ---
        frame_trans = tk.LabelFrame(self, text="Crear Transacción Manualmente", padx=10, pady=10)
        frame_trans.pack(pady=10, fill="x")

        tk.Label(frame_trans, text="Empresa:").grid(row=0, column=0, sticky="e")
        self.combo_empresa_trans = ttk.Combobox(frame_trans, state="readonly", width=30)
        self.combo_empresa_trans.grid(row=0, column=1, sticky="w")

        tk.Label(frame_trans, text="ID Transacción:").grid(row=1, column=0, sticky="e")
        self.entry_id_trans = tk.Entry(frame_trans)
        self.entry_id_trans.grid(row=1, column=1, sticky="w")

        tk.Label(frame_trans, text="Nombre:").grid(row=2, column=0, sticky="e")
        self.entry_nombre_trans = tk.Entry(frame_trans)
        self.entry_nombre_trans.grid(row=2, column=1, sticky="w")

        tk.Label(frame_trans, text="Tiempo (min):").grid(row=3, column=0, sticky="e")
        self.entry_tiempo_trans = tk.Entry(frame_trans)
        self.entry_tiempo_trans.grid(row=3, column=1, sticky="w")

        btn_trans = tk.Button(frame_trans, text="Crear Transacción", command=self.crear_transaccion)
        btn_trans.grid(row=4, column=0, columnspan=2, pady=5)

        self.label_estado = tk.Label(self, text="", fg="green", font=("Arial", 12))
        self.label_estado.pack(pady=5)

        self.actualizar_combo_empresas()

    def cargar_config(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos XML", "*.xml")])
        if ruta:
            LectorXML.cargar_configuracion(ruta, self.lista_empresas)
            self.label_estado.config(text="Configuración cargada correctamente.")
            messagebox.showinfo("Éxito", "Archivo de configuración cargado correctamente.")
            self.actualizar_combo_empresas()

    def cargar_inicial(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos XML", "*.xml")])
        if ruta:
            LectorXML.cargar_inicial(ruta, self.lista_empresas)
            self.label_estado.config(text="Archivo de inicio cargado correctamente.")
            messagebox.showinfo("Éxito", "Archivo de inicio cargado correctamente.")
            self.actualizar_combo_empresas()

    def limpiar_sistema(self):
        self.lista_empresas.vaciar()
        self.label_estado.config(text="Sistema limpiado.")
        messagebox.showinfo("Limpieza completada", "El sistema ha sido reiniciado correctamente.")
        self.actualizar_combo_empresas()

    def crear_empresa(self):
        id_ = self.entry_id.get().strip()
        nombre = self.entry_nombre.get().strip()
        abrev = self.entry_abrev.get().strip()

        if not id_ or not nombre or not abrev:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        for e in self.lista_empresas.recorrer():
            if e.id == id_:
                messagebox.showwarning("Duplicado", "Ya existe una empresa con ese ID.")
                return

        nueva = Empresa(id_, nombre, abrev)
        self.lista_empresas.agregar_final(nueva)
        messagebox.showinfo("Éxito", f"Empresa '{nombre}' creada correctamente.")
        self.label_estado.config(text=f"Empresa '{nombre}' registrada.")
        self.entry_id.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_abrev.delete(0, tk.END)
        self.actualizar_combo_empresas()

    def crear_punto(self):
        id_punto = self.entry_id_punto.get().strip()
        nombre_punto = self.entry_nombre_punto.get().strip()
        direccion = self.entry_direccion_punto.get().strip()
        nombre_empresa = self.combo_empresa.get()

        if not id_punto or not nombre_punto or not direccion or not nombre_empresa:
            messagebox.showerror("Error", "Completa todos los campos para crear el punto.")
            return

        empresa = next((e for e in self.lista_empresas.recorrer() if e.nombre == nombre_empresa), None)
        if not empresa:
            messagebox.showerror("Error", "Empresa no encontrada.")
            return

        nuevo_punto = PuntoAtencion(id_punto, nombre_punto, direccion)
        try:
            empresa.agregar_punto(nuevo_punto)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        messagebox.showinfo("Éxito", f"Punto '{nombre_punto}' agregado a la empresa '{nombre_empresa}'.")
        self.label_estado.config(text=f"Punto '{nombre_punto}' registrado.")
        self.entry_id_punto.delete(0, tk.END)
        self.entry_nombre_punto.delete(0, tk.END)
        self.entry_direccion_punto.delete(0, tk.END)
        self.actualizar_combo_empresas()
    

    def crear_escritorio(self):
        nombre_empresa = self.combo_empresa_esc.get()
        nombre_punto = self.combo_punto_esc.get()
        id_esc = self.entry_id_esc.get().strip()
        identificacion = self.entry_ident_esc.get().strip()
        encargado = self.entry_encargado_esc.get().strip()

        if not (nombre_empresa and nombre_punto and id_esc and identificacion and encargado):
            messagebox.showerror("Error", "Completa todos los campos del escritorio.")
            return

        empresa = next((e for e in self.lista_empresas.recorrer() if e.nombre == nombre_empresa), None)
        if not empresa:
            messagebox.showerror("Error", "Empresa no encontrada.")
            return

        punto = next((p for p in empresa.puntos.recorrer() if p.nombre == nombre_punto), None)
        if not punto:
            messagebox.showerror("Error", "Punto de atención no encontrado.")
            return

        nuevo = Escritorio(id_esc, identificacion, encargado)
        punto.agregar_escritorio(nuevo)
        messagebox.showinfo("Éxito", f"Escritorio '{identificacion}' creado.")
        self.label_estado.config(text=f"Escritorio '{identificacion}' agregado.")
        self.entry_id_esc.delete(0, tk.END)
        self.entry_ident_esc.delete(0, tk.END)
        self.entry_encargado_esc.delete(0, tk.END)

    def crear_transaccion(self):
        nombre_empresa = self.combo_empresa_trans.get()
        id_trans = self.entry_id_trans.get().strip()
        nombre = self.entry_nombre_trans.get().strip()
        tiempo_str = self.entry_tiempo_trans.get().strip()

        if not (nombre_empresa and id_trans and nombre and tiempo_str):
            messagebox.showerror("Error", "Completa todos los campos de la transacción.")
            return

        try:
            tiempo = int(tiempo_str)
            if tiempo <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "El tiempo debe ser un número entero positivo.")
            return

        empresa = next((e for e in self.lista_empresas.recorrer() if e.nombre == nombre_empresa), None)
        if not empresa:
            messagebox.showerror("Error", "Empresa no encontrada.")
            return

        nueva = Transaccion(id_trans, nombre, tiempo)
        empresa.transacciones.agregar_final(nueva)
        messagebox.showinfo("Éxito", f"Transacción '{nombre}' registrada.")
        self.label_estado.config(text=f"Transacción '{nombre}' registrada.")
        self.entry_id_trans.delete(0, tk.END)
        self.entry_nombre_trans.delete(0, tk.END)
        self.entry_tiempo_trans.delete(0, tk.END)

    def actualizar_combo_empresas(self):
        empresas = self.lista_empresas.recorrer()
        nombres = [e.nombre for e in empresas]
        self.combo_empresa["values"] = nombres
        self.combo_empresa.set("")
        self.combo_empresa_esc["values"] = nombres
        self.combo_empresa_esc.set("")
        self.combo_empresa_trans["values"] = nombres
        self.combo_empresa_trans.set("")

    def actualizar_puntos_escritorio(self, event=None):
        nombre_empresa = self.combo_empresa_esc.get()
        empresa = next((e for e in self.lista_empresas.recorrer() if e.nombre == nombre_empresa), None)
        if empresa:
            puntos = empresa.puntos.recorrer()
            self.combo_punto_esc["values"] = [p.nombre for p in puntos]
            self.combo_punto_esc.set("")
