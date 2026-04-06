from app import db

class Guru(db.Model):
    __tablename__ = 'guru_profile'

    id = db.Column(db.Integer, primary_key=True)
    nip = db.Column(db.String(20), unique=True, nullable=False)
    nama_lengkap = db.Column(db.String(100), nullable=False)
    gelar = db.Column(db.String(20), nullable=True)
    jenis_kelamin = db.Column(db.Enum('L', 'P'), nullable=False)
    no_hp = db.Column(db.String(15), nullable=True)
    alamat = db.Column(db.Text, nullable=True)
    
    # Relasi ke Akun Login
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    # Relasi balik: Satu guru bisa jadi wali di satu kelas
    # kelas_diampu = db.relationship('Kelas', backref='wali_kelas', lazy=True)

    def __repr__(self):
        return f'<Guru {self.nama_lengkap}>'