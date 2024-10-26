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


def open_line_plot_window(root, category=None, month=None):

    dataframe = pandas.read_csv("planista_database.csv")
    dataframe['date'] = pandas.to_datetime(dataframe['date'], format="%d.%m.%Y")
    sum_lst = []

    counter = 5

    if month:
        month_used = month - 5

        for i in range(6):
            earnings = calc_total_earnings(month_used)
            if earnings < 0:
                earnings = 0
            sum_lst.append(earnings)
            try:
                month_used += 1
            except TypeError:
                pass

    else:
        for i in range(6):

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

    x = [month_dict[current_month - x] for x in range(6)[::-1]]
    print(x)

    y = [summ for summ in sum_lst]
    print(y)

    lp_window = tk.Toplevel(root)
    lp_window.minsize(500, 500)
    if month:
        lp_window.title("Total income last 6 months")
    else:
        lp_window.title(f"Total expenses for {category.title()} last 6 months")

    fig, ax = plt.subplots()

    ax.plot(x, y)
    ax.set_xlabel("Month")
    ax.set_ylabel("Money")
    if month:
        ax.set_title("Total income last 6 months")
    else:
        ax.set_title(f"Expenses for {category.title()} last 6 months")

    canvas = FigureCanvasTkAgg(fig, master=lp_window)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0)

    lp_window.mainloop()

