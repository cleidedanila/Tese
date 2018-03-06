"""
Procedure
"""

def main(xmin, xmax, ymin, ymax, width, height,
         path_to_grass_location, sysRef):
    """
    Para ja, faz o seguinte:
    * Inicia uma nova sessao do GRASS GIS
    (Para isto resultar no Windows, o caminho para o
    executavel do GRASS GIS deve constar na variavel
    de ambiente PATH)
    * Cria uma grelha regular vectorial (fishnet)
    * Adiciona essa grelha ao GRASS GIS
    """

    # Import modules
    import os
    
    from pyosm.grass_ import run_grass
    from pyosm.Grelha import grelha

    # Create a GRASS GIS Location and Mapset
    """
    Se path_to_grass_location tiver o valor:
    r'C:\um\caminho\qualquer'
    workspace vai ser igual a:
    r'C:\um\caminho
    e location vai ser igual a:
    'qualquer'
    """
    workspace  = os.path.dirname(path_to_grass_location)
    location   = os.path.basename(path_to_grass_location)
    grass_base = run_grass(workspace, location, sysRef)

    # Start GRASS GIS Session
    import grass.script as _grass_
    import grass.script.setup as gsetup
    gsetup.init(grass_base, workspace, location, 'PERMANENT')

    # Create a fishnet
    """
    Se path_to_grass_location tiver o valor:
    r'C:\um\caminho\qualquer'
    outGrelha sera igual a:
    r'C:\um\caminho\qualqer\grid_ref.shp'
    """
    outGrelha = os.path.join(
        path_to_grass_location,
        'grid_ref.shp'
    )
    outGrelha = grelha(outGrelha, xmin, xmax, ymin, ymax, height,
                       width)

    # Import fishnet to GRASS GIS
    from pyosm.grass_.tools import convert
    convert(outGrelha, 'grid_ref')

