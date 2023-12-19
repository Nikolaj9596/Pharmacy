from src.profession_app.repositories import ProfessionRepository
from src.profession_app.services import ProfessionService


def profession_service() -> ProfessionService:
    return ProfessionService(repository=ProfessionRepository())
