from exctract_shop_category import extract_shop_category
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from pie_chart_window import pie_chart_window

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


def small_plt(root, title, row, column, orig_values, orig_labels):
    extr_values, extr_labels = extract_shop_category(orig_values, orig_labels)

    extr_labels = [label.title() for label in extr_labels]

    chart_frame = tk.Frame(root)
    chart_frame.grid(row=row, column=column)

    if not extr_values or not extr_labels:
        fig, ax = plt.subplots(figsize=(4, 3))
        ax.pie([1], labels=['No Data'], colors=['lightgrey'])
        ax.set_title(title)
    else:
        fig, ax = plt.subplots(figsize=(4, 3))
        ax.pie(extr_values, labels=extr_labels, autopct='%1.1f%%', colors=color_list)
        ax.set_title(title)

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=row, column=column)

    canvas_widget.bind("<Button-1>", lambda event: pie_chart_window(
        root=root,
        values=orig_values,
        labels=orig_labels,
        title=title))

    plt.close(fig)
