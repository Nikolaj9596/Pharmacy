from fastapi import FastAPI
from src.profession_app.routs import profession_api
from src.config import settings

app = FastAPI(debug=settings.debug, version='1.0', title='Clinic')

app.include_router(profession_api)
