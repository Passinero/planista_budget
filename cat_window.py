import tkinter as tk
# from line_plot_window import open_line_plot_window

FONT = ("open sans", 15)
BOLD_FONT = ("open sans", 18, "bold")

DARK_BLUE_COLOR = "#3bc4cf"
DARK_ORANGE_COLOR = "#FFCF81"


def open_cat_window(root, df, chosen_cat):
    local_cat_sum = sum(df['price'])

    catwin_font = ("open sans", 14)

    if len(df["price"]) > 28:
        catwin_font = ("open sans", 14)

    # Neues Fenster erstellen
    cat_window = tk.Toplevel(root)
    cat_window.minsize(760, 800)
    cat_window.title(f"Category {chosen_cat.title()}")
    cat_window.config(bg="white")

    # Rahmen für das Layout
    cat_frame = tk.Frame(cat_window, bg="white")
    cat_frame.grid(row=0, column=0, sticky="nsew")
    cat_window.grid_rowconfigure(0, weight=1)
    cat_window.grid_columnconfigure(0, weight=1)

    # Canvas erstellen
    canvas = tk.Canvas(cat_frame, bg="white")
    canvas.grid(row=0, column=0, sticky="nsew")

    # Scrollbar hinzufügen
    scrollbar = tk.Scrollbar(cat_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Inhalt im Canvas einbetten
    content_frame = tk.Frame(canvas, bg="white")
    canvas.create_window((0, 0), window=content_frame, anchor="nw")

    # Funktion zur Anpassung der Scrollregion
    def update_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    content_frame.bind("<Configure>", update_scroll_region)

    # Funktion zur Breitenanpassung des content_frame
    def update_content_frame_width(event):
        canvas_width = event.width
        content_frame.config(width=canvas_width)

    canvas.bind("<Configure>", update_content_frame_width)

    # Labels und Inhalte hinzufügen
    top_label = tk.Label(content_frame,
                         text=f"All purchases for {chosen_cat.title()}",
                         bg="white",
                         font=BOLD_FONT,
                         fg=DARK_ORANGE_COLOR)
    top_label.grid(row=0, column=0, padx=20, sticky="w", columnspan=4)

    sum_label = tk.Label(content_frame,
                         text=f"Total sum: {local_cat_sum:.2f} EUR",
                         font=FONT,
                         bg="white",
                         fg=DARK_BLUE_COLOR)
    sum_label.grid(row=1, column=0, padx=20, pady=10, sticky="w", columnspan=4)

    empty_row = tk.Label(content_frame, text="", bg="white")
    empty_row.grid(row=2, column=0)

    label_row = 3

    for index, row in df.iterrows():
        raw_date = row['date'].date()
        cat_date = raw_date.strftime("%d.%m.%Y")
        raw_price = str(row['price']).replace(".", ",")
        if len(raw_price.split(",")[1]) == 1:
            raw_price = f"{raw_price}0"

        item_label = tk.Label(content_frame, text=row['item'].title(), font=catwin_font, bg="white")
        item_label.grid(row=label_row, column=0, padx=20, sticky="w")

        price_label = tk.Label(content_frame, text=f"{raw_price} EUR", font=catwin_font, bg="white")
        price_label.grid(row=label_row, column=1, padx=20, sticky="e")

        shop_label = tk.Label(content_frame, text=row['shop'].upper(), font=catwin_font, bg="white")
        shop_label.grid(row=label_row, column=2, padx=20, sticky="w")

        date_label = tk.Label(content_frame, text=cat_date, font=catwin_font, bg="white")
        date_label.grid(row=label_row, column=3, padx=20, sticky="w")

        label_row += 1

    # Funktion, um Scrollen mit dem Mausrad zu ermöglichen
    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    # Rahmen so konfigurieren, dass sie skalieren
    cat_frame.grid_rowconfigure(0, weight=1)
    cat_frame.grid_columnconfigure(0, weight=1)
