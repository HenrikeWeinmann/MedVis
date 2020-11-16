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

        self.Port = vtk.vtkSphereSource()
        self.Port.Umkreisungskoerper = Umkreisungskoerper
        self.Port.SetCenter(position)
        self.Port.SetRadius(radius)
        self.Port.color = color
        self.Port.SetPhiResolution(100)
        self.Port.SetThetaResolution(100)




Sonne = Himmelskoerper(0, (0, 0, 0), 5, "yellow")
Erde = Himmelskoerper(Sonne, (8, -5, 0), 1, "blue")
Mond = Himmelskoerper(Erde, (6, -7, 0), 0.5, "red")


# get the names of VTK's predefined colors
colors = vtk.vtkNamedColors()


#############################################################

#############################################################
# fill the VTK rendering pipeline with the data of the objects
# source (-> filter) -> mapper -> actor -> renderer -> render window
mapper = vtk.vtkPolyDataMapper()
mapper2 = vtk.vtkPolyDataMapper()
mapper3 = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(Sonne.Port.GetOutputPort())
mapper2.SetInputConnection(Erde.Port.GetOutputPort())
mapper3.SetInputConnection(Mond.Port.GetOutputPort())

actor = vtk.vtkActor()
actor2 = vtk.vtkActor()
actor3 = vtk.vtkActor()
actor.SetMapper(mapper)
actor2.SetMapper(mapper2)
actor3.SetMapper(mapper3)
actor.GetProperty().SetColor(colors.GetColor3d("Yellow"))
actor2.GetProperty().SetColor(colors.GetColor3d("Blue"))
actor3.GetProperty().SetColor(colors.GetColor3d("Red"))

renderer = vtk.vtkRenderer()
render_window = vtk.vtkRenderWindow()
render_window.SetWindowName("Sphere")
render_window.AddRenderer(renderer)
render_window_interactor = vtk.vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

renderer.AddActor(actor)
renderer.AddActor(actor2)
renderer.AddActor(actor3)
renderer.SetBackground(colors.GetColor3d("Black"))

render_window.Render()
render_window_interactor.Start()
    #############################################################
    # Aufgabe 3
    #transform = vtk.vtkTransform()
    #transform.Translate(3, 2, 1)
    #transform.SetInputConnection(Mond.GetOutputPort())
    #transform.Update()
    # Sign up to receive TimerEvent
    #cb = vtk.TimerCallback()
    #cb.actor = actor
    #vtk.renderWindowInteractor.AddObserver('TimerEvent', cb.execute)
    #timerId = vtk.renderWindowInteractor.CreateRepeatingTimer(100)

    #start the interaction and timer
    #vtk.renderWindowInteractor.Start()'''

