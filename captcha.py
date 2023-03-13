from PIL import Image
import numpy as np
import json
import amazoncaptcha
from io import BytesIO as IO

with open('C:/Users/omara/Desktop/VSCODE/DigitalSquad/riddles/captchav2-riddles/riddles.json') as f:
  arr = json.load(f)
    
data = arr[0]["question"]
img = Image.fromarray(np.uint8(data), mode='L')
img_byte_arr = IO()
img.save(img_byte_arr, format='PNG')
captcha = amazoncaptcha.AmazonCaptcha(img_byte_arr)
text = captcha.solve()


print(text)