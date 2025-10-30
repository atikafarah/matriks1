from matrix import Matrix
from operations.adder import add_matrices
from operations.subtractor import subtract_matrices
from operations.multiplier import multiply_matrices
from utilitiesp import print_matrix
from exporters.csv_exporter import export_to_csv
import time
from operations.multiplier import multiply_matrices
from sparsematrix import SparseMatrix
from operations.multiplier import multiply_matrices
from exporters.csv_exporter import export_to_csv
from exporters.json_exporter import export_to_json
from operations.inverse import inverse_matrix
from operations.transpose import transpose_matrix
from importers.csv_importer import import_from_csv

def create_sparse_data(size):
    data = [[0] * size for _ in range(size)]
    data[0][0] = 1
    data[size-1][size-1] = 1
    return data

if __name__ == "__main__":
    matriks_a = Matrix([[1, 2], [3, 4]])
    matriks_b = Matrix([[5, 6], [7, 8]])

    print("Hasil Penjumlahan:")
    hasil_penjumlahan = add_matrices(matriks_a, matriks_b)
    print_matrix(hasil_penjumlahan)

    print("\nHasil Pengurangan:")
    hasil_pengurangan = subtract_matrices(matriks_a, matriks_b)
    print_matrix(hasil_pengurangan)

    print("\nHasil Perkalian:")
    hasil_perkalian = multiply_matrices(matriks_a, matriks_b)
    print_matrix(hasil_perkalian)

    print("\nHasil Inverse:")
    hasil_invers = inverse_matrix(matriks_a)
    print_matrix(hasil_invers)

    print("\nHasil Transpose:")
    hasil_transpose = transpose_matrix(matriks_a)
    print_matrix(hasil_transpose)

    print("\nDemo Import CSV")
    m_csv = import_from_csv("data/mat_2x2.csv", has_header=False)
    print_matrix(m_csv)
