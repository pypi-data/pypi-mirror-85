"""Main module."""
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def say_hello(name=None):
    if name is None:
        return 'Welcome to Athena...'
    else:
        return f'Welcome to Athena, {name}!'


def sqrt_function(num):
    return np.sqrt(num)


def stats_data(df):
    """
    returns the basic statistics of the dataframe
    :param df: dataframe provided by the user
    """
    return pd.DataFrame(df.describe().reset_index().rename(columns={'index': 'stats'}))


# TODO: Write a function that takes a dictionary as an input and renames the columns in the dataframe with that
