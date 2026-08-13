from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.models.appointment import Appointment
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.schemas.appointment import AppointmentCreate


def check_appointment_overlap(
    db: Session,
    doctor_id: int,
    appointment_start,
    appointment_end,
) -> bool:
    """
    Check if a new appointment overlaps with existing appointments for the same doctor.
    
    Overlap condition: existing_start < new_end AND existing_end > new_start
    Returns True if overlap exists, False otherwise.
    """
    existing = db.scalars(
        select(Appointment).where(
            and_(
                Appointment.doctor_id == doctor_id,
                Appointment.appointment_start < appointment_end,
                Appointment.appointment_end > appointment_start,
            )
        )
    ).all()
    
    return len(existing) > 0


def get_appointments(db: Session):
    return list(db.scalars(select(Appointment)).all())


def get_appointment(db: Session, appointment_id: int):
    return db.get(Appointment, appointment_id)


def create_appointment(db: Session, appointment_data: AppointmentCreate):
    # Verify patient exists
    patient = db.get(Patient, appointment_data.patient_id)
    if patient is None:
        raise ValueError(f"Patient with id {appointment_data.patient_id} not found")
    
    # Verify doctor exists
    doctor = db.get(Doctor, appointment_data.doctor_id)
    if doctor is None:
        raise ValueError(f"Doctor with id {appointment_data.doctor_id} not found")
    
    # Check for overlapping appointments
    if check_appointment_overlap(
        db,
        appointment_data.doctor_id,
        appointment_data.appointment_start,
        appointment_data.appointment_end,
    ):
        raise ValueError(
            f"Doctor {doctor.name} has an overlapping appointment in this time slot"
        )
    
    appointment = Appointment(
        patient_id=appointment_data.patient_id,
        doctor_id=appointment_data.doctor_id,
        appointment_start=appointment_data.appointment_start,
        appointment_end=appointment_data.appointment_end,
    )
    
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    
    return appointment
