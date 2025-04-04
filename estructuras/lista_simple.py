# estructuras/lista_simple.py

class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class ListaSimple:
    def __init__(self):
        self.primero = None
        self._size = 0

    def esta_vacia(self):
        return self.primero is None

    def agregar(self, dato):
        nuevo = Nodo(dato)
        if self.esta_vacia():
            self.primero = nuevo
        else:
            actual = self.primero
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo
        self._size += 1

    def eliminar(self, dato):
        actual = self.primero
        anterior = None
        while actual:
            if actual.dato == dato:
                if anterior:
                    anterior.siguiente = actual.siguiente
                else:
                    self.primero = actual.siguiente
                self._size -= 1
                return True
            anterior = actual
            actual = actual.siguiente
        return False

    def buscar(self, condicion):
        actual = self.primero
        while actual:
            if condicion(actual.dato):
                return actual.dato
            actual = actual.siguiente
        return None

    def recorrer(self):
        actual = self.primero
        elementos = []
        while actual:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos

    def tamano(self):
        return self._size
    
    def vaciar(self):
        self.primero = None
        self._size = 0

