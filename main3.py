# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox
import pandas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import date
from PIL import Image, ImageTk
from text_label import text_label, month_dict
import numpy as np

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
              PURPLE_COLOR, YELLOW_COLOR,
              ]

current_date = date.today().strftime("%d.%m.%Y")
current_month = date.today().month
current_year = date.today().year

category_list = ["Lebensmittel", "Haushalt", "Kleidung", "Elektronik", "Pflanzen",
                 "Fast Food", "Ausbildung", "Fluff", "Tabakwaren",
                 "Auto", "Alkohol", "Restaurant", "Gluecksspiel",
                 "Tanken", "Geschenke", "Arbeit", "Daniela",
                 "Post", "Bueroartikel", "Urlaub", "Sonstiges",
                 ]

shop_list = ["Penny", "Famila", "Aldi", "Growshop",
             "DM", "Rewe", "Edeka", "Amazon",
             "Kleinanzeigen", "Online Sonstiges", "Restaurant", "Tankstelle",
             "Kiosk", "Action", "Kik", "H&M",
             "Fast Food", "Werkstatt", "Paypal", "Sonstiges",
             "McDonald's", 'Burger King',
             ]

shop_list.sort()
category_list.sort()

month_list = [f"0{month}" if month < 10 else str(month) for month in range(1, 13)]

price_per_cat = []
found_cat = []

label_to_remove = []

bad_stuff_list = []
bad_stuff_values = []

cat_dict = {}


dataframe = pandas.read_csv("planista_database.csv")
dataframe["date"] = pandas.to_datetime(dataframe["date"], format="%d.%m.%Y")

current_month_df = dataframe[dataframe["date"].dt.month == current_month]

if current_month == 1:
    last_month_df = dataframe[dataframe["date"].dt.month == 12]
else:
    last_month_df = dataframe[dataframe["date"].dt.month == current_month - 1]

category_sums = current_month_df.groupby("category")["price"].sum()

for cat in category_list:
    cat_df = dataframe[dataframe["category"] == cat.lower()]
    cat_sum = cat_df["price"].sum()
    cat_dict[cat] = cat_sum

try:
    last_entry_df = dataframe.iloc[-1]
    last_entry_item = last_entry_df["item"]
    last_entry_price = last_entry_df["price"]
    last_entry_date = last_entry_df["date"]

except IndexError:
    last_entry_df = ""
    last_entry_item = ""
    last_entry_price = ""
    last_entry_date = ""


def update_last_entry():
    """ updates the last item bought """
    try:
        temp_df = pandas.read_csv("planista_database.csv")

        if temp_df.empty:
            last_entry_text.config(text="No entries found")
            return

        last_item = temp_df.iloc[-1]

        last_entry_text.config(text=f"Your last entry: "
                                    f"{last_item['item'].title()} - "
                                    f"{last_item['price']:.2f} EUR - "
                                    f"{last_item['date']}")

    except (KeyError, IndexError, FileNotFoundError) as e:
        last_entry_text.config(text=f"Error: {str(e)}")


def save_data():
    """ saves the data put in """
    item = item_entry.get().lower()
    price = cost_entry.get().lower().replace(",", ".")
    category = selected_category.get().lower()
    shop = selected_shop.get().lower()
    curr_date = date_entry.get()

    if not item or not price or not category or not shop:
        messagebox.showerror("error", "All fields must be filled")
        return

    try:
        price = float(price)
    except ValueError:
        messagebox.showerror("error", "The price is not right")
        return

    new_data = pandas.DataFrame({"item": [item],
                                 "shop": [shop],
                                 "category": [category],
                                 "price": [price],
                                 "date": [curr_date],
                                 })

    new_data.to_csv("planista_database.csv", mode="a", index=False, header=False)

    item_entry.delete(0, tk.END)
    cost_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    date_entry.insert(1, current_date)
    selected_category.set("---")
    selected_shop.set("---")

    hall_of_shame_plt(main_window, 7, 0, (5,4), current_month)

    update_last_entry()
    main_window.update()
    messagebox.showinfo("Data saved successfully", "Your data was saved")


def plt_window_1(values, labels, title):
    labels = labels.tolist()
    labels = [label.title() for label in labels]

    plt_window = tk.Toplevel(main_window)
    plt_window.minsize(400, 400)
    plt_window.title(title.title())
    plt_window.config(bg="white")

    chart_frame = tk.Frame(plt_window)
    chart_frame.grid(row=0, column=0, padx=20, pady=10)

    fig, ax = plt.subplots(figsize=(11, 11))

    ax.pie(values,
           labels=labels,
           colors=color_list,
           autopct=lambda p: f'{p * sum(values) / 100 :.0f} EUR')
    ax.set_title(title)

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.LEFT)


def hall_of_shame_plt(root, row, column, figsize, chosen_month):

    global bad_stuff_list, bad_stuff_values

    def hos_bar_chart_window():

        categories = ["alkohol", "fast food", "gluecksspiel", "tabakwaren"]

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
        chart_frame_2.grid(row=0, column=0, pady=50)

        x = np.arange(len(categories))

        width = 0.35

        fig2, ax2 = plt.subplots(figsize=figsize)
        fig2.patch.set_facecolor('white')

        bars_current = ax2.bar(x - width / 2, current_month_values, width, label='Current Month')
        bars_previous = ax2.bar(x + width / 2, last_month_values, width, label='Last Month')

        ax2.set_xlabel('')
        ax2.set_ylabel('')
        ax2.set_title('Comparison Current and Previous Month')
        ax2.set_xticks(x)
        ax2.set_xticklabels(["Alkohol", "Fast Food", "gluecksspiel", "Tabakwaren"])
        ax2.legend()

        ax2.set_aspect('auto')

        canvas2 = FigureCanvasTkAgg(fig2, master=chart_frame_2)
        canvas2.draw()
        canvas_widget2 = canvas2.get_tk_widget()
        canvas_widget2.config(bg="white")
        canvas_widget2.grid(row=0, column=0)

    bad_stuff_list.clear()
    bad_stuff_values.clear()

    hos_df = pandas.read_csv("planista_database.csv")
    hos_df["date"] = pandas.to_datetime(hos_df["date"], format="%d.%m.%Y")

    hos_month_df = hos_df[hos_df["date"].dt.month == chosen_month]

    if chosen_month == 1:
        last_month = 12
    else:
        last_month = chosen_month - 1

    hos_last_month_df = hos_df[hos_df["date"].dt.month == last_month]

    hos_cat_sums = hos_month_df.groupby("category")["price"].sum()
    hos_last_month_cat_sums = hos_last_month_df.groupby("category")["price"].sum()

    alc_sum = hos_cat_sums.get("alkohol", 0)
    fastfood_sum = hos_cat_sums.get("fast food", 0)
    gambling_sum = hos_cat_sums.get("gluecksspiel", 0)
    tobacco_sum = hos_cat_sums.get("tabakwaren", 0)

    tupel_list = []

    if alc_sum:
        tupel_list.append(("Alkohol", alc_sum))

    if fastfood_sum:
        tupel_list.append(("Fast Food", fastfood_sum))

    if gambling_sum:
        tupel_list.append(("gluecksspiel", gambling_sum))

    if tobacco_sum:
        tupel_list.append(("Tabakwaren", tobacco_sum))

    hos_sum = alc_sum + gambling_sum + tobacco_sum + fastfood_sum
    tupel_list.sort(key=lambda x: x[1])

    for pair in tupel_list:
        bad_stuff_list.append(pair[0])
        bad_stuff_values.append(pair[1])

    chart_frame = tk.Frame(root)
    chart_frame.grid(row=row, column=column)

    fig, ax = plt.subplots(figsize=figsize)

    if bad_stuff_list:
        ax.pie(bad_stuff_values,
               labels=bad_stuff_list,
               colors=color_list,
               autopct=lambda p: f'{p * sum(bad_stuff_values) / 100 :.0f} EUR')
        ax.set_title(f"Hall of Shame {month_dict[chosen_month]} {current_year} - {round(hos_sum, 2)} EUR")

    else:
        ax.pie([1], labels=["No data"], colors=['gray'])
        ax.set_title(f"Hall of Shame {month_dict[chosen_month]} {current_year} - No data")

    ax.set_aspect('equal')

    fig.subplots_adjust(left=0.1, right=1.0, top=0.9, bottom=0.1)

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.bind("<Button-1>", lambda event: hos_bar_chart_window())
    canvas_widget.grid(row=row, column=column)


def open_cat_window(df, chosen_cat):
    local_cat_sum = sum(df['price'])

    cat_window = tk.Toplevel(main_window)
    cat_window.minsize(400, 500)
    cat_window.title(f" Category {chosen_cat.title()}")
    cat_window.config(bg="white")

    cat_frame = tk.Frame(cat_window, bg="white")
    cat_frame.grid(row=0, column=0)

    top_label = tk.Label(cat_frame,
                         text=f"All purchases for {chosen_cat.title()}",
                         bg="white",
                         font=BOLD_FONT,
                         fg=DARK_ORANGE_COLOR)

    top_label.grid(row=1, column=0, padx=20)

    sum_label = tk.Label(cat_frame,
                         text=f"Total sum: {local_cat_sum:.2f} EUR",
                         font=FONT,
                         bg="white",
                         fg=DARK_BLUE_COLOR)

    sum_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")

    empty_row = tk.Label(cat_frame, text="")
    empty_row.grid(row=3, column=0)

    label_row = 4
    for index, row in df.iterrows():
        raw_date = row['date'].date()
        cat_date = raw_date.strftime("%d.%m.%Y")
        raw_price = str(row['price']).replace(".", ",")
        if len(raw_price.split(",")[1]) == 1:
            raw_price = f"{raw_price}0"

        item_label = tk.Label(cat_frame, text=row['item'].title(), font=("open sans", 14), bg="white")
        item_label.grid(row=label_row, column=0, padx=20, sticky="w")

        price_label = tk.Label(cat_frame, text=f"{raw_price} EUR", font=("open sans", 14), bg="white")
        price_label.grid(row=label_row, column=1, padx=20, sticky="e")

        shop_label = tk.Label(cat_frame, text=row['shop'].title(), font=("open sans", 14), bg="white")
        shop_label.grid(row=label_row, column=2, padx=20, sticky="w")

        date_label = tk.Label(cat_frame, text=cat_date, font=("open sans", 14), bg="white")
        date_label.grid(row=label_row, column=3, padx=20, sticky="w")

        label_row += 1


def open_stats_window():
    """ opens the statistics window and creates several widgets"""
    global cat_dict, label_to_remove

    main_window.update_idletasks()

    overall_stats_df = pandas.read_csv("planista_database.csv")
    overall_stats_df["date"] = pandas.to_datetime(overall_stats_df["date"], format="%d.%m.%Y")
    overall_curr_month_df = overall_stats_df[overall_stats_df["date"].dt.month == current_month]
    overall_sum = round(sum(overall_stats_df["price"]), 2)
    sum_current_month = sum(overall_curr_month_df["price"])
    sum_last_month = sum(last_month_df["price"])

    def extract_shop_category(values_list, labels_list):
        sorted_labels = []
        sorted_values = []

        comb_name = "Other"
        comb_shop_perc = 0

        percentage = (sum(values_list) / 100) * 5

        for val, label in zip(values_list, labels_list):

            if val < percentage:
                comb_shop_perc += val
            else:
                sorted_labels.append(label)
                sorted_values.append(val)

        if comb_shop_perc > 0:
            sorted_labels.append(comb_name)
            sorted_values.append(round(comb_shop_perc))

        return sorted_values, sorted_labels

    def small_plt(root, value_list, label_list, title, row, column, orig_values, orig_labels):

        chart_frame = tk.Frame(root)
        chart_frame.grid(row=row, column=column)

        fig, ax = plt.subplots(figsize=(4, 3))

        ax.set_aspect('equal')
        ax.pie(value_list, labels=label_list, autopct="%1.1f%%", colors=color_list)
        ax.set_title(title)

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=row, column=column)

        canvas_widget.bind("<Button-1>", lambda event: plt_window_1(
            values=orig_values,
            labels=orig_labels,
            title=title))

        plt.close(fig)

    def reset_entries():
        global label_to_remove
        selected_month.set("")
        selected_cat_stats.set("")

        for label in label_to_remove:
            label.config(text="")

        total_purchases.config(text=f"Total purchases: {len(overall_stats_df['item'])}\n"
                                    f"Total cost: {overall_sum} EUR")

        new_cat_text = tk.Label(master=gui_frame_2,
                                text=f"All Transactions",
                                font=("open sans", 18, "bold"),
                                bg="white"
                                )
        new_cat_text.grid(row=4, column=1, pady=10)
        label_to_remove.append(new_cat_text)

        year_entry.delete(0, tk.END)
        year_entry.insert(0, str(current_year))

        extr_values, extr_labels = extract_shop_category(start_shop_sums.values, start_shop_sums.index)

        extr_labels = [label.title() for label in extr_labels]

        small_plt(gui_frame_2, extr_values, extr_labels,
                  "Overall Shops", 8, 0, start_shop_sums.values, start_shop_sums.index)

        extr_values2, extr_labels2 = extract_shop_category(start_cat_sums.values, start_cat_sums.index)

        extr_labels2 = [label.title() for label in extr_labels2]

        small_plt(gui_frame_2, extr_values2, extr_labels2,
                  "Overall Categories", 8, 2, start_cat_sums.values, start_cat_sums.index)

    def clear_year(event):
        """ clears the year entry widget """
        year_entry.delete(0, tk.END)
        year_entry.config(fg="black")

    def percentage_deviation(sum_curr, sum_last):
        try:
            perc_dev = round(sum_curr / (sum_last / 100) - 100, 2)
        except ZeroDivisionError:
            perc_dev = "100"

        return perc_dev

    def search_stats():
        global cat_dict, label_to_remove

        for label in label_to_remove:
            label.destroy()

        label_to_remove.clear()

        search_df = pandas.read_csv("planista_database.csv")

        try:
            chosen_month = int(selected_month.get())
        except ValueError:
            chosen_month = 0

        try:
            chosen_year = int(year_entry.get())
        except ValueError:
            chosen_year = 0

        chosen_cat = selected_cat_stats.get().lower()

        search_df["date"] = pandas.to_datetime(search_df["date"], format="%d.%m.%Y")

        entries_month = search_df[(search_df["date"].dt.month == chosen_month) &
                                  (search_df["date"].dt.year == chosen_year)]

        entries_year = search_df[search_df["date"].dt.year == chosen_year]

        entries_month_cat = search_df[(search_df["date"].dt.month == chosen_month) &
                                      (search_df["date"].dt.year == chosen_year) &
                                      (search_df["category"] == chosen_cat.lower())]

        for c in category_list:
            cat_df1 = search_df[search_df["category"] == c.lower()]
            cat_sum1 = cat_df1["price"].sum()
            cat_dict[c] = cat_sum1

        total_sum_per_month = sum(entries_month["price"])
        total_sum_per_year = sum(entries_year["price"])

        # wenn keine Kategorie gewaehlt wurde
        if not chosen_cat:

            shop_sums = entries_month.groupby("shop")["price"].sum()
            cat_sums = entries_month.groupby("category")["price"].sum()

            # when nothing was chosen
            if chosen_month == 0 and chosen_year == 0 and not chosen_cat:

                overall_shopsums = search_df.groupby("shop")["price"].sum()
                overall_catsums = search_df.groupby("category")["price"].sum()
                perc_dev = percentage_deviation(sum_current_month, sum_last_month)
                total_purchases.config(text=f"Total purchases: {len(overall_stats_df['price'])}\n"
                                            f"Total cost: {round(sum(overall_stats_df['price']), 2):.2f} EUR\n"
                                            f"Difference last month: {perc_dev} %")

                text_label(gui_frame_2, label_to_remove, 0, 0, 0)

                extr_values, extr_labels = extract_shop_category(overall_shopsums.values, overall_shopsums.index)

                extr_labels = [label.title() for label in extr_labels]

                small_plt(gui_frame_2, extr_values, extr_labels,
                          f"Overall Shops", 8, 0,
                          overall_shopsums.values, overall_shopsums.index)

                extr_values2, extr_labels2 = extract_shop_category(overall_catsums.values, overall_catsums.index)

                extr_labels2 = [label.title() for label in extr_labels2]

                small_plt(gui_frame_2, extr_values2, extr_labels2,
                          f"Overall Categories", 8, 2,
                          overall_catsums.values, overall_catsums.index)

            # wenn Monat gewaehlt wurde
            elif chosen_month > 0 and chosen_year != 0:
                sum_month_before_chosen_month_df = search_df[search_df["date"].dt.month == chosen_month - 1 if not chosen_month == 1 else chosen_month + 11]
                sum_month_before_chosen_month = sum(sum_month_before_chosen_month_df["price"])

                perc_dev_month = percentage_deviation(chosen_month, sum_month_before_chosen_month)
                total_purchases.config(text=f"Total purchases: {len(entries_month)}\n"
                                            f"Total cost: {round(total_sum_per_month, 2):.2f} EUR\n"
                                            f"Difference last month: {perc_dev_month} %")

                text_label(gui_frame_2, label_to_remove, 0, chosen_month, chosen_year)

                extr_values, extr_labels = extract_shop_category(shop_sums.values, shop_sums.index)

                extr_labels = [label.title() for label in extr_labels]

                small_plt(gui_frame_2, extr_values, extr_labels,
                          f"Shops for {month_dict[chosen_month]} {chosen_year}", 8, 0,
                          shop_sums.values, shop_sums.index)

                hall_of_shame_plt(stats_window, 9, 0, (4, 3), chosen_month)

                extr_values2, extr_labels2 = extract_shop_category(cat_sums.values, cat_sums.index)

                extr_labels2 = [label.title() for label in extr_labels2]

                small_plt(gui_frame_2, extr_values2, extr_labels2,
                          f"Categories for {month_dict[chosen_month]} {chosen_year}", 8, 2,
                          cat_sums.values, cat_sums.index)

            # wenn kein Jahr gewählt wurde
            elif chosen_year == 0 or chosen_month == 0 and chosen_year == 0:
                total_purchases.config(text=f"Total purchases: {len(search_df['category'])}\n"
                                            f"Total cost: {round(sum(search_df['price']), 2):.2f} EUR")

                text_label(gui_frame_2, label_to_remove, 0, 0, 0)

                values1, labels1 = extract_shop_category(start_shop_sums.values, start_shop_sums.index)

                labels1 = [label.title() for label in labels1]

                small_plt(gui_frame_2, values1, labels1,
                          "Overall Shops", 8, 0, start_shop_sums.values, start_shop_sums.index)

                values2, labels2 = extract_shop_category(start_cat_sums.values, start_cat_sums.index)

                labels2 = [label.title() for label in labels2]

                small_plt(gui_frame_2, values2, labels2,
                          "Overall Categories", 8, 2, start_cat_sums.values, start_cat_sums.index)

            # wenn kein Monat gewaehlt wurde
            else:
                shop_sums = entries_year.groupby("shop")["price"].sum()
                cat_sums = entries_year.groupby("category")["price"].sum()
                total_purchases.config(text=f"Total purchases: {len(entries_year)}\n"
                                            f"Total cost: {round(total_sum_per_year, 2):.2f} EUR")

                text_label(gui_frame_2, label_to_remove, 0, 0, chosen_year)

                extr_values, extr_labels = extract_shop_category(shop_sums.values, shop_sums.index)

                extr_labels = [label.title() for label in extr_labels]

                small_plt(gui_frame_2, extr_values, extr_labels,
                          f"Shops for {chosen_year}", 8, 0, shop_sums.values, shop_sums.index)

                extr_values2, extr_labels2 = extract_shop_category(cat_sums.values, cat_sums.index)

                extr_labels2 = [label.title() for label in extr_labels2]

                small_plt(gui_frame_2, extr_values2, extr_labels2,
                          f"Categories for {chosen_year}", 8, 2, cat_sums.values, cat_sums.index)

        # wenn Kategorie gewaehlt wurde
        else:

            cat_df2 = search_df[search_df["category"] == chosen_cat]
            cat_df_month = cat_df2[(cat_df2["date"].dt.month == chosen_month) &
                                   (cat_df2["date"].dt.year == chosen_year)]
            cat_df_year = cat_df2[cat_df2["date"].dt.year == chosen_year]
            open_cat_window(cat_df_month, chosen_cat)
            # when nothing was chosen
            if chosen_month == 0 and not chosen_year:
                # cat_df3 = overall_stats_df[overall_stats_df['category'] == chosen_cat]

                cat_sums = sum(cat_df2['price'])

                total_purchases.config(text=f"Total purchases: {len(cat_df2['price'])}\n"
                                            f"Total cost: {cat_sums:.2f} EUR\n",
                                       font=BOLD_FONT)

                text_label(gui_frame_2, label_to_remove, chosen_cat.title(), chosen_month, current_year)

            # wenn Kategorie und Monat gewaehlt wurden
            elif chosen_month > 0:

                cat_sums = entries_month_cat.groupby("category")["price"].sum()
                cat_df_last_month = last_month_df[last_month_df['category'] == chosen_cat]
                cat_sum_lm = sum(cat_df_last_month['price'])
                cat_perc_1 = percentage_deviation(sum(cat_sums), cat_sum_lm)
                total_purchases.config(text=f"Total purchases: {len(cat_df_month)}\n"
                                            f"Total cost: {sum(cat_sums):.2f} EUR\n"
                                            f"Difference last month: {cat_perc_1} %",
                                       font=BOLD_FONT)

                text_label(gui_frame_2, label_to_remove, chosen_cat.title(), chosen_month, current_year)

            # wenn Kategorie aber kein Monat gewaehlt wurde
            else:
                cat_sums = cat_df_year.groupby("category")["price"].sum()
                total_purchases.config(text=f"Total purchases: {len(cat_df_year)}\n"
                                            f"Total cost: {sum(cat_sums):.2f} EUR",
                                       font=BOLD_FONT)

                text_label(gui_frame_2, label_to_remove, chosen_cat.title(), 0, current_year)

    stats_window = tk.Toplevel(main_window)
    stats_window.minsize(900, 800)
    stats_window.config(bg="white")
    stats_window.title("PLANISTA Statistics")

    selected_month = tk.StringVar()
    selected_cat_stats = tk.StringVar()

    gui_frame_2 = tk.Frame(stats_window, bg="white")
    gui_frame_2.grid(row=0, column=0)

    logo_label_2 = tk.Label(gui_frame_2, image=logo)
    logo_label_2.grid(row=0, column=1)

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
                             command=reset_entries,
                             )
    reset_button.grid(row=3, column=2)

    text_label(gui_frame_2, label_to_remove, 0, current_month, current_year)

    perc_dev = percentage_deviation(sum_current_month, sum_last_month)

    total_purchases = tk.Label(master=gui_frame_2,
                               text=f"Total purchases: {len(overall_curr_month_df)}\n"
                                    f"Total cost: {sum_current_month :.2f} EUR\n"
                                    f"Difference last month: {perc_dev} %",
                               font=BOLD_FONT,
                               bg="white"
                               )
    total_purchases.grid(row=8, column=1, padx=20, pady=10)

    start_shop_sums = overall_curr_month_df.groupby("shop")["price"].sum()
    start_cat_sums = overall_curr_month_df.groupby("category")["price"].sum()

    values, labels = extract_shop_category(start_shop_sums.values, start_shop_sums.index)

    labels = [label.title() for label in labels]

    small_plt(gui_frame_2, values, labels,
              f"Shops for {month_dict[current_month]} {current_year}", 8, 0,
              start_shop_sums.values, start_shop_sums.index)

    hall_of_shame_plt(stats_window, 9, 0, (4, 3), current_month)

    values, labels = extract_shop_category(start_cat_sums.values, start_cat_sums.index)

    labels = [label.title() for label in labels]

    small_plt(gui_frame_2, values, labels,
              f"Categories for {month_dict[current_month]} {current_year}", 8, 2,
              start_cat_sums.values, start_cat_sums.index)


# MAIN WINDOW UI

main_window = tk.Tk()
main_window.minsize(600, 600)
main_window.config(bg="white")
main_window.title("PLANISTA")

gui_frame = tk.Frame(main_window)
gui_frame.grid(row=0, column=0)
gui_frame.config(bg="white")

image = Image.open("logo.png")
logo = ImageTk.PhotoImage(image)

selected_category = tk.StringVar()
selected_category.set("---")

selected_shop = tk.StringVar()
selected_shop.set("---")

logo_label = tk.Label(gui_frame, image=logo)
logo_label.grid(row=0, column=2, columnspan=3, pady=20)

item_text = tk.Label(master=gui_frame, text="Item", font=FONT, bg="white")
item_text.grid(row=1, column=1)

cost_text = tk.Label(master=gui_frame, text="Cost", font=("open sans", 14), bg="white")
cost_text.grid(row=1, column=2)

category_text = tk.Label(master=gui_frame, text="Category", font=FONT, bg="white")
category_text.grid(row=1, column=4)

shop_text = tk.Label(master=gui_frame, text="Shop", font=FONT, bg="white")
shop_text.grid(row=1, column=3)

date_text = tk.Label(master=gui_frame, text="Date (dd.mm.yyyy)", font=FONT, bg="white")
date_text.grid(row=1, column=7)

if last_entry_item:
    last_entry_text = tk.Label(master=gui_frame,
                               text=f"Your last entry: {last_entry_item.title()} - "
                               f"{last_entry_price:.2f} EUR - "
                               f"{last_entry_date}",
                               font=FONT,
                               bg="white"
                               )
    last_entry_text.grid(row=4, column=2, columnspan=3)
else:
    last_entry_text = tk.Label(master=gui_frame,
                               text="",
                               font=FONT,
                               bg="white"
                               )
    last_entry_text.grid(row=4, column=2, columnspan=3)

item_entry = tk.Entry(master=gui_frame, justify="right", font=FONT, bg=PAPER_COLOR)
item_entry.grid(row=2, column=1, padx=10)

cost_entry = tk.Entry(master=gui_frame, justify="right", font=("courier", 20), bg=PAPER_COLOR, width=8)
cost_entry.grid(row=2, column=2)

date_entry = tk.Entry(master=gui_frame, font=("courier", 15), justify="right", bg=PAPER_COLOR, width=14)
date_entry.grid(row=2, column=7, padx=10)
date_entry.insert(1, current_date)

save_button = tk.Button(master=gui_frame,
                        text="SAVE",
                        font=FONT,
                        command=save_data,
                        bg=GREEN_COLOR,
                        width=20,
                        )
save_button.grid(row=3, column=2, pady=40, columnspan=3)

stats_button = tk.Button(master=gui_frame,
                         text="Statistics",
                         font=FONT,
                         command=open_stats_window,
                         bg=BLUE_COLOR,
                         width=25,
                         )
stats_button.grid(row=5, column=2, pady=50, columnspan=3)

# fixed_button = tk.Button(text="Add fixed costs",
#                          bg=red_color)
# fixed_button.grid(row=5, column=3)

drop_down_cat = tk.OptionMenu(gui_frame, selected_category, *category_list)
drop_down_cat.config(bg=ORANGE_COLOR, font=FONT, width=6)
drop_down_cat.grid(row=2, column=4)

menu_3 = gui_frame.nametowidget(drop_down_cat.menuname)
menu_3.config(font=FONT)

drop_down_shop = tk.OptionMenu(gui_frame, selected_shop, *shop_list)
drop_down_shop.config(bg=ORANGE_COLOR, font=FONT, width=6)
drop_down_shop.grid(row=2, column=3, padx=10)

menu_4 = gui_frame.nametowidget(drop_down_shop.menuname)
menu_4.config(font=FONT)

hall_of_shame_plt(main_window, 7, 0, (5, 4), current_month)

update_last_entry()

main_window.mainloop()
