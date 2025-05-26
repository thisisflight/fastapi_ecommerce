from fastapi import FastAPI
from starlette.responses import RedirectResponse

from app.routers import all_routers

app = FastAPI(summary="My e-commerce app")
[app.include_router(router) for router in all_routers]


@app.get("/", include_in_schema=False)
async def root() -> dict:
    return RedirectResponse(url="/docs")
