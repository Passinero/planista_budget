import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import pandas
from datetime import date

from text_label import month_dict
from calc_earnings import calc_total_earnings

current_date = date.today().strftime("%d.%m.%Y")
current_day = date.today().day
current_month = date.today().month


def open_line_plot_window(root, category=None, month=None, year=None):
    dataframe = pandas.read_csv("planista_database.csv")
    dataframe['date'] = pandas.to_datetime(dataframe['date'], format="%d.%m.%Y")
    sum_lst = []

    x = []

    counter = 5
    le_range = 6
    month_count = 0

    if month and not year:
        month_used = month - 5

        for i in range(le_range)[::-1]:
            month_x = month_dict[current_month - i]
            if month_x:
                x.append(month_x)

        for i in range(le_range):
            earnings = calc_total_earnings(month_used)
            # if earnings < 0:
            #     earnings = 0
            sum_lst.append(earnings)
            try:
                month_used += 1
            except TypeError:
                pass

            month_count = 6

    elif year and not month:

        for i in range(11)[::-1]:
            month_x = month_dict[current_month - i]
            if month_x:
                if not len(month_x) == 4:
                    month_x = month_x[:3]
                x.append(month_x)

        le_range = len(x)
        counter = 10
        for i in range(le_range):
            if not category:
                new_df = dataframe[dataframe['date'].dt.month == current_month - counter]
                new_sum = round(sum(new_df['price']), 2)
                sum_lst.append(new_sum)
            else:
                new_df = dataframe[(dataframe['date'].dt.month == current_month - counter) &
                                   (dataframe['category'] == category)]
                new_sum = round(sum(new_df['price']), 2)
                sum_lst.append(new_sum)

                counter -= 1

        month_count = 12

    else:
        print(f"else getriggert. le range: {le_range}")

        for i in range(6)[::-1]:
            month_x = month_dict[current_month - i]
            if month_x:
                x.append(month_x)

        for i in range(le_range):

            if not category:
                new_df = dataframe[dataframe['date'].dt.month == current_month - counter]
                new_sum = round(sum(new_df['price']), 2)
                sum_lst.append(new_sum)
            else:
                new_df = dataframe[(dataframe['date'].dt.month == current_month - counter) &
                                   (dataframe['category'] == category)]
                new_sum = round(sum(new_df['price']), 2)
                sum_lst.append(new_sum)

            counter -= 1

        month_count = 6

    y = [summ for summ in sum_lst]

    lp_window = tk.Toplevel(root)
    lp_window.minsize(500, 500)

    if month:
        lp_window.title("Total income last 6 months")
    else:
        lp_window.title(f"Expenses for {category.title()} last {month_count} months")

    fig, ax = plt.subplots()

    ax.plot(x, y)
    ax.set_xlabel("Month")
    ax.set_ylabel("Money")
    if month:
        ax.set_title("Total income last 6 months")
    else:
        ax.set_title(f"Expenses for {category.title()} last {month_count} months")

    canvas = FigureCanvasTkAgg(fig, master=lp_window)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0)
