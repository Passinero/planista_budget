import pandas


def update_last_entry(label):
    """ updates the last item bought """
    try:
        temp_df = pandas.read_csv("planista_database.csv")

        if temp_df.empty:
            label.config(text="No entries found")
            return

        last_item = temp_df.iloc[-1]

        label.config(text=f"Your last entry: "
                                    f"{last_item['item'].title()} - "
                                    f"{last_item['price']:.2f} EUR - "
                                    f"{last_item['date']}")

    except (KeyError, IndexError, FileNotFoundError) as e:
        label.config(text=f"Error: {str(e)}")