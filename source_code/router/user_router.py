from http import HTTPStatus

from fastapi import APIRouter, Response, Request, Form
from starlette.responses import HTMLResponse

from __init__ import templates
from common import platform_data_definitions
from dao import user_dao
from utils import utils

api = APIRouter(tags=['user api'], prefix="/user")


@api.get("", status_code=200, response_class=HTMLResponse)
# @api.get("", status_code=200, response_model=CourseFindManyItemListResponseModel)
async def get_all_users(request: Request):
    # print(request.client.host)
    # get all users from database
    user_type = utils.get_request_attribute(request, 'user_type', '')
    search = utils.get_request_attribute(request, 'search', '')

    if user_type.lower() == 'all':
        user_type = ''

    if filter or user_type:
        data = user_dao.get_user_by_filter(user_type.lower(), search.lower())
    else:
        data = user_dao.get_all_users()

    # convert dataframe to list of dict
    data_dict = utils.build_data_dict(data, '', '', 'users')
    data_dict['user_type'] = user_type
    data_dict['search'] = search
    data_dict['user_type_list'] = platform_data_definitions.USER_ROLE_LIST

    return templates.TemplateResponse("user_list.html", {"request": request, "data_dict": data_dict})


@api.get("/add", status_code=200, response_class=HTMLResponse)
async def show_add_user_page(request: Request):
    first_name = utils.get_request_attribute(request, 'first_name', '')
    last_name = utils.get_request_attribute(request, 'last_name', '')
    email = utils.get_request_attribute(request, 'email', '')
    password = utils.get_request_attribute(request, 'password', '')
    user_type = utils.get_request_attribute(request, 'user_type', '')
    dob = utils.get_request_attribute(request, 'dob', '')
    user_group = utils.get_request_attribute(request, 'user_group', '')
    status_message = ''
    error_message = ''
    return templates.TemplateResponse("user_add.html",
                                      {"request": request,
                                       "first_name": first_name,
                                       "last_name": last_name,
                                       "email": email,
                                       "password": password,
                                       "user_type": user_type,
                                       "dob": dob,
                                       "user_group": user_group,
                                       "status_message": status_message,
                                       "error_message": error_message})


@api.post("/", status_code=200, response_class=HTMLResponse)
async def save_user_data(request: Request, first_name: str = Form(...),
                         last_name: str = Form(...),
                         email: str = Form(...),
                         password: str = Form(...),
                         user_type: str = Form(...),
                         dob: str = Form(...),
                         user_group: str = Form(...)):
    ret_sts = user_dao.insert_user(first_name, last_name, email, password, user_type, dob, user_group)

    status_message = ''
    error_message = ''
    if ret_sts:
        status_message = 'User ' + first_name + ' ' + last_name + ' has been added successfully'
    else:
        error_message = 'User ' + first_name + ' ' + last_name + ' has not been added successfully'

    return templates.TemplateResponse("user_add.html",
                                      {"request": request,
                                       "first_name": first_name,
                                       "last_name": last_name,
                                       "email": email,
                                       "password": password,
                                       "user_type": user_type,
                                       "dob": dob,
                                       "user_group": user_group,
                                       "status_message": status_message,
                                       "error_message": error_message
                                       })


@api.get("/email", status_code=200)
def get_one_by_email(
        request: Request,
        response: Response):
    if 'email' not in request.query_params:
        return Response('input param email not provided', status_code=HTTPStatus.NOT_FOUND,
                        headers={"x-total-count": str(0)})

    email = request.query_params['email']

    data_df = user_dao.get_user_by_email(email)
    if data_df is None or len(data_df) < 1:
        return Response('specific data not found', status_code=HTTPStatus.NOT_FOUND, headers={"x-total-count": str(0)})

    response.headers["x-total-count"] = str(1)
    # encode the dataframe to json
    return data_df.to_json()
