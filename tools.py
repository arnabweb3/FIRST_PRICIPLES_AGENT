import csv


def calculator(a,b,operation):
    
    if operation == "multiply":
        return a * b

    if operation == "add":
        return a + b

    if operation == "subtract":
        return a - b

    if operation == "divide":
        if b == 0:
            raise ValueError("Division by zero")

        return a / b

    raise ValueError("Unsupported operation")



def write_file(filepath, content):
    with open(filepath, "w") as file:
        return file.write(content)

def read_file(filepath):
    with open(filepath,"r") as file:
        content = file.read()
        return content

def calculate_revenue(filepath):
    total_revenue = 0

    with open(filepath, "r", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:

            quantity = int(row["quantity"])
            unit_price = float(row["unit_price"])

            total_revenue += quantity * unit_price

    return total_revenue