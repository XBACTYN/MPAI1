import json

import numpy as np
from matplotlib import pyplot as plt
from skimage.exposure import histogram
from skimage.io import imread, imsave
from skimage.io import imshow

settings = {
    'source': 'C:/Users/dream/OneDrive/Рабочий стол/MPAI1/mandrill.tif',
    'result': 'C:/Users/dream/OneDrive/Рабочий стол/MPAI1/monster1.tif'
}

with open('settings.json', 'w') as fp:
    json.dump(settings, fp)
with open('settings.json') as json_file:
    json_data = json.load(json_file)

path = json_data['source']
img = imread(path)
print('Image shape: ', img.shape)
fig,ax = plt.subplots(2, 2)
img2 = img

ax[0, 0].imshow(img, cmap = plt.cm.gray,vmin=0, vmax=255)

def build_histogram(image,n,m):
    ax[n,m].hist(image.ravel(), bins=256, color='orange', )
    #ax[0].hist(image[:, :, 0].ravel(), bins=256, color='red', alpha=0.5)
    #ax[0].hist(image[:, :, 1].ravel(), bins=256, color='Green', alpha=0.5)
    #ax[0].hist(image[:, :, 2].ravel(), bins=256, color='Blue', alpha=0.5)
    #ax[0].legend(['Total', 'Red_Channel', 'Green_Channel', 'Blue_Channel'])
    maximum = max(image.ravel())
    minimum = min(image.ravel())
    print('max ', maximum)
    print('min ', minimum)
    ax[n,m].set_title("Brightness")
    #plt.show()
    return maximum, minimum

def contrast(fmax,fmin):
    a = 255/(fmax - fmin)
    b = (-255*fmin)/(fmax-fmin)

    res_img = np.vectorize(contr_pixel)
    img3 = res_img(img2,a,b)

    ax[0,1].imshow(img3, cmap = plt.cm.gray,vmin=0, vmax=255)
    imsave(json_data['result'], img3)
    maximum = max(img3.ravel())
    minimum = min(img3.ravel())
    print('new max ', maximum)
    print('new min ', minimum)
    return img3

def contr_pixel(image, a, b):
    image = a*image+b
    return image

def main():
    fmax, fmin = build_histogram(img, 1, 0)
    result = contrast(fmax, fmin)
    fmax, fmin = build_histogram(result, 1, 1)
    plt.show()

if __name__ == '__main__':
    main()

