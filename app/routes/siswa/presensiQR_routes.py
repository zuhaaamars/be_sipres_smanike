from flask import Blueprint, request, jsonify
from app import db
from datetime import datetime, timedelta

# 🔹 Blueprint
presensi_bp = Blueprint('presensi_bp', __name__)

# =========================
# 🔥 POST: SIMPAN PRESENSI (DARI QR)
# =========================
@presensi_bp.route('/', methods=['POST'])
def tambah_presensi():
    try:
        data = request.json

        # 🔹 Ambil data dari QR
        mapel = data.get('mapel')
        kelas = data.get('kelas')
        jam = data.get('jam')
        waktu_qr = data.get('waktu')

        # 🔴 VALIDASI WAJIB
        if not mapel or not kelas or not jam or not waktu_qr:
            return jsonify({
                "status": "error",
                "message": "Data tidak lengkap"
            }), 400

        # 🔥 VALIDASI EXPIRED (5 menit)
        waktu_qr = datetime.fromisoformat(waktu_qr)
        sekarang = datetime.utcnow()

        if sekarang - waktu_qr > timedelta(minutes=5):
            return jsonify({
                "status": "error",
                "message": "QR sudah kadaluarsa"
            }), 400

        # 🔥 SIMPAN KE DATABASE (sementara tanpa model relasi)
        query = """
            INSERT INTO presensi (mapel, kelas, jam, waktu)
            VALUES (:mapel, :kelas, :jam, :waktu)
        """

        db.session.execute(query, {
            "mapel": mapel,
            "kelas": kelas,
            "jam": jam,
            "waktu": sekarang
        })

        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Presensi berhasil disimpan"
        }), 201

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# =========================
# 🔥 GET: AMBIL SEMUA PRESENSI (UNTUK REKAP)
# =========================
@presensi_bp.route('/', methods=['GET'])
def get_presensi():
    try:
        query = "SELECT * FROM presensi ORDER BY waktu DESC"
        result = db.session.execute(query)

        data = []
        for row in result:
            data.append({
                "id": row.id,
                "mapel": row.mapel,
                "kelas": row.kelas,
                "jam": row.jam,
                "waktu": row.waktu
            })

        return jsonify(data), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500