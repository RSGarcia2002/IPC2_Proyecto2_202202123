# estructuras/cola.py

class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class Cola:
    def __init__(self):
        self.frente = None
        self.final = None
        self._size = 0

    def esta_vacia(self):
        return self.frente is None

    def encolar(self, dato):
        nuevo = Nodo(dato)
        if self.esta_vacia():
            self.frente = self.final = nuevo
        else:
            self.final.siguiente = nuevo
            self.final = nuevo
        self._size += 1

    def desencolar(self):
        if self.esta_vacia():
            return None
        dato = self.frente.dato
        self.frente = self.frente.siguiente
        if self.frente is None:
            self.final = None
        self._size -= 1
        return dato

    def primero(self):
        return self.frente.dato if not self.esta_vacia() else None

    def tamano(self):
        return self._size

    def recorrer(self):
        actual = self.frente
        elementos = []
        while actual:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos
