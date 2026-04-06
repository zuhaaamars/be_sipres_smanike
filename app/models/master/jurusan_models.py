from app import db

class Jurusan(db.Model):
    __tablename__ = 'master_jurusan'

    id = db.Column(db.Integer, primary_key=True)
    nama_jurusan = db.Column(db.String(50), unique=True, nullable=False) # Contoh: MIPA, IPS, Bahasa

    # Relasi: Satu jurusan bisa memiliki banyak siswa
    siswa = db.relationship('Siswa', backref='data_jurusan', lazy=True)

    def __repr__(self):
        return f'<Jurusan {self.nama_jurusan}>'