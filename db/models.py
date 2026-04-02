from pydantic import BaseModel
from datetime import date
from bson import ObjectId


class RegisterUser(BaseModel):
    name: str
    mobile: str
    date_of_birth: str

class ValidateUser(BaseModel):
    mobile: str
    date_of_birth: str


class ScheduleAppointment(BaseModel):
    user_id: str
    date_of_appointment: str
    time_of_appointment: str

class RescheduleAppointment(BaseModel):
    appointment_id: str
    date_of_appointment: str
    time_of_appointment: str

class CancelAppointment(BaseModel):
    appointment_id: str

class GetAppointment(BaseModel):
    user_id: str





















#! Validations to be added in production level code.