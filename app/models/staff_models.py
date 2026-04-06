from app import db

class Staf(db.Model):
    __tablename__ = 'staf_profile'

    id = db.Column(db.Integer, primary_key=True)
    nip = db.Column(db.String(20), unique=True, nullable=True) # Staf bisa saja honorer (NIP kosong)
    nama_lengkap = db.Column(db.String(100), nullable=False)
    bagian = db.Column(db.String(50), nullable=True) # Contoh: Tata Usaha, Perpustakaan
    no_hp = db.Column(db.String(15), nullable=True)
    
    # Relasi ke Akun Login
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f'<Staf {self.nama_lengkap}>'