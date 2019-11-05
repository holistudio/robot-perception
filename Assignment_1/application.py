import numpy as np
from numpy import linalg as LA

from math import sqrt, floor, pow
import random

import matplotlib.pyplot as plt
from PIL import Image

import cv2
import pyAprilTag

# Calibration Matrix from Task 3
# AprilCalib log 2
# CalibRig::mode=2d
# @ Sun Nov  3 21:18:57 2019

def main():
    K=np.array([[3.14072514e+03, 0.00000000e+00, 2.01964606e+03],
     [0.00000000e+00, 3.14336567e+03, 1.48452385e+03],
     [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]]);

    print(f"\nK = \n{K}\n");

    image_path = 'img/task_4/Task4_02.png';
    img = cv2.imread(image_path, 0);
    ids, corners, centers, Hs = pyAprilTag.find(img);

    H_matrix = np.array(Hs[0]);
    print(f"H = \n{H_matrix}");

    tag_corners = corners[0];
    print(f"\nCorner Image Coordinates = \n{tag_corners}\n");

    # corner_0 = tag_corners[0];
    # corner_0 = np.append(corner_0,1);
    # corner_0_w = np.matmul(LA.inv(H_matrix),np.array(corner_0))
    # print(corner_0_w/corner_0_w[2])
    A_matrix = np.matmul(LA.inv(K), H_matrix);

    a1_n = LA.norm(A_matrix[:,0])

    r1 = A_matrix[:,0];
    r1 = r1 / a1_n;

    r2 = A_matrix[:,1];
    r2 = r2 / a1_n;

    r3 = np.cross(r1,r2);
    r3 = r3 / (a1_n * a1_n);

    tr = A_matrix[:,2];
    tr = tr / a1_n;
    print(f"\nTranslation = \n{tr}\n");

    R_matrix = np.array([r1,r2,r3]).transpose();

    print(f"\nR Matrix = \n{R_matrix}\n");

    P_matrix = np.array([r1, r2, r3, tr]).transpose();
    print(f"\nExtrinsics [ R | t ] = \n{P_matrix}\n");

    P_matrix = np.matmul(K,P_matrix);

    print(f"\nCamera Matrix K * [ R | t ] = \n{P_matrix}\n");

    world_coordinates = np.array([[1, 1, 0, 1],
    [-1, 1, 0, 1],
    [-1, -1, 0, 1],
    [1, -1, 0, 1]]);
    print(f"\nWorld Coordinates = \n{world_coordinates}\n");


    # xyz = np.matmul(P_matrix, world_coordinates.transpose());
    #
    # xy_p = np.array([xyz[0], xyz[1]]) / xyz[2];
    #
    # r_sq = xy_p[0]*xy_p[0] + xy_p[1]*xy_p[1];
    #
    # xy_pp = xy_p * (1+distCoeffs[0]*pow(r_sq,2)+distCoeffs[1]*pow(r_sq,4)+distCoeffs[2]*pow(r_sq,6))/(1+distCoeffs[3]*pow(r_sq,2))
    #
    # xy_pp = np.append(xy_pp,1);
    #
    # image_coordinates = np.array([np.matmul(K,xy_pp)]);

    image_coordinates = np.matmul(P_matrix, world_coordinates.transpose()).transpose();

    for i in range(0,len(image_coordinates)):
        image_coordinates[i] = image_coordinates[i] / image_coordinates[i][2];
    print(f"\nImage Coordinates = \n{image_coordinates}\n");

    im = np.array(Image.open(image_path), dtype=np.uint8);
    fig,ax = plt.subplots(1);

    # Display the image
    ax.imshow(im);

    ax.scatter(tag_corners[:,0], tag_corners[:,1], color='red');
    ax.scatter(image_coordinates[:,0], image_coordinates[:,1], color='green');
    plt.show();



if __name__ == "__main__":
    main()
