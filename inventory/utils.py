import sqlite3
import logging
import getpass
from tabulate import tabulate
from user_management import create_user_table

# Konfigurasi logging
logging.basicConfig(filename='inventory.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Fungsi untuk validasi input
def validate_input(name, quantity, price):
    if not name:
        print("Nama item tidak boleh kosong.")
        return False
    if quantity < 0:
        print("Kuantiti mestilah nombor positif.")
        return False
    if price < 0:
        print("Harga mestilah nombor positif.")
        return False
    return True

# Fungsi untuk log aktiviti
def log_activity(activity):
    logging.info(activity)

# Fungsi untuk autentikasi pengguna
def authenticate(cursor, username, password):
    create_user_table(cursor)
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    if user:
        return True
    else:
        return False

# Fungsi untuk periksa stok rendah
def check_low_stock(cursor, threshold=10):
    cursor.execute('SELECT * FROM inventory WHERE quantity < ?', (threshold,))
    items = cursor.fetchall()
    if items:
        headers = ["ID", "Nama", "Kuantiti", "Harga"]
        print("\nItem dengan stok rendah:")
        print(tabulate(items, headers, tablefmt="grid"))
    else:
        print("Tiada item dengan stok rendah.")

# Fungsi untuk menjana laporan dan statistik
def generate_report(cursor):
    cursor.execute('SELECT SUM(quantity), SUM(quantity * price) FROM inventory')
    total_items, total_value = cursor.fetchone()
    print(f"Jumlah item dalam stok: {total_items}")
    print(f"Nilai keseluruhan inventori: RM {total_value:.2f}")
