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

