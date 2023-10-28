from fastapi import APIRouter, Request, Form
from starlette.responses import HTMLResponse

from auth import session_manager
from common import platform_data_definitions
from __init__ import templates
from dao import course_dao
from utils import utils

api = APIRouter(tags=['course api'], prefix="/course")


@api.get("", status_code=200, response_class=HTMLResponse)
async def get_all_courses_by_teacher(request: Request):
    # get all courses from database
    user_id = session_manager.get_session_data_attrib(request, 'user_id')
    # if logged in user is Admin, get all courses
    if utils.is_admin_user(request):
        data = course_dao.get_all_courses()
    else:
        data = course_dao.get_course_data_by_teacher_id(user_id)

    return templates.TemplateResponse("course_list.html",
                                      {"request": request, "data": utils.convert_dataframe_to_dict(data)})


@api.get("/add", status_code=200, response_class=HTMLResponse)
async def show_add_course_page(request: Request):
    course_name = utils.get_request_attribute(request, 'course_name', '')
    subject = utils.get_request_attribute(request, 'subject', '')
    course_description = utils.get_request_attribute(request, 'course_description', '')
    status_message = ''
    error_message = ''
    data_dict = utils.build_data_dict(None, '', '', 'courses')
    data_dict['subject_list'] = sorted(platform_data_definitions.course_subject_list, key=lambda k: k['subject'])
    return templates.TemplateResponse("course_add.html",
                                      {"request": request,
                                       "course_name": course_name,
                                       "subject": subject,
                                       "course_description": course_description,
                                       'data_dict': data_dict,
                                       "status_message": status_message,
                                       "error_message": error_message})


@api.post("/", status_code=200, response_class=HTMLResponse)
async def save_course_data(request: Request, course_name: str = Form(...),
                           subject: str = Form(...),
                           course_description: str = Form(...)):
    # course_name = utils.get_request_attribute(request, 'course_name', '')
    # subject = utils.get_request_attribute(request, 'subject', '')
    # course_description = utils.get_request_attribute(request, 'course_description', '')

    ret_sts = course_dao.insert_course(course_name, subject, course_description)

    status_message = ''
    error_message = ''
    if ret_sts:
        status_message = 'Course ' + course_name + ' has been added successfully'
    else:
        error_message = 'Course ' + course_name + ' has not been added successfully'

    data_dict = utils.build_data_dict(None, '', '', 'courses')
    # sort the list platform_data_definitions.course_subject_list based on the value of the key
    data_dict['subject_list'] = sorted(platform_data_definitions.course_subject_list, key=lambda k: k['subject'])
    # data_dict['subject_list'] = platform_data_definitions.course_subject_list

    return templates.TemplateResponse("course_add.html",
                                      {"request": request,
                                       "course_name": course_name,
                                       "subject": subject,
                                       "course_description": course_description,
                                       'data_dict': data_dict,
                                       "status_message": status_message,
                                       "error_message": error_message
                                       })
