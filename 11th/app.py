import pygame as pg
import os, copy, easygui
from math import sin, cos
from src.colours import *
from src.objects import *
from src.classes import *
from operator import itemgetter


########################
##    INITIALIZATION  ##
########################
prevMousePos = (0, 0)
RMB = False
LMB = False

winWidth = 1600
winHeight = 900

pg.init()
pg.display.set_caption("Blender? more like Blunder :D")
display = pg.display.set_mode((winWidth, winHeight))
clock = pg.time.Clock()
os.system("cls")

shapes = Shapes()
functions = Functions()

# check for fonts before starting please
font = pg.font.Font(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "fonts", "Poppins.ttf")), 20)
fontSmall = pg.font.Font(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "fonts", "Poppins.ttf")), 15)



########################
##       BUTTONS      ##
########################
# rect
cubeButtRect = pg.Rect((1500, 110), (60, 20))
sphereButtRect = pg.Rect((1500, 180), (60, 20))
customShapeButtRect = pg.Rect((1500, 250), (60, 20))

vertButtRect = pg.Rect((1500, 640), (60, 20))
edgeButtRect = pg.Rect((1500, 570), (60, 20))
faceButtRect = pg.Rect((1500, 500), (60, 20))

# txt
shapes_text = font.render('Shapes', True, WHITE)

cubeButtTxt = fontSmall.render('Cube', True, WHITE)
sphereButtTxt = fontSmall.render('Sphere', True, WHITE)
customShapeButtTxt = fontSmall.render('.obj file', True, WHITE)

settings_text = font.render('Settings', True, WHITE)

vertButtTxt = fontSmall.render('View verts', True, WHITE)
edgeButtTxt = fontSmall.render('View edges', True, WHITE)
faceButtTxt = fontSmall.render('View faces', True, WHITE)

# actual buttons
cubeButt = ToggleButt(cubeButtRect, display, 1, False)
sphereButt = ToggleButt(sphereButtRect, display, 0, False)
customShapeButt = ToggleButt(customShapeButtRect, display, 0, False)

toggleVertsButt = ToggleButt(vertButtRect, display, 1, False)
toggleEdgesButt = ToggleButt(edgeButtRect, display, 1, False)
toggleFacesButt = ToggleButt(faceButtRect, display, 1, False)

def renderButtonTxt():
    display.blit(shapes_text, (1500, 50))
    display.blit(cubeButtTxt, (1500, 90))
    display.blit(sphereButtTxt, (1500, 160))
    display.blit(customShapeButtTxt, (1500, 230))
    
    display.blit(settings_text, (1500, 390))
    display.blit(vertButtTxt, (1500, 620))
    display.blit(edgeButtTxt, (1500, 550))
    display.blit(faceButtTxt, (1500, 480))

rotX = 0
rotY = 0
rotZ = 0

objPos = [winWidth//2, winHeight//2]
fov = 500 # what the fuck man, im going to kill myself this shit is so not cool i hate pygame you stupid non cartesian fuck i will find you and i will kill
# you, remember this mf i will end you, this is not a threat this is a fucking promise. NIGHTMARE NIGHTMARE NIGHTMARE NIGHTMARE
distFromObj = 10

pts = 'asdf'
edges = 'asdf'
ogFaces = 'asdf'
currShape = 'asdf'
currObjFile = 'asdf'

def changeShape(shape, file=None, resetCam=True):
    global pts
    global edges
    global ogFaces

    global currShape
    global currObjFile

    global distFromObj
    global rotX
    global rotY
    global rotZ

    if shape == 0:
        pts, edges, ogFaces = shapes.cube()
        currShape = 0
    elif shape == 1:
        pts, edges, ogFaces = shapes.pyramid()
        currShape = 1
    elif shape == 2:
        pts, edges, ogFaces = shapes.sphere()
        currShape = 2
    elif shape == 3:
        pts, ogFaces = Importer.loadObj(file)
        edges = []
        currShape = 3
        currObjFile = file

    for face in ogFaces:
        exists = False
        for item in face:
            if type(item) is tuple: exists = True
        if exists == False: face.append(functions.randColour())

    autoZoomList = []
    for point in pts:
        for item in point:
            autoZoomList.append(item[0])

    if resetCam == True:
        distFromObj = max(autoZoomList) + 2 * 3
        rotX = 0
        rotY = 0
        rotZ = 0

changeShape(0)

doRenderFaces = True
doRenderEdges = True
doRenderVerts = True

sens = 0.01
scrollSens = 1
maxDist = 250
minDist = 2


########################
##      MAIN LOOP     ##
########################
run = True
while run:
    clock.tick(144)
    fps = clock.get_fps()

    display.fill(BG)

    mouseButts = pg.mouse.get_pressed()
    if mouseButts[2]:
        LMB = True 
    else:
        LMB = False

    if mouseButts[0]:
        RMB = True 
    else:
        RMB = False


    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        if event.type == pg.MOUSEMOTION:
            pos = event.pos
            moveAmt = (prevMousePos[0] - pos[0], prevMousePos[1] - pos[1])
            if RMB:
                rotX += moveAmt[1] * sens
                rotY += moveAmt[0] * sens
            prevMousePos = pos

        if event.type == pg.MOUSEBUTTONDOWN:
            mousePOS = pg.mouse.get_pos()

            if event.button == 4:
                if distFromObj >= minDist:
                    distFromObj -= scrollSens
            if event.button == 5:
                if distFromObj <= maxDist:
                    distFromObj += scrollSens

            if event.button == 1:
                if vertButtRect.collidepoint(mousePOS[0], mousePOS[1]):
                    if toggleVertsButt.disabled == False:
                        if toggleVertsButt.clicked():
                            doRenderVerts = True
                        else:
                            doRenderVerts = False
                
                if edgeButtRect.collidepoint(mousePOS[0], mousePOS[1]):
                    if toggleEdgesButt.disabled == False:
                        if toggleEdgesButt.clicked():
                            doRenderEdges = True
                        else:
                            doRenderEdges = False

                if faceButtRect.collidepoint(mousePOS[0], mousePOS[1]):
                    if toggleFacesButt.disabled == False:
                        if toggleFacesButt.clicked():
                            doRenderFaces = True
                        else:
                            doRenderFaces = False
                
                if cubeButtRect.collidepoint(mousePOS[0], mousePOS[1]):
                    if cubeButt.disabled == False:
                        if cubeButt.toggle == 0:
                            cubeButt.clicked()
                            changeShape(0)
                            sphereButt.toggle = 0
                            customShapeButt.toggle = 0

                if sphereButtRect.collidepoint(mousePOS[0], mousePOS[1]):
                    if sphereButt.disabled == False:
                        if sphereButt.toggle == 0:
                            sphereButt.clicked()
                            changeShape(2)
                            cubeButt.toggle = 0
                            customShapeButt.toggle = 0

                if customShapeButtRect.collidepoint(mousePOS[0], mousePOS[1]):
                    if customShapeButt.disabled == False:
                        if customShapeButt.toggle == 0:
                            file = easygui.fileopenbox(default = './meshes/*.obj')
                            changeShape(0)
                            customShapeButt.clicked()
                            changeShape(3, file)
                            cubeButt.toggle = 0
                            sphereButt.toggle = 0

    faces = copy.deepcopy(ogFaces)

    # -- VERTEX MATHS --
    projectedPts = [p for p in range(len(pts))]

    rotXMatrix = [[1, 0, 0], [0, cos(rotX), -sin(rotX)], [0, sin(rotX), cos(rotX)]]
    rotYMatrix = [[cos(rotY), 0, -sin(rotY)], [0, 1, 0], [sin(rotY), 0, cos(rotY)]]
    rotZMatrix = [[cos(rotZ), -sin(rotZ), 0], [sin(rotZ), cos(rotZ), 0], [0, 0, 1]]

    pointsZ = []
    for i, v in enumerate(pts):
        rotated = functions.matrixMult(rotXMatrix, v)
        rotated = functions.matrixMult(rotYMatrix, rotated)
        rotated = functions.matrixMult(rotZMatrix, rotated)

        if distFromObj != 0:
            z = 1/(distFromObj - rotated[2][0])
        else:
            z = 0
        projection = [[z, 0, 0], [0, z, 0]]

        projected = functions.matrixMult(projection, rotated)

        x = projected[0][0] * fov + objPos[0]
        y = projected[1][0] * fov + objPos[1]

        projectedPts[i] = [x, y]

        pointsZ.append(z)

    # -- SPRITE MATHS --
    rotated = functions.matrixMult(rotYMatrix, rotated)
    rotated = functions.matrixMult(rotZMatrix, rotated)

    if distFromObj != 0:
        z = 1/(distFromObj - rotated[2][0])
    else:
        z = 0
    projection = [[z, 0, 0], [0, z, 0]]
    projected = functions.matrixMult(projection, rotated)


    for face in faces:
        faceZ = []
        for value in face:
            if isinstance(value, int) == True:
                faceZ.append(pointsZ[value])
        face.append(faceZ)
        if len(face) == 6:
            face.append(sum([face[5][0], face[5][1], face[5][2], face[5][3]]) / 4)
        elif len(face) == 5:
            face.append("asdf")
            face.append(sum([face[4][0], face[4][1], face[4][2]]) / 3)
    faces.sort(key=itemgetter(6))
    for i, face in enumerate(faces):
        if "asdf" in face:
            face.remove("asdf")


    def renderFaces():
        for i, v in enumerate(faces):
            a = (projectedPts[v[0]][0], projectedPts[v[0]][1])
            b = (projectedPts[v[1]][0], projectedPts[v[1]][1])
            c = (projectedPts[v[2]][0], projectedPts[v[2]][1])
            if len(v) == 7:
                d = (projectedPts[v[3]][0], projectedPts[v[3]][1])
                e = v[4]
                pg.draw.polygon(display, e, (a, b, c, d))
            else:
                e = v[3]
                pg.draw.polygon(display, e, (a, b, c))

    def renderEdges():
        for edge in edges:
            a = (projectedPts[edge[0]][0], projectedPts[edge[0]][1])
            b = (projectedPts[edge[1]][0], projectedPts[edge[1]][1])

            pg.draw.line(display, Functions.hexToRgb("#29C0CB"), a, b, 2)

    def renderVerts():
        for pt in projectedPts: pg.draw.circle(display, Functions.hexToRgb("#F8C205"), (int(pt[0]), int(pt[1])), 4)

    if doRenderFaces == True: renderFaces()
    if doRenderEdges == True: renderEdges()
    if doRenderVerts == True: renderVerts()

    if edges == []:
        toggleEdgesButt.disabled = True
    else:
        toggleEdgesButt.disabled = False

    toggleVertsButt.draw()
    toggleEdgesButt.draw()
    toggleFacesButt.draw()
    
    cubeButt.draw()
    sphereButt.draw()
    customShapeButt.draw()

    fps_text = font.render(f'FPS: {round(fps, 2)}', True, WHITE)
    hint_text = fontSmall.render('use lmb to rotate view', True, WHITE)

    display.blit(fps_text, (0, 0))
    display.blit(hint_text, (725, 0))

    renderButtonTxt()

    pg.display.update()


########################
##      POST LOOP     ##
########################
pg.quit()
