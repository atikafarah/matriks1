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
