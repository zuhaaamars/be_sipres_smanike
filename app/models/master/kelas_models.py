<<<<<<< HEAD
from app.app import db
=======
from app import db  
>>>>>>> 2e1146c (21-04-26)

class Kelas(db.Model):
    __tablename__ = 'master_kelas'
    
    id = db.Column(db.Integer, primary_key=True)
    kelas = db.Column(db.String(50), nullable=False)
    jurusan_id = db.Column(db.Integer, db.ForeignKey('master_jurusan.id'), nullable=False)
    wali_kelas = db.Column(db.String(100), nullable=False)

    # 🔥 RELASI KE JURUSAN
    jurusan = db.relationship('Jurusan', backref='kelas', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "kelas": self.kelas,
            "jurusan_id": self.jurusan_id,

            # 🔥 INI KUNCI UTAMA
            "nama_jurusan": self.jurusan.nama_jurusan if self.jurusan else None,

            "wali_kelas": self.wali_kelas
        }