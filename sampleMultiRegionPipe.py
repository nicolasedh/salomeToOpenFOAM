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
Sphere_1 = geompy.MakeSphereR(10)
Cylinder_1 = geompy.MakeCylinder(Vertex_1, OX, 20, 150)
fluid_only = geompy.MakeCut(Cylinder_1, Sphere_1)
Partition_1 = geompy.MakePartition([fluid_only, Sphere_1], [], [], [], geompy.ShapeType["SOLID"], 0, [], 0)
wall = geompy.CreateGroup(Partition_1, geompy.ShapeType["FACE"])
geompy.UnionIDs(wall, [4])
outlet = geompy.CreateGroup(Partition_1, geompy.ShapeType["FACE"])
geompy.UnionIDs(outlet, [11])
inlet = geompy.CreateGroup(Partition_1, geompy.ShapeType["FACE"])
geompy.UnionIDs(inlet, [13])
fluid = geompy.CreateGroup(Partition_1, geompy.ShapeType["SOLID"])
geompy.UnionIDs(fluid, [2])
solid = geompy.CreateGroup(Partition_1, geompy.ShapeType["SOLID"])
geompy.UnionIDs(solid, [23])

geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( Vertex_1, 'Vertex_1' )
geompy.addToStudy( Sphere_1, 'Sphere_1' )
geompy.addToStudy( Cylinder_1, 'Cylinder_1' )
geompy.addToStudy( fluid_only, 'fluid_only' )
geompy.addToStudy( Partition_1, 'Partition_1' )
geompy.addToStudyInFather( Partition_1, wall, 'wall' )
geompy.addToStudyInFather( Partition_1, outlet, 'outlet' )
geompy.addToStudyInFather( Partition_1, inlet, 'inlet' )
geompy.addToStudyInFather( Partition_1, fluid, 'fluid' )
geompy.addToStudyInFather( Partition_1, solid, 'solid' )

###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New(theStudy)
from salome.NETGENPlugin import NETGENPluginBuilder
Mesh_1 = smesh.Mesh(Partition_1)
NETGEN_2D3D = Mesh_1.Tetrahedron(algo=smeshBuilder.NETGEN_1D2D3D)
NETGEN_3D_Parameters = NETGEN_2D3D.Parameters()
NETGEN_3D_Parameters.SetMaxSize( 5 )
NETGEN_3D_Parameters.SetSecondOrder( 0 )
NETGEN_3D_Parameters.SetOptimize( 1 )
NETGEN_3D_Parameters.SetFineness( 2 )
NETGEN_3D_Parameters.SetMinSize( 1 )
fluid_1 = Mesh_1.GroupOnGeom(fluid,'fluid',SMESH.VOLUME)
solid_1 = Mesh_1.GroupOnGeom(solid,'solid',SMESH.VOLUME)
wall_1 = Mesh_1.GroupOnGeom(wall,'wall',SMESH.FACE)
inlet_1 = Mesh_1.GroupOnGeom(inlet,'inlet',SMESH.FACE)
outlet_1 = Mesh_1.GroupOnGeom(outlet,'outlet',SMESH.FACE)
isDone = Mesh_1.Compute()

## set object names
smesh.SetName(Mesh_1.GetMesh(), 'Mesh_1')
smesh.SetName(NETGEN_2D3D.GetAlgorithm(), 'NETGEN_2D3D')
smesh.SetName(NETGEN_3D_Parameters, 'NETGEN 3D Parameters')
smesh.SetName(fluid_1, 'fluid')
smesh.SetName(solid_1, 'solid')
smesh.SetName(wall_1, 'wall')
smesh.SetName(inlet_1, 'inlet')
smesh.SetName(outlet_1, 'outlet')

if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(1)

import salomeToOpenFOAM
import profile
profile.run("salomeToOpenFOAM.exportToFoam(Mesh_1,'./sampleMultiRegionPipe/constant/polyMesh')")
#salomeToOpenFOAM.exportToFoam(Mesh_1,'./sampleMultiRegionPipe/constant/polyMesh')

#Note that no internal BC has ben set up. splitMeshRegions -cellZones will create regeionX_to_regionY
#Boundaries.
