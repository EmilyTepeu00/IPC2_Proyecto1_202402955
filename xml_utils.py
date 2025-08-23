import xml.etree.ElementTree as ET
from modelos import CampoAgricola, Estacion, SensorSuelo, SensorCultivo

def cargar_xml(rutaArchivo):
    try:
        print(f"Leyendo archivo: {rutaArchivo}")
        arbol = ET.parse(rutaArchivo) #Parsea el XML a un arbol de elementos
        raiz = arbol.getroot() #Obtiene el elemento raiz
        campos = []

        #Iterar sobre todos los elementos campo en el XML
        for campo_elemento in raiz.findall("campo"):
            print(f"Procesando campo: {campo_elemento.get("nombre")}")

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
                        estacion_elemento.get("nomvbre")
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
                    sensor.agregar_frecuencia(
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
