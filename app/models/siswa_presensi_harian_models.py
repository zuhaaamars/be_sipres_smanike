from app.app import db # Sesuaikan jika db kamu ada di app/app.py
from datetime import datetime

class PresensiHarian(db.Model):
    __tablename__ = 'presensi_harian'
    
    id = db.Column(db.Integer, primary_key=True)
    siswa_id = db.Column(db.Integer, db.ForeignKey('siswa_profile.id'), nullable=False)
    tanggal = db.Column(db.Date, default=datetime.now().date)
    jam_masuk = db.Column(db.DateTime, nullable=True)
    jam_pulang = db.Column(db.DateTime, nullable=True)
    foto_bukti = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    status = db.Column(db.String(20), default='Hadir')