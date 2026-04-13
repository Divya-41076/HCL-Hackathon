from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import accounts

# ✅ FIRST create app
app = FastAPI(title="Banking API")

# ✅ THEN middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ THEN include routes
app.include_router(accounts.router)

# ✅ TEST ROUTE
@app.get("/")
def root():
    return {"message": "Banking API running"}