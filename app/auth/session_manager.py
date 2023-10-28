import json

from fastapi import Response
from pydantic import BaseModel
from starlette.requests import Request

from utils import date_utility

fmt_ymd_hms_z = '%Y-%m-%d %H:%M:%S %Z%z'


# reference: https://en.wikiversity.org/wiki/Server-Side_Scripting/Cookies_and_Sessions/Python_(FastAPI)

class SessionData(BaseModel):
    user_id: str = None
    user_name: str
    user_email: str
    user_role: str
    created_at: str = None

    def __init__(self, user_id: str, user_name: str, user_email: str, user_role: str, created_at: str):
        super().__init__(user_id=user_id, user_name=user_name, user_email=user_email, user_role=user_role,
                         created_at=created_at)


def build_session_data(user_id: str, user_name: str, user_email: str, user_role: str):
    global fmt_ymd_hms_z
    # store current time with timezone in session data
    curr_time = date_utility.get_current_time_in_pst()
    # convert to string
    curr_time_str = date_utility.format_date_time_to_string(curr_time, fmt=fmt_ymd_hms_z)
    session_data = SessionData(user_id=user_id, user_name=user_name, user_email=user_email, user_role=user_role.title(),
                               created_at=curr_time_str)
    return session_data


def create_cookie_with_session_data(session_data: SessionData, request: Request, response: Response):
    curr_time = date_utility.get_current_time_in_pst()
    expire_time = date_utility.add_time_in_minutes(curr_time, 60)
    # covert session data to json
    session_data = session_data.json()
    # get unique id [UUID] of the session based on the client request
    uniqie_session_id = 'incenti'  # str(uuid4())
    print('create_session - expire_time=', expire_time)
    # response.set_cookie(uniqie_session_id, session_data, expires=expire_time)

    response.set_cookie(
        key=uniqie_session_id,
        value=str(session_data),
        expires=expire_time)

    return response


def update_cookie_with_session_data(request: Request, response: Response):
    global fmt_ymd_hms_z
    # get unique id [UUID] of the session
    uniqie_session_id = 'incenti'  # str(uuid4())
    print('update_session - uniqie_session_id', uniqie_session_id)
    # get session data from request. If session data is not available, then redirect to login page, else continue with home page
    session_data = request.cookies.get(uniqie_session_id)
    if session_data is None:
        return response
    else:
        # convert session data to json
        session_data = session_data.json()
        # store current time with timezone in session data
        curr_time = date_utility.get_current_time_in_pst()
        expire_time = date_utility.add_time_in_minutes(curr_time, 60)
        # convert to string
        # covert session data to json
        session_data = session_data.json()
        # get unique id [UUID] of the session based on the client request
        uniqie_session_id = 'incenti'
        print('update_session - expire_time=', expire_time)
        response.set_cookie(uniqie_session_id, session_data, expires=expire_time)
        return response


def get_session_data(request: Request):
    # get unique id [UUID] of the session
    uniqie_session_id = 'incenti'  # str(uuid4())
    return request.cookies.get(uniqie_session_id)


def get_all_cookies(request: Request):
    # get unique id [UUID] of the session
    uniqie_session_id = 'incenti'  # str(uuid4())
    return request.cookies


def delete_session(request: Request, response: Response):
    # get unique id [UUID] of the session
    uniqie_session_id = 'incenti'  # str(uuid4())
    # response.delete_cookie(uniqie_session_id)
    # request.session.clear()
    response.set_cookie(uniqie_session_id, "", expires=0)
    all_cookies = get_all_cookies(request)
    print(all_cookies)

    return response


def convert_json_to_session_data(session_data_json_str):
    if session_data_json_str is None:
        return None
    else:
        # Parse json string
        session_data_dict = json.loads(session_data_json_str)
        return session_data_dict


def get_session_data_attrib(request: Request, req_val: str):
    session_data_json_str = get_session_data(request)
    # convert session_data as str to json
    session_data_dict = convert_json_to_session_data(session_data_json_str)
    return session_data_dict[req_val] if (session_data_dict is not None and session_data_dict is not None) else None


def save_data_to_session(request: Request, var_name: str, value):
    request.session[var_name] = value


def get_data_from_http_session(request, req_val):
    return request.session.get(req_val)
