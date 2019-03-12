import numpy as np
import matplotlib.pyplot as plt
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

def make_vertex(centro=(0, 0), radio=5, ver=5):
    x = list()
    y = list()
    for i in range(ver):
        t = i*(2*np.pi)/ver
        x.append(float(radio*np.sin(t))+centro[0])
        y.append(float(radio*np.cos(t))+centro[1])
    return x, y

def make_edges(x, y, z):
    lista_vertices = []
    for i, j in zip(x, y):  # Vertices parte inferior
        lista_vertices.append((i, j, 0))
    for i, j in zip(x, y):  # Vertices parte superior
        lista_vertices.append((i, j, z))
    lista_edges = list()
    lista_surfaces = list()
    n = len(lista_vertices)
    for index in range(int(n/2)-1):  # Conexiones parte superior
        lista_edges.append((index, index+1))
    lista_edges.append((index+1, 0))
    for index in range(int(n/2), n-1):  # Conexiones parte inferior
        lista_edges.append((index, index + 1))
    lista_edges.append((index+1, int(n/2)))

    for index in range(int(n/2)):  # Conexiones entre parte superior e inferior
        lista_edges.append((index, index+int(n/2)))
        lista_surfaces.append((index, index+int(n/2), index+int(n/2)+1, index+1))
    lista_surfaces.pop()
    lista_surfaces.append((index, index+int(n/2), int(n/2), 0))
    return lista_vertices, lista_edges, lista_surfaces

def plot_figure(x, y):
    plt.plot(x, y)
    plt.show()

def Cube(verticies, edges, surfaces, colors):
    glBegin(GL_QUADS)
    for surface in surfaces:
        x = 0
        for vertex in surface:
            x += 1
            glColor((1, 0, 0))
            glVertex3fv(verticies[vertex])
    glEnd()

    """glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glColor3fv((1, 0, 0))
            glVertex3fv(verticies[vertex])
    glEnd()"""


def Ground(ground_vertices):
    glBegin(GL_QUADS)
    x = 0
    for vertex in ground_vertices:
        x += 1
        glColor3fv((0, 1, 1))
        glVertex3fv(vertex)

    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    x, y = make_vertex(centro=(25, 25), ver=20)
    vertices, edges, surfaces = make_edges(x, y, 10)
    x2, y2 = make_vertex(radio=7, ver=40)
    vertices2, edges2, surfaces2 = make_edges(x2, y2, 5)
    gluPerspective(45, (display[0] / display[1]), 1, 300)  # Define el espacio de trabajo 250

    glRotatef(-90, 1, 0, 0)
    glTranslatef(0, 0, -5)  # define la lejania
    colors = (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (0, 1, 0),
        (1, 1, 1),
        (0, 1, 1),
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (1, 0, 0),
        (1, 1, 1),
        (0, 1, 1),
    )
    ground_vertices = (
        (-40, 50, 0),
        (40, 50, 0),
        (40, -50, 0),
        (-40, -50, 0),

    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    glTranslatef(-0.5, 0, 0)
                if event.key == pygame.K_RIGHT:
                    glTranslatef(0.5, 0, 0)
                if event.key == pygame.K_UP:
                    glTranslatef(0, -1, 0)
                if event.key == pygame.K_DOWN:
                    glTranslatef(0, 1, 0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pressed())
                if pygame.mouse.get_pressed()[0]:
                    glTranslatef(0, 0, -1.0)

                if pygame.mouse.get_pressed()[2]:
                    glTranslatef(0, 0, 1.0)

        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Ground(ground_vertices)
        Cube(vertices, edges, surfaces, colors)
        Cube(vertices2, edges2, surfaces2, colors)
        pygame.display.flip()
        pygame.time.wait(10)



if __name__.endswith("__main__"):
    main()