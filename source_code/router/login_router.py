# from apis.version1.route_login import login_for_access_token
# from db.session import get_db
import json

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request
from starlette.responses import HTMLResponse, Response

from utils import utils
from __init__ import templates
from auth import session_manager
from auth.forms import LoginForm
from dao import user_dao

# from webapps.auth.forms import LoginForm


auth_router = APIRouter(prefix="/login", include_in_schema=False)


@auth_router.get("/")
def login_get(request: Request):
    form = LoginForm(request)
    form.username = ''
    form.password = ''

    session_data = session_manager.get_session_data(request)
    if session_data is None:
        # redirect response to /login page
        return templates.TemplateResponse("login.html", {"request": request})
    else:
        data_dict = utils.build_data_dict(None, '', '', 'home')
        return templates.TemplateResponse("home.html", {"request": request, 'data_dict': data_dict})



@auth_router.post("/")
async def login_post(request: Request):
    form = LoginForm(request)
    await form.load_data()

    data_dict = {}
    data_dict['username'] = form.username
    data_dict['password'] = form.password

    if await form.is_valid():
        try:
            user_data = user_dao.get_user_data_by_email_and_password(form.username, form.password)
            user_data = utils.convert_dataframe_to_dict(user_data)

            if user_data is not None and len(user_data) == 1:
                user_data = user_data[0]
                # remove 'password' from user_data if exists
                user_data = utils.remove_password_from_user(user_data)
                # build full name from first_name and last_name
                user_data['full_name'] = user_data['first_name'] + ' ' + user_data['last_name']

                session_data = session_manager.build_session_data(user_data['id'],
                                                                  user_data['first_name'] + ' ' + user_data['last_name'],
                                                                  user_data['email'],
                                                                  str(user_data['user_type']).title())

                # convert date type to string
                user_data['date_of_birth'] = utils.convert_date_to_string(user_data['date_of_birth'])

                # convert user_data dict to json
                user_data_json = json.dumps(user_data)
                # save user data to session
                session_manager.save_data_to_session(request, 'user_data', user_data_json)

                form.__dict__.update(session_data=session_data.json())
                response = templates.TemplateResponse("home.html", form.__dict__)
                response.headers["session_data"] = (session_data.json())
                request.headers.__dict__["_list"].append(
                    (
                        'session_data', session_data.json()
                    )
                )
                session_manager.create_cookie_with_session_data(session_data, request, response)
            else:
                raise HTTPException(status_code=401, detail="Incorrect username or password")

            # redirect the request to /h/ page
            # response = Response(status_code=200)
            return response
        except HTTPException:
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return templates.TemplateResponse("login.html", form.__dict__)

    return templates.TemplateResponse("login.html", form.__dict__)


@auth_router.get("/logout", status_code=200, response_class=HTMLResponse)
async def logout(request: Request, response: Response):
    print(request.client.host)
    # get session data from request. If session data is not available, then redirect to login page, else continue with home page
    session_data = session_manager.get_session_data(request)
    if session_data is None:
        return templates.TemplateResponse("login.html", {"request": request})
    else:
        response = templates.TemplateResponse("login.html",
                                              {"request": request, "msg": "You have been logged out successfully."})
        session_manager.delete_session(request, response)
        return response
