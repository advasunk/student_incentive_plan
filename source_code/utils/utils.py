from datetime import datetime

from starlette.requests import Request

from auth import session_manager


def remove_password_from_user(user_data):
    # remove 'password' from user_data if exists
    if 'password' in user_data:
        user_data['password'] = ''

    return user_data


def get_user_role(request: Request):
    return session_manager.get_session_data_attrib(request, 'user_role')


def is_admin_user(request: Request):
    return get_user_role(request).lower() == 'Admin'.lower()


def is_teacher_user(request: Request):
    return get_user_role(request).lower() == 'Teacher'.lower()


def is_student_user(request: Request):
    return get_user_role(request).lower() == 'Student'.lower()


def is_parent_user(request: Request):
    return get_user_role(request).lower() == 'Parent'.lower()


def get_user_id(request: Request):
    return session_manager.get_session_data_attrib(request, 'user_id')


def get_request_ip(request: Request):
    return request.client.host


def get_request_url(request: Request):
    return request.url


def get_request_headers(request: Request):
    return request.headers


def get_request_attribute(request: Request, param_name, default_value=None):
    if request is not None and request.query_params is not None and param_name in request.query_params:
        return request.query_params.get(param_name, default_value)
    else:
        return default_value


def convert_dataframe_to_dict(in_dataframe):
    if in_dataframe is None or len(in_dataframe) < 1:
        return {}

    return in_dataframe.to_dict(orient='records')


def get_unique_id():
    # get unique timestamp in UTC and return
    ret_id = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    # remove last 3 digits so we can get just milli-seconds (not micro-seconds?)
    return ret_id[:-3]


def build_data_dict(data, status_message, error_message, data_set_name='data'):
    data_dict = {}
    if data is not None:
        data_dict[data_set_name] = convert_dataframe_to_dict(data)
    if status_message:
        data_dict['status_message'] = status_message
    if error_message:
        data_dict['error_message'] = error_message

    return data_dict


def get_form_attribute(form_data_list, attribute_id, default_value=None):
    for form_data in form_data_list:
        if form_data[0] == attribute_id:
            return form_data[1]
    return default_value


def convert_date_to_string(in_date_val):
    if in_date_val is None:
        return None
    else:
        return in_date_val.strftime('%Y-%m-%d')
