from sqlalchemy.orm import Session
from datetime import datetime

from app.models.harga import Harga

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np

def get_harga_bulan_ini_dan_lalu(db: Session):
    today = datetime.today()
    bulan_ini = today.month
    tahun_ini = today.year

    # Hitung bulan lalu
    if bulan_ini == 1:
        bulan_lalu = 12
        tahun_lalu = tahun_ini - 1
    else:
        bulan_lalu = bulan_ini - 1
        tahun_lalu = tahun_ini

    harga_bulan_ini = (
        db.query(Harga)
        .filter(Harga.bulan == bulan_ini, Harga.tahun == tahun_ini)
        .first()
    )

    harga_bulan_lalu = (
        db.query(Harga)
        .filter(Harga.bulan == bulan_lalu, Harga.tahun == tahun_lalu)
        .first()
    )

    return {
        "harga_bulan_ini": harga_bulan_ini.harga if harga_bulan_ini else 0,
        "harga_bulan_lalu": harga_bulan_lalu.harga if harga_bulan_lalu else 0,
    }
def predict_harga_bulan_depan(db: Session):
    today = datetime.today()
    bulan_ini = today.month
    tahun_ini = today.year
    
    tahun_3_tahun_lalu = tahun_ini - 3
    
    data = (
        db.query(Harga)
        .filter(Harga.tahun >= tahun_3_tahun_lalu)
        .order_by(Harga.tahun, Harga.bulan)
        .all()
    )
    
    if len(data) < 24:  # minimal 2 tahun data untuk model lebih baik
        return None, None  # error, data kurang
    
    # Siapkan data fitur dan target
    X = []
    y = []
    for row in data:
        total_bulan = row.tahun * 12 + row.bulan
        X.append([total_bulan, row.curah_hujan])
        y.append(row.harga)
    
    X = np.array(X)
    y = np.array(y)
    
    # Split train-test (misal 80-20)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
    # Normalisasi fitur
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Model Linear Regression
    model = LinearRegression()
    model.fit(X_train_scaled, y_train)
    
    # Evaluasi model sederhana
    y_pred_test = model.predict(X_test_scaled)
    mse = mean_squared_error(y_test, y_pred_test)
    
    # Prediksi bulan depan
    if bulan_ini == 12:
        bulan_depan = 1
        tahun_depan = tahun_ini + 1
    else:
        bulan_depan = bulan_ini + 1
        tahun_depan = tahun_ini
    total_bulan_depan = tahun_depan * 12 + bulan_depan
    
    # Kita butuh curah hujan bulan depan, tapi ini prediksi kasar. Bisa pakai rata-rata 3 tahun terakhir bulan yang sama
    curah_hujan_bulan_depan = get_avg_curah_hujan_bulan(db, bulan_depan)
    
    X_pred = np.array([[total_bulan_depan, curah_hujan_bulan_depan]])
    X_pred_scaled = scaler.transform(X_pred)
    
    harga_prediksi = model.predict(X_pred_scaled)[0]
    
    return round(float(harga_prediksi), 2), round(float(mse), 2)


def get_avg_curah_hujan_bulan(db: Session, bulan: int):
    today = datetime.today()
    tahun_ini = today.year
    tahun_3_tahun_lalu = tahun_ini - 3
    
    data_curah = (
        db.query(Harga.curah_hujan)
        .filter(Harga.bulan == bulan, Harga.tahun >= tahun_3_tahun_lalu)
        .all()
    )
    if not data_curah:
        return 0.0
    
    total = sum([c[0] for c in data_curah])
    return total / len(data_curah)

