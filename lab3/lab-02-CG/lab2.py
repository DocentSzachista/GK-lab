#!/usr/bin/env python3

import sys
import math
from glfw import X11_CLASS_NAME
import numpy as np

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *
from numpy.core.fromnumeric import var
import random



RED = random.uniform(0, 255)/255
BLUE = random.uniform(0,255)/255
GREEN = random.uniform(0, 255)/255
MAX_RECUR = 3

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    spin( time *180  / math.pi )
    #axes()
    #generate_egg_with_points()
    #generate_egg_with_lines()
    #generate_egg_with_triangles()
    #generate_egg_with_strip()
    #sierpinski_triangle_3d(0, 0,0, 5, 2)
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

def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)

N = 20

v_array = np.linspace(0, 1, num=N)
u_array = np.linspace(0, 1, num=N)


def count_points_egg():
    tab= np.zeros((N, N, 3))
    for v in range(N):
        for u in range(N):
            x= (-90 * u_array[u]**5 + 225 * u_array[u]**4 - 270 * u_array[u]**3 + 180 * u_array[u]**2 - 45 * u_array[u]) * math.cos( math.pi*v_array[v])
            y= 160 * u_array[u]**4 - 320 * u_array[u]**3 + 160 * u_array[u]**2
            z= (-90 * u_array[u]**5 + 225 * u_array[u]**4 - 270 * u_array[u]**3 + 180 * u_array[u]**2 - 45 * u_array[u]) * math.sin( math.pi*v_array[v])
            tab[u, v,0] = x
            tab[u,v,1] = y
            tab[u,v,2] = z 
    return tab

array_3d_corrected = count_points_egg()

# def count_torus():
#     tab= np.zeros((N, N, 3))
#     for v in range(N):
#         for u in range(N):
#             x = (R +r*math.cos(2*math.pi*v_array[v])*math.cos(2*math.pi*u_array[u]) )
#             y = (R +r*math.cos(2*math.pi*v_array[v])*math.sin(2*math.pi*u_array[u]) )
#             z = r*math.sin(2*math.pi*v_array[v])
#             tab[u,v] = [x,y,z]
#     return tab
# torus_array = count_torus()

# 3.0 
def generate_egg_with_points():
    glBegin(GL_POINTS)
    for i in range(N):
        for j in range(N):
            glColor3f(0, 1.0, 0.0)
            glVertex3fv(array_3d_corrected[i, j])
    glEnd()


# 3.5
def generate_egg_with_lines():
    glBegin(GL_LINES)
    for i in range(N-1):
        for j in range(N-1):
            glColor3f(0, 1.0, 1.0)
            glVertex3fv(array_3d_corrected[i,j])
            glVertex3fv(array_3d_corrected[i+1,j])
            glVertex3fv(array_3d_corrected[i,j+1])
    # for variable in range(0, N**2):
    #     glColor3f(0, 1.0, 0.0)
    #     glVertex3f(array_3d[0][variable], array_3d[1][variable], array_3d[2][variable])
    #     if variable< N**2-1:
    #         glVertex3f(array_3d[0][variable+1], array_3d[1][variable], array_3d[2][variable])
    #         glVertex3f(array_3d[0][variable], array_3d[1][variable+1], array_3d[2][variable])
    glEnd()


# 4.0
def generate_egg_with_triangles():
    
        for i in range(N -1):
            for j in range(N -1) :
            # trojkat 
                # 1 trojkat
                glBegin(GL_TRIANGLES)
                glColor3f(RED, BLUE, GREEN)
                glVertex3fv(array_3d_corrected[i,j])
                glVertex3fv(array_3d_corrected[1+i, j])
                glVertex3fv(array_3d_corrected[i, j+1])
                glEnd()
                # 2 trojkat 
                glBegin(GL_TRIANGLES)
                
                glColor3f(BLUE, GREEN, RED)
                glVertex3fv(array_3d_corrected[i+1,j+1])
                glVertex3fv(array_3d_corrected[i+1,j])
                glVertex3fv(array_3d_corrected[i,j+1])
                glEnd()
# 4.5
def generate_egg_with_strip():
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(N // 2) :
        for j in range(N):
            glColor3f(GREEN, BLUE, RED)
            glVertex3fv(array_3d_corrected[i,j])
            glColor3f(GREEN, RED, RED)
            glVertex3fv(array_3d_corrected[1+i, j])
        for j in range(N):
            glColor3f(GREEN, RED, BLUE)
            glVertex3fv(array_3d_corrected[N-1-i,j])
            glColor3f(GREEN, BLUE, BLUE)
            glVertex3fv(array_3d_corrected[N-1-i-1,j])
    glEnd()
#5.0
def genetarte_piramid(x,y,z,a):
    half = a
    # prostokt
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(RED, 0, BLUE)
    glVertex3f(  x - half,   y-half,  z -half)
    glVertex3f(  half+x,    y-half,   z-half)
    glVertex3f(  half+x ,   y-half,   z+half)
    glVertex3f(  x - half,   y-half,   z+half)
    glEnd()
    # sciany 
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(0, GREEN, BLUE)
    glVertex3f(     x,      half+y,     z)
    glVertex3f(  x - half,   y-half,  z -half)
    glVertex3f(  half+x,    y-half,   z-half)
    glVertex3f(  half+x ,   y-half,   z+half)
    glVertex3f(  x - half,   y-half,   z+half)
    glVertex3f(  x - half,   y-half,  z -half)
    glEnd()
def sierpinski_triangle_3d(x, y, z, iterations, length):
    half = length/2
    if iterations >1 :
        sierpinski_triangle_3d(x-half, y-half, z-half, iterations-1, half)
        sierpinski_triangle_3d(x+half, y-half, z-half, iterations-1, half)
        sierpinski_triangle_3d(x-half, y-half, z+half, iterations-1, half)
        sierpinski_triangle_3d(x+half, y-half, z+half, iterations-1, half)
        sierpinski_triangle_3d(x, y+half, z, iterations-1, half)
    else:
        genetarte_piramid(x, y,z, length)

    pass
# def pyramid():
#     glBegin(GL_TRIANGLES)
    
#     glVertex3f(0.0, 1.0, 0.0)
#     glVertex3f(-1.0, -1.0, 1.0)
#     glVertex3f(1.0, -1.0, 1.0)

#     glVertex3f(0.0, 1.0, 0.0)
#     glVertex3f()

#def generate_sierpinski_3d():




def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
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
    print(len(array_3d_corrected))
    print(array_3d_corrected)
    main()
    array_with_fixed_vertices = np.zeros((5, 3))

    array_with_fixed_vertices[0] = [-1.0, -1.0, 0.0]
    array_with_fixed_vertices[1] = [ 1.0, -1.0, 0.0 ]
    array_with_fixed_vertices[2] = [ 1.0,  1.0, 0.0]
    array_with_fixed_vertices[3] = [-1.0,  1.0, 0.0]
    array_with_fixed_vertices[4] = [0.0, 0.0, 1.0]
    