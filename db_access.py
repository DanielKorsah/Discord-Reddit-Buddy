import sqlite3

conn = sqlite3.connect("server_data.db")


def make_table():
    c = conn.cursor()
    c.execute("""
                --sql
                CREATE TABLE servers(
                id INT PRIMARY KEY,
                default_results_length INT,
                nsfw_unrestricted INT
                )
                --endsql
            """)
    conn.commit()


def add_settings(id, results, nsfw):
    c = conn.cursor()
    c.execute("""
                --sql
                INSERT OR REPLACE INTO servers
                VALUES (:id, :results, :nsfw)
                --endsql
            """, {"id": id, "results": results, "nsfw": nsfw})
    conn.commit()


def get_settings(query_id):
    c = conn.cursor()
    c.execute("""
                --sql
                SELECT default_results_length, nsfw_restricted
                FROM servers
                WHERE id=:query_id
                --endsql
            """, {"query_id": query_id})
    conn.commit()
    return c.fetchall()


def get_all():
    c = conn.cursor()
    c.execute("""
                --sql
                SELECT * FROM servers
                --endsql
            """)
    conn.commit()
    print("getting all servers' settings")
    return c.fetchall()


def del_table():
    c = conn.cursor()
    c.execute("""
                --sql
                DROP TABLE servers
                --endsql
            """)
    conn.commit()
    print("Servers table deleted")


# del_table()
# make_table()
#add_settings(1, 2, False)
#add_settings(2, 9, False)
#add_settings(3, 14, True)

# print(get_settings(1))
#add_settings(2, 9, True)
# print(len(get_settings(5)))
# c.execute("""--sql SELECT * FROM servers --endsql""")
# conn.commit()
