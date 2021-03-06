import vtk
from vtkmodules.util.colors import red
from vtkmodules.util.colors import green
from vtkmodules.util.colors import blue
from vtkmodules.util.colors import black
# ------------------------------------------------------
# Insert the path to your data for the exercise here


data_root = "/Users/Heni/Downloads/Blatt 2/python/"
# here you can choose the mode that should be used to
# visualize the given data
visualization_mode = 'color_map'  # None, 'color_map', 'cutting', 'probing', 'isosurf'
# ------------------------------------------------------

# Insert explanations for this section------------------
# Type of reader that can read PLOT3D files and generates structured grid(s) as an output.
pl3d = vtk.vtkMultiBlockPLOT3DReader()
# adds a file name to a series of files using the super class AddFileName()
pl3d.SetXYZFileName(data_root + "combxyz.bin")
pl3d.SetQFileName(data_root + "combq.bin")
# Specify the scalar function to extract.
#
# If ==(-1), then no scalar function is extracted.
pl3d.SetScalarFunctionNumber(100)
# Specify the vector function to extract.
#
# If ==(-1), then no vector function is extracted.
pl3d.SetVectorFunctionNumber(202)
# Specify additional functions to read.
#
# These are placed into the point data as data arrays. Later on they can be used by labeling them as scalars, etc.
pl3d.AddFunction(153)
# Update() is required when you want to use an object before the pipeline updates it for you.
pl3d.Update()
# returns a Block at a given index
pl3d_output = pl3d.GetOutput().GetBlock(0)
# End section ------------------------------------------

#geometryFilter = vtk.vtkStructuredGridGeometryFilter
#geometryFilter.SetInputData(pl3d_output)
#geometryFilter.SetExtent(1,100,1,100,7,7)
#lut = vtk.vtkLookupTable()
#geometryFilter_mapper = vtk.vtkPolyDataMapper()
#geometryFilter_mapper.SetLookUpTable(lut)
#geometryFilter_mapper.SetInputConnection(geometryFilter.GetOutputPort())
#geometryFilter_mapper.SetScalarRange(pl3d_output.GetScalarRange())
#geometryFilter_actor = vtk.vtkActor()
#geometryFilter_actor.SetMapper(geometryFilter_mapper)
plane = vtk.vtkStructuredGridGeometryFilter()
plane.SetInputData(pl3d_output)
plane.SetExtent(1, 100, 1, 100, 7, 7)
lut = vtk.vtkLookupTable()
lut.SetNumberOfColors(256)
lut.Build()
for i in range(0, 16):
    lut.SetTableValue(i*16, red[0], red[1], red[2], 1)
    lut.SetTableValue(i*16+1, green[0], green[1], green[2], 1)
    lut.SetTableValue(i*16+2, blue[0], blue[1], blue[2], 1)
    lut.SetTableValue(i*16+3, black[0], black[1], black[2], 1)
planeMapper = vtk.vtkPolyDataMapper()
planeMapper.SetLookupTable(lut)
planeMapper.SetInputConnection(plane.GetOutputPort())
planeMapper.SetScalarRange(pl3d_output.GetScalarRange())
planeActor = vtk.vtkActor()
planeActor.SetMapper(planeMapper)

# Create the RenderWindow and Renderer
renderer = vtk.vtkRenderer()
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window_interactor = vtk.vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# create an outline to your data using the vtkStructuredGridOutlineFiler()
outline = vtk.vtkStructuredGridOutlineFilter()
outline.SetInputData(pl3d_output)
outline_mapper = vtk.vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())
outline_actor = vtk.vtkActor()
outline_actor.SetMapper(outline_mapper)

# ------------------------------------------------------
if visualization_mode == 'color_map':
    import Color_Mapper as color_mapper

    color_mapper.visualize(pl3d_output, renderer)
elif visualization_mode == 'cutting':
    import Cutter as cutter

    cutter.visualize(pl3d_output, renderer)
elif visualization_mode == 'probing':
    import Probe as probe

    probe.visualize(pl3d_output, renderer)
elif visualization_mode == 'isosurf':
    import Isosurf as isosurf

    isosurf.visualize(pl3d_output, renderer)
# ------------------------------------------------------

renderer.AddActor(outline_actor)
#renderer.AddActor(geometryFilter_actor)
renderer.SetBackground(0.1, 0.2, 0.4)
render_window.SetSize(1200, 1200)

cam1 = renderer.GetActiveCamera()
cam1.SetClippingRange(3.94, 50)
cam1.SetFocalPoint(9.7, 0.5, 29.4)
cam1.SetPosition(2.7, -37.3, 38.7)
cam1.SetViewUp(-0.16, 0.26, 0.95)

if __name__ == "__main__":
    render_window_interactor.Initialize()
    render_window.Render()
    render_window_interactor.Start()
