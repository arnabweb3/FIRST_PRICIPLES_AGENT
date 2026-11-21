import os
import csv
import sqlite3
from tavily import TavilyClient
from tool_safety import (
    check_tool_permission,
    validate_output_path
)

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
    with open(filepath, "w", encoding="utf-8") as file:
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


def database_query(query):

    normalized_query = query.strip().lower()

    if not normalized_query.startswith("select"):
        raise ValueError("Only SELECT queries are allowed")


    connection = sqlite3.connect(
        "file:data/sales.db?mode=ro",
        uri=True
    )

    def authorize(action, arg1, arg2, database, trigger):
        allowed_actions = {
            sqlite3.SQLITE_SELECT,
            sqlite3.SQLITE_READ,
            sqlite3.SQLITE_FUNCTION,
        }

        if action in allowed_actions:
            return sqlite3.SQLITE_OK

        return sqlite3.SQLITE_DENY

    try:
        connection.set_authorizer(authorizer_callback=authorize)

        cursor = connection.cursor()

        cursor.execute(query)


        columns = [
            description[0] for description in cursor.description
        ]


        rows = cursor.fetchall()

        return {
            "columns" : columns,
            "rows" : rows,
            "row_count" : len(rows)
        }

    finally:
        connection.close()



def search_web(query):
    api_key = os.getenv('TAVILY_API_KEY')

    if not api_key:
        raise ValueError("TAVILY_API_KEY is missing")

    client = TavilyClient(api_key=api_key)

    response = client.search(
        query=query,
        max_results=5
    )

    results = []

    for item in response.get('results', []):

        results.append(
            {
                "title" : item.get('title'),
                "url" : item.get("url"),
                "content" : item.get('content')
            }
        )

    return {
        "query" : query,
        "results" : results,
        "results_count" : len(results)
    }




def is_retryable_error(error):
    
    message = str(error).lower()

    retryable_errors = [
        "timeout",
        "timed out",
        "connection reset",
        "connection error",
        "temporarily unavailable",
        "500",
        "429",
        "502",
        "503",
        "504"
    ]


    if isinstance(error , (TimeoutError, ConnectionError)):
        return True

    return any(
        term in message
        for term in retryable_errors
    )
