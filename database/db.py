import psycopg2

class Database:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="shoe_store",
            user="postgres",
            password="postgres",
        )

    def execute_query(self, query, params=None):

        with self.conn.cursor() as cur:
            cur.execute(query, params or ())
            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            return [dict(zip(columns, row)) for row in rows]

    def execute_non_query(self, query, params=None):

        with self.conn.cursor() as cur:
            cur.execute(query, params or ())
            self.conn.commit()
            return cur.rowcount

    def close(self):
        self.conn.close()