# -*- coding: utf-8 -*-

import tkinter as tk
import pandas

from datetime import date
from PIL import Image, ImageTk
from text_label import text_label, month_dict
from cat_window import open_cat_window
from hall_of_shame import hall_of_shame_plt
from get_income_sums import get_income_sums
from small_plt import small_plt
from line_plot_window import open_line_plot_window
from calc_earnings import calc_total_earnings

FONT = ("open sans", 15)
BOLD_FONT = ("open sans", 18, "bold")

PAPER_COLOR = "#fbfbfb"
ORANGE_COLOR = "#fcd9a8"
DARK_COLOR = "#6addda"
BLUE_COLOR = "#d0eef8"
DARK_BLUE_COLOR = "#3bc4cf"
GREEN_COLOR = "#D9EDBF"
RED_COLOR = "#FFB996"
DARK_ORANGE_COLOR = "#FFCF81"
PINK_COLOR = "#F7B5CA"
PURPLE_COLOR = "#AC87C5"
YELLOW_COLOR = "#F9F3CC"

color_list = [ORANGE_COLOR, DARK_ORANGE_COLOR, BLUE_COLOR, DARK_COLOR,
              DARK_BLUE_COLOR, GREEN_COLOR, RED_COLOR, PINK_COLOR,
              PURPLE_COLOR, YELLOW_COLOR, PAPER_COLOR,
              ]

current_date = date.today().strftime("%d.%m.%Y")
current_day = date.today().day
current_month = date.today().month
current_year = date.today().year

month_list = [f"0{month}" if month < 10 else str(month) for month in range(1, 13)]
category_list = []

try:
    with open("categories.txt", mode="r") as file:
        lines = file.readlines()
        for c in lines:
            clean_cat = c.split("/")[0].strip()
            category_list.append(clean_cat)
except FileNotFoundError:
    with open("categories.txt", mode="w") as file:
        file.write("")

category_list.sort()


def get_len_of_used_months():
    df = pandas.read_csv("planista_database.csv")

    df["date"] = pandas.to_datetime(df["date"], format="%d.%m.%Y")

    liste = []
    new_list = []

    for index, row in df.iterrows():
        liste.append(row.date.month)

    first_month = liste[0]
    new_list.append(first_month)

    for mo in liste:
        if not mo == first_month:
            first_month = mo
            if mo not in new_list:
                new_list.append(mo)

    result = len(new_list)

    return result


def open_statistics(main_window, lm_df, cat_dict, label_to_remove, bs_list, bs_values):
    """ opens the statistics window and creates several widgets"""
    global current_month

    main_window.update_idletasks()

    overall_stats_df = pandas.read_csv("planista_database.csv")
    overall_stats_df["date"] = pandas.to_datetime(overall_stats_df["date"], format="%d.%m.%Y")
    overall_curr_month_df = overall_stats_df[overall_stats_df["date"].dt.month == current_month]
    sum_current_month = sum(overall_curr_month_df["price"])
    sum_last_month = sum(lm_df["price"])

    income_tupel = get_income_sums(month=current_month, year=current_year)
    yearly_income_sum = income_tupel[1]

    def reset_entries():

        selected_month.set("")
        selected_cat_stats.set("")

        entries_year = overall_stats_df[overall_stats_df['date'].dt.year == current_year]

        total_sum_per_year = sum(entries_year['price'])

        for label in label_to_remove:
            label.destroy()

        year_entry.delete(0, tk.END)
        year_entry.insert(0, str(current_year))

        shop_sums = entries_year.groupby("shop")["price"].sum()
        cat_sums = entries_year.groupby("category")["price"].sum()
        total_purchases.config(text=f"Total items: {len(entries_year)}\n"
                                    f"Total cost: {round(total_sum_per_year, 2):.2f} EUR\n"
                                    f"Income: {yearly_income_sum} EUR"
                               )

        text_label(gui_frame_2, label_to_remove, 0, 0, current_year)

        small_plt(gui_frame_2, f"Shops for {current_year}", 8, 0, shop_sums.values, shop_sums.index)

        hall_of_shame_plt(stats_window, 9, 0, (4, 3), 0,
                          current_year, bs_list, bs_values, main_window)

        small_plt(gui_frame_2, f"Categories for {current_year}", 8, 2, cat_sums.values, cat_sums.index)

    def clear_year(event):
        """ clears the year entry widget """
        year_entry.delete(0, tk.END)
        year_entry.config(fg="black")

    def percentage_deviation(sum_curr, sum_last):
        """ Calculates the percentage deviation between the chosen/current month and the previous one"""
        try:
            perc_devi = round(sum_curr / (sum_last / 100) - 100, 2)
        except ZeroDivisionError:
            perc_devi = "100"

        return perc_devi

    # small PLTs zum jeweiligen monat ändern, auch wenn eine kategorie gewählt wurde
    def search_stats():

        for label in label_to_remove:
            label.destroy()

        label_to_remove.clear()

        search_df = pandas.read_csv("planista_database.csv")
        search_df["date"] = pandas.to_datetime(search_df["date"], format="%d.%m.%Y")

        try:
            chosen_month = int(selected_month.get())

        except ValueError:
            chosen_month = 0

        try:
            chosen_year = int(year_entry.get())
        except ValueError:
            chosen_year = 0

        chosen_cat = selected_cat_stats.get().lower()

        lm_dataframe = search_df[search_df['date'].dt.month == chosen_month - 1]
        # sum_actual_last_month = sum(lm_dataframe["price"])

        entries_month = search_df[(search_df["date"].dt.month == chosen_month) &
                                  (search_df["date"].dt.year == chosen_year)]

        entries_month_cat = search_df[(search_df["date"].dt.month == chosen_month) &
                                      (search_df["date"].dt.year == chosen_year) &
                                      (search_df["category"] == chosen_cat.lower())]

        entries_year = search_df[search_df["date"].dt.year == chosen_year]

        entries_year_cat = search_df[(search_df["date"].dt.year == chosen_year) &
                                     (search_df["category"] == chosen_cat.lower())]

        inner_income_tupel = get_income_sums(month=chosen_month, year=chosen_year)

        # len_months = get_len_of_used_months()

        fix_sum = 0

        try:
            fix_df = pandas.read_csv("fixed_cost.csv")
            fix_in = 0
            for index, row in fix_df.iterrows():
                fix_in += row.price
            fix_sum += fix_in

        except FileNotFoundError:
            pass

        for cate in category_list:
            cat_df1 = search_df[search_df["category"] == cate.lower()]
            cat_sum1 = cat_df1["price"].sum()
            cat_dict[cate] = cat_sum1

        total_sum_per_month = sum(entries_month["price"])
        total_sum_per_year = sum(entries_year["price"])

        # total_sum = round(inner_income_tupel[1] - (fix_sum * len_months) - total_sum_per_year, 2)

        # wenn keine Kategorie gewaehlt wurde
        if not chosen_cat:

            shop_sums = entries_month.groupby("shop")["price"].sum()
            cat_sums = entries_month.groupby("category")["price"].sum()

            # when nothing was chosen
            if chosen_month == 0 and chosen_year == 0 and not chosen_cat:

                overall_shopsums = search_df.groupby("shop")["price"].sum()
                overall_catsums = search_df.groupby("category")["price"].sum()

                total_purchases.config(text=f"Total items: {len(overall_stats_df['price'])}\n"
                                            f"Total cost: {round(sum(overall_stats_df['price']), 2):.2f} EUR\n"
                                            f"Income: {inner_income_tupel[2]} EUR"
                                       )

                text_label(gui_frame_2, label_to_remove, 0, 0, 0)

                small_plt(gui_frame_2, f"Overall Shops", 8, 0, overall_shopsums.values, overall_shopsums.index)

                hall_of_shame_plt(stats_window, 9, 0, (4, 3), 0, 0, bs_list, bs_values, main_window)

                small_plt(gui_frame_2, f"Overall Categories", 8, 2, overall_catsums.values, overall_catsums.index)

            # wenn Monat und Jahr gewaehlt wurden
            elif chosen_month > 0 and chosen_year != 0:
                try:
                    total_earnings = round(calc_total_earnings(chosen_month), 2)
                except TypeError:
                    total_earnings = 0
                if total_earnings > 0:
                    total_earnings = f"+{total_earnings}"

                sum_month_before_chosen_month_df = search_df[search_df["date"].dt.month == (chosen_month - 2) % 12 + 1]
                sum_month_before_chosen_month = sum(sum_month_before_chosen_month_df["price"])
                perc_dev_month = percentage_deviation(total_sum_per_month, sum_month_before_chosen_month)

                total_purchases.config(text=f"Total items: {len(entries_month)}\n"
                                            f"Total cost: {round(total_sum_per_month, 2):.2f} EUR\n"
                                            f"Difference last month: {perc_dev_month} %\n"
                                            f" Income: {inner_income_tupel[0]} EUR\n"
                                            f"{total_earnings} EUR"
                                       )

                text_label(gui_frame_2, label_to_remove, 0, chosen_month, chosen_year)

                small_plt(gui_frame_2, f"Shops for {month_dict[chosen_month]} {chosen_year}", 8, 0,
                          shop_sums.values, shop_sums.index)

                hall_of_shame_plt(stats_window, 9, 0, (4, 3),
                                  chosen_month, chosen_year, bs_list, bs_values, main_window)
                open_cat_window(gui_frame_2, entries_month, "All Categories")

                small_plt(gui_frame_2, f"Categories for {month_dict[chosen_month]} {chosen_year}", 8, 2,
                          cat_sums.values, cat_sums.index)

                # open_line_plot_window(main_window, month=chosen_month)

            # wenn kein Jahr gewählt wurde
            elif chosen_year == 0 or chosen_month == 0 and chosen_year == 0:
                total_purchases.config(text=f"Total items: {len(search_df['category'])}\n"
                                            f"Total cost: {round(sum(search_df['price']), 2):.2f} EUR\n"
                                            f"Income: {inner_income_tupel[2]} EUR"
                                       )

                text_label(gui_frame_2, label_to_remove, 0, 0, 0)

                small_plt(gui_frame_2, "Overall Shops", 8, 0, start_shop_sums.values, start_shop_sums.index)

                small_plt(gui_frame_2, "Overall Categories", 8, 2, start_cat_sums.values, start_cat_sums.index)

            # wenn nur Jahr gewaehlt wurde
            else:
                shop_sums = entries_year.groupby("shop")["price"].sum()
                cat_sums = entries_year.groupby("category")["price"].sum()
                total_purchases.config(text=f"Total items: {len(entries_year)}\n"
                                            f"Total cost: {round(total_sum_per_year, 2):.2f} EUR\n"
                                            f"Raw Income: {inner_income_tupel[1]} EUR"
                                       )

                text_label(gui_frame_2, label_to_remove, 0, 0, chosen_year)

                small_plt(gui_frame_2, f"Shops for {chosen_year}", 8, 0, shop_sums.values, shop_sums.index)

                hall_of_shame_plt(stats_window, 9, 0, (4, 3), 0,
                                  chosen_year, bs_list, bs_values, main_window)

                small_plt(gui_frame_2, f"Categories for {chosen_year}", 8, 2, cat_sums.values, cat_sums.index)

        # wenn Kategorie gewaehlt wurde
        else:
            cat_df2 = search_df[search_df["category"] == chosen_cat]
            cat_df_month = cat_df2[(cat_df2["date"].dt.month == chosen_month) &
                                   (cat_df2["date"].dt.year == chosen_year)]
            cat_df_year = cat_df2[cat_df2["date"].dt.year == chosen_year]

            # when only Cat was chosen
            if chosen_month == 0 and not chosen_year:
                cat_df3 = overall_stats_df[overall_stats_df['category'] == chosen_cat]
                only_cat_sums = round(sum(cat_df3['price']), 2)

                total_purchases.config(text=f"Total items: {len(cat_df3)}\n"
                                            f"Total cost: {only_cat_sums:.2f} EUR\n",
                                       font=BOLD_FONT)

                text_label(gui_frame_2, label_to_remove, chosen_cat.title(), 0, chosen_year)
                # open_line_plot_window(main_window, category=chosen_cat)

            # wenn Kategorie und Monat und Jahr gewaehlt wurden
            elif chosen_month > 0 and chosen_year:
                cat_sums = entries_month_cat.groupby("category")["price"].sum()
                cat_df_last_month = lm_dataframe[lm_dataframe['category'] == chosen_cat]
                cat_sum_lm = sum(cat_df_last_month['price'])
                cat_perc_1 = percentage_deviation(sum(cat_sums), cat_sum_lm)
                total_purchases.config(text=f"Total items: {len(cat_df_month)}\n"
                                            f"Total cost: {sum(cat_sums):.2f} EUR\n"
                                            f"Difference last month: {cat_perc_1} %",
                                       font=BOLD_FONT)

                text_label(gui_frame_2, label_to_remove, chosen_cat.title(), chosen_month, current_year)
                open_cat_window(gui_frame_2, entries_month_cat, chosen_cat)

                open_line_plot_window(main_window, category=chosen_cat)

            # when Cat and Year were chosen
            elif chosen_month == 0 and chosen_year:
                cat_sums = sum(cat_df2['price'])

                total_purchases.config(text=f"Total items: {len(cat_df2['price'])}\n"
                                            f"Total cost: {cat_sums:.2f} EUR\n",
                                       font=BOLD_FONT)

                text_label(gui_frame_2, label_to_remove, chosen_cat.title(), chosen_month, current_year)

                open_cat_window(gui_frame_2, entries_year_cat, chosen_cat)

                open_line_plot_window(main_window, category=chosen_cat, year=chosen_year)

            # wenn Kategorie und Monat gewaehlt wurden
            elif chosen_month > 0:
                open_cat_window(gui_frame_2, entries_month_cat, chosen_cat)
                cat_sums = entries_month_cat.groupby("category")["price"].sum()
                cat_df_last_month = lm_dataframe[lm_dataframe['category'] == chosen_cat]
                cat_sum_lm = sum(cat_df_last_month['price'])
                cat_perc_1 = percentage_deviation(sum(cat_sums), cat_sum_lm)
                total_purchases.config(text=f"Total items: {len(cat_df_month)}\n"
                                            f"Total cost: {sum(cat_sums):.2f} EUR\n"
                                            f"Difference last month: {cat_perc_1} %",
                                       font=BOLD_FONT)

                text_label(gui_frame_2, label_to_remove, chosen_cat.title(), chosen_month, current_year)

                # open_line_plot_window(main_window, category=chosen_cat)

            else:
                open_cat_window(gui_frame_2, entries_year_cat, chosen_cat)
                cat_sums = cat_df_year.groupby("category")["price"].sum()
                total_purchases.config(text=f"Total items: {len(cat_df_year)}\n"
                                            f"Total cost: {sum(cat_sums):.2f} EUR",
                                       font=BOLD_FONT)

                text_label(gui_frame_2, label_to_remove, chosen_cat.title(), 0, current_year)
                # open_line_plot_window(main_window, category=chosen_cat)
    try:
        current_month_earnings = round(calc_total_earnings(current_month), 2)
    except TypeError:
        current_month_earnings = 0

    if current_month_earnings > 0:
        current_month_earnings = f"+{round(current_month_earnings, 2)}"

    # WINDOW

    stats_window = tk.Toplevel(main_window)
    stats_window.minsize(900, 800)
    stats_window.config(bg="white")
    stats_window.title("PLANISTA Statistics")

    stats_image = Image.open("logo_stats.png")
    stats_logo = ImageTk.PhotoImage(stats_image)
    stats_window.stats_logo = stats_logo  # Speichere das Bild im Fenster

    selected_month = tk.StringVar()
    selected_cat_stats = tk.StringVar()

    gui_frame_2 = tk.Frame(stats_window, bg="white")
    gui_frame_2.grid(row=0, column=0)

    logo_label = tk.Label(gui_frame_2, image=stats_logo)
    logo_label.grid(row=0, column=1)

    month_text = tk.Label(master=gui_frame_2, text="Month", font=FONT, bg="white")
    month_text.grid(row=1, column=0, pady=15)

    year_text = tk.Label(master=gui_frame_2, text="Year", font=FONT, bg="white")
    year_text.grid(row=1, column=1, pady=15)

    cat_text = tk.Label(master=gui_frame_2, text="Category", font=FONT, bg="white")
    cat_text.grid(row=1, column=2, pady=15)

    text_label(gui_frame_2, label_to_remove, 0, 0, 0)

    month_menu = tk.OptionMenu(gui_frame_2, selected_month, *month_list)
    month_menu.config(bg=ORANGE_COLOR, font=FONT, width=2)
    month_menu.grid(row=2, column=0, padx=20)
    selected_month.set(f"{current_month}")

    menu_1 = gui_frame_2.nametowidget(month_menu.menuname)
    menu_1.config(font=("open sans", 13))

    year_entry = tk.Entry(master=gui_frame_2, justify="right", font=("courier", 16), bg=PAPER_COLOR)
    year_entry.grid(row=2, column=1)
    year_entry.insert(0, str(current_year))
    year_entry.bind("<Button-1>", clear_year)

    category_menu = tk.OptionMenu(gui_frame_2, selected_cat_stats, *category_list)
    category_menu.config(bg=ORANGE_COLOR, width=15, font=FONT)
    category_menu.grid(row=2, column=2, padx=30)

    menu_2 = gui_frame_2.nametowidget(category_menu.menuname)
    menu_2.config(font=("open sans", 13))

    search_button = tk.Button(master=gui_frame_2,
                              text="Search",
                              font=FONT,
                              command=search_stats,
                              bg=BLUE_COLOR,
                              width=10
                              )
    search_button.grid(row=3, column=1, padx=20, pady=20)

    reset_button = tk.Button(master=gui_frame_2,
                             text="RESET",
                             font=FONT,
                             bg=RED_COLOR,
                             width=10,
                             command=lambda: reset_entries(),
                             )
    reset_button.grid(row=3, column=2)

    text_label(gui_frame_2, label_to_remove, 0, current_month, current_year)

    perc_dev = percentage_deviation(sum_current_month, sum_last_month)

    total_purchases = tk.Label(master=gui_frame_2,
                               text=f"Total items: {len(overall_curr_month_df)}\n"
                                    f"Total cost: {sum_current_month :.2f} EUR\n"
                                    f"Difference last month: {perc_dev} %\n"
                                    f"Income: {income_tupel[0]} EUR\n"
                                    f"{current_month_earnings} EUR",
                               font=BOLD_FONT,
                               bg="white"
                               )
    total_purchases.grid(row=8, column=1, padx=20, pady=10)

    start_shop_sums = overall_curr_month_df.groupby("shop")["price"].sum()
    start_cat_sums = overall_curr_month_df.groupby("category")["price"].sum()

    small_plt(gui_frame_2,
              f"Shops for {month_dict[current_month]} {current_year}", 8, 0,
              start_shop_sums.values, start_shop_sums.index)

    hall_of_shame_plt(stats_window, 9, 0, (4, 3),
                      current_month, current_year, bs_list, bs_values, main_window)

    small_plt(gui_frame_2,
              f"Categories for {month_dict[current_month]} {current_year}", 8, 2,
              start_cat_sums.values, start_cat_sums.index)
