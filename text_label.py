import tkinter as tk
from datetime import date

font = ("open sans", 20, "bold")

current_month = date.today().month
current_year = date.today().year

month_dict = {1: "January",
              2: "February",
              3: "March",
              4: "April",
              5: "May",
              6: "June",
              7: "July",
              8: "August",
              9: "September",
              10: "October",
              11: "November",
              12: "December",
              0: None
              }


def text_label(root, list_to_remove, cat, month, year):
    """ takes: root, the list it will append to, chosen category, month and year. creates a tkinter text label """
    try:
        month_name = month_dict[month]
    except KeyError:
        month = 0
        month_name = ""

    # when nothing was chosen (bei Start von Statistics)
    if cat == 0 and month == 0 and year == 0:
        chosen_year_text = tk.Label(master=root,
                                    text=f"",
                                    font=font,
                                    bg="white"
                                    )
        chosen_year_text.grid(row=4, column=1, pady=10, sticky="s")
        list_to_remove.append(chosen_year_text)
    # when no category and no month were chosen
    elif cat == 0 and month == 0:
        chosen_year_text = tk.Label(master=root,
                                    text=f"{year}",
                                    font=font,
                                    bg="white"
                                    )
        chosen_year_text.grid(row=4, column=1, pady=10, sticky="s")
        list_to_remove.append(chosen_year_text)
    # when category and month were chosen
    elif cat != 0 and month != 0:
        chosen_year_text = tk.Label(master=root,
                                    text=f" {cat} in {month_name} {year}",
                                    font=font,
                                    bg="white"
                                    )
        chosen_year_text.grid(row=4, column=1, pady=10, sticky="s")
        list_to_remove.append(chosen_year_text)

    # when category and year were chosen
    elif cat != 0 and year != 0:
        chosen_year_text = tk.Label(master=root,
                                    text=f" {cat.title()} in {year}",
                                    font=font,
                                    bg="white"
                                    )
        chosen_year_text.grid(row=4, column=1, pady=10, sticky="s")
        list_to_remove.append(chosen_year_text)

    # when category was chosen
    elif cat != 0:
        chosen_year_text = tk.Label(master=root,
                                    text=f"Total {cat.title()}",
                                    font=font,
                                    bg="white"
                                    )
        chosen_year_text.grid(row=4, column=1, pady=10, sticky="s")
        list_to_remove.append(chosen_year_text)
    # when month and year chosen
    elif month != 0:
        chosen_year_text = tk.Label(master=root,
                                    text=f"{month_name} {year}",
                                    font=font,
                                    bg="white"
                                    )
        chosen_year_text.grid(row=4, column=1, pady=10, sticky="s")
        list_to_remove.append(chosen_year_text)
