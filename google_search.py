#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import csv
import urllib
from datetime import datetime, timedelta
import sys
import argparse
import time

def end_of_month(first_day):
    nm = first_day + timedelta(days=32)
    return datetime(nm.year, nm.month, 1) - timedelta(days=1)

def start_of_month(some_date):
    return datetime(some_date.year, some_date.month, 1)


class GCS(object):
    """ object to represent Google Custom Search API requester """
    base_url = "https://www.googleapis.com/customsearch/v1?"

    def __init__(self, query, key, cse_id):
        self.params = {
            'key': key,
            'cx' : cse_id,
            'q'  : query,
        }
        self.today = datetime.today()

    def search(self, date):
        """ return number of search results for query given in the params"""
        td = self.today - date

        params = self.params
        params['dateRestrict'] = "d%s"%td.days

        url = self.base_url + urllib.urlencode(params)
        #sys.stderr.write(url + "\n")

        response = urllib.urlopen(url)
        response_text = response.read()
        response_obj = json.loads(response_text)

        try:
            count = int(response_obj['searchInformation']['totalResults'])
        except KeyError, ValueError:
            sys.stderr.write("response: %s"%response_text)
            raise

        return count


if __name__ =='__main__':

    parser = argparse.ArgumentParser(description="Download Google Search stats")
    parser.add_argument('query', help='Search query')
    parser.add_argument('-s', '--start-date', help='start date, inclusive, YYYY-MM', default='2009-04')
    parser.add_argument('-e', '--end-date', help='end date, exclusive, YYYY-MM', default='2015-04')

    args = parser.parse_args()

    try:
        start_date = datetime.strptime(args.start_date, "%Y-%m")
        end_date = datetime.strptime(args.end_date, "%Y-%m")
    except ValueError:
        parser.exit(1, "Invalid date\n")

    today = datetime.today()

    writer = csv.DictWriter(sys.stdout, ['date', 'search results'])
    writer.writeheader()

    gcs = GCS(args.query,
            "your API key",
            "your CSE id")

    # because there is a huge variance in data, get first measurement 10 times
    # it will be averaged later to serve as a base for diff for everything else.
    # Resulting CSV will be taken at least 5 times for each query to average later
    date = start_of_month(end_date)
    for i in range(10):
        count = gcs.search(date)
        writer.writerow({'date': date.strftime("%Y-%m"), 'search results': count})

    while True:
        date = start_of_month(date - timedelta(28))

        try:
            count = gcs.search(date)
        except KeyError:
            parser.exit(2, 'Unexpected result, probably out of daily quota')
        except ValueError:
            parser.exit(2, 'Unexpected value in number of search results')


        writer.writerow({'date': date.strftime("%Y-%m"), 'search results': count})

        if date < start_date:
            break
