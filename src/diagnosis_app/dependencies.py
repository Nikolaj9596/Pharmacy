
from src.diagnosis_app.repositories import CategoryDiseaseRepository, DiagnosisRepository, DiseaseRepository
from src.diagnosis_app.services import CategoryDiseaseService, DiagnosisService, DiseaseService


def category_disease_service() -> CategoryDiseaseService:
    return CategoryDiseaseService(repository=CategoryDiseaseRepository())

def disease_service() -> DiseaseService:
    return DiseaseService(repository=DiseaseRepository())

def diagnosis_service() -> DiagnosisService:
    return DiagnosisService(repository=DiagnosisRepository())
