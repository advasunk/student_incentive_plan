from fastapi import APIRouter, Request, Form
from starlette.responses import HTMLResponse

from __init__ import templates
from auth import session_manager
from common import platform_data_definitions
from dao import course_year_dao, user_dao, course_dao
from utils import utils

api = APIRouter(tags=['academic year to course relation api'], prefix="/course_year")


@api.get("", status_code=200, response_class=HTMLResponse)
async def get_all_courses_by_year_(request: Request):
    user_id = session_manager.get_session_data_attrib(request, 'user_id')
    # if logged in user is Admin, get all courses
    if utils.is_admin_user(request):
        data = course_year_dao.get_all_courses_year_list()
    else:
        data = course_year_dao.get_all_courses_year_list_by_teacher_id(user_id)

    return templates.TemplateResponse("course_year_list.html",
                                      {"request": request, "data": utils.convert_dataframe_to_dict(data)})


@api.get("/add", status_code=200, response_class=HTMLResponse)
async def show_add_course_page(request: Request):
    data_dict = {}
    data_dict['status_message'] = ''
    data_dict['error_message'] = ''
    data_dict['academic_year_list'] = platform_data_definitions.academic_year_list
    data_dict['room_number'] = utils.get_request_attribute(request, 'room_number', '')
    course_list = course_dao.get_all_courses()
    data_dict['course_list'] = utils.convert_dataframe_to_dict(course_list)
    teacher_list = user_dao.get_all_users_by_user_type('teacher')
    data_dict['teacher_list'] = utils.convert_dataframe_to_dict(teacher_list)

    return templates.TemplateResponse("course_year_add.html",
                                      {"request": request,
                                       "data_dict": data_dict
                                       })


@api.post("/", status_code=200, response_class=HTMLResponse)
async def save_course_year_data(request: Request, academic_year: str = Form(...),
                                course_id: str = Form(...),
                                room_number: str = Form(...),
                                teacher_id: str = Form(...)):
    ret_sts = False

    try:
        ret_sts = course_year_dao.insert_course_year_data(academic_year, course_id, room_number,
                                                          teacher_id)
    except Exception as e:
        print(e)
        error_message = str(e)  # "Course is already assigned to an Acadamic year"
        ret_sts = False

    data_dict = {}
    data_dict['status_message'] = ''
    data_dict['error_message'] = ''
    data_dict['academic_year'] = academic_year
    data_dict['course_id'] = course_id
    data_dict['room_number'] = room_number
    data_dict['teacher_id'] = teacher_id
    data_dict['academic_year_list'] = platform_data_definitions.academic_year_list
    course_list = course_dao.get_all_courses()
    data_dict['course_list'] = utils.convert_dataframe_to_dict(course_list)
    teacher_list = user_dao.get_all_users_by_user_type('teacher')
    data_dict['teacher_list'] = utils.convert_dataframe_to_dict(teacher_list)

    if ret_sts:
        data_dict['status_message'] = 'Course has been added successfully'
    elif error_message is not None and len(error_message) > 0:
        data_dict['error_message'] = error_message
    else:
        data_dict['error_message'] = 'Course has not been added successfully'

    return templates.TemplateResponse("course_year_add.html",
                                      {"request": request,
                                       "data_dict": data_dict
                                       })
