# app/main.py
from fastapi import FastAPI

from app.database.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

from app.routers.auth import router as  auth_router 
from app.routers.grades import router as grades_router
# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = [
    "http://localhost:3000",  # Frontend URL 
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins ,  # Allow all or specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)
# Include routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(grades_router, prefix="/grades", tags=["Grades"])

# Root path for health check
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Application!"}