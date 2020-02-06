#! /usr/bin/python

# 6ta Practica Laboratorio
# Complementos Matematicos I
# Ejemplo parseo argumentos

# CONSTANTES
G = 0.1
AREA = 10000
ca = 10  # Constante que se usa para la fuerza de atracción
C = 0.95  # Constante que se usa para la temperatura
CLOSEZERO = 0.00001
EPSILON = 0.005
G = 0.1  # Constante de gravedad

import argparse
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt, pow
from random import uniform


def mul_escalar(vector, e):
    v1 = (vector[0] * e, vector[1] * e)
    return v1

class LayoutGraph:

    def __init__(self, grafo, iters, refresh, c1, c2, verbose = False):
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
        self.posicion_x = {}  # Diccionario, la clave es el vertice el valor la posición x
        self.posicion_y = {}  # Diccionario, la clave es el vertice el valor la posición y
        self.fuerzas = {}
        self.acum_x = {}
        self.acum_y = {}
        self.t = 1

        # Guardo opciones
        self.iters = iters
        self.verbose = verbose
        # TODO: faltan opciones
        self.refresh = refresh
        self.c1 = c1
        self.c2 = c2

    def posiciones_random(self):
        vertices = self.grafo[0]
        for vertice in vertices:
            self.posicion_x[vertice] = uniform(0, AREA)
            self.posicion_y[vertice] = uniform(0, AREA)

    def distancia(self, vertice0, vertice1):
        d = sqrt(pow(self.posicion_x[vertice0] - self.posicion_x[vertice1], 2) + pow(
            self.posicion_y[vertice0] - self.posicion_y[vertice1], 2))
        return d

    def fuerza_atraccion(self, d, vertices):
        k = ca * sqrt(AREA / len(vertices))
        f = pow(d, 2) / k
        return f

    def fuerza_repulsion(self, d, vertices):
        k = ca * sqrt(AREA / len(vertices))
        f = pow(k, 2) / d
        return f

    def inicializar_acumuladores(self):
        vertices = self.grafo[0]
        for vertice in vertices:
            self.acum_x[vertice] = 0
            self.acum_y[vertice] = 0

    def calcular_fuerza_atraccion(self):

        aristas = self.grafo[1]
        for arista in aristas:
            d = self.distancia(arista[0], arista[1])
            mod_fa = self.fuerza_atraccion(d, self.grafo[0])

            # Consideramos el caso de divisiones por 0
            while (d < 0):
                f = random.random()
                self.posicion_x[arista[0]] += f
                self.posicion_y[arista[0]] += f
                self.posicion_x[arista[1]] -= f
                self.posicion_y[arista[1]] -= f
                d = dist(arista[0], arista[1])

            mod_fa = self.fuerza_atraccion(d, self.grafo[0])
            fx = ((mod_fa) * (self.posicion_x[arista[0]] - self.posicion_x[arista[1]]))
            fy = ((mod_fa) * (self.posicion_y[arista[0]] - self.posicion_y[arista[1]]))

            self.acum_x[arista[0]] += fx
            self.acum_y[arista[0]] += fy
            self.acum_x[arista[1]] -= fx
            self.acum_y[arista[1]] -= fy

    def calcular_fuerza_repulsion(self):
        vertices = self.grafo[0]
        for i in range(0, len(vertices)):
            for j in range(i + 1, len(vertices)):
                vertice1 = vertices[i]
                vertice2 = vertices[j]
                d = self.distancia(vertice1, vertice2)

                # Consideramos el caso de divisiones por 0
                while (d < 0):
                    f = random.random()
                    self.posicion_x[vertice1] += f
                    self.posicion_y[vertice1] += f
                    self.posicion_x[vertice2] -= f
                    self.posicion_y[vertice2] -= f
                    d = dist(vertice1, vertice2)

                mod_fa = self.fuerza_repulsion(d, self.grafo[0])
                fx = ((mod_fa) * (self.posicion_x[vertice1] - self.posicion_x[vertice2]))
                fy = ((mod_fa) * (self.posicion_y[vertice1] - self.posicion_y[vertice2]))

                self.acum_x[vertice1] -= fx
                self.acum_y[vertice1] -= fy
                self.acum_x[vertice2] += fx
                self.acum_y[vertice2] += fy



    def actualizar_posiciones(self):
        vertices = self.grafo[0]
        for vertice in vertices:

            f = (self.acum_x[vertice], self.acum_y[vertice])
            modulo_f = sqrt(pow(f[0], 2) + pow(f[1], 2))
            if modulo_f > self.t:
                f = mul_escalar(mul_escalar(f, 1 / modulo_f), self.t)
                (self.acum_x[vertice], self.acum_y[vertice]) = f
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

    def calcular_fuerza_gravedad(self):
        pos_x = sqrt(AREA) / 2
        pos_y = pos_x
        for vertice in self.grafo[0]:
            dist = sqrt(pow((pos_x - self.posicion_x[vertice]), 2) + (pow((pos_y - self.posicion_y[vertice]), 2)))
            fx = ((G * (pos_x - self.posicion_x[vertice])) / dist)
            fy = ((G * (pos_y - self.posicion_y[vertice])) / dist)
            self.acum_x[vertice] -= fx
            self.acum_y[vertice] -= fy

    def actualizar_temperatura(self):
        self.t = self.t * C  # Multiplicamos por la constante definida.

    def step(self):
        self.inicializar_acumuladores()
        self.calcular_fuerza_atraccion()
        self.calcular_fuerza_repulsion()
        self.calcular_fuerza_gravedad()
        self.actualizar_posiciones()
        self.actualizar_temperatura()

    def show_graph(self):
        plt.pause(0.001)
        posx = [self.posicion_x[i] for i in self.grafo[0]]
        posy = [self.posicion_y[i] for i in self.grafo[0]]
        plt.clf()

        plt.scatter(posx, posy)  # dibuja los puntos.

        for arista in self.grafo[1]:
            vertice1 = arista[0]
            vertice2 = arista[1]
            plt.plot([self.posicion_x[vertice1], self.posicion_x[vertice2]],
                     [self.posicion_y[vertice1], self.posicion_y[vertice2]])

    def layout(self):
        '''
        Aplica el algoritmo de Fruchtermann-Reingold para obtener (y mostrar)
        un layout
        '''
        self.posiciones_random()
        aristas = self.grafo[1]
        plt.ion()

        for i in range(self.iters):
            self.step()
            if self.refresh != 0:
                self.show_graph()
        if self.refresh == 0:
            self.show_graph()
        plt.show  # lo muestra
        plt.ioff()  # lo cierra


def main():
    # Definimos los argumentos de linea de comando que aceptamos
    parser = argparse.ArgumentParser()

    # Verbosidad, opcional, False por defecto
    parser.add_argument(
        '-v', '--verbose',
        action = 'store_true',
        help = 'Muestra mas informacion al correr el programa'
    )
    # Cantidad de iteraciones, opcional, 50 por defecto
    parser.add_argument(
        '--iters',
        type = int,
        help = 'Cantidad de iteraciones a efectuar',
        default = 50
    )
    # Temperatura inicial
    parser.add_argument(
        '--temp',
        type = float,
        help = 'Temperatura inicial',
        default = 100.0
    )
    # Archivo del cual leer el grafo
    parser.add_argument(
        'file_name',
        help = 'Archivo del cual leer el grafo a dibujar'
    )

    args = parser.parse_args()

    # Descomentar abajo para ver funcionamiento de argparse
    print(args.verbose)
    print(args.iters)
    print(args.file_name)
    print(args.temp)
    # return

    # TODO: Borrar antes de la entrega
    grafo1 = ([1, 2, 3, 4, 5, 6, 7],
              [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 1)])

    # Creamos nuestro objeto LayoutGraph
    layout_gr = LayoutGraph(
        grafo1,  # TODO: Cambiar para usar grafo leido de archivo
        iters = args.iters,
        refresh = 1,
        c1 = 0.1,
        c2 = 5.0,
        verbose = args.verbose
    )

    # Ejecutamos el layout
    layout_gr.layout()
    return


if __name__ == '__main__':
    main()
