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
Cylinder_1 = geompy.MakeCylinder(O, OX, 100, 300)
Vertex_1 = geompy.MakeVertex(150, 0, 0)
Disk_1 = geompy.MakeDiskPntVecR(Vertex_1, OX, 60)
Partition_1 = geompy.MakePartition([Cylinder_1], [Disk_1], [], [], geompy.ShapeType["SOLID"], 0, [], 1)
baffle = geompy.CreateGroup(Partition_1, geompy.ShapeType["FACE"])
geompy.UnionIDs(baffle, [15])
walls = geompy.CreateGroup(Partition_1, geompy.ShapeType["FACE"])
geompy.UnionIDs(walls, [3])
inlet = geompy.CreateGroup(Partition_1, geompy.ShapeType["FACE"])
geompy.UnionIDs(inlet, [12])
outlet = geompy.CreateGroup(Partition_1, geompy.ShapeType["FACE"])
geompy.UnionIDs(outlet, [10])
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( Cylinder_1, 'Cylinder_1' )
geompy.addToStudy( Vertex_1, 'Vertex_1' )
geompy.addToStudy( Disk_1, 'Disk_1' )
geompy.addToStudy( Partition_1, 'Partition_1' )
geompy.addToStudyInFather( Partition_1, baffle, 'baffle' )
geompy.addToStudyInFather( Partition_1, walls, 'walls' )
geompy.addToStudyInFather( Partition_1, inlet, 'inlet' )
geompy.addToStudyInFather( Partition_1, outlet, 'outlet' )

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
NETGEN_3D_Parameters.SetMaxSize( 30 )
NETGEN_3D_Parameters.SetSecondOrder( 0 )
NETGEN_3D_Parameters.SetOptimize( 1 )
NETGEN_3D_Parameters.SetFineness( 2 )
NETGEN_3D_Parameters.SetMinSize( 10 )
baffle_1 = Mesh_1.GroupOnGeom(baffle,'baffle',SMESH.FACE)
walls_1 = Mesh_1.GroupOnGeom(walls,'walls',SMESH.FACE)
inlet_1 = Mesh_1.GroupOnGeom(inlet,'inlet',SMESH.FACE)
outlet_1 = Mesh_1.GroupOnGeom(outlet,'outlet',SMESH.FACE)
isDone = Mesh_1.Compute()
baffle_1.SetColor( SALOMEDS.Color( 1, 0.666667, 0 ))

## set object names
smesh.SetName(Mesh_1.GetMesh(), 'Mesh_1')
smesh.SetName(NETGEN_2D3D.GetAlgorithm(), 'NETGEN_2D3D')
smesh.SetName(NETGEN_3D_Parameters, 'NETGEN 3D Parameters')
smesh.SetName(baffle_1, 'baffle')
smesh.SetName(walls_1, 'walls')
smesh.SetName(inlet_1, 'inlet')
smesh.SetName(outlet_1, 'outlet')

if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(1)

import salomeToOpenFOAM as st
st.debug=0
st.exportToFoam(Mesh_1,"samplePipeWithBaffle/polyMesh")
print """
Mesh has been exported. The utility checkMesh
will report report the baffle as "multiply connected (shared edge)".
It seems that is not a problem
"""
