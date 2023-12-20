

from src.client_app.repositories import ClientRepository
from src.client_app.services import ClientService


def client_service() -> ClientService:
    return ClientService(repository=ClientRepository())
