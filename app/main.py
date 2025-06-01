from fastapi import FastAPI
from starlette.responses import JSONResponse, RedirectResponse

from app.log import LoggingMiddleware
from app.routers import all_routers
from app.tools import exception_handlers

app = FastAPI(summary="My e-commerce app")
[app.include_router(router) for router in all_routers]
app.add_middleware(LoggingMiddleware)


@app.get("/", include_in_schema=False)
async def root() -> dict:
    return RedirectResponse(url="/docs")


def create_exception_handler(status_code: int, detail: str):
    async def handler(request, exception):
        return JSONResponse(content={"detail": detail}, status_code=status_code)

    return handler


for exc, params in exception_handlers.items():
    app.add_exception_handler(
        exc, create_exception_handler(params["status_code"], params["detail"])
    )
