#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree
import csv
import urllib
from datetime import datetime, timedelta
import sys
import argparse

def start_of_month(some_date):
    return datetime(some_date.year, some_date.month, 1)


class YandexSearcher(object):
    """ object to represent Yandex XML API requester """
    base_url = "https://yandex.com/search/xml?"

    def __init__(self, query, user, key, filtering, **kwargs):
        self.query = query
        self.params = {
            'user': user,
            'key': key,
            'l10n':'en',  # make sure it corresponds to the type of search in Yandex.XML settings
            'filter': filtering,
        }

    def search(self, date):
        """ return number of search results for query given in the params"""

        params = self.params
        params['query'] = 'date:{datefilt} "{query}"'.format(
            datefilt=date.strftime("%Y%m*"), query=self.query)

        url = self.base_url + urllib.urlencode(params)

        response = urllib.urlopen(url)
        response_text = response.read()
        response_xml = etree.fromstring(response_text)

        return response_xml.xpath('/yandexsearch/response/found[@priority="strict"]/text()')[0].strip()


if __name__ =='__main__':

    parser = argparse.ArgumentParser(description="Download Google Search stats")
    parser.add_argument('query', help='Search query')
    parser.add_argument('-s', '--start-date', help='start date, inclusive, YYYY-MM', default='2005-01')
    parser.add_argument('-e', '--end-date', help='end date, exclusive, YYYY-MM', default='2015-06')

    args = parser.parse_args()

    try:
        start_date = datetime.strptime(args.start_date, "%Y-%m")
        end_date = datetime.strptime(args.end_date, "%Y-%m")
    except ValueError:
        parser.exit(1, "Invalid date\n")

    today = datetime.today()

    writer = csv.DictWriter(sys.stdout, ['date', 'search results'])
    writer.writeheader()

    ys = YandexSearcher(
            args.query,
            "<your yandex username>",
            "your key after registration at https://xml.yandex.ru/",
            filtering="none"
        )

    date = start_date

    while date < end_date:
        count = ys.search(date)
        writer.writerow({'date': date.strftime("%Y-%m"), 'search results': count})
        date = start_of_month(date + timedelta(32))
