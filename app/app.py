import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

# Import Konfigurasi dari config.py
from config import Config

# 1. Inisialisasi Plugin Secara Global
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    # 2. Load Configuration
    app.config.from_object(Config)
    
    # 3. Konfigurasi CORS (PENTING untuk komunikasi React <-> Flask)
    # Ini akan membuka akses khusus untuk port 3000 agar tidak kena blokir browser
    CORS(app, resources={r"/api/*": {
    "origins": "http://localhost:3000",
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"]
    }})
    
    # 4. Hubungkan Plugin ke Aplikasi
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # 5. IMPORT SEMUA MODELS (Wajib agar database & migrasi mengenali tabel)
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

    # --- MODUL PRESENSI ---
    from app.models.siswa_presensi_harian_models import PresensiHarian

    # 6. REGISTER BLUEPRINTS (Menghubungkan Jalur API)
    from app.routes.auth_routes import auth_bp
    from app.routes.presensi_routes import harian_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(harian_bp, url_prefix='/api/presensi')

    # 7. ROUTE DASAR & STATIC FILES
    @app.route("/")
    def home():
        return jsonify({
            "status": "success",
            "message": "Backend SIPRES SMANIKE Aktif!",
            "version": "1.0.0",
            "author": "Zuha Mars Azahra"
        })

    # Route untuk akses foto profil
    @app.route('/static/uploads/profile/<path:filename>')
    def serve_profile_images(filename):
        return send_from_directory(os.path.join(app.root_path, 'static/uploads/profile'), filename)

    # Route untuk akses foto bukti presensi (Harian & Mapel)
    @app.route('/static/uploads/presensi/<path:folder>/<path:filename>')
    def serve_presensi_images(folder, filename):
        # folder: 'harian' atau 'mapel'
        target_path = os.path.join(app.root_path, 'static', 'uploads', 'presensi', folder)
        return send_from_directory(target_path, filename)

    # 8. CUSTOM ERROR HANDLER
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "status": "error",
            "message": "Endpoint atau halaman tidak ditemukan"
        }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        # Tips: Jika error ini muncul, cek log di terminal VS Code untuk detailnya
        return jsonify({
            "status": "error",
            "message": "Terjadi kesalahan pada server backend. Cek terminal VS Code untuk melihat error aslinya."
        }), 500

    return app