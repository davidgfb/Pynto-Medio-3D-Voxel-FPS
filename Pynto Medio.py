from pygame import init, QUIT, KEYDOWN, K_ESCAPE, K_RETURN, K_PAUSE,\
                   K_p, MOUSEMOTION, K_w, K_s, K_d, K_a, quit
from pygame.mouse import set_pos, set_visible
from pygame.display import set_mode, flip, set_caption
from pygame.event import get
from pygame.key import get_pressed
from pygame.time import wait

from OpenGL.GL import GL_DEPTH_TEST, GL_LIGHTING,\
     GL_COLOR_MATERIAL, GL_LIGHT0, glShadeModel, GL_SMOOTH,\
     glColorMaterial, GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,\
     GL_AMBIENT, GL_DIFFUSE, glLightfv, glMatrixMode,\
     GL_PROJECTION, GL_MODELVIEW, glGetFloatv,\
     GL_MODELVIEW_MATRIX, glLoadIdentity, glRotatef, glPushMatrix,\
     glTranslatef, glMultMatrixf, glPopMatrix, GL_POSITION,\
     glClear, glColor4f, glBegin, GL_QUADS, glVertex3f, glEnd,\
     glMaterialfv, GL_FRONT, GL_SPECULAR, glMateriali,\
     GL_SHININESS, glEnable, glScalef
from OpenGL.GLU import gluNewQuadric, gluPerspective, gluLookAt,\
     gluSphere
from OpenGL.GLUT import glutInit, glutSolidCube

from numpy import array

from time import time

ptos_Linea, pos_Elem = [(1,) * 3, (4,) * 3], 0

def pp(met):
    glPushMatrix()
    met()
    glPopMatrix()

def draw_gun():
    # Setting up materials, ambient, diffuse, specular and shininess properties are all
    # different properties of how a material will react in low/high/direct light for
    # example.
    ambient_coeffsGray, diffuse_coeffsGray, specular_coeffsGray =\
                        (*(0.3,) * 3, 1), (*(0.5,) * 3, 1),\
                        (*(0,) * 3, 1)

    tuple(glMaterialfv(*a) for a in\
          ((GL_FRONT, GL_AMBIENT, ambient_coeffsGray),\
           (GL_FRONT, GL_DIFFUSE, diffuse_coeffsGray),\
           (GL_FRONT, GL_SPECULAR, specular_coeffsGray))) #opc
    glMateriali(GL_FRONT, GL_SHININESS, 1)

    # OpenGL is very finicky when it comes to transformations, for all of them are global,
    # so it's good to seperate the transformations which are used to generate the object
    # from the actual global transformations like animation, movement and such.
    # The glPushMatrix() ----code----- glPopMatrix() just means that the code in between
    # these two functions calls is isolated from the rest of your project.
    # Even inside this push-pop (pp for short) block, we can use nested pp blocks,
    # which are used to further isolate code in it's entirety.
    for pto_Linea in ptos_Linea:
        x, y, z = pto_Linea

        pp(lambda : (glTranslatef(x, y, z), glutSolidCube(1)))

    tuple(pp(a) for a in\
            (lambda : (glTranslatef(*(0, 0, 1)),\
                       glScalef(*(7, 1, 1)), glutSolidCube(1)),\
             lambda : (glTranslatef(*(-2, 0, -1)),\
                       glScalef(*(3, 1, 3)), glutSolidCube(1)),\
             lambda : (glTranslatef(*(2, 0, -1)),\
                       glScalef(*(3, 1, 3)), glutSolidCube(1))))
    
while pos_Elem + 1 < len(ptos_Linea):
    p_0, p_F = ptos_Linea[pos_Elem : pos_Elem + 2]
    ptoMedio = tuple((array(p_0) + array(p_F)) // 2)
 
    if ptoMedio in ptos_Linea:
        pos_Elem += 1
            
    else:
        ptos_Linea.insert(pos_Elem + 1, ptoMedio) #list.insert()

display = (1280, 720)
displayCenter = array(set_mode(display, 1073741826).get_size())\
                // 2

set_pos(displayCenter)
set_visible(False)
init()
glutInit()
tuple(map(glEnable, (GL_DEPTH_TEST, GL_LIGHTING,\
                     GL_COLOR_MATERIAL, GL_LIGHT0))) #opc
glShadeModel(GL_SMOOTH)
glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
tuple(glLightfv(*a) for a in ((GL_LIGHT0, GL_AMBIENT,\
                        array((1,) * 3 + (2,)) / 2),\
                        (GL_LIGHT0, GL_DIFFUSE, (1,) * 4))) #opc

sphere = gluNewQuadric()
w, h = display

glMatrixMode(GL_PROJECTION)
gluPerspective(*array((450, 10 / h * w, 1, 500)) / 10)
glMatrixMode(GL_MODELVIEW)
gluLookAt(*(0, -8,) + (0,) * 6 + (1,))

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
        glPopMatrix()
        draw_gun()
        flip()
        wait(5) #cap 144 fps

        if not time() == t:
            set_caption(str(round(1 / (time() - t))))
        
        t = time()

quit()
