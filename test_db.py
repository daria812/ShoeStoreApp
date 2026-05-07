import psycopg2

def test_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="shoe_store",
            user="postgres",
            password="postgres"
        )
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        print(" Подключение успешно!")
        print("Версия PostgreSQL:", version)
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(" Ошибка подключения:", e)
        return False

if __name__ == "__main__":
    test_connection()