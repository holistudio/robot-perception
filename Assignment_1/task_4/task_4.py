import numpy as np
from numpy import linalg as LA

from math import sqrt, floor, pow
import random

import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.lines import Line2D

import cv2
import pyAprilTag


def main():
    # Calibration Matrix from Task 3
    K=np.array([[1.17136545e+03, 0.00000000e+00, 8.01203424e+02],
    [0.00000000e+00, 1.17497866e+03, 5.38637778e+02],
    [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]], dtype='float64');
    print(f"\nK = \n{K}\n");

    # detect AprilTag pattern and homography matrix, Hs
    image_path = '../img/task_4/Task4_03.png';
    img = cv2.imread(image_path, 0);
    ids, corners, centers, Hs = pyAprilTag.find(img);

    H_matrix = np.array(Hs[0]);
    print(f"H = \n{H_matrix}");

    # store tag corner coordinates to show in resulting image later
    tag_corners = corners[0];
    print(f"\nCorner Image Coordinates = \n{tag_corners}\n");

    # Calculate camera extrinsics using homography and calibration matrix
    A_matrix = np.matmul(LA.inv(K), H_matrix);
    print(f"\nA = K^-1 * H = \n{A_matrix}\n");

    a1_n = LA.norm(A_matrix[:,0])

    r1 = A_matrix[:,0];
    r2 = A_matrix[:,1];
    r3 = np.cross(r1,r2);

    r1 = r1 / a1_n;
    r2 = r2 / a1_n;
    r3 = r3 / (a1_n * a1_n);

    tr = A_matrix[:,2];
    tr = tr / a1_n;

    print(f"\nTranslation = \n{tr}\n");

    R_matrix = np.array([r1,r2,r3]).transpose();

    print(f"\nR Matrix = \n{R_matrix}\n");

    P_matrix = np.array([r1, r2, r3, tr]).transpose();
    print(f"\nExtrinsics [ R | t ] = \n{P_matrix}\n");

    # Recalculate Camera Matrix P for converting 3D points to 2D image coordinates
    P_matrix = np.matmul(K,P_matrix);
    print(f"\nCamera Matrix K * [ R | t ] = \n{P_matrix}\n");

    # Cube corners world coordinates, sorted in a way that makes it easy for line drawing later
    world_coordinates = np.array([[1, 1, 0, 1],
    [-1, 1, 0, 1],
    [-1, -1, 0, 1], # since our cube "base" is from -1 to 1, its side length is 2
    [-1, -1, 2, 1], # so z-coordinates should be equal to 2 for it to be a cube!
    [-1, 1, 2, 1],
    [1, 1, 2, 1],
    [1, -1, 2, 1],
    [1, -1, 0, 1]]);
    print(f"\nWorld Coordinates = \n{world_coordinates}\n");

    # Convert to image coordinates uing Camera Matrix, P
    image_coordinates = np.matmul(P_matrix, world_coordinates.transpose()).transpose();

    # Homogenous form requires division by last vector value to complete the perspective projection
    for i in range(0,len(image_coordinates)):
        image_coordinates[i] = image_coordinates[i] / image_coordinates[i][2];
    print(f"\nImage Coordinates = \n{image_coordinates}\n");

    im = np.array(Image.open(image_path), dtype=np.uint8);
    fig,ax = plt.subplots(1);

    # Display the image
    ax.imshow(im);

    # Display AprilTag corners as detected by pyAprilTag
    ax.scatter(tag_corners[:,0], tag_corners[:,1], color='red');

    # Draw cube lines based on image coordinates of corners
    for i in range(0,4):
        for j in range(0,3):
            x = [];
            y = [];
            x.append(image_coordinates[i*2,0]);
            y.append(image_coordinates[i*2,1]);
            if j == 0:
                x.append(image_coordinates[i*2+1,0]);
                y.append(image_coordinates[i*2+1,1]);
            elif j == 1:
                if i*2+5 > len(image_coordinates):
                    x.append(image_coordinates[i*2-3,0]);
                    y.append(image_coordinates[i*2-3,1]);
                else:
                    x.append(image_coordinates[i*2+5,0]);
                    y.append(image_coordinates[i*2+5,1]);
            elif j == 2:
                if i*2+7 > len(image_coordinates):
                    x.append(image_coordinates[i*2-1,0]);
                    y.append(image_coordinates[i*2-1,1]);
                else:
                    x.append(image_coordinates[i*2+7,0]);
                    y.append(image_coordinates[i*2+7,1]);
            line = Line2D(x, y);
            ax.add_line(line);

    plt.show();



if __name__ == "__main__":
    main()
