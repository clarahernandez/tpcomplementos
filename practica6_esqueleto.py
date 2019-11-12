#! /usr/bin/python

# 6ta Practica Laboratorio
# Complementos Matematicos I
# Ejemplo parseo argumentos

#CONSTANTES
AREA = 100


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

        def posiciones_random(self):
            area = 100
            vertices = self.grafo[0]
            for vertice in vertices:
                self.posicion_x(vertice) = uniform(area)
                self.posicion_y(vertice) = uniform(area)


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
                self.acum_x(vertice) = 0
                self.acum_y(vertice) = 0

        def calcular_fuerza_atraccion(self):
            AREA =
            k =
            aristas = self.grafo[1]
            for arista in aristas:
                d = distancia(self, arista[0], arista[1])
                mod_fa = fuerza_atraccion(self, d, )


        def step():
            inicializar_acumuladores()
            calcular_fuerza_atraccion()
            calcular_fuerza_repulsion()
            actualizar_posiciones()





    def layout(self):
        '''
        Aplica el algoritmo de Fruchtermann-Reingold para obtener (y mostrar)
        un layout
        '''
        posiciones_random()
        numIteraciones = 50
        aristas = self.grafo[1]
        for i in range(numIteraciones):
            reset_acum()
        for arista in aristas:
            f = fuerza_atraccion(self, aristas[arista][0], aristas[arista][1])
            accum[]

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
