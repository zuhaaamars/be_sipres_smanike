from app import db

class Kelas(db.Model):
    __tablename__ = 'master_kelas'
    
    id = db.Column(db.Integer, primary_key=True)
    nama_kelas = db.Column(db.String(50), nullable=False)
    # PASTIKAN BARIS INI ADA & TIDAK DI-COMMENT:
    jurusan_id = db.Column(db.Integer, db.ForeignKey('master_jurusan.id'))