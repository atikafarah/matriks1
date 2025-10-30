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
from ml.linear_regression import LinearRegression
from ml.utils import train_test_split
import pandas as pd

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

    print("\nDemo Linear Regression (Bike Sharing: day.csv)")
    try:
        # Pastikan file dataset ada di data/day.csv
        df = pd.read_csv("data/day.csv", delimiter=";")

        features = ["temp", "atemp", "hum", "windspeed"]
        target = "cnt"

        # pastikan tidak ada NaN di kolom yang dipakai
        df = df.dropna(subset=features + [target])

        X = df[features].values.tolist()
        y = df[target].values.tolist()

        # split sederhana
        X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, seed=42)

        # fit (pakai intercept & ridge kecil agar stabil)
        lr = LinearRegression(fit_intercept=True, l2=1e-6).fit(X_tr, y_tr)

        # evaluasi
        r2_tr = lr.score(X_tr, y_tr)
        r2_te = lr.score(X_te, y_te)
        print(f"R^2 train: {r2_tr:.4f} | R^2 test: {r2_te:.4f}")

        # contoh prediksi 5 data test
        preds = lr.predict(X_te[:5])
        for i, (xh, yh, ph) in enumerate(zip(X_te[:5], y_te[:5], preds), 1):
            print(f"{i}. X={xh} → y_true={yh:.1f}, y_pred={ph:.1f}")

        # (opsional) simpan plot hasil
        # import matplotlib.pyplot as plt
        # y_pred_all = lr.predict(X_te)
        # plt.figure(); plt.scatter(y_te, y_pred_all, s=10)
        # plt.xlabel("y True (cnt)"); plt.ylabel("y Pred (cnt)")
        # plt.title("Bike Sharing: y_true vs y_pred (Test)")
        # plt.savefig("data/regression_scatter.png")
        # print("Plot disimpan ke data/regression_scatter.png")

    except FileNotFoundError:
        print("[INFO] 'data/day.csv' tidak ditemukan. Taruh dataset UCI di folder data/.")
    except Exception as e:
        print(f"[INFO] Demo regresi gagal: {e}")
