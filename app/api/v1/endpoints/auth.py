import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.security import create_access_token, hash_password, verify_password
from app.models import Doctor, Patient
from app.schemas import RegisterRequest, SignInRequest, TokenResponse

logger = logging.getLogger("red_heart.auth")

router = APIRouter(tags=["auth"])
doctor_router = APIRouter(prefix="/doctor", tags=["doctor"])


# ----- Patient: /signin, /register -----


@router.post("/signin", response_model=TokenResponse)
def patient_signin(data: SignInRequest, db: Session = Depends(get_db)):
    logger.info("Patient sign-in attempt: %s", data.email)
    user = db.query(Patient).filter(Patient.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        logger.warning("Patient sign-in failed (bad credentials): %s", data.email)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    token = create_access_token(email=user.email, role="patient")
    logger.info("Patient signed in successfully: %s", data.email)
    return TokenResponse(access_token=token)


@router.post("/register", response_model=TokenResponse)
def patient_register(data: RegisterRequest, db: Session = Depends(get_db)):
    logger.info("Patient register attempt: %s", data.email)
    if db.query(Patient).filter(Patient.email == data.email).first():
        logger.warning("Patient register failed (email exists): %s", data.email)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = Patient(email=data.email, password_hash=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token(email=user.email, role="patient")
    logger.info("Patient registered successfully: %s", data.email)
    return TokenResponse(access_token=token)


# ----- Doctor: /doctor/signin, /doctor/register -----


@doctor_router.post("/signin", response_model=TokenResponse)
def doctor_signin(data: SignInRequest, db: Session = Depends(get_db)):
    logger.info("Doctor sign-in attempt: %s", data.email)
    user = db.query(Doctor).filter(Doctor.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        logger.warning("Doctor sign-in failed (bad credentials): %s", data.email)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    token = create_access_token(email=user.email, role="doctor")
    logger.info("Doctor signed in successfully: %s", data.email)
    return TokenResponse(access_token=token)


@doctor_router.post("/register", response_model=TokenResponse)
def doctor_register(data: RegisterRequest, db: Session = Depends(get_db)):
    logger.info("Doctor register attempt: %s", data.email)
    if db.query(Doctor).filter(Doctor.email == data.email).first():
        logger.warning("Doctor register failed (email exists): %s", data.email)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = Doctor(email=data.email, password_hash=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token(email=user.email, role="doctor")
    logger.info("Doctor registered successfully: %s", data.email)
    return TokenResponse(access_token=token)
