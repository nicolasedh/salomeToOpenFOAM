salomeToOpenFOAM
================

A python script that outputs a Salome mesh to OpenFOAM

To run just select the mesh you wish to export and 
go to file->load script and run salomeToOpenFOAM

Support for regions, or rather cellZones has been added.
Create groups of volumes, these will be exported to a file
called cellZones, in order to split use 
splitMeshRegions -cellZones

The face are reoreded to "upper triangular order" but
you might still benifit from a renumberMesh.

License

    This script is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    salomeToOpenFOAM  is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with hexBlocker.  If not, see <http://www.gnu.org/licenses/>.

    The license is included in the file LICENSE.