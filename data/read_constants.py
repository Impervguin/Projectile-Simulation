import sqlite3


def transfer():
    data = {}
    db = sqlite3.connect("db/physical_values.db")
    cur = db.cursor()
    tables_information = cur.execute("SELECT * FROM sqlite_master").fetchall()
    tables = {}
    for table_inf in tables_information:
        parsed_inf = table_inf[4].split()
        col_names = [parsed_inf[i] for i in range(4, len(parsed_inf) - 1, 2)]
        tables[table_inf[1]] = col_names
    for table in tables:
        data[table] = {}
        for elems in cur.execute(f"SElECT * FROM {table}").fetchall():
            row = {}
            for i in range(len(tables[table])):
                row[tables[table][i]] = elems[i]
            data[table][elems[1]] = row
    return data