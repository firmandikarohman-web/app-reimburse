from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.config import get_db
from database.models import Reimbursement, Budget

router = APIRouter(prefix="/api/admin", tags=["Admin Approval"])

@router.get("/pending")
def get_pending_reimbursements(db: Session = Depends(get_db)):
    pending = db.query(Reimbursement).filter(Reimbursement.status == "Pending").all()
    return pending

@router.post("/approve/{reimburse_id}")
def approve_reimbursement(reimburse_id: int, db: Session = Depends(get_db)):
    reimburse = db.query(Reimbursement).filter(Reimbursement.id == reimburse_id).first()
    if not reimburse:
        raise HTTPException(status_code=404, detail="Not found")
    
    budget = db.query(Budget).filter(Budget.id == reimburse.budget_id).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
        
    if reimburse.status != "Pending":
        raise HTTPException(status_code=400, detail="Already processed")
        
    # Deduct from budget
    if budget.sisa_anggaran < reimburse.nominal_diajukan:
        raise HTTPException(status_code=400, detail="Insufficient budget")
        
    budget.sisa_anggaran -= reimburse.nominal_diajukan
    reimburse.status = "Disetujui"
    
    db.commit()
    return {"message": "Reimbursement approved"}

@router.post("/reject/{reimburse_id}")
def reject_reimbursement(reimburse_id: int, db: Session = Depends(get_db)):
    reimburse = db.query(Reimbursement).filter(Reimbursement.id == reimburse_id).first()
    if not reimburse:
        raise HTTPException(status_code=404, detail="Not found")
    
    if reimburse.status != "Pending":
        raise HTTPException(status_code=400, detail="Already processed")
        
    reimburse.status = "Ditolak"
    db.commit()
    return {"message": "Reimbursement rejected"}

@router.patch("/budget/{budget_id}")
def update_budget(budget_id: int, nominal_total: float, db: Session = Depends(get_db)):
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    
    budget.nominal_total = nominal_total
    db.commit()
    return {"message": "Budget updated"}
