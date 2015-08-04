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

    response = urllib.urlopen("http://stats.wikimedia.org/archive/squid_reports"
                              "/{year}-{month:0>2d}/SquidReportOperatingSystems"
                              ".htm".format(year=d.year, month=d.month))

    res = {}

    x = etree.HTML(response.read())
    rows = x.xpath('//h3[text()="In order of popularity"]/../../../tr')
    for row in rows[2:]:  # first row is table title, second is th
        tds = row.getchildren()
        if len(tds) != 3 or tds[0].tag != 'td' or tds[0].text == 'Total':
            continue
        share = float(tds[2].text.strip("%"))
        os = tds[0].text.replace(",", "_").replace(";", "_")
        if os not in res:
            res[os] = share

    return res


def header_name(service, column):
    return ": ".join((service.encode('utf-8'), column.encode('utf-8')))

if __name__ == '__main__':

    end_date = date.today() - timedelta(32)
    # end_date = date(2014, 10, 1)
    d = date(2009, 4, 1)
    res = []
    columns = set()

    while d < end_date:
        month = stats(d)
        columns = columns.union(month.keys())
        month['date'] = d.strftime("%Y-%m")
        res.append(month)
        d = start_of_month(d + timedelta(32))

    col_names = ['date'] + sorted(list(columns))
    writer = csv.DictWriter(sys.stdout, col_names)
    writer.writeheader()

    for month in res:
        writer.writerow(month)
