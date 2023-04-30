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
        raise MyException(f"Couldn't read data from url : {e}")

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

    exchange_rate = petl.fromcolumns([date, rate], header=['date', 'rate'])

    return exchange_rate


def read_data_file(file_path):
    """read the Finances file in xlsx format
        return the petl table of dates and rates (USD)
    """
    try:
        expenses = petl.io.xlsx.fromxlsx(file_path)
    except Exception as e:
        raise (f"Couldn't open the file: {e}")

    return expenses


def populate_database(dest_server, db_name, data, table):
    try:
        db_connection = pymssql.connect(
            server=dest_server, database=db_name)
    except Exception as e:
        raise MyException(f"Couldn't make connection with database {e}")

    try:
        petl.io.todb(data, db_connection, table)
    except Exception as e:
        raise MyException(f"Couldn't populate datbase {e}")


def main():
    start_date, url, dest_server, dest_db = read_configuration('project.ini')
    raw_data = fetch_data(url, start_date)
    exhchange_rate = process_data(raw_data)
    expenses = read_data_file('data/Expenses.xlsx')

    # join the tables
    expenses = petl.outerjoin(exhchange_rate, expenses, key='date')

    # fill the missing values in null column
    expenses = petl.filldown(expenses, 'rate')

    # drop dates with no expenses
    expenses = petl.select(expenses, lambda rec: rec.USD != None)

    # add Canadian dollar exchange column
    expenses = petl.addfield(
        expenses, 'CAD', lambda rec: decimal.Decimal(rec.USD) * rec.rate)

    populate_database(dest_server, dest_db, expenses, 'expenses')


if __name__ == '__main__':
    main()
