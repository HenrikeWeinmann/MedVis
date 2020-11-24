# Nicole, Hannah, Henrike
#MedVis Blatt1
import vtk
import math
refresh_rate = 60 # In Hertz


class Himmelskoerper():
    def __init__(self, Umkreisungskoerper, X,Y,Z, radius, texture, speed):

        self.Source = vtk.vtkSphereSource()
        self.Source.Umkreisungskoerper = Umkreisungskoerper
        self.Source.SetCenter(X, Y, Z)
        self.Source.Position = [X, Y, Z]
        self.Source.SetRadius(radius)
        self.Source.Texture = texture
        self.Source.SetPhiResolution(100)
        self.Source.SetThetaResolution(100)
        self.Source.Speed = speed


#############################################################
# Create the objects that should be rendered

Sonne = Himmelskoerper(0, 0, 0, 0, 4, "sun.jpg", 0)
Venus = Himmelskoerper(Sonne, 6, -4, 0, 1.1, "venus.jpg", 100)
Erde = Himmelskoerper(Sonne,9,6, 0, 1, "earth.jpg", 300)
Mond = Himmelskoerper(Erde, 2, 1, 0, 0.5, "moon.jpg", 70)
Mars = Himmelskoerper(Sonne, 12, -13.5, 0, 0.75, "mars.jpg", 600)



def callback_func(caller, timer_event):
    transformErde.Translate(newPos(Erde))
    transformErdeFilter.Update()
    transformMond.Translate(newPos(Mond))
    transformMondFilter.Update()
    translateMond()
    transformMars.Translate(newPos(Mars))
    transformMarsFilter.Update()
    transformVenus.Translate(newPos(Venus))
    transformVenusFilter.Update()
    actorSonne.RotateZ(1)

    window.Render()


def newPos(Himmelskoerper):
    speed = Himmelskoerper.Source.Speed
    pos = Himmelskoerper.Source.Position
    deg = math.pi/speed
    oldPos = Himmelskoerper.Source.Position
    newpos = [(math.cos(deg) * oldPos[0] - math.sin(deg) * oldPos[1]),
              (math.sin(deg) * oldPos[0] + math.cos(deg) * oldPos[1]),
              (oldPos[2])]

    updatePos(Himmelskoerper, newpos)
    return [newpos[0] - pos[0], newpos[1] - pos[1], newpos[2] - pos[2]]


def updatePos(Himmelskoerper,newpos):
    Himmelskoerper.Source.Position = newpos

def translateMond():
    actorMond.SetPosition(Erde.Source.Position)


# get the names of VTK's predefined colors
colors = vtk.vtkNamedColors()


#############################################################
#Transformer
#Sonne
transformSonne = vtk.vtkTransform()
transformSonneFilter = vtk.vtkTransformPolyDataFilter()
transformSonneFilter.SetTransform(transformSonne)
transformSonneFilter.SetInputConnection(Sonne.Source.GetOutputPort())

#Erde
transformErde = vtk.vtkTransform()
transformErdeFilter = vtk.vtkTransformPolyDataFilter()
transformErdeFilter.SetTransform(transformErde)
transformErdeFilter.SetInputConnection(Erde.Source.GetOutputPort())

#Mond
transformMond = vtk.vtkTransform()
transformMondFilter = vtk.vtkTransformPolyDataFilter()
transformMondFilter.SetTransform(transformMond)
transformMondFilter.SetInputConnection(Mond.Source.GetOutputPort())

#Mars
transformMars = vtk.vtkTransform()
transformMarsFilter = vtk.vtkTransformPolyDataFilter()
transformMarsFilter.SetTransform(transformMars)
transformMarsFilter.SetInputConnection(Mars.Source.GetOutputPort())

#Venus
transformVenus = vtk.vtkTransform()
transformVenusFilter = vtk.vtkTransformPolyDataFilter()
transformVenusFilter.SetTransform(transformVenus)
transformVenusFilter.SetInputConnection(Venus.Source.GetOutputPort())


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

##################################################################
# Map texture coordinates
#Sonne
map_to_sphere_Sonne = vtk.vtkTextureMapToSphere()
map_to_sphere_Sonne.SetInputConnection(Sonne.Source.GetOutputPort())


#Erde
map_to_sphere_Erde = vtk.vtkTextureMapToSphere()
map_to_sphere_Erde.SetInputConnection(transformErdeFilter.GetOutputPort())


#Mond
map_to_sphere_Mond = vtk.vtkTextureMapToSphere()
map_to_sphere_Mond.SetInputConnection(transformMondFilter.GetOutputPort())

#Mars
map_to_sphere_Mars = vtk.vtkTextureMapToSphere()
map_to_sphere_Mars.SetInputConnection(transformMarsFilter.GetOutputPort())


#Venus
map_to_sphere_Venus = vtk.vtkTextureMapToSphere()
map_to_sphere_Venus.SetInputConnection(transformVenusFilter.GetOutputPort())


##################################################################

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

##################################################################
#actor
actorSonne = vtk.vtkActor()
actorSonne.SetMapper(mapperSonne)
actorSonne.SetTexture(textureSonne)

actorErde = vtk.vtkActor()
actorErde.SetMapper(mapperErde)
actorErde.SetTexture(textureErde)

actorMond = vtk.vtkActor()
actorMond.SetMapper(mapperMond)
actorMond.SetTexture(textureMond)

actorMars = vtk.vtkActor()
actorMars.SetMapper(mapperMars)
actorMars.SetTexture(textureMars)

actorVenus = vtk.vtkActor()
actorVenus.SetMapper(mapperVenus)
actorVenus.SetTexture(textureVenus)

##################################################################
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
window.SetSize(1000,1000)
#interactor
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(window)
interactor.Initialize()
interactor.CreateRepeatingTimer(int(1/refresh_rate))
interactor.AddObserver("TimerEvent", callback_func)
# set camera position
cam = renderer.GetActiveCamera()
cam.SetPosition(0,0,70)

window.Render()
interactor.Start()
