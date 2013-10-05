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
pipe = geompy.MakeCylinder(O, OX, 100, 1000)
wall = geompy.CreateGroup(pipe, geompy.ShapeType["FACE"])
geompy.UnionIDs(wall, [3])
inlet = geompy.CreateGroup(pipe, geompy.ShapeType["FACE"])
geompy.UnionIDs(inlet, [12])
outlet = geompy.CreateGroup(pipe, geompy.ShapeType["FACE"])
geompy.UnionIDs(outlet, [10])
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( pipe, 'pipe' )
geompy.addToStudyInFather( pipe, wall, 'wall' )
geompy.addToStudyInFather( pipe, inlet, 'inlet' )
geompy.addToStudyInFather( pipe, outlet, 'outlet' )

###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New(theStudy)
from salome.NETGENPlugin import NETGENPluginBuilder
from salome.StdMeshers import StdMeshersBuilder
Mesh_1 = smesh.Mesh(pipe)
NETGEN_2D = Mesh_1.Triangle(algo=smeshBuilder.NETGEN_1D2D)
NETGEN_2D_Parameters_wall = NETGEN_2D.Parameters()
NETGEN_2D_Parameters_wall.SetMaxSize( 20 )
NETGEN_2D_Parameters_wall.SetSecondOrder( 0 )
NETGEN_2D_Parameters_wall.SetOptimize( 1 )
NETGEN_2D_Parameters_wall.SetFineness( 2 )
NETGEN_2D_Parameters_wall.SetMinSize( 10 )
NETGEN_2D_Parameters_wall.SetQuadAllowed( 1 )
NETGEN_3D = Mesh_1.Tetrahedron()
NETGEN_3D_Parameters = NETGEN_3D.Parameters()
NETGEN_3D_Parameters.SetMaxSize( 20 )
NETGEN_3D_Parameters.SetSecondOrder( 0 )
NETGEN_3D_Parameters.SetOptimize( 1 )
NETGEN_3D_Parameters.SetFineness( 2 )
NETGEN_3D_Parameters.SetMinSize( 3 )
Viscous_Layers_1 = NETGEN_3D.ViscousLayers(20,4,1.3,[ 12, 10 ])
wall_1 = Mesh_1.GroupOnGeom(wall,'wall',SMESH.FACE)
inlet_1 = Mesh_1.GroupOnGeom(inlet,'inlet',SMESH.FACE)
outlet_1 = Mesh_1.GroupOnGeom(outlet,'outlet',SMESH.FACE)
NETGEN_2D_1 = Mesh_1.Triangle(algo=smeshBuilder.NETGEN_1D2D,geom=wall)
status = Mesh_1.AddHypothesis(NETGEN_2D_Parameters_wall,wall)
NETGEN_2D_2 = Mesh_1.Triangle(algo=smeshBuilder.NETGEN_1D2D,geom=inlet)
NETGEN_2D_Parameters = NETGEN_2D_2.Parameters()
NETGEN_2D_Parameters.SetMaxSize( 25 )
NETGEN_2D_Parameters.SetSecondOrder( 0 )
NETGEN_2D_Parameters.SetOptimize( 1 )
NETGEN_2D_Parameters.SetFineness( 2 )
NETGEN_2D_Parameters.SetMinSize( 5 )
NETGEN_2D_Parameters.SetQuadAllowed( 0 )
isDone = Mesh_1.Compute()
SubMesh_1 = NETGEN_2D_1.GetSubMesh()
SubMesh_2 = NETGEN_2D_2.GetSubMesh()

## set object names
smesh.SetName(Mesh_1.GetMesh(), 'Mesh_1')
smesh.SetName(NETGEN_2D.GetAlgorithm(), 'NETGEN_2D')
smesh.SetName(NETGEN_2D_Parameters_wall, 'NETGEN 2D Parameters wall')
smesh.SetName(NETGEN_3D.GetAlgorithm(), 'NETGEN_3D')
smesh.SetName(NETGEN_3D_Parameters, 'NETGEN 3D Parameters')
smesh.SetName(Viscous_Layers_1, 'Viscous Layers_1')
smesh.SetName(wall_1, 'wall')
smesh.SetName(inlet_1, 'inlet')
smesh.SetName(outlet_1, 'outlet')
smesh.SetName(NETGEN_2D_Parameters, 'NETGEN 2D Parameters in out')
smesh.SetName(SubMesh_1, 'SubMesh_1')
smesh.SetName(SubMesh_2, 'SubMesh_2')

if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(1)

import salomeToOpenFOAM
salomeToOpenFOAM.exportToFoam(Mesh_1,'./samplePipe/polyMesh')

