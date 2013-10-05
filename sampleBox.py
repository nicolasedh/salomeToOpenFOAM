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
sys.path.insert( 0, r'/home/nico/OpenFOAM/Salome/testFiles')

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
Box_1 = geompy.MakeBoxDXDYDZ(200, 200, 200)
listSubShapeIDs = geompy.SubShapeAllIDs(Box_1, geompy.ShapeType["FACE"])
top = geompy.CreateGroup(Box_1, geompy.ShapeType["FACE"])
geompy.UnionIDs(top, [33])
walls = geompy.CreateGroup(Box_1, geompy.ShapeType["FACE"])
geompy.UnionIDs(walls, [3, 13, 23, 27, 31])
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( Box_1, 'Box_1' )
geompy.addToStudyInFather( Box_1, top, 'top' )
geompy.addToStudyInFather( Box_1, walls, 'walls' )

###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New(theStudy)
from salome.NETGENPlugin import NETGENPluginBuilder
Mesh_1 = smesh.Mesh(Box_1)
NETGEN_2D3D = Mesh_1.Tetrahedron(algo=smeshBuilder.NETGEN_1D2D3D)
NETGEN_3D_Parameters = NETGEN_2D3D.Parameters()
NETGEN_3D_Parameters.SetMaxSize( 100 )
NETGEN_3D_Parameters.SetSecondOrder( 0 )
NETGEN_3D_Parameters.SetOptimize( 1 )
NETGEN_3D_Parameters.SetFineness( 2 )
NETGEN_3D_Parameters.SetMinSize( 50 )
isDone = Mesh_1.Compute()
top_1 = Mesh_1.GroupOnGeom(top,'top',SMESH.FACE)
walls_1 = Mesh_1.GroupOnGeom(walls,'walls',SMESH.FACE)

## set object names
smesh.SetName(Mesh_1.GetMesh(), 'Mesh_1')
smesh.SetName(NETGEN_2D3D.GetAlgorithm(), 'NETGEN_2D3D')
smesh.SetName(NETGEN_3D_Parameters, 'NETGEN 3D Parameters')
smesh.SetName(top_1, 'top')
smesh.SetName(walls_1, 'walls')

if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(1)

import salomeToOpenFOAM
import profile
profile.run("salomeToOpenFOAM.exportToFoam(Mesh_1,'./sampleBox/polyMesh')")


