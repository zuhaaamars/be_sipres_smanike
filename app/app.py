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
    
    # 3. Konfigurasi CORS
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
    from app.models.master.jurusan_models import Jurusan
    from app.models.master.kelas_models import Kelas
    from app.models.master.mapel_models import Mapel
    from app.models.master.jenis_surat_models import JenisSurat
    from app.models.siswa.presensiQR_models import Presensi

    from app.models.user_models import User
    from app.models.admin_models import Admin
    from app.models.siswa_models import Siswa
    from app.models.guru_models import Guru
    from app.models.staff_models import Staf
    from app.models.kepsek_models import KepalaSekolah
    from app.models.siswa_presensi_harian_models import PresensiHarian

    # 6. REGISTER BLUEPRINTS (Menghubungkan Jalur API)
    from app.routes.auth_routes import auth_bp
    from app.routes.presensi_routes import harian_bp, presensi_bp
    from app.routes.master.mapel_routes import mapel_bp
    from app.routes.master.Jurusan_routes import jurusan_bp
    from app.routes.master.kelas_routes import kelas_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(harian_bp, url_prefix='/api/presensi/harian')
    app.register_blueprint(presensi_bp, url_prefix='/api/presensi')
    app.register_blueprint(mapel_bp, url_prefix='/api/mapel')
    app.register_blueprint(jurusan_bp, url_prefix='/api/jurusan')
    app.register_blueprint(kelas_bp, url_prefix='/api/kelas')

    # 7. ROUTE DASAR
    @app.route("/")
    def home():
        return jsonify({
            "status": "success",
            "message": "Backend SIPRES SMANIKE Aktif!",
            "version": "1.0.0",
            "author": "Zuha Mars Azahra"
        })

    # STATIC FILES (Foto Profil & Presensi)
    @app.route('/static/uploads/profile/<path:filename>')
    def serve_profile_images(filename):
        return send_from_directory(os.path.join(app.root_path, 'static', 'uploads', 'profile'), filename)

    @app.route('/static/uploads/presensi/<path:folder>/<path:filename>')
    def serve_presensi_images(folder, filename):
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
        return jsonify({
            "status": "error",
            "message": "Terjadi kesalahan pada server backend."
        }), 500

    return app