# Basic Inventory System

Sistem Inventori Asas ini adalah aplikasi Python yang membolehkan pengguna menguruskan inventori dengan ciri-ciri seperti menambah, mengemaskini, mencari dan membuang item dari inventori. Aplikasi ini menggunakan SQLite untuk pengurusan data dan `tabulate` untuk paparan data yang lebih kemas. Antaramuka pengguna grafikal (GUI) dibuat menggunakan Tkinter.

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
- **Daftar Pengguna Baru**: Tambah pengguna baru ke dalam sistem.
- **Cetak Inventori ke PDF**: Cetak inventori ke dalam fail PDF.

## Keperluan

- Python 3.x
- SQLite (termasuk dalam Python standard library)
- Library `tabulate`
- Library `fpdf`
- Library `tkinter` (biasanya sudah disertakan dalam Python)

## Pemasangan

1. Clone repositori atau muat turun fail `inventory_system_gui.py`, `utils.py`, dan `user_management.py` dari GitHub:
    ```sh
    git clone https://github.com/HafizalJohari/basic-inventory.git
    cd basic-inventory
    ```

2. Pasang keperluan menggunakan pip:
    ```sh
    pip install -r requirements.txt
    ```

## Penggunaan

1. Jalankan fail `inventory_system_gui.py` menggunakan Python:
    ```sh
    python inventory_system_gui.py
    ```
2. Ikut arahan yang dipaparkan dalam GUI untuk menguruskan inventori.

## Muat Turun

Anda boleh memuat turun projek ini secara langsung dari [GitHub](https://github.com/HafizalJohari/basic-inventory) dengan mengklik butang `Code` dan memilih `Download ZIP`, atau dengan menggunakan arahan git di atas.

MIT License

Copyright (c) 2024 Hafizal Johari

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR AN

