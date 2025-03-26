# modelos/transaccion.py

class Transaccion:
    def __init__(self, id_transaccion, nombre, tiempo):
        self.id = id_transaccion
        self.nombre = nombre
        self.tiempo = tiempo  # Tiempo de atención en minutos

    def __str__(self):
        return f"{self.nombre} ({self.tiempo} min)"
