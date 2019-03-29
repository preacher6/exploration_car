import os
from textbox import TextBox
import numpy as np
import matplotlib.pyplot as plt
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from scipy.linalg import rq
import matplotlib.pyplot as plt

GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def circle_vertex(centro=(0, 0), radio=5, ver=5):
    x = list()
    y = list()
    for i in range(ver):
        t = i*(2*np.pi)/ver
        x.append(float(radio*np.sin(t))+centro[0])
        y.append(float(radio*np.cos(t))+centro[1])
    return x, y

def circle_edges(x, y, z):
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

def rect_vertex(centro=(0, 0), size=(5, 5), h=6):
    vertex = list()
    vertex.append((centro[0] - size[0] / 2, centro[1] - size[1] / 2, 0))
    vertex.append((centro[0] + size[0] / 2, centro[1] - size[1] / 2, 0))
    vertex.append((centro[0] - size[0] / 2, centro[1] + size[1] / 2, 0))
    vertex.append((centro[0] + size[0] / 2, centro[1] + size[1] / 2, 0))
    vertex.append((centro[0] - size[0] / 2, centro[1] - size[1] / 2, h))
    vertex.append((centro[0] + size[0] / 2, centro[1] - size[1] / 2, h))
    vertex.append((centro[0] - size[0] / 2, centro[1] + size[1] / 2, h))
    vertex.append((centro[0] + size[0] / 2, centro[1] + size[1] / 2, h))
    edges = [(0, 1), (0, 2), (0, 4), (3, 1), (3, 2), (3, 7), (6, 2), (6, 4), (6, 7), (5, 1), (5, 4), (5, 7)]
    surfaces = [(0, 2, 6, 4), (0, 1, 5, 4), (1, 3, 7, 5), (2, 3, 7, 6), (0, 1, 3, 2), (4, 5, 7, 6)]
    return  vertex, edges, surfaces

def plot_figure(x, y):
    plt.plot(x, y)
    plt.show()

def Cilinder(verticies, edges, surfaces, colors):
    """Dibujar obstaculos con forma de cilindros"""
    glBegin(GL_QUADS)
    for surface in surfaces:
        x = 0
        for vertex in surface:
            x += 1
            glColor3fv((0.51, 0.52, 0.57))
            glVertex3fv(verticies[vertex])
    glEnd()

def Cube(verticies, edges, surfaces, colors):
    """Dibujar obstaculos con forma de cilindros"""
    glBegin(GL_QUADS)
    for surface in surfaces:
        x = 0
        for vertex in surface:
            x += 1
            glColor3fv((0.1, 0.52, 0.57))
            glVertex3fv(verticies[vertex])
    glEnd()

    """glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glColor3fv((1, 0, 0))
            glVertex3fv(verticies[vertex])
    glEnd()"""

def Car(verticies, edges, surfaces, colors):
    #print(verticies)
    """Dibujar obstaculos con forma de carro"""
    glBegin(GL_QUADS)
    for surface in surfaces:
        x = 0
        for vertex in surface:
            x += 1
            glColor3fv((0.1, 0.52, 0.57))
            glVertex3fv(verticies[vertex])
    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glColor3fv((0, 0, 0))
            glVertex3fv(verticies[vertex])
    glEnd()

def Ground(ground_vertices):
    """Dibujar superficie planp"""
    glBegin(GL_QUADS)
    x = 0
    for vertex in ground_vertices:
        x += 1
        glColor3fv((0.4, 0.43, 0.16))
        glVertex3fv(vertex)

    glEnd()

def transform(lista_posiciones):
    """Transformar de pygame a pyopengl"""
    new_pos = list()
    for posicion in lista_posiciones:
        xgl = (1/5)*posicion[0]-100
        ygl = -(1/5)*posicion[1]+60
        new_pos.append((xgl, ygl))
    return new_pos

def trans_position(punto):
    """Transformar puntos entre espacios"""
    xgl = (1 / 5) * punto[0] - 100
    ygl = -(1 / 5) * punto[1] + 60
    return (xgl, ygl)

def robot_scale(path_image, inicio=(0, 0)):
    """Escalar robot"""
    image = pygame.image.load(path_image)
    image_scale = pygame.transform.rotozoom(image, 0, 0.07)
    rect_image = image_scale.get_rect()
    rect_image.center = inicio
    return image_scale, rect_image

def dibujar_panel(pantalla):
    """Panel de objetos"""
    circulo = pygame.image.load(os.path.join('pics', 'circulo.png'))
    recta_circulo = circulo.get_rect()
    recta_circulo.center = (120, 100)
    cuadro = pygame.image.load(os.path.join('pics', 'recta.png'))
    recta_cuadro = cuadro.get_rect()
    recta_cuadro.center = (120, 180)
    pantalla.blit(cuadro, recta_cuadro)
    pantalla.blit(circulo, recta_circulo)
    return recta_circulo, recta_cuadro

def dibujar_objeto(pantalla, position, elemento, size):
    """Dibujar objeto seleccionado en pantalla"""
    if elemento == 'circulo':
        size = int(size)
        pygame.draw.circle(pantalla, (1, 0, 0), (position[0], position[1]), size*5)
    if elemento == 'cuadro':
        size = (int(size[0]), int(size[1]))
        pygame.draw.rect(pantalla, (1, 0, 0), (position[0]-(size[0]/2)*5, position[1]-(size[1]/2)*5, size[0]*5, size[1]*5))

def circulo_en_espacio(pantalla, posiciones, size):
    """Dibuja circulos area de trabajo"""
    print(size)
    for posicion, radio in zip(posiciones, size):
        pygame.draw.circle(pantalla, (1, 0, 0), (posicion[0], posicion[1]), radio*5)

def recta_en_espacio(pantalla, posiciones, sizes):
    """Dibujar rectas area de trabajo"""
    for posicion, size in zip(posiciones, sizes):
        pygame.draw.rect(pantalla, (1, 0, 0), (posicion[0]-(size[0]/2)*5, posicion[1]-(size[1]/2)*5, size[0]*5, size[1]*5))

def round_base(pos, base=5):
    """Definir centroides en una posicion con valores enteros"""
    outx = (base*round(pos[0]/base))
    outy = (base*round(pos[1]/base))
    out = (outx, outy)
    return out

def build_matriz(matriz, centro_actual, element, size):
    """Rellenar matriz para circulos"""
    if element == 'circulo':
        size = int(size)
        size=size*5
        for i in range(centro_actual[0]-size, centro_actual[0]+size+1):
            for j in range(centro_actual[1]-size, centro_actual[1]+size+1):
                if np.sqrt((i-centro_actual[0])**2+(j-centro_actual[1])**2) < size:
                    matriz[i][j] = 1
    elif element == 'cuadro':
        size = (int(size[0]), int(size[1]))
        matriz[centro_actual[0]:centro_actual[0]+size[0]*10, centro_actual[1]:centro_actual[1]+size[1]*10] = 1

    return matriz

def build_textboxes():
    """Crear textboxes"""
    box_1 = TextBox((100, 430, 100, 20), id="name_con", active=True,
                        clear_on_enter=False, inactive_on_enter=True)
    box_2 = TextBox((100, 460, 100, 20), id="name_con", active=False,
                                clear_on_enter=False, inactive_on_enter=True)
    return box_1, box_2

def build_car(centro, ancho, largo, h=2):
    vertex = list()
    vertex.append((centro[0]-largo/2, centro[1]+ancho/2, 0))
    vertex.append((centro[0]+largo, centro[1]+1, 0))
    vertex.append((centro[0] + largo, centro[1] - 1, 0))
    vertex.append((centro[0]-largo/2, centro[1] - ancho / 2, 0))
    vertex.append((centro[0], centro[1] + ancho / 2, h))
    vertex.append((centro[0] + largo, centro[1] + 1, 1))
    vertex.append((centro[0] + largo, centro[1] - 1, 1))
    vertex.append((centro[0], centro[1] - ancho / 2, h))
    #print(vertex)
    edges = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]
    surfaces = [(0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (0, 3, 7, 4), (0, 1, 2, 3), (4, 5, 6, 7)]
    return vertex, edges, surfaces

def re_vertex(vertex, desp):
    vertex[0] = (vertex[0][0] + desp[0], vertex[0][1] + desp[1], 0)
    vertex[1] = (vertex[1][0] + desp[0], vertex[1][1] + desp[1], 0)
    vertex[2] = (vertex[2][0] + desp[0], vertex[2][1] + desp[1], 0)
    vertex[3] = (vertex[3][0] + desp[0], vertex[3][1] + desp[1], 0)
    vertex[4] = (vertex[4][0] + desp[0], vertex[4][1] + desp[1], 2)
    vertex[5] = (vertex[5][0] + desp[0], vertex[5][1] + desp[1], 1)
    vertex[6] = (vertex[6][0] + desp[0], vertex[6][1] + desp[1], 1)
    vertex[7] = (vertex[7][0] + desp[0], vertex[7][1] + desp[1], 2)
    #print(vertex)
    return vertex


def Walls(walls_vertices):
    glBegin(GL_QUADS)
    for surface in walls_vertices:
        x = 0
        for vertex in surface:
            x += 1
            glColor((0.7, 0.72, 0.57))
            glVertex3fv(vertex)
    glEnd()

def make_walls(ground_vertices):
    walls_vertices = list()
    for index, ground in enumerate(ground_vertices):
        if index < len(ground_vertices)-1:
            walls_vertices.append((ground, ground_vertices[index+1], ground_vertices[index+1][:2]+[10], ground[:2]+[10]))
        else:
            walls_vertices.append((ground, ground_vertices[0], ground_vertices[0][:2]+[10], ground[:2]+[10]))
    return walls_vertices

def main():
    pygame.init()
    pygame.display.set_caption('El Bairon')
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    display = (800, 600)
    pantalla = pygame.display.set_mode(display)  # Define la pantalla
    clock = pygame.time.Clock()
    init = True  # Indica si me encuentro en el ingreso de parametros
    objects_surface = pygame.Surface((150, 300))  # Contiene los objetos a dibujar
    objects_surface.fill(WHITE)
    ground_rect = pygame.Rect(250, 50, 500, 500)
    ground_surface = pygame.Surface((500, 500))  # Espacio donde se ubican los objetos
    plane_matriz = np.zeros((500, 500))  # Matriz que indica posiciones de objetos
    ground_surface.fill(WHITE)
    draw = False
    hold_robot = False
    posiciones_circulos = list()  # Posiciones cilindros
    posiciones_rectas = list()  # Posiciones rectas
    radios = list()  # Radios de circulos
    rect_sizes = list()  # Tamaño de los rectangulos
    pos_ground = (250, 50)  # Posicion plano pygame
    pos_robot = (280, 70)  # Posicion inicial del robot (en pygame)
    robot, recta_robot = robot_scale(os.path.join('pics', 'robot.png'), inicio=pos_robot)
    elemento = None  # Tipo de obstaculo a dibujar
    box_1, box_2 = build_textboxes()
    font = pygame.font.SysFont('Arial', 15)


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
    ground_vertices = [
        [-50, 50, 0],
        [50, 50, 0],
        [50, -50, 0],
        [-50, -50, 0],
    ]
    walls_verticies = make_walls(ground_vertices)
    angulo = 0
    while True:
        for event in pygame.event.get():
            if draw:
                if elemento == 'circulo':
                    box_1.get_event(event)
                elif elemento == 'cuadro':
                    box_1.get_event(event)
                    box_2.get_event(event)
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:  # Cambiar entorno gráfico
                    if init:  # PyopenGL
                        init = False
                        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
                        gluPerspective(45, (display[0] / display[1]), 0, 300)  # Define el espacio de trabajo 250
                        glRotatef(-90, 1, 0, 0)  # Rotacion alrededor de X
                        glRotatef(90, 0, 0, 1)  # Rotacion alrededor de Z
                        new_pos_robot = trans_position(pos_robot)  # Posicion robot (Cámara)

                        vertex_car, edges_car, surfaces_car = build_car(new_pos_robot, 2, 10)
                        glTranslatef(-new_pos_robot[0], -new_pos_robot[1], -3)  # Trasladar el objeto
                        nuevos_circulos = transform(posiciones_circulos)  # Nuevas posiciones para los circulos
                        nuevos_rectangulos = transform(posiciones_rectas)  # Nuevas posiciones para los rectangulos
                        data_circle = list()  # Lista de circulos
                        data_rect = list()  # Lista de rectangulos
                        for posicion, radio in zip(nuevos_circulos, radios):
                            x, y = circle_vertex(centro=(posicion[0], posicion[1]), radio=radio, ver=20)
                            vertices, edges, surfaces = circle_edges(x, y, 10)
                            data_circle.append((vertices, edges, surfaces))
                        for posicion, size in zip(nuevos_rectangulos, rect_sizes):
                            vertices, edges, surfaces = rect_vertex(centro=(posicion[0], posicion[1]), size=size)
                            data_rect.append((vertices, edges, surfaces))
                    else:  # Pygame
                        init = True
                        pygame.display.set_mode(display)
                if event.key == pygame.K_ESCAPE:
                    draw = False
                if not init:
                    if event.key == pygame.K_LEFT:
                        glTranslatef(-5, 0, 0)
                        vertex_car = re_vertex(vertex_car, (5, 0))
                    if event.key == pygame.K_RIGHT:
                        glTranslatef(5, 0, 0)
                        vertex_car = re_vertex(vertex_car, (-5, 0))
                    if event.key == pygame.K_UP:
                        glTranslatef(0, -5, 0)
                        vertex_car = re_vertex(vertex_car, (0, 5))
                    if event.key == pygame.K_DOWN:
                        glTranslatef(0, 5, 0)
                        vertex_car = re_vertex(vertex_car, (0, -5))
                    if event.key == pygame.K_a:
                        glTranslatef(-50, 50, 0)
                        vertex_car = re_vertex(vertex_car, (50, -50))
                        angulo -= 2
                        rot_c = np.array([[np.cos(np.deg2rad(-2)), -np.sin(np.deg2rad(-2))],
                                          [np.sin(np.deg2rad(-2)), np.cos(np.deg2rad(-2))]])
                        print(rot_c)
                        print(vertex_car)
                        for ind, point in enumerate(vertex_car):
                            print('...')
                            print(point)
                            data = rot_c@np.array([point[0], point[1]])
                            print(data)
                            vertex_car[ind] = (data[0], data[1], point[2])
                        #print(vertex_car)
                        glRotatef(2, 0, 0, 1)
                        glTranslatef(50, -50, 0)
                        vertex_car = re_vertex(vertex_car, (-50, 50))
                    if event.key == pygame.K_d:
                        glTranslatef(-50, 50, 0)
                        vertex_car = re_vertex(vertex_car, (50, -50))
                        angulo -= 2
                        rot_c = np.array([[np.cos(np.deg2rad(2)), -np.sin(np.deg2rad(2))],
                                          [np.sin(np.deg2rad(2)), np.cos(np.deg2rad(2))]])
                        print(rot_c)
                        print(vertex_car)
                        for ind, point in enumerate(vertex_car):
                            print('...')
                            print(point)
                            data = rot_c @ np.array([point[0], point[1]])
                            print(data)
                            vertex_car[ind] = (data[0], data[1], point[2])
                        # print(vertex_car)
                        glRotatef(-2, 0, 0, 1)
                        glTranslatef(50, -50, 0)
                        vertex_car = re_vertex(vertex_car, (-50, 50))
                if event.key == pygame.K_m:
                    plt.imshow(plane_matriz.T)
                    plt.show()
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                if draw:  # Posicionar objeto dentro del espacio de trabajo
                    plane_matriz = build_matriz(plane_matriz, (position[0] - 250, position[1] - 50), elemento, size)
                    if ground_rect.collidepoint(position):
                        if elemento == 'circulo':
                            posiciones_circulos.append(position)  # Agregar posicion de objeto a lista
                            radios.append(int(size))
                        elif elemento == 'cuadro':
                            posiciones_rectas.append((position[0], position[1]))  # Agregar posicion de objeto a lista
                            rect_sizes.append((int(size[0]), int(size[1])))

                if not init:  # PyOpenGL
                    if pygame.mouse.get_pressed()[0]:
                        glTranslatef(0, 0, -5)
                    if pygame.mouse.get_pressed()[2]:
                        #glTranslatef(0, 0, 5)
                        modelview = glGetFloatv(GL_MODELVIEW_MATRIX)
                        print(modelview)
                else:  # Pygame
                    if recta_robot.collidepoint(position):  # Clic sobre el robot
                        if hold_robot:  # Si se encuentra reubicando robot -> Detener
                            hold_robot = False
                        else:
                            hold_robot = True  # Variable que permite reubicar robot
                if recta_circulo.collidepoint(position):
                    elemento = 'circulo'
                    draw = True
                    size = 5
                    box_1.buffer = [str(size)]
                if recta_cuadro.collidepoint(position):
                    elemento = 'cuadro'
                    draw = True
                    size = (10, 8)
                    box_1.buffer = [str(size[0])]
                    box_2.buffer = [str(size[1])]

        abs_position = pygame.mouse.get_pos()
        if init:  # 2D
            pantalla.fill(GRAY)
            pantalla.blit(objects_surface, (50, 50))
            pantalla.blit(ground_surface, pos_ground)
            pantalla.blit(robot, recta_robot)
            if hold_robot:  # Arrastrar robot
                recta_robot.center = abs_position
                pos_robot = abs_position
            recta_circulo, recta_cuadro = dibujar_panel(pantalla)
            if draw:
                if elemento == 'circulo':
                    box_1.update()
                    box_1.draw(pantalla)
                    size = "".join(box_1.buffer)
                    pantalla.blit(font.render('Radio:', True, (0, 0, 0)), (60, 430))
                elif elemento == 'cuadro':
                    box_1.update()
                    box_1.draw(pantalla)
                    box_2.update()
                    box_2.draw(pantalla)
                    size = ("".join(box_1.buffer), "".join(box_2.buffer))
                    pantalla.blit(font.render('Largo:', True, (0, 0, 0)), (60, 430))
                    pantalla.blit(font.render('Ancho:', True, (0, 0, 0)), (60, 460))
                if ground_rect.collidepoint(abs_position):
                    dibujar_objeto(pantalla, abs_position, elemento, size)
            if posiciones_circulos:
                circulo_en_espacio(pantalla, posiciones_circulos, radios)
            if posiciones_rectas:
                recta_en_espacio(pantalla, posiciones_rectas, rect_sizes)
        else:  # 3D
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            Ground(ground_vertices)
            Walls(walls_verticies)
            for data in data_circle:
                Cilinder(data[0], data[1], data[2], colors)
            for data in data_rect:
                Cube(data[0], data[1], data[2], colors)
            #vertex_car, edges_car, surfaces_car = build_car(new_pos_robot, 5, 7)
            Car(vertex_car, edges_car, surfaces_car, colors)

        clock.tick(60)
        pygame.display.flip()


if __name__.endswith("__main__"):
    main()
