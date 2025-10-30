# ml/linear_regression.py
# Linear Regression via Normal Equation:
#     theta = (X^T X + λI)^(-1) X^T y
# Kompatibel dengan struktur repo (matrix.py di root, operasi di operations/).

from typing import List, Sequence, Optional, Union
from matrix import Matrix
from operations.multiplier import multiply_matrices
from operations.transpose import transpose_matrix      # fungsi transpose (bukan method)
from operations.inverse import inverse_matrix           # fungsi inverse (bukan method)

AnyMatrix = Union[Matrix, list]  # hasil operasi bisa Matrix atau list of lists


def _as_matrix(obj: AnyMatrix) -> Matrix:
    """
    Pastikan keluaran operasi menjadi Matrix.
    - Jika sudah Matrix -> kembalikan apa adanya.
    - Jika list of lists -> bungkus ke Matrix.
    """
    if isinstance(obj, Matrix):
        return obj
    if isinstance(obj, list):
        return Matrix(obj)
    raise TypeError(f"Tipe tak didukung untuk konversi Matrix: {type(obj)}")


def _add_intercept(X: Matrix) -> Matrix:
    """Tambah kolom konstanta 1 di kiri (untuk intercept)."""
    data = [[1.0] + row for row in X.data]
    return Matrix(data)


def _identity(n: int) -> Matrix:
    """Buat matriks identitas n x n."""
    return Matrix([[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)])


class LinearRegression:
    """
    Linear Regression berbasis operasi matriks internal.
    Parameter:
        fit_intercept: bool  -> jika True, tambahkan kolom bias 1
        l2           : float -> koefisien Ridge (0.0 = tanpa regularisasi)
    Atribut:
        theta        : Matrix (p x 1), parameter hasil training
        n_features_  : jumlah fitur input (tanpa intercept)
    """

    def __init__(self, fit_intercept: bool = True, l2: float = 0.0):
        self.fit_intercept = fit_intercept
        self.l2 = float(l2)
        self.theta: Optional[Matrix] = None
        self.n_features_: Optional[int] = None

    def fit(self, X: Sequence[Sequence[float]], y: Sequence[float]) -> "LinearRegression":
        """
        Latih model dengan Normal Equation:
            theta = (X^T X + λI)^(-1) X^T y
        X: list of lists (n_samples x n_features)
        y: list (n_samples,)
        """
        # 1) Bungkus ke Matrix
        X_m = Matrix([list(map(float, row)) for row in X])
        y_m = Matrix([[float(v)] for v in y])  # column vector (n x 1)

        # 2) Tambah intercept bila diminta
        if self.fit_intercept:
            X_m = _add_intercept(X_m)

        # 3) Hitung komponen normal equation (pakai fungsi operations/*)
        XT = _as_matrix(transpose_matrix(X_m))                  # X^T (pastikan Matrix)
        XTX = _as_matrix(multiply_matrices(XT, X_m))            # X^T X

        # 4) Ridge (opsional): tambahkan λ pada diagonal agar invertible/stabil
        if self.l2 > 0.0:
            r, c = XTX.rows, XTX.cols
            XTX = Matrix([
                [XTX.data[i][j] + (self.l2 if i == j else 0.0) for j in range(c)]
                for i in range(r)
            ])

        # 5) Invers & hitung theta
        XTX_inv = _as_matrix(inverse_matrix(XTX))               # (X^T X + λI)^(-1)
        XTy = _as_matrix(multiply_matrices(XT, y_m))            # X^T y
        self.theta = _as_matrix(multiply_matrices(XTX_inv, XTy))  # (p x 1)

        # 6) Simpan jumlah fitur asli (tanpa kolom intercept)
        self.n_features_ = X_m.cols - (1 if self.fit_intercept else 0)
        return self

    def predict(self, X: Sequence[Sequence[float]]) -> List[float]:
        """Prediksi nilai y untuk input X."""
        if self.theta is None:
            raise RuntimeError("Model belum di-fit. Panggil fit() terlebih dahulu.")

        X_m = Matrix([list(map(float, row)) for row in X])
        if self.fit_intercept:
            X_m = _add_intercept(X_m)

        yhat = _as_matrix(multiply_matrices(X_m, self.theta))   # (n x 1)
        return [row[0] for row in yhat.data]

    def score(self, X: Sequence[Sequence[float]], y: Sequence[float]) -> float:
        """R^2 score (koefisien determinasi)."""
        y = [float(v) for v in y]
        yhat = self.predict(X)
        ybar = sum(y) / len(y)
        ss_tot = sum((v - ybar) ** 2 for v in y)
        ss_res = sum((yi - yh) ** 2 for yi, yh in zip(y, yhat))
        return 1.0 - (ss_res / ss_tot if ss_tot != 0 else 0.0)
