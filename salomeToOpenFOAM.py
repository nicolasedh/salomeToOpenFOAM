u"""
Export a Salome Mesh to OpenFOAM.

It handles all types of cells. Use 
salomeToOpenFOAM.exportToFoam(Mesh_1) 
to export. Optionally an output dir can be given as argument.

It's also possible to select a mesh in the object browser and
run the script via file->load script (ctrl-T).

Groups of volumes will be treated as cellZones. If they are 
present they will be put in the file cellZones. In order to convert
to regions use the OpenFOAM tool 
splitMeshRegions - cellZones

No sorting of faces is done so you'll have to run
renumberMesh -overwrite
In order to use the mesh.
"""
#Copyright 2013
#Author Nicolas Edh,
#Nicolas.Edh@gmail.com,
#or user "nsf" at cfd-online.com
#
#License
#
#    This script is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    salomeToOpenFOAM  is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with hexBlocker.  If not, see <http://www.gnu.org/licenses/>.
#
#    The license is included in the file LICENSE.
#

import sys
import salome
import SMESH
from salome.smesh import smeshBuilder
import os,time

#different levels of verbosities, 0 all quiet,
#higher values means more information
debug=1


verify=False
"""verify face order, migt take longer time"""

#Note: to skip renumberMesh just sort owner 
#while moving positions also move neighbour,faces, and bcfaces
#will probably have to first sort the internal faces then bc-faces within each bc

#obj=theStudy.FindObjectByName('name').GetObject()
def exportToFoam(mesh,dirname='polyMesh'):
    u"""
    Export a mesh to OpenFOAM.

    dirname is the output directory i.e. constant/polyMesh

    The algorith works as follows.
    First loop through the boundaries and collect all faces
    in each group. Faces that don't have a group will be added
    to the group defaultPatches.

    Next loop through all cells (volumes) and each face in the cell. 
    If the face has been visited before we add it to the neighbour list
    If it hasn't been visited before then it might be a boundary face. 
    If so then add the cell to the end of owner. If it's not a boundary face and
    has not yet been visited then add it to the list of internal faces. 

    In order to compare if faces has been visited a dictionary is used. 
    The key is the sorted list of face nodes converted to a string. The value 
    is the face id. I.e.

    facesSorted[key]=value
    """
    starttime=time.time()
    #try to open files
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    try:
        filePoints=open(dirname +"/points",'w')
        fileFaces=open(dirname +"/faces",'w')
        fileOwner=open(dirname + "/owner",'w')
        fileNeighbour=open(dirname + "/neighbour",'w')
        fileBoundary=open(dirname + "/boundary",'w')
    except Exception:
        print "could not open files aborting"
        return

    #Get salome properties
    theStudy = salome.myStudy
    smesh = smeshBuilder.New(theStudy)
    

    __debugPrint__('Number of nodes: %d\n' %(mesh.NbNodes()))
    volumes=mesh.GetElementsByType(SMESH.VOLUME)
    __debugPrint__("Number of cells: %d\n" %len(volumes))
    __debugPrint__('Counting number of faces:\n')
    #Filter faces
    filter=smesh.GetFilter(SMESH.EDGE,SMESH.FT_FreeFaces)
    extFaces=mesh.GetIdsFromFilter(filter)
    nrBCfaces=len(extFaces)
    nrExtFaces=len(extFaces)
    #nrBCfaces=mesh.NbFaces();#number of bcfaces in Salome

    nrFaces=0;
    for v in volumes:
        nrFaces+=mesh.ElemNbFaces(v)
    #all internal faces will be counted twice, external faces once
    #so:
    nrFaces=(nrFaces+nrExtFaces)/2
    nrIntFaces=nrFaces-nrBCfaces #
    __debugPrint__('total number of faces: %d, internal: %d, external %d\n'  \
        %(nrFaces,nrIntFaces,nrExtFaces))

    __debugPrint__("Converting mesh to OpenFOAM\n")
    faces=[] #list of internal face nodes ((1 2 3 4 ... ))
    facesSorted=dict() #each list of nodes is sorted.
    bcFaces=[] #list of bc faces (
    bcFacesSorted=dict()
    owner=[] #owner file, (of face id, volume id)
    neighbour=[] #neighbour file (of face id, volume id) only internal faces

#Loop over all salome boundary elemets (faces) 
# and store them inte the list bcFaces
    grpStartFace=[] # list of face ids where the BCs starts
    grpNrFaces=[] # list of number faces in each BC
    grpNames=[] #list of the group name.
    ofbcfid=0;  # bc face id in openfoam
    nrExtFacesInGroups=0
    for gr in mesh.GetGroups():
        if gr.GetType() == SMESH.FACE:
            grpNames.append(gr.GetName())
            __debugPrint__('found group \"%s\" of type %s, %d\n' \
                           %(gr.GetName(),gr.GetType(),len(gr.GetIDs())),2)
            nr=len(gr.GetIDs())
            if  nr >0 :
                grpStartFace.append(nrIntFaces+ofbcfid)
                grpNrFaces.append(nr)
            #loop over faces in group
            for sfid in gr.GetIDs():
                fnodes=mesh.GetElemNodes(sfid)
                key="%s" %sorted(fnodes)
                if not key in bcFacesSorted:
                    bcFaces.append(fnodes)
                    bcFacesSorted[key]=ofbcfid
                    ofbcfid=ofbcfid+1
                else:
                    raise Exception(\
                        "Error the face, elemId %d, %s belongs to two " %(sfid,fnodes)  +\
                            "or more groups. One is : %s"  %(gr.GetName()))

            #if the group is a baffle then the faces should be added twice
            if __isGroupBaffle__(mesh,gr,extFaces):
                nrBCfaces+=nr
                nrFaces+=nr
                nrIntFaces-=nr
                #since nrIntFaces is reduced all previously grpStartFaces are 
                #out of sync
                grpStartFace=[x-nr for x in grpStartFace]
                grpNrFaces[-1]=nr*2
                for sfid in gr.GetIDs():
                    fnodes=mesh.GetElemNodes(sfid)
                    key="%s" %sorted(fnodes,reverse=True)
                    bcFaces.append(fnodes)
                    bcFacesSorted[key]=ofbcfid
                    ofbcfid=ofbcfid+1
            else:
                nrExtFacesInGroups+=nr

    __debugPrint__('total number of faces: %d, internal: %d, external %d\n'  \
        %(nrFaces,nrIntFaces,nrExtFaces),2)
    #Do the defined groups cover all BC-faces?
    if nrExtFacesInGroups < nrExtFaces:
        __debugPrint__("Warning, some elements don't have a group (BC). " +\
                       "Adding to a new group called defaultPatches\n",1)
        grpStartFace.append(nrIntFaces+ofbcfid)
        grpNrFaces.append(nrExtFaces-nrExtFacesInGroups)
        salomeIDs=[]
        for face in extFaces:
            fnodes=mesh.GetElemNodes(face)
            key="%s" %sorted(fnodes)
            try:
                bcFacesSorted[key]
            except KeyError:
                #if not in dict then add to default patches
                bcFaces.append(fnodes)
                bcFacesSorted[key]=ofbcfid
                salomeIDs.append(face)
                ofbcfid+=1
        newGrpName="defaultPatches"
        nri=1
        while newGrpName in grpNames:
            newGrpName="defaultPatches_%d" %nri
            nri+=1
        grpNames.append(newGrpName)
        #function might have different name
        try:
            defGroup=mesh.CreateGroup(SMESH.FACE, 'defaultPatches' )
        except AttributeError:
            defGroup=mesh.CreateEmptyGroup(SMESH.FACE, 'defaultPatches' )

        defGroup.Add(salomeIDs)
        smesh.SetName(defGroup, 'defaultPatches')
        if salome.sg.hasDesktop():
            salome.sg.updateObjBrowser(1)

    #initialise the list faces vs owner/neighbour cells
    owner=[-1]*nrFaces
    neighbour=[-1]*nrIntFaces
    __debugPrint__("Finished processing boundary faces\n")
    __debugPrint__('bcFaces: %d\n' %(len(bcFaces)),2)
    __debugPrint__(str(bcFaces)+"\n",3)
    __debugPrint__('bcFacesSorted: %d\n' %(len(bcFacesSorted)),2)
    __debugPrint__(str(bcFacesSorted)+"\n",3)
    __debugPrint__('owner: %d\n' %(len(owner)),2)
    __debugPrint__(str(owner)+"\n",3)
    __debugPrint__('neighbour: %d\n' %(len(neighbour)),2)
    __debugPrint__(str(neighbour)+"\n",3)


    offid=0;
    ofvid=0; #volume id in openfoam
    for v in volumes:
        nodes=mesh.GetElemNodes(v)
        __debugPrint__('volume id: %d, num nodes %d, nodes:%s \n' %(v,len(nodes),nodes),3)
        nbface=mesh.ElemNbFaces(v)
        for fi in range(0,nbface):
            fnodes=mesh.GetElemFaceNodes(v,fi)
            #Check if the node is already in list
            try:
                key="%s" %sorted(fnodes)
                fidinof=facesSorted[key]
                #if faceSorted didn't throw an exception then the face is 
                #already in the dict. Its an internal face and should be added 
                # to the neighbour list
                #print "fidinof %d" %fidinof
                neighbour[fidinof]=ofvid
                __debugPrint__('\tan owner already exist for %d, %s, cell %d\n' %(fi,fnodes,ofvid),3)
            except KeyError:
                #the face is not in the list of internal faces
                #it might a new face or a BCface.
                try:
                    key="%s" %sorted(fnodes)
                    bcind=bcFacesSorted[key]
                    #if no exception was trown then it's a bc face
                    __debugPrint__('\t found bc face: %d, %s, cell %d\n' %(bcind,fnodes,ofvid),3)
                    #if the face belongs to a baffle then it exits twice in owner
                    #check dont overwrite owner
                    if owner[nrIntFaces+bcind]==-1:
                        owner[nrIntFaces+bcind]=ofvid
                        bcFaces[bcind]=fnodes
                    else:
                        #build functions that looks for baffles in bclist. with bcind
                        key="%s" %sorted(fnodes,reverse=True)
                        bcind=bcFacesSorted[key]
                        #make sure the faces has the correct orientation
                        bcFaces[bcind]=fnodes
                        owner[nrIntFaces+bcind]=ofvid
                except KeyError:
                    #the face is not in bc list either so it's a new internal face
                    __debugPrint__('\t a new face was found, %d, %s, cell %d\n' %(fi,fnodes,ofvid),3)
                    if verify:
                        if not __verifyFaceOrder__(mesh,nodes,fnodes):
                            __debugPrint__("\t face has bad order, reversing order\n",3)
                            fnodes.reverse()
                    faces.append(fnodes)
                    key="%s" %sorted(fnodes)
                    facesSorted[key]=offid
                    owner[offid]=ofvid
                    offid=offid+1
                    if(nrFaces > 50 and offid % (nrFaces/50)==0):
                        if(offid % ((nrFaces/50)*10) == 0):
                            __debugPrint__(':',1)
                        else:
                            __debugPrint__('.',1)

        ofvid=ofvid+1;
# end for v in volumes

    nrCells=ofvid
    __debugPrint__("Finished processing volumes.\n")
    __debugPrint__('faces: %d\n' %(len(faces)),2)
    __debugPrint__(str(faces)+"\n",3)
    __debugPrint__('facesSorted: %d\n' %(len(facesSorted)),2)
    __debugPrint__(str(facesSorted)+"\n",3)
    __debugPrint__('owner: %d\n' %(len(owner)),2)
    __debugPrint__(str(owner)+"\n",3)
    __debugPrint__('neighbour: %d\n' %(len(neighbour)),2)
    __debugPrint__(str(neighbour)+"\n",3)


    #Convert to "upper triangular order"
    #owner is sorted, for each cell sort faces it's neighbour faces
    # i.e. change 
    # owner   neighbour          owner   neighbour
    #     0          15                    0                3
    #     0            3          to       0              15
    #     0           17                   0              17
    #     1            5                    1                5
    # any changes made to neighbour are repeated to faces.
    __debugPrint__("Sorting faces in upper triangular order\n",1)
    ownedfaces=1
    for faceId in xrange(0,nrIntFaces):
        cellId=owner[faceId]
        nextCellId=owner[faceId+1] #np since len(owner) > nrIntFaces
        if cellId == nextCellId:
            ownedfaces+=1
            continue
        
        if ownedfaces >1:
            sId=faceId-ownedfaces+1 #start ID
            eId=faceId #end ID
            inds=range(sId,eId+1)
            inds.sort(key=neighbour.__getitem__)
            neighbour[sId:eId+1]=map(neighbour.__getitem__,inds)
            faces[sId:eId+1]=map(faces.__getitem__,inds)

        ownedfaces=1
    converttime=time.time()-starttime

    #WRITE points to file
    __debugPrint__("Writing the file points\n")
    __writeHeader__(filePoints,"points")
    points=mesh.GetElementsByType(SMESH.NODE)
    nrPoints=len(points)
    filePoints.write("\n%d\n(\n" %(nrPoints))
    for n,ni in enumerate(points):
        pos=mesh.GetNodeXYZ(ni)
        filePoints.write("\t(%g %g %g)\n" %(pos[0],pos[1],pos[2]))
    filePoints.write(")\n")
    filePoints.flush()
    filePoints.close()

    #WRITE faces to file
    __debugPrint__("Writing the file faces\n")
    __writeHeader__(fileFaces,"faces")
    fileFaces.write("\n%d\n(\n" %(nrFaces))
    for node in faces:
        fileFaces.write("\t%d(" %(len(node)))
        for p in node:
            #salome starts to count from one, OpenFOAM from zero
            fileFaces.write("%d " %(p-1))
        fileFaces.write(")\n")
    #internal nodes are done output bcnodes
    for node in bcFaces:
        fileFaces.write("\t%d(" %(len(node)))
        for p in node:
            #salome starts to count from one, OpenFOAM from zero
            fileFaces.write("%d " %(p-1))
        fileFaces.write(")\n")
    fileFaces.write(")\n")
    fileFaces.flush()
    fileFaces.close()

    #WRITE owner to file
    __debugPrint__("Writing the file owner\n")
    __writeHeader__(fileOwner,"owner",nrPoints,nrCells,nrFaces,nrIntFaces)
    fileOwner.write("\n%d\n(\n" %(len(owner)))
    for cell in owner:
        fileOwner.write(" %d \n" %(cell))
    fileOwner.write(")\n")
    fileOwner.flush()
    fileOwner.close()

    #WRITE neighbour
    __debugPrint__("Writing the file neighbour\n")
    __writeHeader__(fileNeighbour,"neighbour",nrPoints,nrCells,nrFaces,nrIntFaces)
    fileNeighbour.write("\n%d\n(\n" %(len(neighbour)))
    for cell in neighbour:
        fileNeighbour.write(" %d\n" %(cell))
    fileNeighbour.write(")\n")
    fileNeighbour.flush()
    fileNeighbour.close()

    #WRITE boundary file
    __debugPrint__("Writing the file boundary\n")
    __writeHeader__(fileBoundary,"boundary")
    fileBoundary.write("%d\n(\n" %len(grpStartFace))
    for ind,gname in enumerate(grpNames):
        fileBoundary.write("\t%s\n\t{\n" %gname)
        fileBoundary.write("\ttype\t\t")
        if "wall" in gname.lower():
            fileBoundary.write("wall;\n")
        else:
            fileBoundary.write("patch;\n")
        fileBoundary.write("\tnFaces\t\t%d;\n" %grpNrFaces[ind])
        fileBoundary.write("\tstartFace\t%d;\n" %grpStartFace[ind])
        fileBoundary.write("\t}\n")
    fileBoundary.write(")\n")
    fileBoundary.close()

    #WRITE cellZones
#Count number of cellZones
    nrCellZones=0;
    cellZonesName=list();
    for grp in mesh.GetGroups():
        if grp.GetType() == SMESH.VOLUME:
            nrCellZones+=1
            cellZonesName.append(grp.GetName())
    if nrCellZones > 0:
        try:
            fileCellZones=open(dirname + "/cellZones",'w')
        except Exception:
            print "Could not open the file cellZones, other files are ok."
        __debugPrint__("Writing file cellZones\n")
        #create a dictionary where salomeIDs are keys
        #and OF cell ids are values.
        scToOFc=dict([sa,of] for of,sa in enumerate(volumes))
        __writeHeader__(fileCellZones,"cellZones")
        fileCellZones.write("\n%d(\n" %nrCellZones)
        for grp in mesh.GetGroups():
            if grp.GetType() == SMESH.VOLUME:
                fileCellZones.write(grp.GetName()+"\n{\n")
                fileCellZones.write("\ttype\tcellZone;\n")
                fileCellZones.write("\tcellLabels\tList<label>\n")
                cellSalomeIDs=grp.GetIDs()
                nrGrpCells=len(cellSalomeIDs)
                fileCellZones.write("%d\n(\n" %nrGrpCells)
                for csId in cellSalomeIDs:
                    ofID=scToOFc[csId]
                    fileCellZones.write("%d\n" %ofID)

                fileCellZones.write(");\n}\n")
        fileCellZones.write(")\n")
        fileCellZones.flush()
        fileCellZones.close()

    totaltime=time.time()-starttime
    __debugPrint__("Finished writing to %s/%s \n" %(os.getcwd(),dirname))
    __debugPrint__("Converted mesh in %.0fs\n" %(converttime),1)
    __debugPrint__("Wrote mesh in %.0fs\n" %(totaltime-converttime),1)
    __debugPrint__("Total time: %0.fs\n" %totaltime,1)
                   

def __writeHeader__(file,fileType,nrPoints=0,nrCells=0,nrFaces=0,nrIntFaces=0):
    """Write a header for the files points, faces, owner, neighbour"""

    file.write("/*" + "-"*68 + "*\\\n" )
    file.write("|" + " "*70 + "|\n")
    file.write("|" + " "*4 + "File exported from Salome Platform" +\
                   " using SalomeToFoamExporter" +" "*5 +"|\n")
    file.write("|" + " "*70 + "|\n")
    file.write("\*" + "-"*68 + "*/\n")

    file.write("FoamFile\n{\n")
    file.write("\tversion\t\t2.0;\n")
    file.write("\tformat\t\tascii;\n")
    file.write("\tclass\t\t")
    if(fileType =="points"):
        file.write("vectorField;\n")
    elif(fileType =="faces"):
        file.write("faceList;\n")
    elif(fileType =="owner" or fileType=="neighbour"):
        file.write("labelList;\n")
        file.write("\tnote\t\t\"nPoints: %d nCells: %d nFaces: %d nInternalFaces: %d\";\n" \
                       %(nrPoints,nrCells,nrFaces,nrIntFaces))
    elif(fileType == "boundary"):
        file.write("polyBoundaryMesh;\n")
    elif(fileType=="cellZones"):
        file.write("regIOobject;\n")
    file.write("\tlocation\t\"constant/polyMesh\";\n")
    file.write("\tobject\t\t" + fileType +";\n")
    file.write("}\n\n")


    
def __debugPrint__(msg,level=1):
    """Print only if level >= debug """
    if(debug >= level ):
        print msg,


def __verifyFaceOrder__(mesh,vnodes,fnodes):
    """ 
    Verify if the face order is correct. I.e. pointing out of the cell 

    calc vol center
    calc f center 
    calc ftov=fcenter-vcenter 
     calc fnormal=first to second cross first to last
    if ftov dot fnormal >0 reverse order

    """
    vc=__cog__(mesh,vnodes)
    fc=__cog__(mesh,fnodes)
    fcTovc=__diff__(vc,fc)
    fn=__calcNormal__(mesh,fnodes)
    if(__dotprod__(fn,fcTovc)>0.0):
        return False
    else:
        return True
    
def __cog__(mesh,nodes):
    """
    calculate the center of gravity. 
    """
    c=[0.0,0.0,0.0]
    for n in nodes:
        pos=mesh.GetNodeXYZ(n)
        c[0]+=pos[0]
        c[1]+=pos[1]
        c[2]+=pos[2]
    c[0]/=len(nodes)
    c[1]/=len(nodes)
    c[2]/=len(nodes)
    return c

def __calcNormal__(mesh,nodes):
    """ 
    Calculate and return face normal. 
    """
    p0=mesh.GetNodeXYZ(nodes[0])
    p1=mesh.GetNodeXYZ(nodes[1])
    pn=mesh.GetNodeXYZ(nodes[-1])
    u=__diff__(p1,p0)
    v=__diff__(pn,p0)
    return __crossprod__(u,v)
                       
                 
    
def __diff__(u,v):
    """ 
    u - v, in 3D 
    """
    res=[0.0]*3
    res[0]=u[0]-v[0]
    res[1]=u[1]-v[1]
    res[2]=u[2]-v[2]
    return res
    
def __dotprod__(u,v):
    """ 
    3D scalar dot product 
    """
    return u[0]*v[0] + u[1]*v[1] + u[2]*v[2]

def __crossprod__(u,v):
    """
    3D cross product 
    """
    res=[0.0]*3
    res[0]=u[1]*v[2]-u[2]*v[1]
    res[1]=u[2]*v[0]-u[0]*v[2]
    res[2]=u[0]*v[1]-u[1]*v[0]
    return res

def findSelectedMeshes():
    meshes=list()
    smesh = smeshBuilder.New(salome.myStudy)
    nrSelected=salome.sg.SelectedCount() # total number of selected items
    
    foundMesh=False
    for i in range(nrSelected):
        selected=salome.sg.getSelected(i)
        selobjID=salome.myStudy.FindObjectID(selected)
        selobj=selobjID.GetObject()
        if selobj.__class__ == SMESH._objref_SMESH_Mesh or selobj.__class__ == salome.smesh.smeshBuilder.meshProxy :
            mName=selobjID.GetName().replace(" ","_")
            foundMesh=True
            mesh=smesh.Mesh(selobj)
            meshes.append(mesh)

    if not foundMesh:
        print "You have to select a mesh object and then run this script."
        print "or run the export function directly from TUI"
        print " import SalomeToOpenFOAM"
        print " SalomeToOpenFOAM.exportToFoam(mesh,path)" 
        return list()
    else:
        return meshes

def __isGroupBaffle__(mesh,group,extFaces):
    for sid in group.GetIDs():
        if not sid in extFaces:
            __debugPrint__("group %s is a baffle\n" %group.GetName(),1)
            return True
    return False
        

def main():
    """ 
    Main function. Export the selected mesh.
    
    Will try to find the selected mesh.
    """
    meshes=findSelectedMeshes()
    for mesh in meshes:
        if not mesh == None:
            mName=mesh.GetName()
            outdir=os.getcwd()+"/"+mName+"/constant/polyMesh"
            __debugPrint__("found selected mesh exporting to " + outdir + ".\n",1)            
            exportToFoam(mesh,outdir)
            __debugPrint__("finished exporting\n",1)
            
    
if __name__ == "__main__":
    main()
