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

class Himmelskoerper():
    def __init__(self, Umkreisungskoerper, position, radius, color):

        self.Source = vtk.vtkSphereSource()
        self.Source.Umkreisungskoerper = Umkreisungskoerper
        self.Source.Position = self.Source.SetCenter(position)
        self.Source.SetRadius(radius)
        self.Source.color = color
        self.Source.SetPhiResolution(100)
        self.Source.SetThetaResolution(100)
        self.Source.mapper = vtk.vtkPolyDataMapper()
        self.Source.mapper.SetInputConnection(self.Source.GetOutputPort())


refresh_rate = 60 # In Hertz
def callback_func(caller, timer_event):
    actor.RotateZ(1)
    # This needs to be called to render the updated actor
    # orientation.
    window.Render()

#############################################################
# Create the objects that should be rendered
# Create a sphere using the vtk class.

Sonne = Himmelskoerper(0, (0, 0, 0), 5, "yellow")
Erde = Himmelskoerper(Sonne, (8, -5, 0), 1, "blue")
Mond = Himmelskoerper(Erde, (6, -7, 0), 0.5, "red")


# get the names of VTK's predefined colors
colors = vtk.vtkNamedColors()


#############################################################

#############################################################
# fill the VTK rendering pipeline with the data of the objects
# source (-> filter) -> mapper -> actor -> renderer -> render window

actor = vtk.vtkActor()
actor2 = vtk.vtkActor()
actor3 = vtk.vtkActor()
actor.SetMapper(Sonne.Source.mapper)
actor2.SetMapper(Erde.Source.mapper)
actor3.SetMapper(Mond.Source.mapper)
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

window.Render()
interactor.Start()