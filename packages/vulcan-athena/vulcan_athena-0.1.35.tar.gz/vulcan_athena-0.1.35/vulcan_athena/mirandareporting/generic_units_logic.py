from vulcan_athena.mirandareporting.setup import GEN_LIST


def calculate_wacgu(df):
    opening_inv = sum(df['Price'])
    vol = sum(df['Volume'])

    return round(opening_inv / vol, 2) if vol else 0


def wacgu(gen_dict):
    wacgu_dict = {}

    for gen in gen_dict.keys():
        val = calculate_wacgu(gen_dict[gen]) if len(gen_dict[gen]) else 0
        wacgu_dict[gen] = val

    return wacgu_dict


def get_gen_stock_list(gen_dict):
    gen_stock_list = set(GEN_LIST)
    for gen in gen_dict.keys():
        if len(gen_dict[gen]):
            for name in gen_dict[gen]['Name']:
                gen_stock_list.add(name)

    return gen_stock_list


def get_last_buy_price(df):
    last_buy_price = {}
    gen_set = set(df['Name'])
    for stock in gen_set:
        if stock not in GEN_LIST:
            last_buy_price[stock] = \
                df[(df['Status'] == 'Delivered') & (df['Name'] == stock) & (df['Direction'] == 'Buy')].iloc[-1][
                    'Actual_Sale_Px'] if len(
                    df[(df['Status'] == 'Delivered') & (df['Name'] == stock) & (df['Direction'] == 'Buy')]) else 0

    return last_buy_price


def drawdown(df, wacgu_dict):

    def outstanding_dd(row):
        if row['Name'] == row['Generalised_Name'] and len(row['outstanding_sales']):
            value_list = row['gen_inventory_on_hand']
            gen_units_on_hand = sum([vol for vol, price in value_list])

            wacgu_price = wacgu_dict[row['Generalised_Name']] if row['Generalised_Name'] in wacgu_dict.keys() else 0

            if gen_units_on_hand:
                return - (row['outstanding_sales'][0] * wacgu_price)
            else:
                dd_units = row['outstanding_sales'][0] - row['gen_outstanding_sales'][0]
                return - (dd_units * wacgu_price)

        return 0

    df['Drawdown_Inventory'] = df.apply(outstanding_dd, axis=1)

    return df
