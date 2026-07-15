# Custom Transformers

def undefined_meal(data):
    data = data.copy()
    data["meal"] = data["meal"].replace("Undefined", "SC")
    return data


def month_name_to_number(data):
    data = data.copy()
    month_map = {"January": 1, "February": 2, "March": 3, "April": 4,
             "May": 5, "June": 6, "July": 7, "August": 8,
             "September": 9, "October": 10, "November": 11, "December": 12}
    data["arrival_date_month"] = data["arrival_date_month"].map(month_map)
    return data
