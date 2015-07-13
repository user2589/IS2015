#!/usr/bin/python

import argparse
import csv

from scipy import stats
import numpy as np



if __name__ =='__main__':
    parser = argparse.ArgumentParser(description="Compute linear regression parameters for data in CSV file")
    parser.add_argument('csv', help='CSV file with data, train data in first column')


    args = parser.parse_args()

    try:
        fh = open(args.csv, 'r')
    except IOError:
        parser.exit(1, "Can't open file\n")

    reader = csv.reader(fh)
    data = list(reader)
    train = np.array([float(line[0]) for line in  data[1:]])
    features = np.array([map(float, line[1:]) for line in  data[1:]])

    # actually it returns coeffs, residuals, rank, singular_values
    coeff = np.linalg.lstsq(features, train)[0]
    print coeff
