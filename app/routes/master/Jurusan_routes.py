from flask import Blueprint, request, jsonify
from app import db
from app.models.master.jurusan_models import Jurusan

jurusan_bp = Blueprint('jurusan_bp', __name__)

# 🔹 GET semua jurusan
@jurusan_bp.route('/', methods=['GET'])
def get_jurusan():
    data = Jurusan.query.all()
    return jsonify([
        {
            "id": j.id,
            "nama_jurusan": j.nama_jurusan
        } for j in data
    ])

# 🔹 POST tambah jurusan
@jurusan_bp.route('/', methods=['POST'])
def tambah_jurusan():
    data = request.json

    new_jurusan = Jurusan(
        nama_jurusan=data['nama_jurusan']
    )

    db.session.add(new_jurusan)
    db.session.commit()

    return jsonify({"message": "Jurusan berhasil ditambahkan"})