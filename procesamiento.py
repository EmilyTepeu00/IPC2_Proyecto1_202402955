from modelos import MatrizFrecuencia, MatrizPatron, GrupoEstaciones, GrupoEstacionesUnificado
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

#AGRUPAR ESTACIONES CON EL MISMO PATRON BINARIO
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

#PARA VERIFICAR SI EL ELEMENTO CUMPLE CON EL PREDICADO
def any(lista, predicado):
    actual = lista.primero
    while actual:
        if predicado(actual.dato):
            return True
        actual = actual.siguiente
    return False

#GRUPOS UNIFICADOS BASADOS EN LOS "PATRONES" DE LAS 2 MATRICES
def agruparEstacionesUnificado(matriz_p_suelo, matriz_p_cultivo): #p: patron
    print("Creando grupos unificados...")

    grupos = ListaEnlazada()
    estaciones_procesadas = ListaEnlazada()

    #Recorrer todas las estaciones
    actual_estacion = matriz_p_suelo.estaciones.primero
    while actual_estacion:
        idEstacion = actual_estacion.dato

        #Si ya se procesó la estacion, saltar
        if any(estaciones_procesadas, lambda x: x == idEstacion):
            actual_estacion = actual_estacion.siguiente
            continue

        #Obtener patrones de ambas matrices
        patron_suelo = matriz_p_suelo.obtenerPatronEstacion(idEstacion)
        patron_cultivo = matriz_p_cultivo.obtenerPatronEstacion(idEstacion)

        #Para crear nuevo grupo unificado
        nuevo_grupo = GrupoEstacionesUnificado(patron_suelo, patron_cultivo)
        nuevo_grupo.agregarEstacion(idEstacion)
        estaciones_procesadas.agregar(idEstacion)

        #Buscar estaciones con el mismo patron combinado
        actual_estacion2 = actual_estacion.siguiente
        while actual_estacion2:
            idEstacion2 = actual_estacion2.dato

            if any(estaciones_procesadas, lambda x: x == idEstacion2):
                actual_estacion2 = actual_estacion2.siguiente
                continue

            patron_suelo2 = matriz_p_suelo.obtenerPatronEstacion(idEstacion2)
            patron_cultivo2 = matriz_p_cultivo.obtenerPatronEstacion(idEstacion2)

            if (matriz_p_suelo.patronesIguales(patron_suelo, patron_suelo2) and 
                matriz_p_cultivo.patronesIguales(patron_cultivo, patron_cultivo2)):
                
                nuevo_grupo.agregarEstacion(idEstacion2)
                estaciones_procesadas.agregar(idEstacion2)

            actual_estacion2 = actual_estacion2.siguiente

        grupos.agregar(nuevo_grupo)
        actual_estacion = actual_estacion.siguiente

    print(f"Se formaron {grupos.tamaño()} grupos unificados")
    return grupos

#GRUPOS UNIFICADOS BASADOS EN LAS "FRECUENCIAS" DE LAS 2 MATRICES
def calcularFrecuenciasGrupoUnificado(grupo, matriz_f_suelo, matriz_f_cultivo): #f: frecuencia
    print(f"Calculando frecuencias para grupo con {grupo.estaciones.tamaño()} estaciones...")

    #Limpiar listas existentes
    grupo.frecuencias_totales_suelo.limpiar()
    grupo.frecuencias_totales_cultivo.limpiar()

    #Inicializar frecuencias para sensores de suelo
    actual_sensor_suelo = matriz_f_suelo.sensores.primero
    while actual_sensor_suelo:
        grupo.frecuencias_totales_suelo.agregar(0)
        actual_sensor_suelo = actual_sensor_suelo.siguiente

    #Inializar frecuencias para sensores de cultivo
    actual_sensor_cultivo = matriz_f_cultivo.sensores.primero
    while actual_sensor_cultivo:
        grupo.frecuencias_totales_cultivo.agregar(0)
        actual_sensor_cultivo = actual_sensor_cultivo.siguiente

    #Suma de frecuencias de todas las estaciones del grupo
    actual_estacion = grupo.estaciones.primero
    while actual_estacion:
        idEstacion = actual_estacion.dato

        #Para sensores de suelo
        idx_sensor = 0
        actual_sensor = matriz_f_suelo.sensores.primero
        while actual_sensor:
            idSensor = actual_sensor.dato
            valor = matriz_f_suelo.obtenerValor(idEstacion, idSensor)

            valor_actual = obtener_elemento_lista(grupo.frecuencias_totales_suelo, idx_sensor)
            establecer_elemento_lista(grupo.frecuencias_totales_suelo, idx_sensor, valor_actual + valor)

            idx_sensor += 1
            actual_sensor = actual_sensor.siguiente

        #Para sensores de cultivo
        idx_sensor = 0
        actual_sensor = matriz_f_cultivo.sensores.primero
        while actual_sensor:
            idSensor = actual_sensor.dato
            valor = matriz_f_cultivo.obtenerValor(idEstacion, idSensor)

            valor_actual = obtener_elemento_lista(grupo.frecuencias_totales_cultivo, idx_sensor)
            establecer_elemento_lista(grupo.frecuencias_totales_cultivo, idx_sensor, valor_actual + valor)

            idx_sensor += 1
            actual_sensor = actual_sensor.siguiente

        actual_estacion = actual_estacion.siguiente

    print(f"Frecuencias calculadas para cada grupo")

#PROCESAR UN CAMPO AGRICOLA POR COMPLETO
def procesarCampo(campo):
    print(f"\nProcesando campo {campo.id}...")

    #Construir matrices de frecuencia
    matriz_f_suelo = construirMatrizFSuelo(campo)
    matriz_f_cultivo = construirMatrizFCultivo(campo)
    
    #Construir matrices de patrones
    matriz_p_suelo = construirMatrizPatron(matriz_f_suelo)
    matriz_p_cultivo = construirMatrizPatron(matriz_f_cultivo)

    #Grupos unificados
    grupos_unificados = agruparEstacionesUnificado(matriz_p_suelo, matriz_p_cultivo)
    
    # Calcular frecuencias totales para ambos tipos de sensores
    actual_grupo = grupos_unificados.primero
    while actual_grupo:
        calcularFrecuenciasGrupoUnificado(actual_grupo.dato, matriz_f_suelo, matriz_f_cultivo)
        actual_grupo = actual_grupo.siguiente
    
    print(f"Campo {campo.id} procesado con exito")
    
    return {
        'matriz_f_suelo': matriz_f_suelo,
        'matriz_f_cultivo': matriz_f_cultivo,
        'matriz_p_suelo': matriz_p_suelo,
        'matriz_p_cultivo': matriz_p_cultivo,
        'grupos_unificados': grupos_unificados
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
