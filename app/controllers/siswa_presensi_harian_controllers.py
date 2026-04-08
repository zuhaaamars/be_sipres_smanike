import os
import base64
import uuid
from flask import request, jsonify
from datetime import datetime
from app.app import db
from app.models.siswa_presensi_harian_models import PresensiHarian

UPLOAD_PATH = 'static/uploads/presensi/harian'

def save_harian_image(image_base64):
    if not image_base64 or "," not in image_base64:
        return None
    
    try:
        header, encoded = image_base64.split(",", 1)
        data = base64.b64decode(encoded)
        
        if not os.path.exists(UPLOAD_PATH):
            os.makedirs(UPLOAD_PATH)
            
        filename = f"{uuid.uuid4().hex}.png"
        filepath = os.path.join(UPLOAD_PATH, filename)
        
        with open(filepath, "wb") as f:
            f.write(data)
        return filepath
    except Exception as e:
        print(f"Error saving image: {str(e)}")
        return None

def submit_presensi_harian():
    # 1. TANGANI REQUEST OPTIONS (Jabat tangan CORS)
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200

    # 2. BACA DATA JSON (Hanya jika method POST)
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Data JSON tidak ditemukan"}), 415

    siswa_id = data.get('siswa_id')
    
    # Validasi: Pastikan siswa_id dikirim dari React
    if not siswa_id:
        return jsonify({"status": "error", "message": "Siswa ID wajib diisi"}), 400

    foto = save_harian_image(data.get('image'))
    hari_ini = datetime.now().date()

    try:
        # Cari apakah sudah ada absen hari ini
        record = PresensiHarian.query.filter_by(siswa_id=siswa_id, tanggal=hari_ini).first()

        if not record:
            # Absen Masuk
            new_entry = PresensiHarian(
                siswa_id=siswa_id,
                tanggal=hari_ini, # Tambahkan field tanggal jika ada di model
                jam_masuk=datetime.now(),
                foto_bukti=foto,
                latitude=data.get('latitude'),
                longitude=data.get('longitude')
            )
            db.session.add(new_entry)
            msg = "Berhasil Absen Masuk"
        else:
            # Absen Pulang
            if record.jam_pulang:
                return jsonify({"status": "error", "message": "Anda sudah absen pulang hari ini"}), 400
            
            record.jam_pulang = datetime.now()
            msg = "Berhasil Absen Pulang"
        
        db.session.commit()
        return jsonify({"status": "success", "message": msg}), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error Database: {str(e)}")
        return jsonify({"status": "error", "message": f"Gagal simpan ke database: {str(e)}"}), 500
    
def get_riwayat_presensi(siswa_id):
    try:
        # Ambil semua data absen untuk siswa_id tersebut, urutkan dari yang terbaru
        riwayat = PresensiHarian.query.filter_by(siswa_id=siswa_id).order_by(PresensiHarian.tanggal.desc()).all()
        
        output = []
        for r in riwayat:
            output.append({
                "id": r.id,
                "tanggal": r.tanggal.strftime('%Y-%m-%d'),
                "jam_masuk": r.jam_masuk.strftime('%H:%M:%S') if r.jam_masuk else "-",
                "jam_pulang": r.jam_pulang.strftime('%H:%M:%S') if r.jam_pulang else "-",
                "status": r.status
            })
        
        return jsonify({"status": "success", "data": output}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500