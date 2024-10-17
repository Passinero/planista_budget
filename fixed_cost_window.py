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

    def edit_fixed():

        try:
            fixed_dataframe = pandas.read_csv("fixed_cost.csv")
            add_more_button.destroy()

            curr_row = 3
            for widget in entry_list:
                widget[0].destroy()
                widget[1].destroy()

            for index, row in fixed_dataframe.iterrows():
                new_cat_entry = tk.Entry(master=fixed_window, font=FONT)
                new_cat_entry.grid(row=curr_row, column=0)
                new_cat_entry.insert(0, row.category)

                new_price_entry = tk.Entry(master=fixed_window, font=FONT, width=8)
                new_price_entry.grid(row=curr_row, column=1)
                new_price_entry.insert(0, row.price)

                curr_row += 1

        except FileNotFoundError:
            messagebox.showerror("File not found", "You haven't added fixed costs yet")
            pass

    def add_more_entries():
        curr_row = len(entry_list) + 4

        new_cat_entry = tk.Entry(master=fixed_window, font=FONT, bg=PAPER_COLOR)
        new_cat_entry.grid(row=curr_row, column=0, padx=20)

        new_price_entry = tk.Entry(master=fixed_window, font=FONT, bg=PAPER_COLOR, width=8)
        new_price_entry.grid(row=curr_row, column=1, sticky="w")
        entry_list.append((new_cat_entry, new_price_entry))

        add_more_button.grid(row=curr_row + 4, column=0, padx=20, pady=10)

    def save_fixed_data():
        correct_data = True

        new_data_fixed = {"category": [],
                          "price": [],
                          }

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

        if correct_data:
            new_df = pandas.DataFrame(new_data_fixed)
            new_df.to_csv("fixed_cost.csv", index=False)
            messagebox.showinfo("Success", "Data added")
            fixed_window.destroy()

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
    top_label.grid(row=0, column=0, padx=20, columnspan=3)

    rent_entry = tk.Entry(master=fixed_window, font=FONT, bg=PAPER_COLOR)
    rent_entry.grid(row=3, column=0, padx=10)
    rent_entry.insert(0, "Rent")

    rent_price_entry = tk.Entry(fixed_window, font=FONT, width=8, bg=PAPER_COLOR)
    rent_price_entry.grid(row=3, column=1, sticky="w")

    elec_entry = tk.Entry(fixed_window, font=FONT, bg=PAPER_COLOR)
    elec_entry.grid(row=4, column=0)
    elec_entry.insert(0, "Electricity")

    elec_price_entry = tk.Entry(fixed_window, font=FONT, width=8, bg=PAPER_COLOR)
    elec_price_entry.grid(row=4, column=1, sticky="w")

    telephone_entry = tk.Entry(master=fixed_window, font=FONT, bg=PAPER_COLOR)
    telephone_entry.grid(row=5, column=0, padx=20)
    telephone_entry.insert(0, "Telephone / Internet")

    tel_price_entry = tk.Entry(fixed_window, font=FONT, width=8, bg=PAPER_COLOR)
    tel_price_entry.grid(row=5, column=1, sticky="w")

    transport_entry = tk.Entry(master=fixed_window, font=FONT, bg=PAPER_COLOR)
    transport_entry.grid(row=6, column=0, padx=20)
    transport_entry.insert(0, "Public Transport")

    trans_price_entry = tk.Entry(fixed_window, font=FONT, width=8, bg=PAPER_COLOR)
    trans_price_entry.grid(row=6, column=1, sticky="w")

    insurance_entry = tk.Entry(master=fixed_window, font=FONT, bg=PAPER_COLOR)
    insurance_entry.grid(row=7, column=0, padx=20)
    insurance_entry.insert(0, "Insurance")

    ins_price_entry = tk.Entry(fixed_window, font=FONT, width=8, bg=PAPER_COLOR)
    ins_price_entry.grid(row=7, column=1, sticky="w")

    streaming_entry = tk.Entry(master=fixed_window, font=FONT, bg=PAPER_COLOR)
    streaming_entry.grid(row=8, column=0, padx=20)
    streaming_entry.insert(0, "Streaming")

    stream_price_entry = tk.Entry(fixed_window, font=FONT, width=8, bg=PAPER_COLOR)
    stream_price_entry.grid(row=8, column=1, sticky="w")

    entry_list = [(rent_entry, rent_price_entry), (elec_entry, elec_price_entry), (telephone_entry, tel_price_entry),
                  (insurance_entry, ins_price_entry), (transport_entry, trans_price_entry),
                  (streaming_entry, stream_price_entry)]

    save_button_2 = tk.Button(master=fixed_window, text="SAVE", font=FONT, bg=GREEN_COLOR, command=save_fixed_data)
    save_button_2.grid(row=1, column=0, padx=20, pady=10, sticky="w")

    edit_fixed_button = tk.Button(master=fixed_window, text="Edit", font=FONT, bg=ORANGE_COLOR, command=edit_fixed)
    edit_fixed_button.grid(row=1, column=1, padx=20, pady=20, sticky="w")

    empty_row = tk.Label(fixed_window, text="", font=FONT, bg="white")
    empty_row.grid(row=9, column=0)

    add_more_button = tk.Button(master=fixed_window, text="+ add more", command=add_more_entries, font=FONT)
    add_more_button.grid(row=10, column=0)
