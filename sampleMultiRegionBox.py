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
Box_1 = geompy.MakeBoxDXDYDZ(200, 100, 100)
Vertex_1 = geompy.MakeVertex(100, 0, 0)
Plane_1 = geompy.MakePlane(Vertex_1, OX, 2000)
Partition_1 = geompy.MakeHalfPartition(Box_1, Plane_1)
fluid = geompy.CreateGroup(Partition_1, geompy.ShapeType["SOLID"])
geompy.UnionIDs(fluid, [2])
solid = geompy.CreateGroup(Partition_1, geompy.ShapeType["SOLID"])
geompy.UnionIDs(solid, [36])
solidWal = geompy.CreateGroup(Partition_1, geompy.ShapeType["FACE"])
geompy.UnionIDs(solidWal, [52, 38, 48, 55, 58])
fluidWall = geompy.CreateGroup(Partition_1, geompy.ShapeType["FACE"])
geompy.UnionIDs(fluidWall, [31, 26, 21, 4, 14])
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( Box_1, 'Box_1' )
geompy.addToStudy( Vertex_1, 'Vertex_1' )
geompy.addToStudy( Plane_1, 'Plane_1' )
geompy.addToStudy( Partition_1, 'Partition_1' )
geompy.addToStudyInFather( Partition_1, fluid, 'fluid' )
geompy.addToStudyInFather( Partition_1, solid, 'solid' )
geompy.addToStudyInFather( Partition_1, solidWal, 'solidWal' )
geompy.addToStudyInFather( Partition_1, fluidWall, 'fluidWall' )

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
NETGEN_3D_Parameters.SetMaxSize( 200 )
NETGEN_3D_Parameters.SetSecondOrder( 0 )
NETGEN_3D_Parameters.SetOptimize( 1 )
NETGEN_3D_Parameters.SetFineness( 2 )
NETGEN_3D_Parameters.SetMinSize( 100 )
fluid_1 = Mesh_1.GroupOnGeom(fluid,'fluid',SMESH.VOLUME)
solid_1 = Mesh_1.GroupOnGeom(solid,'solid',SMESH.VOLUME)
solidWal_1 = Mesh_1.GroupOnGeom(solidWal,'solidWal',SMESH.FACE)
fluidWall_1 = Mesh_1.GroupOnGeom(fluidWall,'fluidWall',SMESH.FACE)
isDone = Mesh_1.Compute()

## set object names
smesh.SetName(Mesh_1.GetMesh(), 'Mesh_1')
smesh.SetName(NETGEN_2D3D.GetAlgorithm(), 'NETGEN_2D3D')
smesh.SetName(NETGEN_3D_Parameters, 'NETGEN 3D Parameters')
smesh.SetName(fluid_1, 'fluid')
smesh.SetName(solid_1, 'solid')
smesh.SetName(solidWal_1, 'solidWal')
smesh.SetName(fluidWall_1, 'fluidWall')

if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(1)

import salomeToOpenFOAM
import profile
profile.run("salomeToOpenFOAM.exportToFoam(Mesh_1,'./sampleMultiRegionBox/constant/polyMesh')")
#salomeToOpenFOAM.exportToFoam(Mesh_1,'./sampleMultiRegionBox/constant/polyMesh')
#Note that no internal BC has ben set up. splitMeshRegions -cellZones will create regeionX_to_regionY
#Boundaries.
