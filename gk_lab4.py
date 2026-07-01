#!/usr/bin/env python3
import sys
import math
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
viewer = [0.0, 0.0, 10.0]
theta = 0.0   
gamma = 0.0  
pix2angle = 1.0
left_mouse_button_pressed = 0
right_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0
R = 10.0
R_min = 2.0
R_max = 40.0
scale = 1.0
zad = 3


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x, delta_y, mouse_x_pos_old, mouse_y_pos_old
    delta_x = x_pos - mouse_x_pos_old
    delta_y = y_pos - mouse_y_pos_old
    mouse_x_pos_old = x_pos
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed, right_mouse_button_pressed
    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    elif button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_RELEASE:
        left_mouse_button_pressed = 0
    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        right_mouse_button_pressed = 1
    elif button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_RELEASE:
        right_mouse_button_pressed = 0


def keyboard_key_callback(window, key, scancode, action, mods):
    global zad
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    if key == GLFW_KEY_N and action == GLFW_PRESS:
        if zad == 1:
            zad = 3
        else:
            zad = 1


def render(time):
    global theta, gamma, scale, R, zad
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    if zad == 1:
        gluLookAt(viewer[0], viewer[1], viewer[2],
                  0.0, 0.0, 0.0,
                  0.0, 1.0, 0.0)
        if left_mouse_button_pressed:
            theta += delta_x * pix2angle
            gamma += delta_y * pix2angle
        glRotatef(theta, 0.0, 1.0, 0.0)
        glRotatef(gamma, 1.0, 0.0, 0.0)
        if right_mouse_button_pressed:
            scale += delta_y * 0.01
            if scale < 0.1: scale = 0.1
            if scale > 8.0: scale = 8.0
        glScalef(scale, scale, scale)

    else:
        if right_mouse_button_pressed:
            R -= delta_y * 0.05
            if R < R_min: R = R_min
            if R > R_max: R = R_max
        if left_mouse_button_pressed:
            theta += delta_x * pix2angle
            gamma += delta_y * pix2angle
        theta = theta % 360.0
        gamma = gamma % 360.0
        theta_rad = math.radians(theta)
        gamma_rad = math.radians(gamma)
        x_eye = R * math.cos(gamma_rad) * math.cos(theta_rad)
        y_eye = R * math.sin(gamma_rad)
        z_eye = R * math.cos(gamma_rad) * math.sin(theta_rad)
        up_y = 1.0
        if gamma_rad > math.pi/2 and gamma_rad < 3*math.pi/2:
            up_y = -1.0
        gluLookAt(x_eye, y_eye, z_eye,
                  0.0, 0.0, 0.0,
                  0.0, up_y, 0.0)
    axes()
    example_object()
    glFlush()


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


def example_object():
    glColor3f(0.1, 0.5, 0.9)
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    glRotatef(90, 1.0, 0.0, 0.0)
    glRotatef(-90, 0.0, 1.0, 0.0)
    gluSphere(quadric, 1.5, 10, 10)
    glTranslatef(0.0, 0.0, 1.1)
    gluCylinder(quadric, 1.0, 1.5, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, -1.1)
    glTranslatef(0.0, 0.0, -2.6)
    gluCylinder(quadric, 0.0, 1.0, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, 2.6)
    glRotatef(90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(-90, 1.0, 0.0, 1.0)
    glRotatef(-90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(90, 1.0, 0.0, 1.0)
    glRotatef(90, 0.0, 1.0, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    gluDeleteQuadric(quadric)


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(70, 1.0, 0.1, 300.0)
    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def main():
    if not glfwInit():
        sys.exit(-1)
    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)
    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
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
