import sqlite3

# make db connection when module is imported
conn = sqlite3.connect("server_data.db")


def make_table():
    # create table for servers settings
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


def add_settings(id, results, maximum, nsfw):
    # insert new settings or update existing ones
    c = conn.cursor()
    c.execute("""
                --sql
                INSERT OR REPLACE INTO servers(id, default_results_length, max_results, nsfw_restricted)
                VALUES (:id, :results, :max_results, :nsfw)
                --endsql
            """, {"id": id, "results": results, "nsfw": nsfw, "max_results": maximum})
    conn.commit()


def delete_settings(query_id):
    # remove a row
    c = conn.cursor()
    c.execute("""
                --sql
                DELETE FROM servers 
                WHERE id=:query_id
                --endsql
            """, {"query_id": query_id})
    conn.commit()


def set_max_results(query_id, val):
    # update max results setting
    c = conn.cursor()
    c.execute("""
                --sql
                UPDATE servers
                SET max_results = :val
                WHERE id=:query_id
                --endsql
            """, {"query_id": query_id, "val": val})
    conn.commit()


def set_default_results(query_id, val):
    # update default results setting
    c = conn.cursor()
    c.execute("""
                --sql
                UPDATE servers
                SET default_results_length = :val
                WHERE id=:query_id
                --endsql
            """, {"query_id": query_id, "val": val})
    conn.commit()


def get_settings(query_id):
    # return all settings in a row
    c = conn.cursor()
    c.execute("""
                --sql
                SELECT default_results_length, max_results, nsfw_restricted
                FROM servers
                WHERE id=:query_id
                --endsql
            """, {"query_id": query_id})
    conn.commit()

    return c.fetchall()


def verify_record(row_id):
    '''Returns True if record can successfully be verified to exist, else sets defualt values and return False'''

    # return all settings in a row
    c = conn.cursor()
    c.execute("""
                --sql
                SELECT default_results_length, max_results, nsfw_restricted
                FROM servers
                WHERE id=:query_id
                --endsql
            """, {"query_id": row_id})
    conn.commit()
    # if id not found in db
    if len(c.fetchall()) == 0:
        # add the default settings
        add_settings(row_id, 5, 20, 1)
        return False
    else:
        return True


def get_all():
    # return entire servers table
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
    # delete the servers table
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
