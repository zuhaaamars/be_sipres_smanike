from app.app import db

class Mapel(db.Model):
    __tablename__ = 'master_mapel'
    id = db.Column(db.Integer, primary_key=True)
    nama_mapel = db.Column(db.String(50), unique=True, nullable=False) # Contoh: Matematika