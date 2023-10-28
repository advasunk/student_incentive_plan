from starlette.requests import Request
from starlette.templating import Jinja2Templates

from auth import session_manager
from common import platform_data_definitions

templates = Jinja2Templates(directory="templates")


def clever_function_1():
    return u'HELLO'


def clever_function_2(a, b):
    return a + b


def get_session_data_attrib(request: Request, req_val: str = 'user_name'):
    session_data_json = session_manager.get_session_data(request)
    # convert session_data as str to json
    session_data_dict = session_manager.convert_json_to_session_data(session_data_json)
    return session_data_dict[req_val] if session_data_dict is not None else None


def get_session_data_attrib_from_json(session_data_json: str, req_val: str = 'user_name'):
    # convert session_data as str to json
    session_data_dict = session_manager.convert_json_to_session_data(session_data_json)
    return session_data_dict[req_val] if session_data_dict is not None else None


def get_academic_year_list():
    academic_year_sorted = sorted(platform_data_definitions.academic_year_list, key=lambda k: k['academic_year'])
    return academic_year_sorted


def get_data_from_http_session(request: Request, req_val: str = 'user_name'):
    return session_manager.get_data_from_http_session(request, req_val)


templates.env.globals.update(clever_function_1=clever_function_1,
                             clever_function_2=clever_function_2,
                             get_session_data_attrib=get_session_data_attrib,
                             get_session_data_attrib_from_json=get_session_data_attrib_from_json,
                             get_academic_year_list=get_academic_year_list,
                             get_data_from_http_session=get_data_from_http_session
                             )
