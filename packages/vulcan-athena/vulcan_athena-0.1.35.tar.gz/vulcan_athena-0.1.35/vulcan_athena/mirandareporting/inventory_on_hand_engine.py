import pandas as pd
import copy

from vulcan_athena.mirandareporting.setup import dataframe_tradebook

# reading in the data
data = dataframe_tradebook
data = data.fillna(0)  # TODO: data issue
# df = data[data['Status'] == STATUS].sort_values(['ValueDate', 'Direction'])
df = data.sort_values(['ValueDate', 'Direction'])


def add_index(df):
    length = len(df)
    index = [n for n in range(1, length + 1)]
    df.insert(loc=len(df.columns), value=index, column='tempIndex')
    return df


def seller(mylist, sell):
    while sell:

        if not mylist[0][0]:  # pop the first item off if the volume is 0
            mylist.pop(0)

        if mylist[0][0] > sell:
            mylist[0][0] -= sell
            sell = 0

        elif mylist[0][0] == sell:
            mylist[0][0] = 0
            sell = 0

        elif mylist[0][0] < sell:
            sell -= mylist[0][0]
            mylist[0][0] = 0

    return mylist


def create_inventory_list(df):
    mylist = []
    sell_list = []
    quantity = 0

    inventory_list = []
    sales_list = []

    future_flag = False

    for idx, row in df.iterrows():

        if row['Direction'] == 'Buy' and row['Status'] == 'Delivered':
            mylist.append([row['Volume'], row['Actual_Sale_Px']])
            quantity = sum([x for x in sell_list])

        elif row['Direction'] == 'Buy' and row['Status'] in ['Future', 'Prospective']:

            mylist.append([row['Volume'], row['Actual_Sale_Px']])
            quantity = 0

            future_flag = True

        elif row['Direction'] == 'Sell':
            sell = abs(row['Volume'])
            quantity = sell + sum([x for x in sell_list])

        units_on_hand = sum([x[0] for x in mylist])

        if future_flag:
            sell_list = []
            future_flag = False
        else:
            if units_on_hand >= quantity:
                mylist = seller(mylist, quantity)
                sell_list = []
            else:
                mylist = []
                # sell_list.append(quantity - units_on_hand)
                sell_list = [quantity - units_on_hand]

        x = copy.deepcopy(mylist)
        inventory_list.append(x)

        y = copy.deepcopy(sell_list)
        sales_list.append(y)

    return inventory_list, sales_list


def add_columns(df):
    length = len(df)
    index = [n for n in range(1, length + 1)]
    df.insert(loc=len(df.columns), value=index, column='tempIndex')

    inventory_column, sales_column = create_inventory_list(df)

    df.insert(loc=len(df.columns), value=inventory_column, column='inventory_on_hand')

    df.insert(loc=len(df.columns), value=sales_column, column='outstanding_sales')

    return df


stock_list = set(df['Name'])

master_list = []
count = 0

for stock in stock_list:
    group = add_columns(df[df['Name'] == stock])
    master_list.append(group)

# adding the dataframes together
stocks_df = master_list[0]

for df in master_list[1:]:
    stocks_df = stocks_df.append(df)
