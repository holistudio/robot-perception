# Based on the demo_calib_by_photo.py provided in pyAprilTag
# https://github.com/ai4ce/pyAprilTag/tree/master/python/pyAprilTag

import os
import sys
import pyAprilTag

# get current working directory
CUR_DIR = os.getcwd()

#establish a log folder in working directory
LOG_DIR = os.path.join(CUR_DIR,'calib_log')
sys.path.insert(0, CUR_DIR) #otherwise importlib cannot find the path
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
    print(f"Calibration Pattern Path: {pyAprilTag.calib_pattern_path}")

    # PNG images of the calibration pattern should be placed in the same working directory
    pyAprilTag.calib(pyAprilTag.calib_pattern_path,
                   'photo://{}'.format(os.path.join(CUR_DIR, '*.png')),
                   log_dir=LOG_DIR, nDistCoeffs=4)

import importlib
logs = sorted([f for f in os.listdir(LOG_DIR) if f.endswith('.py')])
if len(logs) == 0:
    print('no calibration log available!')
    exit(-1)

last_log = os.path.relpath(os.path.join(LOG_DIR, logs[-1])).replace(os.path.sep,'.')[:-3]
calib = importlib.import_module(last_log)
print('last log: '+last_log)

# Print calibration intrinsics
print('camera intrinsic matrix:')
print(calib.K)
print('camera distortion parameters:')
print(calib.distCoeffs)
