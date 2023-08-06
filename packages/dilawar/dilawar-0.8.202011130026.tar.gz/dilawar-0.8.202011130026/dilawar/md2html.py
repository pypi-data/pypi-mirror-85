"""
Convert a pandoc file to HTML.
"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import re
from pathlib import Path
import subprocess 
from dilawar.pandoc.utils import available_pandoc_filters

srcFile_ = None
sdir_ = Path(__file__).parent

cdn = "http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"


pandoc_ = [ 'pandoc' 
        , '--mathml'
        , '--css', sdir_/"pandoc"/"theorem.css"
        , '--to', 'html5'
        ,  '--standalone', '--number-sections' , '--self-contained'
        ]

# append pandoc filters.
for cmd in available_pandoc_filters():
    pandoc_.append('-F')
    pandoc_.append(cmd)

# imgPat_ = re.compile( r'\!\[.*?\]\(?P<filename>.?\)' )
imgPat_ = re.compile( r'\!\[.*?\]\((?P<figure>.+?)\)', re.DOTALL )

def convertToPNG( img, text ):
    global srcFile_
    srcDir = os.path.dirname( srcFile_ )
    imgPath = os.path.join( srcDir, img )
    imgNameWe = '.'.join( img.split( '.' )[:-1] )
    pngPath = imgNameWe + '.png'
    if os.path.isfile( pngPath ):
        # File exits, if modification of png is later than the img then ignore.
        if os.path.getctime( pngPath ) > os.path.getctime( img ):
            text = text.replace( img, pngPath )
            return text

    print( 'Converting %s to %s' % (imgPath, pngPath) )
    cmd = [ 'convert', '-density', '300', '-quality', '90', imgPath, pngPath ]
    subprocess.check_output(cmd, shell = False )
    if not os.path.exists( pngPath ):
        print( '[WARN] to create PNG file' )
        print( '\t CMD: %s' % ' '.join( cmd ) )
    else:
        text = text.replace( img, pngPath )
    return text

def toHtml(text, outfile):
    global srcFile_
    global pandoc_
    htmlFile = outfile
    pFile = '%s_html.md' % srcFile_ 
    with open(pFile, 'w') as f:
        f.write(text)
    cmd = pandoc_ + [ '-o', htmlFile, pFile ]
    subprocess.call( cmd, shell = False )
    print( '[INFO] Wrote HTML to %s' % htmlFile )


def process(text, outfile):
    imgs = imgPat_.findall( text )
    for img in imgs:
        ext = img.split( '.' )[-1]
        if ext.lower( ) not in [ 'png', 'jpg', 'jpeg' ]:
            text = convertToPNG( img, text )

    with open( '/tmp/%s_html' % os.path.basename( srcFile_ ), 'w' ) as f:
        f.write( text )
    toHtml(text, outfile)

def main(args):
    global srcFile_
    srcFile_ = args.input
    with open( srcFile_, 'r' ) as f:
        text = f.read( )
    outfile = args.output or f'{srcFile_}.html'
    process(text, outfile)

if __name__ == '__main__':
    import argparse
    # Argument parser.
    description = '''Convert md to HTML'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('input', help = 'Input TeX file')
    parser.add_argument('--output', '-o'
            , required = False
            , help = 'Output file'
            )
    class Args: pass 
    args = Args()
    parser.parse_args(namespace=args)
    main(args)
