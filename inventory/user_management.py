import sqlite3

def create_user_table(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT
    )
    ''')

def register_user(cursor, conn):
    create_user_table(cursor)
    username = input("Masukkan nama pengguna baru: ")
    password = input("Masukkan kata laluan baru: ")
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        print(f'Pengguna "{username}" telah didaftarkan.')
    except sqlite3.IntegrityError:
        print(f'Pengguna "{username}" sudah wujud.')
