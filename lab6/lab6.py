#!/usr/bin/env python3
import sys
import math
import numpy as np
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

from PIL import Image


viewer = [0.0, 0.0, 10.0]
phi = 0.0 
theta = 0.0
pix2angle = 1.0

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
light_position = [0.0, 0.0, 10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

# variables added by student 
image = [Image.open("tekstura.tga"), Image.open("bienat.TGA") ]
index =0
# egg vars
N = 20
v_array = np.linspace(0, 1, num=N)
u_array = np.linspace(0, 1, num=N)





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

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    # umozliwienie texturowania 
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_CULL_FACE)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    # Koniec definicji opcji 
    
    switch_picture()
    # glTexImage2D(
    #     GL_TEXTURE_2D, 0, 3, image[0].size[0], image[0].size[1], 0,
    #     GL_RGB, GL_UNSIGNED_BYTE, image[0].tobytes("raw", "RGB", 0, -1)
    # )
def switch_picture():
        global index
        
        glTexImage2D(
        GL_TEXTURE_2D, 0, 3, image[index].size[index], image[index].size[1], 0,
        GL_RGB, GL_UNSIGNED_BYTE, image[index].tobytes("raw", "RGB", 0, -1)
    )
        index = (index +1) %2

def shutdown():
    pass


def render(time):
    global theta, phi

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle
    glRotatef(theta, 0.0, 1.0, 0.0)
    glRotatef(phi, 0.0, 0.0, 1.0)
    #draw_triangle_example()
    #3.0
    #draw_rectangle(0, 0, 10)
    #3.5
    genetarte_piramid(0, 0, 0, 2)
    #generate_egg_with_strip(theta)
    glFlush()
def draw_triangle_example():
    glBegin(GL_TRIANGLES)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-5.0, -5.0, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(5.0, -5.0, 0.0)
    glTexCoord2f(0.5, 1.0)
    glVertex3f(0.0, 5.0, 0.0)
    glEnd()



#3.0
def draw_rectangle(x, y, a):
    
    glBegin(GL_QUADS)

    glTexCoord2f(0.0, 0.0)
    glVertex3f(x - a/2, y - a/2, 0)

    glTexCoord2f(0.0, 1.0)
    glVertex3f(x - a/2, y + a/2, 0)

    glTexCoord2f(1.0, 1.0)
    glVertex3f( x + a/2, y + a/2, 0)

    glTexCoord2f(1.0, 0.0)
    glVertex3f( x + a/2, y - a/2, 0)

    glEnd()



def genetarte_piramid(x,y,z,a):
    half = a
    # prostokt
    glBegin(GL_TRIANGLE_STRIP)
   
    glTexCoord2f(0.0, 0.0)
    glVertex3f(  x - half,   y-half,  z -half)

    glTexCoord2f(1.0, 0.0)
    glVertex3f(  half+x,    y-half,   z-half)

    glTexCoord2f(0.0, 1.0)
    glVertex3f(  x - half,   y-half,   z+half)

    glTexCoord2f(1.0, 1.0)
    glVertex3f(  half+x ,   y-half,   z+half)
    
    glEnd()
    # sciany 


    glBegin(GL_TRIANGLE_FAN)

    glTexCoord2f(0.5, 0.5)    
    glVertex3f(     x,      half+y,     z)

    glTexCoord2f(0.0, 0.0)
    glVertex3f(  x - half,   y-half,   z+half)

    glTexCoord2f(1.0, 0.0)
    glVertex3f(  half+x ,   y-half,   z+half)

    glTexCoord2f(1.0, 1.0)
    glVertex3f(  half+x,    y-half,   z-half)

    glTexCoord2f(0.0, 1.0)
    glVertex3f(  x - half,   y-half,  z -half)

    glTexCoord2f(0.0, 0.0)
    glVertex3f(  x - half,   y-half,   z+half)
    glEnd()

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
def count_texture_egg():
    tab = np.zeros((N, N, 2))
    for u in range(N):
        for v in range(N):
            tab[u, v] = [u/(N-1), v/(N-1)]
    return tab
# points for egg 
array_3d_corrected = count_points_egg()
texture_array = count_texture_egg()
def generate_egg_with_strip(theta):

    glRotatef(theta, 0.0, 1.0, 0.0)
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(N // 2) :
        for j in range(N):
            glTexCoord2fv(texture_array[i, j])
            glVertex3fv(array_3d_corrected[i,j])
            glTexCoord2fv(texture_array[i+1, j])
            glVertex3fv(array_3d_corrected[1+i, j])
        for j in range(N):
            glTexCoord2fv(texture_array[N-1-i, j])
            glVertex3fv(array_3d_corrected[N-1-i,j])
            glTexCoord2fv(texture_array[N-1-i-1, j])
            glVertex3fv(array_3d_corrected[N-1-i-1,j])
    glEnd()



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
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    if key == GLFW_KEY_1 and action == GLFW_PRESS:
        switch_picture()

def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x, delta_y
    global mouse_x_pos_old , mouse_y_pos_old

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
