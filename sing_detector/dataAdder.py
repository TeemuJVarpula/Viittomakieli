import os
import shutil

if input( "Are you sure you wisht to append images [y, n]: " ) != "y":
    print( "Terminated" )
    exit(0)

DATA_DIR_DST = "data"
DATA_DIR_SRC = [ "dataSushila", "dataSeppo", "dataTeemu" ]

for userDir in DATA_DIR_SRC:
    print( "userDir", userDir )
    
    for char in os.listdir( userDir ):
        pathSrc = os.path.join( userDir, char )
        startIndex = len( os.listdir( DATA_DIR_DST + "/" + char ) )

        for img in os.listdir( pathSrc ):
            pathDst = DATA_DIR_DST + "/" + char + "/" + str( startIndex ) + ".jpg"
            src = os.path.join( pathSrc, img )
            dst = pathDst
            shutil.copyfile( src, dst )
            startIndex += 1
