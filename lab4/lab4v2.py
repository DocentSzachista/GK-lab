
#!/usr/bin/env python3
import sys
import math
from glfw import VERSION_REVISION
from glfw.GLFW import *
import random
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy
from numpy.lib.function_base import angle
RED = random.uniform(0, 255)/255
BLUE = random.uniform(0,255)/255
GREEN = random.uniform(0, 255)/255
viewer = [0.0, 0.0, 10.0]

theta = 0.0
phi = 0.0 
R =1

pix2angle = 1.0

left_mouse_button_pressed = 0
right_mouse_button_pressed = 0

scale = 1.0

mouse_x_pos_old = 0
delta_x = 0

mouse_y_pos_old = 0
delta_y = 0

ZOOMKEY = False
VIEWMODE = True

W,A,S,D = False, False, False,False
 
CAMERA_FRONT = [0.0, 0.0, -1.0]
POSITION = [0, 0, 0]



upVector = [0,1,0]
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
    glColor3f(1.0, 1.0, 1.0)

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


def render(time):
    
    global theta, phi, vector 
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    
    if left_mouse_button_pressed :
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle
        

    # elif left_mouse_button_pressed and not VIEWMODE:
    #     theta += delta_x * pix2radian
    #     phi = delta_y * pix2radian
    
    if  VIEWMODE:
        object_steering(theta, phi)
    else:
        camera_mode(theta, phi)
        #camera_WASD(theta, phi)
        pass 
    object_zooming()




    axes()
    #
    example_object()
    #sierpinski_triangle_3d()
    #sierpinski_triangle_3d(0, 0, 0, 3, 5)
    glFlush()

# 3.0 
def object_steering(theta, phi):

    """
        Obracanko przedmiotu po x i y i przyblizajacy/oddalajacy
    """
   
    glRotatef(theta, 0.0, 1.0, 0.0)
    glRotatef(phi, 1.0, 0.0, 0.0)

 
# 3.5 object zooming

def object_zooming():
    """
        Przyblizanie i oddalanie obiektu w zaleznosci od tego jaki mode wlaczylismy za pomoca klawisza 1
    """
    global scale
    if right_mouse_button_pressed==1 and  ZOOMKEY:
        scale+= 0.1
    elif right_mouse_button_pressed==1 and  not ZOOMKEY:
        scale-= 0.1
    if scale <0.3 :
        scale = 0.3
    elif scale > 2:
        scale = 2
    glScalef(scale, scale, scale)

# 4.0 camera mode

def camera_mode(theta, phi):
    global R,  upVector
    theta %= 360
    phi %=360
    x, y, z = count_points(R, theta* math.pi/180, phi * math.pi/180)

    print(theta, phi)
    if phi >90 and phi <270:
        upVector[1] =-1
    else:
        upVector[1] =1
    #glMultMatrixf(view_matrix)
   # view_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
    gluLookAt(x, y, z, 0, 0, 0,  upVector[0], upVector[1], upVector[2])
    #gluLookAt(x,y,z , 0, 0, 0, upVector[0], upVector[1], upVector[2])
    pass

def camera_WASD(theta, phi):
    global angle_for_WASD, X, Z, Iz, Ix, Y 
    global R, upVector
    theta %= 360
    phi %=360
    x, y, z = count_points(R, theta* math.pi/180, phi * math.pi/180)
    POSITION = [x, y, z]
    if phi >90 and phi <270:
        upVector[1] =-1
    else:
        upVector[1] =1

    gluLookAt(POSITION[0], POSITION[1], POSITION[2],
              POSITION[0]+CAMERA_FRONT[0], POSITION[1]+CAMERA_FRONT[1], POSITION[2]+CAMERA_FRONT[2],
              upVector[0], upVector[1], upVector[2])

def count_points(R ,theta, phi):

    x_eye = R * math.cos(theta) * math.cos(phi) 
    y_eye = R * math.sin(phi)
    z_eye = R * math.sin(theta) * math.cos(phi)
    return x_eye, y_eye, z_eye


def genetarte_piramid(x,y,z,a):
    half = a
    # prostokt
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(RED, GREEN, BLUE)
    glVertex3f(  x - half,   y-half,  z -half)
    glVertex3f(  half+x,    y-half,   z-half)
    glVertex3f(  half+x ,   y-half,   z+half)
    glVertex3f(  x - half,   y-half,   z+half)
    glEnd()
    # sciany 
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(GREEN, RED, BLUE)
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





def update_viewport(window, width, height):
    global pix2angle
    global pix2radian
    pix2angle = 360.0 / width
    pix2radian = 2*math.pi / width
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
    global ZOOMKEY, VIEWMODE, POSITION
    spped = 0.05
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    if key == GLFW_KEY_1 and action == GLFW_PRESS:
        ZOOMKEY = not ZOOMKEY
    if key == GLFW_KEY_2 and action == GLFW_PRESS:
        VIEWMODE = not VIEWMODE
    
    if key == GLFW_KEY_S and action == GLFW_PRESS:
        POSITION[0] -= CAMERA_FRONT[0]*spped
        POSITION[1] -= CAMERA_FRONT[1]*spped
        POSITION[2] -= CAMERA_FRONT[2]*spped 
        
    
    if key == GLFW_KEY_A and action == GLFW_PRESS:
        pass
    

    if key == GLFW_KEY_D and action == GLFW_PRESS:
        D = True

    if key == GLFW_KEY_W and action == GLFW_PRESS:
        POSITION[0] += CAMERA_FRONT[0]*spped
        POSITION[1] += CAMERA_FRONT[1]*spped
        POSITION[2] += CAMERA_FRONT[2]*spped 
        

def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x, delta_y
    global mouse_x_pos_old, mouse_y_pos_old
    #obliczanie pozycji X
    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos
    # obliczanie pozycji y 
    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos

def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed
    global right_mouse_button_pressed
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