from matriks.matrix import Matrix
from matriks.operations.adder import add_matrices
from matriks.operations.subtractor import subtract_matrices
from matriks.operations.multiplier import multiply_matrices
from matriks.utilities import print_matrix
from exporters.csv_exporter import export_to_csv

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

    matrix_c = Matrix([[10, 20], [30, 40]])
    print("\nMenyimpan Matriks C ke file CSV:")
    export_to_csv(matrix_c, "matriks_c.csv")
