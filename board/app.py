from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os, json, sys, glob
import pandas as pd
import plotly.express as px
from config import Config
from pathlib import Path

# ====== Pastikan bisa import modul buatan Farah dari root repo ======
ROOT_DIR = Path(__file__).resolve().parent.parent  # .../matriks1
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Modul ML Farah (akan dipakai di /visualize → regression)
try:
    from ml.linear_regression import LinearRegression
    from ml.utils import train_test_split
except Exception as e:
    # tidak fatal untuk /about; fatalnya hanya saat regression dipanggil
    LinearRegression = None
    train_test_split = None

app = Flask(__name__, instance_relative_config=True, static_folder="static", template_folder="templates")
app.config.from_object(Config)

CURRENT_DF = None
CURRENT_NAME = None

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

# ====== Loader robust untuk day.csv ======
def load_day_csv():
    """
    Cari & baca 'day.csv' dari beberapa lokasi umum, bisa override via ENV DAY_CSV_PATH.
    Autodetect delimiter (',' atau ';') dan fallback encoding (utf-8 → latin1).
    """
    bases = [
        Path(app.root_path) / "data",
        Path(app.root_path) / "instance" / "uploads",
        ROOT_DIR / "board" / "data",
        ROOT_DIR / "data",
    ]
    env = os.environ.get("DAY_CSV_PATH")
    if env:
        cands = [Path(env)]
    else:
        cands = [b / "day.csv" for b in bases]
        # cari pola day*.csv jika nama tidak persis
        for b in bases:
            for g in glob.glob(str(b / "day*.csv")):
                cands.append(Path(g))

    found = next((p for p in cands if p.exists()), None)
    if not found:
        return None, "File board/data/day.csv belum tersedia. Letakkan file di sana atau set ENV DAY_CSV_PATH.", None

    try:
        df = pd.read_csv(found, sep=None, engine="python", encoding="utf-8")
    except Exception:
        try:
            df = pd.read_csv(found, sep=None, engine="python", encoding="latin1")
        except Exception as e:
            return None, f"Gagal membaca {found}: {e}", str(found)
    return df, None, str(found)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    # Deskripsi kolom dataset Bike Sharing (UCI)
    col_desc = {
        "instant": "Index record (ID baris).",
        "dteday": "Tanggal (YYYY-MM-DD).",
        "season": "Musim (1: semi, 2: panas, 3: gugur, 4: dingin).",
        "yr": "Tahun (0:2011, 1:2012).",
        "mnth": "Bulan (1–12).",
        "holiday": "Hari libur (0/1).",
        "weekday": "Hari (0:Min … 6:Sab).",
        "workingday": "Hari kerja (1).",
        "weathersit": "Kondisi cuaca (1 baik → 4 buruk).",
        "temp": "Suhu ternormalisasi (0–1).",
        "atemp": "Suhu terasa (0–1).",
        "hum": "Kelembapan (0–1).",
        "windspeed": "Kecepatan angin (0–1).",
        "casual": "Penyewa kasual / hari.",
        "registered": "Penyewa terdaftar / hari.",
        "cnt": "Total penyewaan / hari (casual + registered).",
    }

    df, error, used_path = load_day_csv()

    narrative = (
        "Dataset ini berisi catatan penyewaan sepeda harian, lengkap dengan tanggal, musim, indikator hari kerja/libur, "
        "kondisi cuaca (temperatur, kelembapan, kecepatan angin), dan jumlah penyewaan kasual, terdaftar, serta total. "
        "Cocok untuk analisis pola permintaan, pengaruh cuaca & musim, dan perbedaan hari kerja vs akhir pekan."
    )

    if isinstance(df, pd.DataFrame):
        head_rows = df.head(5).to_dict(orient="records")
        columns = list(df.columns)
        meta = {
            "dataset_name": f"day.csv (Bike Sharing — harian) — {used_path}",
            "rows": len(df),
            "cols": len(df.columns),
            "columns": columns,
            "expected_note": "(Ekspektasi: 731 baris × 16 kolom)",
        }
    else:
        head_rows, columns, meta = [], [], {
            "dataset_name": "Belum ada dataset diunggah",
            "rows": 0, "cols": 0, "columns": [],
            "expected_note": "(Ekspektasi: 731 baris × 16 kolom)",
        }

    return render_template(
        "about.html",
        meta=meta, columns=columns, head_rows=head_rows,
        col_desc=col_desc, narrative=narrative, error=error
    )

@app.route("/upload", methods=["POST"])
def upload():
    # route lama—biarkan ada, tapi halaman About tidak menampilkan form
    global CURRENT_DF, CURRENT_NAME
    if "file" not in request.files:
        flash("Tidak ada berkas pada form.", "error")
        return redirect(url_for("about"))
    file = request.files["file"]
    if file.filename == "":
        flash("Nama file kosong.", "error")
        return redirect(url_for("about"))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(save_path)
        try:
            df = pd.read_csv(save_path)
            CURRENT_DF = df
            CURRENT_NAME = filename
            flash(f"Dataset '{filename}' berhasil dimuat. {df.shape[0]} baris x {df.shape[1]} kolom.", "success")
        except Exception as e:
            flash(f"Gagal membaca CSV: {e}", "error")
    else:
        flash("Format file tidak didukung. Upload .csv", "error")
    return redirect(url_for("about"))

@app.route("/visualize", methods=["GET","POST"])
def visualize():
    """
    - GET: tampilkan tombol 'Jalankan Regresi' + (opsi) form chart umum.
    - POST (mode=regression): jalankan regresi dengan modul Farah dan tampilkan plot y_true vs y_pred.
    """
    df, error, used_path = load_day_csv()
    columns = list(df.columns) if isinstance(df, pd.DataFrame) else []
    chartJSON, chart_title = None, None
    metrics = None
    reg_error = None

    if request.method == "POST":
        mode = request.form.get("mode")
        if mode == "regression":
            if df is None:
                reg_error = "Dataset belum tersedia. Pastikan board/data/day.csv ada."
            elif LinearRegression is None or train_test_split is None:
                reg_error = "Modul ML belum bisa di-import. Pastikan struktur repo sesuai (folder ml/)."
            else:
                try:
                    features = ["temp", "atemp", "hum", "windspeed"]
                    target = "cnt"
                    use = df.dropna(subset=features + [target]).copy()

                    X = use[features].values.tolist()
                    y = use[target].values.tolist()

                    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, seed=42)
                    lr = LinearRegression(fit_intercept=True, l2=1e-6).fit(X_tr, y_tr)
                    r2_tr = lr.score(X_tr, y_tr)
                    r2_te = lr.score(X_te, y_te)
                    y_pred = lr.predict(X_te)

                    # Plot: y_true vs y_pred
                    fig = px.scatter(x=y_te, y=y_pred, labels={"x":"y True (cnt)", "y":"y Pred (cnt)"},
                                     title="")
                    # garis y=x
                    fig.add_shape(type="line", x0=min(y_te), y0=min(y_te), x1=max(y_te), y1=max(y_te),
                                  line=dict(dash="dash"))
                    fig.update_layout(
                        paper_bgcolor="#FFFFFF",
                        plot_bgcolor="#FFFDD0",
                        margin=dict(l=40,r=20,t=40,b=40),
                        font=dict(size=14),
                    )
                    chart_title = "Regresi Linear — y_true vs y_pred (Test)"
                    chartJSON = fig.to_json()
                    metrics = {
                        "r2_train": round(r2_tr, 4),
                        "r2_test": round(r2_te, 4),
                        "n_train": len(X_tr),
                        "n_test": len(X_te),
                        "used_path": used_path,
                        "features": features,
                        "target": target,
                    }
                except Exception as e:
                    reg_error = f"Gagal menjalankan regresi: {e}"

    return render_template(
        "visualize.html",
        columns=columns,
        chartJSON=chartJSON, chart_title=chart_title,
        error=error, reg_error=reg_error, metrics=metrics
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

