from http import HTTPStatus

from fastapi import APIRouter, Response, Request
from fastapi.params import Form

from __init__ import templates
from auth import session_manager
from common import platform_data_definitions
from dao import user_dao, user_reln_dao
from utils import utils

api = APIRouter(tags=['user api'], prefix="/user_reln")


@api.get("/", status_code=200)
def open_user_reln_add_by_email(
        request: Request,
        response: Response):
    data_dict = {}
    data_dict['reln_email'] = ''
    data_dict['status_message'] = ''
    data_dict['error_message'] = ''

    curr_user_reln_df = user_reln_dao.get_all_related_users(session_manager.get_session_data_attrib(request, 'user_id'))
    data_dict['user_reln_list'] = utils.convert_dataframe_to_dict(curr_user_reln_df)

    return templates.TemplateResponse("user_reln_list.html",
                                      {"request": request,
                                       "data_dict": data_dict
                                       })


@api.post("/search", status_code=200)
def get_one_by_email(
        request: Request,
        response: Response,
        reln_email: str = Form(...)):
    curr_user_id = session_manager.get_session_data_attrib(request, 'user_id')
    data_df = user_dao.get_user_by_email_but_not_linked(reln_email, curr_user_id)

    status_message = ''
    error_message = ''
    data_json = ''

    if data_df is None or len(data_df) < 1:
        error_message = 'User is either not found or already linked with the email ' + reln_email
    else:
        data_json = utils.convert_dataframe_to_dict(data_df)
        status_message = 'User has been found with the email ' + reln_email

    data_dict = {}
    data_dict['reln_email'] = reln_email
    data_dict['user_list'] = data_json
    data_dict['status_message'] = status_message
    data_dict['error_message'] = error_message
    data_dict['user_reln_list'] = platform_data_definitions.USER_RELN_LIST

    return templates.TemplateResponse("user_reln_add.html",
                                      {"request": request,
                                       "data_dict": data_dict})


@api.get("/add", status_code=200)
def get_one_by_email(
        request: Request,
        response: Response):
    data_dict = {}
    data_dict['reln_email'] = ''
    data_dict['status_message'] = ''
    data_dict['error_message'] = ''

    return templates.TemplateResponse("user_reln_add.html",
                                      {"request": request,
                                       "data_dict": data_dict})


@api.get("/delete", status_code=200)
def get_one_by_email(
        request: Request,
        response: Response,
        user_reln_id: str):
    # delete reln_user_id from user_reln table
    curr_user_id = session_manager.get_session_data_attrib(request, 'user_id')
    ret_sts = user_reln_dao.delete_user_reln(curr_user_id, user_reln_id)

    status_message = ''
    error_message = ''
    if ret_sts:
        status_message = 'User has been deleted successfully'
    else:
        error_message = 'User has not been deleted successfully'

    data_dict = {}
    data_dict['reln_email'] = ''
    data_dict['status_message'] = status_message
    data_dict['error_message'] = error_message

    curr_user_reln_df = user_reln_dao.get_all_related_users(session_manager.get_session_data_attrib(request, 'user_id'))
    data_dict['user_reln_list'] = utils.convert_dataframe_to_dict(curr_user_reln_df)

    return templates.TemplateResponse("user_reln_list.html",
                                      {"request": request,
                                       "data_dict": data_dict})


@api.post("/add", status_code=200)
def get_one_by_email(
        request: Request,
        response: Response,
        user_reln_id: str = Form(...),
        relationship: str = Form(...)):
    # insert reln_user_id into user_reln table along with the current user_id
    curr_user_id = session_manager.get_session_data_attrib(request, 'user_id')
    ret_sts = user_reln_dao.insert_user_reln(curr_user_id, user_reln_id, relationship)

    status_message = ''
    error_message = ''
    if ret_sts:
        status_message = 'User has been added successfully'
    else:
        error_message = 'User has not been added successfully'

    data_dict = {}
    data_dict['reln_email'] = ''
    data_dict['status_message'] = status_message
    data_dict['error_message'] = error_message

    curr_user_reln_df = user_reln_dao.get_all_related_users(session_manager.get_session_data_attrib(request, 'user_id'))
    data_dict['user_reln_list'] = utils.convert_dataframe_to_dict(curr_user_reln_df)

    return templates.TemplateResponse("user_reln_list.html",
                                      {"request": request,
                                       "data_dict": data_dict})
