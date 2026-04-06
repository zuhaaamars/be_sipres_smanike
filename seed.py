from app import create_app, db
# Import Model Autentikasi & Profile
from app.models.user_models import User
from app.models.admin_models import Admin
# Import Master Data
from app.models.master.jurusan_models import Jurusan
from app.models.master.kelas_models import Kelas
from app.models.master.mapel_models import Mapel
from app.models.master.jenis_surat_models import JenisSurat

app = create_app()

def seed_data():
    with app.app_context():
        print("=== Memulai Seeding Data Master SIPRES SMANIKE ===")

        # 1. SEED USER & ADMIN (Akun Login Utama)
        # Kita cek dulu apakah username sudah ada supaya tidak duplikat
        if not User.query.filter_by(username='admin_smanike').first():
            user_admin = User(username='admin_smanike', role='super_admin')
            user_admin.set_password('smanike2026')
            db.session.add(user_admin)
            db.session.commit() # Commit dulu agar user_id tersedia

            prof_admin = Admin(
                nama_lengkap="Zuha Mars Azahra",
                email="admin@smanike.sch.id",
                user_id=user_admin.id
            )
            db.session.add(prof_admin)
            print("[✓] Super Admin & Profil berhasil dibuat.")

        # 2. SEED JURUSAN
        # Jurusan adalah master data level 1
        jurusan_data = ['MIPA', 'IPS', 'Bahasa']
        for j_name in jurusan_data:
            if not Jurusan.query.filter_by(nama_jurusan=j_name).first():
                db.session.add(Jurusan(nama_jurusan=j_name))
        db.session.commit()
        print("[✓] Data Jurusan berhasil disiapkan.")

        # 3. SEED KELAS
        # Kelas butuh ID Jurusan (Relasi), pastikan mipa_id ada
        mipa = Jurusan.query.filter_by(nama_jurusan='MIPA').first()
        ips = Jurusan.query.filter_by(nama_jurusan='IPS').first()
        
        if mipa:
            list_kelas_mipa = ['X MIPA 1', 'XI MIPA 1', 'XII MIPA 1']
            for k in list_kelas_mipa:
                if not Kelas.query.filter_by(nama_kelas=k).first():
                    db.session.add(Kelas(nama_kelas=k, jurusan_id=mipa.id))
        
        if ips:
            list_kelas_ips = ['X IPS 1', 'XI IPS 1', 'XII IPS 1']
            for k in list_kelas_ips:
                if not Kelas.query.filter_by(nama_kelas=k).first():
                    db.session.add(Kelas(nama_kelas=k, jurusan_id=ips.id))
                    
        db.session.commit()
        print("[✓] Data Kelas (MIPA & IPS) berhasil disiapkan.")

        # 4. SEED MATA PELAJARAN (MAPEL)
        mapel_data = ['Matematika', 'Bahasa Indonesia', 'Bahasa Inggris', 'Fisika', 'Biologi', 'Ekonomi', 'Sosiologi']
        for m in mapel_data:
            if not Mapel.query.filter_by(nama_mapel=m).first():
                db.session.add(Mapel(nama_mapel=m))
        db.session.commit()
        print("[✓] Data Mapel berhasil disiapkan.")

        # 5. SEED JENIS SURAT
        surat_data = ['Surat Keterangan Aktif', 'Surat Izin Pindah', 'Surat Panggilan Orang Tua', 'Surat Keterangan Lulus']
        for s in surat_data:
            if not JenisSurat.query.filter_by(nama_jenis=s).first():
                db.session.add(JenisSurat(nama_jenis=s))
        db.session.commit()
        print("[✓] Data Jenis Surat berhasil disiapkan.")

        print("\n=== SEEDING SELESAI: Database SIPRES SMANIKE Siap Digunakan! ===")

if __name__ == '__main__':
    seed_data()