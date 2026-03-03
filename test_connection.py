from db_connection import get_connection

def test_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()

    for row in result:
        print(row)

    conn.close()


if __name__ == "__main__":
    test_db()