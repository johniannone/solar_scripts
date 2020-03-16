#!/usr/bin/env python3

"""
A simple script to download a site's solar power generation from SolarEdge and
print a table. This may be saved to a file via the shell.

API documentation:
https://www.solaredge.com/sites/default/files/se_monitoring_api.pdf

"""

import requests
import json
import os
import sys
from datetime import date, timedelta


def load_config(file_name):
    """ read the .json config file and return a dictionary of values """
    cfg = {}
    with open(os.path.join(sys.path[0], file_name)) as config:
        cfg = json.load(config)

    cfg['address'] = \
        f"https://monitoringapi.solaredge.com/site/{cfg['site_id']}/energy"

    return cfg


def daysback(d):
    """ get today minus a timedelta of days, returned as iso format date """
    return (date.today() + timedelta(days=d)).strftime("%Y-%m-%d")


def print_v(v):
    """ make Watt hour values ready for printing """
    if v is not None:
        # convert to int to drop the decimal values
        return str(int(v))
    else:
        return "No data"


def print_d(d):
    """ make date values ready for printing """
    if d is not None:
        # take only the first 10 digits to retain the date portion
        return (d[:10])
    else:
        return "No data"


def output_table(dict):
    """ print the key/value pairs of the dictionary passed in """
    s = '\n   Date    |   Wh\n'
    s += ('-----------|------\n')
    for d in dict:
        s += (print_d(d['date']) + ' | ' + print_v(d['value']) + '\n')
    return s


def handle_request(r):
    """ call output_table for a successful request, else return the code """
    if r.status_code == 200:
        return output_table(r.json()['energy']['values'])
    else:
        return 'Response status: ' + r.status_code


def build_request():
    """ use the config dictionary to form and return the API request """
    cfg = load_config('solar_config.json')
    params={
        "api_key"  : cfg['api_key'],
        "startDate": daysback(int(cfg['start'])),
        "endDate"  : daysback(int(cfg['end'])),
        "timeUnit" : cfg['unit']
    }
    return requests.get(cfg['address'], params)


print(handle_request(build_request()))
