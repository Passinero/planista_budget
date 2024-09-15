import tkinter as tk

font = ("open sans", 18, "bold")

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
              12: "December"
              }


def text_label(root, list_to_remove, cat, month, year):
    """ takes: root, the list it will append to, chosen category, month and year. creates a tkinter text label """
    try:
        month_name = month_dict[month]
    except KeyError:
        month = 0
    # when only the year is chosen
    if cat == 0 and month == 0 and year == 0:
        chosen_year_text = tk.Label(master=root,
                                    text=f"All Transactions",
                                    font=font,
                                    bg="white"
                                    )
        chosen_year_text.grid(row=4, column=1, pady=10, sticky="s")
        list_to_remove.append(chosen_year_text)

    elif cat == 0 and month == 0:
        chosen_year_text = tk.Label(master=root,
                                    text=f"Money spend in:\n{year}",
                                    font=font,
                                    bg="white"
                                    )
        chosen_year_text.grid(row=4, column=1, pady=10, sticky="s")
        list_to_remove.append(chosen_year_text)

    elif cat != 0 and month != 0:
        chosen_year_text = tk.Label(master=root,
                                    text=f"Money spend on {cat} in:\n{month_name} {year}",
                                    font=font,
                                    bg="white"
                                    )
        chosen_year_text.grid(row=4, column=1, pady=10, sticky="s")
        list_to_remove.append(chosen_year_text)

    # when category was chosen
    elif cat != 0:
        chosen_year_text = tk.Label(master=root,
                                    text = f"Money spend on:\n{cat.title()}",
                                    font=font,
                                    bg="white"
                                    )
        chosen_year_text.grid(row=4, column=1, pady=10, sticky="s")
        list_to_remove.append(chosen_year_text)
    # when month and year chosen
    elif month != 0:
        chosen_year_text = tk.Label(master=root,
                                    text=f"Money spend in:\n{month_name} {year}",
                                    font=font,
                                    bg="white"
                                    )
        chosen_year_text.grid(row=4, column=1, pady=10, sticky="s")
        list_to_remove.append(chosen_year_text)
