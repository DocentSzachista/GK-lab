#!/usr/bin/env python3
import sys
import time as t
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

import random

RED = random.uniform(0, 255)/255
BLUE = random.uniform(0,255)/255
GREEN = random.uniform(0, 255)/255
MAX_REC = 5


def startup():
    glClearColor(0.5, 0.5, 0.5, 1.0)
    update_viewport(None, 400, 400)


def shutdown():
    pass

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    glFlush()

def update_viewport(window, width, height):
 if height == 0:
    height = 1
 if width == 0:
    width = 1
 aspectRatio = width / height
 glMatrixMode(GL_PROJECTION)
 glViewport(0, 0, width, height)
 glLoadIdentity()
 
 if width <= height:
    glOrtho(-100.0, 100.0, -100.0 / aspectRatio, 100.0 / aspectRatio, 1.0, -1.0)
 else:
    glOrtho(-100.0 * aspectRatio, 100.0 * aspectRatio, -100.0, 100.0, 1.0, -1.0)
 
 glMatrixMode(GL_MODELVIEW)
 glLoadIdentity()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT) 
    
    #render_triangle(0,100,100) #Working
    #render_rectangle(15,35,20,30) #Working
    #render_rectangle_deformation(15,35,20,30,0.75) #Working
    #render_rectangle_middle(4,3 ,30, 15) #alternatywa
    #sierpinski_model(0,0,1,200,200) #working 
    iterated_system(0, 0) # works 
    glFlush()




# my implementation for 3.0 :) 

def render_triangle(a,b,c):
    glColor3f(1, 0.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(-a, 0.0)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(0.0, b)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(c, 0.0)
    glEnd()


# 3.5 
def render_rectangle(x, y, a,b):
    # jako wierzcholek
    """
        Generates a rectangle with randomly generated colour

        Parameters
        ----------
        x: float
            value that corresponds to x-axis
        y: float
            value that corresponds to y-axis
        a: float
            length of rectangle side
        b: float
            length of second rectangle side


    """
    glColor3f(32.0, 10.0, 0.0)
    
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x+a, y)
    glVertex2f(x, b+y)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2f(x+a, y+b)
    glVertex2f(x+a, y)
    glVertex2f(x, b+y)
    glEnd()


    
#4.0
def render_rectangle_deformation(x, y, a, b, d=0):
    """
        Draw a rectangle with possibility to deform its sides

        Parameters
        ----------
        x: float
            value that corresponds to x-axis
        y: float
            value that corresponds to y-axis
        a: float
            length of rectangle side
        b: float
            length of second rectangle side
        d: float must be in range (0, 1)
            degree of rectangle deformation, 
    """
    if d > 1 or d < 0:
        print("Wrong deformation value. program will close")
        sys.exit(-1)
    
    
    deform = d*100
    glColor3f(RED, BLUE, GREEN)
    
    glBegin(GL_TRIANGLES)
    glVertex2f(x-deform, y)
    glVertex2f(x+a, y)
    glVertex2f(x, b+y)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2f(x+a+deform, y+b)
    glVertex2f(x+a, y)
    glVertex2f(x, b+y)
    glEnd()

#wersja prostokata z podanym punktem posrodku 
def render_rectangle_middle(x,y,a,b):
    """
        Wersja w ktorej podany punkt traktujemy jako srodek prostokata
        
        Parameters
        ----------
        x: float
            value that corresponds to x-axis
        y: float
            value that corresponds to y-axis
        a: float
            length of rectangle side
        b: float
            length of second rectangle side
    """
    glColor3f(RED, BLUE, GREEN)
    glBegin(GL_TRIANGLES)
    glVertex2f(x - a/2, y - b/2)
    glVertex2f(x + a/2, y - b/2)
    glVertex2f(x - a/2, y + b/2)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2f(x + a/2, y + b/2)
    glVertex2f(x + a/2, y - b/2)
    glVertex2f(x - a/2, y + b/2)
    glEnd()



#4.5
def sierpinski_model(x, y, iterations, a, b): 
    
    a /=3.0 
    b /=3.0
    render_rectangle_middle(x,y,a,b)

    if iterations < MAX_REC :
        
        sierpinski_model(x-a, y, iterations+1,a,b)
        sierpinski_model(x, y-b, iterations+1,a,b)
        sierpinski_model(x+a, y, iterations+1,a,b)
        sierpinski_model(x, y+b, iterations+1,a,b)
        
        sierpinski_model(x-a, y-b, iterations+1,a, b)
        sierpinski_model(x-a, y+b, iterations+1,a, b)
        sierpinski_model(x+a, y+b, iterations+1,a, b)
        sierpinski_model(x+a, y-b, iterations+1,a, b)

array_2d = [
    [-0.67, -0.02, 0.00, -0.18, 0.81, 10.00],
    [ 0.40,  0.40, 0.00, -0.10, 0.40,  0.00],
    [-0.40, -0.40, 0.00, -0.10, 0.40,  0.00],
    [-0.10,  0.00, 0.00,  0.44, 0.44, -2.00]
    ]
#5.0
def iterated_system(start_x, start_y, number_of_iterations= 10000000, seed = 4):
    glBegin(GL_POINTS)
    for iterator in range(0, number_of_iterations):
        glVertex2f(start_x, start_y)
        rand = int(random.uniform(0, seed))
        x = array_2d[rand][0]*start_x + array_2d[rand][1]*start_y+array_2d[rand][2]
        y = array_2d[rand][3]*start_x + array_2d[rand][4]*start_y+array_2d[rand][5]          
        start_x = x
        start_y = y
    glEnd()


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
 main()