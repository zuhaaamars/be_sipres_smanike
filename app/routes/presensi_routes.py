from flask import Blueprint
from app.controllers.siswa_presensi_harian_controllers import submit_presensi_harian

harian_bp = Blueprint('harian_bp', __name__)

# Tambahkan OPTIONS di sini
@harian_bp.route('/harian', methods=['POST', 'OPTIONS'])
def harian_route():
    return submit_presensi_harian()

@harian_bp.route('/riwayat/<int:siswa_id>', methods=['GET'])
def riwayat_route(siswa_id):
    from app.controllers.siswa_presensi_harian_controllers import get_riwayat_presensi
    return get_riwayat_presensi(siswa_id)