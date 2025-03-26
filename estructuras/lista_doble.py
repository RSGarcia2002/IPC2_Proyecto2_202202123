# estructuras/lista_doble.py

class NodoDoble:
    def __init__(self, dato):
        self.dato = dato
        self.anterior = None
        self.siguiente = None

class ListaDoble:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self._size = 0

    def esta_vacia(self):
        return self.primero is None

    def agregar_final(self, dato):
        nuevo = NodoDoble(dato)
        if self.esta_vacia():
            self.primero = self.ultimo = nuevo
        else:
            self.ultimo.siguiente = nuevo
            nuevo.anterior = self.ultimo
            self.ultimo = nuevo
        self._size += 1

    def eliminar(self, dato):
        actual = self.primero
        while actual:
            if actual.dato == dato:
                if actual.anterior:
                    actual.anterior.siguiente = actual.siguiente
                else:
                    self.primero = actual.siguiente
                if actual.siguiente:
                    actual.siguiente.anterior = actual.anterior
                else:
                    self.ultimo = actual.anterior
                self._size -= 1
                return True
            actual = actual.siguiente
        return False

    def recorrer_adelante(self):
        actual = self.primero
        elementos = []
        while actual:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos

    def recorrer_atras(self):
        actual = self.ultimo
        elementos = []
        while actual:
            elementos.append(actual.dato)
            actual = actual.anterior
        return elementos

    def tamano(self):
        return self._size
    
    def buscar(self, condicion):
        actual = self.primero
        while actual:
            if condicion(actual.dato):
                return actual.dato
            actual = actual.siguiente
        return None
