import numpy as np
import cv2 as cv
import matplotlib as mpl
from numpy import linalg as LA
from matplotlib import pyplot as plt
from PIL import Image


def main():
    img = cv.imread('for_watson.png',0);

    # display image in grayscale
    # cv.imshow('image',img);
    # cv.waitKey(0);
    # cv.destroyAllWindows();

    # seeing the image in grayscale, a very faint message appears!

    # convert pixels to array
    pixels = np.array(img);

    # plot pixels and record rows where message appears
    # plt.imshow(pixels, cmap='gray', vmin=0, vmax=255);
    # plt.show()

    # check rows 75, 240, and 390
    # print(pixels[75,:]); #background is 29, message is 30
    # print(pixels[240,:]); #background is 149, message is 150
    # print(pixels[390,:]); #background is 76, message is 77

    # change pixels to black and white based on color values from rows
    for i in range(0,len(pixels)):
        for j in range(0,len(pixels[i,:])):
            if (pixels[i,j] == 29 or pixels[i,j] == 149 or pixels[i,j] == 76):
                pixels[i,j]=0;
            if (pixels[i,j] == 30 or pixels[i,j] == 150 or pixels[i,j] == 77):
                pixels[i,j]=255;

    # plot new image
    plt.imshow(pixels, cmap='gray', vmin=0, vmax=255);
    plt.show();

if __name__ == "__main__":
    main()
