# -*- coding: utf-8 -*-

import pandas


def get_income_sums(month=None, year=None):

    try:
        income_df = pandas.read_csv("income_database.csv")
        income_df['date'] = pandas.to_datetime(income_df['date'], format="%d.%m.%Y")
        total_income_sum = round(sum(income_df['amount']), 2)
        monthly_income_df = income_df[
            (income_df['date'].dt.month == month) &
            (income_df['date'].dt.year == year)
        ]
        monthly_income_sum = round(sum(monthly_income_df['amount']), 2)
        yearly_income_df = income_df[income_df['date'].dt.year == year]
        yearly_income_sum = round(sum(yearly_income_df['amount']), 2)

        return monthly_income_sum, yearly_income_sum, total_income_sum

    except FileNotFoundError:
        total_income_sum = 0
        monthly_income_sum = 0
        yearly_income_sum = 0

        return monthly_income_sum, yearly_income_sum, total_income_sum
