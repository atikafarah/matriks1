# operations/invers.py
import numpy as np

def inverse_matrix(matrix):
    """
    Menghitung invers matriks menggunakan numpy.
    Parameter:
        matrix (Matrix atau list of lists)
    Return:
        Matrix hasil invers (list of lists)
    """
    try:
        # Ambil data mentah kalau yang dikasih adalah objek Matrix
        data = matrix.data if hasattr(matrix, "data") else matrix

        arr = np.array(data, dtype=float)
        inv = np.linalg.inv(arr)

        return inv.tolist()

    except np.linalg.LinAlgError:
        print("Terjadi kesalahan saat menghitung invers: determinan = 0 (tidak bisa di-invers).")
        return None
    except Exception as e:
        print("Terjadi kesalahan saat menghitung invers:", e)
        return None
