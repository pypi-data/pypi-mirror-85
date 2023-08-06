from collections import defaultdict, OrderedDict
from vulcan_athena.mirandareporting.setup import GEN_LIST


def inventory_logic(value_list, o_sales):
    mydict = OrderedDict()

    for i in value_list:
        mydict[i[1]] = i[0]

    sales = sum(o_sales)

    for key in mydict.keys():
        if sales:
            if mydict[key] >= sales:
                mydict[key] -= sales
                sales = 0

            elif mydict[key] < sales:
                sales -= mydict[key]
                mydict[key] = 0

    return mydict


def opening_inv_gen(df):
    units = df['Volume'].sum()
    value_list = df['inventory_on_hand'].iloc[-1]
    o_sales = df['outstanding_sales'].iloc[-1]

    if o_sales:
        inv_dict = inventory_logic(value_list, o_sales)
        price = sum([key * val for key, val in inv_dict.items()])
    else:
        price = sum([vol * price for vol, price in value_list])

    return {'Volume': units, 'Price': price}


def closing_value_gen(df, stock, wacgu_dict, last_buy_price, stat, data):
    value_list = df['inventory_on_hand'].iloc[-1]
    o_sales = df['outstanding_sales'].iloc[-1]
    month = 'April'  # calendar.month_name[df['ValueDate'].iloc[0].month] # TODO: Change this harcoded value

    if stock in last_buy_price.keys():
        price = last_buy_price[stock]
    elif stock in wacgu_dict[month].keys():
        price = wacgu_dict[month][stock]
    else:
        price = 0

    if o_sales:
        if not value_list:
            vol = sum(o_sales)
        else:
            vol = sum(o_sales) - sum([x[0] for x in value_list])
    else:
        vol = 0

    if vol and (stat == 'Prospective'):
        future_o_sales = \
            data[(data['Name'] == stock) & (data['Status'] == 'Future')].sort_values(by='ValueDate').iloc[-1][
                'outstanding_sales'] if len(data[(data['Name'] == stock) & (data['Status'] == 'Future')]) else []
        vol -= sum(future_o_sales)

    return -vol * price


def opening_value(df):
    value_list = df['inventory_on_hand'].iloc[-1]
    o_sales = df['outstanding_sales'].iloc[-1]

    if o_sales:
        inv_dict = inventory_logic(value_list, o_sales)
        return sum([key * val for key, val in inv_dict.items()])
    else:
        return sum([vol * price for vol, price in value_list])


def closing_value(df):
    value_list = df['inventory_on_hand'].iloc[-1]
    o_sales = df['outstanding_sales'].iloc[-1]

    if o_sales:
        inv_dict = inventory_logic(value_list, o_sales)
        return sum([key * val for key, val in inv_dict.items()])
    else:
        return sum([vol * price for vol, price in value_list])


def movement_in_value(df, stock, ssp_dict):
    if stock in ssp_dict.keys():
        ssp = ssp_dict[stock]
    else:
        ssp = 0
        print(f'Error - {stock} SSP not found \n')
        with open('logfile.txt', 'a+') as logger:
            logger.write(stock + ' not found' + '\n')

    inventory_1 = df['inventory_on_hand'].iloc[0]
    inventory_2 = df['inventory_on_hand'].iloc[-1]

    initial_inventory = sum([vol for vol, price in inventory_1])
    final_inventory = sum([vol for vol, price in inventory_2])

    return ssp * (final_inventory - initial_inventory)


def voi(df, stock, ssp_df):
    if stock in ssp_df.index:
        year = str(df['ValueDate'].iloc[-1]).split('-')[0]
        ssp = ssp_df.xs(stock)[year]
    else:
        ssp = 0

    current_units = df['inventory_on_hand'].iloc[-1]
    o_sales = df['outstanding_sales'].iloc[-1]

    if o_sales:
        inv_dict = inventory_logic(current_units, o_sales)
        final_inventory = sum(inv_dict.values())
    else:
        final_inventory = sum([vol for vol, price in current_units])

    return ssp * final_inventory


def dict_creator(sales, purchases, sale_margin):
    '''
    function to create a dictionary from the calculated values
    :return: a dictionary object
    '''
    d = {'Sales': sales, 'Purchases': purchases, 'Sale Margin': sale_margin}

    return d


def calculate_stock_info(df):
    '''
    calculate the information about the stock
    :param data: information af all the trades in the month
    :param stat: status of the trade
    :param last_buy_price: dictionary that contains the last buy price of the generalized units
    :param wacgu_dict: dictionary that contains the weighted average cost of generalized units
    :param check_flag: flag for a special closing inventory logic to avoid double counts
    :param ssp_df: dataframe that contains the current SSP values of each stock
    :param stock: the stock name for which the financials are being calculated
    :param previous_data: subset dataframe containg historical information of the stock
    :param df: subset dataframe and sorted values of the stock
    :return: returns a dictionary with the stock name and the relevant information
    '''

    # get the ledger
    ledger = defaultdict()
    for idx, row in df.iterrows():
        ledger[idx] = {'Direction': row['Direction'], 'Volume': row['Volume'], 'SSP': row['SSP'],
                       'ActualPrice': row['Actual_Sale_Px'], 'Date': row['FormattedDate']}

    # get the queue
    sell_list = []
    buy_list = []
    for key, item in ledger.items():
        if item['Direction'] == 'Buy':
            buy_list.append(item)
        else:
            sell_list.append(item)

    # Sales
    sales = sum(abs(sell['Volume']) * sell['ActualPrice'] for sell in sell_list)
    # Purchases
    purchases = sum(buy['Volume'] * buy['ActualPrice'] for buy in buy_list)

    # sale margin
    sale_margin = sum(abs(sell['Volume']) * (sell['ActualPrice'] - sell['SSP']) for sell in sell_list)

    d = dict_creator(sales, purchases, sale_margin)

    return d


def calculate_sales(df):
    '''
    calculate the sale information about the stock
    :param df: subset dataframe and sorted values of the stock
    :return: returns total sales for that value of the stock
    '''

    # get the ledger
    ledger = defaultdict()
    for idx, row in df.iterrows():
        ledger[idx] = {'Direction': row['Direction'], 'Volume': row['Volume'], 'SSP': row['SSP'],
                       'ActualPrice': row['Actual_Sale_Px'], 'Date': row['FormattedDate']}

    # get the queue
    sell_list = []
    buy_list = []
    for key, item in ledger.items():
        if item['Direction'] == 'Buy':
            buy_list.append(item)
        else:
            sell_list.append(item)

    # Sales
    sales = sum(abs(sell['Volume']) * sell['ActualPrice'] for sell in sell_list) if sell_list else 0
    # sale margin
    sale_margin = sum(
        abs(sell['Volume']) * (sell['ActualPrice'] - sell['SSP']) for sell in sell_list) if sell_list else 0

    return {'Sales': sales, 'Sale Margin': sale_margin}


def calculate_opening_inventory_actual(df, df_period, df_shortfall, ssp_df, stock, ssp_year, wacgu_dict, month,
                                       shortfall_flag):
    """
    Actual Period - Aggregate of inventory on hand balance for each unit
    :param shortfall_flag: forecast for previous time period should not be included
    :param month: current month
    :param df_period: sliced dataframe till the end of the month
    :param df_shortfall: sliced data for that particular month
    :param wacgu_dict: weighted average cost of generalized units
    :param ssp_year: year for which the corresponding ssp should be calculated for
    :param stock: name of the stock
    :param ssp_df: dataframe contains the relevant SSP
    :param df: sliced dataframe
    :return: returns opening inventory for the stock at the beginning of the reporting period
    """
    if (not len(df)) and (not len(df_period)):
        return {'Opening Inventory': 0, 'Shortfall': 0, 'Value of Inventory': 0}

    ssp_year = str(ssp_year)  # change type

    if stock in ssp_df.index:
        if ssp_year in ssp_df.columns:
            ssp = ssp_df.xs(stock)[ssp_year]
        else:
            ssp = ssp_df.xs(stock)['2019']
    else:
        ssp = 0

    value_list = df['inventory_on_hand'].iloc[-1] if len(df) else []
    value_list_2 = df_period['inventory_on_hand'].iloc[-1] if len(df_period) else []
    outstanding_sales_list = df_shortfall['outstanding_sales'].iloc[-1] if len(df_shortfall) else []

    outstanding_sales = outstanding_sales_list[0] if len(outstanding_sales_list) else 0

    drawdown = df['difference_bw_shortfalls'].sum()
    drawdown_2 = df_period['difference_bw_shortfalls'].sum()

    wacgu_price = wacgu_dict[stock] if stock in wacgu_dict.keys() else 0
    drawdown_value = - (drawdown * wacgu_price)
    drawdown_2_value = - (drawdown_2 * wacgu_price)

    opening_inventory = (sum([vol * price for vol, price in value_list]) + drawdown_value)
    # shortfall = (outstanding_sales - drawdown_2) * ssp
    value_of_inventory = (sum([vol for vol, price in value_list_2]) * ssp) + drawdown_2_value

    if stock in GEN_LIST:
        shortfall_vol = df_shortfall['Shortfall_Gen'].sum()
    else:
        shortfall_vol = df_shortfall['Shortfall_Individual'].sum()

    if not shortfall_flag:
        shortfall_vol = 0

    shortfall = shortfall_vol * ssp

    return {'Opening Inventory': opening_inventory,
            'Shortfall': shortfall,
            'Shortfall Volume': shortfall_vol,
            'Value of Inventory': value_of_inventory}


def calculate_opening_inventory_forecast(df, ssp_df, stock, ssp_year):
    """
    Forecast Period - Aggregate of inventory on hand balance for each unit (considered at the parent/head code level)
    :param ssp_year: year for which the corresponding ssp should be calculated for
    :param stock: name of the stock
    :param ssp_df: dataframe contains the relevant SSP
    :param df: sliced dataframe
    :return: returns opening inventory for the stock at the beginning of the reporting period
    """
    if not len(df):
        return {'Opening Inventory': 0, 'Shortfall': 0}

    if stock in ssp_df.index:

        if ssp_year in ssp_df.columns:
            ssp = ssp_df.xs(stock)[ssp_year]
        else:
            ssp = ssp_df.xs(stock)['2019']  # TODO: change this
    else:
        ssp = 0

    value_list = df['gen_inventory_on_hand'].iloc[-1]
    sales_list = df['gen_outstanding_sales'].iloc[-1]
    return {'Opening Inventory': sum([vol * price for vol, price in value_list]), 'Shortfall': sum(sales_list) * ssp}


def calculate_opening_inventory(df, wacgu_dict, last_buy_price, stock, month, start_date):
    '''
    calculate the opening inventory of each stock
    :param month: month
    :param stock: name of the stock
    :param last_buy_price: last buy price of the stock
    :param wacgu_dict: weighted average price of the generalized stock
    :param df: subset dataframe and sorted values of the stock
    :return: returns opening inventory for the stock at the beginning of the reporting period
    '''

    if not len(df):
        return {'Opening Inventory': 0, 'Shortfall': 0}

    value_list = df['inventory_on_hand'].iloc[-1]
    o_sales = df['outstanding_sales'].iloc[-1]

    inv_on_hand = sum([x[0] for x in value_list])
    outstanding_items = sum([x for x in o_sales])

    if inv_on_hand == outstanding_items:
        return {'Opening Inventory': 0, 'Shortfall': 0}

    if inv_on_hand > outstanding_items:

        for idx, j in enumerate(value_list):
            if j[0] > outstanding_items:
                value_list[idx][0] -= outstanding_items
                outstanding_items = 0
            else:
                outstanding_items -= value_list[idx][0]
                value_list[idx][0] = 0

        return {'Opening Inventory': sum([vol * price for vol, price in value_list]), 'Shortfall': 0}

    o_value = sum([vol * price for vol, price in value_list])

    if outstanding_items - inv_on_hand > 0:
        if stock in wacgu_dict.keys():
            price = wacgu_dict[stock]
        else:
            price = last_buy_price[stock] if stock in last_buy_price.keys() else 0

        # return {'Opening Inventory': o_value - (sum(o_sales) * price)}
        return {'Opening Inventory': 0, 'Shortfall': - (outstanding_items - inv_on_hand) * price}
