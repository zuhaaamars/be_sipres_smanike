from app.app import db

class Mapel(db.Model):
    __tablename__ = 'master_mapel'

    id = db.Column(db.Integer, primary_key=True)
    kode_mapel = db.Column(db.String(20), unique=True, nullable=False)
    nama_mapel = db.Column(db.String(50), nullable=False)
    kelompok = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "kode_mapel": self.kode_mapel,
            "nama_mapel": self.nama_mapel,
            "kelompok": self.kelompok,
        }