import tkinter as tk
from tkinter import messagebox

hos_cat_list = []
all_categories_list = []

with open("categories.txt", mode="r") as file:
    for cat in file:
        if cat:
            all_categories_list.append(cat.strip().lower())

FONT = ("open sans", 15)
SMALL_FONT = ("open sans", 12)
BOLD_FONT = ("open sans", 20, "bold")

ORANGE_COLOR = "#fcd9a8"
GREEN_COLOR = "#D9EDBF"
PAPER_COLOR = "#fbfbfb"

temp_widgets = []


def add_edit_hos_cats(root):
    hos_cat_list.clear()
    with open("hos_database.txt", mode="r") as file3:
        items_list = file3.readlines()
        for item in items_list:
            hos_cat_list.append(item.split("/")[0].strip())
    print(hos_cat_list)
    entry_list = []
    items_to_save = []

    def save_data():
        hos_cat_list.clear()

        for widget in entry_list:
            hos_cat = widget.get()
            if hos_cat:
                items_to_save.append(hos_cat)

        for new_cats in items_to_save:
            if new_cats.lower() not in all_categories_list:
                all_categories_list.append(new_cats.lower())
                with open("categories.txt", mode="a") as file4:
                    file4.write(f"{new_cats}\n")
                    print(f"categories.txt edited")

        with open("hos_database.txt", mode="w") as file2:
            for item2 in items_to_save:
                file2.write(f"{item2.strip().lower()}\n")

        messagebox.showinfo("Success", "Data saved successfully")
        edit_hos.destroy()
        add_edit_hos_cats(root)

    def additional_entry():

        addit_entry = tk.Entry(master=edit_hos, font=FONT)
        addit_entry.grid(row=len(entry_list) + 3, column=0, padx=30, sticky="w")
        entry_list.append(addit_entry)

        plus_one_button.grid(row=len(entry_list) + 3, column=0, padx=30, sticky="w")
        save_button.grid(row=len(entry_list) + 4)

    edit_hos = tk.Toplevel(root, bg="white")
    edit_hos.minsize(300, 500)
    edit_hos.title("Edit your Hall of Shame")

    header = tk.Label(master=edit_hos, text="Edit your Hall of ...", font=BOLD_FONT, bg="white", fg=ORANGE_COLOR)
    header.grid(row=0, column=0, padx=30, pady=15, sticky="w")

    # name_entry = tk.Entry(master=edit_hos, font=FONT, bg=PAPER_COLOR, fg="#D3D3D3")
    # name_entry.grid(row=2, column=0, padx=30, pady=20, sticky="w")
    # name_entry.insert(0, "Hall of Shame")
    # name_entry.bind("<Button-1>", clear_entry)

    if not hos_cat_list:
        curr_row = 3
        for i in range(5):
            new_entry = tk.Entry(master=edit_hos, font=FONT)
            new_entry.grid(row=curr_row, column=0, padx=30, sticky="w")
            entry_list.append(new_entry)

            curr_row += 1

    else:
        curr_row2 = 3
        for cats in hos_cat_list:
            new_entry2 = tk.Entry(master=edit_hos, font=FONT)
            new_entry2.grid(row=curr_row2, column=0, padx=30, sticky="w")
            new_entry2.insert(0, cats.title())
            entry_list.append(new_entry2)
            curr_row2 += 1

        empty_entry = tk.Entry(master=edit_hos, font=FONT)
        empty_entry.grid(row=len(entry_list) + 3, column=0, padx=30, sticky="w")
        entry_list.append(empty_entry)

    plus_one_button = tk.Button(master=edit_hos,
                                text="+",
                                font=FONT,
                                width=20,
                                command=additional_entry,
                                )
    plus_one_button.grid(row=len(entry_list) + 4, column=0, padx=30, pady=5, sticky="w")

    save_button = tk.Button(master=edit_hos,
                            text="Save",
                            font=FONT,
                            command=save_data,
                            width=20,
                            bg=GREEN_COLOR,
                            )
    save_button.grid(row=len(entry_list) + 5, column=0, padx=30, pady=20, sticky="w")
