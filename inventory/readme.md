# Sistem Inventori

Sistem Inventori ini adalah aplikasi Python yang membolehkan pengguna menguruskan inventori dengan ciri-ciri seperti menambah, mengemaskini, mencari dan membuang item dari inventori. Aplikasi ini menggunakan SQLite untuk pengurusan data dan `tabulate` untuk paparan data yang lebih kemas.

## Ciri-ciri

- **Paparkan Inventory**: Paparkan senarai semua item dalam inventori.
- **Tambah Item**: Tambah item baru ke dalam inventori.
- **Buang Item**: Buang item dari inventori berdasarkan ID.
- **Kemas Kini Item**: Kemas kini maklumat item berdasarkan ID.
- **Cari Item**: Cari item berdasarkan nama atau ID.
- **Log Aktiviti**: Rekod setiap aktiviti pengguna dalam fail log.
- **Fungsi Import/Export**: Import dan eksport data inventori dari/ke fail CSV.
- **Pemberitahuan Stok Rendah**: Maklumkan pengguna apabila stok sesuatu item rendah.
- **Autentikasi Pengguna**: Sistem login untuk mengawal akses ke aplikasi.
- **Laporan dan Statistik**: Jana laporan dan statistik inventori.

## Keperluan

- Python 3.x
- SQLite (termasuk dalam Python standard library)
- Library `tabulate`

## Pemasangan

1. Clone repositori atau muat turun fail `inventory_system.py`.
2. Pasang keperluan menggunakan pip:
    ```sh
    pip install -r requirements.txt
    ```

## Penggunaan

1. Jalankan fail `inventory_system.py` menggunakan Python:
    ```sh
    python inventory_system.py
    ```
2. Ikut arahan yang dipaparkan untuk menguruskan inventori.

## Struktur Kod

```python
import sqlite3
import csv
import logging
from tabulate import tabulate
import getpass

# Konfigurasi logging
logging.basicConfig(filename='inventory.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Sambung ke database (atau buat baru jika belum ada)
conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()

# Buat table jika belum ada
cursor.execute('''
CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY,
    name TEXT,
    quantity INTEGER,
    price REAL
)
''')

# Fungsi untuk kemas kini item
def kemas_kini_item(item_id, item_name, quantity, price):
    cursor.execute('''
    UPDATE inventory
    SET name = ?, quantity = ?, price = ?
    WHERE id = ?
    ''', (item_name, quantity, price, item_id))
    conn.commit()
    print(f'Item dengan ID {item_id} telah dikemas kini.')
    log_activity(f'Item dengan ID {item_id} dikemas kini: {item_name}, Kuantiti: {quantity}, Harga: {price}')

# Fungsi untuk cari item berdasarkan nama atau ID
def cari_item(cari_value):
    cursor.execute('SELECT * FROM inventory WHERE name LIKE ? OR id LIKE ?', (f'%{cari_value}%', f'%{cari_value}%'))
    items = cursor.fetchall()
    if items:
        headers = ["ID", "Nama", "Kuantiti", "Harga"]
        print("\nHasil Carian:")
        print(tabulate(items, headers, tablefmt="grid"))
    else:
        print("Tiada item yang sepadan.")

# Fungsi untuk eksport data ke fail CSV
def export_to_csv(filename='inventory.csv'):
    cursor.execute('SELECT * FROM inventory')
    items = cursor.fetchall()
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Nama", "Kuantiti", "Harga"])
        writer.writerows(items)
    print(f"Data telah dieksport ke {filename}.")

# Fungsi untuk import data dari fail CSV
def import_from_csv(filename='inventory.csv'):
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            cursor.execute('INSERT INTO inventory (id, name, quantity, price) VALUES (?, ?, ?, ?)', row)
        conn.commit()
    print(f"Data telah diimport dari {filename}.")

# Fungsi untuk periksa stok rendah
def check_low_stock(threshold=10):
    cursor.execute('SELECT * FROM inventory WHERE quantity < ?', (threshold,))
    items = cursor.fetchall()
    if items:
        headers = ["ID", "Nama", "Kuantiti", "Harga"]
        print("\nItem dengan stok rendah:")
        print(tabulate(items, headers, tablefmt="grid"))
    else:
        print("Tiada item dengan stok rendah.")

# Fungsi untuk autentikasi pengguna
def authenticate():
    users = {"admin": "password123", "user": "userpass"}
    username = input("Masukkan nama pengguna: ")
    password = getpass.getpass("Masukkan kata laluan: ")
    if users.get(username) == password:
        print("Login berjaya!")
        return True
    else:
        print("Login gagal.")
        return False

# Fungsi untuk menjana laporan dan statistik
def generate_report():
    cursor.execute('SELECT SUM(quantity), SUM(quantity * price) FROM inventory')
    total_items, total_value = cursor.fetchone()
    print(f"Jumlah item dalam stok: {total_items}")
    print(f"Nilai keseluruhan inventori: RM {total_value:.2f}")

# Fungsi untuk log aktiviti
def log_activity(activity):
    logging.info(activity)

# Contoh fungsi utama untuk demonstrasi
def main():
    if not authenticate():
        return

    while True:
        print("\nSistem Inventory")
        print("1. Paparkan inventory")
        print("2. Tambah item")
        print("3. Buang item")
        print("4. Kemas kini item")
        print("5. Cari item")
        print("6. Eksport ke CSV")
        print("7. Import dari CSV")
        print("8. Periksa stok rendah")
        print("9. Jana laporan")
        print("10. Keluar")
        pilihan = input("Masukkan pilihan (1/2/3/4/5/6/7/8/9/10): ")

        if pilihan == '1':
            cursor.execute('SELECT * FROM inventory')
            items = cursor.fetchall()
            headers = ["ID", "Nama", "Kuantiti", "Harga (RM)"]
            print("\nSenarai Inventory:")
            print(tabulate(items, headers, tablefmt="grid"))

        elif pilihan == '2':
            name = input("Masukkan nama item: ")
            quantity = int(input("Masukkan kuantiti: "))
            price = float(input("Masukkan harga: "))
            if validate_input(name, quantity, price):
                cursor.execute('INSERT INTO inventory (name, quantity, price) VALUES (?, ?, ?)', (name, quantity, price))
                conn.commit()
                print(f'Item "{name}" telah ditambah.')
                log_activity(f'Item ditambah: {name}, Kuantiti: {quantity}, Harga: {price}')

        elif pilihan == '3':
            item_id = int(input("Masukkan ID item untuk dibuang: "))
            cursor.execute('DELETE FROM inventory WHERE id = ?', (item_id,))
            conn.commit()
            print(f'Item dengan ID {item_id} telah dibuang.')
            log_activity(f'Item dengan ID {item_id} dibuang.')

        elif pilihan == '4':
            item_id = int(input("Masukkan ID item untuk dikemas kini: "))
            name = input("Masukkan nama item baru: ")
            quantity = int(input("Masukkan kuantiti baru: "))
            price = float(input("Masukkan harga baru: "))
            if validate_input(name, quantity, price):
                kemas_kini_item(item_id, name, quantity, price)

        elif pilihan == '5':
            cari_value = input("Masukkan nama atau ID item untuk dicari: ")
            cari_item(cari_value)

        elif pilihan == '6':
            export_to_csv()

        elif pilihan == '7':
            import_from_csv()

        elif pilihan == '8':
            check_low_stock()

        elif pilihan == '9':
            generate_report()

        elif pilihan == '10':
            break

        else:
            print("Pilihan tidak sah, sila masukkan pilihan yang betul.")

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

if __name__ == "__main__":
    main()
