import numpy as np

def transpose_matrix(matrix):
    try:
        data = np.array(matrix.data)
        transposed = np.transpose(data)
        return transposed.tolist()  # pastikan dikonversi ke list
    except Exception as e:
        print(f"Terjadi kesalahan saat transpose: {e}")
        return None
