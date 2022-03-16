import json

import numpy as np
import skimage
from matplotlib import pyplot as plt
from skimage.exposure import histogram
from skimage.io import imread, imsave
from skimage.io import imshow

settings = {
    'source': 'C:/Users/dream/OneDrive/Рабочий стол/MPAI1/zelda.tif',
    'result': 'C:/Users/dream/OneDrive/Рабочий стол/MPAI1/monster1.tif'
}

with open('settings.json', 'w') as fp:
    json.dump(settings, fp)
with open('settings.json') as json_file:
    json_data = json.load(json_file)

path = json_data['source']
img = imread(path)
print('Image shape: ', img.shape)
fig, ax = plt.subplots(2, 2)
fig2, bx = plt.subplots(2, 2)
img2 = img

ax[0, 0].imshow(img, cmap=plt.cm.gray, vmin=0, vmax=255)
ax[0, 0].set_title('Original')

bx[0, 0].imshow(img, cmap=plt.cm.gray, vmin=0, vmax=255)


def build_histogram(image, n, m, xx):
    #xx[n, m].hist(image.flatten(), bins=256, color='orange')
    hist, bins = np.histogram(image.flatten(), bins=256, range=[0, 256])
    xx[n,m].bar(bins[:-1], hist, color='gray')

    maximum = max(image.ravel())
    minimum = min(image.ravel())
    print('max ', maximum)
    print('min ', minimum)
    xx[n, m].set_title("Brightness")
    #return maximum, minimum, xx[n, m].hist(image.flatten(), bins=256, color='orange')
    return maximum, minimum, hist


def contrast(fmax, fmin):
    a = 255 / (fmax - fmin)
    b = (-255 * fmin) / (fmax - fmin)

    res_img = np.vectorize(contr_pixel)
    img3 = res_img(img2, a, b)

    ax[0, 1].imshow(img3, cmap=plt.cm.gray, vmin=0, vmax=255)
    ax[0, 1].set_title('Linear contrast')
    imsave(json_data['result'], img3)
    maximum = max(img3.ravel())
    minimum = min(img3.ravel())
    print('new max ', maximum)
    print('new min ', minimum)
    return img3


def contr_pixel(image, a, b):
    image = a * image + b
    return image


def equalization(histo, image):
    temp = np.cumsum(histo)
    # width, height = image.size
    F = temp / (512 * 512)
    res_eq = np.vectorize(eq_pixel, excluded=[1])
    img_eq = res_eq(image, F)
    bx[0, 1].imshow(img_eq, cmap=plt.cm.gray)
    print(img_eq)
    return img_eq


def eq_pixel(image, F):
    return 255 * F[image]


def all_show():
    plt.show()


def main():
    fmax, fmin, h12 = build_histogram(img, 1, 0, ax)
    contr_result = contrast(fmax, fmin)
    fmax, fmin, h14 = build_histogram(contr_result, 1, 1, ax)
    fmax, fmin, h22 = build_histogram(img, 1, 0, bx)
    eq_result = equalization(h22, img)
    fmax, fmin, h24 = build_histogram(eq_result.astype(np.uint8), 1, 1, bx)
    all_show()


if __name__ == '__main__':
    main()
