import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

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
              PURPLE_COLOR, YELLOW_COLOR,
              ]


def pie_chart_window(root, values, labels, title):
    labels = labels.tolist()
    labels = [label.title() for label in labels]

    label_pair = sorted(zip(values, labels), reverse=True)
    values, labels = zip(*label_pair)

    plt_window = tk.Toplevel(root)
    plt_window.minsize(400, 400)
    plt_window.title(title.title())
    plt_window.config(bg="white")

    chart_frame = tk.Frame(plt_window)
    chart_frame.grid(row=0, column=0, padx=20, pady=10)

    fig, ax = plt.subplots(figsize=(11, 11))

    ax.pie(values,
           labels=labels,
           colors=color_list,
           autopct=lambda p: f'{p * sum(values) / 100 :.0f} EUR')
    ax.set_title(title)

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.LEFT)