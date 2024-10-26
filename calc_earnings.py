# -*- coding: utf-8 -*-

import pandas as pd


def calc_total_earnings(month):
    search_df = pd.read_csv("planista_database.csv")
    try:
        fc_df = pd.read_csv("fixed_cost.csv")
        fixcosts = 0
        for index, row in fc_df.iterrows():
            fixcosts += row.price

    except FileNotFoundError:
        fixcosts = 0

    try:
        income_dataframe = pd.read_csv("income_database.csv")
        income_dataframe['date'] = pd.to_datetime(income_dataframe['date'], format="%d.%m.%Y")
        search_df['date'] = pd.to_datetime(search_df['date'], format="%d.%m.%Y")

        monthly_income = income_dataframe[income_dataframe['date'].dt.month == month]
        income_sum = sum(monthly_income['amount'])

        monthly_cost = search_df[search_df['date'].dt.month == month]
        cost_sum = sum(monthly_cost['price'])

        earnings = income_sum - cost_sum - fixcosts
        if cost_sum == 0:
            earnings = 0

        return earnings

    except FileNotFoundError:
        return
