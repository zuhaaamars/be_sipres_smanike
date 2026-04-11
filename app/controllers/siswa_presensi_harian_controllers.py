import os
import base64
import uuid
from sqlalchemy import and_
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
    
# REKAP GURU
def get_rekap_harian_guru():
    try:
        from app.models.siswa_models import Siswa
        from app.models.user_models import User
        from app.models.master.kelas_models import Kelas

        # PERBAIKAN: Kita ambil nama_lengkap dari model Siswa, bukan User
        results = db.session.query(
            PresensiHarian.tanggal,
            Siswa.nisn,
            Siswa.nama_lengkap, # Diubah: Siswa punya attribute nama_lengkap
            Kelas.nama_kelas,
            PresensiHarian.jam_masuk,
            PresensiHarian.jam_pulang,
            PresensiHarian.status,
            PresensiHarian.foto_bukti,
            PresensiHarian.latitude,
            PresensiHarian.id
        ).join(Siswa, PresensiHarian.siswa_id == Siswa.id)\
         .join(Kelas, Siswa.kelas_id == Kelas.id)\
         .order_by(PresensiHarian.tanggal.desc(), PresensiHarian.jam_masuk.desc())\
         .all()

        output = []
        for r in results:
            # Format tanggal Indonesia sederhana
            tgl_indo = r.tanggal.strftime('%d/%m/%y') if r.tanggal else "-"
            
            # Bersihkan path foto agar tidak error di browser
            foto_url = None
            if r.foto_bukti:
                foto_clean = r.foto_bukti.replace('\\', '/')
                foto_url = f"http://localhost:5000/{foto_clean}"

            output.append({
                "id": r.id,
                "nis": r.nisn or "-",
                "nama": r.nama_lengkap, # Sekarang mengambil data yang benar
                "kelas": f"{r.nama_kelas} ({tgl_indo})", 
                "waktuMasuk": r.jam_masuk.strftime('%H:%M') if r.jam_masuk else "-",
                "waktuPulang": r.jam_pulang.strftime('%H:%M') if r.jam_pulang else "-",
                "status": r.status if r.status else "Hadir",
                "foto": foto_url,
                "jarak": "Terdeteksi" if r.latitude else "-",
                "wa": "Terkirim" if r.jam_masuk else "Pending",
                "validated": True if r.status == "Hadir" else False
            })

        return jsonify({"status": "success", "data": output}), 200
    except Exception as e:
        # Print error ke terminal Flask agar kamu bisa lihat detailnya
        print(f"Error pada Rekap Guru: {str(e)}")
        return jsonify({"status": "error", "message": f"Server Error: {str(e)}"}), 500