import psycopg2
from psycopg2 import extras


class Database:
    def __init__(self):
        self.config = {
            "dbname": "BaiTapLonPython",
            "user": "postgres",
            "password": "2006",
            "host": "localhost",
            "port": "5432"
        }

    
    def get_connection(self):
        return psycopg2.connect(**self.config)

   
    def fetch_tasks(self, search_query=None, sort_by="deadline"):
        conn = self.get_connection()
        cur = conn.cursor(cursor_factory=extras.RealDictCursor)

        sql = """
            SELECT 
                t.id,
                INITCAP(t.task_name) AS task_name,
                c.name AS category_name,
                u.full_name AS user_name,
                INITCAP(t.status::text) AS status,
                INITCAP(t.priority) AS priority,
                t.deadline
            FROM tasks t
            LEFT JOIN categories c ON t.category_id = c.id
            LEFT JOIN users u ON t.user_id = u.id
        """

        params = []

        
        if search_query:
            sql += """
                WHERE t.task_name ILIKE %s
                OR u.full_name ILIKE %s
            """
            keyword = f"%{search_query}%"
            params.extend([keyword, keyword])

        
        if sort_by == "id":
            sql += " ORDER BY t.id ASC"
        elif sort_by == "category":
            sql += " ORDER BY c.name ASC"
        else:
            sql += " ORDER BY t.deadline ASC"

        cur.execute(sql, params)
        data = cur.fetchall()

        cur.close()
        conn.close()
        return data

    
    def get_lookup(self, table):
        conn = self.get_connection()
        cur = conn.cursor()

        col = "name" if table == "categories" else "full_name"

        sql = f"""
            SELECT id, {col}
            FROM {table}
            ORDER BY id ASC
        """

        cur.execute(sql)
        data = cur.fetchall()

        cur.close()
        conn.close()
        return data

    
    def execute(self, query, params=None):
        conn = self.get_connection()
        cur = conn.cursor()

        try:
            cur.execute(query, params)
            conn.commit()
            return True
        except Exception as e:
            print("Lỗi SQL:", e)
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()