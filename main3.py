# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox
import pandas
from datetime import date
from PIL import Image, ImageTk

from lists import category_list, shop_list
from income_window import open_income_window
from fixed_cost_window import open_fixed_window
from update_last_entry import update_last_entry
from statistics_window import open_statistics
from hall_of_shame import hall_of_shame_plt


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

fixed_costs = 0

category_list = category_list
shop_list = shop_list

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

try:
    fixed_df = pandas.read_csv("fixed_cost.csv")
    fixed_costs = sum(fixed_df['price'])

except FileNotFoundError:
    pass


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

    new_data_save = pandas.DataFrame({"item": [item],
                                      "shop": [shop],
                                      "category": [category],
                                      "price": [price],
                                      "date": [curr_date],
                                      })

    new_data_save.to_csv("planista_database.csv", mode="a", index=False, header=False)

    item_entry.delete(0, tk.END)
    cost_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    date_entry.insert(1, current_date)
    selected_category.set("---")
    selected_shop.set("---")

    hall_of_shame_plt(main_window, 7, 0, (5, 4), current_month,
                      current_year, bad_stuff_list, bad_stuff_values, main_window)

    update_last_entry(last_entry_text)
    main_window.update()
    messagebox.showinfo("Data saved successfully", "Your data was saved")


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
logo_label.grid(row=0, column=2, pady=20, sticky="w")

item_text = tk.Label(master=gui_frame, text="Item", font=FONT, bg="white")
item_text.grid(row=1, column=0)

cost_text = tk.Label(master=gui_frame, text="Cost", font=("open sans", 14), bg="white")
cost_text.grid(row=1, column=1)

category_text = tk.Label(master=gui_frame, text="Category", font=FONT, bg="white")
category_text.grid(row=1, column=3, pady=10)

shop_text = tk.Label(master=gui_frame, text="Shop", font=FONT, bg="white")
shop_text.grid(row=1, column=2, pady=10)

date_text = tk.Label(master=gui_frame, text="Date (dd.mm.yyyy)", font=FONT, bg="white")
date_text.grid(row=1, column=4)

if last_entry_item:
    last_entry_text = tk.Label(master=gui_frame,
                               text=f"Your last entry: {last_entry_item.title()} - "
                               f"{last_entry_price:.2f} EUR - "
                               f"{last_entry_date}",
                               font=FONT,
                               bg="white"
                               )
    last_entry_text.grid(row=4, column=2, columnspan=1)
else:
    last_entry_text = tk.Label(master=gui_frame,
                               text="",
                               font=FONT,
                               bg="white"
                               )
    last_entry_text.grid(row=4, column=2)

item_entry = tk.Entry(master=gui_frame, justify="right", font=("open sans", 18), bg=PAPER_COLOR)
item_entry.grid(row=2, column=0, padx=20)

cost_entry = tk.Entry(master=gui_frame, justify="right", font=("courier", 18), bg=PAPER_COLOR, width=8)
cost_entry.grid(row=2, column=1)

date_entry = tk.Entry(master=gui_frame, font=("courier", 15), justify="right", bg=PAPER_COLOR, width=14)
date_entry.grid(row=2, column=4, padx=20)
date_entry.insert(1, current_date)

save_button = tk.Button(master=gui_frame,
                        text="SAVE",
                        font=FONT,
                        command=save_data,
                        bg=GREEN_COLOR,
                        width=20
                        )
save_button.grid(row=3, column=2, pady=40)

fixed_button = tk.Button(master=gui_frame,
                         text="Add fixed costs",
                         bg=RED_COLOR,
                         font=FONT,
                         command=lambda: open_fixed_window(main_window),
                         )
fixed_button.grid(row=3, column=3, pady=50)

stats_button = tk.Button(master=gui_frame,
                         text="Statistics",
                         font=FONT,
                         command=lambda: open_statistics(main_window, last_month_df, cat_dict, label_to_remove,
                                                         bad_stuff_list, bad_stuff_values),
                         bg=BLUE_COLOR,
                         width=20
                         )
stats_button.grid(row=5, column=2, pady=50)

add_income_button = tk.Button(master=gui_frame,
                              text="Add Income",
                              font=FONT,
                              bg=YELLOW_COLOR,
                              command=lambda: open_income_window(main_window),
                              )
add_income_button.grid(row=3, column=1, sticky="e")

drop_down_cat = tk.OptionMenu(gui_frame, selected_category, *category_list)
drop_down_cat.config(bg=ORANGE_COLOR, font=FONT, width=10)
drop_down_cat.grid(row=2, column=3, padx=15)

menu_3 = gui_frame.nametowidget(drop_down_cat.menuname)
menu_3.config(font=FONT)

drop_down_shop = tk.OptionMenu(gui_frame, selected_shop, *shop_list)
drop_down_shop.config(bg=ORANGE_COLOR, font=FONT, width=10)
drop_down_shop.grid(row=2, column=2, padx=15)

menu_4 = gui_frame.nametowidget(drop_down_shop.menuname)
menu_4.config(font=FONT)

hall_of_shame_plt(main_window, 7, 0, (5, 4),
                  current_month, current_year, bad_stuff_list, bad_stuff_values, main_window)

update_last_entry(last_entry_text)

main_window.mainloop()
