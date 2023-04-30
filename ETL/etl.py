import os
import petl
import sys
import pymssql
import configparser
import requests
import datetime
import json
import decimal


class MyException(Exception):
    """A custom exception class for raising custom errors"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def read_configuration(file_name):
    """reads configuration file

        return configuration tuple:
            (start_date, url, dest_server, dest_database)
    """
    config = configparser.ConfigParser()

    file_read = config.read(file_name)
    if len(file_read) == 0:
        raise MyException("Couldn't read file")

    # values from configuration file
    start_date = config['CONFIG']['startDate']
    url = config['CONFIG']['url']
    dest_server = config['CONFIG']['server']
    dest_db = config['CONFIG']['database']

    return start_date, url, dest_server, dest_db


def fetch_data(url, start_date):
    """Takes the url of the bank api and start date

      returns raw data from the api response as a dictionary/Json
    """
    try:
        boc_resp = requests.get(url+start_date)
    except Exception as e:
        raise MyException("Couldn't read data from url : ", e)

    if (boc_resp.status_code == 200):
        boc_raw = json.loads(boc_resp.text)

    return boc_raw


def process_data(raw_data):
    """
    recieves raw data dictionary
    return a list of lists containing
    rate_list and correspoding date list

    """
    rate = []
    date = []
    for row in raw_data['observations']:
        date.append(datetime.datetime.strptime(row['d'], '%Y-%m-%d'))
        rate.append(decimal.Decimal(row['FXUSDCAD']['v']))

    return [rate, date]


def main():
    start_date, url, dest_server, dest_db = read_configuration('project.ini')
    raw_data = fetch_data(url, start_date)
    rate_date = process_data(raw_data)


if __name__ == '__main__':
    main()
