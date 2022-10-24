from pygame.mouse import set_pos, set_visible
from pygame.display import set_mode, flip, set_caption
from pygame.event import get
from pygame import init, QUIT, KEYDOWN, K_ESCAPE, K_RETURN, K_PAUSE,\
                   K_p, MOUSEMOTION, K_w, K_s, K_d, K_a, quit
from pygame.key import get_pressed
from pygame.time import wait

from OpenGL.GL import GL_DEPTH_TEST, GL_LIGHTING,\
     GL_COLOR_MATERIAL, GL_LIGHT0, glShadeModel, GL_SMOOTH,\
     glColorMaterial, GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,\
     GL_AMBIENT, GL_DIFFUSE, glLightfv, glMatrixMode,\
     GL_PROJECTION, GL_MODELVIEW, glGetFloatv,\
     GL_MODELVIEW_MATRIX, glLoadIdentity, glRotatef, glPushMatrix,\
     glTranslatef, glMultMatrixf, glPopMatrix, GL_POSITION,\
     glClear, glColor4f, glBegin, GL_QUADS, glVertex3f, glEnd
from OpenGL.GL import glEnable
from OpenGL.GLU import gluNewQuadric, gluPerspective, gluLookAt,\
     gluSphere

from numpy import array

from time import time

display = (1280, 720)
displayCenter = array(set_mode(display, 1073741826).get_size())\
                // 2

set_pos(displayCenter)
set_visible(False)
init()
tuple(map(glEnable, (GL_DEPTH_TEST, GL_LIGHTING,\
                     GL_COLOR_MATERIAL, GL_LIGHT0))) #opc
glShadeModel(GL_SMOOTH)
glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
tuple(glLightfv(*a) for a in ((GL_LIGHT0, GL_AMBIENT,\
                               array(((1,) * 3 + (2,))) / 2),\
       (GL_LIGHT0, GL_DIFFUSE, (1,) * 4))) #opc

sphere = gluNewQuadric()
w, h = display

glMatrixMode(GL_PROJECTION)
gluPerspective(*(array((450, 10 / h * w, 1, 500)) / 10))
glMatrixMode(GL_MODELVIEW)
gluLookAt(*((0, -8,) + (0,) * 6 + (1,)))

viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

glLoadIdentity()

# init mouse movement and center mouse on screen
mouseMove, up_down_angle, paused, run, t = [0, 0], 0, False,\
                                           True, time()

while run:    
    for event in get(): #dicc
        if event.type == QUIT or\
           (event.type == KEYDOWN and\
            (event.key == K_ESCAPE or event.key == K_RETURN)):
            run = False

        if event.type == KEYDOWN and\
           (event.key == K_PAUSE or event.key == K_p):
            paused = not paused

        if event.type == KEYDOWN and\
           (event.key == K_PAUSE or event.key == K_p) or not paused:
            set_pos(displayCenter)

        if not paused: 
            if event.type == MOUSEMOTION:
                mouseMove = event.pos - displayCenter
                
    if not paused:
        # get keys
        keypress = get_pressed()
        #mouseMove = pygame.mouse.get_rel()
    
        # init model view matrix
        glLoadIdentity()
        glRotatef(up_down_angle, 1, 0, 0) #inmovil

        # init the view matrix
        glPushMatrix()
        glLoadIdentity()

        x, y, z = 0, 0, 0

        # apply the movment
        d = {'X' : {keypress[K_d] : -1, keypress[K_a] : 1},\
             'Z' : {keypress[K_w] : 1, keypress[K_s] : -1}}

        for c in d:
            d_C = d[c]
            
            for e in d_C:                
                if e:
                    k_E = d_C[e]
                    
                    if c == 'X':
                        x = k_E

                    if c == 'Z':
                        z = k_E

        glTranslatef(*array((x, y, z)) / 20) #v_D

        # apply the look up and down
        x, y = mouseMove
        up_down_angle += y / 10 #v_Y

        # apply the left and right rotation
        glRotatef(x / 10, 0, 1, 0) #v_X #se repite

        # multiply the current matrix by the get the new view matrix and store the final vie matrix 
        glMultMatrixf(viewMatrix)

        viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

        # apply view matrix
        glPopMatrix()
        glMultMatrixf(viewMatrix)
        glLightfv(GL_LIGHT0, GL_POSITION, (1, -1, 1, 0))
        glClear(16640)
        glPushMatrix()
        glColor4f(*(array(((1,) * 3 + (2,))) / 2))
        glBegin(GL_QUADS) 
        tuple(glVertex3f(*a) for a in ((-2 * array((5, 5, 1))),\
            (-2 * array((-5, 5, 1))), (2 * array((5, 5, -1))),\
                                       (-2 * array((5, -5, 1)))))
        glEnd()
        glTranslatef(-1.5, 0, 0)
        glColor4f(*(array((5, 2, 2, 10)) / 10))
        gluSphere(sphere, 1, 32, 16) 
        glTranslatef(*(array((1, 0, 0)) * 3))
        glColor4f(*(array((2, 2, 5, 10)) / 10))
        gluSphere(sphere, 1, 32, 16) 
        glPopMatrix()
        flip()
        wait(5) #cap 144 fps

        if not time() == t:
            set_caption(str(round(1 / (time() - t))))
        
        t = time()

quit()
