import numpy as np
from math import sqrt
import random
import open3d as o3d

class Point:
    def __init__(self, x, y, z):
        self.x = x;
        self.y = y;
        self.z = z;

class Plane:
    def __init__(self, x, y, z, nx, ny, nz):
        self.x = x;
        self.y = y;
        self.z = z;
        self.nx = nx;
        self.ny = ny;
        self.nz = nz;

def rand_unique_numbers(n, low, high):
    randoms = [];
    for i in range(0,n):
        unique = False;
        while(unique == False):
            unique = True;
            new_num = random.randint(low,high);
            for j in range(0,len(randoms)):
                if(randoms[j]==new_num):
                    unique = False;
        randoms.append(new_num);
    return randoms;

def main():
    # load point cloud data points
    pcd = o3d.io.read_point_cloud("data/record_00348.pcd");
    print(pcd); #27193
    points_array = np.asarray(pcd.points);
    o3d.visualization.draw_geometries([pcd])


    # set consensus score threshold to 80% of number of data points
    score_T = floor(0.8*len(points_array));
    # model score
    score_m = 0;

    # distance threshold for determining inliers/consensus points
    dist_t = 0.01;

    # initial sample size for building a model
    init_s = 3;

    # number of potential models
    N = 5;

    trial_models = []
    # for N trials
    for i in range(0,N):
        while(score_m < score_T):
            # randomly select init_s data points and build a plane as the model
            rand_p_ind = rand_unique_numbers(init_s,0,len(points_array));

            model_plane = Plane();

            consensus_set = [];
            for j in range(0,len(rand_p_ind)):
                consensus_set.append(points_array[rand_p_ind[j]]);

            # determine data points within distance threshold, t, of model
            for j in range(0,len(points_array)):
                if(rand_p_ind.count(j) == 0):
                    test_point = Point(points_array[j][0],points_array[j][1],points_array[j][2]);
                    # calculate orthogonal distance between point and plane
                    orth_dist;

                    if(orth_dist<dist_t):
                        consensus_set.append(test_point);

                # assign number of data points as consensus score of that model
                score_m = len(consensus_set);
                print(f"Trial: {i}, Score: {score_m}");
                # if model score is less than score threshold, T
                # repeat this process
        # build a new plane with the entire consensus set of data points/inliers
        model_plane = Plane();

        # store plane model and its consensus score
        trial_models.append([model_plane,score_m]);
        print(f"Trial: {i}, Final Score: {score_m}");

    # display plane with the highest consensus score
    max_ind = 0;
    max_score = 0;

    for i in range(0,len(trial_models)):
        if(trial_models[i][1]>max_score):
            max_ind = i;
            max_score = trial_models[i][1];
    best_plane = trial_models[max_ind][0];

if __name__ == "__main__":
    main()
