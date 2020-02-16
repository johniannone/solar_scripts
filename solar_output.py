#!/usr/bin/env python3

"""
A simple script to download a site's solar power generation from SolarEdge and
print a table. This may be saved to a file via the shell.

API documentation:
https://www.solaredge.com/sites/default/files/se_monitoring_api.pdf

"""

import requests
import json
from datetime import date, timedelta


def load_config(file_name):
    cfg = {}
    with open(file_name) as config:
        cfg = json.load(config)

    cfg['address'] = \
        f"https://monitoringapi.solaredge.com/site/{cfg['site_id']}/energy"

    return cfg


def daysback(d):
    """ get today minus a timedelta of days, returned as iso """
    return (date.today() + timedelta(days=d)).strftime("%Y-%m-%d")


def print_v(v):
    """ convert to int then string to drop the decimal values """
    if v is not None:
        return str(int(v))
    else:
        return "No data"


def print_d(d):
    """ take the first 10 digits to drop the time values """
    if d is not None:
        return (d[:10])
    else:
        return "No data"


def output_table(dict):
    """ use key/value pairs in dictionary to print a table """
    s = '\n   Date    |   Wh\n'
    s += ('-----------|------\n')
    for d in dict:
        s += (print_d(d['date']) + ' | ' + print_v(d['value']) + '\n')
    return s


def handle_request(r):
    if r.status_code == 200:
        return output_table(r.json()['energy']['values'])
    else:
        return 'Response status: ' + r.status_code


def build_request():
    cfg = load_config('solar_config.json')
    params={
        "api_key"  : cfg['api_key'],
        "startDate": daysback(int(cfg['start'])),
        "endDate"  : daysback(int(cfg['end'])),
        "timeUnit" : cfg['unit']
    }
    return requests.get(cfg['address'], params)


print(handle_request(build_request()))
