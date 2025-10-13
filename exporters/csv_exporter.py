# matriks/exporters/csv_exporter.py
import csv

def export_to_csv(matriks, nama_file):
    """
    Mengekspor data matriks ke file CSV.
    """
    try:
        # 1. Buka file dalam mode tulis
        with open(nama_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # 2. Tulis setiap baris data dari matriks ke file
            for row in matriks.data:
                writer.writerow(row)

        # 3. Pesan sukses
        print(f"Data matriks berhasil diekspor ke file CSV: {nama_file}")

    except Exception as e:
        print(f"Gagal mengekspor ke CSV: {e}")

