import pandas
import tkinter as tk
from tkinter import messagebox

FONT = ("open sans", 15)
BOLD_FONT = ("open sans", 18, "bold")

PAPER_COLOR = "#fbfbfb"
ORANGE_COLOR = "#fcd9a8"
BLUE_COLOR = "#d0eef8"
GREEN_COLOR = "#D9EDBF"
DARK_ORANGE_COLOR = "#FFCF81"


def open_fixed_window(root):

    def clear_entries(event):
        event.widget.delete(0, tk.END)

    def add_more_entries():
        curr_row_add = len(entry_list) + 4

        new_cat_entry = tk.Entry(master=fixed_window, font=FONT, bg=PAPER_COLOR)
        new_cat_entry.grid(row=curr_row_add, column=0, padx=20)
        new_cat_entry.bind("<Button-1>", clear_entries)

        new_price_entry_add = tk.Entry(master=fixed_window, font=FONT, bg=PAPER_COLOR, width=8)
        new_price_entry_add.grid(row=curr_row_add, column=1, sticky="w")
        new_price_entry_add.bind("<Button-1>", clear_entries)
        entry_list.append((new_cat_entry, new_price_entry_add))

        add_more_button.grid(row=curr_row_add + 4, column=0, padx=20)

    def save_fixed_data(status):
        correct_data = True

        new_data_fixed = {"category": [],
                          "price": [],
                          }

        if status == "new":
            for entries in entry_list:
                cat_value = entries[0].get()
                price_value = entries[1].get().replace(",", ".")

                if cat_value and price_value:
                    new_data_fixed['category'].append(cat_value)
                    new_data_fixed['price'].append(price_value)

                elif cat_value or price_value:
                    correct_data = False
                    messagebox.showerror("Something went wrong", "Both category and price have to be filled out")
                    break
        else:
            for entries in edit_entry_list:
                cat_value = entries[0].get()
                price_value = entries[1].get().replace(",", ".")

                if cat_value and price_value:
                    new_data_fixed['category'].append(cat_value)
                    new_data_fixed['price'].append(price_value)

                elif cat_value or price_value:
                    correct_data = False
                    messagebox.showerror("Something went wrong", "Both category and price have to be filled out")
                    break

        if correct_data:
            new_df = pandas.DataFrame(new_data_fixed)
            new_df.to_csv("fixed_cost.csv", index=False)
            messagebox.showinfo("Success", "Data added")
            fixed_window.destroy()
            open_fixed_window(root)

    entry_list = []
    edit_entry_list = []

    fixed_window = tk.Toplevel(root)
    fixed_window.minsize(400, 500)
    fixed_window.title("Add your fixed costs")
    fixed_window.config(bg="white")

    top_label = tk.Label(fixed_window,
                         text="Add your fixed costs below:",
                         fg=DARK_ORANGE_COLOR,
                         bg="white",
                         font=BOLD_FONT,
                         )
    top_label.grid(row=0, column=0, padx=20, columnspan=3, pady=20)

    try:
        fixed_df = pandas.read_csv("fixed_cost.csv")
        curr_row = 3
        for index, row in fixed_df.iterrows():
            new_entry = tk.Entry(master=fixed_window, font=FONT, bg=PAPER_COLOR)
            new_entry.grid(row=curr_row, column=0, padx=15)
            new_entry.insert(0, row.category)
            new_entry.bind("<Button-1>", clear_entries)

            new_price_entry = tk.Entry(fixed_window, font=FONT, width=8, bg=PAPER_COLOR, justify="right")
            new_price_entry.grid(row=curr_row, column=1, sticky="w")
            new_price_entry.insert(0, row.price)

            entry_list.append((new_entry, new_price_entry))

            curr_row += 1

    except FileNotFoundError:
        empty_entry = tk.Entry(master=fixed_window, font=FONT, bg=PAPER_COLOR)
        empty_entry.grid(row=3, column=0, padx=15)

        empty_price_entry = tk.Entry(master=fixed_window, width=8, font=FONT, bg=PAPER_COLOR)
        empty_price_entry.grid(row=3, column=1, sticky="w")

        entry_list.append((empty_entry, empty_price_entry))

    save_button_2 = tk.Button(master=fixed_window,
                              text="SAVE",
                              font=FONT,
                              bg=GREEN_COLOR,
                              command=lambda: save_fixed_data("new")
                              )
    save_button_2.grid(row=1, column=0, padx=20, pady=10, sticky="w")

    name_label = tk.Label(master=fixed_window, text="Name", font=FONT, bg="white")
    name_label.grid(row=2, column=0, padx=15, pady=15, sticky="w")

    cost_label = tk.Label(master=fixed_window, text="Cost", font=FONT, bg="white")
    cost_label.grid(row=2, column=1, pady=15, sticky="w")

    empty_row = tk.Label(fixed_window, text="", font=FONT, bg="white")
    empty_row.grid(row=9, column=0)

    add_more_button = tk.Button(master=fixed_window, text="+ add more", command=add_more_entries, font=FONT)
    add_more_button.grid(row=10, column=0)
