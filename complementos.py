#! /usr/bin/python

# 6ta Practica Laboratorio
# Complementos Matematicos I
# Ejemplo parseo argumentos

# CONSTANTES


import argparse
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
from random import uniform
from random import random


def leer_archivo(nombreArchivo):
    f = open(nombreArchivo, "r")
    grafo = [[],[]]
    tupla = f.readlines()
    cantidadVertices = int(tupla[0].rstrip("\n"))
    for i in range(0, cantidadVertices):
        grafo[0].append(tupla[i+1].rstrip("\n"))
    for j in range(cantidadVertices+1, len(tupla)):
        grafo[1].append(tupla[j].split())
    print(grafo)
    return grafo

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
        self.vertices = grafo[0]
        self.aristas = grafo[1]

        # Inicializo estado
        # Completar
        self.posicion_x = {}  # Diccionario, la clave es el vertice el valor la posición x
        self.posicion_y = {}  # Diccionario, la clave es el vertice el valor la posición y
        self.fuerzas = {}
        self.acum_x = {}
        self.acum_y = {}
        self.t = 20000000
        self.ancho = 1000
        self.epsilon = 0.5
        self.g = 0.5 # Constante de gravedad

        # Guardo opciones
        self.iters = iters
        self.verbose = verbose
        # TODO: faltan opciones
        self.refresh = refresh
        self.c1 = c1
        self.c2 = c2


    def posiciones_random(self):  #Está bien
        for vertice in self.vertices:
            self.posicion_x[vertice] = uniform(0, self.ancho)
            self.posicion_y[vertice] = uniform(0, self.ancho)

    def distancia(self, vertice0, vertice1):  #Está bien
        d = sqrt((self.posicion_x[vertice0] - self.posicion_x[vertice1])**2 + (self.posicion_y[vertice0] - self.posicion_y[vertice1])** 2)
        return d

    def mul_escalar(self, vector, e):  #Está bien
        v1 = [vector[0] * e, vector[1] * e]
        return v1

    def fuerza_atraccion(self, d):  #Está bien
        k = self.c2 * sqrt((self.ancho*self.ancho) / len(self.vertices))
        f = d**2 / k
        return f

    def fuerza_repulsion(self, d):  #Está bien
        k = self.c1 * sqrt((self.ancho*self.ancho) / len(self.vertices))
        return k**2 / d

    def inicializar_acumuladores(self): #Está bien
        for vertice in self.vertices:
            self.acum_x[vertice] = 0
            self.acum_y[vertice] = 0

    def calcular_fuerza_atraccion(self):  #Está bien
        for arista in self.aristas:
            d = self.distancia(arista[0], arista[1])
            mod_fa = self.fuerza_atraccion(d)

            # Consideramos el caso de divisiones por 0
            while (d < self.epsilon):
                f = uniform(0, 1.00)
                self.posicion_x[arista[0]] += f
                self.posicion_y[arista[0]] += f
                self.posicion_x[arista[1]] -= f
                self.posicion_y[arista[1]] -= f
                d = self.distancia(arista[0], arista[1])

            mod_fa = self.fuerza_atraccion(d)
            fx = (mod_fa * (self.posicion_x[arista[1]] - self.posicion_x[arista[0]])) / d
            fy = (mod_fa * (self.posicion_y[arista[1]] - self.posicion_y[arista[0]])) / d

            self.acum_x[arista[0]] += fx
            self.acum_y[arista[0]] += fy
            self.acum_x[arista[1]] -= fx
            self.acum_y[arista[1]] -= fy

    def calcular_fuerza_repulsion(self): #Está bien
        for vertice1 in self.vertices:
            for vertice2 in self.vertices:
                    if vertice1 != vertice2:
                        d = self.distancia(vertice1, vertice2)

                        # Consideramos el caso de divisiones por 0
                        while (d < self.epsilon):
                            f = uniform(0,1.00)
                            self.posicion_x[vertice1] += f
                            self.posicion_y[vertice1] += f
                            self.posicion_x[vertice2] -= f
                            self.posicion_y[vertice2] -= f
                            d = self.distancia(vertice1, vertice2)

                        mod_fa = self.fuerza_repulsion(d)
                        fx = (mod_fa * (self.posicion_x[vertice2] - self.posicion_x[vertice1])) / d
                        fy = (mod_fa * (self.posicion_y[vertice2] - self.posicion_y[vertice1])) / d

                        self.acum_x[vertice1] -= fx
                        self.acum_y[vertice1] -= fy
                        self.acum_x[vertice2] += fx
                        self.acum_y[vertice2] += fy



    def actualizar_posiciones(self):  #Está bien, pero pensar si funciona cuando se va de los límites de la pantalla.
        for vertice in self.vertices:
            fx = self.acum_x[vertice]
            fy = self.acum_y[vertice]
            modulo_f = sqrt(fx**2 + fy**2)
            if modulo_f > self.t:
                fx = fx / modulo_f * self.t
                fy = fy / modulo_f * self.t
                self.acum_x[vertice] = fx
                self.acum_y[vertice] = fy

        #    print(vertice, self.posicion_x[vertice], self.posicion_y[vertice], fx, fy)
            nueva_posicion_x = self.posicion_x[vertice] + self.acum_x[vertice]
            nueva_posicion_y = self.posicion_y[vertice] + self.acum_y[vertice]
            if (nueva_posicion_x > self.ancho):
                self.posicion_x[vertice] = self.ancho - self.epsilon
            elif (nueva_posicion_x < 0):
                self.posicion_x[vertice] = 0 + self.epsilon
            else:
                self.posicion_x[vertice] = nueva_posicion_x
            if (nueva_posicion_y > self.ancho):
                self.posicion_y[vertice] = self.ancho - self.epsilon
            elif (nueva_posicion_y < 0):
                self.posicion_y[vertice] = 0 + self.epsilon
            else:
                self.posicion_y[vertice] = nueva_posicion_y
        #    print(vertice, self.posicion_x[vertice], self.posicion_y[vertice], fx, fy)

    def calcular_fuerza_gravedad(self):  #Está bien.
        centro = self.ancho / 2
        for vertice in self.vertices:

            d = sqrt((self.posicion_x[vertice] - centro)**2 + (self.posicion_y[vertice] - centro)** 2)

            #Consideramos el caso de divisiones por 0
            while d < self.epsilon:
                f = random.random()
                self.posicion_x[vertice] += f
                self.posicion_y[vertice] += f
                d = sqrt((self.posicion_x[vertice] - centro)**2 + (self.posicion_y[vertice] - centro)** 2)

            fx = ((self.g * (self.posicion_x[vertice] - centro)) / d)
            fy = ((self.g * (self.posicion_y[vertice] - centro)) / d)
            self.acum_x[vertice] -= fx
            self.acum_y[vertice] -= fy

    def actualizar_temperatura(self):  #Está bien.
        self.t = self.t * self.g  # Multiplicamos por la constante definida.

    def step(self):
        self.inicializar_acumuladores()
        self.calcular_fuerza_atraccion()
        self.calcular_fuerza_repulsion()
        self.calcular_fuerza_gravedad()
        self.actualizar_posiciones()
        self.actualizar_temperatura()

    def show_graph(self):
        plt.pause(0.0001)
        x = [self.posicion_x[i] for i in self.grafo[0]]
        y = [self.posicion_y[i] for i in self.grafo[0]]

        plt.clf() #Limpia la pantalla.
        axes = plt.gca() #gca viene de get current axes.
        axes.set_xlim([0, self.ancho])
        axes.set_ylim([0, self.ancho])
        plt.scatter(x, y)  #Dibuja los puntos.
        for arista in self.aristas:
            vertice1 = arista[0]
            vertice2 = arista[1]
            plt.plot((self.posicion_x[vertice1], self.posicion_x[vertice2]),
                     (self.posicion_y[vertice1], self.posicion_y[vertice2]))

    def layout(self):
        '''
        Aplica el algoritmo de Fruchtermann-Reingold para obtener (y mostrar)
        un layout
        '''
        self.posiciones_random()
        plt.ion()

        for i in range(self.iters):
            if self.refresh != 0 and i % self.refresh == 0:  #Ya que imprime cada determinadas iteraciones.
                    self.step()
                    self.show_graph()
            if self.refresh == 0:
                self.show_graph()
        plt.ioff()  # lo cierra
        plt.show()  # lo muestra

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
        default = 200
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


    # Creamos nuestro objeto LayoutGraph
    layout_gr = LayoutGraph(
        leer_archivo(args.file_name),
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
