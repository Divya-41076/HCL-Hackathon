from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine
from app.db.base import Base
import app.db.registry  # registers all models with Base
from app.routers import auth, accounts, transactions, service_requests, insights

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Online Banking API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(accounts.router)
app.include_router(transactions.router)
app.include_router(service_requests.router)
app.include_router(insights.router)

@app.get("/")
def root():
    return {"message": "Banking API is live"}