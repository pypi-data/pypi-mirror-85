import calendar
from datetime import date
import time

import pandas as pd

from vulcan_athena.mirandareporting.data_wrangler import data_dict, data_combined
from vulcan_athena.mirandareporting.fifo_business_logic import calculate_stock_info, calculate_sales, opening_inv_gen, \
    calculate_opening_inventory_actual
from vulcan_athena.mirandareporting.generic_units_logic import wacgu, get_last_buy_price
from vulcan_athena.mirandareporting.reporting_framework import dashboard_files_new, inv_dashboard_files
from vulcan_athena.mirandareporting.setup import STATUS, BUSINESS_LINE, GEN_LIST, FY_YEAR, FY_MAPPER, dataframe_ssp


# from vulcan_athena.mirandareporting.ssp_logic import ssp_df_creator


def processor(d_df, df_master, ssp_df, wacgu_dict, fy_year, month_dict):
    months = d_df.keys()

    # dictionary to store the numbers
    value_dict = {}

    # dictionary to get inventory data
    inventory_dict = {}

    # dictionary to store info in regards to deal reference
    deal_ref_dict = {}

    # get today date
    today_date = date.today()
    report_year = today_date.year
    report_month = today_date.month

    # get the stocks for which the information needs to be calculated
    stock_names = set(df_master['Name'])

    for month in months:
        # subset the data
        data = d_df[month].copy()
        data['FormattedDate'] = data['ValueDate'].copy()

        month_num = time.strptime(month, "%B").tm_mon
        year_num = fy_year - 1 if month_num > 6 else fy_year
        last_day = calendar.monthrange(year_num, month_num)[-1]

        start_date = min(data.sort_values(by='ValueDate')['ValueDate']) if len(data) else pd.Timestamp(
            date(year_num, month_num, 1))
        end_date = max(data.sort_values(by='ValueDate')['ValueDate']) if len(data) else pd.Timestamp(
            date(year_num, month_num,
                 last_day))

        submaster_dict = {}

        for stat in STATUS:
            df = data[data['Status'] == stat]

            # variables to hold the stock information
            stock_list = []

            for stock in stock_names:
                stock_dict = {'Name': stock}
                stock_data = df[df['Name'] == stock]

                stock_dict.update(calculate_stock_info(stock_data))
                stock_list.append(stock_dict)

            submaster_dict[stat] = pd.DataFrame(stock_list)

            for business in BUSINESS_LINE:
                df_business_line = df[df['business_line'] == business]

                # variables to hold the stock information
                stock_list_business = []

                for stock in stock_names:
                    stock_dict_business = {'Name': stock}
                    stock_data_business = df_business_line[df_business_line['Name'] == stock]
                    # getting the information for opening inventory
                    stock_dict_business.update(calculate_sales(stock_data_business))
                    stock_list_business.append(stock_dict_business)

                submaster_dict[stat + ' ' + business] = pd.DataFrame(stock_list_business)

        value_dict[month] = submaster_dict

        # Logic to calculate inventory and shortfall

        if FY_MAPPER[month] <= 6:
            ssp_year = fy_year - 1
        else:
            ssp_year = fy_year

        # variables to hold the stock information
        stock_list = []

        for stock in stock_names:
            stock_dict = {'Name': stock}
            stock_data = data[data['Name'] == stock]

            previous_data = df_master[
                (df_master['ValueDate'] < start_date) & (
                        df_master['Name'] == stock)] if start_date else pd.DataFrame()

            period_data = df_master[
                (df_master['ValueDate'] <= end_date) & (
                        df_master['Name'] == stock)] if start_date else pd.DataFrame()

            # logic for shortfalls in previous period
            shortfall_flag = True
            if ssp_year < report_year:
                shortfall_flag = False
            elif (ssp_year == report_year) and (month_dict[month] < report_month):
                shortfall_flag = False

            stock_dict.update(
                calculate_opening_inventory_actual(previous_data, period_data, stock_data, ssp_df, stock, ssp_year,
                                                   wacgu_dict, month, shortfall_flag))

            stock_list.append(stock_dict)

        inventory_dict[month] = pd.DataFrame(stock_list)

        # Logic to save info by Counterpart
        # get the deal refs
        deal_refs = set(df_master['Counterpart'])

        sub_deal_dict = {}

        for stat in STATUS:
            df = data[data['Status'] == stat]

            # variables to hold the stock information
            stock_list = []

            for deal in deal_refs:
                stock_dict = {'DealRef': deal}
                stock_data = df[df['Counterpart'] == deal]

                stock_dict.update(calculate_stock_info(stock_data))
                stock_list.append(stock_dict)

            sub_deal_dict[stat] = pd.DataFrame(stock_list)

            for business in BUSINESS_LINE:
                df_business_line = df[df['business_line'] == business]

                # variables to hold the stock information
                stock_list_business = []

                for deal in deal_refs:
                    stock_dict_business = {'DealRef': deal}
                    stock_data_business = df_business_line[df_business_line['Counterpart'] == deal]
                    # getting the information for opening inventory
                    stock_dict_business.update(calculate_sales(stock_data_business))
                    stock_list_business.append(stock_dict_business)

                sub_deal_dict[stat + ' ' + business] = pd.DataFrame(stock_list_business)

        deal_ref_dict[month] = sub_deal_dict

    return value_dict, inventory_dict, deal_ref_dict


def fixing_generalised_logic(d_df, master_df, ssp_df):
    today_date = date.today()
    months = calendar.month_name[today_date.month - 1]
    # master dictionary to store all the values
    gen_dict = {}

    start_date = min(d_df[months].sort_values(by='ValueDate')['ValueDate'])

    for gen in GEN_LIST:

        # df = data[data['Generalised_Name'] == gen]
        df = master_df[master_df['Generalised_Name'] == gen]

        # get the stocks for which the information needs to be calculated
        stock_names = set(df['Name'])

        # variables to hold the stock information
        stock_list = []

        # getting the information for opening inventory
        for stock in stock_names:
            stock_dict = {'Name': stock}
            stock_data = df[df['Name'] == stock]

            previous_data = master_df[
                (master_df['Status'] == 'Delivered') & (master_df['ValueDate'] < start_date) & (
                        master_df['Name'] == stock)]

            stock_dict.update(opening_inv_gen(previous_data) if len(previous_data) else {'Volume': 0, 'Price': 0})
            stock_list.append(stock_dict)

        gen_dict[gen] = pd.DataFrame(stock_list)

    return gen_dict


# dictionary to store the latest ssp values
ssp_df = dataframe_ssp
ssp_df = ssp_df.fillna(0)

# getting the master list
master_df = data_combined()

# getting the monthly sliced dictionaries
dict_df, dict_df_future, dict_fy_2022, dict_fy_2023 = data_dict(master_df)

gen_dict = fixing_generalised_logic(dict_df, master_df, ssp_df)
wacgu_dict = wacgu(gen_dict)
last_buy_price = get_last_buy_price(master_df)

# logic for drawdown
# master_df = drawdown(master_df, wacgu_dict)

# get month dictionary
month_dict = {}
for i in range(1, 13):
    month_dict[calendar.month_name[i]] = i

# Contracted Inventory information

inv_master_df = data_combined(True)
inv_dict_df, inv_dict_df_future, inv_dict_fy_2022, inv_dict_fy_2023 = data_dict(inv_master_df)

inv_gen_dict = fixing_generalised_logic(inv_dict_df, inv_master_df, ssp_df)
inv_wacgu_dict = wacgu(inv_gen_dict)
inv_last_buy_price = get_last_buy_price(inv_master_df)


# main wrapper function

def main_execute():
    print('Package run 35 executing...')

    # collect the base tables
    base_table_2020, base_table_2020_Inv, base_table_2020_Deal = processor(dict_df, master_df, ssp_df, wacgu_dict,
                                                                           FY_YEAR[0], month_dict)
    base_table_2021, base_table_2021_Inv, base_table_2021_Deal = processor(dict_df_future, master_df, ssp_df,
                                                                           wacgu_dict,
                                                                           FY_YEAR[1], month_dict)
    base_table_2022, base_table_2022_Inv, base_table_2022_Deal = processor(dict_fy_2022, master_df, ssp_df, wacgu_dict,
                                                                           FY_YEAR[2], month_dict)
    base_table_2023, base_table_2023_Inv, base_table_2023_Deal = processor(dict_fy_2023, master_df, ssp_df, wacgu_dict,
                                                                           FY_YEAR[3], month_dict)

    # Contracted Inventory information
    inv_base_table_2020, inv_base_table_2020_Inv, inv_base_table_2020_Deal = processor(inv_dict_df, inv_master_df,
                                                                                       ssp_df, inv_wacgu_dict,
                                                                                       FY_YEAR[0], month_dict)
    inv_base_table_2021, inv_base_table_2021_Inv, inv_base_table_2021_Deal = processor(inv_dict_df_future,
                                                                                       inv_master_df, ssp_df,
                                                                                       inv_wacgu_dict,
                                                                                       FY_YEAR[1], month_dict)
    inv_base_table_2022, inv_base_table_2022_Inv, inv_base_table_2022_Deal = processor(inv_dict_fy_2022, inv_master_df,
                                                                                       ssp_df, inv_wacgu_dict,
                                                                                       FY_YEAR[2], month_dict)
    inv_base_table_2023, inv_base_table_2023_Inv, inv_base_table_2023_Deal = processor(inv_dict_fy_2023, inv_master_df,
                                                                                       ssp_df, inv_wacgu_dict,
                                                                                       FY_YEAR[3], month_dict)

    # Generate base tables

    dashboard_files_new(base_table_2020, base_table_2020_Inv, base_table_2020_Deal, dict_df, FY_YEAR[0])
    dashboard_files_new(base_table_2021, base_table_2021_Inv, base_table_2021_Deal, dict_df_future, FY_YEAR[1])
    dashboard_files_new(base_table_2022, base_table_2022_Inv, base_table_2022_Deal, dict_fy_2022, FY_YEAR[2])
    dashboard_files_new(base_table_2023, base_table_2023_Inv, base_table_2023_Deal, dict_fy_2023, FY_YEAR[3])

    # contracted inv base tables
    print('Running Contracted Inventory code')

    inv_dashboard_files(inv_base_table_2020_Inv, FY_YEAR[0])
    inv_dashboard_files(inv_base_table_2021_Inv, FY_YEAR[1])
    inv_dashboard_files(inv_base_table_2022_Inv, FY_YEAR[2])
    inv_dashboard_files(inv_base_table_2023_Inv, FY_YEAR[3])

    return base_table_2020
