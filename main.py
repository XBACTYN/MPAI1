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
fig, ax = plt.subplots(3, 2)
fig.tight_layout()
fig2, bx = plt.subplots(4, 2)
fig2.tight_layout()
fig3, cx = plt.subplots(3, 2)
fig3.tight_layout()
#img2 = img

ax[0, 0].imshow(img, cmap=plt.cm.gray, vmin=0, vmax=255)
ax[0, 0].set_title('Original')

bx[0, 0].imshow(img, cmap=plt.cm.gray, vmin=0, vmax=255)
bx[0, 0].set_title('Original')

cx[0, 0].imshow(img, cmap=plt.cm.gray, vmin=0, vmax=255)
cx[0, 0].set_title('Original')


def build_histogram(image, n, m, xx):
    #xx[n, m].hist(image.flatten(), bins=256, color='orange')
    hist, bins = np.histogram(image.flatten(), bins=256, range=[0, 256])
    xx[n,m].bar(bins[:-1], hist, color='gray')

    #maximum = max(image.ravel())
    #minimum = min(image.ravel())
    #print('max ', maximum)
    #print('min ', minimum)
    xx[n, m].set_title("Brightness")
    return hist


def contrast(image):
    fmax = max(image.ravel())
    fmin = min(image.ravel())
    print('max ', fmax)
    print('min ', fmin)
    a = 255 / (fmax - fmin)
    b = (-255 * fmin) / (fmax - fmin)

    res_img = np.vectorize(contr_pixel)
    img3 = res_img(image, a, b)

    #ax[0, 1].imshow(img3, cmap=plt.cm.gray, vmin=0, vmax=255)
    #ax[0, 1].set_title('Linear contrast')
    #imsave(json_data['result'], img3)
    return img3


def contr_pixel(image, a, b):
    image = a * image + b
    return image


def equalization(histo, image):
    temp = np.cumsum(histo)
    #bx[2, 1].imshow( temp,vmin=0, vmax=255)
    # width, height = image.size
    #F = temp / (512 * 512)
    F =  temp/temp[255]
    res_eq = np.vectorize(eq_pixel, excluded=[1])
    img_eq = res_eq(image, F)
    #bx[0, 1].set_title('Equalization')
    #bx[0, 1].imshow(img_eq, cmap=plt.cm.gray)
    print(img_eq)
    return img_eq


def eq_pixel(image, F):
    return 255 * F[image]


def thresholding(image):
    f0 = 100 #for zelda
    res_th = np.vectorize(threshold_pixel,excluded = [1])
    img_thr = res_th(image,f0)
    #cx[0, 1].set_title('Thresholding')
    #cx[0, 1].imshow(img_thr, cmap=plt.cm.gray)
    return img_thr

def threshold_pixel(image,f0):
    if(image <= f0):
        return 0
    else:
        return 255

def build_by_elem_diag(hist_orig, hist_eq):
    x = np.arange(0,256,1)
    diag = contrast(x)
    ax[2, 1].plot(x, diag/255, color='black', linestyle = '-', linewidth=1)
    ax[2,1].set_title('El-by-el conversion')
    diag21 = equalization(hist_orig,x)
    diag22 = equalization(hist_eq,x)
    bx[2, 0].plot(x, diag21/255, color='black', linestyle='-', linewidth=1)
    bx[2,0].set_title('El-by-el conversion original')
    bx[2, 1].plot(x, diag22/255, color='black', linestyle='-', linewidth=1)
    bx[2,1].set_title('El-by-el conversion')
    diag3 = thresholding(x)
    cx[2, 1].plot(x, diag3/255, color='black', linestyle='-', linewidth=1)
    cx[2,1].set_title('El-by-el conversion')

def build_integr(hist,image,i):
    x = np.arange(0, 256, 1)
    temp = np.cumsum(hist)
    bx[3,i].plot(x,temp, color='black', linestyle='-', linewidth=1)
    bx[3,i].set_title('Integral Lum Distr Function')

def all_show():
    plt.show()


def main():
    h12 = build_histogram(img, 1, 0, ax)
    contr_result = contrast(img)
    ax[0, 1].imshow(contr_result, cmap=plt.cm.gray, vmin=0, vmax=255)
    ax[0, 1].set_title('Linear contrast')
    #imsave(json_data['result'], contr_result)
    h14 = build_histogram(contr_result, 1, 1, ax)


    h22 = build_histogram(img, 1, 0, bx)
    eq_result = equalization(h22, img)
    bx[0, 1].set_title('Equalization')
    bx[0, 1].imshow(eq_result, cmap=plt.cm.gray)
    h24 = build_histogram(eq_result.astype(np.uint8), 1, 1, bx)
    build_integr(h22, img, 0)
    build_integr(h24, eq_result, 1)

    h32 = build_histogram(img, 1, 0, cx)
    th_result = thresholding(img)
    cx[0, 1].set_title('Thresholding')
    cx[0, 1].imshow(th_result, cmap=plt.cm.gray)
    h34 = build_histogram(th_result, 1, 1, cx)

    build_by_elem_diag(h22,h24)

    all_show()


if __name__ == '__main__':
    main()
