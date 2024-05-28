import sqlite3
import csv
from tabulate import tabulate
from utils import validate_input, log_activity, authenticate, check_low_stock, generate_report
from user_management import register_user
from fpdf import FPDF

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

# Fungsi untuk mencetak inventori ke fail PDF
def print_inventory_to_pdf(filename='inventory.pdf'):
    cursor.execute('SELECT * FROM inventory')
    items = cursor.fetchall()
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Header
    pdf.cell(200, 10, txt="Inventory Report", ln=True, align='C')
    
    # Table header
    pdf.cell(40, 10, txt="ID", border=1)
    pdf.cell(60, 10, txt="Nama", border=1)
    pdf.cell(40, 10, txt="Kuantiti", border=1)
    pdf.cell(40, 10, txt="Harga (RM)", border=1)
    pdf.ln()
    
    # Table data
    for item in items:
        pdf.cell(40, 10, txt=str(item[0]), border=1)
        pdf.cell(60, 10, txt=item[1], border=1)
        pdf.cell(40, 10, txt=str(item[2]), border=1)
        pdf.cell(40, 10, txt=str(item[3]), border=1)
        pdf.ln()
    
    pdf.output(filename)
    print(f"Inventori telah dicetak ke {filename}.")

# Fungsi untuk paparan menu utama
def menu_utama():
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
        print("10. Cetak inventori ke PDF")
        print("11. Keluar")
        pilihan = input("Masukkan pilihan (1/2/3/4/5/6/7/8/9/10/11): ")

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
            check_low_stock(cursor)

        elif pilihan == '9':
            generate_report(cursor)

        elif pilihan == '10':
            print_inventory_to_pdf()

        elif pilihan == '11':
            break

        else:
            print("Pilihan tidak sah, sila masukkan pilihan yang betul.")

# Fungsi selamat datang untuk pilih login atau daftar pengguna baru
def selamat_datang():
    while True:
        print("\nSelamat Datang ke Sistem Inventory")
        print("1. Login")
        print("2. Daftar Pengguna Baru")
        pilihan = input("Masukkan pilihan (1/2): ")

        if pilihan == '1':
            if authenticate(cursor):
                menu_utama()
                break
            else:
                print("Login gagal. Sila cuba lagi.")

        elif pilihan == '2':
            register_user(cursor, conn)

        else:
            print("Pilihan tidak sah, sila masukkan pilihan yang betul.")

if __name__ == "__main__":
    selamat_datang()
