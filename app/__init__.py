from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

# Import Konfigurasi dari config.py
from config import Config

# 1. Inisialisasi Plugin Secara Global (Agar bisa dipakai di file lain)
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    # 2. Load Configuration
    app.config.from_object(Config)
    
    # 3. Hubungkan Plugin ke Aplikasi
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # 4. IMPORT SEMUA MODELS (WAJIB agar database & migrasi mengenali tabel)
    # --- Kelompok Data Master ---
    from app.models.master.jurusan_models import Jurusan
    from app.models.master.kelas_models import Kelas
    from app.models.master.mapel_models import Mapel
    from app.models.master.jenis_surat_models import JenisSurat

    # --- Kelompok User & Profile Lengkap ---
    from app.models.user_models import User
    from app.models.admin_models import Admin
    from app.models.siswa_models import Siswa
    from app.models.guru_models import Guru
    from app.models.staff_models import Staf
    from app.models.kepsek_models import KepalaSekolah

    # MODUL PRESENSI
    from app.routes.presensi_routes import presensi_bp

    # 5. REGISTER BLUEPRINTS (Menghubungkan Jalur API)
    # Pastikan file app/routes/auth_routes.py sudah kamu buat
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(presensi_bp, url_prefix='/api/presensi')

    # 6. ROUTE DASAR & STATIC FILES
    @app.route("/")
    def home():
        return jsonify({
            "status": "success",
            "message": "Backend SIPRES SMANIKE Aktif!",
            "version": "1.0.0",
            "author": "Zuha Mars Azahra"
        })

    # Route untuk akses foto profil yang diupload
    @app.route('/static/uploads/profile/<path:filename>')
    def serve_profile_images(filename):
        return send_from_directory('static/uploads/profile', filename)

    # 7. CUSTOM ERROR HANDLER (Biar pesan errornya rapi/JSON)
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "status": "error",
            "message": "Endpoint atau halaman tidak ditemukan"
        }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "status": "error",
            "message": "Terjadi kesalahan pada server backend"
        }), 500

    return app