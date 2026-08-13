from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.patient import PatientCreate, PatientResponse
from app.services.patient_service import (
    create_patient,
    get_patient,
    get_patients,
)


router = APIRouter(
    prefix="/patients",
    tags=["Patients"],
)


@router.get("", response_model=list[PatientResponse])
def get_all_patients(db: Session = Depends(get_db)):
    return get_patients(db)


@router.post(
    "",
    response_model=PatientResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_patient(db, patient)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient_by_id(
    patient_id: int,
    db: Session = Depends(get_db),
):
    patient = get_patient(db, patient_id)

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found",
        )

    return patient