from app import db

class KepalaSekolah(db.Model):
    __tablename__ = 'kepsek_profile'

    id = db.Column(db.Integer, primary_key=True)
    nip = db.Column(db.String(20), unique=True, nullable=False)
    nama_lengkap = db.Column(db.String(100), nullable=False)
    periode_mulai = db.Column(db.Date, nullable=True)
    periode_selesai = db.Column(db.Date, nullable=True)
    
    # Relasi ke Akun Login
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f'<Kepsek {self.nama_lengkap}>'