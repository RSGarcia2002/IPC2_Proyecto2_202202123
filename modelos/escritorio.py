class Escritorio:
    def __init__(self, id_escritorio, identificacion, encargado):
        self.id = id_escritorio
        self.identificacion = identificacion
        self.encargado = encargado
        self.activo = False
        self.cliente_actual = None
        self.tiempo_restante = 0

        # Estadísticas
        self.clientes_atendidos = 0
        self.total_tiempo = 0
        self.max_tiempo = 0
        self.min_tiempo = float('inf')

        self.ultimo_cliente = None
        self.ultimo_tiempo = 0

    def activar(self):
        self.activo = True

    def desactivar(self):
        self.activo = False

    def asignar_cliente(self, cliente):
        self.cliente_actual = cliente
        self.tiempo_restante = cliente.calcular_tiempo_total()

    def atender(self):
        if self.cliente_actual:
            self.tiempo_restante -= 1
            self.cliente_actual.tiempo_espera += 1

            if self.tiempo_restante <= 0:
                tiempo = self.cliente_actual.calcular_tiempo_total()

                # Estadísticas
                self.total_tiempo += tiempo
                self.max_tiempo = max(self.max_tiempo, tiempo)
                self.min_tiempo = min(self.min_tiempo, tiempo)
                self.clientes_atendidos += 1

                # Guardar referencia para estadísticas externas
                self.ultimo_cliente = self.cliente_actual
                self.ultimo_tiempo = tiempo

                self.cliente_actual = None

    def promedio_atencion(self):
        if self.clientes_atendidos == 0:
            return 0
        return self.total_tiempo / self.clientes_atendidos
