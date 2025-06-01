import uuid
from contextvars import ContextVar
from datetime import datetime

import jwt
from fastapi import Request
from loguru import logger
from starlette.types import ASGIApp, Receive, Scope, Send

from app.backend import settings

request_id_var: ContextVar[str] = ContextVar("request_id")
logger.remove()

logger.add(
    f"{datetime.now().strftime('%Y-%m-%d')}.log",
    format="Log: [{extra[log_id]} | {time:DD.MM.YYYY HH:mm:ss} | {level} | {message}]",
    level="INFO",
    enqueue=True,
    rotation="10 MB",
    retention="30 days",
    compression="zip",
)


class LoggingMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        request = Request(scope, receive)
        request_id = str(uuid.uuid4())
        request_id_var.set(request_id)

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                user_info = "anonymous"
                try:
                    auth_header = request.headers.get("Authorization")
                    if auth_header and auth_header.startswith("Bearer "):
                        token = auth_header.split(" ")[1]
                        payload = jwt.decode(
                            token,
                            settings.SECRET_KEY,
                            algorithms=[settings.ALGORITHM],
                            options={"verify_exp": False},
                        )
                        if username := payload.get("sub"):
                            user_info = f"{username}"
                            if user_id := payload.get("user_id"):
                                user_info += f" (user_id: {user_id})"
                except Exception as e:
                    logger.debug(f"Failed to parse user from token: {str(e)}")

                with logger.contextualize(log_id=request_id):
                    logger.info(
                        f"User: {user_info} | "
                        f"Path: {request.url.path} | "
                        f"Status: {message['status']}"
                    )

            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        except Exception as e:
            with logger.contextualize(log_id=request_id):
                logger.error(f"Request failed: {str(e)}")
            raise
