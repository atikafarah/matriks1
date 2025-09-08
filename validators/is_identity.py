def is_identity(matriks):
    # 1. Periksa apakah matriks adalah matriks persegi
    if matriks.jumlah_baris != matriks.jumlah_kolom:
        return False

    # 2. Periksa elemen-elemen matriks
    for i in range(matriks.jumlah_baris):
        for j in range(matriks.jumlah_kolom):
            if i == j:
                if matriks.data[i][j] != 1:
                    return False
            else:
                if matriks.data[i][j] != 0:
                    return False

    # 3. Jika semua elemen sesuai, matriks adalah identitas
    return True
