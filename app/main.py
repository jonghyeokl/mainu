from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.api import api_router
from app.exceptions.custom_exception import CustomException

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.may-mvp.com", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.response_code,
        content={
            "code": exc.code.value,
            "msg": exc.code.to_str(),
            "detail": exc.detail,
        },
    )
