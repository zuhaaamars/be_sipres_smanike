from flask import jsonify, request
from flask_jwt_extended import create_access_token
from app.models.user_models import User
from app.models.admin_models import Admin
from app.models.guru_models import Guru
from app.models.siswa_models import Siswa
from app.models.staff_models import Staf 
from app.models.kepsek_models import KepalaSekolah
from app.app import db
from datetime import datetime

def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"status": "error", "message": "Username dan password wajib diisi"}), 400

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=str(user.id))
        
        # --- MENCARI ID PROFIL SECARA DINAMIS ---
        profile_id = None
        if user.role == 'siswa':
            profil = Siswa.query.filter_by(user_id=user.id).first()
            profile_id = profil.id if profil else None
        elif user.role == 'guru':
            profil = Guru.query.filter_by(user_id=user.id).first()
            profile_id = profil.id if profil else None
        elif user.role in ['staf', 'staff']:
            profil = Staf.query.filter_by(user_id=user.id).first()
            profile_id = profil.id if profil else None
        elif user.role == 'kepsek':
            profil = KepalaSekolah.query.filter_by(user_id=user.id).first()
            profile_id = profil.id if profil else None
        elif user.role == 'admin':
            profil = Admin.query.filter_by(user_id=user.id).first()
            profile_id = profil.id if profil else None

        return jsonify({
            "status": "success",
            "message": f"Login Berhasil sebagai {user.role.capitalize()}",
            "access_token": access_token,
            "user": {
                "id": user.id,
                "profile_id": profile_id, # Mengirim angka 16 ke React
                "username": user.username,
                "role": user.role
            }
        }), 200
    
    return jsonify({"status": "error", "message": "Username atau password salah"}), 401

# ... (fungsi register_user dan update tetap sama seperti kodemu sebelumnya)

# =================[ 2. REGISTER (TAHAP 1: UMUM) ]=================
def register_user():
    data = request.get_json()
    role = data.get('role') 
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password or not role:
        return jsonify({"status": "error", "message": "Data wajib diisi (Username, Password, Role)"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"status": "error", "message": "Username/Nama sudah terdaftar"}), 400

    try:
        # Simpan Akun Utama
        new_user = User(username=username, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit() 

        # Konversi Tanggal Lahir agar tidak error di database
        tgl_str = data.get('tanggal_lahir')
        tgl_obj = datetime.strptime(tgl_str, '%Y-%m-%d').date() if tgl_str else None

        # Data Kolektif (Sesuai model yang sudah diseragamkan kolom dasarnya)
        # Di dalam fungsi register_user, bagian common_fields
        common_fields = {
            "user_id": new_user.id,
            "nama_lengkap": data.get('nama_lengkap'),
            "tempat_lahir": data.get('tempat_lahir'),
            "tanggal_lahir": tgl_obj,
            "jenis_kelamin": data.get('jenis_kelamin'),
            "alamat": data.get('alamat'),
            # UBAH BARIS DI BAWAH INI:
            "no_telp_ortu": data.get('no_hp')  # Ambil 'no_hp' dari React, simpan ke 'no_telp_ortu' di DB
        }

        profile = None

        # Routing pembuatan profil kosong berdasarkan Role
        if role == 'siswa':
            profile = Siswa(**common_fields, nisn=None, kelas_id=None, jurusan_id=None)
        elif role == 'guru':
            profile = Guru(**common_fields, nip=None, gelar=data.get('gelar'))
        elif role in ['staf', 'staff']:
            profile = Staf(**common_fields, nip=None, bagian=None)
        elif role == 'kepsek':
            profile = KepalaSekolah(**common_fields, nip=None, periode_mulai=None, periode_selesai=None)
        elif role == 'admin':
            profile = Admin(user_id=new_user.id, nama_lengkap=data.get('nama_lengkap'), email=data.get('email'))

        if profile:
            db.session.add(profile)
            db.session.commit()
            return jsonify({
                "status": "success", 
                "message": "Akun berhasil dibuat, silakan lengkapi profil", 
                "userId": new_user.id 
            }), 201
        
        # Jika role tidak terdaftar, batalkan pembuatan user
        db.session.delete(new_user)
        db.session.commit()
        return jsonify({"status": "error", "message": "Role tidak valid"}), 400

    except Exception as e:
        db.session.rollback()
        print(f"Error Register: {str(e)}")
        return jsonify({"status": "error", "message": f"Gagal Daftar: {str(e)}"}), 500

# =================[ 3. UPDATE PROFIL (TAHAP 2: SPESIFIK) ]=================

# --- Update Lanjutan Siswa ---
def update_siswa_profile():
    data = request.get_json()
    user_id = data.get('userId')
    try:
        siswa = Siswa.query.filter_by(user_id=user_id).first()
        if not siswa: return jsonify({"status": "error", "message": "Data siswa tidak ditemukan"}), 404
        
        siswa.nisn = data.get('nisn')
        siswa.nama_ortu = data.get('nama_ortu')
        siswa.no_telp_ortu = data.get('no_telp_ortu')
        siswa.kelas_id = data.get('kelas_id')
        siswa.jurusan_id = data.get('jurusan_id')
        
        db.session.commit()
        return jsonify({"status": "success", "message": "Profil Siswa Berhasil Dilengkapi!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# --- Update Lanjutan Guru ---
def update_guru_profile():
    data = request.get_json()
    user_id = data.get('userId')
    try:
        guru = Guru.query.filter_by(user_id=user_id).first()
        if not guru: return jsonify({"status": "error", "message": "Data guru tidak ditemukan"}), 404
        
        guru.nip = data.get('nip')
        guru.gelar = data.get('gelar')
        db.session.commit()
        return jsonify({"status": "success", "message": "Profil Guru Berhasil Dilengkapi!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# --- Update Lanjutan Staf ---
def update_staf_profile():
    data = request.get_json()
    user_id = data.get('userId')
    try:
        staf = Staf.query.filter_by(user_id=user_id).first()
        if not staf: return jsonify({"status": "error", "message": "Data staf tidak ditemukan"}), 404
        
        staf.nip = data.get('nip')
        staf.bagian = data.get('bagian')
        db.session.commit()
        return jsonify({"status": "success", "message": "Profil Staf Berhasil Dilengkapi!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# --- Update Lanjutan Kepala Sekolah ---
def update_kepsek_profile():
    data = request.get_json()
    user_id = data.get('userId')
    try:
        kepsek = KepalaSekolah.query.filter_by(user_id=user_id).first()
        if not kepsek: return jsonify({"status": "error", "message": "Data Kepala Sekolah tidak ditemukan"}), 404
        
        kepsek.nip = data.get('nip')
        kepsek.gelar = data.get('gelar')
        kepsek.periode_mulai = data.get('periode_mulai')
        kepsek.periode_selesai = data.get('periode_selesai')
        
        db.session.commit()
        return jsonify({"status": "success", "message": "Profil Kepala Sekolah Berhasil Dilengkapi!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500