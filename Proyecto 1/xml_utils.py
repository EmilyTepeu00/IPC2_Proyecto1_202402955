import xml.etree.ElementTree as ET
from modelos import CampoAgricola, Estacion, SensorSuelo, SensorCultivo
from lista import ListaEnlazada

def cargar_xml(rutaArchivo):
    try:
        print(f"\nLeyendo archivo: {rutaArchivo}")
        arbol = ET.parse(rutaArchivo) #Parsea el XML a un arbol de elementos
        raiz = arbol.getroot() #Obtiene el elemento raiz
        campos = []

        #Iterar sobre todos los elementos campo en el XML
        for campo_elemento in raiz.findall("campo"):
            print(f"Procesando campo: {campo_elemento.get('nombre')}")

            #Objeto CampoAgricola
            campo = CampoAgricola(
                campo_elemento.get("id"),
                campo_elemento.get("nombre")
            )

            #PROCESAR ESTACIONES BASE
            estaciones_elemento = campo_elemento.find("estacionesBase")
            if estaciones_elemento is not None:
                for estacion_elemento in estaciones_elemento.findall("estacion"):
                    estacion = Estacion(
                        estacion_elemento.get("id"),
                        estacion_elemento.get("nombre")
                    )

                    campo.estaciones.agregar(estacion)
                    print(f"Estacion agregada: {estacion.id}")

            #PROCESAR SENSORES DE SUELO
            sensores_suelo_elemento = campo_elemento.find("sensoresSuelo")
            if sensores_suelo_elemento is not None:
                for sensor_elemento in sensores_suelo_elemento.findall("sensorS"):
                    sensor = SensorSuelo(
                        sensor_elemento.get("id"),
                        sensor_elemento.get("nombre")
                    )

                    #procesar las frecuencias del sensor
                    for freq_elemento in sensor_elemento.findall("frecuencia"):
                        #strip() elimina espacios en blanco alrededor del texto
                        valor = int(freq_elemento.text.strip()) if freq_elemento.text else 0
                        sensor.agregarFrecuencia(
                            freq_elemento.get("idEstacion"),
                            valor
                        )

                    campo.sensores_suelo.agregar(sensor)
                    print(f"Sensor suelo agregado: {sensor.id}")

            #PROCESAR SENSORES DE CULTIVO
            sensores_cultivo_elemento = campo_elemento.find("sensoresCultivo")
            if sensores_cultivo_elemento is not None:
                for sensor_elemento in sensores_cultivo_elemento.findall("sensorT"):
                    sensor = SensorCultivo(
                        sensor_elemento.get("id"),
                        sensor_elemento.get("nombre")
                    )

                    for freq_elemento in sensor_elemento.findall("frecuencia"):
                        valor = int(freq_elemento.text.strip()) if freq_elemento.text else 0
                        sensor.agregarFrecuencia(
                            freq_elemento.get("idEstacion"),
                            valor
                        )

                    campo.sensores_cultivo.agregar(sensor)
                    print(f"Sensor cultivo agregado: {sensor.id}")

            campos.append(campo)
            print(f"Campo {campo.id} procesado correctamente\n")

        print(f"Carga completada. {len(campos)} campo(s) procesado(s)")
        return campos
    
    except ET.ParseError as e:
        print(f"Error de formato XML: {e}")
        return None
    
    except FileNotFoundError:
        print(f"Archivo no encontrado: {rutaArchivo}")
        return None

    except Exception as e:
        print(f"Error al cargar XML: {e}")
        return None
    
#PARA ESCRIBIR EL ARCHIVO DE SALIDA
def escribir_xml_salida(rutaArchivo, campo_originales, resultados_procesamiento):
    try:
        #Elemento raiz
        raiz = ET.Element("camposAgricolas")

        #Procesar cada campo agricola
        for i, campo_original in enumerate(campo_originales):
            resultado = resultados_procesamiento[i]

            #Elemento campo
            campo_elemento = ET.SubElement(raiz, "campo")
            campo_elemento.set("id", campo_original.id)
            campo_elemento.set("nombre", campo_original.nombre)

            #Elemento estacionesBaseReducidas
            estaciones_reducidas = ET.SubElement(campo_elemento, "estacionesBaseReducidas")

            #Obtener grupos de suelo
            grupos_unificados = resultado['grupos_unificados']

            #Estaciones reducidas basadas en grupos unificados
            actual_grupo = grupos_unificados.primero
            grupo_index = 1
            while actual_grupo:
                grupo = actual_grupo.dato

                #Nombre de estacion reducida
                nombres_estaciones = ListaEnlazada()
                actual_estacion = grupo.estaciones.primero
                while actual_estacion:
                    # Buscar la estación original
                    estacion_original = None
                    actual_est_orig = campo_original.estaciones.primero
                    while actual_est_orig:
                        if actual_est_orig.dato.id == actual_estacion.dato:
                            estacion_original = actual_est_orig.dato
                            break
                        actual_est_orig = actual_est_orig.siguiente

                    if estacion_original:
                        nombres_estaciones.agregar(estacion_original.nombre)
                    actual_estacion = actual_estacion.siguiente

                #Construir string de nombres
                nombres_str = ""
                actual_nombre = nombres_estaciones.primero
                while actual_nombre:
                    nombres_str += actual_nombre.dato
                    if actual_nombre.siguiente:
                        nombres_str += ", "
                    actual_nombre = actual_nombre.siguiente

                #Elemento estacion reducida
                estacion_reducida = ET.SubElement(estaciones_reducidas, "estacion")
                estacion_reducida.set("id", f"e{grupo_index:02d}")  # e01, e02, e03...
                estacion_reducida.set("nombre", nombres_str)

                actual_grupo = actual_grupo.siguiente
                grupo_index += 1

            #Elemento sensoresSuelo
            sensores_suelo_elemento = ET.SubElement(campo_elemento, "sensoresSuelo")

            #Procesar sensores de suelo originales
            actual_sensor_original = campo_original.sensores_suelo.primero
            while actual_sensor_original:
                sensor_original = actual_sensor_original.dato

                sensor_elemento = ET.SubElement(sensores_suelo_elemento, "sensorS")
                sensor_elemento.set("id", sensor_original.id)
                sensor_elemento.set("nombre", sensor_original.nombre)

                #Asignar frecuencias a los grupos correspondientes (suelo)
                actual_grupo = grupos_unificados.primero
                grupo_index = 1
                while actual_grupo:
                    grupo = actual_grupo.dato

                    #Obtener el indice del sensor en la matriz
                    idx_sensor = 0
                    actual_sensor_id = resultado['matriz_f_suelo'].sensores.primero
                    while actual_sensor_id:
                        if actual_sensor_id.dato == sensor_original.id:
                            break
                        idx_sensor += 1
                        actual_sensor_id = actual_sensor_id.siguiente

                    #Obtener frecuencia total del sensor en el grupo
                    frecuencia_valor = obtener_elemento_lista(grupo.frecuencias_totales_suelo, idx_sensor)

                    if frecuencia_valor > 0:
                        frecuencia_elemento = ET.SubElement(sensor_elemento, "frecuencia")
                        frecuencia_elemento.set("idEstacion", f"e{grupo_index:02d}")
                        frecuencia_elemento.text = f" {frecuencia_valor} "  # Con espacios como en el ejemplo
                    
                    actual_grupo = actual_grupo.siguiente
                    grupo_index += 1

                actual_sensor_original = actual_sensor_original.siguiente

            #Elemento sensoresCultivo
            sensores_cultivo_elemento = ET.SubElement(campo_elemento, "sensoresCultivo")


            #Procesar sensores de cultivo originales
            actual_sensor_original = campo_original.sensores_cultivo.primero
            while actual_sensor_original:
                sensor_original = actual_sensor_original.dato
                
                sensor_elemento = ET.SubElement(sensores_cultivo_elemento, "sensorT")
                sensor_elemento.set("id", sensor_original.id)
                sensor_elemento.set("nombre", sensor_original.nombre)

                #Asignar frecuencias a los grupos correspondientes (cultivo)
                actual_grupo = grupos_unificados.primero
                grupo_index = 1
                while actual_grupo:
                    grupo = actual_grupo.dato

                    #Obtener el indice del sensor en la matriz
                    idx_sensor = 0
                    actual_sensor_id = resultado['matriz_f_cultivo'].sensores.primero
                    while actual_sensor_id:
                        if actual_sensor_id.dato == sensor_original.id:
                            break
                        idx_sensor += 1
                        actual_sensor_id = actual_sensor_id.siguiente

                    #Obtener frecuencia total  del sensor en el grupo
                    frecuencia_valor = obtener_elemento_lista(grupo.frecuencias_totales_cultivo, idx_sensor)

                    if frecuencia_valor > 0:
                        frecuencia_elemento = ET.SubElement(sensor_elemento, "frecuencia")
                        frecuencia_elemento.set("idEstacion", f"e{grupo_index:02d}")
                        frecuencia_elemento.text = f" {frecuencia_valor} "

                    actual_grupo = actual_grupo.siguiente
                    grupo_index += 1

                actual_sensor_original = actual_sensor_original.siguiente

        #Para crear el arbol XML y escribir el archivo
        arbol = ET.ElementTree(raiz)
        ET.indent(arbol, space="    ", level=0)
        arbol.write(rutaArchivo, encoding="utf-8", xml_declaration=True)

        print(f"Archivo de salida escrito con exito: {rutaArchivo}")
        return True
        
    except Exception as e:
        print(f"Error al escribir el archivo XML: {e}")
        return False
    
#FUNCION PARA OBTENER ELEMENTO DE LISTA POR INDICE
def obtener_elemento_lista(lista, indice):
    actual = lista.primero
    for i in range(indice):
        if actual is None:
            return None
        actual = actual.siguiente
    return actual.dato if actual else None
    