from flask import Blueprint, request, jsonify
from app import db
from app.models.master.kelas_models import Kelas

kelas_bp = Blueprint('kelas_bp', __name__)

# 🔹 GET semua kelas
@kelas_bp.route('/', methods=['GET'])
def get_kelas():
    data = Kelas.query.all()
    
    return jsonify([
        {
            "id": k.id,
            "kelas": k.kelas,
            "jurusan_id": k.jurusan_id,
            "nama_jurusan": k.jurusan.nama_jurusan if k.jurusan else None,
            "wali_kelas": k.wali_kelas
        } for k in data
    ])


# 🔹 POST tambah kelas
@kelas_bp.route('/', methods=['POST'])
def tambah_kelas():
    data = request.json

    try:
        new_kelas = Kelas(
            kelas=data['kelas'],
            jurusan_id=data['jurusan_id'],
            wali_kelas=data['wali_kelas']
        )

        db.session.add(new_kelas)
        db.session.commit()

        return jsonify({
            "message": "Kelas berhasil ditambahkan"
        }), 201

    except Exception as e:
        return jsonify({
            "message": str(e)
        }), 500