import tkinter as tk

FONT = ("open sans", 15)
BOLD_FONT = ("open sans", 18, "bold")

DARK_BLUE_COLOR = "#3bc4cf"
DARK_ORANGE_COLOR = "#FFCF81"


def open_cat_window(root, df, chosen_cat):
    local_cat_sum = sum(df['price'])

    catwin_font = ("open sans", 14)

    if len(df["price"]) > 28:
        catwin_font = ("open sans", 10)

    cat_window = tk.Toplevel(root)
    cat_window.minsize(400, 800)
    cat_window.title(f" Category {chosen_cat.title()}")
    cat_window.config(bg="white")

    cat_frame = tk.Frame(cat_window, bg="white")
    cat_frame.grid(row=0, column=0)

    top_label = tk.Label(cat_frame,
                         text=f"All purchases for {chosen_cat.title()}",
                         bg="white",
                         font=BOLD_FONT,
                         fg=DARK_ORANGE_COLOR)

    top_label.grid(row=1, column=0, padx=20, sticky="w")

    sum_label = tk.Label(cat_frame,
                         text=f"Total sum: {local_cat_sum:.2f} EUR",
                         font=FONT,
                         bg="white",
                         fg=DARK_BLUE_COLOR)

    sum_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")

    empty_row = tk.Label(cat_frame, text="", bg="white")
    empty_row.grid(row=3, column=0)

    label_row = 4

    for index, row in df.iterrows():
        raw_date = row['date'].date()
        cat_date = raw_date.strftime("%d.%m.%Y")
        raw_price = str(row['price']).replace(".", ",")
        if len(raw_price.split(",")[1]) == 1:
            raw_price = f"{raw_price}0"

        item_label = tk.Label(cat_frame, text=row['item'].title(), font=catwin_font, bg="white")
        item_label.grid(row=label_row, column=0, padx=20, sticky="w")

        price_label = tk.Label(cat_frame, text=f"{raw_price} EUR", font=catwin_font, bg="white")
        price_label.grid(row=label_row, column=1, padx=20, sticky="e")

        shop_label = tk.Label(cat_frame, text=row['shop'].upper(), font=catwin_font, bg="white")
        shop_label.grid(row=label_row, column=2, padx=20, sticky="w")

        date_label = tk.Label(cat_frame, text=cat_date, font=catwin_font, bg="white")
        date_label.grid(row=label_row, column=3, padx=20, sticky="w")

        label_row += 1
