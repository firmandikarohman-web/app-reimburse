from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from database.config import get_db
from database.models import Reimbursement, FieldExpense
from typing import Optional
from ai_engine.ocr_processor import process_receipt
import os

router = APIRouter(prefix="/api/reimburse", tags=["Reimbursement"])

@router.post("/upload")
async def upload_reimbursement(
    user_id: int = Form(...),
    budget_id: int = Form(...),
    nominal_diajukan: float = Form(...),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    file_path = None
    nominal_ai = None
    catatan = "Input Manual (Tanpa Struk)"
    
    if file:
        os.makedirs("uploads", exist_ok=True)
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # Ocr Process
        nominal_ai = process_receipt(file_path)
        catatan = "Terdeteksi AI"

    new_reimburse = Reimbursement(
        user_id=user_id,
        budget_id=budget_id,
        nominal_diajukan=nominal_diajukan,
        foto_kuitansi_url=file_path,
        nominal_ai_baca=nominal_ai,
        catatan_ai=catatan,
        status="Pending"
    )
    db.add(new_reimburse)
    db.commit()
    db.refresh(new_reimburse)
    return {"message": "Upload success", "id": new_reimburse.id}

@router.post("/field-expense")
def add_field_expense(user_id: int = Form(...), nominal: float = Form(...), keterangan: str = Form(...), db: Session = Depends(get_db)):
    expense = FieldExpense(user_id=user_id, nominal=nominal, keterangan=keterangan)
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return {"message": "Pengeluaran dicatat", "data": expense}

@router.get("/field-expenses/{user_id}")
def get_field_expenses(user_id: int, db: Session = Depends(get_db)):
    return db.query(FieldExpense).filter(FieldExpense.user_id == user_id).all()

@router.get("/history/{user_id}")
def get_history(user_id: int, db: Session = Depends(get_db)):
    return db.query(Reimbursement).filter(Reimbursement.user_id == user_id).all()
