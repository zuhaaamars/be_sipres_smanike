from app.app import db

class Guru(db.Model):
    __tablename__ = 'guru_profile'
    id = db.Column(db.Integer, primary_key=True)
    # Kolom Dasar (Disamakan dengan Siswa)
    nama_lengkap = db.Column(db.String(100), nullable=False)
    jenis_kelamin = db.Column(db.Enum('L', 'P'), nullable=True)
    tempat_lahir = db.Column(db.String(50), nullable=True)
    tanggal_lahir = db.Column(db.Date, nullable=True)
    alamat = db.Column(db.Text, nullable=True)
    no_hp = db.Column(db.String(15), nullable=True)

    # Kolom Spesifik Guru
    nip = db.Column(db.String(30), unique=True, nullable=True)
    gelar = db.Column(db.String(20), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)