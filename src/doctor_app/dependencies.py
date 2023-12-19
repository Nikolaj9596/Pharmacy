from src.doctor_app.repositories import DoctorRepository
from src.doctor_app.services import DoctorService


def doctor_service() -> DoctorService:
    return DoctorService(repository=DoctorRepository())
