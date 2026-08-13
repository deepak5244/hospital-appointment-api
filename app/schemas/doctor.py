from pydantic import BaseModel, ConfigDict, Field


class DoctorBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    specialization: str = Field(min_length=1, max_length=100)


class DoctorCreate(DoctorBase):
    pass


class DoctorResponse(DoctorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int