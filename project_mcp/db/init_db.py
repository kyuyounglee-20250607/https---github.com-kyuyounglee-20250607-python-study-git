import sqlite3
with sqlite3.connect(r'./project_mcp/db/sample.db') as conn:
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users(
                id integer primary key,
                name text
            )
                ''')
    conn.commit()