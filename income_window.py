import pandas
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

CURRENT_DATE = datetime.today().strftime("%d.%m.%Y")
FONT = ("open sans", 15)

entry_list = []
widget_list = []


def open_income_window(root):
    new_income_data = {"title": [],
                       "amount": [],
                       "date": []
                       }

    def label_widget_output(widget):

        entry_list.clear()
        widget_list.clear()

        dataframe = pandas.read_csv("income_database.csv")

        curr_row = 5

        if widget == "entry":
            for index, row in dataframe.iterrows():
                title_entry = tk.Entry(master=income_win, font=FONT)
                title_entry.grid(row=curr_row, column=0, padx=20, sticky="w")
                title_entry.insert(0, row.title.title())
                widget_list.append(title_entry)

                amount_entry = tk.Entry(master=income_win, font=FONT)
                amount_entry.grid(row=curr_row, column=1, padx=20, sticky="e")
                amount_entry.insert(0, row.amount)
                widget_list.append(amount_entry)

                date_entry = tk.Entry(master=income_win, font=FONT)
                date_entry.grid(row=curr_row, column=2, padx=20, sticky="w")
                date_entry.insert(0, row.date)
                widget_list.append(date_entry)

                entry_list.append((title_entry, amount_entry, date_entry))

                curr_row += 1

        else:
            income_df = pandas.read_csv("income_database.csv")
            curr_row = 5
            for index, row in income_df.iterrows():
                title_label = tk.Label(master=income_win, text=f"{row.title.title()}", font=FONT, bg="white")
                title_label.grid(row=curr_row, column=0, padx=20, sticky="w")
                text_labels.append(title_label)

                amount_label = tk.Label(master=income_win, text=f"{row.amount} EUR", font=FONT, bg="white")
                amount_label.grid(row=curr_row, column=1, padx=20, sticky="e")
                text_labels.append(amount_label)

                date_label = tk.Label(master=income_win, text=f"{row.date}", font=FONT, bg="white")
                date_label.grid(row=curr_row, column=2, padx=20, sticky="e")
                text_labels.append(date_label)

                curr_row += 1

        return curr_row

    def edit_entries():

        def save_new_data():
            correct_data = True
            new_data = {"title": [],
                        "amount": [],
                        "date": []
                        }

            for entries in entry_list:
                title_value = entries[0].get()
                amount_value = entries[1].get()
                date_value = entries[2].get()

                if title_value and amount_value and date_value:
                    new_data['title'].append(title_value)
                    new_data['amount'].append(amount_value)
                    new_data['date'].append(date_value)

                else:
                    correct_data = False
                    messagebox.showerror("Something went wrong", "Both category and price have to be filled out")
                    break

            if correct_data:
                new_df = pandas.DataFrame(new_data)
                new_df.to_csv("income_database.csv", index=False)
                messagebox.showinfo("Success", "Data saved")

                for widget in widget_list:
                    widget.destroy()

                save_button2.destroy()

                label_widget_output("label")

        for label in text_labels:
            label.destroy()

        try:
            row = label_widget_output("entry")

            save_button2 = tk.Button(master=income_win,
                                     text="Save",
                                     font=FONT,
                                     command=save_new_data,
                                     bg="#D9EDBF"
                                     )
            save_button2.grid(row=row + 1, column=1, pady=20)

        except FileNotFoundError:
            messagebox.showerror("Error", "No data found")
            return

    def save_income_data(status):

        if status == "new":
            correct_data = False
            title = title_entry.get()
            amount = amount_entry.get()
            if "," in amount:
                amount = amount.replace(",", ".")
            inc_date = inc_date_entry.get()

            title_entry.delete(0, tk.END)
            amount_entry.delete(0, tk.END)

            if title and amount and inc_date:
                new_income_data["title"].append(title)
                new_income_data["amount"].append(amount)
                new_income_data["date"].append(inc_date)

                correct_data = True

            elif title or amount or inc_date:
                messagebox.showerror("Data missing", "Please insert title, amount and date")
                return

            try:
                new_income_df = pandas.DataFrame(new_income_data)
                if correct_data:
                    new_income_df.to_csv("income_database.csv", mode="a", index=False, header=False)
                    messagebox.showinfo("Success", "Data saved successfully")
                    income_win.destroy()
                    open_income_window(root)

            except FileNotFoundError:
                income_df_2 = pandas.DataFrame(new_income_data)
                income_df_2.to_csv("income_database.csv", mode="a", index=False, header=False)
        else:
            correct_data = True
            new_data = {"title": [],
                        "amount": [],
                        "date": []
                        }

            for entries in entry_list:
                title_value = entries[0].get()
                amount_value = entries[1].get()
                date_value = entries[2].get()

                if title_value and amount_value and date_value:
                    new_data['title'].append(title_value)
                    new_data['amount'].append(amount_value)
                    new_data['date'].append(date_value)

                else:
                    correct_data = False
                    messagebox.showerror("Something went wrong", "Both category and price have to be filled out")
                    break

            if correct_data:
                new_df = pandas.DataFrame(new_data)
                new_df.to_csv("income_database.csv", index=False)
                messagebox.showinfo("Success", "Data saved")

                for widget in widget_list:
                    widget.destroy()

                label_widget_output("label")


    income_win = tk.Toplevel(root)
    income_win.minsize(500, 700)
    income_win.title("Add your Income")
    income_win.config(bg="white")

    text_labels = []

    try:
        label_widget_output("label")

    except FileNotFoundError:
        pass

    header = tk.Label(master=income_win,
                      text="Add your Income",
                      font=("open sans", 18, "bold"),
                      bg="white",
                      fg="#FFCF81")

    header.grid(row=0, column=0, padx=20, pady=20)

    title_label = tk.Label(master=income_win, text="Title", font=FONT, bg="white")
    title_label.grid(row=1, column=0, padx=10, pady=10)

    amount_label = tk.Label(master=income_win, text="Amount", font=FONT, bg="white")
    amount_label.grid(row=1, column=1, padx=10, pady=10)

    date_label = tk.Label(master=income_win, text="Date", font=FONT, bg="white")
    date_label.grid(row=1, column=2, padx=10, pady=10)

    title_entry = tk.Entry(master=income_win, font=FONT)
    title_entry.grid(row=2, column=0, padx=10)

    amount_entry = tk.Entry(master=income_win, font=FONT)
    amount_entry.grid(row=2, column=1, padx=10)

    inc_date_entry = tk.Entry(master=income_win, font=FONT, justify="right")
    inc_date_entry.grid(row=2, column=2, padx=10)
    inc_date_entry.insert(tk.END, CURRENT_DATE)

    save_button = tk.Button(master=income_win,
                            text="Save",
                            font=FONT,
                            bg="#d0eef8",
                            command=lambda: save_income_data("new")
                            )
    save_button.grid(row=4, column=0, pady=40)

    edit_button = tk.Button(master=income_win,
                            text="Edit",
                            font=FONT,
                            bg="#fcd9a8",
                            command=edit_entries
                            )
    edit_button.grid(row=4, column=2, padx=20)

    income_win.update()
    income_win.mainloop()
