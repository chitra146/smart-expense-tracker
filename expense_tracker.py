from db_connection import get_connection
from datetime import datetime
import matplotlib.pyplot as plt
import bcrypt
import csv
import os


VALID_CATEGORIES = ['Food','Travel','Rent','Shopping','Bills','Other']
MONTHLY_BUDGET = 20000


# ------------------------------
# REGISTER NEW USER
# ------------------------------
def register_user():
    username = input("Enter new username: ").strip()
    password = input("Enter new password: ").strip()

    if len(username) < 3:
        print("Username must be at least 3 characters.")
        return

    if len(password) < 4:
        print("Password must be at least 4 characters.")
        return

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(query, (username, hashed_password))
        conn.commit()

        print("User Registered Successfully!")

        cursor.close()
        conn.close()

    except Exception as e:
        print("Error or User already exists:", e)


# ------------------------------
# AUTO LOGIN
# ------------------------------
def auto_login():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT user_id, username FROM users ORDER BY user_id LIMIT 1")
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            print(f"\nAuto Logged in as: {user[1]}")
            return user[0]
        else:
            print("No users found in database.")
            return None

    except Exception as e:
        print("Database Error:", e)
        return None


# ------------------------------
# VALIDATION HELPERS
# ------------------------------
def validate_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_amount(amount):
    try:
        amt = float(amount)
        return amt > 0
    except:
        return False


def validate_category(category):
    return category in VALID_CATEGORIES


# ------------------------------
# ADD EXPENSE
# ------------------------------
def add_expense(user_id):
    date = input("Enter date (YYYY-MM-DD): ")
    if not validate_date(date):
        print("Invalid Date Format!")
        return

    amount = input("Enter amount: ")
    if not validate_amount(amount):
        print("Amount must be positive number!")
        return

    print("Categories:", VALID_CATEGORIES)
    category = input("Enter category: ")
    if not validate_category(category):
        print("Invalid Category!")
        return

    description = input("Enter description: ")

    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO expenses
        (user_id, expense_date, amount, category, description)
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(query, (user_id, date, float(amount), category, description))
        conn.commit()   

        # ------------------------------
        # SAVE TO CSV FILE
        # ------------------------------
        file_exists = os.path.isfile("expenses.csv")

        with open("expenses.csv", mode="a", newline="") as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow(["user_id","date","amount","category","description"])

            writer.writerow([user_id, date, amount, category, description])

        cursor.close()
        conn.close()

        print("Expense Added Successfully!")

    except Exception as e:
        print("Error:", e)


# ------------------------------
# VIEW EXPENSES
# ------------------------------
def view_expenses(user_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT expense_date, amount, category, description
            FROM expenses
            WHERE user_id=%s
            ORDER BY expense_date DESC
        """, (user_id,))

        results = cursor.fetchall()

        print("\n===== All Expenses =====")
        print("Date       | Amount   | Category  | Description")
        print("-" * 55)

        for row in results:
            date = row[0].strftime("%Y-%m-%d")
            amount = float(row[1])
            category = row[2]
            description = row[3]

            print(f"{date} | ₹{amount:.2f} | {category:<9} | {description}")

        cursor.close()
        conn.close()

    except Exception as e:
        print("Error:", e)


# ------------------------------
# CATEGORY SUMMARY
# ------------------------------
def category_summary(user_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT category, SUM(amount)
            FROM expenses
            WHERE user_id=%s
            GROUP BY category
        """, (user_id,))

        results = cursor.fetchall()

        print("\n===== Category Summary =====")
        for row in results:
            print(f"{row[0]} : ₹{float(row[1]):.2f}")

        cursor.close()
        conn.close()

    except Exception as e:
        print("Error:", e)


# ------------------------------
# CHECK MONTHLY BUDGET
# ------------------------------
def check_budget(user_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT SUM(amount)
            FROM expenses
            WHERE user_id=%s
            AND MONTH(expense_date)=MONTH(CURDATE())
            AND YEAR(expense_date)=YEAR(CURDATE())
        """, (user_id,))

        total = cursor.fetchone()[0] or 0

        print("\n===== Budget Check =====")
        print("Monthly Spending:", float(total))
        print("Budget:", MONTHLY_BUDGET)

        if total > MONTHLY_BUDGET:
            print("⚠ Budget Exceeded!")
        else:
            print("Within Budget")

        cursor.close()
        conn.close()

    except Exception as e:
        print("Error:", e)


# ------------------------------
# VISUALIZATION
# ------------------------------
def visualize(user_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT category, SUM(amount)
            FROM expenses
            WHERE user_id=%s
            GROUP BY category
        """, (user_id,))

        results = cursor.fetchall()

        categories = [row[0] for row in results]
        amounts = [float(row[1]) for row in results]

        plt.figure()
        plt.bar(categories, amounts)
        plt.title("Expenses by Category")
        plt.xlabel("Category")
        plt.ylabel("Amount")
        plt.show()

        cursor.close()
        conn.close()

    except Exception as e:
        print("Error:", e)


# ------------------------------
# MAIN MENU
# ------------------------------
def main():
    user_id = auto_login()
    if not user_id:
        return

    while True:
        print("\n===== Expense Tracker Menu =====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Category Summary")
        print("4. Check Monthly Budget")
        print("5. Visualize Expenses")
        print("6. Register New User")
        print("7. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            add_expense(user_id)
        elif choice == "2":
            view_expenses(user_id)
        elif choice == "3":
            category_summary(user_id)
        elif choice == "4":
            check_budget(user_id)
        elif choice == "5":
            visualize(user_id)
        elif choice == "6":
            register_user()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid Choice")


if __name__ == "__main__":
    main()