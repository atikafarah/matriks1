def is_symmetric(matriks):
    # 1. Periksa apakah matriks adalah matriks persegi
    if matriks.jumlah_baris != matriks.jumlah_kolom:
        return False

    # 2. Periksa apakah elemen (i, j) sama dengan elemen (j, i)
    for i in range(matriks.jumlah_baris):
        for j in range(matriks.jumlah_kolom):
            if matriks.data[i][j] != matriks.data[j][i]:
                return False

    # 3. Jika semua elemen sesuai, matriks adalah simetris
    return True
