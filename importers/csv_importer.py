import csv
from typing import List
from matrix import Matrix

def import_from_csv(path: str, delimiter: str = ",", has_header: bool = False) -> Matrix:
    rows: List[List[str]] = []
    with open(path, newline="") as f:
        reader = csv.reader(f, delimiter=delimiter)
        for i, row in enumerate(reader):
            if not row:
                continue
            if has_header and i == 0:
                continue
            rows.append(row)

    if not rows:
        raise ValueError("CSV kosong atau tidak terbaca.")

    try:
        numeric_rows = [[float(x) for x in r] for r in rows]
    except Exception as e:
        raise ValueError(f"CSV berisi nilai non-numerik: {e}")

    return Matrix(numeric_rows)
