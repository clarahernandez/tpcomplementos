#! /usr/bin/python

# 6ta Practica Laboratorio
# Complementos Matematicos I
# Ejemplo parseo argumentos

#CONSTANTES
AREA = 1000
K = 10  #Constante que se usa para las fuerzas
C = 0.95 #Constante que se usa para la temperatura

import argparse
import matplotlib.pyplot as plt
import numpy as np
from random import uniform
from math import sqrt, pow


class LayoutGraph:

    def __init__(self, grafo, iters, refresh, c1, c2, verbose=False):
        '''
        Parametros de layout:
        iters: cantidad de iteraciones a realizar
        refresh: Numero de iteraciones entre actualizaciones de pantalla.
        0 -> se grafica solo al final.
        c1: constante usada para calcular la repulsion entre nodos
        c2: constante usada para calcular la atraccion de aristas
        '''

        # Guardo el grafo
        self.grafo = grafo

        # Inicializo estado
        # Completar
        self.posicion_x = {}   #Diccionario, la clave es el vertice el valor la posición x
        self.posicion_y = {}  #Diccionario, la clave es el vertice el valor la posición y
        self.fuerzas = {}
        self.acum_x = {}
        self.acum_y = {}


        # Guardo opciones
        self.iters = iters
        self.verbose = verbose
        # TODO: faltan opciones
        self.refresh = refresh
        self.c1 = c1
        self.c2 = c2
        self.t = t

        def posiciones_random(self):
            area = 100
            vertices = self.grafo[0]
            for vertice in vertices:
                self.posicion_x[vertice] = uniform(area)
                self.posicion_y[vertice] = uniform(area)


        def distancia(self, vertice0, vertice1):
            d = sqrt( pow(posicion_x(vertice0) - posicion_x(vertice1), 2)
                            + pow(posicion_y(vertice0) - posicion_y(vertice1), 2))
            return d

        def fuerza_atraccion(self, d, k):
            f = pow(d, 2) / k
            return f

        def fuerza_repulsion(self, d, k):
            f = pow(k, 2) / d
            return f

        def inicializar_acumuladores(self):
            numVertices = len(self.grafo[0])
            for vertice in range(numVertices):
                self.acum_x[vertice] = 0
                self.acum_y[vertice] = 0

        def calcular_fuerza_atraccion(self):

            aristas = self.grafo[1]
            for arista in aristas:
                d = distancia(self, arista[0], arista[1])
                mod_fa = fuerza_atraccion(self, d, K)
                #fx = mod_fa( self.posicion_x[arista(0) - self.posicion_x[arista(1)] ) / d
                #fy = mod_fa( self.posicion_y[arista(0) - self.posicion_y[arista(1)] ) / d

                self.acum_x[arista[0]] = self.acum_x[arista[0]] + fx
                self.acum_y[arista[0]] = self.acum_y[arista[0]] + fy
                self.acum_x[arista[1]] = self.acum_x[arista[1]] + fx
                self.acum_y[arista[1]] = self.acum_y[arista[1]] + fy

        def calcular_fuerza_repulsion(self): #TODO
            pass

        def actualizar_posiciones(self):
            vertices = self.grafo[0]
            for vertice in vertices:

                posicion_x = self.posicion_x[vertice] + self.acum_x[vertice]
                posicion_y = self.posicion_y[vertice] + self.acum_y[vertice]

                if posicion_x < AREA:
                    self.posicion_x[vertice] = posicion_x
                else:
                    self.posicion_x[vertice] = AREA
                if posicion_y < AREA:
                    self.posicion_y[vertice] = posicion_y
                else:
                    self.posicion_y[vertice] = AREA

        def calcular_fuerza_gravedad(self): #TODO
            pass
        def actualizar_temperatura(self):
            self.t = self.t*C  #Multiplicamos por la constante definida.


        def step():
            inicializar_acumuladores()
            calcular_fuerza_atraccion()
            calcular_fuerza_repulsion()
            calcular_fuerza_gravedad()
            actualizar_posiciones()
            actualizar_temperatura()





    def layout(self):
        '''
        Aplica el algoritmo de Fruchtermann-Reingold para obtener (y mostrar)
        un layout
        '''
        posiciones_random()
        aristas = self.grafo[1]
        for i in range(self.iters):
            step()
        pass


def main():
    # Definimos los argumentos de linea de comando que aceptamos
    parser = argparse.ArgumentParser()

    # Verbosidad, opcional, False por defecto
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Muestra mas informacion al correr el programa'
    )
    # Cantidad de iteraciones, opcional, 50 por defecto
    parser.add_argument(
        '--iters',
        type=int,
        help='Cantidad de iteraciones a efectuar',
        default=50
    )
    # Temperatura inicial
    parser.add_argument(
        '--temp',
        type=float,
        help='Temperatura inicial',
        default=100.0
    )
    # Archivo del cual leer el grafo
    parser.add_argument(
        'file_name',
        help='Archivo del cual leer el grafo a dibujar'
    )

    args = parser.parse_args()

    # Descomentar abajo para ver funcionamiento de argparse
    # print args.verbose
    # print args.iters
    # print args.file_name
    # print args.temp
    # return

    # TODO: Borrar antes de la entrega
    grafo1 = ([1, 2, 3, 4, 5, 6, 7],
              [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 1)])

    # Creamos nuestro objeto LayoutGraph
    layout_gr = LayoutGraph(
        grafo1,  # TODO: Cambiar para usar grafo leido de archivo
        iters=args.iters,
        refresh=1,
        c1=0.1,
        c2=5.0,
        verbose=args.verbose
        )

    # Ejecutamos el layout
    layout_gr.layout()
    return


if __name__ == '__main__':
    main()
