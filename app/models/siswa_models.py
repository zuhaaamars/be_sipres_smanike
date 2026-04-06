from app import db

class Siswa(db.Model):
    __tablename__ = 'siswa_profile'

    id = db.Column(db.Integer, primary_key=True)
    nisn = db.Column(db.String(20), unique=True, nullable=False)
    nama_lengkap = db.Column(db.String(100), nullable=False)
    tempat_lahir = db.Column(db.String(50), nullable=True)
    tanggal_lahir = db.Column(db.Date, nullable=True)
    jenis_kelamin = db.Column(db.Enum('L', 'P'), nullable=False)
    alamat = db.Column(db.Text, nullable=True)
    
    # Logika Data Orang Tua untuk Notifikasi Chat
    nama_ortu = db.Column(db.String(100), nullable=True)
    no_telp_ortu = db.Column(db.String(15), nullable=True) # Untuk WA/SMS Notifikasi

    # Relasi ke Akun Login
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    # Relasi ke Master Data
    kelas_id = db.Column(db.Integer, db.ForeignKey('master_kelas.id'), nullable=True)
    jurusan_id = db.Column(db.Integer, db.ForeignKey('master_jurusan.id'), nullable=True)

    def __repr__(self):
        return f'<Siswa {self.nama_lengkap}>'