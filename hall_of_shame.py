# -*- coding: utf-8 -*-

import tkinter as tk
import pandas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import date
import numpy as np

from text_label import month_dict
# from color_list import (ORANGE_COLOR, DARK_ORANGE_COLOR, DARK_BLUE_COLOR,
#                         BLUE_COLOR, GREEN_COLOR, RED_COLOR, PINK_COLOR, PURPLE_COLOR, YELLOW_COLOR, DARK_COLOR)

FONT = ("open sans", 15)
BOLD_FONT = ("open sans", 18, "bold")

PAPER_COLOR = "#fbfbfb"
ORANGE_COLOR = "#fcd9a8"
DARK_COLOR = "#6addda"
BLUE_COLOR = "#d0eef8"
DARK_BLUE_COLOR = "#3bc4cf"
GREEN_COLOR = "#D9EDBF"
RED_COLOR = "#FFB996",
DARK_ORANGE_COLOR = "#FFCF81"
PINK_COLOR = "#F7B5CA"
PURPLE_COLOR = "#AC87C5"
YELLOW_COLOR = "#F9F3CC"

color_list = [ORANGE_COLOR, DARK_ORANGE_COLOR, BLUE_COLOR, DARK_COLOR,
              DARK_BLUE_COLOR, GREEN_COLOR, RED_COLOR, PINK_COLOR,
              PURPLE_COLOR, YELLOW_COLOR,
              ]

current_date = date.today().strftime("%d.%m.%Y")
current_day = date.today().day
current_month = date.today().month
current_year = date.today().year


def hall_of_shame_plt(root, row, column, figsize, chosen_month, chosen_year, bs_list, bs_values, main_window):

    def fill_bs_list(df):

        tupel_list = []

        hos_sums = df.groupby('category')['price'].sum()

        alc = hos_sums.get('alkohol', 0)
        fastfood = hos_sums.get('fast food', 0)
        gambling = hos_sums.get('gluecksspiel', 0)
        tobacco = hos_sums.get('tabakwaren', 0)
        sweets = hos_sums.get('sweets', 0)

        if alc:
            tupel_list.append(("Alkohol", alc))
        if fastfood:
            tupel_list.append(("Fast Food", fastfood))
        if gambling:
            tupel_list.append(("Gluecksspiel", gambling))
        if tobacco:
            tupel_list.append(("Tabakwaren", tobacco))
        if sweets:
            tupel_list.append(("Sweets", sweets))

        bad_sum = alc + fastfood + gambling + tobacco + sweets

        tupel_list.sort(key=lambda x: x[1])

        for pair in tupel_list:
            bs_list.append(pair[0])
            bs_values.append(pair[1])

        return bad_sum

    def hos_bar_chart_window():

        categories = ["alkohol", "fast food", "gluecksspiel", "tabakwaren", "sweets"]

        current_month_values = []
        last_month_values = []

        for category in categories:
            current_value = hos_cat_sums.get(category, 0)
            last_month_value = hos_last_month_cat_sums.get(category, 0)

            current_month_values.append(current_value)
            last_month_values.append(last_month_value)

        bar_chart_window = tk.Toplevel(main_window)
        bar_chart_window.title("Hall of Shame Comparison")
        bar_chart_window.config(bg="white")
        bar_chart_window.minsize(400, 400)

        chart_frame_2 = tk.Frame(bar_chart_window, bg="white")
        chart_frame_2.grid(row=0, column=0, pady=10)

        x = np.arange(len(categories))

        width = 0.35

        fig2, ax2 = plt.subplots(figsize=(6, 5))
        fig2.patch.set_facecolor('white')

        bars_current = ax2.bar(x - width / 2, current_month_values, width, label='Current Month')
        bars_previous = ax2.bar(x + width / 2, last_month_values, width, label='Last Month')

        ax2.set_xlabel('')
        ax2.set_ylabel('')
        ax2.set_title('Comparison Current and Previous Month')
        ax2.set_xticks(x)
        ax2.set_xticklabels(["Alk", "Fast Food", "Gambling", "Tabak", "Sweets"])
        ax2.legend()

        ax2.set_aspect('auto')

        canvas2 = FigureCanvasTkAgg(fig2, master=chart_frame_2)
        canvas2.draw()
        canvas_widget2 = canvas2.get_tk_widget()
        canvas_widget2.config(bg="white")
        canvas_widget2.grid(row=0, column=0)

    bs_list.clear()
    bs_values.clear()

    hos_df = pandas.read_csv("planista_database.csv")
    hos_df["date"] = pandas.to_datetime(hos_df["date"], format="%d.%m.%Y")

    if chosen_month == 1:
        last_month = 12
    else:
        last_month = chosen_month - 1

    hos_month_df = hos_df[hos_df["date"].dt.month == chosen_month]
    hos_last_month_df = hos_df[hos_df["date"].dt.month == last_month]
    hos_year_df = hos_df[hos_df['date'].dt.year == chosen_year]

    hos_cat_sums = hos_month_df.groupby("category")["price"].sum()
    hos_last_month_cat_sums = hos_last_month_df.groupby("category")["price"].sum()

    if chosen_month == 0 and chosen_year == 0:
        month_name = ""
        curr_year = "Overall"
        hos_sum = fill_bs_list(hos_df)

    elif chosen_month == 0:
        month_name = ""
        curr_year = current_year
        hos_sum = fill_bs_list(hos_year_df)

    else:
        month_name = month_dict[chosen_month]
        curr_year = current_year
        hos_sum = fill_bs_list(hos_month_df)

    chart_frame = tk.Frame(root)
    chart_frame.grid(row=row, column=column)

    fig, ax = plt.subplots(figsize=figsize)

    if bs_list:
        ax.pie(bs_values,
               labels=bs_list,
               colors=color_list,
               autopct=lambda p: f'{p * sum(bs_values) / 100 :.0f} EUR')
        ax.set_title(f"Hall of Shame {month_name} {curr_year} - {round(hos_sum, 2)} EUR")

    else:
        ax.pie([1], labels=["No data"], colors=['gray'])
        ax.set_title(f"Hall of Shame {month_name} {current_year} - No data")

    ax.set_aspect('equal')

    fig.subplots_adjust(left=0.1, right=1.0, top=0.9, bottom=0.1)

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.bind("<Button-1>", lambda event: hos_bar_chart_window())
    canvas_widget.grid(row=row, column=column)
