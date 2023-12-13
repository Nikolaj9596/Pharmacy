from fastapi import FastAPI
from src.config import settings

app = FastAPI(debug=settings.debug, version='1.0', title='Pharmacy App')
