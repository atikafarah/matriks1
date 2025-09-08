def print_matrix(matrix):
    """
    Mencetak isi dari objek matriks.
    """
    for row in matrix.data:
        print(row)

def find_determinant(matrix):
    # Asumsi: matrix adalah list of list, square
    if len(matrix) != len(matrix[0]):
        raise ValueError("Matrix harus persegi")
    if len(matrix) == 1:
        return matrix[0][0]
    if len(matrix) == 2:
        return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]

    # Rekursif untuk ukuran lebih besar
    determinant = 0
    for c in range(len(matrix)):
        minor = [row[:c] + row[c+1:] for row in matrix[1:]]
        determinant += ((-1)**c) * matrix[0][c] * find_determinant(minor)
    return determinant

def is_square(matrix):
    return len(matrix) == len(matrix[0])

def is_symmetric(matrix):
    if len(matrix) != len(matrix[0]):
        return False
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] != matrix[j][i]:
                return False
    return True
