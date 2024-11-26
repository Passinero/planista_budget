def extract_shop_category(values_list, labels_list):
    sorted_labels = []
    sorted_values = []

    comb_name = "Other"
    comb_shop_perc = 0

    percentage = (sum(values_list) / 100) * 3

    for val, label in zip(values_list, labels_list):

        if val < percentage:
            comb_shop_perc += val
        else:
            sorted_labels.append(label)
            sorted_values.append(val)

    if comb_shop_perc > 0:
        sorted_labels.append(comb_name)
        sorted_values.append(round(comb_shop_perc))

    sorted_pairs = sorted(zip(sorted_values, sorted_labels), reverse=True)

    if not sorted_pairs:
        return [], []

    sorted_values, sorted_labels = zip(*sorted_pairs)

    return sorted_values, sorted_labels
