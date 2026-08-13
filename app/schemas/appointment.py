from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AppointmentBase(BaseModel):
    patient_id: int = Field(gt=0)
    doctor_id: int = Field(gt=0)
    appointment_start: datetime
    appointment_end: datetime


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentResponse(AppointmentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
