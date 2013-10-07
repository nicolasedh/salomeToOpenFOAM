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
Vertex_1 = geompy.MakeVertex(-200, 0, 0)
Sphere_1 = geompy.MakeSphereR(10)
Cylinder_1 = geompy.MakeCylinder(Vertex_1, OX, 25, 400)
Cut_1 = geompy.MakeCut(Cylinder_1, Sphere_1)
cyllWall = geompy.CreateGroup(Cut_1, geompy.ShapeType["FACE"])
geompy.UnionIDs(cyllWall, [3])
outlet = geompy.CreateGroup(Cut_1, geompy.ShapeType["FACE"])
geompy.UnionIDs(outlet, [10])
inlet = geompy.CreateGroup(Cut_1, geompy.ShapeType["FACE"])
geompy.UnionIDs(inlet, [12])
sphereWall = geompy.CreateGroup(Cut_1, geompy.ShapeType["FACE"])
geompy.UnionIDs(sphereWall, [15])
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( Vertex_1, 'Vertex_1' )
geompy.addToStudy( Sphere_1, 'Sphere_1' )
geompy.addToStudy( Cylinder_1, 'Cylinder_1' )
geompy.addToStudy( Cut_1, 'Cut_1' )
geompy.addToStudyInFather( Cut_1, cyllWall, 'cyllWall' )
geompy.addToStudyInFather( Cut_1, outlet, 'outlet' )
geompy.addToStudyInFather( Cut_1, inlet, 'inlet' )
geompy.addToStudyInFather( Cut_1, sphereWall, 'sphereWall' )

###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New(theStudy)
from salome.NETGENPlugin import NETGENPluginBuilder
from salome.StdMeshers import StdMeshersBuilder
Mesh_1 = smesh.Mesh(Cut_1)
NETGEN_3D = Mesh_1.Tetrahedron()
NETGEN_3D_Parameters = NETGEN_3D.Parameters()
NETGEN_3D_Parameters.SetOptimize( 1 )
NETGEN_3D_Parameters.SetFineness( 2 )
Viscous_Layers_1 = NETGEN_3D.ViscousLayers(5,3,1.3,[ 10, 12 ])
NETGEN_2D = Mesh_1.Triangle(algo=smeshBuilder.NETGEN_1D2D,geom=sphereWall)
sphere_NETGEN_2D_Parameters = NETGEN_2D.Parameters()
sphere_NETGEN_2D_Parameters.SetMaxSize( 3 )
sphere_NETGEN_2D_Parameters.SetSecondOrder( 0 )
sphere_NETGEN_2D_Parameters.SetOptimize( 1 )
sphere_NETGEN_2D_Parameters.SetFineness( 2 )
sphere_NETGEN_2D_Parameters.SetQuadAllowed( 0 )
NETGEN_2D_ONLY = Mesh_1.Triangle(algo=smeshBuilder.NETGEN_2D,geom=outlet)
inout_NETGEN_2D_Parameters = NETGEN_2D_ONLY.Parameters()
inout_NETGEN_2D_Parameters.SetMaxSize( 5 )
inout_NETGEN_2D_Parameters.SetOptimize( 1 )
inout_NETGEN_2D_Parameters.SetFineness( 2 )
NETGEN_2D_ONLY_1 = Mesh_1.Triangle(algo=smeshBuilder.NETGEN_2D,geom=inlet)
status = Mesh_1.AddHypothesis(inout_NETGEN_2D_Parameters,inlet)
NETGEN_2D_1 = Mesh_1.Triangle(algo=smeshBuilder.NETGEN_1D2D,geom=cyllWall)
cyl_NETGEN_2D_Parameters = NETGEN_2D_1.Parameters()
cyl_NETGEN_2D_Parameters.SetMaxSize( 5 )
cyl_NETGEN_2D_Parameters.SetSecondOrder( 0 )
cyl_NETGEN_2D_Parameters.SetOptimize( 1 )
cyl_NETGEN_2D_Parameters.SetFineness( 2 )
cyl_NETGEN_2D_Parameters.SetQuadAllowed( 1 )
cyllWall_1 = Mesh_1.GroupOnGeom(cyllWall,'cyllWall',SMESH.FACE)
outlet_1 = Mesh_1.GroupOnGeom(outlet,'outlet',SMESH.FACE)
inlet_1 = Mesh_1.GroupOnGeom(inlet,'inlet',SMESH.FACE)
sphereWall_1 = Mesh_1.GroupOnGeom(sphereWall,'sphereWall',SMESH.FACE)
NETGEN_3D_Parameters.SetMaxSize( 6 )
NETGEN_3D_Parameters.SetSecondOrder( 0 )
NETGEN_3D_Parameters.SetMinSize( 0.5 )
Viscous_Layers_1.SetTotalThickness( 5 )
Viscous_Layers_1.SetNumberLayers( 3 )
Viscous_Layers_1.SetStretchFactor( 1.3 )
sphere_NETGEN_2D_Parameters.SetMinSize( 0.5 )
inout_NETGEN_2D_Parameters.SetSecondOrder( 0)
inout_NETGEN_2D_Parameters.SetMinSize( 0.5 )
cyl_NETGEN_2D_Parameters.SetMinSize( 0.5 )
inout_NETGEN_2D_Parameters.SetQuadAllowed( 0 )
isDone = Mesh_1.Compute()
sphere = NETGEN_2D.GetSubMesh()
outlet_2 = NETGEN_2D_ONLY.GetSubMesh()
inlet_2 = NETGEN_2D_ONLY_1.GetSubMesh()
cylWall = NETGEN_2D_1.GetSubMesh()

## set object names
smesh.SetName(Mesh_1.GetMesh(), 'Mesh_1')
smesh.SetName(NETGEN_3D.GetAlgorithm(), 'NETGEN_3D')
smesh.SetName(NETGEN_3D_Parameters, 'NETGEN 3D Parameters')
smesh.SetName(Viscous_Layers_1, 'Viscous Layers_1')
smesh.SetName(NETGEN_2D.GetAlgorithm(), 'NETGEN_2D')
smesh.SetName(sphere_NETGEN_2D_Parameters, 'sphere NETGEN 2D Parameters')
smesh.SetName(NETGEN_2D_ONLY.GetAlgorithm(), 'NETGEN_2D_ONLY')
smesh.SetName(inout_NETGEN_2D_Parameters, 'inout NETGEN 2D Parameters')
smesh.SetName(cyl_NETGEN_2D_Parameters, 'cyl NETGEN 2D Parameters')
smesh.SetName(cyllWall_1, 'cyllWall')
smesh.SetName(outlet_1, 'outlet')
smesh.SetName(inlet_1, 'inlet')
smesh.SetName(sphereWall_1, 'sphereWall')
smesh.SetName(sphere, 'sphere')
smesh.SetName(outlet_2, 'outlet')
smesh.SetName(inlet_2, 'inlet')
smesh.SetName(cylWall, 'cylWall')

if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(1)

import salomeToOpenFOAM
import profile
profile.run("salomeToOpenFOAM.exportToFoam(Mesh_1,'./sampleObstruction/polyMesh')")
