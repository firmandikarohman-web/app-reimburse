from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .config import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    nrp = Column(String, unique=True, index=True)
    nama_lengkap = Column(String)
    pangkat_satker = Column(String) # e.g., Bripka / Satreskrim
    role = Column(String, default="anggota") # "anggota" or "keuangan"
    password_hash = Column(String)

class Budget(Base):
    __tablename__ = "budgets"
    id = Column(Integer, primary_key=True, index=True)
    nama_kegiatan = Column(String)
    total_anggaran = Column(Float)
    sisa_anggaran = Column(Float)

class Reimbursement(Base):
    __tablename__ = "reimbursements"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    budget_id = Column(Integer, ForeignKey("budgets.id"))
    nominal_diajukan = Column(Float)
    foto_kuitansi_url = Column(String, nullable=True)  # Made nullable for optional receipt
    status = Column(String, default="Pending")
    tanggal_pengajuan = Column(DateTime, default=datetime.utcnow)
    
    # AI Results
    nominal_ai_baca = Column(Float, nullable=True)     # Made nullable
    catatan_ai = Column(String, nullable=True)

    user = relationship("User")
    budget = relationship("Budget")

class FieldExpense(Base):
    __tablename__ = "field_expenses"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    nominal = Column(Float)
    keterangan = Column(String)
    tanggal = Column(DateTime, default=datetime.utcnow)
