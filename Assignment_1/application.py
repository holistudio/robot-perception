import numpy as np
from math import sqrt
import open3d as o3d

class Point:
    def __init__(self, x, y, z):
        self.x = x;
        self.y = y;
        self.z = z;

def main():
    # load point cloud data points
    pcd = o3d.io.read_point_cloud("data/record_00348.pcd");
    print(pcd);
    print(np.asarray(pcd.points))
    o3d.visualization.draw_geometries([pcd])


    # set consensus score threshold to 80% of number of data points
    # for N trials
        # randomly select s data points and build a plane as the model
        # determine data points within distance threshold, t, of model
        # assign number of data points as consensus score of that model
        # if model score is less than score threshold, T
            # repeat this process
        # else
            # build a new plane with the entire consensus set of data points/inliers
        # store plane model and its consensus score
    # at the end of trials
    # display plane with the highest consensus score

if __name__ == "__main__":
    main()
