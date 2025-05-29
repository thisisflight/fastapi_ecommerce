from fastapi import FastAPI
from starlette.responses import JSONResponse, RedirectResponse

from app import exceptions
from app.routers import all_routers

app = FastAPI(summary="My e-commerce app")
[app.include_router(router) for router in all_routers]


@app.get("/", include_in_schema=False)
async def root() -> dict:
    return RedirectResponse(url="/docs")


@app.exception_handler(exceptions.UserAlreadyExists)
async def user_already_exists_handler(request, exception):
    return JSONResponse(content={"detail": "User already exists"}, status_code=409)


@app.exception_handler(exceptions.UserNotFoundError)
async def user_not_found_handler(request, exception):
    return JSONResponse(content={"detail": "User not found"}, status_code=404)


@app.exception_handler(exceptions.InvalidCredentialsError)
async def invalid_credentials_handler(request, exception):
    return JSONResponse(content={"detail": "Invalid credentials"}, status_code=401)
