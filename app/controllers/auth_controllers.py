from flask import jsonify, request
from flask_jwt_extended import create_access_token
from app.models.user_models import User
from app.models.admin_models import Admin
from app.models.guru_models import Guru
from app.models.siswa_models import Siswa
from app.models.staff_models import Staf
from app.models.kepsek_models import KepalaSekolah
from app import db
from datetime import datetime

# =================[ LOGIN ]=================
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"status": "error", "message": "Username dan password wajib diisi"}), 400

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            "status": "success",
            "message": "Login Berhasil",
            "access_token": access_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "role": user.role
            }
        }), 200
    
    return jsonify({"status": "error", "message": "Username atau password salah"}), 401

# =================[ REGISTER LENGKAP SEMUA ROLE ]=================
def register_user():
    data = request.get_json()
    role = data.get('role') # admin, guru, siswa, staff, kepsek
    
    username = data.get('username')
    password = data.get('password')
    
    # Validasi Input Dasar
    if not username or not password or not role:
        return jsonify({"status": "error", "message": "Username, password, dan role wajib diisi"}), 400

    # Cek apakah username sudah ada
    if User.query.filter_by(username=username).first():
        return jsonify({"status": "error", "message": "Username sudah terdaftar"}), 400

    try:
        # 1. Simpan Akun ke Tabel User
        new_user = User(username=username, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit() # Commit awal untuk mendapatkan new_user.id

        profile = None

        # 2. Kondisi pembuatan profil berdasarkan Role
        if role == 'admin':
            profile = Admin(
                nama_lengkap=data.get('nama_lengkap'),
                email=data.get('email'),
                user_id=new_user.id
            )
            
        elif role == 'guru':
            profile = Guru(
                nama_lengkap=data.get('nama_lengkap'),
                nip=data.get('nip'),
                gelar=data.get('gelar'), # Sesuai isi tabel kamu
                jenis_kelamin=data.get('jenis_kelamin'), # 'L' atau 'P'
                no_hp=data.get('no_hp'), # Sesuai isi tabel kamu
                alamat=data.get('alamat'),
                user_id=new_user.id
            )
            
        elif role == 'siswa':
            # Logika konversi tanggal lahir agar tidak error
            tgl_str = data.get('tanggal_lahir')
            tgl_obj = None
            if tgl_str:
                try:
                    tgl_obj = datetime.strptime(tgl_str, '%Y-%m-%d').date()
                except ValueError:
                    return jsonify({"status": "error", "message": "Format tanggal_lahir salah (Gunakan YYYY-MM-DD)"}), 400

            profile = Siswa(
                nisn=data.get('nisn'),
                nama_lengkap=data.get('nama_lengkap'),
                tempat_lahir=data.get('tempat_lahir'),
                tanggal_lahir=tgl_obj,
                jenis_kelamin=data.get('jenis_kelamin'), # Isi 'L' atau 'P'
                alamat=data.get('alamat'),
                nama_ortu=data.get('nama_ortu'),
                no_telp_ortu=data.get('no_telp_ortu'),
                user_id=new_user.id,
                kelas_id=data.get('kelas_id'),
                jurusan_id=data.get('jurusan_id')
            )
            
        elif role == 'staff':
            profile = Staf(
                nama_lengkap=data.get('nama_lengkap'),
                nip=data.get('nip'),
                bagian=data.get('bagian'), # Sesuai Model: Tata Usaha, Perpustakaan, dll
                no_hp=data.get('no_hp'),
                user_id=new_user.id
            )
            
        elif role == 'kepsek':
            profile = KepalaSekolah(
                nama_lengkap=data.get('nama_lengkap'),
                nip=data.get('nip'),
                periode_mulai=data.get('periode_mulai'),   # Contoh: 2024
                periode_selesai=data.get('periode_selesai'), # Contoh: 2028
                user_id=new_user.id
            )
            
        else:
            # Jika role tidak cocok, hapus user yang sempat dibuat
            db.session.delete(new_user)
            db.session.commit()
            return jsonify({"status": "error", "message": "Role tidak dikenal"}), 400

        # Simpan profil ke database
        if profile:
            db.session.add(profile)
            db.session.commit()

        return jsonify({
            "status": "success", 
            "message": f"Registrasi {role} dengan nama {data.get('nama_lengkap')} berhasil!"
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": f"Terjadi kesalahan: {str(e)}"}), 500