import numpy as np
from math import sqrt

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def main():
    # array of vanishing point coordinates
    v = [Point(1911.622,-2888.174), Point(6577.018,3963.804), Point(-1821.64,4067.708)];

    # center point coordinates
    c = Point(1965.774,1488.922);

    # based on derivations for focal length:
    f1 = sqrt(-(v[0].x-c.x)*(v[1].x-c.x)-(v[0].y-c.y)*(v[1].y-c.y));
    print(f"Focal Length, f= {f1} (points 1 and 2)");

    # use the other two pairs of vanishing points to calculate focal length
    f2 = sqrt(-(v[1].x-c.x)*(v[2].x-c.x)-(v[1].y-c.y)*(v[2].y-c.y));
    f3 = sqrt(-(v[0].x-c.x)*(v[2].x-c.x)-(v[0].y-c.y)*(v[2].y-c.y));

    # as expected the three pairs yield the same value
    print(f"Focal Length, f= {f2} (points 2 and 3)");
    print(f"Focal Length, f= {f3} (points 1 and 3)");

    #final calibration method.
    K = np.matrix([[f1, 0, c.x],[0, f1, c.y],[0, 0, 1]]);

    print(f"\nCalibration Matrix:\n{K}")


if __name__ == "__main__":
    main()
