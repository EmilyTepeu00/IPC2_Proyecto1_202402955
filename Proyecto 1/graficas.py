from graphviz import Digraph
from lista import ListaEnlazada

class GeneradorGraficas:
    def __init__(self):
        pass

    #GRAFICA PARA UNA MATRIZ
    def graficaMatriz(self, matriz, titulo, tipoMatriz, nombreArchivo):
        dot = Digraph(comment = titulo)
        dot.attr(rankdir='TB', label=titulo, labelloc='t', fontsize='20')

        #Tabla HTML para la matriz
        tabla_html = self._crearTablaMatriz(matriz, tipoMatriz)

        dot.node('matriz', label=tabla_html, shape='none')

        #Guardar y renderizar
        dot.render(nombreArchivo, view=False, cleanup=True)
        print(f"Grafica generada: {nombreArchivo}.pdf")

    #TABLA HTML PARA REPRESENTAR LA MATRIZ
    def _crearTablaMatriz(self, matriz, tipoMatriz):
        html = '''<
        <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">
        <TR>
            <TD BGCOLOR="lightgray"></TD>'''
        
        #Encabezado de las columnas (SENSORES)
        actual_sensor = matriz.sensores.primero
        while actual_sensor:
            html += (f'<TD BGCOLOR="lightgray"><B>{actual_sensor.dato}</B></TD>')
            actual_sensor = actual_sensor.siguiente
        html += '</TR>'

        #Filas de la matriz
        idx_estacion = 0
        actual_estacion = matriz.estaciones.primero
        while actual_estacion:
            html += f'<TR><TD BGCOLOR="lightgray"><B>{actual_estacion.dato}</B></TD>'

            #Valores de la fila
            fila = self._obtenerElementoLista(matriz.filas, idx_estacion)
            if fila:
                actual_valor = fila.primero
                while actual_valor:
                    if tipoMatriz == 'patron':
                        valor_str = '1' if actual_valor.dato > 0 else '0'
                        color = 'lightgreen' if actual_valor.dato > 0 else 'lightcoral'
                    else:
                        valor_str = str(actual_valor.dato)
                        color = 'lightblue' if actual_valor.dato > 0 else 'white'

                    html += f'<TD BGCOLOR="{color}">{valor_str}</TD>'
                    actual_valor = actual_valor.siguiente

            html += '</TR>'
            idx_estacion += 1
            actual_estacion = actual_estacion.siguiente

        html += '</TABLE>>'
        return html
    
    #OBTENER ELEMENTO DE ListaEnlazada POR INDICE
    def _obtenerElementoLista(self, lista, indice):
        actual = lista.primero
        for i in range(indice):
            if actual is None:
                return None
            actual = actual.siguiente
        return actual.dato if actual else None
    
    #GRAFICA PARA LOS GRUPOS DE ESTACIONES
    def graficaGrupos(self, gruposUnificados, nombreArchivo):
        dot = Digraph(comment='Grupo de Estaciones')
        dot.attr(rankdir='TB', label='Grupo de Estaciones Unificados', labelloc='t', fontsize='20')

        #Crear nodos para cada grupo
        grupo_idx = 1
        actual_grupo = gruposUnificados.primero
        while actual_grupo:
            grupo = actual_grupo.dato

            #Obtener nombres de estaciones del grupo
            estaciones_str = ""
            actual_estacion = grupo.estaciones.primero
            while actual_estacion:
                estaciones_str += (f"{actual_estacion.dato}\\n")
                actual_estacion = actual_estacion.siguiente

            dot.node(f'grupo_{grupo_idx}', 
                    label=f'Grupo {grupo_idx}\\n{estaciones_str}',
                    shape='box', style='filled', fillcolor='lightyellow')
            
            grupo_idx += 1
            actual_grupo = actual_grupo.siguiente

        dot.render(nombreArchivo, view=False, cleanup=True)
        print(f"Grafica de grupos generada: {nombreArchivo}.pdf")


    #GENERAR GRAFICA PARA MATRIZ REDUCIDA
    def graficaMatrizReducida(self, matrizReducida, titulo, nombreArchivo):
        dot = Digraph(comment = titulo)
        dot.attr(rankdir='TB', label=titulo, labelloc='t', fontsize='20')

        #Tabla HTML para la matriz reducida
        tabla_html = self._crearTablaMatrizReducida(matrizReducida)

        dot.node('matrizReducida', label=tabla_html, shape='none')

        #Guardar y renderizar
        dot.render(nombreArchivo, view=False, cleanup=True)
        print(f"Grafica de matriz reducida generada: {nombreArchivo}.pdf")

    #TABLA HTML PARA LA MATRIZ REDUCIDA
    def _crearTablaMatrizReducida(self, matrizReducida):
        html = '''<
        <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">
        <TR>
            <TD BGCOLOR="lightgray"></TD>'''

        #Encabezado de columnas (SENSORES)
        actual_sensor = matrizReducida.matriz_original.sensores.primero
        while actual_sensor:
            html += f'<TD BGCOLOR="lightgray"><B>{actual_sensor.dato}</B></TD>'
            actual_sensor = actual_sensor.siguiente
        html += '</TR>'

        #Filas de la matriz reducida (GRUPOS)
        grupo_idx = 1
        actual_fila = matrizReducida.filas.primero
        while actual_fila:
            html += f'<TR><TD BGCOLOR="lightgray"><B>Grupo {grupo_idx}</B></TD>'

            #Valores de la fila (FRECUNECIAS DEL GRUPO)
            actual_valor = actual_fila.dato.primero if actual_fila.dato else None
            while actual_valor:
                valor_str = str(actual_valor.dato)
                color = 'lightblue' if actual_valor.dato > 0 else 'white'

                html += f'<TD BGCOLOR="{color}">{valor_str}</TD>'
                actual_valor = actual_valor.siguiente
            
            html += '</TR>'
            grupo_idx += 1
            actual_fila = actual_fila.siguiente

        html += '</TABLE>>'
        return html

    #OBTENER LISTA DE IDs DE GRUPOS
    def obtener_ids_grupos(self, gruposUnificados):
        ids_grupos = ListaEnlazada()
        grupo_idx = 1
        actual_grupo = gruposUnificados.primero

        while actual_grupo:
            grupo = actual_grupo.dato

            #Obtener nombres de estaciones del grupo
            estaciones_str = ""
            actual_estacion = grupo.estaciones.primero
            while actual_estacion:
                estaciones_str += (f"{actual_estacion.dato}, ")
                actual_estacion = actual_estacion.siguiente

            #Para quitar la ultima coma
            if estaciones_str:
                estaciones_str = estaciones_str[:-2]

            ids_grupos.agregar(f"Grupo {grupo_idx}: {estaciones_str}")
            grupo_idx += 1
            actual_grupo = actual_grupo.siguiente

        return ids_grupos