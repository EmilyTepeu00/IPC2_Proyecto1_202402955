from nodo import Nodo

class ListaEnlazada:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self._tamaño = 0

    def estaVacia(self):
        return self.primero is None
    
    def agregar(self, dato):
        nuevo_nodo = Nodo(dato) #Agrega un nuevo elemento a la lista

        if self.primero is None:
            #El nodo sera el primero y el ultimo
            self.primero = nuevo_nodo
            self.ultimo = nuevo_nodo

        else: #Lista no vacia - agrega despues del ultimo
            self.ultimo.siguiente = nuevo_nodo
            self.ultimo = nuevo_nodo

        self._tamaño += 1

    def tamaño(self):
        return self._tamaño
    
    def __iter__(self):
        #Lista iterable
        actual = self.primero
        while actual is not None:
            yield actual.dato #yield -> permite iteracion perezosa
            actual = actual.siguiente

    #Buscar elemento que cumpla con el predicado
    def buscar(self, predicado):
        actual = self.primero
        while actual is not None:
            if predicado(actual.dato):
                return actual.dato #dato encontrado
            actual = actual.siguiente
        return None
    
    #Eliminar elementos de la lista
    def limpiar(self):
        self.primero = None
        self.ultimo = None
        self._tamaño = 0

    def __str__(self):
        elementos = []
        actual = self.primero
        while actual:
            elementos.append(str(actual.dato))
            actual = actual.siguiente
        return " -> ".join(elementos) if elementos else "Lista vacia"

