from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.presensi_harian_controllers import absen_masuk_siswa

presensi_bp = Blueprint('presensi', __name__)

@presensi_bp.route('/masuk', methods=['POST'])
@jwt_required()
def route_absen_masuk():
    current_user = get_jwt_identity()
    # current_user['id'] diasumsikan menyimpan ID profil siswa
    return absen_masuk_siswa(current_user['id'])