#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree
import sys
import datetime
import collections
import csv
import urllib

months = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']


def monthly_stats():
    """ Get monthly browser market share from w3schools.com.

    Here is an example of page source fragment
    <table class="reference notranslate">
        <tr>
        <th>2015</th>
        <th class="right"><a href="browsers_chrome.asp">Chrome</a></th>
        <th class="right"><a href="browsers_explorer.asp">IE</a></th>
        <th class="right"><a href="browsers_firefox.asp">Firefox</a></th>
        <th class="right"><a href="browsers_safari.asp">Safari</a></th>
        <th class="right"><a href="browsers_opera.asp">Opera</a></th>
        </tr>
        <tr>
        <td>July</td>
        <td class="right">63.3 %</td>
        <td class="right">6.5 %</td>
        <td class="right">21.6 %</td>
        <td class="right">4.9 %</td>
        <td class="right">2.5 %</td>
        </tr>
    """
    results = collections.defaultdict(lambda: {})
    x = etree.HTML(urllib.urlopen(
        'http://www.w3schools.com/browsers/browsers_stats.asp').read())
    for table in x.xpath('//div[@class="table-responsive"]/table'):
        rows = table.xpath('tr')
        row = rows[0]
        etree.strip_tags(row, 'a')
        browsers = [th.text for th in row]
        year = int(browsers.pop(0))
        for row in rows[1:]:
            labels = [td.text for td in row]
            month = months.index(labels.pop(0))
            for i, label in enumerate(labels):
                browser = browsers[i]
                results[datetime.datetime(year, month, 1)][browser] = \
                    label.strip(" %").encode('utf-8')
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
