#from __future__ import print_function
import vtk
import math

class vtkTimerCallback():
   def __init__(self):
       self.timer_count = 1

   def execute(self, obj, event):
       print(self.timer_count)
       self.actorErde.RotateX(Erde.Rotationsgeschwindigkeit)
       self.actorErde.SetPosition(math.cos(math.radians(self.timer_count * 360 / Erde.Umrundungsdauer)) * (abs(Sonne.Position[0] - Erde.Position[0])) - (abs(Sonne.Position[0] - Erde.Position[0])), 0, math.sin(math.radians(self.timer_count * 360 / Erde.Umrundungsdauer)) * (abs(Sonne.Position[0] - Erde.Position[0])))
       self.actorMond.SetPosition(math.cos(math.radians(self.timer_count * 360 / Erde.Umrundungsdauer)) * (abs(Sonne.Position[0] - Erde.Position[0])) - (abs(Sonne.Position[0] - Erde.Position[0])) + math.cos(math.radians(self.timer_count * 360 / Mond.Umrundungsdauer)) * (abs(Erde.Position[0] - Mond.Position[0])) - (abs(Erde.Position[0] - Mond.Position[0])), 0, math.sin(math.radians(self.timer_count * 360 / Erde.Umrundungsdauer)) * (abs(Sonne.Position[0] - Erde.Position[0])) + math.sin(math.radians(self.timer_count * 360 / Mond.Umrundungsdauer)) * (abs(Mond.Position[0] - Erde.Position[0])))
       self.actorVenus.SetPosition(math.cos(math.radians(self.timer_count * 360 / Venus.Umrundungsdauer)) * (abs(Sonne.Position[0] - Venus.Position[0])) - (abs(Sonne.Position[0] - Venus.Position[0])), 0, math.sin(math.radians(self.timer_count * 360 / Venus.Umrundungsdauer)) * (abs(Sonne.Position[0] - Venus.Position[0])))
       self.actorMars.SetPosition(math.cos(math.radians(self.timer_count * 360 / Mars.Umrundungsdauer)) * (abs(Sonne.Position[0] - Mars.Position[0])) - (abs(Sonne.Position[0] - Mars.Position[0])), 0, math.sin(math.radians(self.timer_count * 360 / Mars.Umrundungsdauer)) * (abs(Sonne.Position[0] - Mars.Position[0])))
       obj.GetRenderWindow().Render()
       self.timer_count += 1


class Himmelskörper:
   def __init__(self, Himmelskörper_2, Position, Radius, Farbe, Umrundungsdauer, image, Rotationsgeschwindigkeit):
      self.Radius = Radius
      self.Farbe = Farbe
      self.Himmelskörper_2 = Himmelskörper_2
      self.Position = Position
      self.Umrundungsdauer = Umrundungsdauer
      self.image = image
      self.Rotationsgeschwindigkeit = Rotationsgeschwindigkeit


# Raius im Maßstab 100000:1
Sonne = Himmelskörper(None, [0, 0, 0], 13.92, "Yellow", None, "Bild_Sonne.jpg", 0)
# Radius im Maßstab 2500:1, Umlaufzeit in Tagen, Position im Maßstab 5000000:1
Erde = Himmelskörper(Sonne, [Sonne.Position[0] + 30, Sonne.Position[1], Sonne.Position[2]], 4.25, "Blue", 365, "Bild_Erde.jpg", 365)
Mond = Himmelskörper(Erde, [Erde.Position[0] + 7, Erde.Position[1], Erde.Position[2]], 1.16, "Grey", 27.32, "Bild_Mond.jpg", 0)
Venus = Himmelskörper(Sonne, [Sonne.Position[0] + 21.6, Sonne.Position[1], Sonne.Position[2]], 4.03, None, 225, "Bild_Venus.jpg", 365)
Mars = Himmelskörper(Sonne, [Sonne.Position[0] + 45.6, Sonne.Position[1], Sonne.Position[2]], 2.26, None, 687, "Bild_Mars.jpg", 365)


def build_source(planet):
    sphere_source = vtk.vtkSphereSource()
    sphere_source.SetCenter(planet.Position[0], planet.Position[1], planet.Position[2])
    sphere_source.SetRadius(planet.Radius)
    # Make the surface smooth.
    sphere_source.SetPhiResolution(100)
    sphere_source.SetThetaResolution(100)
    return sphere_source

def build_texture(source, mapper, planet):
    # Read the image data from a file
    Planet_image = planet.image
    reader = vtk.vtkJPEGReader()
    reader.SetFileName(Planet_image)

    # Create texture object
    Planet_texture = vtk.vtkTexture()
    if vtk.VTK_MAJOR_VERSION <= 5:
        Planet_texture.SetInput(reader.GetOutput())
    else:
        Planet_texture.SetInputConnection(reader.GetOutputPort())

    # Map texture coordinates
    map_to_planet = vtk.vtkTextureMapToSphere()
    if vtk.VTK_MAJOR_VERSION <= 5:
        map_to_planet.SetInput(source.GetOutput())
    else:
        map_to_planet.SetInputConnection(source.GetOutputPort())
    map_to_planet.PreventSeamOn()

    # Create mapper and set the mapped texture as input
    # mapper = vtk.vtkPolyDataMapper()
    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper.SetInput(map_to_planet.GetOutput())
    else:
        mapper.SetInputConnection(map_to_planet.GetOutputPort())

    return Planet_texture


def main():
   colors = vtk.vtkNamedColors()

#############################################################
# Create the objects that should be rendered
# Create a sphere using the vtk class.
   Sonne_source = build_source(Sonne)
   Erde_source = build_source(Erde)
   Mond_source = build_source(Mond)
   Venus_source = build_source(Venus)
   Mars_source = build_source(Mars)


#############################################################
# Setup mapper and actor for the Planets
   Sonne_mapper = vtk.vtkPolyDataMapper()
   Sonne_mapper.SetInputConnection(Sonne_source.GetOutputPort())

   Sonne_actor = vtk.vtkActor()
   Sonne_actor.SetMapper(Sonne_mapper)
   #Sonne_actor.GetProperty().SetColor(colors.GetColor3d(Sonne.Farbe))

   Erde_mapper = vtk.vtkPolyDataMapper()
   Erde_mapper.SetInputConnection(Erde_source.GetOutputPort())

   Erde_actor = vtk.vtkActor()
   Erde_actor.SetMapper(Erde_mapper)
   #Erde_actor.GetProperty().SetColor(colors.GetColor3d(Erde.Farbe))

   Mond_mapper = vtk.vtkPolyDataMapper()
   Mond_mapper.SetInputConnection(Mond_source.GetOutputPort())

   Mond_actor = vtk.vtkActor()
   Mond_actor.SetMapper(Mond_mapper)
   #Mond_actor.GetProperty().SetColor(colors.GetColor3d(Mond.Farbe))

   Venus_mapper = vtk.vtkPolyDataMapper()
   Venus_mapper.SetInputConnection(Venus_source.GetOutputPort())

   Venus_actor = vtk.vtkActor()
   Venus_actor.SetMapper(Venus_mapper)
   #Venus_actor.GetProperty().SetColor(colors.GetColor3d(Venus.Farbe))

   Mars_mapper = vtk.vtkPolyDataMapper()
   Mars_mapper.SetInputConnection(Mars_source.GetOutputPort())

   Mars_actor = vtk.vtkActor()
   Mars_actor.SetMapper(Mars_mapper)
   #Mars_actor.GetProperty().SetColor(colors.GetColor3d(Mars.Farbe))


#############################################################
# Setup a renderer, render window, and interactor
   renderer = vtk.vtkRenderer()
   renderWindow = vtk.vtkRenderWindow()
   renderWindow.AddRenderer(renderer);
   renderWindowInteractor = vtk.vtkRenderWindowInteractor()
   renderWindowInteractor.SetRenderWindow(renderWindow)

# Add the texture to the source
   Mond_actor.SetTexture(build_texture(Mond_source, Mond_mapper, Mond))
   Sonne_actor.SetTexture(build_texture(Sonne_source, Sonne_mapper, Sonne))
   Erde_actor.SetTexture(build_texture(Erde_source, Erde_mapper, Erde))
   Venus_actor.SetTexture(build_texture(Venus_source, Venus_mapper, Venus))
   Mars_actor.SetTexture(build_texture(Mars_source, Mars_mapper, Mars))

#Add the actor to the scene
   renderer.AddActor(Mond_actor)
   renderer.AddActor(Erde_actor)
   renderer.AddActor(Sonne_actor)
   renderer.AddActor(Venus_actor)
   renderer.AddActor(Mars_actor)
   renderer.SetBackground(colors.GetColor3d("Black")) # Background color Black

#Render and interact
   renderWindow.Render()

# Initialize must be called prior to creating timer events.
   renderWindowInteractor.Initialize()

   # Sign up to receive TimerEvent
   cb = vtkTimerCallback()
   cb.actorErde = Erde_actor
   cb.actorMond = Mond_actor
   cb.actorVenus = Venus_actor
   cb.actorMars = Mars_actor
   renderWindowInteractor.AddObserver('TimerEvent', cb.execute)
   timerId = renderWindowInteractor.CreateRepeatingTimer(100)  #Rate mit der Bild aktualisiert wird

   #start the interaction and timer
   renderWindowInteractor.Start()


if __name__ == '__main__':
   main()