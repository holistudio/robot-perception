import numpy as np
from numpy import linalg as LA
from math import sqrt, floor
import random
import open3d as o3d
import pptk

class Vector:
    def __init__(self, x, y, z):
        self.x = x;
        self.y = y;
        self.z = z;

class Plane:
    def __init__(self, point, n):
        self.point = point;
        self.n = n;

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

def fit_points_to_plane(points):
    # given array of points (as Vector objects), find plane that best fits those points

    num_points = len(points);
    print(f"Consensus set size: {num_points}");
    centroid = Vector(0,0,0);
    for p in points:
        centroid.x += p[0];
        centroid.y += p[1];
        centroid.z += p[2];
    centroid = Vector(centroid.x/num_points,centroid.y/num_points,centroid.z/num_points);
    centroid_arr = np.array([centroid.x,centroid.y,centroid.z])

    covariance_m = [[0,0,0]];
    for p in points:
        r = p - centroid_arr;
        covariance_m = np.append(covariance_m,[r],axis=0);
    covariance_m = np.delete(covariance_m, 0, 0);
    covariance_m = covariance_m.transpose();
    # print(f"Covariance Matrix:\n{covariance_m}\n");

    u, s, vh = np.linalg.svd(covariance_m, full_matrices=True);

    # print(f"Singular Values:\n{s}\n");
    # print(f"U:\n{u}\n");
    dir = [u.item((0,2)), u.item((1,2)), u.item((2,2))];
    print(f"Plane Normal Vector:\n{dir}\n");
    # code based on https://www.ilikebigbits.com/2015_03_04_plane_from_points.html
    # and https://www.ilikebigbits.com/2017_09_25_plane_from_points_2.html
    # xx = 0.0;
    # xy = 0.0;
    # xz = 0.0;
    # yy = 0.0;
    # yz = 0.0;
    # zz = 0.0;
    # for p in points:
    #     r = [p.x - centroid.x, p.y - centroid.y, p.z - centroid.z];
    #     xx += r[0] * r[0];
    #     xy += r[0] * r[1];
    #     xz += r[0] * r[2];
    #     yy += r[1] * r[1];
    #     yz += r[1] * r[2];
    #     zz += r[2] * r[2];
    #
    # det_x = yy*zz - yz*yz;
    # det_y = xx*zz - xz*xz;
    # det_z = xx*yy - xy*xy;
    dir = Vector(dir[0],dir[1],dir[2]);
    return Plane(centroid, dir);


def main():
    # load point cloud data points
    pcd = o3d.io.read_point_cloud("data/record_00348.pcd");
    print(pcd); #271983
    points_array = np.asarray(pcd.points);
    # o3d.visualization.draw_geometries([pcd])


    # set consensus score threshold to 80% of number of data points
    score_T = floor(0.80*len(points_array));
    print(f"Threshold Score: {score_T}")
    # model score
    score_m = 0;

    # distance threshold for determining inliers/consensus points
    dist_t = 0.01;

    # initial sample size for building a model
    init_s = 5;

    # number of potential models
    N = 3;

    trial_sets = []
    # for N trials
    for i in range(0,N):
        while(score_m < score_T):
            # randomly select init_s data points and build a plane as the model
            rand_p_ind = rand_unique_numbers(init_s,0,len(points_array));
            consensus_set = [];
            for j in rand_p_ind:
                consensus_set.append(points_array[j]);

            model_plane = fit_points_to_plane(consensus_set);

            # determine data points within distance threshold, t, of model
            for j in range(0,len(points_array)):
                if(rand_p_ind.count(j) == 0):
                    test_point = np.array([points_array[j][0],points_array[j][1],points_array[j][2]]);

                    # calculate orthogonal distance between point and plane
                    plane_p = np.array([model_plane.point.x, model_plane.point.y, model_plane.point.z]);
                    normal = np.array([model_plane.n.x, model_plane.n.y, model_plane.n.z]);
                    orth_dist = np.dot((test_point - plane_p),normal);
                    # print(f"Distance: {orth_dist}");

                    if(abs(orth_dist)<dist_t):
                        consensus_set.append(test_point);

                # assign number of data points as consensus score of that model
                score_m = len(consensus_set);
            print(f"Trial: {i}, Score: {score_m}");
            print(f"Trial Done?: {score_m >= score_T}\n");
            print(f"---\n");
            # if model score is less than score threshold, T
            # repeat this process

        # store plane model and its consensus score
        trial_sets.append([consensus_set,score_m]);
        print(f"Trial: {i}, Final Score: {score_m}\n");
        print(f"---\n");
        score_m=0;

    # display plane with the highest consensus score
    max_ind = 0;
    max_score = 0;

    for i in range(0,len(trial_sets)):
        if(trial_sets[i][1]>max_score):
            max_ind = i;
            max_score = trial_sets[i][1];
    best_set = trial_sets[max_ind][0];
    pptk.viewer(best_set);
    # build a new plane with the entire consensus set of data points/inliers
    model_plane = fit_points_to_plane(best_set);

if __name__ == "__main__":
    main()
