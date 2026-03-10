import bcrypt
from sqlalchemy.orm import Session
from database.config import engine, SessionLocal
from database.models import User, Budget, Base

def seed():
    # Create tables if not exists
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # 1. Check/Create User
    nrp_test = "12345678"
    user = db.query(User).filter(User.nrp == nrp_test).first()
    if not user:
        password = b"password123"
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt).decode('utf-8')
        
        new_user = User(
            nrp=nrp_test,
            nama_lengkap="Bripka Rohman",
            password_hash=hashed_password,
            pangkat_satker="Satreskrim / Mabes Polri",
            role="anggota"
        )
        db.add(new_user)
        print(f"User {nrp_test} created")
    
    # 2. Check/Create Budget
    budget = db.query(Budget).filter(Budget.nama_kegiatan == "Giat Satker A").first()
    if not budget:
        new_budget = Budget(
            nama_kegiatan="Giat Satker A",
            total_anggaran=10000000.0,
            sisa_anggaran=10000000.0
        )
        db.add(new_budget)
        print("Budget 'Giat Satker A' created")
    
    db.commit()
    db.close()
    print("Seeding complete!")

if __name__ == "__main__":
    seed()

if __name__ == "__main__":
    seed()
