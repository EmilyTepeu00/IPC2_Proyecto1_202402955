from xml_utils import cargar_xml

def mostrarDatos():
    print("\n" + "="*50)
    print("DATOS DE ESTUDIANTE")
    print("="*50)
    print("Emily Maritza Tepeu Guacamaya")
    print("202402955")
    print("Introduccion a la Programacion y Computacion 2")
    print("Seccion: P")
    print("4to Semestre")
    print("enlaceeee documentaciooooon")
    print("="*50)

def mostrarMenu():
    print("\n" + "="*50)
    print("SISTEMA DE AGRICULTURA DE PRESICION")
    print("="*50)
    print("1. Cargar archivo")
    print("2. Procesar archivo")
    print("3. Escribir archivo salida")
    print("4. Mostrar datos del estudiante")
    print("5. Generar grafica")
    print("6. Salir")
    print("="*50)

def main():
    datos_cargados = None #Para guardar los campos agricolas cargados

    print("Bienvenido al sistema de Optimización de Agricultura")

    while True:
        mostrarMenu()
        opcion = input("Seleccione una opcion: ").strip()

        #CARGAR ARCHIVO XML
        if opcion == "1":
            print("-"*30)
            ruta = input("Ingrese la ruta del archivo xml: ").strip()
            nombre = input("Ingrese el nombre del archivo: ").strip

            archivo_completo = f"{ruta}/{nombre}" if ruta else nombre

            #Para cargar el archivo
            datos_cargados = cargar_xml(archivo_completo)

            if datos_cargados:
                print(f"Archivo cargado con exito")
                print(f"Se encontraron {len(datos_cargados)} campos agricolas")
            else:
                print("No se pudo cargar el archivo")

        #PROCESAR EL ARCHIVO
        elif opcion == "2":
            print("-"*30)
            if datos_cargados:
                print("no hay")
            else:
                print("ERROR: Primero debe cargar un archivo")

        #ESCRIBIR ARCHIVO DE SALIDA
        elif opcion == "3":
            print("-"*30)
            if datos_cargados:
                print("no hay")
            else:
                print("ERROR: Primero debe cargar y procesar un archivo")

        #MOSTRAR DATOS DE ESTUDIANTE
        elif opcion == "4":
            mostrarDatos()

        #GENERAR GRAFICA
        elif opcion == "5":
            print("-"*30)
            if datos_cargados:
                print("no hay")
            else:
                print("ERROR: Primero debe cargar un archivo")

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
