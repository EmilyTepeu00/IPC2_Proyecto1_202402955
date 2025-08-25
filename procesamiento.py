from modelos import MatrizFrecuencia, MatrizPatron, GrupoEstaciones
from lista import ListaEnlazada

#MATRIZ DE FRECUENCIA PARA SENSORES DE SUELO
def construirMatrizFSuelo(campo):
    print("Construyendo la matriz de suelo...")

    #Obtener listas de IDs
    estaciones_ids = ListaEnlazada()
    sensores_ids = ListaEnlazada()

    for estacion in campo.estaciones:
        estaciones_ids.agregar(estacion.id)

    for sensor in campo.sensores_suelo:
        sensores_ids.agregar(sensor.id)

    matriz = MatrizFrecuencia(estaciones_ids, sensores_ids)

    #Para llenar la matriz con los valores de frecuencia
    for sensor in campo.sensores_suelo:
        for frecuencia in sensor.frecuencias:
            matriz.establecerValor(frecuencia.idEstacion, sensor.id, frecuencia.valor)
    
    print(f"   Matriz F[{estaciones_ids.tamaño()},{sensores_ids.tamaño()}] construida")
    return matriz

#MATRIZ DE FRECUENCIA PARA SENSORES DE CULTIVO
def construirMatrizFCultivo(campo):
    print("Construyendo la matriz de cultivo...")

    #Obtener listas de IDs
    estaciones_ids = ListaEnlazada()
    sensores_ids = ListaEnlazada()

    for estacion in campo.estaciones:
        estaciones_ids.agregar(estacion.id)

    for sensor in campo.sensores_cultivo:
        sensores_ids.agregar(sensor.id)

    matriz = MatrizFrecuencia(estaciones_ids, sensores_ids)

    #Para llenar la matriz con los valores de frecuencia
    for sensor in campo.sensores_cultivo:
        for frecuencia in sensor.frecuencias:
            matriz.establecerValor(frecuencia.idEstacion, sensor.id, frecuencia.valor)
    
    print(f"   Matriz F[{estaciones_ids.tamaño()},{sensores_ids.tamaño()}] construida")
    return matriz

#CONVERTIR MATRIZ DE FRECUNECIA EN MATRIZ DE PATRONES BINARIOS
def construirMatrizPatron(matrizFrecuencia):
    print("Construyendo matriz de patrones...")

    matriz_patron = MatrizPatron(matrizFrecuencia.estaciones, matrizFrecuencia.sensores)

    #Usar IDs de las estaciones y sensores
    actual_estacion = matrizFrecuencia.estaciones.primero
    while actual_estacion:
        idEstacion = actual_estacion.dato

        actual_sensor = matrizFrecuencia.sensores.primero
        while actual_sensor:
            idSensor = actual_sensor.dato
            valor = matrizFrecuencia.obtenerValor(idEstacion, idSensor)
            matriz_patron.establecerPatron(idEstacion, idSensor, valor)
            actual_sensor = actual_sensor.siguiente

        actual_estacion = actual_estacion.siguiente

    print("Matriz de patrones construida")
    return matriz_patron

#Agrupar estaciones con el mismo patron binarip
def agruparEstacionesPatron(matriz_patron):
    print("Agrupando estaciones por patron...")

    grupos = ListaEnlazada()

    #Recorrer todas las estaciones
    actual_estacion = matriz_patron.estaciones.primero
    while actual_estacion:
        idEstacion = actual_estacion.dato
        patron_actual = matriz_patron.obtenerPatronEstacion(idEstacion)

        #Buscar si ya existe un grupo con este patron
        grupo_existente = None
        actual_grupo = grupos.primero
        while actual_grupo:
            if matriz_patron.patronesIguales(actual_grupo.dato.patron, patron_actual):
                grupo_existente = actual_grupo.dato
                break
            actual_grupo = actual_grupo.siguiente

        if grupo_existente:
            grupo_existente.agregarEstacion(idEstacion)
        else:
            nuevo_grupo = GrupoEstaciones(patron_actual)
            nuevo_grupo.agregarEstacion(idEstacion)
            grupos.agregar(nuevo_grupo)

        actual_estacion = actual_estacion.siguiente

    print(f"Se formaron {grupos.tamaño()} grupos de estaciones")
    return grupos

# CALCULAR LAS FRECUENCIAS TOTALES 
def calcularFrecuenciasGrupo(grupo, matrizFrecuencia):
    #Inicializar frecuencias totales
    actual_sensor = matrizFrecuencia.sensores.primero
    while actual_sensor:
        grupo.frecuenciasTotales.agregar(0)
        actual_sensor = actual_sensor.siguiente

    #Suma de todas las frecuencias
    actual_estacion = grupo.estaciones.primero
    while actual_estacion:
        idEstacion = actual_estacion.dato

        idx_sensor = 0
        actual_sensor = matrizFrecuencia.sensores.primero
        while actual_sensor:
            idSensor = actual_sensor.dato
            valor = matrizFrecuencia.obtenerValor(idEstacion, idSensor)

            #Actualizar la suma total (¡CORREGIDO!)
            valor_actual = obtener_elemento_lista(grupo.frecuenciasTotales, idx_sensor)
            establecer_elemento_lista(grupo.frecuenciasTotales, idx_sensor, valor_actual + valor)

            idx_sensor += 1
            actual_sensor = actual_sensor.siguiente

        actual_estacion = actual_estacion.siguiente

#PROCESAR UN CAMPO AGRICOLA POR COMPLETO
def procesarCampo(campo):
    print(f"\nProcesando campo {campo.id}...")

    #Construir matrices de frecuencia
    matriz_f_suelo = construirMatrizFSuelo(campo)
    matriz_f_cultivo = construirMatrizFCultivo(campo)
    
    #Construir matrices de patrones
    matriz_p_suelo = construirMatrizPatron(matriz_f_suelo)
    matriz_p_cultivo = construirMatrizPatron(matriz_f_cultivo)
    
    #Agrupar estaciones
    grupos_suelo = agruparEstacionesPatron(matriz_p_suelo)
    grupos_cultivo = agruparEstacionesPatron(matriz_p_cultivo)
    
    #Calcular frecuencias totales para cada grupo
    actual_grupo = grupos_suelo.primero
    while actual_grupo:
        calcularFrecuenciasGrupo(actual_grupo.dato, matriz_f_suelo)
        actual_grupo = actual_grupo.siguiente
    
    actual_grupo = grupos_cultivo.primero
    while actual_grupo:
        calcularFrecuenciasGrupo(actual_grupo.dato, matriz_f_cultivo)
        actual_grupo = actual_grupo.siguiente
    
    print(f"Campo {campo.id} procesado con exito")
    
    return {
        'matriz_f_suelo': matriz_f_suelo,
        'matriz_f_cultivo': matriz_f_cultivo,
        'matriz_p_suelo': matriz_p_suelo,
        'matriz_p_cultivo': matriz_p_cultivo,
        'grupos_suelo': grupos_suelo,
        'grupos_cultivo': grupos_cultivo
    }

#OBTENER ELEMENTO POR INDICE DE ListaEnlazada
def obtener_elemento_lista(lista, indice):
    actual = lista.primero
    for i in range(indice):
        if actual is None:
            return None
        actual = actual.siguiente
    return actual.dato if actual else None

#ESTABLECER ELEMENTO POR INDICE DE ListaEnlazada
def establecer_elemento_lista(lista, indice, valor):
    actual = lista.primero
    for i in range(indice):
        if actual is None:
            return
        actual = actual.siguiente
    if actual:
        actual.dato = valor