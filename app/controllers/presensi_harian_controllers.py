import os, math
from flask import request, jsonify
from app import db
from app.models.presensi_harian.presensi_siswa_models import PresensiSiswa
from datetime import datetime
from werkzeug.utils import secure_filename

# Koordinat Pusat SMAN 1 Kedunggalar (Sesuaikan dengan aslinya)
SEKOLAH_LAT = -7.603496 
SEKOLAH_LON = 111.550720
RADIUS_KM = 0.05 # 50 Meter

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371 # Radius bumi dalam KM
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def absen_masuk_siswa(current_user_id):
    try:
        data = request.form
        file = request.files.get('foto')
        lat_siswa = float(data.get('latitude'))
        lon_siswa = float(data.get('longitude'))

        # 1. Cek Jarak Geofencing
        jarak = calculate_distance(lat_siswa, lon_siswa, SEKOLAH_LAT, SEKOLAH_LON)
        if jarak > RADIUS_KM:
            return jsonify({"status": "error", "message": "Anda di luar area sekolah"}), 403

        # 2. Proses Simpan Foto
        filename = None
        if file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = secure_filename(f"selfie_{current_user_id}_{timestamp}.jpg")
            file.save(os.path.join('app/static/uploads/presensi', filename))

        # 3. Tentukan Status (Contoh batas jam 07:15)
        now = datetime.now().time()
        status = 'Hadir' if now <= datetime.strptime("07:15", "%H:%M").time() else 'Terlambat'

        # 4. Simpan ke Database
        new_absen = PresensiSiswa(
            siswa_id=current_user_id, # Pastikan ini ID dari tabel siswa_profile
            tanggal=datetime.utcnow().date(),
            jam_masuk=now,
            latitude=lat_siswa,
            longitude=lon_siswa,
            foto_selfie=filename,
            status=status
        )
        db.session.add(new_absen)
        db.session.commit()

        return jsonify({"status": "success", "message": f"Absen berhasil! Status: {status}"}), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500