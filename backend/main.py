from fastapi import FastAPI
from database.config import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, reimburse, admin

# Auto-create tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistem Reimbursement Pintar (AI) Polri API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(reimburse.router)
app.include_router(admin.router)

@app.get("/")
def read_root():
    return {"message": "Sistem Reimbursement Pintar (AI) Polri API up and running!"}
