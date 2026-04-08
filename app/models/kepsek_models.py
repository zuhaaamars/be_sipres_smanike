from app.app import db

class KepalaSekolah(db.Model):
    __tablename__ = 'kepsek_profile'

    id = db.Column(db.Integer, primary_key=True)
    # --- KOLOM DASAR (Sama dengan role lain) ---
    nama_lengkap = db.Column(db.String(100), nullable=False)
    jenis_kelamin = db.Column(db.Enum('L', 'P'), nullable=True)
    tempat_lahir = db.Column(db.String(50), nullable=True)
    tanggal_lahir = db.Column(db.Date, nullable=True)
    alamat = db.Column(db.Text, nullable=True)
    no_hp = db.Column(db.String(15), nullable=True)

    # --- KOLOM SPESIFIK KEPSEK ---
    nip = db.Column(db.String(30), unique=True, nullable=True) # Nullable=True agar tahap 1 aman
    gelar = db.Column(db.String(20), nullable=True)
    periode_mulai = db.Column(db.String(10), nullable=True)   # Contoh: 2024
    periode_selesai = db.Column(db.String(10), nullable=True) # Contoh: 2028

    # Relasi ke Akun Login
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f'<KepalaSekolah {self.nama_lengkap}>'