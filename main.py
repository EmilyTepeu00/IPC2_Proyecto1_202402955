from xml_utils import cargar_xml, escribir_xml_salida
from procesamiento import procesarCampo

def mostrarDatos():
    print("\n" + "*"*50)
    print("DATOS DE ESTUDIANTE")
    print("*"*50)
    print("Emily Maritza Tepeu Guacamaya")
    print("202402955")
    print("Introduccion a la Programacion y Computacion 2")
    print("Seccion: P")
    print("4to Semestre")
    print("enlaceeee documentaciooooon")
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
    datos_cargados = None #Para guardar los campos agricolas cargados
    datos_procesados = None #Para los resultados del procesamiento

    while True:
        mostrarMenu()
        opcion = input("Seleccione una opcion: ").strip()

        #CARGAR ARCHIVO XML
        if opcion == "1":
            ruta = input("Ingrese la ruta del archivo xml: ").strip()
            nombre = input("Ingrese el nombre del archivo: ").strip()

            archivo_completo = f"{ruta}/{nombre}" if ruta else nombre

            #Para cargar el archivo
            datos_cargados = cargar_xml(archivo_completo)
            datos_procesados = None

            if datos_cargados:
                print(f"Archivo cargado con exito")
                print(f"Se encontraron {len(datos_cargados)} campos agricolas")
            else:
                print("No se pudo cargar el archivo")

        #PROCESAR EL ARCHIVO
        elif opcion == "2":
            if datos_cargados:
                print("Iniciando el procesamiento de datos...")

                resultados_procesamiento = []

                for i, campo in enumerate(datos_cargados, 1):
                    print(f"\nProcesando campo {i} de {len(datos_cargados)}...")
                    try:
                        resultado = procesarCampo(campo)
                        resultados_procesamiento.append(resultado)
                        print(f"Campo {campo.id} procesado con exito")
                    except Exception as e:
                        print(f"Error al procesar campo {campo.id}: {e}")

                if resultados_procesamiento:
                    datos_procesados = resultados_procesamiento
                    print("\nPROCESAMIENTO COMPLETADO")
                    print("=" * 40)
                    print("✓ Matrices de frecuencia construidas")
                    print("✓ Matrices de patrones generadas")
                    print("✓ Estaciones agrupadas por patrones similares")
                    print("✓ Frecuencias totales calculadas")
                    print("=" * 40)

                    #Mostrar resumen de agrupamiento
                    for i, resultado in enumerate(datos_procesados):
                        print(f"\nCampo {datos_cargados[i].id}:")
                        print(f"  - Grupos sensores suelo: {resultado['grupos_suelo'].tamaño()}")
                        print(f"  - Grupos sensores cultivo: {resultado['grupos_cultivo'].tamaño()}")

                else:
                    print("No se pudo procesar ningun campo")

            else:
                print("\nERROR: Primero debe cargar un archivo")

        #ESCRIBIR ARCHIVO DE SALIDA
        elif opcion == "3":
            if datos_cargados and datos_procesados:
                print("\nGENERAR ARCHIVO DE SALIDA")

                ruta = input("Ingrese la ruta del archivo: ").strip()
                nombre = input("Ingrese el nombre del archivo: ").strip()

                archivo_completo = (f"{ruta}/{nombre}") if ruta else nombre

                #Asegurar que el archivo sea .xml
                if not archivo_completo.endswith('.xml'):
                    archivo_completo += '.xml'

                #Escribir el archivo de salida
                exito = escribir_xml_salida(archivo_completo, datos_cargados, datos_procesados)

                if exito:
                    print("Archivo de salida generado con exito") 
                else:
                    print("Error al generar el archivo de salida")

            else:
                print("\nERROR: Primero debe cargar y procesar un archivo")

        #MOSTRAR DATOS DE ESTUDIANTE
        elif opcion == "4":
            mostrarDatos()

        #GENERAR GRAFICA
        elif opcion == "5":
            if datos_cargados:
                print("no hay")
            else:
                print("\nERROR: Primero debe cargar un archivo")

        #SALIR DEL PROGRAMA
        elif opcion == "6":
            print("Saliendo del sistema...")
            break

        else:
            print("\nOpcion no valida, intente de nuevo")
            main()

        input("\nPresione Enter para continuar")

#PARA EJECUTAR
if __name__ == "__main__":
    main()
