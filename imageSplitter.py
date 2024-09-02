from split_image import split_image as sp
from pathlib import Path
import random
import os
from PIL import Image
import numpy as np

def dataSetCreator():
    chunker = 24
    imageList = []
    totImgNo = chunker * chunker * 2

    for i in range(totImgNo):
        imageList.append(f"image_{i}.png")
        
    random.shuffle(imageList)
    trainList = imageList[:int(totImgNo * 0.75)] # I didn't hardcode this because i learned my lesson!  This caused me great strife before!  

    directory = Path("data/train/lr")
    directory.mkdir(parents=True, exist_ok=True)
    directory = Path("data/train/hr")
    directory.mkdir(parents=True, exist_ok=True)
    directory = Path("data/val/lr")
    directory.mkdir(parents=True, exist_ok=True)
    directory = Path("data/val/hr")
    directory.mkdir(parents=True, exist_ok=True)

    directory = Path("tempDump/lr")
    directory.mkdir(parents=True, exist_ok=True)
    directory = Path("tempDump/hr")
    directory.mkdir(parents=True, exist_ok=True)
    
    sp("./textures/image.png", chunker, chunker*2, False, False, False, './tempDump/hr') 
    sp("./sketches/image.png", chunker, chunker*2, False, False, False, './tempDump/lr')

    for filename in os.listdir('tempDump/lr'):
        img = Image.open(f"./tempDump/lr/{filename}")
        width, height = img.size
        new_size = (width // 2, height // 2)
        shrunk = img.resize(new_size)
        shrunk.save(f"./tempDump/lr/{filename}")
        if filename in trainList:
            os.rename(f"./tempDump/lr/{filename}", f"./data/train/lr/{filename}")
        else:
            os.rename(f"./tempDump/lr/{filename}", f"./data/val/lr/{filename}")
            
    for filename in os.listdir('tempDump/hr'):
        if filename in trainList:
            os.rename(f"./tempDump/hr/{filename}", f"./data/train/hr/{filename}")
        else:
            os.rename(f"./tempDump/hr/{filename}", f"./data/val/hr/{filename}")
                
    os.rmdir("./tempDump/lr")
    os.rmdir("./tempDump/hr")
    os.rmdir("./tempDump")
    
dataSetCreator()