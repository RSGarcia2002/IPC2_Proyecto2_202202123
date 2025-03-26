# modelos/empresa.py

from estructuras.lista_simple import ListaSimple
from modelos.transaccion import Transaccion

class Empresa:
    def __init__(self, id_empresa, nombre, abreviatura):
        self.id = id_empresa
        self.nombre = nombre
        self.abreviatura = abreviatura

        self.puntos = ListaSimple()
        self.transacciones = ListaSimple()

    def agregar_punto(self, punto):
        self.puntos.agregar(punto)

    def agregar_transaccion(self, transaccion):
        self.transacciones.agregar(transaccion)

    def obtener_transaccion(self, id_transaccion):
        return self.transacciones.buscar(lambda t: t.id == id_transaccion)

    def obtener_punto(self, id_punto):
        return self.puntos.buscar(lambda p: p.id == id_punto)

    def __str__(self):
        return f"{self.nombre} ({self.abreviatura})"
