import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter.simpledialog import askstring
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

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Inventori")
        self.create_welcome_screen()

    def create_welcome_screen(self):
        self.clear_screen()

        welcome_label = Label(self.root, text="Selamat Datang ke Sistem Inventory", font=("Arial", 16))
        welcome_label.pack(pady=20)

        login_button = Button(self.root, text="Login", command=self.login_screen, width=20)
        login_button.pack(pady=10)

        register_button = Button(self.root, text="Daftar Pengguna Baru", command=self.register_screen, width=20)
        register_button.pack(pady=10)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login_screen(self):
        self.clear_screen()

        username_label = Label(self.root, text="Nama Pengguna:")
        username_label.pack(pady=5)
        self.username_entry = Entry(self.root)
        self.username_entry.pack(pady=5)

        password_label = Label(self.root, text="Kata Laluan:")
        password_label.pack(pady=5)
        self.password_entry = Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        login_button = Button(self.root, text="Login", command=self.login, width=20)
        login_button.pack(pady=10)

        back_button = Button(self.root, text="Kembali", command=self.create_welcome_screen, width=20)
        back_button.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if authenticate(cursor, username, password):
            self.create_main_menu()
        else:
            messagebox.showerror("Login Gagal", "Nama pengguna atau kata laluan salah")

    def register_screen(self):
        self.clear_screen()

        username_label = Label(self.root, text="Nama Pengguna Baru:")
        username_label.pack(pady=5)
        self.new_username_entry = Entry(self.root)
        self.new_username_entry.pack(pady=5)

        password_label = Label(self.root, text="Kata Laluan Baru:")
        password_label.pack(pady=5)
        self.new_password_entry = Entry(self.root, show="*")
        self.new_password_entry.pack(pady=5)

        register_button = Button(self.root, text="Daftar", command=self.register, width=20)
        register_button.pack(pady=10)

        back_button = Button(self.root, text="Kembali", command=self.create_welcome_screen, width=20)
        back_button.pack(pady=10)

    def register(self):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()
        if register_user(cursor, conn, username, password):
            messagebox.showinfo("Pendaftaran Berjaya", f'Pengguna "{username}" telah didaftarkan')
            self.create_welcome_screen()
        else:
            messagebox.showerror("Pendaftaran Gagal", f'Pengguna "{username}" sudah wujud')

    def create_main_menu(self):
        self.clear_screen()

        main_menu_label = Label(self.root, text="Sistem Inventory", font=("Arial", 16))
        main_menu_label.pack(pady=20)

        buttons = [
            ("Paparkan inventory", self.display_inventory),
            ("Tambah item", self.add_item_screen),
            ("Buang item", self.delete_item_screen),
            ("Kemas kini item", self.update_item_screen),
            ("Cari item", self.search_item_screen),
            ("Eksport ke CSV", self.export_to_csv),
            ("Import dari CSV", self.import_from_csv_screen),
            ("Periksa stok rendah", self.check_low_stock_screen),
            ("Jana laporan", self.generate_report_screen),
            ("Cetak inventori ke PDF", self.print_inventory_to_pdf),
            ("Keluar", self.root.quit)
        ]

        for text, command in buttons:
            button = Button(self.root, text=text, command=command, width=30)
            button.pack(pady=5)

    def display_inventory(self):
        cursor.execute('SELECT * FROM inventory')
        items = cursor.fetchall()
        headers = ["ID", "Nama", "Kuantiti", "Harga (RM)"]
        display_text = tabulate(items, headers, tablefmt="grid")
        self.show_text_window("Inventori", display_text)

    def add_item_screen(self):
        self.clear_screen()

        name_label = Label(self.root, text="Nama Item:")
        name_label.pack(pady=5)
        self.name_entry = Entry(self.root)
        self.name_entry.pack(pady=5)

        quantity_label = Label(self.root, text="Kuantiti:")
        quantity_label.pack(pady=5)
        self.quantity_entry = Entry(self.root)
        self.quantity_entry.pack(pady=5)

        price_label = Label(self.root, text="Harga:")
        price_label.pack(pady=5)
        self.price_entry = Entry(self.root)
        self.price_entry.pack(pady=5)

        add_button = Button(self.root, text="Tambah", command=self.add_item, width=20)
        add_button.pack(pady=10)

        back_button = Button(self.root, text="Kembali", command=self.create_main_menu, width=20)
        back_button.pack(pady=10)

    def add_item(self):
        name = self.name_entry.get()
        quantity = int(self.quantity_entry.get())
        price = float(self.price_entry.get())
        if validate_input(name, quantity, price):
            cursor.execute('INSERT INTO inventory (name, quantity, price) VALUES (?, ?, ?)', (name, quantity, price))
            conn.commit()
            messagebox.showinfo("Berjaya", f'Item "{name}" telah ditambah')
            log_activity(f'Item ditambah: {name}, Kuantiti: {quantity}, Harga: {price}')
            self.create_main_menu()
        else:
            messagebox.showerror("Gagal", "Input tidak sah")

    def delete_item_screen(self):
        self.clear_screen()

        item_id_label = Label(self.root, text="ID Item untuk Dibuang:")
        item_id_label.pack(pady=5)
        self.item_id_entry = Entry(self.root)
        self.item_id_entry.pack(pady=5)

        delete_button = Button(self.root, text="Buang", command=self.delete_item, width=20)
        delete_button.pack(pady=10)

        back_button = Button(self.root, text="Kembali", command=self.create_main_menu, width=20)
        back_button.pack(pady=10)

    def delete_item(self):
        item_id = int(self.item_id_entry.get())
        cursor.execute('DELETE FROM inventory WHERE id = ?', (item_id,))
        conn.commit()
        messagebox.showinfo("Berjaya", f'Item dengan ID {item_id} telah dibuang')
        log_activity(f'Item dengan ID {item_id} dibuang')
        self.create_main_menu()

    def update_item_screen(self):
        self.clear_screen()

        item_id_label = Label(self.root, text="ID Item untuk Dikemas Kini:")
        item_id_label.pack(pady=5)
        self.item_id_entry = Entry(self.root)
        self.item_id_entry.pack(pady=5)

        name_label = Label(self.root, text="Nama Item Baru:")
        name_label.pack(pady=5)
        self.name_entry = Entry(self.root)
        self.name_entry.pack(pady=5)

        quantity_label = Label(self.root, text="Kuantiti Baru:")
        quantity_label.pack(pady=5)
        self.quantity_entry = Entry(self.root)
        self.quantity_entry.pack(pady=5)

        price_label = Label(self.root, text="Harga Baru:")
        price_label.pack(pady=5)
        self.price_entry = Entry(self.root)
        self.price_entry.pack(pady=5)

        update_button = Button(self.root, text="Kemas Kini", command=self.update_item, width=20)
        update_button.pack(pady=10)

        back_button = Button(self.root, text="Kembali", command=self.create_main_menu, width=20)
        back_button.pack(pady=10)

    def update_item(self):
        item_id = int(self.item_id_entry.get())
        name = self.name_entry.get()
        quantity = int(self.quantity_entry.get())
        price = float(self.price_entry.get())
        if validate_input(name, quantity, price):
            cursor.execute('''
            UPDATE inventory
            SET name = ?, quantity = ?, price = ?
            WHERE id = ?
            ''', (name, quantity, price, item_id))
            conn.commit()
            messagebox.showinfo("Berjaya", f'Item dengan ID {item_id} telah dikemas kini')
            log_activity(f'Item dengan ID {item_id} dikemas kini: {name}, Kuantiti: {quantity}, Harga: {price}')
            self.create_main_menu()
        else:
            messagebox.showerror("Gagal", "Input tidak sah")

    def search_item_screen(self):
        self.clear_screen()

        search_label = Label(self.root, text="Nama atau ID Item untuk Dicari:")
        search_label.pack(pady=5)
        self.search_entry = Entry(self.root)
        self.search_entry.pack(pady=5)

        search_button = Button(self.root, text="Cari", command=self.search_item, width=20)
        search_button.pack(pady=10)

        back_button = Button(self.root, text="Kembali", command=self.create_main_menu, width=20)
        back_button.pack(pady=10)

    def search_item(self):
        search_value = self.search_entry.get()
        cursor.execute('SELECT * FROM inventory WHERE name LIKE ? OR id LIKE ?', (f'%{search_value}%', f'%{search_value}%'))
        items = cursor.fetchall()
        headers = ["ID", "Nama", "Kuantiti", "Harga"]
        search_result = tabulate(items, headers, tablefmt="grid")
        self.show_text_window("Hasil Carian", search_result)

    def import_from_csv_screen(self):
        filename = askstring("Import CSV", "Masukkan nama fail CSV:")
        if filename:
            self.import_from_csv(filename)

    def check_low_stock_screen(self):
        threshold = askstring("Stok Rendah", "Masukkan ambang stok rendah:")
        if threshold:
            self.check_low_stock(int(threshold))

    def generate_report_screen(self):
        self.clear_screen()

        filename_label = Label(self.root, text="Nama fail laporan:")
        filename_label.pack(pady=5)
        self.filename_entry = Entry(self.root)
        self.filename_entry.pack(pady=5)

        generate_button = Button(self.root, text="Jana Laporan", command=self.generate_report, width=20)
        generate_button.pack(pady=10)

        back_button = Button(self.root, text="Kembali", command=self.create_main_menu, width=20)
        back_button.pack(pady=10)

    def show_text_window(self, title, text):
        text_window = Toplevel(self.root)
        text_window.title(title)
        text_area = Text(text_window, wrap='word', width=80, height=20)
        text_area.insert('1.0', text)
        text_area.config(state=DISABLED)
        text_area.pack(padx=10, pady=10)

    def export_to_csv(self, filename='inventory.csv'):
        cursor.execute('SELECT * FROM inventory')
        items = cursor.fetchall()
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Nama", "Kuantiti", "Harga"])
            writer.writerows(items)
        messagebox.showinfo("Berjaya", f"Data telah dieksport ke {filename}")

    def import_from_csv(self, filename='inventory.csv'):
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                cursor.execute('INSERT INTO inventory (id, name, quantity, price) VALUES (?, ?, ?, ?)', row)
            conn.commit()
        messagebox.showinfo("Berjaya", f"Data telah diimport dari {filename}")

    def check_low_stock(self, threshold=10):
        cursor.execute('SELECT * FROM inventory WHERE quantity < ?', (threshold,))
        items = cursor.fetchall()
        headers = ["ID", "Nama", "Kuantiti", "Harga"]
        low_stock_result = tabulate(items, headers, tablefmt="grid")
        self.show_text_window("Stok Rendah", low_stock_result)

    def generate_report(self):
        filename = self.filename_entry.get()
        cursor.execute('SELECT * FROM inventory')
        items = cursor.fetchall()
        with open(filename, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Nama", "Kuantiti", "Harga"])
            writer.writerows(items)
        messagebox.showinfo("Berjaya", f"Laporan telah dijana ke {filename}")

    def print_inventory_to_pdf(self, filename='inventory.pdf'):
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
        messagebox.showinfo("Berjaya", f"Inventori telah dicetak ke {filename}")

if __name__ == "__main__":
    root = Tk()
    app = InventoryApp(root)
    root.mainloop()
