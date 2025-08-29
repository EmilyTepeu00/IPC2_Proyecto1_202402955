from graphviz import Digraph
from lista import ListaEnlazada

class GeneradorGraficas:
    def __init__(self):
        pass

    #GRAFICA PARA UNA MATRIZ
    def graficaMatriz(self, matriz, titulo, tipoMatriz, nombreArchivo):
        dot = Digraph(comment = titulo)
        dot.attr(rankdir='TB', label=titulo, labelloc='t', fontsize='20')

        #Tabla HTML para la mtriz
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
