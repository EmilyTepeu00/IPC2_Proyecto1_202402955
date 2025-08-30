from xml_utils import cargar_xml, escribir_xml_salida
from procesamiento import procesarCampo
from graficas import GeneradorGraficas

def mostrarDatos():
    print("\n" + "*"*50)
    print("DATOS DE ESTUDIANTE")
    print("*"*50)
    print("Emily Maritza Tepeu Guacamaya")
    print("202402955")
    print("Introduccion a la Programacion y Computacion 2")
    print("Seccion: P")
    print("4to Semestre")
    print("Documentación:")
    print("https://github.com/EmilyTepeu00/IPC2_Proyecto1_202402955/tree/main/Documentaci%C3%B3n")
    print("https://github.com/EmilyTepeu00/IPC2_Proyecto1_202402955")
    print("*"*50)

def mostrarMenu():
    print("\n" + "="*35)
    print("SISTEMA DE AGRICULTURA DE PRESICION")
    print("="*35)
    print("1. Cargar archivo")
    print("2. Procesar archivo")
    print("3. Escribir archivo salida")
    print("4. Mostrar datos del estudiante")
    print("5. Generar grafica")
    print("6. Salir")
    print("="*35)

def main():
    lista_campos_cargados = []  #Lista de todos los campos cargados
    lista_resultados_procesados = []  #Lista de todos los resultados

    while True:
        mostrarMenu()
        opcion = input("Seleccione una opcion: ").strip()

        #CARGAR ARCHIVO XML
        if opcion == "1":
            ruta = input("Ingrese la ruta del archivo xml: ").strip()
            nombre = input("Ingrese el nombre del archivo: ").strip()

            archivo_completo = f"{ruta}/{nombre}" if ruta else nombre

            #Para cargar el archivo
            nuevos_campos = cargar_xml(archivo_completo)
            if nuevos_campos:
                lista_campos_cargados.extend(nuevos_campos)  #Agregar a la lista
                print(f"Archivo cargado con exito")
                print(f"Total de campos cargados: {len(lista_campos_cargados)}")
                # Mostrar los campos cargados
                for i, campo in enumerate(lista_campos_cargados, 1):
                    print(f"  {i}. {campo.nombre} (ID: {campo.id})")
            else:
                print("No se pudo cargar el archivo")

        #PROCESAR EL ARCHIVO
        elif opcion == "2":
            if lista_campos_cargados:
                print("Iniciando el procesamiento de datos...")
                print(f"Procesando {len(lista_campos_cargados)} campos...")

                # Limpiar resultados previos y procesar todos
                lista_resultados_procesados = []
                
                for i, campo in enumerate(lista_campos_cargados, 1):
                    print(f"\nProcesando campo {i} de {len(lista_campos_cargados)}...")
                    print(f"Campo: {campo.nombre} (ID: {campo.id})")
                    try:
                        resultado = procesarCampo(campo)
                        lista_resultados_procesados.append(resultado)
                        print(f"✓ Campo {campo.id} procesado con exito")
                    except Exception as e:
                        print(f"✗ Error al procesar campo {campo.id}: {e}")
                        lista_resultados_procesados.append(None)

                print("\nPROCESAMIENTO COMPLETADO")
                print("=" * 40)
                print("✓ Matrices de frecuencia construidas")
                print("✓ Matrices de patrones generadas")
                print("✓ Estaciones agrupadas por patrones similares")
                print("✓ Frecuencias totales calculadas")
                print("=" * 40)

                #Mostrar resumen de agrupamiento
                print("\nRESUMEN DE AGRUPAMIENTO:")
                for i, (campo, resultado) in enumerate(zip(lista_campos_cargados, lista_resultados_procesados)):
                    if resultado:
                        print(f"  Campo {campo.id}: {resultado['grupos_unificados'].tamaño()} grupos unificados")
                    else:
                        print(f"  Campo {campo.id}: Error en procesamiento")

            else:
                print("\nERROR: Primero debe cargar un archivo")

        #ESCRIBIR ARCHIVO DE SALIDA
        elif opcion == "3":
            if lista_campos_cargados and lista_resultados_procesados:
                if len(lista_resultados_procesados) != len(lista_campos_cargados):
                    print("ERROR: Algunos campos no se procesaron correctamente")
                    continue
                    
                print("\nGENERAR ARCHIVO DE SALIDA")
                print(f"Campos disponibles ({len(lista_campos_cargados)}):")
                
                # Mostrar opciones de campos
                for i, campo in enumerate(lista_campos_cargados, 1):
                    print(f"{i}. {campo.nombre} (ID: {campo.id})")
                
                try:
                    opcion_campo = int(input("Seleccione el campo a exportar: ")) - 1
                    if 0 <= opcion_campo < len(lista_campos_cargados):
                        campo_seleccionado = lista_campos_cargados[opcion_campo]
                        resultado_seleccionado = lista_resultados_procesados[opcion_campo]
                        
                        if resultado_seleccionado is None:
                            print("ERROR: Este campo no se procesó correctamente")
                            continue

                        ruta = input("Ingrese la ruta del archivo: ").strip()
                        nombre = input("Ingrese el nombre del archivo: ").strip()

                        archivo_completo = (f"{ruta}/{nombre}") if ruta else nombre

                        #Asegurar que el archivo sea .xml
                        if not archivo_completo.endswith('.xml'):
                            archivo_completo += '.xml'

                        #Escribir el archivo de salida
                        exito = escribir_xml_salida(archivo_completo, [campo_seleccionado], [resultado_seleccionado])

                        if exito:
                            print("Archivo de salida generado con exito") 
                        else:
                            print("Error al generar el archivo de salida")
                    else:
                        print("Numero de campo no valido")

                except ValueError:
                    print("Ingrese un numero valido")

            else:
                print("\nERROR: Primero debe cargar y procesar un archivo")

        #MOSTRAR DATOS DE ESTUDIANTE
        elif opcion == "4":
            mostrarDatos()

        #GENERAR GRAFICA
        elif opcion == "5":
            if lista_campos_cargados and lista_resultados_procesados:
                if len(lista_resultados_procesados) != len(lista_campos_cargados):
                    print("ERROR: Algunos campos no se procesaron correctamente")
                    continue
                    
                print("\nGENERAR GRAFICA")
                print("Campos disponibles:")

                #Mostrar campos disponibles
                for i, campo in enumerate(lista_campos_cargados, 1):
                    status = "✓" if lista_resultados_procesados[i-1] else "✗"
                    print(f"{i}. {status} {campo.nombre} (ID: {campo.id})")

                try:
                    opcionCampo = int(input("Seleccione el campo: ")) - 1
                    if 0 <= opcionCampo < len(lista_campos_cargados):
                        campoSeleccionado = lista_campos_cargados[opcionCampo]
                        resultado = lista_resultados_procesados[opcionCampo]
                        
                        if resultado is None:
                            print("ERROR: Este campo no se procesó correctamente")
                            continue

                        print("\nTipos de grafica disponibles: ")
                        print("1. Matriz de Frecuencias (suelo)")
                        print("2. Matriz de Frecuencias (cultivo)")
                        print("3. Matriz de Patrones (suelo)")
                        print("4. Matriz de Patrones (cultivo)")
                        print("5. Matriz de Reducida (suelo)")
                        print("6. Matriz de Reducida (cultivo)")
                        print("7. Grupos de Estaciones")

                        opcionGrafica = input("Seleccione el tipo de grafica: ").strip()

                        nombreBase = (f"campo_{campoSeleccionado.id}")
                        generador = GeneradorGraficas()

                        if opcionGrafica == "1":
                            generador.graficaMatriz(
                                resultado['matriz_f_suelo'],
                                f"Matriz Frecuencias Suelo - {campoSeleccionado.nombre}",
                                'frecuencia',
                                f"{nombreBase}_frecuencia_suelo"
                            )

                        elif opcionGrafica == "2":
                            generador.graficaMatriz(
                                resultado['matriz_f_cultivo'],
                                f"Matriz Frecuencias Cultivo - {campoSeleccionado.nombre}",
                                'frecuencia',
                                f"{nombreBase}_frecuencia_cultivo"
                            )

                        elif opcionGrafica == "3":
                            generador.graficaMatriz(
                                resultado['matriz_p_suelo'],
                                f"Matriz de Patrones Suelo - {campoSeleccionado.nombre}",
                                'patron',
                                f"{nombreBase}_patron_suelo"
                            )

                        elif opcionGrafica == "4":
                            generador.graficaMatriz(
                                resultado['matriz_p_cultivo'],
                                f"Matriz de Patrones Cultivo - {campoSeleccionado.nombre}",
                                'patron',
                                f"{nombreBase}_patron_cultivo"
                            )

                        elif opcionGrafica == "5":
                            #Matriz reducida suelo
                            generador.graficaMatrizReducida(
                                resultado['matriz_reducida_suelo'],
                                f"Matriz Reducida Suelo - {campoSeleccionado.nombre}",
                                f"{nombreBase}_reducida_suelo"
                            )   
                        
                        elif opcionGrafica == "6":
                            #Matriz reducida cultivo
                            generador.graficaMatrizReducida(
                                resultado['matriz_reducida_cultivo'],
                                f"Matriz Reducida Cultivo - {campoSeleccionado.nombre}",
                                f"{nombreBase}_reducida_cultivo"
                            )

                        elif opcionGrafica == "7":
                            generador.graficaGrupos(
                                resultado['grupos_unificados'],
                                f"{nombreBase}_grupos"
                            )
                                                        
                        else:
                            print("Opcion no valida")

                    else:
                        print("Numero de campo no valido")

                except ValueError:
                    print("Ingrese un numero valido")
                        
            else:
                print("\nERROR: Primero debe cargar y procesar un archivo")

        #SALIR DEL PROGRAMA
        elif opcion == "6":
            print("Saliendo del sistema...")
            break

        else:
            print("\nOpcion no valida, intente de nuevo")

        input("\nPresione Enter para continuar")

#PARA EJECUTAR
if __name__ == "__main__":
    main()