# -*- coding: iso-8859-1 -*-

###
### This file is generated automatically by SALOME v7.2.0 with dump python functionality
###

import sys
import salome

salome.salome_init()
theStudy = salome.myStudy

import salome_notebook
notebook = salome_notebook.NoteBook(theStudy)
sys.path.insert( 0, r'/home/nico/Dropbox/Projekt/Salome/salomeToOpenFOAM')

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS


geompy = geomBuilder.New(theStudy)

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
Vertex_1 = geompy.MakeVertex(-50, 0, 0)
solid = geompy.MakeSphereR(10)
[solid_to_fluid] = geompy.ExtractShapes(solid, geompy.ShapeType["FACE"], True)
Cylinder_1 = geompy.MakeCylinder(Vertex_1, OX, 20, 150)
fluid = geompy.MakeCut(Cylinder_1, solid)
[fluid_to_solid] = geompy.SubShapes(fluid, [0, 15])
walls = geompy.CreateGroup(fluid, geompy.ShapeType["FACE"])
geompy.UnionIDs(walls, [3])
inlet = geompy.CreateGroup(fluid, geompy.ShapeType["FACE"])
geompy.UnionIDs(inlet, [12])
outlet = geompy.CreateGroup(fluid, geompy.ShapeType["FACE"])
geompy.UnionIDs(outlet, [10])
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( Vertex_1, 'Vertex_1' )
geompy.addToStudy( solid, 'solid' )
geompy.addToStudyInFather( solid, solid_to_fluid, 'solid_to_fluid' )
geompy.addToStudy( Cylinder_1, 'Cylinder_1' )
geompy.addToStudy( fluid, 'fluid' )
geompy.addToStudyInFather( fluid, fluid_to_solid, 'fluid_to_solid' )
geompy.addToStudyInFather( fluid, walls, 'walls' )
geompy.addToStudyInFather( fluid, inlet, 'inlet' )
geompy.addToStudyInFather( fluid, outlet, 'outlet' )

###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New(theStudy)
from salome.StdMeshers import StdMeshersBuilder
from salome.NETGENPlugin import NETGENPluginBuilder
solidMesh = smesh.Mesh(solid)
NETGEN_2D = solidMesh.Triangle(algo=smeshBuilder.NETGEN_1D2D)
solid2Dparams = NETGEN_2D.Parameters()
solid2Dparams.SetMaxSize( 3 )
solid2Dparams.SetSecondOrder( 0 )
solid2Dparams.SetOptimize( 1 )
solid2Dparams.SetFineness( 2 )
solid2Dparams.SetMinSize( 0.1 )
solid2Dparams.SetQuadAllowed( 0 )
NETGEN_3D = solidMesh.Tetrahedron()
solid3Dparams = NETGEN_3D.Parameters()
solid3Dparams.SetMaxSize( 3 )
solid3Dparams.SetSecondOrder( 1 )
solid3Dparams.SetOptimize( 1 )
solid3Dparams.SetFineness( 2 )
solid3Dparams.SetMinSize( 0.1 )
solidLayers = NETGEN_3D.ViscousLayers(1,3,1.2,[  ])
fluidMesh = smesh.Mesh(fluid)
NETGEN_3D_1 = fluidMesh.Tetrahedron()
fluid3Dparams = NETGEN_3D_1.Parameters()
fluid3Dparams.SetMaxSize( 5 )
fluid3Dparams.SetSecondOrder( 1 )
fluid3Dparams.SetOptimize( 1 )
fluid3Dparams.SetFineness( 2 )
fluid3Dparams.SetMinSize( 0.1 )
fluidLayers = NETGEN_3D_1.ViscousLayers(3,3,1.2,[ 12, 10 ])
solid_to_fluid_1 = solidMesh.GroupOnGeom(solid_to_fluid,'solid_to_fluid',SMESH.FACE)
walls_1 = fluidMesh.GroupOnGeom(walls,'walls',SMESH.FACE)
inlet_1 = fluidMesh.GroupOnGeom(inlet,'inlet',SMESH.FACE)
outlet_1 = fluidMesh.GroupOnGeom(outlet,'outlet',SMESH.FACE)
Import_1D2D = fluidMesh.UseExisting2DElements(geom=fluid_to_solid)
Source_Faces_1 = Import_1D2D.SourceFaces([ solid_to_fluid_1 ],0,0)
solid_1 = solidMesh.GroupOnGeom(solid,'solid',SMESH.VOLUME)
fluid_1 = fluidMesh.GroupOnGeom(fluid,'fluid',SMESH.VOLUME)
isDone = solidMesh.Compute()
NETGEN_2D_1 = fluidMesh.Triangle(algo=smeshBuilder.NETGEN_1D2D)
fluid2Dparams = NETGEN_2D_1.Parameters()
fluid2Dparams.SetMaxSize( 3 )
fluid2Dparams.SetSecondOrder( 0 )
fluid2Dparams.SetOptimize( 1 )
fluid2Dparams.SetFineness( 2 )
fluid2Dparams.SetMinSize( 0.1 )
fluid2Dparams.SetQuadAllowed( 0 )
isDone = fluidMesh.Compute()
FinalMesh = smesh.Concatenate([solidMesh.GetMesh(), fluidMesh.GetMesh()], 1, 1, 1e-05)
[ solid_to_fluid_2, solid_2, walls_2, inlet_2, outlet_2, fluid_2 ] = FinalMesh.GetGroups()
SubMesh_1 = Import_1D2D.GetSubMesh()

## set object names
smesh.SetName(solidMesh.GetMesh(), 'solidMesh')
smesh.SetName(NETGEN_2D.GetAlgorithm(), 'NETGEN_2D')
smesh.SetName(solid2Dparams, 'solid2Dparams')
smesh.SetName(NETGEN_3D.GetAlgorithm(), 'NETGEN_3D')
smesh.SetName(solid3Dparams, 'solid3Dparams')
smesh.SetName(solidLayers, 'solidLayers')
smesh.SetName(fluidMesh.GetMesh(), 'fluidMesh')
smesh.SetName(fluid3Dparams, 'fluid3Dparams')
smesh.SetName(fluidLayers, 'fluidLayers')
smesh.SetName(solid_to_fluid_1, 'solid_to_fluid')
smesh.SetName(walls_1, 'walls')
smesh.SetName(inlet_1, 'inlet')
smesh.SetName(outlet_1, 'outlet')
smesh.SetName(Import_1D2D.GetAlgorithm(), 'Import_1D2D')
smesh.SetName(Source_Faces_1, 'Source Faces_1')
smesh.SetName(solid_1, 'solid')
smesh.SetName(fluid_1, 'fluid')
smesh.SetName(fluid2Dparams, 'fluid2Dparams')
smesh.SetName(FinalMesh.GetMesh(), 'FinalMesh')
smesh.SetName(solid_to_fluid_2, 'solid_to_fluid')
smesh.SetName(solid_2, 'solid')
smesh.SetName(walls_2, 'walls')
smesh.SetName(inlet_2, 'inlet')
smesh.SetName(outlet_2, 'outlet')
smesh.SetName(fluid_2, 'fluid')
smesh.SetName(SubMesh_1, 'SubMesh_1')

if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(1)

import salomeToOpenFOAM as sof
sof.debug=0
sof.exportToFoam(FinalMesh,'./sampleMultiRegionPipeWithViscous/polyMesh')
print """
Mesh has been exported. 
Run the OpenFOAM utility 
splitMeshRegions -cellZones
to split the mesh in regeions

"""
