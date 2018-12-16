import numpy as np
from PIL import Image

image = Image.open('test_image.png').convert('L')
print(image)
image_input = np.array(image)

image_input = np.full(image_input.shape, 255) - image_input
image_input[image_input > 0 ] = 255
print('image_input', image_input)

image_new = Image.open('test_new.png')
print('image_new', image_new)

image2 = image_input - image_new
print('image2: ', image2.max(), image2.min())

# image = Image.open('model/samples/tooth.png')
# print(image)
# image_array = np.array(image)
# print(image_array)


