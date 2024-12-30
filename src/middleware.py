from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import json

class CustomSessionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, secret_key: str):
        super().__init__(app)
        self.secret_key = secret_key

    async def dispatch(self, request: Request, call_next):
        if "session" not in request.scope:
            request.scope["session"] = {}

        session_cookie = request.cookies.get("session")
        if session_cookie:
            try:
                request.scope["session"] = json.loads(session_cookie)
            except json.JSONDecodeError:
                pass

        response = await call_next(request)

        session_data = json.dumps(request.scope.get("session", {}))
        response.set_cookie(
            key="session", value=session_data, httponly=True, secure=False
        )

        return response