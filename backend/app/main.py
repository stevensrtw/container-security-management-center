from fastapi import FastAPI
from app.routes import sbom, scan, approval, emass
from app.auth import router as auth_router
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(sbom.router, prefix="/sbom")
app.include_router(scan.router, prefix="/scan")
app.include_router(approval.router, prefix="/approval")
app.include_router(emass.router, prefix="/emass")
# All routes under /scan require auth
app.include_router(scan.router, prefix="/scan", dependencies=[Depends(get_current_user)])

# SBOM routes require auth too
app.include_router(sbom.router, prefix="/sboms", dependencies=[Depends(get_current_user)])
# backend/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@db:5432/devsecops"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()