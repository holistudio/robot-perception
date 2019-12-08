
#!/usr/bin/env python

'''
Stitching sample
================
https://github.com/opencv/opencv/blob/master/samples/python/stitching.py
================
Show how to use Stitcher API from python in a simple way to stitch panoramas
or scans.
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

    files = os.listdir('C:/Daniel/Documents/Grad School/NYU/robot-perception/Assignment_2/')
    # print(files);

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
