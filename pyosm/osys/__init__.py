"""
Operations related with Operative System

* Create, rename, manage, delete folders and files
"""

import os
import shutil

def os_name():
    import platform
    return str(platform.system())


def del_folder(folder):
    """
    Delete folder if exists
    """
    if os.path.exists(folder):
        shutil.rmtree(folder)

