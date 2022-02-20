from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.db.database import init_db
from app.exceptions import BadRequestResponse, ErrorResponse
from app.routers import admin, auth, user

app = FastAPI()

app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(user.router)


@app.on_event('startup')
async def startup():
    await init_db()


@app.exception_handler(BadRequestResponse)
async def bad_request_exception_handler(request: Request,
                                        exc: BadRequestResponse):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            'code': status.HTTP_400_BAD_REQUEST,
            'message': exc.message
        }
    )


@app.exception_handler(ErrorResponse)
async def error_response_handler(request: Request, exc: ErrorResponse):
    return JSONResponse(status_code=exc.status_code, content=exc.message)
