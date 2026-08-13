from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.appointment import AppointmentCreate, AppointmentResponse
from app.services.appointment_service import (
    create_appointment,
    get_appointment,
    get_appointments,
)


router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"],
)


@router.get("", response_model=list[AppointmentResponse])
def get_all_appointments(db: Session = Depends(get_db)):
    return get_appointments(db)


@router.post(
    "",
    response_model=AppointmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_appointment(db, appointment)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment_by_id(
    appointment_id: int,
    db: Session = Depends(get_db),
):
    appointment = get_appointment(db, appointment_id)

    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found",
        )

    return appointment
