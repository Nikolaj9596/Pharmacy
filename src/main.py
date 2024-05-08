from fastapi import FastAPI
import fastapi
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.exceptions import BadRequestEx, NotFoundEx
from src.profession_app.routs import profession_api
from src.doctor_app.routs import doctor_api, appointment_api
from src.client_app.routs import client_api
from src.diagnosis_app.routs import (
    category_disease_api,
    diagnosis_api,
    disease_api,
)
from src.config import settings

app = FastAPI(debug=settings.debug, version='1.0', title='Clinic')
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api = fastapi.APIRouter(prefix='/api')
v1 = fastapi.APIRouter(prefix='/v1')

v1.include_router(profession_api)
v1.include_router(doctor_api)
v1.include_router(appointment_api)
v1.include_router(client_api)
v1.include_router(category_disease_api)
v1.include_router(disease_api)
v1.include_router(diagnosis_api)
api.include_router(v1)
app.include_router(api)


@app.exception_handler(BadRequestEx)
async def bad_request_exception_handler(request: Request, exc: BadRequestEx):
    return JSONResponse(
        status_code=400,
        content={'message': f'{exc.detail}'},
    )


@app.exception_handler(NotFoundEx)
async def not_found_exception_handler(request: Request, exc: NotFoundEx):
    return JSONResponse(
        status_code=404,
        content={'message': f'{exc.detail}'},
    )
