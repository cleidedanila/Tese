# criar uma grelha vectorial

from osgeo import ogr
import sys
from math import ceil

def grelha (OutGrelha, xmin, xmax, ymin, ymax):
    
    # converter as coordenas 'sys.argv' em float
    
    alturaGrelha = input ("enter a grid heigtht: ")
    compGrelha = input ("enter a grid widtht: ")
    xmin = float (xmin)
    xmax = float (xmax)
    ymin = float (ymin)
    ymax = float (ymax)
    
    #criar linhas
    linhas = ceil ((ymax-ymin)/alturaGrelha)
    
    #criar colunas
    linhas = ceil ((xmax-xmin)/compGrelha)
    
    #criacao dos limites da grelha
    ringXleftOrigin = xmin
    ringXrightOrigin = xmin + compGrelha
    ringYtopOrigin = ymax
    ringYbottomOrigin = ymax-alturaGrelha
    
    # criacao do ficheiro de saida
    outDriver = ogr.GetDriverByName('ESRI Shapefile')
    
    if os.path.exists(OutGrelha):
        os.remove(OutGrelha)# vai remover o ficheiro de saída, caso haja
        outDataSource = outDriver.CreateDataSource(OutGrelha)# vai criar um novo ficheiro
        outLayer = outDataSource.CreateLayer(OutGrelha,geom_type=ogr.wkbPolygon)
        OutGrelha = outLayer.GetLayerDefn()
        
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
            poly.AddGeometry(ring)#transforma a linha fechada em um poligono
                 
            #adicionar o poligono ao layer 'OutGrelha'
            outFeature = ogr.Feature(OutGrelha)
            outFeature.SetGeometry(poly)
            outLayer.CreateFeature(outFeature)
            outFeature = None
            
            #Limites do novo poligono
            ringYtop = ringYtop - gridHeight
            ringYbottom = ringYbottom - gridHeight
            
        #Limites do novo poligono
        ringXleftOrigin = ringXleftOrigin + gridWidth
        ringXrightOrigin = ringXrightOrigin + gridWidth
        
        #Calcular a area da celula
        areaCelula = alturaGrelha * compGrelha
        
    # Salvar e fechar as fontes de dados
    outDataSource = None
    
    # intersepcao dos dois layers (grelha e resultado da conversão)
    