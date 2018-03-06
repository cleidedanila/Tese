"""
Tools for executing sheel commands
"""


def execute_cmd(cmd):
    """
    Execute a command and provide information about the results
    """
    import subprocess
    
    p = subprocess.Popen(cmd, shell=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    out, err = p.communicate()
    
    return p.returncode, out, err