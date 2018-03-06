# criar uma grelha vectorial

from osgeo import ogr
import os
import sys
from math import ceil

def grelha (OutGrelha, xmin, xmax, ymin, ymax, alturaGrelha, compGrelha):
    # converter as coordenas 'sys.argv' em float
    xmin = float (xmin)
    xmax = float (xmax)
    ymin = float (ymin)
    ymax = float (ymax)
    
    #criar linhas
    linhas = ceil ((ymax-ymin)/alturaGrelha)
    
    #criar colunas
    colunas = ceil ((xmax-xmin)/compGrelha)
    
    #criacao dos limites da grelha
    ringXleftOrigin = xmin
    ringXrightOrigin = xmin + compGrelha
    ringYtopOrigin = ymax
    ringYbottomOrigin = ymax-alturaGrelha
    
    # criacao do ficheiro de saida
    outDriver = ogr.GetDriverByName('ESRI Shapefile')
    
    if os.path.exists(OutGrelha):
        # Remove output file if exists
        os.remove(OutGrelha)
    
    # vai criar um novo ficheiro
    outDataSource = outDriver.CreateDataSource(OutGrelha)
    outLayer = outDataSource.CreateLayer(
        os.path.splitext(os.path.basename(OutGrelha))[0],
        geom_type=ogr.wkbPolygon
    )
    outLyrDefn = outLayer.GetLayerDefn()
        
    # criacao da grelha
    numeroColunas = 0
    while numeroColunas < colunas:
        numeroColunas += 1
        # Difinicao dos limites das linhas
        ringYtop = ringYtopOrigin
        ringYbottom = ringYbottomOrigin
        
        numeroLinhas = 0
        while numeroLinhas < linhas:
            numeroLinhas += 1
            #criar uma linha
            ring = ogr.Geometry(ogr.wkbLinearRing)
            ring.AddPoint(ringXleftOrigin, ringYtop)
            ring.AddPoint(ringXrightOrigin, ringYtop)
            ring.AddPoint(ringXrightOrigin, ringYbottom)
            ring.AddPoint(ringXleftOrigin, ringYbottom)
            ring.AddPoint(ringXleftOrigin, ringYtop)
            
            #criar um poligono
            poly = ogr.Geometry(ogr.wkbPolygon)
            #transforma a linha fechada em um poligono
            poly.AddGeometry(ring)
                 
            # adicionar o poligono ao layer 'OutGrelha'
            outFeature = ogr.Feature(outLyrDefn)
            outFeature.SetGeometry(poly)
            outLayer.CreateFeature(outFeature)
            outFeature = None
            
            #Limites do novo poligono
            ringYtop = ringYtop - alturaGrelha
            ringYbottom = ringYbottom - alturaGrelha
            
        #Limites do novo poligono
        ringXleftOrigin = ringXleftOrigin + compGrelha
        ringXrightOrigin = ringXrightOrigin + compGrelha
        
    # Salvar e fechar as fontes de dados
    outDataSource.Destroy()
    
    return OutGrelha

