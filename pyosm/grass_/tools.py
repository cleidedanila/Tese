"""
Convert formats with GRASS GIS
"""

from grass.pygrass.modules import Module


def VectorialDrivers():
    return {
        '.shp': 'ESRI_Shapefile',
    }


def RasterDrivers():
    return {
        '.tif': 'GTiff',
        '.img': 'HFA'
    }


def convert(inLyr, outLyr, geom_type=None):
    """
    Add or export data from/to GRASS GIS
    """
    
    import os
    
    
    if os.path.splitext(inLyr)[1] in VectorialDrivers():
        inOrOut = 'import'
        data = 'vector'
    
    elif os.path.splitext(inLyr)[1] in RasterDrivers():
        inOrOut = 'import'
        data = 'raster'
    
    else:
        outFormat = os.path.splitext(outLyr)[1]
        inOrOut = 'export'
        if outFormat in VectorialDrivers():    
            data = 'vector'
        elif outFormat in RasterDrivers():
            data = 'raster'
        else:
            raise ValueError(
                "Not possible to identify if you want export or import data"
            )
    
    #*************************************************************************#
    if data == 'vector':
        if inOrOut == 'import':
            m = Module('v.in.ogr', input=inLyr, output=outLyr, flags='o',
                       overwrite=True, run_=False, quiet=True)
        elif inOrOut == 'export':
            m = Module('v.out.ogr', input=inLyr, type=geom_type, output=outLyr,
                       format=VectorialDrivers()[outFormat],
                       overwrite=True, run_=False, quiet=True)
    
    elif data == 'raster':
        if inOrOut == 'import':
            m = Module("r.in.gdal", input=inLyr, output=outLyr, flags='o',
                       overwrite=True, run_=False, quiet=True)
        elif inOrOut == 'export':
            m = Module("r.out.gdal", input=inLyr, output=outLyr,
                       format=RasterDrivers()[outFormat],
                       overwrite=True, run_=False, quiet=True)
    
    m()
