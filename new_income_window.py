import pandas
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

CURRENT_DATE = datetime.today().strftime("%d.%m.%Y")
FONT = ("open sans", 13)
LARGE_FONT = ("open sans", 18)

PAPER_COLOR = "#fbfbfb"
ORANGE_COLOR = "#fcd9a8"
GREEN_COLOR = "#D9EDBF"
ROSA_COLOR = "#FFD7C4"


def open_income_window(main_window):

    entry_list = []
    tupel_list = []
    save_tupel_list = []

    def change_entry_color(event):
        event.widget.config(bg=PAPER_COLOR)

    def save_data():
        new_data = {"title": [],
                    "amount": [],
                    "date": []
                    }

        for tupel in save_tupel_list:
            item = tupel[0].get()
            amount = tupel[1].get()
            date = tupel[2].get()

            if item and amount and date:
                new_data['title'].append(item)
                new_data['amount'].append(amount)
                new_data['date'].append(date)

        with open("income_database.csv", mode="w") as file1:
            file1.write(f"title,amount,date\n")

        new_income_df = pandas.DataFrame(new_data)
        new_income_df.to_csv("income_database.csv", mode="a", index=False, header=False)
        messagebox.showinfo("Success", "Data saved successfully")
        income_window.destroy()
        open_income_window(main_window)

    def label_output(current_row, date=None, bg=None):

        # def clear_entry(event):
        #     event.widget.config(bg=PAPER_COLOR)

        new_item_entry = tk.Entry(master=income_window, font=FONT, width=20, bg=PAPER_COLOR)
        new_item_entry.grid(row=current_row, column=0, padx=20, pady=2, sticky="w")

        new_amount_entry = tk.Entry(master=income_window, font=FONT, width=10, bg=PAPER_COLOR, justify="right")
        new_amount_entry.grid(row=current_row, column=1, padx=20, pady=2)

        new_date_entry = tk.Entry(master=income_window, font=FONT, width=10, bg=PAPER_COLOR, justify="right")
        new_date_entry.grid(row=current_row, column=2, padx=20, pady=2, sticky="w")

        if date:
            new_date_entry.insert(0, date)

        if bg:
            new_item_entry.config(bg=bg)
            new_item_entry.bind("<Button-1>", change_entry_color)
            new_amount_entry.config(bg=bg)
            new_amount_entry.bind("<Button-1>", change_entry_color)
            new_date_entry.config(bg=bg)
            new_date_entry.bind("<Button-1>", change_entry_color)

        entry_list.append(new_item_entry)
        save_tupel_list.append((new_item_entry, new_amount_entry, new_date_entry))

        return new_item_entry, new_amount_entry, new_date_entry

    def additional_entry():

        label_output(len(entry_list) + 4, date=CURRENT_DATE, bg=GREEN_COLOR)

        plus_one_button.grid(row=len(entry_list) + 6, column=0, padx=20, pady=20, sticky="w")
        save_button.grid(row=len(entry_list) + 7)

    try:
        with open("income_database.csv", mode="r") as file:
            pass

    except FileNotFoundError:
        with open("income_database.csv", mode="w") as file:
            file.write(f"title,amount,date\n")
            print("File income_database.csv created")

    income_df = pandas.read_csv("income_database.csv")
    for index, row in income_df.iterrows():
        tupel_list.append((row.title, row.amount, row.date))

    len_income_db = len(tupel_list)

    # USER INTERFACE
    income_window = tk.Toplevel(main_window)
    income_window.minsize(500, 500)
    income_window.title("Add your Income")
    income_window.config(bg="white")

    header = tk.Label(master=income_window,
                      text=f"Add/Edit your Income",
                      font=LARGE_FONT,
                      bg="white",
                      fg=ORANGE_COLOR,
                      )
    header.grid(row=0, column=0, padx=20, pady=20, sticky="w")

    item_text = tk.Label(master=income_window, text="Source", font=FONT, bg="white")
    item_text.grid(row=1, column=0, padx=30, pady=10, sticky="w")

    amount_text = tk.Label(master=income_window, text="Amount (EUR)", font=FONT, bg="white")
    amount_text.grid(row=1, column=1, pady=10, padx=50, sticky="w")

    date_text = tk.Label(master=income_window, text="Date", font=FONT, bg="white")
    date_text.grid(row=1, column=2, pady=10, padx=50, sticky="w")

    curr_row = 2
    i = 0

    for row in range(len_income_db):

        entry_tupel = label_output(curr_row)

        try:
            entry_tupel[0].insert(0, tupel_list[i][0])
            entry_tupel[1].insert(0, tupel_list[i][1])
            entry_tupel[2].insert(0, tupel_list[i][2])
        except IndexError:
            pass

        curr_row += 1
        i += 1

    label_output(len(entry_list) + 3, date=CURRENT_DATE, bg=GREEN_COLOR)

    plus_one_button = tk.Button(master=income_window,
                                text="+",
                                font=("open sans", 12),
                                width=19,
                                command=additional_entry,
                                )

    plus_one_button.grid(row=len(entry_list) + 4, column=0, padx=20, pady=20, columnspan=2, sticky="w")

    save_button = tk.Button(master=income_window,
                            text="Save",
                            font=FONT,
                            bg=GREEN_COLOR,
                            width=19,
                            command=save_data,
                            )
    save_button.grid(row=len(entry_list) + 5, column=0, padx=20, pady=10, sticky="w")
