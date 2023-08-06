import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from collections import defaultdict
import math
from scipy import stats


def get_deviation(item, df):
    """
    get the standard deviation of the different price points at which the item is being sold
    :param item: item code
    :param df: dataframe
    :return: logged standard deviation of the item price
    """
    data = df[(df['item_code'] == item) & (df['unit_price'] > 0)]
    return np.std(data['unit_price'].apply(math.log) / max(data['unit_price'].apply(math.log))) if len(data) else 0


def get_qty(item, df):
    """
    get the distribution of quantity at different price points
    :param item: item code
    :param df: dataframe
    :return: dictionary with key as price and quantity as value for that item
    """
    unique_prices = list(set(df[df['item_code'] == item]['unit_price']))
    mydict = {}

    for i in range(len(unique_prices)):
        mydict[unique_prices[i]] = sum(df[(df['item_code'] == item) & (df['unit_price'] == unique_prices[i])]['qty'])

    return mydict


def get_entropy(mydict):
    """
    calculate the entropy of the price distribution for the item
    :param mydict: dictionary of quantity distribution for different price points
    :return: entropy value
    """
    total = sum(mydict.values())
    entropy_list = [(val / total) for key, val in mydict.items()] if total else []
    return stats.entropy(entropy_list, base=2)


def get_variability(item, df):
    """
    calculate the price variability
    :param item: item code
    :param df: dataframe
    :return: variability metric as a product of standard deviation and entropy
    """
    return get_deviation(item, df) * get_entropy(get_qty(item, df))


def mean_item_price(df):
    """
    calculate the mean price for each item
    :param df: original dataframe
    :return: dataframe with mean prices for each item
    """
    mean_item_df = pd.DataFrame(df[['item_code', 'unit_price']].groupby('item_code').mean())
    mean_item_df = mean_item_df.reset_index()
    mean_item_df.columns = ['item_code', 'mean']
    return mean_item_df


def sd_item_price(df):
    """
    calculate the standard deviation for each item
    :param df: original dataframe
    :return: dataframe with mean prices for each item
    """
    sd_item_df = pd.DataFrame(df[['item_code', 'unit_price']].groupby('item_code').sd())
    sd_item_df = sd_item_df.reset_index()
    sd_item_df.columns = ['item_code', 'sd']
    return sd_item_df


def avg_customer_spend(customer, df, mean_item_df):
    """
    on average based on the purchase history, how much would the customer spend
    :param mean_item_df: mean prices for each item
    :param customer: customer name
    :param df: dataframe for that period
    :return: aggregated average spend
    """

    ideal_customer = []
    for idx, row in df[df['customer_name'] == customer][['item_code', 'unit_price', 'qty']].iterrows():
        mean_price = float(mean_item_df[mean_item_df['item_code'] == row['item_code']]['mean'])
        ideal_customer.append(mean_price * row['qty'])

    return sum(ideal_customer)


def expected_sales(df, mean_item_df, group='customer_name'):
    """
    expected sales for all the customers
    :param group: column name that it needs to be grouped by
    :param df: dataframe for the period
    :param mean_item_df: mean prices for each item
    :return: return the aggregated expected sales for each customer
    """

    df['actual_sales'] = df['qty'] * df['unit_price']
    summarized_df = pd.DataFrame(df.groupby(group).sum()['actual_sales']).reset_index()
    summarized_df['expected_sales'] = summarized_df[group].apply(lambda x: avg_customer_spend(x, df, mean_item_df))
    return summarized_df

