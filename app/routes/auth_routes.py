from flask import Blueprint
# Tambahkan semua fungsi update yang baru dibuat di controller
from app.controllers.auth_controllers import (
    login, 
    register_user, 
    update_siswa_profile, 
    update_guru_profile, 
    update_staf_profile, 
    update_kepsek_profile
)

auth_bp = Blueprint('auth', __name__)

# --- Tahap 1: Pendaftaran Akun & Data Umum ---
# Endpoint: /api/login & /api/register
auth_bp.route('/login', methods=['POST'])(login)
auth_bp.route('/register', methods=['POST'])(register_user)

# --- Tahap 2: Melengkapi Data Spesifik (Halaman Lanjutan di FE) ---
# Endpoint ini yang akan dipanggil di halaman Daftar-siswa.jsx, Daftar-guru.jsx, dsb.
auth_bp.route('/siswa/update', methods=['POST'])(update_siswa_profile)
auth_bp.route('/guru/update', methods=['POST'])(update_guru_profile)
auth_bp.route('/staf/update', methods=['POST'])(update_staf_profile)
auth_bp.route('/kepsek/update', methods=['POST'])(update_kepsek_profile)