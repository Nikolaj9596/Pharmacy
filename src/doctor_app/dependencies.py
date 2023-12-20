from datetime import datetime
from typing import Optional
from src.doctor_app.repositories import DoctorRepository, DoctorAppointmentRepository
from src.doctor_app.services import AppointmentService, DoctorService


def doctor_service() -> DoctorService:
    return DoctorService(repository=DoctorRepository())

def appointment_service() -> AppointmentService:
    return AppointmentService(repository=DoctorAppointmentRepository())
