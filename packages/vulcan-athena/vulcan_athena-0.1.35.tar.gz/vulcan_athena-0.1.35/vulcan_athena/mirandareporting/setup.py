'''
This file is for setting up the global variables used throughout the project
Customized folder paths and details to be initialized here
'''
import pyodbc
from azure.storage.blob import BlockBlobService

import pandas as pd

# Azure credentials
CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=sttemfinancialreporting;AccountKey=ow3mO+jsdSuM7REmLnSupIOyz0mPfwayuy1lt+5UMNykhNgWKfshr6SMV9ttyVxIP9kApKwW716xRaH3GGh8Og=="
STORAGEACCOUNTNAME = "sttemfinancialreporting"
STORAGEACCOUNTKEY = "ow3mO+jsdSuM7REmLnSupIOyz0mPfwayuy1lt+5UMNykhNgWKfshr6SMV9ttyVxIP9kApKwW716xRaH3GGh8Og=="


def blob_reader(BLOBNAME, LOCALFILENAME, text_reader=False):
    READ_CONTAINERNAME = "tem-db-tables"

    # download from blob
    blob_service = BlockBlobService(account_name=STORAGEACCOUNTNAME, account_key=STORAGEACCOUNTKEY)

    if text_reader:
        blob = blob_service.get_blob_to_text(READ_CONTAINERNAME, BLOBNAME)
        dataframe_blobdata = blob.content
    else:
        blob_service.get_blob_to_path(READ_CONTAINERNAME, BLOBNAME, LOCALFILENAME)
        dataframe_blobdata = pd.read_csv(LOCALFILENAME)

    return dataframe_blobdata


def read_sql(sql_conn):
    conn = pyodbc.connect(sql_conn)
    sql_query = pd.read_sql_query("SELECT * from Tradebook", conn)

    df = pd.DataFrame(sql_query, columns=['Id', 'TradeDate', 'Direction', 'TradeType', 'Status',
                                          'Name', 'Shares', 'Volume', 'SSP', 'Actual_Sale_Px', 'Instrument',
                                          'Country', 'ValueDate', 'CacheDate', 'Face_SSP', 'Face_Sales',
                                          'Counterpart', 'TEM_Margin', 'QF_Margin', 'Trader', 'Ref', 'DealRef',
                                          'House', 'RetirementType', 'QF_PO_Reference', 'QF_PO_IssuanceDate',
                                          'QF_InvoiceNumber', 'QF_InvoiceIssuanceDate', 'QF_InvoiceDueDate',
                                          'QF_InvoicePaymentDate', 'TEM_InvoiceNumber', 'TEM_InvoicePaymentDate',
                                          'RetirementReferenceNumber', 'RetirementDate', 'POS',
                                          'TEM_InvoiceIssuanceDate',
                                          'TEM_InvoiceDueDate'])

    return df


dataframe_ssp = blob_reader('ssp_table.csv', 'ssp_table.csv')

sql_connection = blob_reader('sql_connection.txt', ' ', True)
print(f'Read from text file successful. \n{str(sql_connection)}')
dataframe_tradebook = read_sql(str(sql_connection))
print(f'Read from DB successful.')

# dataframe_tradebook = blob_reader('tradebook.csv', 'tradebook.csv')
#
# dataframe_tradebook['Id'] = dataframe_tradebook['Id'].astype('int')
# dataframe_tradebook['TradeDate'] = pd.to_datetime(dataframe_tradebook['TradeDate'])
# dataframe_tradebook['Shares'] = pd.to_numeric(dataframe_tradebook["Shares"])
# dataframe_tradebook['Volume'] = pd.to_numeric(dataframe_tradebook["Volume"])
# dataframe_tradebook['SSP'] = pd.to_numeric(dataframe_tradebook["SSP"])
# dataframe_tradebook['Actual_Sale_Px'] = pd.to_numeric(dataframe_tradebook["Actual_Sale_Px"])
# dataframe_tradebook['ValueDate'] = pd.to_datetime(dataframe_tradebook['ValueDate'])
# dataframe_tradebook['Face_SSP'] = pd.to_numeric(dataframe_tradebook["Face_SSP"])
# dataframe_tradebook['Face_Sales'] = pd.to_numeric(dataframe_tradebook["Face_Sales"])
# dataframe_tradebook['TEM_Margin'] = pd.to_numeric(dataframe_tradebook["TEM_Margin"])
# dataframe_tradebook['QF_Margin'] = pd.to_numeric(dataframe_tradebook["QF_Margin"])
# dataframe_tradebook['House'] = dataframe_tradebook['House'].astype('bool')
# dataframe_tradebook['POS'] = pd.to_numeric(dataframe_tradebook["POS"])


dataframe_ssp['2019'] = pd.to_numeric(dataframe_ssp["2019"])
dataframe_ssp['2020'] = pd.to_numeric(dataframe_ssp["2020"])
dataframe_ssp['2021'] = pd.to_numeric(dataframe_ssp["2021"])
dataframe_ssp['2022'] = pd.to_numeric(dataframe_ssp["2022"])
dataframe_ssp['2023'] = pd.to_numeric(dataframe_ssp["2023"])

dataframe_ssp.set_index("Row Labels", inplace=True)

# for the spp_logic file
filepath = ''
sheetname = ''

STATUS = ['Delivered', 'Future', 'Prospective']
BUSINESS_LINE = ['TEM Corporate', 'TEM Bluehalo', 'Qantas FP', 'Qantas FCN']

TEST_MODE = False

EXCEL_FILENAME = "MVP template - June 2020.xlsx"
EXCEL_PATH = "reports/bridge/"

# column mapping
COL_DICT = {'July': 'C', 'August': 'D', 'September': 'E', 'October': 'F', 'November': 'G', 'December': 'H',
            'January': 'I',
            'February': 'J', 'March': 'K', 'April': 'L', 'May': 'M', 'June': 'N'}
COL_DICT_FUTURE = {'July': 'S', 'August': 'T', 'September': 'U', 'October': 'V', 'November': 'W', 'December': 'X',
                   'January': 'Y',
                   'February': 'Z', 'March': 'AA', 'April': 'AB', 'May': 'AC', 'June': 'AD'}

SALES_LIST = ['Delivered TEM Corporate', 'Delivered TEM Bluehalo', 'Delivered Qantas FP', 'Delivered Qantas FCN',
              'Future TEM Corporate', 'Future TEM Bluehalo', 'Future Qantas FP', 'Future Qantas FCN',
              'Prospective TEM Corporate', 'Prospective TEM Bluehalo', 'Prospective Qantas FP',
              'Prospective Qantas FCN']

GEN_LIST = ['GSC-XXX-GS Generalised', 'KACCU-AUS-Generic HIR', 'KACCU-Generic', 'VCS-IND-Wind Generalised',
            'VCS-IND-Generalised Biomass', 'KACCU-AUS-ALFA Generalised',
            'NZU-NZL-Generalised', 'EUA-EUR-Generic European Allowance', "LGC-AUS-Generic LGC's"]

FY_YEAR = [2020, 2021, 2022, 2023]
FY_MAPPER = {'July': 1, 'August': 2, 'September': 3, 'October': 4, 'November': 5, 'December': 6,
             'January': 7, 'February': 8, 'March': 9, 'April': 10, 'May': 11, 'June': 12}

HIR = ['KACCU-AUS-Babinda GBR',
       'KACCU-AUS-Barney Gumble HIR',
       'KACCU-AUS-Berangabah HIR',
       'KACCU-AUS-Bierbank & Lanherne HIR',
       'KACCU-AUS-Blinky Forest HIR',
       'KACCU-AUS-Boonora Downs HIR',
       'KACCU-AUS-Byrock Station Regrowth Project',
       'KACCU-AUS-Colodan GBR',
       'KACCU-AUS-Colodan GBR #6',
       'KACCU-AUS-Darling River Eco Corridor 3',
       'KACCU-AUS-Generic HIR',
       'KACCU-AUS-Hillview Park',
       'KACCU-AUS-Kilcowera & Zenonie HIR',
       'KACCU-AUS-Lindermans HIR',
       'KACCU-AUS-Lynwood Human-Induced Regeneration Project',
       'KACCU-AUS-Mullagalah HIR',
       'KACCU-AUS-Mullagalah II HIR',
       'KACCU-AUS-Myroolia HIR',
       'KACCU-AUS-Paroo River HIR',
       'KACCU-AUS-Paroowidgee HIR',
       'KACCU-AUS-Quimby Forest HIR',
       'KACCU-AUS-The Range HIR',
       'KACCU-AUS-Tuncoona Forest',
       'KACCU-AUS-Uteara Regeneration',
       'KACCU-AUS-Wiralla Regeneration HIR',
       'KACCU-AUS-Wongalee Mervyndale & Rundalua HIR',
       'KACCU-AUS-Woodstock Regeneration Project',
       'NKACCU-AUS-Inverness Human-Induced Regen',
       'KACCU-AUS-Generic HIR'
       ]

# OpEx information
client_id = 'A81BEC698C134BC88405217CA4AD3B0D'
client_secret = 'DQBNeDAUV4BPdSf2-Dx_FJz1hNqH6d0AzImAZSh5rd372u0R'
redirect_url = 'https://xero.com/'
scope = 'offline_access payroll.payruns'
