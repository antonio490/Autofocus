
import sys
import os
import csv
import shutil
import pandas as pd
from csv import writer

dSmall = "img_root/small"
dBig = "img_root/big"
dFocus = "img_root/focus"


fAlbum = "album/"


def createFolders():

    wdir = os.getcwd()
    new_dirs = ["/img_root", "/small", "/big", "/focus"]

    if not os.path.exists(wdir+new_dirs[0]):
        os.mkdir(wdir+new_dirs[0]) 
    
    if not os.path.exists(wdir+new_dirs[0]+new_dirs[1]):
        os.mkdir(wdir+new_dirs[0]+new_dirs[1])  

    if not os.path.exists(wdir+new_dirs[0]+new_dirs[2]):
        os.mkdir(wdir+new_dirs[0]+new_dirs[2]) 

    if not os.path.exists(wdir+new_dirs[0]+new_dirs[3]):
        os.mkdir(wdir+new_dirs[0]+new_dirs[3])


'''
Order images based on the column value 'due'. Due column can have 
either small or a big value. We have also created two folder where
we store orderly images.
:param path: None
:type path: none
:returns: none
'''
def orderImages():

    col_names = ['STEP','LAPV','TENG','LAPM','prevF','nextF', 'MV_STEP', 'ratio','trend','IMG_PATH','due']

    album = pd.read_csv('~/Desktop/Autofocus/album/album.csv', header=0, names=col_names)

    # loop over every row and read IMG_PATH and due columns
    for row in album.itertuples():
        due = row.due
        mv_step = row.MV_STEP
        img_path = row.IMG_PATH[-18:]

        print("IMG_PATH: %s" % img_path)


        if mv_step == 0:
            shutil.copy(fAlbum + img_path, dFocus)

        elif mv_step != 0:
            if due == 'small':
                shutil.copy(fAlbum + img_path, dSmall)
            else:
                shutil.copy(fAlbum + img_path, dBig)
        else:
            print("Do nothing")



if __name__ == "__main__":

    createFolders()
    orderImages()
    