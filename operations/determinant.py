def find_determinant(matrix):
    if len(matrix) != len(matrix[0]):
        raise ValueError("Matrix harus persegi")
    if len(matrix) == 1:
        return matrix[0][0]
    if len(matrix) == 2:
        return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]

    determinant = 0
    for c in range(len(matrix)):
        minor = [row[:c] + row[c+1:] for row in matrix[1:]]
        determinant += ((-1)**c) * matrix[0][c] * find_determinant(minor)
    return determinant
