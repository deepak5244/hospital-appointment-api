from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.doctor import DoctorCreate, DoctorResponse
from app.services.doctor_services import (
    create_doctor,
    get_doctor,
    get_doctors,
)


router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"],
)


@router.get("", response_model=list[DoctorResponse])
def get_all_doctors(db: Session = Depends(get_db)):
    return get_doctors(db)


@router.post(
    "",
    response_model=DoctorResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(get_db),
):
    return create_doctor(db, doctor)


@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor_by_id(
    doctor_id: int,
    db: Session = Depends(get_db),
):
    doctor = get_doctor(db, doctor_id)

    if doctor is None:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found",
        )

    return doctor