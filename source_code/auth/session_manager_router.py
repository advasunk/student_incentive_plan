from fastapi import APIRouter
from fastapi import Request, Response

from source_code.auth import session_manager

# api = APIRouter(tags=['course api'], prefix="/course")
session_manager_router = APIRouter(include_in_schema=False)


@session_manager_router.post("/create_session/{user_name}")
async def create_session(user_name: str, request: Request, response: Response):
    # get query params
    params = request.query_params
    user_role = ''
    if params.get("user_role") is not None:
        user_role = params.get("user_role")

    session_data = session_manager.build_session_data(user_id='1', user_name=user_name, user_role=user_role)
    session_manager.create_cookie_with_session_data(session_data, request=request,
                                                    response=response)
    return f"created session for {user_name}"


@session_manager_router.get("/whoami")
async def whoami(request: Request):
    return session_manager.get_session_data(request)


@session_manager_router.get("/cookies")
async def get_all_cookies(request: Request):
    return session_manager.get_all_cookies(request)


@session_manager_router.post("/delete_session")
async def delete_session(request: Request, response: Response):
    session_manager.delete_session(request, response)
    return "deleted session"
