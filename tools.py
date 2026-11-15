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
        file.write(str(content))

    return f"File saved successfully: {filepath}" 

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


def get_highest_revenue_product(product_revenue):

    if not product_revenue:
        raise ValueError("No product revenue data available")

    highest_product = max(
        product_revenue,
        key=product_revenue.get
    )

    return {
        "product": highest_product,
        "revenue": product_revenue[highest_product]
    }





def revenue_by_product(filepath):

    product_revenue = {}

    with open(filepath, "r", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:

            product = row["product"]

            revenue = (
                int(row["quantity"]) *
                float(row["unit_price"])
            )

            product_revenue[product] = (
                product_revenue.get(product, 0) + revenue
            )

    return product_revenue