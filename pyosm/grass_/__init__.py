"""
GIS API's subpackage:

GRASS GIS Python tools
"""


import os
import sys

from ..osys import os_name
from ..osys import del_folder
from ..osys.shell import execute_cmd


def open_grass_linux(gisdb, location, srs):
    """
    Method to open GRASS GIS on Linux Systems
    
    Parameters:
    * gisdb - abs path to grass workspace
    * location - name for the grass location
    * srs - epsg or file to define spatial reference system of the location that 
    will be created
    """    
    # Delete location if exists
    if os.path.exists(os.path.join(gisdb, location)):
        del_folder(os.path.join(gisdb, location))
    
    grassbin = 'grass72'
    startcmd = grassbin + ' --config path'
    
    code, out, err = execute_cmd(startcmd)
    if code != 0:
        print (
            'Kind: OPEN GRASS on get config path\n'
            'Output: {o} \nError: {e}'
        ).format(
            o=str(out), e=str(err)
        )
        sys.exit(-1)
    
    gisbase = out.strip('\n')
    # Set GISBASE environment variable
    os.environ['GISBASE'] = gisbase
    # the following not needed with trunk
    os.environ['PATH'] += os.pathsep + os.path.join(gisbase, 'extrabin')
    # add path to GRASS addons
    home = os.path.expanduser("~")
    os.environ['PATH'] += os.pathsep + os.path.join(home, '.grass7', 'addons', 'scripts')    
    # define GRASS-Python environment
    gpydir = os.path.join(gisbase, "etc", "python")
    sys.path.append(gpydir)
    location_path = os.path.join(gisdb, location)
    if type(srs) == type(1):
        startcmd = grassbin + ' -c epsg:' + str(srs) + ' -e ' + location_path
    elif type(srs) == type('string'):
        startcmd = grassbin + ' -c ' + srs + ' -e ' + location_path
    
    code, out, err = execute_cmd(startcmd)
    if code != 0:
        print (
            'Kind: OPEN GRASS on location creation\n'
            'Output: {o}\n'
            'Error: {e}'
        ).format(
            o=str(out), e=str(err)
        )
        sys.exit(-1)
    
    # Set GISDBASE environment variable
    os.environ['GISDBASE'] = gisdb
    
    # See if there is location
    if not os.path.exists(os.path.join(gisdb, location)):
        print 'NoError, but location is not created'
        sys.exit(-1)
    
    return gisbase



def open_grass_windows(gisdb, location, srs):
    """
    Method to open GRASS GIS on MS Windows Systems
    
    Parameters:
    * gisdb - abs path to grass workspace
    * location - name for the grass location
    * srs - epsg or file to define spatial reference system of the location that 
    will be created
    
    
    To work, Path to GRASS GIS must be in the PATH Environment 
    Variable
    """
    
    # Delete location if exists
    if os.path.exists(os.path.join(gisdb, location)):
        del_folder(os.path.join(gisdb, location))
    
    # the path to grass can't have white spaces
    grassbin = 'grass72'
    startcmd = grassbin + ' --config path'
    code, out, err = execute_cmd(startcmd)
    if code != 0:
        print (
            'Kind: OPEN GRASS on get config path\n'
            'Output: {o} \nError: {e}'
            ).format(
                o=str(out), e=str(err)
            )
        sys.exit(-1)
    
    # Set GISBASE environment variable
    gisbase = out.strip().split('\r\n')[0]
    os.environ['GRASS_SH'] = os.path.join(gisbase, 'msys', 'bin', 'sh.exe')
    os.environ['GISBASE'] = gisbase
    # define GRASS-Python environment
    gpydir = os.path.join(gisbase, "etc", "python")
    sys.path.append(gpydir)
    
    # define database location
    location_path = os.path.join(gisdb, location)
    if type(srs) == type(1):
        startcmd = '{gb} -c epsg:{e} -e {lp}'.format(
            gb=grassbin, e=srs, lp=location_path
        )
    elif type(srs) == type('string'):
        startcmd = '{gb} -c {extf} -e {lp}'.format(
            gb=grassbin, extf=srs, lp=location_path
        )
    
    # open grass
    code, out, err = execute_cmd(startcmd)
    
    if code != 0:
        print (
            'Kind: OPEN GRASS on location creation\n'
            'Output: {o}\n'
            'Error: {e}'
            ).format(
                o=str(out), e=str(err)
            )
        sys.exit(-1)
    
    # Set GISDBASE environment variable
    os.environ['GISDBASE'] = gisdb
    return gisbase


def run_grass(workspace, location, srs):
    """
    Generic method that could be used to put GRASS GIS running in any Os
    
    To work on MSWindows, Path to GRASS Must be in the PATH Environment 
    Variables
    """
    
    __os = os_name()
    
    base = open_grass_linux(
        workspace, location, srs
    ) if __os == 'Linux' else open_grass_windows(
        workspace, location, srs
    ) if __os == 'Windows' else None
    
    if not base:
        raise ValueError((
            'Could not identify operating system'
        ))
    
    return base

