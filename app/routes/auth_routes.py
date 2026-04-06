from flask import Blueprint
# Pastikan nama fungsi di import sesuai dengan yang ada di controller
from app.controllers.auth_controllers import login, register_user

# Nama variabel ini HARUS 'auth_bp' agar terbaca oleh __init__.py
auth_bp = Blueprint('auth', __name__)

# Daftarkan route ke variabel auth_bp
auth_bp.route('/login', methods=['POST'])(login)
auth_bp.route('/register', methods=['POST'])(register_user)