from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.doctor import Doctor
from app.schemas.doctor import DoctorCreate


def get_doctors(db: Session):
    return list(db.scalars(select(Doctor)).all())


def get_doctor(db: Session, doctor_id: int):
    return db.get(Doctor, doctor_id)


def create_doctor(db: Session, doctor_data: DoctorCreate):
    doctor = Doctor(
        name=doctor_data.name,
        specialization=doctor_data.specialization,
    )

    db.add(doctor)
    db.commit()
    db.refresh(doctor)

    return doctor