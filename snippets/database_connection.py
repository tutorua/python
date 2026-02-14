class DatabaseConnection:

    

with DatabaseConnection("ExampleDB") as db:
    print(f"Is connected? {db.connected}")
