class Cliente:
    def __init__(self, dpi, nombre):
        self.dpi = dpi
        self.nombre = nombre
        self.transacciones = []  # lista de tuplas (transacción, cantidad)
        self.tiempo_espera = 0
        self.tiempo_total = 0

    def agregar_transaccion(self, transaccion, cantidad):
        self.transacciones.append((transaccion, cantidad))

    def calcular_tiempo_total(self):
        total = 0
        for trans, cant in self.transacciones:
            total += trans.tiempo * cant
        return total
