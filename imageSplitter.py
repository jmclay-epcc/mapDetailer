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
    
    sp("./textures/image.png", chunker, chunker*2, False, False, False, './tempDump/hr') # THis image i twice the resolution as the sketch, so while we're only reducing the sketch by a factor of two when we chop it up into bits, these bits will be 4 times smaller than the texture bits.  Moral of the story is we're using this data to train a model to scale up an image by a factor of 4.  
    sp("./sketches/image.png", chunker, chunker*2, False, False, False, './tempDump/lr')

    for filename in os.listdir('tempDump/lr'):
        if filename in trainList:
            os.rename(f"./tempDump/lr/{filename}", f"./data/train/lr/{filename}")
        else:
            os.rename(f"./tempDump/lr/{filename}", f"./data/val/lr/{filename}")
            
    for filename in os.listdir('tempDump/hr'):
        img = Image.open(f"./tempDump/hr/{filename}")
        width, height = img.size
        new_size = (width * 2, height * 2)
        shrunk = img.resize(new_size)
        shrunk.save(f"./tempDump/hr/{filename}")
        if filename in trainList:
            os.rename(f"./tempDump/hr/{filename}", f"./data/train/hr/{filename}")
        else:
            os.rename(f"./tempDump/hr/{filename}", f"./data/val/hr/{filename}")
                
    os.rmdir("./tempDump/lr")
    os.rmdir("./tempDump/hr")
    os.rmdir("./tempDump")
    
dataSetCreator()