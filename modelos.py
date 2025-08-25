from lista import ListaEnlazada

#Estacion base para datos de sensores
class Estacion:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre

    def __str__(self):
        return (f"Estacion({self.id}: {self.nombre})")
    
#Frecuencia de comunicacion entre sensor y estacion
class Frecuencia:
    def __init__(self, idEstacion, valor):
        self.idEstacion = idEstacion
        self.valor = valor

    def __str__(self):
        return (f"Freq({self.idEstacion}: {self.valor})")
    
#Sensor para medir las propiedades del suelo
class SensorSuelo:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        self.frecuencias = ListaEnlazada() #Lista de frecuencias a diferentes estaciones

    #Agregar una frecuencia de comunicacion con una estacion
    def agregarFrecuencia(self, idEstacion, valor):
        self.frecuencias.agregar(Frecuencia(idEstacion, valor))

    def __str__(self):
        return (f"SensorSuelo({self.id}: {self.nombre})")

#Sensor que monitorea el estado del cultivo
class SensorCultivo:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        self.frecuencias = ListaEnlazada() #Lista de frecuencias a diferentes estaciones

    #Agregar una frecuencia de comunicacion con una estacion
    def agregarFrecuencia(self, idEstacion, valor):
        self.frecuencias.agregar(Frecuencia(idEstacion, valor))

    def __str__(self):
        return (f"SensorCultivo({self.id}: {self.nombre})")
    
#Campo agricola con estciones y sensores
class CampoAgricola:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        self.estaciones = ListaEnlazada()
        self.sensores_suelo = ListaEnlazada()
        self.sensores_cultivo = ListaEnlazada()

    def __str__(self):
        return (f"Campo({self.id}: {self.nombre})")

#MATRIZ DE FRECUENCIA PARA LAS ESTACIONES Y SENSORES
class MatrizFrecuencia:
    def __init__(self, estaciones, sensores):
        self.estaciones = estaciones
        self.sensores = sensores
        self.filas = ListaEnlazada()

        #Inicializar matriz con ceros
        for _ in self.estaciones:
            fila = ListaEnlazada()
            for _ in self.sensores:
                fila.agregar(0)
            self.filas.agregar(fila)

    #Establecer valores en la matriz
    def establecerValor(self, idEstacion, idSensor, valor):
        idx_estacion = self._obtenerIndice(self.estaciones, idEstacion)
        idx_sensor = self._obtenerIndice(self.sensores, idSensor)

        if idx_estacion is not None and idx_sensor is not None:
            fila = self._obtenerElemento(self.filas, idx_estacion)
            self._establecerElemento(fila, idx_sensor, valor)

    #Obtener valores en la matriz
    def obtenerValor(self, idEstacion, idSensor):
        idx_estacion = self._obtenerIndice(self.estaciones, idEstacion)
        idx_sensor = self._obtenerIndice(self.sensores, idSensor)

        if idx_estacion is not None and idx_sensor is not None:
            fila = self._obtenerElemento(self.filas, idx_estacion)
            return self._obtenerElemento(fila, idx_sensor)
        return 0
    
    #Obtener el indice de un valor en una lista
    def _obtenerIndice(self, lista, valor):
        for i, item in enumerate(lista):
            if item == valor:
                return i
            return None
        
    #Obtener elemento por inidice de ListaEnlazada
    def _obtenerElemento(self, lista, indice):
        actual = lista.primero
        for i in range(indice):
            if actual is None:
                return None
            actual = actual.siguiente
        return actual.dato if actual else None
    
    #Establecer elemento por inidice en ListaEnlazada
    def _establecerElemento(self, lista, indice, valor):
        actual = lista.primero
        for i in range(indice):
            if actual is None:
                return
            actual = actual.siguiente
        if actual:
            actual.dato = valor

    def __str__(self):
        return (f"MatrizFrecuencia({self.estaciones.tamaño()}x{self.sensores.tamaño()})")

#REPRESENTAR MATRIZ DE PATRONES BINARIOS
class MatrizPatron:
    def __init__(self, estaciones, sensores):
        self.estaciones = estaciones
        self.sensores = sensores
        self.filas = ListaEnlazada()

        #Inicializar matriz con 0
        for _ in self.estaciones:
            fila = ListaEnlazada()
            for _ in self.sensores:
                fila.agregar(0)
            self.filas.agregar(fila)

    #Establecer patron
    def establecerPatron(self, idEstacion, idSensor, valor):
        valorBinario = 1 if valor > 0 else 0
        idx_estacion = self._obtenerIndice(self.estaciones, idEstacion)
        idx_sensor = self._obtenerIndice(self.sensores, idSensor)

        if idx_estacion is not None and idx_sensor is not None:
            fila = self._obtenerElemento(self.filas, idx_estacion)
            self._establecerElemento(fila, idx_sensor, valorBinario)

    #Retornar el patron binario de la estacion como ListaEnlazada
    def obtenerPatronEstacion(self, idEstacion):
        patron = ListaEnlazada()
        idx_estacion = self._obtenerIndice(self.estaciones, idEstacion)

        if idx_estacion is not None:
            fila = self._obtenerElemento(self.filas, idx_estacion)
            actual = fila.primero
            while actual:
                patron.agregar(actual.dato)
                actual = actual.siguiente

        return patron
    
    #Comparar patrones
    def patronesIguales(self, patron1, patron2):
        actual1 = patron1.primero
        actual2 = patron2.primero

        while actual1 and actual2:
            if actual1.dato != actual2.dato:
                return False
            actual1 = actual1.siguiente
            actual2 = actual2.siguiente

        return actual1 is None and actual2 is None
    
    def _obtenerIndice(self, lista, valor):
        for i, item in enumerate(lista):
            if item == valor:
                return i
        return None
    
    def _obtenerElemento(self, lista, indice):
        actual = lista.primero
        for i in range(indice):
            if actual is None:
                return None
            actual = actual.siguiente
        return actual.dato if actual else None
    
    def _establecerElemento(self, lista, indice, valor):
        actual = lista.primero
        for i in range(indice):
            if actual is None:
                return
            actual = actual.siguiente
        if actual:
            actual.dato = valor

    def __str__(self):
        return (f"MatrizPatron({self.estaciones.tamaño()}x{self.sensores.tamaño()})")

#GRUPO DE ESTACIONES CON EL MISMO PATRON
class GrupoEstaciones:
    def __init__(self, patron):
        self.patron = patron #ListaEnlazada con el patron
        self.estaciones = ListaEnlazada() #Lista de IDs de estaciones
        self.frecuenciasTotales = ListaEnlazada() #Lista de valores totales

    def agregarEstacion(self, idEstacion):
        self.estaciones.agregar(idEstacion)

    def __str__(self):
        estaciones_str = []
        actual = self.estaciones.primero
        while actual:
            estaciones_str.append(actual.dato)
            actual = actual.siguiente
        return (f"Grupo({self.estaciones.tamaño()} estaciones: {', '.join(estaciones_str)})")