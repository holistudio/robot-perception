import numpy as np
from numpy import linalg as LA
import os


def main():
    currentDir=os.getcwd();
    print(f"Current Directory: {currentDir}");
    m = np.matrix('1 2 3; 4 5 6; 7 8 9');
    print(f"Matrix {m}");


if __name__ == "__main__":
    main()
