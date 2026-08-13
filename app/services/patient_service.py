from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.patient import Patient
from app.schemas.patient import PatientCreate


def get_patients(db: Session):
    return list(db.scalars(select(Patient)).all())


def get_patient(db: Session, patient_id: int):
    return db.get(Patient, patient_id)


def create_patient(db: Session, patient_data: PatientCreate):
    patient = Patient(
        name=patient_data.name,
        email=patient_data.email,
        phone=patient_data.phone,
    )

    try:
        db.add(patient)
        db.commit()
        db.refresh(patient)
        return patient
    except IntegrityError as e:
        db.rollback()
        if "email" in str(e).lower():
            raise ValueError(f"Patient with email '{patient_data.email}' already exists")
        raise ValueError("Unable to create patient: duplicate or invalid data")
