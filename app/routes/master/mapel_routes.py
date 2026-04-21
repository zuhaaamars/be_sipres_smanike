from flask import Blueprint, request, jsonify
from app import db
from app.models.master.mapel_models import Mapel

mapel_bp = Blueprint('mapel_bp', __name__)

@mapel_bp.route('/', methods=['GET'])
def get_mapel():
    data = Mapel.query.all()
    return jsonify([item.to_dict() for item in data])

@mapel_bp.route('/', methods=['POST'])
def tambah_mapel():
    data = request.json

    new_mapel = Mapel(
        kode_mapel=data['kode_mapel'],
        nama_mapel=data['nama_mapel'],
        kelompok=data['kelompok']
    )

    db.session.add(new_mapel)
    db.session.commit()

    return jsonify({"message": "Mapel berhasil ditambahkan"})