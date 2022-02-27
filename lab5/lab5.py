#!/usr/bin/env python3
import sys
import math
import numpy as np
from glfw.GLFW import *
import random
from OpenGL.GL import *
from OpenGL.GLU import *

#sterowanie tablicami
index = 0
color_change_rate = 0.1
# zmienne do jaja
N = 20
RED = random.uniform(0, 255)/255
BLUE = random.uniform(0,255)/255
GREEN = random.uniform(0, 255)/255
v_array = np.linspace(0, 1, num=N)
u_array = np.linspace(0, 1, num=N)

normalized_vector_list = []

viewer = [0.0, 0.0, 10.0]

#zmienna do wzorku 
R = 1.0
#zmienne do obliczania katow
phi = 0.0 
theta = 0.0
pix2angle = 1.0
object_theta = 0.0

# zmienne do obslugi obrotu
right_mouse_button_pressed = 0 
left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0
mouse_y_pos_old = 0
delta_y = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 10.0, 10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001


show_lines =True
#Wyliczanie wspolrzednych ruchu  w obrocie
def count_points(R ,theta, phi):
    theta = math.radians(theta)
    phi = math.radians(phi)
    x_eye = R * math.cos(theta) * math.cos(phi) 
    y_eye = R * math.sin(phi)
    z_eye = R * math.sin(theta) * math.cos(phi)
    return x_eye, y_eye, z_eye



def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    


# pierwsze zrodlo swiatla
def light_source():



    x, y , z = count_points(10, theta, phi )
    light_position[0] = x
    light_position[1] = y
    light_position[2] = z

    print(light_position)
   
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)
    print(light_ambient)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

# drugie zrodlo swiatla
def light_source_2():
    light_position_v2 = [0.0, -10.0, -10.0, 1.0]
    light_ambient_v2  = [0.3, 0.0, 0.5, 1.0]
    light_diffuse_v2  = [0.0, 0.3, 0.0, 1.0]
    light_specular_v2 =   [1.0, 0.0, 1.0, 1.0]



    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient_v2)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse_v2)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular_v2)
    glLightfv(GL_LIGHT1, GL_POSITION, light_position_v2)

    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT1)


# example sphere to work with 
def sphere(theta):
    glRotatef(theta, 0.0, 1.0, 0.0)
    #glRotatef(phi, 1.0, 0.0, 0.0 )
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 3.0, 10, 10)
    gluDeleteQuadric(quadric)
# for visualization of light in 4.0
def linesphere(theta, phi):
    x, y , z = light_position[0], light_position[1], light_position[2]
    glTranslatef(x, y , z)
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 0.5, 6, 5)
    glTranslatef(-x, -y , -z)
    gluDeleteQuadric(quadric)

# egg for task for 4.5 
def count_points_egg():
    tab= np.zeros((N, N, 3))
    for v in range(N):
        for u in range(N):
            x= (-90 * u_array[u]**5 + 225 * u_array[u]**4 - 270 * u_array[u]**3 + 180 * u_array[u]**2 - 45 * u_array[u]) * math.cos( math.pi*v_array[v])
            y= 160 * u_array[u]**4 - 320 * u_array[u]**3 + 160 * u_array[u]**2 - 5
            z= (-90 * u_array[u]**5 + 225 * u_array[u]**4 - 270 * u_array[u]**3 + 180 * u_array[u]**2 - 45 * u_array[u]) * math.sin( math.pi*v_array[v])
            tab[u, v,0] = x
            tab[u,v,1] = y
            tab[u,v,2] = z 
    return tab


def count_u_x_y_z(u, v):
    x = (-450 * u**4 + 900 * u**3 -810 * u**2 +360 * u -45)*math.cos(math.pi*v)
    y = (640 * u**3 - 960 * u**2 + 320 * u)
    z = (-450 * u**4 + 900 * u**3 -810 * u**2 +360 * u -45)*math.sin(math.pi*v)
    return x, y, z
def count_v_x_y_z(u,v):
    x = math.pi*(90 * u**5 -225 * u**4 +270 * u**3 - 180 * u**2 + 45 * u)*math.sin(math.pi*v)
    y = 0
    z = -math.pi*(90 * u**5 -225 * u**4 +270 * u**3 - 180 * u**2 + 45 * u)*math.cos(math.pi*v)
    return x, y, z
def normalize_vector(x, y, z):
    length = math.sqrt(x**2 + y**2 +z**2)
    if length == 0:
       length =1
    return np.array([x/length, y/length, z/length])


def count_vector():
    global normalized_vector_list
    for v in range(N):
        for u in range(N):
            x_u, y_u, z_u = count_u_x_y_z(u_array[u], v_array[v])
            x_v, y_v, z_v = count_v_x_y_z(u_array[u], v_array[v])
            vector = [y_u*z_v - z_u*y_v , z_u*x_v - x_u*z_v, x_u*y_v - y_u*x_v]
            normalised_vector = normalize_vector(vector[0], vector[1], vector[2])
            if u > N/2:   
                normalized_vector_list[u, v] = -1*normalised_vector    
            else:
                normalized_vector_list[u, v] = normalised_vector
 
array_3d_corrected = count_points_egg()
normalized_vector_list = np.zeros((N, N, 3))
count_vector()
print(normalized_vector_list)
def shutdown():
    pass


def generate_egg_with_triangles(theta):
    
        glRotatef(theta, 0.0, 1.0, 0.0)
        for i in range(N -1):
            for j in range(N -1) :
            # trojkat 
                # 1 trojkat
                glBegin(GL_TRIANGLES)
                glColor3f(RED, BLUE, GREEN)
                glNormal3fv(normalized_vector_list[i][j])
                glVertex3fv(array_3d_corrected[i,j])
                
                glNormal3fv(normalized_vector_list[1+i][j])
                glVertex3fv(array_3d_corrected[1+i, j])
               
                glNormal3fv(normalized_vector_list[i][j+1])
                glVertex3fv(array_3d_corrected[i, j+1])
                glEnd()
                # 2 trojkat 
                glBegin(GL_TRIANGLES)
                glColor3f(BLUE, GREEN, RED)
                
                glNormal3fv(normalized_vector_list[i+1][j+1])
                glVertex3fv(array_3d_corrected[i+1,j+1])
                
                glNormal3fv(normalized_vector_list[i+1][j])
                glVertex3fv(array_3d_corrected[i+1,j])
               
                glNormal3fv(normalized_vector_list[i][j+1])
                glVertex3fv(array_3d_corrected[i,j+1])
                glEnd()


def draw_vector_line():
    glBegin(GL_LINES)
    for i in range(N ):
        for j in range(N ) :
            glVertex3fv(array_3d_corrected[i][j])
            glVertex3fv(normalized_vector_list[i][j]+array_3d_corrected[i][j])
    glEnd()


def render(time):
    global theta, phi, object_theta

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle
    if right_mouse_button_pressed:
        object_theta += delta_x * pix2angle
   
    generate_egg_with_triangles(object_theta)
    if show_lines:
        draw_vector_line()
    #sphere(object_theta)
    linesphere(theta, phi)
    light_source()
    #light_source_2()
    glFlush()



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


def keyboard_key_callback(window, key, scancode, action, mods):
    global index, color_change_rate, show_lines
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    if key == GLFW_KEY_1 and action == GLFW_PRESS:
        index = (index+1 )%3
        #w gore kolor
    if key == GLFW_KEY_2 and action == GLFW_PRESS:
        light_ambient[index]= (light_ambient[index]+ color_change_rate)%1.0
        
        # w dol kolor
    if key == GLFW_KEY_3 and action == GLFW_PRESS:
        light_ambient[index]=(light_ambient[index]- color_change_rate)%1.0
    if key == GLFW_KEY_4 and action == GLFW_PRESS:
        show_lines = not show_lines
        
def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x, delta_y
    global mouse_x_pos_old, mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos
    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos



def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed, right_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0
    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        right_mouse_button_pressed = 1
    else:
        right_mouse_button_pressed = 0

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
