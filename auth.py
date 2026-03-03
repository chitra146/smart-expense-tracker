import bcrypt
from db_connection import get_connection


# ------------------------------
# REGISTER USER
# ------------------------------
def register():
    username = input("Enter new username: ")
    password = input("Enter new password: ")

    if len(username) < 3:
        print("Username too short!")
        return None

    if len(password) < 4:
        print("Password too weak!")
        return None

    # Hash password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(query, (username, hashed_password))

        conn.commit()
        print("Registration Successful!")

        cursor.close()
        conn.close()

    except Exception as e:
        print("Username already exists or error:", e)


# ------------------------------
# LOGIN USER
# ------------------------------
def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "SELECT user_id, password FROM users WHERE username=%s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            user_id = user[0]
            stored_password = user[1]

            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                print("Login Successful!")
                return user_id
            else:
                print("Incorrect password")
                return None
        else:
            print("User not found")
            return None

    except Exception as e:
        print("Error:", e)
        return None