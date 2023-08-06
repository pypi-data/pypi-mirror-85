'''
file that provides information in the required format
Note: month to run this report is April
'''

import pandas as pd
from datetime import datetime, date
import calendar
import re

from vulcan_athena.mirandareporting.inventory_on_hand_engine import add_columns
from vulcan_athena.mirandareporting.setup import dataframe_tradebook, HIR


def financial_status(row):
    if row['Status'] == 'Prospective':
        return 'Non-Contracted - Prospective'
    elif row['Status'] == 'Future':
        return 'Contracted - Future'
    else:
        return 'Contracted - Delivered'


def business_line(row):
    if row['House']:
        if row['DealRef'].split('-')[0] == 'BH':
            return 'TEM Bluehalo'
        else:
            return 'TEM Corporate'

    else:
        if row['DealRef'].split('-')[0] == 'QF':
            return 'Qantas FCN'
        elif row['DealRef'].split('-')[0] != 'QF':
            return 'Qantas FP'
        else:
            return 'Issue 2'


def generalised_unit_name(mystring):
    gsc = re.findall('GSC', mystring)
    kaccu = re.findall('KACCU', mystring)
    gbr = re.findall('GBR', mystring)
    nkaccu = re.findall('NKACCU', mystring)
    regen = re.findall('Regen', mystring)
    vcs = re.findall('VCS', mystring)
    ind = re.findall('IND', mystring)
    wind = re.findall('Wind', mystring)
    nzu = re.findall('NZU', mystring)
    eua = re.findall('EUA', mystring)
    biomass = re.findall('Biomass', mystring)
    lgc = re.findall('LGC', mystring)
    alpha = re.findall('ALFA', mystring)

    if len(gsc):
        return 'GSC-XXX-GS Generalised'

    if mystring in HIR:  # TODO: Hotfix, edit later
        return 'KACCU-AUS-Generic HIR'

    if len(alpha):
        return 'KACCU-AUS-ALFA Generalised'

    if len(kaccu):
        if len(regen):
            return 'KACCU-AUS-Generic HIR'
        elif not (len(gbr)) and not (len(nkaccu)):
            return 'KACCU-Generic'

    if len(ind) and len(vcs):
        if len(wind):
            return 'VCS-IND-Wind Generalised'
        elif len(biomass):
            return 'VCS-IND-Generalised Biomass'

    if len(nzu):
        return 'NZU-NZL-Generalised'

    if len(eua):
        return 'EUA-EUR-Generic European Allowance'

    if len(lgc):
        return "LGC-AUS-Generic LGC's"

    return mystring


def inventory_hotfix(row):
    """
    NOTE: would not expect to have inventory on hand & outstanding sales in the same data line. It would be one or
    the other, or neither
    """
    if len(row['inventory_on_hand']):
        return []
    return row['outstanding_sales']


def shortfall_column(row, gen=False):

    if row['Direction'] == 'Buy':
        return 0

    if gen:
        shortfall = row['gen_outstanding_sales'][0] if len(row['gen_outstanding_sales']) else 0
        return min(abs(row['Volume']), shortfall)

    shortfall = row['outstanding_sales'][0] if len(row['outstanding_sales']) else 0
    return min(abs(row['Volume']), shortfall)


def eom(m, y):
    if m == 2:
        if y % 4 == 0 and not y % 400 == 0:
            return 29
        else:
            return 28
    elif m in [9, 4, 6, 11]:
        return 30
    else:
        return 31


def monthdelta(date, delta):
    m, y = (date.month + delta) % 12, date.year + (date.month + delta - 1) // 12
    if not m:
        m = 12
    d = eom(m, y)
    return date.replace(day=d, month=m, year=y)


def dataframe_generator(time_list, df):
    mydict = {}

    for date in time_list[1:]:
        month = calendar.month_name[date.month]
        mydict[month] = df[(df['ValueDate'] >= date.replace(day=1)) & (df['ValueDate'] <= date)]
    return mydict


def data_df(df, gen=False):
    '''
    function to add the business lines to the dataframe
    :return: master dataframe
    '''

    if not gen:
        stock_list = set(df['Name'])
    else:
        stock_list = set(df['Generalised_Name'])

    master_list = []

    for stock in stock_list:
        if not gen:
            group = add_columns(df[df['Name'] == stock].sort_values(['Unique_Id']))
        else:
            group = add_columns(df[df['Generalised_Name'] == stock].sort_values(['Unique_Id']))
        master_list.append(group)

    # adding the dataframes together
    stocks_df = master_list[0]

    for df in master_list[1:]:
        stocks_df = stocks_df.append(df)

    final_df = stocks_df

    return final_df


def diff_shortfall(row):
    if row['Name'] == row['Generalised_Name']:
        return row['Shortfall_Individual'] - row['Shortfall_Gen']
    else:
        return 0


def data_combined(prospective_flag=False):
    # reading in the data
    data = dataframe_tradebook
    data = data.fillna(0)  # TODO: data issue

    # Issue to only consider delivered and future values #TODO: add into the code later
    if prospective_flag:
        data = data[data['Status'] != 'Prospective']

    # df = data[data['Status'] == STATUS].sort_values(['ValueDate', 'Direction'])
    df = data.sort_values(['ValueDate', 'Direction'])
    df['Unique_Id'] = [x for x in range(len(df))]

    df['financial_status'] = df.apply(financial_status, axis=1)
    df['business_line'] = df.apply(business_line, axis=1)
    df['Generalised_Name'] = df['Name'].apply(generalised_unit_name)
    # df['ModifiedDate'] = df['ValueDate'].apply(lambda x: x.date())

    master_df = data_df(df)
    master_gen_df = data_df(df, gen=True)

    master_gen_df = master_gen_df.rename(
        columns={"inventory_on_hand": "gen_inventory_on_hand", "outstanding_sales": "gen_outstanding_sales"})

    final_df = pd.merge(master_df, master_gen_df[['Id', 'gen_inventory_on_hand', 'gen_outstanding_sales']],
                        left_on='Id',
                        right_on='Id', how='left')

    final_df['Shortfall_Individual'] = final_df.apply(lambda x: shortfall_column(x), axis=1)
    final_df['Shortfall_Gen'] = final_df.apply(lambda x: shortfall_column(x, True), axis=1)

    final_df['difference_bw_shortfalls'] = final_df.apply(lambda x: diff_shortfall(x), axis=1)

    return final_df


def create_time_list(today_date, sofy):
    time_list = [today_date]
    for i in range(12):
        time_list.append(monthdelta(sofy, i))

    return time_list


def data_dict(df):
    """
    function to slice the data
    :return: dictionary of the dataframes by months
    """

    # today_date = date.today
    today_date = date(2020, 6, 30)  # TODO: harcoded value

    if today_date.month <= 6:
        sofy_year = today_date.year - 1
    else:
        sofy_year = today_date.year

    sofy = date(sofy_year, 7, 1)
    time_list = create_time_list(today_date, sofy)
    future_time_list = create_time_list(today_date, date(sofy_year + 1, 7, 1))
    fy_time_list = create_time_list(today_date, date(sofy_year + 2, 7, 1))
    ff_yy_time_list = create_time_list(today_date, date(sofy_year + 3, 7, 1))

    d = dataframe_generator(time_list, df)
    d_future = dataframe_generator(future_time_list, df)
    d_fy = dataframe_generator(fy_time_list, df)
    d_ff_yy = dataframe_generator(ff_yy_time_list, df)

    return d, d_future, d_fy, d_ff_yy
