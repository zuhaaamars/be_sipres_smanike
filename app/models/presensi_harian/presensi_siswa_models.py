from app import db
from datetime import datetime

class PresensiSiswa(db.Model):
    __tablename__ = 'presensi_siswa'

    id = db.Column(db.Integer, primary_key=True)
    siswa_id = db.Column(db.Integer, db.ForeignKey('siswa_profile.id', ondelete='CASCADE'), nullable=False)
    tanggal = db.Column(db.Date, default=datetime.utcnow().date)
    jam_masuk = db.Column(db.Time, nullable=True)
    jam_pulang = db.Column(db.Time, nullable=True)
    
    # Geofencing & Selfie
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    foto_selfie = db.Column(db.String(255), nullable=True)
    
    # Status: Hadir, Terlambat, Izin, Sakit, Alpa
    status = db.Column(db.Enum('Hadir', 'Terlambat', 'Izin', 'Sakit', 'Alpa'), default='Alpa')
    keterangan = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<PresensiSiswa {self.siswa_id} - {self.tanggal}>'