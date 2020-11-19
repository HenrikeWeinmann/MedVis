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
jpegSonne = "sun.jpg"
jpegErde = "earth.jpg"
jpegMond = "moon.jpg"

class Himmelskoerper():
    def __init__(self, Umkreisungskoerper, position, radius, color):

        self.Source = vtk.vtkSphereSource()
        self.Source.Umkreisungskoerper = Umkreisungskoerper
        self.Source.Position = self.Source.SetCenter(position)
        self.Source.SetRadius(radius)
        self.Source.color = color
        self.Source.SetPhiResolution(100)
        self.Source.SetThetaResolution(100)


refresh_rate = 60 # In Hertz
def callback_func(caller, timer_event):

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
'''transform = vtk.vtkTransform()
transform.Translate()
transformFilter = vtk.vtkTransformPolyDataFilter()
transformFilter.SetTransform(transform)
transformFilter.SetInputConnection(Erde.Source.GetOutputPort())
transformFilter.SetInputConnection(Mond.Source.GetOutputPort())
transformFilter.Update()'''
#############################################################
# fill the VTK rendering pipeline with the data of the objects
# source (-> filter) -> mapper -> actor -> renderer -> render window
#reader
readerSonne = vtk.vtkJPEGReader()
readerSonne.SetFileName(jpegSonne)
readerErde = vtk.vtkJPEGReader()
readerErde.SetFileName(jpegErde)
readerMond = vtk.vtkJPEGReader()
readerMond.SetFileName(jpegMond)

#texture
#Sonne
textureSonne = vtk.vtkTexture()
if vtk.VTK_MAJOR_VERSION <= 5:
    textureSonne.setInput(readerSonne.GetOutput())
else:
    textureSonne.SetInputConnection(readerSonne.GetOutputPort())

#Erde
textureErde = vtk.vtkTexture()
if vtk.VTK_MAJOR_VERSION <= 5:
    textureErde.setInput(readerErde.GetOutput())
else:
    textureErde.SetInputConnection(readerErde.GetOutputPort())

#Mond
textureMond = vtk.vtkTexture()
if vtk.VTK_MAJOR_VERSION <= 5:
    textureMond.setInput(readerMond.GetOutput())
else:
    textureMond.SetInputConnection(readerMond.GetOutputPort())

# Map texture coordinates
#Sonne
map_to_sphere_Sonne = vtk.vtkTextureMapToSphere()
if vtk.VTK_MAJOR_VERSION <= 5:
    map_to_sphere_Sonne.SetInput(Sonne.Source.GetOutput())
else:
    map_to_sphere_Sonne.SetInputConnection(Sonne.Source.GetOutputPort())
map_to_sphere_Sonne.PreventSeamOn()

#Erde
map_to_sphere_Erde = vtk.vtkTextureMapToSphere()
if vtk.VTK_MAJOR_VERSION <= 5:
    map_to_sphere_Erde.SetInput(Erde.Source.GetOutput())
else:
    map_to_sphere_Erde.SetInputConnection(Erde.Source.GetOutputPort())
map_to_sphere_Erde.PreventSeamOn()

#Mond
map_to_sphere_Mond = vtk.vtkTextureMapToSphere()
if vtk.VTK_MAJOR_VERSION <= 5:
    map_to_sphere_Mond.SetInput(Mond.Source.GetOutput())
else:
    map_to_sphere_Mond.SetInputConnection(Mond.Source.GetOutputPort())
map_to_sphere_Mond.PreventSeamOn()

#mapper
#Sonne
mapperSonne = vtk.vtkPolyDataMapper()

if vtk.VTK_MAJOR_VERSION <= 5:
    mapperSonne.SetInput(map_to_sphere_Sonne.GetOutput())
else:
    mapperSonne.SetInputConnection(map_to_sphere_Sonne.GetOutputPort())

#Erde
mapperErde = vtk.vtkPolyDataMapper()

if vtk.VTK_MAJOR_VERSION <= 5:
    mapperErde.SetInput(map_to_sphere_Erde.GetOutput())
else:
    mapperErde.SetInputConnection(map_to_sphere_Erde.GetOutputPort())

#Mond    
mapperMond = vtk.vtkPolyDataMapper()

if vtk.VTK_MAJOR_VERSION <= 5:
    mapperMond.SetInput(map_to_sphere_Mond.GetOutput())
else:
    mapperMond.SetInputConnection(map_to_sphere_Mond.GetOutputPort())

#actor
actorSonne = vtk.vtkActor()
actorErde = vtk.vtkActor()
actorMond = vtk.vtkActor()
actorSonne.SetMapper(mapperSonne)
actorSonne.SetTexture(textureSonne)
actorErde.SetMapper(mapperErde)
actorErde.SetTexture(textureErde)
actorMond.SetMapper(mapperMond)
actorMond.SetTexture(textureMond)

#############################################################
##Render
renderer = vtk.vtkRenderer()
renderer.AddActor(actorSonne)
renderer.AddActor(actorErde)
renderer.AddActor(actorMond)
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
