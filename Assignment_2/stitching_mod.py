
#!/usr/bin/env python

'''
Code based on opencv's stitching sample code
================
https://github.com/opencv/opencv/blob/master/samples/python/stitching.py
================

Please have all images in jpg format and in the same directory as the python file.
'''

# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
import cv2 as cv
import os
import argparse
import sys

modes = (cv.Stitcher_PANORAMA, cv.Stitcher_SCANS)

parser = argparse.ArgumentParser(prog='stitching.py', description='Stitching sample.')
parser.add_argument('--mode',
    type = int, choices = modes, default = cv.Stitcher_PANORAMA,
    help = 'Determines configuration of stitcher. The default is `PANORAMA` (%d), '
         'mode suitable for creating photo panoramas. Option `SCANS` (%d) is suitable '
         'for stitching materials under affine transformation, such as scans.' % modes)
parser.add_argument('--output', default = 'result.jpg',
    help = 'Resulting image. The default is `result.jpg`.')
# parser.add_argument('img', nargs='+', help = 'input images')

__doc__ += '\n' + parser.format_help()

def main():
    args = parser.parse_args()

    # get current working directory
    cwd = os.getcwd();
    files = os.listdir(cwd);
    # print(files);

    # finds all jpg files
    img_files = [];
    for file in files:
        if file.find('.jpg') != -1:
            img_files.append(file);
    print(img_files);

    # read input images
    imgs = [];
    for img_name in img_files:
        img = cv.imread(img_name);
        # print(img)
        imgs.append(img);
    imgs = np.array(imgs);

    stitcher = cv.createStitcher(args.mode)
    status, pano = stitcher.stitch(imgs)

    # when all 41 images are used, the following error occurs:
    # Can't stitch images, error code = 3
    # This corresponds to ERR_CAMERA_PARAMS_ADJUST_FAIL

    # when images 37-41 are only included for stitching, the following error occurs:
    # cv2.error: OpenCV(3.4.2) C:\Miniconda3\conda-bld\opencv-suite_1534379934306\work\modules\imgproc\src\imgwarp.cpp:1728: error: (-215:Assertion failed) dst.cols < 32767 && dst.rows < 32767 && src.cols < 32767 && src.rows < 32767 in function 'cv::remap'

    if status != cv.Stitcher_OK:
        print("Can't stitch images, error code = %d" % status)
        sys.exit(-1)

    cv.imwrite(args.output, pano)
    print("stitching completed successfully. %s saved!" % args.output)

    print('Done')


if __name__ == '__main__':
    print(__doc__)
    main()
    cv.destroyAllWindows()
