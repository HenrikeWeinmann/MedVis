# This is a sample Python script using vtk containing a solution of
# an exercise.
# (The original file was downloaded from
# https://lorensen.github.io/VTKExamples/site/Python/GeometricObjects/Sphere/)
#############################################################

#############################################################
# You should always write comments explaining what you had in mind
# when you wrote the code. :-)
# If we do not understand what you wrote, you will get less or even
# no points for your solution. :-(
#############################################################

import vtk
import math

class Himmelskoerper():
    def __init__(self, Umkreisungskoerper, X,Y,Z, radius, texture, speed):

        self.Source = vtk.vtkSphereSource()
        self.Source.Umkreisungskoerper = Umkreisungskoerper
        self.Source.X = X
        self.Source.Y = Y
        self.Source.Z = Z
        self.Source.SetCenter(X, Y, Z)
        self.Source.Position = [X, Y, Z]
        self.Source.SetRadius(radius)
        self.Source.Texture = texture
        self.Source.SetPhiResolution(100)
        self.Source.SetThetaResolution(100)
        self.Source.Speed = speed


refresh_rate = 60 # In Hertz

def callback_func(caller, timer_event):
    # This needs to be called to render the updated actor
    # orientation.
    #transformErde.RotateWXYZ(1, 1, 1, 1)
    transformErde.Translate(translation(Erde,Erde.Source.Speed))
    transformErdeFilter.Update()
    transformMond.Translate(translation(Mond,Erde.Source.Speed))
    #transformMond.RotateWXYZ(0.1,0,1,0)
    transformMondFilter.Update()
    transformMars.Translate(translation(Mars, Mars.Source.Speed))
    transformMarsFilter.Update()
    transformVenus.Translate(translation(Venus, Venus.Source.Speed))
    transformVenusFilter.Update()
    window.Render()


def newPos(oldPos ,axis, deg):
    if axis== "z":
        return [math.cos(deg)*oldPos[0]-math.sin(deg)*oldPos[1],math.sin(deg)*oldPos[0]+math.cos(deg)*oldPos[1],oldPos[2]]
    if axis == "x":
        return [oldPos[0],math.cos(deg)*oldPos[1]-math.sin(deg)*oldPos[2],math.sin(deg)*oldPos[1]+math.cos(deg)*oldPos[2]]

def translation(Himmelskoerper,speed):
    pos = Himmelskoerper.Source.Position
    newpos= newPos(pos,"z",math.pi/speed)

    Himmelskoerper.Source.Position = newpos
    return [newpos[0] - pos[0],newpos[1] - pos[1],newpos[2] - pos[2]]

def updatePos(Himmelskoerper,newpos):
    Himmelskoerper.Source.Position=newpos
#print(newPos([1,0,0],"z",math.pi))

#############################################################
# Create the objects that should be rendered
# Create a sphere using the vtk class.

Sonne = Himmelskoerper(0, 0, 0, 0, 5, "sun.jpg", 0)
Erde = Himmelskoerper(Sonne,Sonne.Source.X +8,Sonne.Source.Y -5, Sonne.Source.Z, 1, "earth.jpg", 300)
Mond = Himmelskoerper(Erde,Erde.Source.X+2, Erde.Source.Y+1, Erde.Source.Z, 0.5, "moon.jpg", 20)
Mars = Himmelskoerper(Sonne, 10, -9.5, 0, 0.75, "mars.jpg", 200)
Venus = Himmelskoerper(Sonne, 6, -4, 0, 1.1, "venus.jpg", 100)


# get the names of VTK's predefined colors
colors = vtk.vtkNamedColors()


#############################################################
#Transformer
#Sonne
transformSonne = vtk.vtkTransform()
transformSonneFilter = vtk.vtkTransformPolyDataFilter()
transformSonneFilter.SetTransform(transformSonne)
transformSonneFilter.SetInputConnection(Sonne.Source.GetOutputPort())
transformSonneFilter.Update()
#Erde
transformErde = vtk.vtkTransform()
transformErdeFilter = vtk.vtkTransformPolyDataFilter()
transformErdeFilter.SetTransform(transformErde)
transformErdeFilter.SetInputConnection(Erde.Source.GetOutputPort())
transformErdeFilter.Update()
#Mond
transformMond = vtk.vtkTransform()
transformMondFilter = vtk.vtkTransformPolyDataFilter()
transformMondFilter.SetTransform(transformMond)
transformMondFilter.SetInputConnection(Mond.Source.GetOutputPort())
transformMondFilter.Update()
#Mars
transformMars = vtk.vtkTransform()
transformMarsFilter = vtk.vtkTransformPolyDataFilter()
transformMarsFilter.SetTransform(transformMars)
transformMarsFilter.SetInputConnection(Mars.Source.GetOutputPort())
transformMarsFilter.Update()
#Venus
transformVenus = vtk.vtkTransform()
transformVenusFilter = vtk.vtkTransformPolyDataFilter()
transformVenusFilter.SetTransform(transformVenus)
transformVenusFilter.SetInputConnection(Venus.Source.GetOutputPort())
transformVenusFilter.Update()

#############################################################
# fill the VTK rendering pipeline with the data of the objects
# source (-> filter) -> mapper -> actor -> renderer -> render window
#reader
readerSonne = vtk.vtkJPEGReader()
readerSonne.SetFileName(Sonne.Source.Texture)
readerErde = vtk.vtkJPEGReader()
readerErde.SetFileName(Erde.Source.Texture)
readerMond = vtk.vtkJPEGReader()
readerMond.SetFileName(Mond.Source.Texture)
readerMars = vtk.vtkJPEGReader()
readerMars.SetFileName(Mars.Source.Texture)
readerVenus = vtk.vtkJPEGReader()
readerVenus.SetFileName(Venus.Source.Texture)

#texture
#Sonne
textureSonne = vtk.vtkTexture()
textureSonne.SetInputConnection(readerSonne.GetOutputPort())

#Erde
textureErde = vtk.vtkTexture()
textureErde.SetInputConnection(readerErde.GetOutputPort())

#Mond
textureMond = vtk.vtkTexture()
textureMond.SetInputConnection(readerMond.GetOutputPort())

#Mars
textureMars = vtk.vtkTexture()
textureMars.SetInputConnection(readerMars.GetOutputPort())

#Venus
textureVenus = vtk.vtkTexture()
textureVenus.SetInputConnection(readerVenus.GetOutputPort())

# Map texture coordinates
#Sonne
map_to_sphere_Sonne = vtk.vtkTextureMapToSphere()
map_to_sphere_Sonne.SetInputConnection(Sonne.Source.GetOutputPort())
map_to_sphere_Sonne.PreventSeamOn()

#Erde
map_to_sphere_Erde = vtk.vtkTextureMapToSphere()
map_to_sphere_Erde.SetInputConnection(transformErdeFilter.GetOutputPort())
map_to_sphere_Erde.PreventSeamOn()

#Mond
map_to_sphere_Mond = vtk.vtkTextureMapToSphere()
map_to_sphere_Mond.SetInputConnection(transformMondFilter.GetOutputPort())
map_to_sphere_Mond.PreventSeamOn()

#Mars
map_to_sphere_Mars = vtk.vtkTextureMapToSphere()
map_to_sphere_Mars.SetInputConnection(transformMarsFilter.GetOutputPort())
map_to_sphere_Mars.PreventSeamOn()

#Venus
map_to_sphere_Venus = vtk.vtkTextureMapToSphere()
map_to_sphere_Venus.SetInputConnection(transformVenusFilter.GetOutputPort())
map_to_sphere_Venus.PreventSeamOn()

#mapper
mapperSonne = vtk.vtkPolyDataMapper()
mapperSonne.SetInputConnection(map_to_sphere_Sonne.GetOutputPort())

mapperErde = vtk.vtkPolyDataMapper()
mapperErde.SetInputConnection(map_to_sphere_Erde.GetOutputPort())

mapperMond = vtk.vtkPolyDataMapper()
mapperMond.SetInputConnection(map_to_sphere_Mond.GetOutputPort())

mapperMars = vtk.vtkPolyDataMapper()
mapperMars.SetInputConnection(map_to_sphere_Mars.GetOutputPort())

mapperVenus = vtk.vtkPolyDataMapper()
mapperVenus.SetInputConnection(map_to_sphere_Venus.GetOutputPort())

#actor
actorSonne = vtk.vtkActor()
actorErde = vtk.vtkActor()
actorMond = vtk.vtkActor()
actorMars = vtk.vtkActor()
actorVenus = vtk.vtkActor()
actorSonne.SetMapper(mapperSonne)
actorSonne.SetTexture(textureSonne)
actorErde.SetMapper(mapperErde)
actorErde.SetTexture(textureErde)
actorMond.SetMapper(mapperMond)
actorMond.SetTexture(textureMond)
actorMars.SetMapper(mapperMars)
actorMars.SetTexture(textureMars)
actorVenus.SetMapper(mapperVenus)
actorVenus.SetTexture(textureVenus)

#############################################################
##Render
renderer = vtk.vtkRenderer()
renderer.AddActor(actorSonne)
renderer.AddActor(actorErde)
renderer.AddActor(actorMond)
renderer.AddActor(actorMars)
renderer.AddActor(actorVenus)
renderer.SetBackground(colors.GetColor3d("Black"))
##window
window = vtk.vtkRenderWindow()
window.SetWindowName("Universe")
window.AddRenderer(renderer)
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(window)
# The interactor needs to be initialised before we
# can create a timer or add observers.
interactor.Initialize()
# The repeating timer takes the interval in 1/1000th
# of a second. Each time it fires off a TimerEvent.
interactor.CreateRepeatingTimer(int(1/refresh_rate))

interactor.AddObserver("TimerEvent", callback_func)
# set camera position
cam = renderer.GetActiveCamera()
cam.SetPosition(0,0,50)

window.Render()
interactor.Start()
