import numpy as np
import cv2 as cv
from numpy import linalg as LA
import os


def main():
    currentDir=os.getcwd();
    print(f"Current Directory: {currentDir}");

    img = cv.imread('data/for_watson.png',0);

    # display image in grayscale
    cv.imshow('image',img);
    cv.waitKey(0);
    cv.destroyAllWindows();

    # m = np.matrix('1 2 3; 4 5 6; 7 8 9');
    # print(f"Matrix {m}");


if __name__ == "__main__":
    main()
