from super_image import EdsrModel, ImageLoader
from PIL import Image
import numpy as np

img = Image.open('./sketches/image.png').convert('RGB')
width, height = img.size
new_size = (width // 4, height // 4)
shrunk = img.resize(new_size)

lr_img = np.array(shrunk)

model = EdsrModel.from_pretrained('./results', scale=4)
inputs = ImageLoader.load_image(lr_img)
preds = model(inputs)

ImageLoader.save_image(preds, 'detailed map.png')
