#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import datetime
import collections
import csv
import urllib


def monthly_stats():
    """ Get monthly browser market share from w3counter.com.

    We are looking for javascript lines like this:
        safari.push(['5/07', 2.4]);
    First parameter is data y/m, second is share in procents
    """
    results = collections.defaultdict(lambda: {})
    pattern = re.compile("\s*(\w*)\.push\(\s*\[(.*?)\]\s*\);.*")
    response = urllib.urlopen('http://www.w3counter.com/trends')
    for line in response:
        match = pattern.match(line)
        if match:
            browser, param_string = match.groups()
            params = [param.strip() for param in param_string.split(",")]
            month = datetime.datetime.strptime(
                params.pop(0).strip("'\""), "%m/%y")
            results[month][browser] = params[0]
    return results


def get_browsers(dataset):
    """ Get set of browsers out of dataset returned by monthly_stats """
    browsers = set()
    [browsers.update(dataset[month].keys()) for month in dataset.keys()]
    return browsers

if __name__ == '__main__':
    data = monthly_stats()
    browsers = get_browsers(data)

    writer = csv.DictWriter(sys.stdout, ['date']+sorted(browsers))
    writer.writeheader()

    for month in sorted(data.keys()):
        row = data[month]
        row['date'] = month.strftime("%m/%d/%Y")
        writer.writerow(row)
