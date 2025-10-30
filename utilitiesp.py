def print_matrix(matrix):
    """
    Mencetak isi dari objek matriks atau list of lists.
    """
    # cek apakah input punya atribut .data (objek Matrix)
    data = matrix.data if hasattr(matrix, "data") else matrix

    for row in data:
        print(row)
