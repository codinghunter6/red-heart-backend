from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.security import create_access_token, hash_password, verify_password
from app.models import Doctor, Patient
from app.schemas import RegisterRequest, SignInRequest, TokenResponse

router = APIRouter(tags=["auth"])
doctor_router = APIRouter(prefix="/doctor", tags=["doctor"])


# ----- Patient: /signin, /register -----


@router.post("/signin", response_model=TokenResponse)
def patient_signin(data: SignInRequest, db: Session = Depends(get_db)):
    user = db.query(Patient).filter(Patient.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    token = create_access_token(email=user.email, role="patient")
    return TokenResponse(access_token=token)


@router.post("/register", response_model=TokenResponse)
def patient_register(data: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(Patient).filter(Patient.email == data.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = Patient(email=data.email, password_hash=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token(email=user.email, role="patient")
    return TokenResponse(access_token=token)


# ----- Doctor: /doctor/signin, /doctor/register -----


@doctor_router.post("/signin", response_model=TokenResponse)
def doctor_signin(data: SignInRequest, db: Session = Depends(get_db)):
    user = db.query(Doctor).filter(Doctor.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    token = create_access_token(email=user.email, role="doctor")
    return TokenResponse(access_token=token)


@doctor_router.post("/register", response_model=TokenResponse)
def doctor_register(data: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(Doctor).filter(Doctor.email == data.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = Doctor(email=data.email, password_hash=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token(email=user.email, role="doctor")
    return TokenResponse(access_token=token)
