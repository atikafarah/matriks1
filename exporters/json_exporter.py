import json

def export_to_json(matriks, nama_file):
    """
    Mengekspor data matriks ke file JSON.
    """
    try:
        # 1. Ubah data matriks jadi list (misalnya list of lists)
        data = matriks.data

        # 2. Konversi ke string JSON
        json_str = json.dumps(data)

        # 3. Buka file dalam mode tulis
        with open(nama_file, mode='w', encoding='utf-8') as file:
            # 4. Tulis JSON ke dalam file
            file.write(json_str)

        # 5. Pesan sukses
        print(f"Data matriks berhasil diekspor ke file JSON: {nama_file}")

    except Exception as e:
        print(f"Gagal mengekspor ke JSON: {e}")
