from app.app import db

class JenisSurat(db.Model):
    __tablename__ = 'master_jenis_surat'
    id = db.Column(db.Integer, primary_key=True)
    nama_jenis = db.Column(db.String(50), nullable=False) # Contoh: Surat Keterangan
    kode_surat = db.Column(db.String(10)) # Contoh: SK, SU, SP