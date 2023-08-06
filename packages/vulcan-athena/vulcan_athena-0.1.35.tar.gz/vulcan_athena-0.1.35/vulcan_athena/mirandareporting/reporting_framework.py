import pandas as pd
import numpy as np
import os, uuid
from vulcan_athena.mirandareporting.setup import CONNECTION_STRING, STORAGEACCOUNTNAME, STORAGEACCOUNTKEY
from azure.storage.blob import BlockBlobService

CAL_MAPPER = {'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12,
              'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6}


def blob_writer(myobj, mystring):
    WRITE_CONTAINERNAME = "tem-financialreporting-base-tables"
    BLOBNAME = mystring

    df_csv = myobj.to_csv(encoding="utf-8")

    blobService = BlockBlobService(account_name=STORAGEACCOUNTNAME, account_key=STORAGEACCOUNTKEY)

    blobService.create_blob_from_text(WRITE_CONTAINERNAME, BLOBNAME, df_csv)


def base_table(data, year, month, status=''):
    df = data.copy()

    if 'Name' not in df.columns:
        df = df.rename({'DealRef': 'Name'}, axis=1)
    df = df.set_index('Name')
    df = df.loc[~(df == 0).all(axis=1)]
    df = df.reset_index()

    df['Year'] = df['Name'].apply(lambda x: year)
    df['Month'] = df['Name'].apply(lambda x: month)
    df['Month Num'] = df['Name'].apply(lambda x: CAL_MAPPER[month])

    if len(status):
        df['Status'] = df['Name'].apply(lambda x: status)

    return df


def base_table_bus_lines(data, year, month, status=''):
    df = data.copy()

    if 'Name' not in df.columns:
        df = df.rename({'DealRef': 'Name'}, axis=1)
    df = df.set_index('Name')
    df = df.loc[~(df == 0).all(axis=1)]
    df = df.reset_index()

    df['Year'] = df['Name'].apply(lambda x: year)
    df['Month'] = df['Name'].apply(lambda x: month)
    df['Month Num'] = df['Name'].apply(lambda x: CAL_MAPPER[month])
    if len(status):
        df['Status'] = df['Name'].apply(lambda x: status.split()[0])
        df['Business Line'] = df['Name'].apply(lambda x: status.split()[1] + ' ' + status.split()[2])

    return df


def dashboard_files_new(master_dict, inventory_dict, deal_dict, dict_df, year):
    qantas_fp_list = ['Delivered Qantas FP', 'Future Qantas FP', 'Prospective Qantas FP']

    # Sales information
    df_list = []

    for month in master_dict.keys():
        for status in master_dict[month].keys():
            if status in ['Delivered', 'Future', 'Prospective']:
                df_list.append(base_table(master_dict[month][status].fillna(0), year, month, status))

    sales_df = pd.concat(df_list)
    # sales_df.to_csv(f'base_agg_tables_tem/{year}_' + 'Sales_Summary' + '.csv')
    blob_writer(sales_df, str(year) + 'Sales_Summary' + '.csv')

    print(f'{year} Sales Summary file written successfully ')

    # Business Line Information
    df_list = []

    for month in master_dict.keys():
        for status in master_dict[month].keys():
            if status not in ['Delivered', 'Future', 'Prospective']:
                # if status not in qantas_fp_list:
                df_list.append(base_table_bus_lines(master_dict[month][status].fillna(0), year, month, status))

    # Qantas FP Sales Margin
    for month in master_dict.keys():
        master_df = dict_df[month]
        for status in qantas_fp_list:
            margin_df = master_df[
                (master_df['business_line'] == 'Qantas FP') & (master_df['Status'] == status.split()[0])]

            commission = (pd.pivot_table(margin_df[margin_df['Direction'] == 'Sell'], values='TEM_Margin',
                                         index=['DealRef'], aggfunc=np.max)).reset_index()

            if len(commission):
                commission.columns = ['Name', 'Sale Margin']
                commission['Sales'] = commission['Name'].apply(lambda x: 0)

                df_list.append(base_table_bus_lines(commission, year, month, status))

    sales_df = pd.concat(df_list, sort=False)
    # sales_df.to_csv(f'base_agg_tables_tem/{year}_' + 'Sales' + '.csv')
    blob_writer(sales_df, str(year) + 'Sales' + '.csv')

    print(f'{year} Sales file written successfully ')

    # Inventory Information
    df_list = []

    for month in inventory_dict.keys():
        df_list.append(base_table(inventory_dict[month].fillna(0), year, month))

    sales_df = pd.concat(df_list, sort=False)
    # sales_df.to_csv(f'base_agg_tables_tem/{year}_' + 'Inventory' + '.csv')
    blob_writer(sales_df, str(year) + 'Inventory' + '.csv')

    print(f'{year} Inventory file written successfully ')

    # Deal Ref information
    df_list = []

    for month in deal_dict.keys():
        for status in deal_dict[month].keys():
            if status in ['Delivered', 'Future', 'Prospective']:
                df_list.append(base_table(deal_dict[month][status].fillna(0), year, month, status))

    sales_df = pd.concat(df_list)
    # sales_df.to_csv(f'base_agg_tables_tem/{year}_' + 'DealRef_Summary' + '.csv')
    blob_writer(sales_df, str(year) + 'DealRef_Summary' + '.csv')

    print(f'{year} DealRef Summary file written successfully ')

    # Deal Ref Business Line Information
    df_list = []

    for month in deal_dict.keys():
        for status in deal_dict[month].keys():
            if status not in ['Delivered', 'Future', 'Prospective']:
                # if status not in qantas_fp_list:
                df_list.append(base_table_bus_lines(deal_dict[month][status].fillna(0), year, month, status))

    # Qantas FP Sales Margin
    for month in deal_dict.keys():
        master_df = dict_df[month]
        for status in qantas_fp_list:
            margin_df = master_df[
                (master_df['business_line'] == 'Qantas FP') & (master_df['Status'] == status.split()[0])]

            commission = (pd.pivot_table(margin_df[margin_df['Direction'] == 'Sell'], values='TEM_Margin',
                                         index=['DealRef'], aggfunc=np.max)).reset_index()

            if len(commission):
                commission.columns = ['Name', 'Sale Margin']
                commission['Sales'] = commission['Name'].apply(lambda x: 0)

                df_list.append(base_table_bus_lines(commission, year, month, status))

    sales_df = pd.concat(df_list, sort=False)
    # sales_df.to_csv(f'base_agg_tables_tem/{year}_' + 'DealRef_Sales_Summary' + '.csv')
    blob_writer(sales_df, str(year) + 'DealRef_Sales_Summary' + '.csv')

    print(f'{year} DealRef Sales Summary file written successfully ')

    # Corporate and FP Sales Margin
    df_list = []

    for month in deal_dict.keys():
        master_df = dict_df[month]
        for status in ['Delivered Qantas FP', 'Future Qantas FP', 'Prospective Qantas FP', 'Delivered TEM Corporate',
                       'Future TEM Corporate', 'Prospective TEM Corporate']:

            if status in ['Delivered Qantas FP', 'Future Qantas FP', 'Prospective Qantas FP']:
                b_line = 'Qantas FP'
            else:
                b_line = 'TEM Corporate'

            margin_df = master_df[
                (master_df['business_line'] == b_line) & (master_df['Status'] == status.split()[0])]

            if len(margin_df):
                if 'TEM_Margin' in margin_df.keys():
                    commission = (pd.pivot_table(margin_df[margin_df['Direction'] == 'Sell'], values='TEM_Margin',
                                                 index=['DealRef'], aggfunc=np.max)).reset_index()

                    if len(commission):
                        commission.columns = ['Name', 'Sale Margin']
                        commission['Sales'] = commission['Name'].apply(lambda x: 0)

                        df_list.append(base_table_bus_lines(commission, year, month, status))

    sales_df = pd.concat(df_list, sort=False)
    # sales_df.to_csv(f'base_agg_tables_tem/{year}_' + 'Replicated_Sales_Summary' + '.csv')
    blob_writer(sales_df, str(year) + 'Replicated__Sales_Summary' + '.csv')

    print(f'{year} Replicated Sales Summary file written successfully ')


def inv_dashboard_files(inventory_dict, year):
    # Inventory Information
    df_list = []

    for month in inventory_dict.keys():
        df_list.append(base_table(inventory_dict[month].fillna(0), year, month))

    sales_df = pd.concat(df_list, sort=False)
    # sales_df.to_csv(f'base_agg_tables_tem/{year}_' + 'Inventory' + '.csv')
    blob_writer(sales_df, str(year) + 'Contracted_Inventory' + '.csv')

    print(f'{year} Contracted Inventory file written successfully ')
