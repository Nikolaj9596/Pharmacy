from fastapi import FastAPI
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

if settings.debug:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_methods=['*'],
        allow_headers=['*'],
    )

app.include_router(profession_api)
app.include_router(doctor_api)
app.include_router(appointment_api)
app.include_router(client_api)
app.include_router(category_disease_api)
app.include_router(disease_api)
app.include_router(diagnosis_api)


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
