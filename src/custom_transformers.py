# Custom Transformers

def undefined_meal(data):
    data = data.copy()
    data["meal"] = data["meal"].replace("Undefined", "SC")
    return data
