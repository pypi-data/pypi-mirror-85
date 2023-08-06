import pandas as pd
from datetime import datetime, date


def str_to_dt(mystring):
    """
    function to convert string into datetime
    Eg: 13/5/2020
    :param mystring: date in string format
    :return: date in datetime format
    """
    mylist = [int(x) for x in mystring.split('/')]
    return datetime(mylist[2], mylist[1], mylist[0])


def data_slicer(start, end, df):
    """
    slices the data to the required time periods
    :param start: start date
    :param end: end date
    :param df: dataframe
    :return: sliced dataframe
    """

    if type(start) == str:
        start = str_to_dt(start)
        end = str_to_dt(end)

    return df[(df['transaction_date'] <= end) & (df['transaction_date'] >= start)]
