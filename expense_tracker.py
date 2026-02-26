import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime

# ------------------------------
# LOGIN SYSTEM
# ------------------------------
def login():
    print("===== Login =====")
    username = input("Enter username: ")
    password = input("Enter password: ")

    # Simple hardcoded login (for beginner level)
    if username == "admin" and password == "1234":
        print("Login Successful ✅\n")
        return True
    else:
        print("Invalid Credentials ❌")
        return False


# ------------------------------
# ADD EXPENSE
# ------------------------------
def add_expense():
    try:
        date = input("Enter date (YYYY-MM-DD): ")
        datetime.strptime(date, "%Y-%m-%d")  # validate date

        amount = float(input("Enter amount: "))
        category = input("Enter category (Food/Travel/Rent/etc): ")
        description = input("Enter description: ")

        new_data = pd.DataFrame(
            [[date, amount, category, description]],
            columns=["date", "amount", "category", "description"]
        )

        if os.path.exists("expenses.csv"):
            new_data.to_csv("expenses.csv", mode="a", header=False, index=False)
        else:
            new_data.to_csv("expenses.csv", index=False)

        print("Expense Added Successfully ✅")

    except ValueError:
        print("Invalid input! Please enter correct data ❌")


# ------------------------------
# VIEW EXPENSES
# ------------------------------
def view_expenses():
    try:
        df = pd.read_csv("expenses.csv")
        print("\n===== All Expenses =====")
        print(df)
    except FileNotFoundError:
        print("No expenses found ❌")


# ------------------------------
# CATEGORY SUMMARY
# ------------------------------
def category_summary():
    try:
        df = pd.read_csv("expenses.csv")
        summary = df.groupby("category")["amount"].sum()
        print("\n===== Category Summary =====")
        print(summary)
    except:
        print("No data available ❌")


# ------------------------------
# SEARCH BY DATE RANGE
# ------------------------------
def search_by_date():
    try:
        df = pd.read_csv("expenses.csv")
        df["date"] = pd.to_datetime(df["date"])

        start = input("Start date (YYYY-MM-DD): ")
        end = input("End date (YYYY-MM-DD): ")

        filtered = df[(df["date"] >= start) & (df["date"] <= end)]

        print("\n===== Filtered Results =====")
        print(filtered)

    except:
        print("Error in searching ❌")


# ------------------------------
# MONTHLY BUDGET CHECK
# ------------------------------
def check_budget():
    try:
        df = pd.read_csv("expenses.csv")
        df["date"] = pd.to_datetime(df["date"])

        current_month = datetime.now().month
        current_year = datetime.now().year

        monthly_total = df[
            (df["date"].dt.month == current_month) &
            (df["date"].dt.year == current_year)
        ]["amount"].sum()

        budget = 10000  # You can change monthly budget here

        print("\n===== Budget Check =====")
        print("Monthly Spending:", monthly_total)
        print("Budget:", budget)

        if monthly_total > budget:
            print("⚠ Budget Exceeded!")
        else:
            print("Within Budget ✅")

    except:
        print("No expense data found ❌")


# ------------------------------
# VISUALIZATION
# ------------------------------
def visualize():
    try:
        df = pd.read_csv("expenses.csv")
        summary = df.groupby("category")["amount"].sum()

        summary.plot(kind="bar")
        plt.title("Expenses by Category")
        plt.ylabel("Amount")
        plt.show()

    except:
        print("No data to visualize ❌")


# ------------------------------
# MAIN MENU
# ------------------------------
def main():
    if not login():
        return

    while True:
        print("\n===== Expense Tracker Menu =====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Category Summary")
        print("4. Search by Date")
        print("5. Check Monthly Budget")
        print("6. Visualize Expenses")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            category_summary()
        elif choice == "4":
            search_by_date()
        elif choice == "5":
            check_budget()
        elif choice == "6":
            visualize()
        elif choice == "7":
            print("Goodbye 👋")
            break
        else:
            print("Invalid choice ❌")


# ------------------------------
# RUN PROGRAM
# ------------------------------
if __name__ == "__main__":
    main()