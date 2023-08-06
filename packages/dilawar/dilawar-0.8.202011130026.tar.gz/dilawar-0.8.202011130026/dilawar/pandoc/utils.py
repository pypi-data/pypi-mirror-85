__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2019-, Dilawar Singh"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"

import os
import re
import sys
import time
import subprocess
import colorama as C
from pathlib import Path

C.init(autoreset=True)

sdir_ = Path(os.path.realpath(__file__)).parent

all_ = [ 'pandoc-imagine'
        , 'pandoc-gls.py'
        # Pantable must come before citeproc else the citation in the table
        # will not be processed.
        , 'pantable'  
        , 'pandoc-crossref'
        , 'pandoc-citeproc' 
        , 'pandoc-imagine' 
        , 'pandoc-quantity.py'
        ]

# This is from  https://stackoverflow.com/a/377028/1805129
def which(program):
    def is_exe(fpath):
        fpath = os.path.realpath(fpath)
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None


def available_pandoc_filters():
    global all_
    cmds = [ which(prog) for prog in all_]
    return [str(x) for x in cmds if x is not None]

def _prefix(msg):
    return f"{C.Fore.BLUE}dilawar.pandoc>{C.Style.RESET_ALL}{msg.strip()}"

def executeCommand(cmd):
    print(_prefix(f"Executing {cmd}"), file=sys.stderr)
    cmd = cmd.split()
    p = subprocess.Popen(cmd
            , stdout=subprocess.PIPE
            , stderr=subprocess.STDOUT
            , stdin=sys.stdin
            # -variable
            , universal_newlines=True
            , encoding="utf-8"
            )
    while True:
        line = p.stdout.readline()
        if not line:
            break
        print(_prefix(line), file=sys.stderr)
    return p.returncode

def execute_pandoc(*args):
    """Top level command.
    """
    #  sdir = Path(__file__).parent
    #  css = sdir / 'pandoc.css'
    argStr = ' '.join(*args)
    extra = ''
    pandoc = which('pandoc')
    if re.search(r'-t\s+latex', argStr):
        extra += ' --pdf-engine lualatex -s'
    if re.search(r'-t\s+html\S*', argStr):
        # --katex may not work when we are behing proxy. So let USER specify it.
        extra += ' --self-contained'
        ##if re.search(r'--css\s+', argStr) is None:
        ##    extra += f' --css {css} '
    filters = ' '.join([f'-F {f}' for f in available_pandoc_filters()])
    cmd = f'{pandoc} {filters} {extra} ' + argStr
    t0 = time.time()
    st = executeCommand(cmd)
    print(_prefix(f" Took {time.time()-t0:.2f} sec"), file=sys.stderr)
    return st

def t_pandoc():
    # test pandoc.
    infile = Path(__file__).parent /'..'/'..'/'README.md'
    assert infile.exists(), infile
    execute_pandoc(f'-t html5 -o a.html {infile}'.split())
    

def test():
    t_pandoc()

if __name__ == '__main__':
    test()
