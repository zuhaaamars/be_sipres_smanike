from app import db
from datetime import datetime

class Presensi(db.Model):
    __tablename__ = 'presensi'

    id = db.Column(db.Integer, primary_key=True)

    mapel = db.Column(db.String(50), nullable=False)
    kelas = db.Column(db.String(50), nullable=False)
    jam = db.Column(db.String(20), nullable=False)

    waktu = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "mapel": self.mapel,
            "kelas": self.kelas,
            "jam": self.jam,
            "waktu": self.waktu.strftime("%Y-%m-%d %H:%M:%S")
        }