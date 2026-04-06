from app import db

class Admin(db.Model):
    __tablename__ = 'admin_profile'

    id = db.Column(db.Integer, primary_key=True)
    nama_lengkap = db.Column(db.String(100), nullable=False)
    nip = db.Column(db.String(20), unique=True, nullable=True) 
    email = db.Column(db.String(100), unique=True, nullable=True)
    no_hp = db.Column(db.String(15), nullable=True)
    
    # Relasi ke tabel User (One-to-One)
    # Jika User dihapus, profil admin ini juga ikut terhapus
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    def __repr__(self):
        return f'<Admin {self.nama_lengkap}>'