#!/usr/bin/env python3
import sys
import math
import random
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def axes():
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)  
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)
    glColor3f(0.0, 1.0, 0.0)  
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)
    glColor3f(0.0, 0.0, 1.0)  
    glVertex3f(0.0, 0.0, -5.0)  
    glVertex3f(0.0, 0.0, 5.0)
    glEnd()


def x(u, v): 
    x = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * math.cos(math.pi*v)
    return x

def y(u, v):
    y = (160 * u**4 - 320 * u**3 + 160 * u**2 - 5)
    return y

def z(u, v):
    z = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * math.sin(math.pi*v)
    return z 

def spin(angle):
    glRotatef(angle, 0.0, 0.0, 1.0)
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 1.0)


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    spin(time * 150 / 3.1415) 
    axes()
    tab = [[[0] * 3 for i in range(25)] for j in range(25)]
    for i in range (25):
        for j in range (25):
                u=i/24
                v=j/24
                x2=x(u,v)
                y2=y(u,v)
                z2=z(u,v)
                tab[i][j] = [x2,y2,z2]


    glBegin(GL_POINTS) # zadanie 1 - punkty
    #glBegin(GL_LINES) # zadanie 2 - linie
    #glBegin(GL_TRIANGLES) # zadanie 3 - trojkąty
    #glBegin(GL_TRIANGLE_STRIP) # zadanie 4 - prymityw paskowy


            # ODKOMENTOWAĆ JEDNĄ FUNKCJĘ DO POPRAWNEGO WYWOŁANIA 

    glColor3f(0.9, 0.95, 0.9)
    for i in range(24):
        for j in range(24):
            
            
            # zadanie 1 - punkty
            glVertex3f(tab[i][j][0], tab[i][j][1], tab[i][j][2])
            
            

            '''
            # zadanie 2 - linie
            glVertex3f(tab[i][j][0], tab[i][j][1], tab[i][j][2])
            glVertex3f(tab[i+1][j][0], tab[i+1][j][1], tab[i+1][j][2])
            glVertex3f(tab[i][j][0], tab[i][j][1], tab[i][j][2])
            glVertex3f(tab[i][j+1][0], tab[i][j+1][1], tab[i][j+1][2])
            '''
    

            '''
            # zadanie 3 - trojkaty
            random.seed() 
            c1 = random.random()
            c2 = random.random()
            c3 = random.random()
            c4 = random.random()
            c5 = random.random()
            c6 = random.random()
            c7 = random.random()
            c8 = random.random()
            c9 = random.random()
            c10 = random.random()
            c11 = random.random()
            c12 = random.random()
            c13 = random.random()
            c14 = random.random()
            c15 = random.random()
            c16 = random.random()
            c17 = random.random()
            c18 = random.random()
            glColor3f(c1, c2, c3)
            glVertex3f(tab[i][j][0], tab[i][j][1], tab[i][j][2])
            glColor3f(c4, c5, c6)
            glVertex3f(tab[i+1][j][0], tab[i+1][j][1], tab[i+1][j][2])
            glColor3f(c7, c8, c9)
            glVertex3f(tab[i][j+1][0], tab[i][j+1][1], tab[i][j+1][2])
            glColor3f(c10, c11, c12)
            glVertex3f(tab[i+1][j+1][0], tab[i+1][j+1][1], tab[i+1][j+1][2])
            glColor3f(c13, c14, c15)
            glVertex3f(tab[i+1][j][0], tab[i+1][j][1], tab[i+1][j][2])
            glColor3f(c16, c17, c18)
            glVertex3f(tab[i][j+1][0], tab[i][j+1][1], tab[i][j+1][2])
            '''

                    
            '''
            #zadanie 4 - prymityw paskowy
            glColor3f(0.4, 0.1, 0.9) 
            glVertex3f(tab[i][j][0], tab[i][j][1], tab[i][j][2])
            glColor3f(0.5, 0.3, 0.7)
            glVertex3f(tab[i+1][j][0], tab[i+1][j][1], tab[i+1][j][2])
            glColor3f(1.0, 0.6, 0.5)
            glVertex3f(tab[i][j+1][0], tab[i][j+1][1], tab[i][j+1][2])
            glColor3f(0.1, 1.0, 0.3)
            glVertex3f(tab[i+1][j+1][0], tab[i+1][j+1][1], tab[i+1][j+1][2])
            '''
            
    glEnd()
    glFlush()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height
    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()
    if width <= height:
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)
    window = glfwCreateWindow(450, 450, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)
    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)
    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()
    glfwTerminate()

if __name__ == '__main__':
    main()
