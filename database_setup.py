import sqlite3

def setup_database():

    connection = sqlite3.connect("data/sales.db")


    cursor = connection.cursor()

    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS sales(
                order_id INTEGER PRIMARY KEY,
                customer TEXT,
                product TEXT,
                quantity INTEGER,
                unit_price REAL,
                region TEXT           
            )
        """
    )

    cursor.execute("DELETE FROM sales")

    sales_data = [
        (1001, "Amit", "Laptop", 2, 55000, "East"),
        (1002, "Priya", "Mouse", 5, 800, "North"),
        (1003, "Rahul", "Keyboard", 3, 1500, "East"),
        (1004, "Neha", "Monitor", 2, 12000, "South"),
        (1005, "Arjun", "Laptop", 1, 55000, "West"),
        (1006, "Sneha", "Mouse", 10, 800, "East"),
        (1007, "Vikram", "Keyboard", 4, 1500, "North"),
        (1008, "Ananya", "Monitor", 3, 12000, "East"),
        (1009, "Rohan", "Laptop", 2, 55000, "South"),
        (1010, "Meera", "Mouse", 8, 800, "West")
    ]


    cursor.executemany(
        """
            INSERT INTO sales VALUES (?, ? , ? ,? ,?,?)
        """, sales_data
    )


    connection.commit()
    connection.close()

    print("Database created successfully")

if __name__ == "__main__":
    setup_database()