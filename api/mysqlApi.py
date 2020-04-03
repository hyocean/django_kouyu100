from django.db import connections


class my_custom_sql:
    def __init__(self):
        self.conn = connections['hawkeye']
        self.cs = self.conn.cursor()

    def run(self, sql):
        try:
            self.cs.execute(sql)
            self.conn.commit()
            ret = self.cs
        except Exception as e:
            self.conn.rollback()
            ret = e
        return ret

    def __enter__(self):
        return self.run

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cs.close()
        self.conn.close()
