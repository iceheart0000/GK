#!/usr/bin/env python3
import sys
import math
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

viewer = [0.0, 0.0, 10.0]
theta = 0.0
pix2angle = 1.0
piy2angle = 1.0
phi = 0.0
egg_theta = 0.0
egg_phi = 0.0
left_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0
R = 5.0  
show_normals = False

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

light_ambient1 = [0.0, 0.0, 0.1, 1.0]
light_diffuse1 = [0.0, 0.0, 1.0, 1.0] 
light_specular1 = [1.0, 1.0, 1.0, 1.0]
light_position1 = [-10.0, 5.0, 5.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

light_components = {
    'ambient': [0.1, 0.1, 0.0, 1.0],
    'diffuse': [0.8, 0.8, 0.0, 1.0],
    'specular': [1.0, 1.0, 1.0, 1.0]
}
current_light_component = 'ambient' 
selected_color_index = 0
N = 20  
egg_mesh = [] 


def oblicz_pozycje(u, v):
    pi = math.pi
    x = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * math.cos(pi * v)
    y = (160 * u**4 - 320 * u**3 + 160 * u**2 - 5)
    z = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * math.sin(pi * v)
    return [x, y, z]

def oblicz_normal(u, v):
    pi = math.pi
    xu = (-450 * u**4 + 900 * u**3 - 810 * u**2 + 360 * u - 45) * math.cos(pi * v)
    xv = pi * (90 * u**5 - 225 * u**4 + 270 * u**3 - 180 * u**2 + 45 * u) * math.sin(pi * v)
    yu = 640 * u**3 - 960 * u**2 + 320 * u
    yv = 0
    zu = (-450 * u**4 + 900 * u**3 - 810 * u**2 + 360 * u - 45) * math.sin(pi * v)
    zv = -pi * (90 * u**5 - 225 * u**4 + 270 * u**3 - 180 * u**2 + 45 * u) * math.cos(pi * v)

    nx = yu * zv - zu * yv
    ny = zu * xv - xu * zv
    nz = xu * yv - yu * xv

    length = math.sqrt(nx**2 + ny**2 + nz**2)
    if length > 0:
        nx /= length
        ny /= length
        nz /= length
    else:
        nx, ny, nz = 0, 1, 0 
    if u > 0.5:
        nx = -nx
        ny = -ny
        nz = -nz
    return [nx, ny, nz]


def zakres(value, min_val, max_val):
    return max(min(value, max_val), min_val)


def update_light():
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_components['ambient'])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_components['diffuse'])
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_components['specular'])
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)


def update_light_color(delta):
    global current_light_component, selected_color_index
    light_components[current_light_component][selected_color_index] = zakres(
        light_components[current_light_component][selected_color_index] + delta, 0.0, 1.0
    )
    update_light()
    comp_name = current_light_component.upper()
    channel_name = ['RED', 'GREEN', 'BLUE', 'ALPHA'][selected_color_index]
    val = light_components[current_light_component][selected_color_index]
    print(f"Zmieniono {comp_name} -> {channel_name}: {val:.2f}")


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)
 
    glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient1)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse1)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular1)
    glLightfv(GL_LIGHT1, GL_POSITION, light_position1)
    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic)
    
    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)

    global egg_mesh
    egg_mesh = [[None for _ in range(N)] for _ in range(N)]
    
    for i in range(N):
        for j in range(N):
            u = i / (N - 1)
            v = j / (N - 1)
            pos = oblicz_pozycje(u, v)
            norm = oblicz_normal(u, v)
            egg_mesh[i][j] = {'pos': pos, 'norm': norm}


def shutdown():
    pass


def render(time):
    global theta, phi, egg_theta, egg_phi, light_position, R, show_normals
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    
    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * piy2angle

    light_x = R * math.cos(2 * math.pi * theta / 360) * math.cos(2 * math.pi * phi / 360)
    light_y = R * math.sin(2 * math.pi * phi / 360)
    light_z = R * math.sin(2 * math.pi * theta / 360) * math.cos(2 * math.pi * phi / 360)
    
    light_position = [light_x, light_y, light_z, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glPushMatrix()
    glRotatef(egg_theta, 0.0, 1.0, 0.0) 
    glRotatef(egg_phi, 1.0, 0.0, 0.0)
    
    glBegin(GL_TRIANGLES)
    for i in range(N - 1):
        for j in range(N - 1):
            p1 = egg_mesh[i][j]
            p2 = egg_mesh[i+1][j]
            p3 = egg_mesh[i+1][j+1]
            p4 = egg_mesh[i][j+1]

            glNormal3fv(p1['norm'])
            glVertex3fv(p1['pos'])
            glNormal3fv(p2['norm'])
            glVertex3fv(p2['pos'])
            glNormal3fv(p4['norm'])
            glVertex3fv(p4['pos'])

            glNormal3fv(p2['norm'])
            glVertex3fv(p2['pos'])
            glNormal3fv(p3['norm'])
            glVertex3fv(p3['pos'])
            glNormal3fv(p4['norm'])
            glVertex3fv(p4['pos'])
    glEnd()

    if show_normals:
        glDisable(GL_LIGHTING)
        glColor3f(0.0, 0.5, 1.0)
        
        glBegin(GL_LINES)
        for i in range(N):
            for j in range(N):
                p = egg_mesh[i][j]
                pos = p['pos']
                norm = p['norm']

                glVertex3fv(pos)
                glVertex3f(pos[0] + norm[0] * 0.5, 
                           pos[1] + norm[1] * 0.5,
                           pos[2] + norm[2] * 0.5)
        glEnd()
        glEnable(GL_LIGHTING) 

    glPopMatrix()

    glPushMatrix()
    glTranslate(light_x, light_y, light_z)
    glDisable(GL_LIGHTING) 
    glColor3f(1.0, 1.0, 0.0)
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 0.2, 6, 5)
    gluDeleteQuadric(quadric)
    glEnable(GL_LIGHTING)
    glPopMatrix()
    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    if width == 0: width = 1
    if height == 0: height = 1
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


def keyboard_key_callback(window, key, scancode, action, mods):
    global selected_color_index, current_light_component, show_normals

    if action == GLFW_PRESS or action == GLFW_REPEAT:
        if key == GLFW_KEY_ESCAPE:
            glfwSetWindowShouldClose(window, GLFW_TRUE)

        if key == GLFW_KEY_N:
            show_normals = not show_normals
            state = "WŁĄCZONE" if show_normals else "WYŁĄCZONE"
            print(f"Wizualizacja wektorów normalnych: {state}")

        if key == GLFW_KEY_1:
            current_light_component = 'ambient'
            print("Zmiana skladowej: AMBIENT")
        elif key == GLFW_KEY_2:
            current_light_component = 'diffuse'
            print("Zmiana skladowej: DIFFUSE")
        elif key == GLFW_KEY_3:
            current_light_component = 'specular'
            print("Zmiana skladowej: SPECULAR")
        
        elif key == GLFW_KEY_R:
            selected_color_index = 0
            print("Wybrano: Czerwony")
        elif key == GLFW_KEY_G:
            selected_color_index = 1
            print("Wybrano: Zielony")
        elif key == GLFW_KEY_B:
            selected_color_index = 2
            print("Wybrano: Niebieski")
        elif key == GLFW_KEY_A:
            selected_color_index = 3
            print("Wybrano: ALPHA")

        elif key == GLFW_KEY_UP:
            update_light_color(0.1)
        elif key == GLFW_KEY_DOWN:
            update_light_color(-0.1)


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x, delta_y, mouse_x_pos_old, mouse_y_pos_old
    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos
    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed
    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)
    window = glfwCreateWindow(600, 600, __file__, None, None)
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