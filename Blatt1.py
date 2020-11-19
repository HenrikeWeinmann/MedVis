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
    def __init__(self, Umkreisungskoerper, X, Y , Z, radius, color, speed):

        self.Source = vtk.vtkSphereSource()
        self.Source.Umkreisungskoerper = Umkreisungskoerper
        self.Source.X = X
        self.Source.Y = Y
        self.Source.Z = Z
        self.Source.SetCenter(X, Y, Z)
        self.Source.Position =[X,Y,Z]
        self.Source.SetRadius(radius)
        self.Source.color = color
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
    transformMond.RotateWXYZ(0.1,0,1,0)
    transformMondFilter.Update()
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

Sonne = Himmelskoerper(0, 0, 0, 0, 5, "yellow",1)
Erde = Himmelskoerper(Sonne, Sonne.Source.X +8,Sonne.Source.Y -5, Sonne.Source.Z, 1, "blue",400)
Mond = Himmelskoerper(Erde, Erde.Source.X+2, Erde.Source.Y+1, Erde.Source.Z, 0.5, "red",50)


# get the names of VTK's predefined colors
colors = vtk.vtkNamedColors()

#############################################################

#############################################################
# fill the VTK rendering pipeline with the data of the objects
# source (-> filter) -> mapper -> actor -> renderer -> render window

#Transformer
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

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(Sonne.Source.GetOutputPort())
mapperE = vtk.vtkPolyDataMapper()
mapperE.SetInputConnection(transformErdeFilter.GetOutputPort())
mapperM = vtk.vtkPolyDataMapper()
mapperM.SetInputConnection(transformMondFilter.GetOutputPort())
actor = vtk.vtkActor()
actor2 = vtk.vtkActor()
actor3 = vtk.vtkActor()
actor.SetMapper(mapper)
actor2.SetMapper(mapperE)
actor3.SetMapper(mapperM)
actor.GetProperty().SetColor(colors.GetColor3d(Sonne.Source.color))
actor2.GetProperty().SetColor(colors.GetColor3d(Erde.Source.color))
actor3.GetProperty().SetColor(colors.GetColor3d(Mond.Source.color))

#############################################################
##Render
renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(actor2)
renderer.AddActor(actor3)
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
# In python you can add an observer directly like this.
# In other languages there is a layer of indireciton where
# a vtkCallbackCommand is created, and the function is set
# in the vtkCallbackCommand.
# We set the callback function to be called for each
# activation of the timer.
interactor.AddObserver("TimerEvent", callback_func)
# The default position of the camera
# is a little too close to see the entire
# motion of the arrow. Zoom out a litle.
cam = renderer.GetActiveCamera()
cam.SetPosition(0,0,50)
window.SetSize(500, 500)
window.Render()
interactor.Start()