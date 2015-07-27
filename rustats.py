#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree
import csv
import urllib
from datetime import date, timedelta
import sys


def start_of_month(some_date):
    return date(some_date.year, some_date.month, 1)


def stats(d):
    """ Retrieve stats for particular month from alexvaleev.ru """

    response = urllib.urlopen("http://alexvaleev.ru/browserstat/{year}/{month}/"
                              "".format(year=d.year, month=d.month))

    res = {}

    x = etree.HTML(response.read())
    d = x.xpath('body/div[@class="container"]/div')[1]
    for service_div in d.xpath('div'):
        service_name = service_div.xpath('h2/text()')[0]
        rows = service_div.xpath('table/tbody/tr')
        cells = [row.xpath('td/text()') for row in rows]
        res[service_name] = [(key, value)
                             for key, value in cells if float(value) > 0.5]

    return res


def header_name(service, column):
    return ": ".join((service.encode('utf-8'), column.encode('utf-8')))

if __name__ == '__main__':

    end_date = date.today() - timedelta(32)
    # end_date = date(2011, 5, 1)
    d = date(2009, 1, 1)
    res = []
    columns = set()

    while d < end_date:
        month = {}
        for service, data in stats(d).items():
            for browser, share in data:
                col_name = header_name(service, browser)
                columns.add(col_name)
                month[col_name] = share
        month['date'] = d.strftime("%Y-%m")
        res.append(month)
        d = start_of_month(d + timedelta(32))

    col_names = ['date'] + sorted(list(columns))
    writer = csv.DictWriter(sys.stdout, col_names)
    writer.writeheader()

    for month in res:
        writer.writerow(month)
