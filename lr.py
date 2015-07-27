#!/usr/bin/python

import argparse
import csv

from scipy import stats
import numpy as np


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Compute linear regression parameters for data in CSV file")
    parser.add_argument(
        'csv', help='CSV file with data, train data in first column')

    args = parser.parse_args()

    try:
        fh = open(args.csv, 'r')
    except IOError:
        parser.exit(1, "Can't open file\n")

    reader = csv.reader(fh)
    data = list(reader)
    # actually, it should be matrices
    train = np.array([float(line[0]) for line in data[1:]])
    features = np.array([[float(i) for i in line[1:]]
                        for line in data[1:]])

    # actually it returns coeffs, residuals, rank, singular_values
    coeff = np.linalg.lstsq(features, train)[0]

    prediction = np.dot(features, coeff)
    print "\nBuilding model on full set"
    print "Regression coefficients:\n", np.transpose(np.asmatrix(coeff))
    print "Correlation: ", np.corrcoef(prediction, train)[0][1]

    print "\n\nCross-validation"
    n = len(train)
    slices = 10
    slice_size = n/slices
    idx = np.random.permutation(n)
    for i in xrange(slices):
        lower_bound = i*slice_size
        upper_bound = (i+1)*slice_size
        validation_idx = idx[lower_bound:upper_bound]
        train_idx = np.concatenate((idx[0:lower_bound], idx[upper_bound:n]))

        validation_features = features[validation_idx]
        validation_values = train[validation_idx]
        train_features = features[train_idx]
        train_values = train[train_idx]

        validation_coeff = np.linalg.lstsq(train_features, train_values)
        validation_prediction = np.dot(validation_features, coeff)
        validation_corr = np.corrcoef(validation_prediction,
                                      validation_values)[0][1]

        print "Slice {i} correlation: {correlation}".format(
            i=i, correlation=validation_corr)
