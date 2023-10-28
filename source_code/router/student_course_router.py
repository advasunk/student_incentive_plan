from fastapi import APIRouter, Request, Form
from starlette.responses import HTMLResponse

from common import platform_data_definitions
from dao import user_dao, user_course_dao, course_year_dao
from utils import utils
from __init__ import templates

api = APIRouter(tags=['user api'], prefix="/student_course")


@api.get("", status_code=200, response_class=HTMLResponse)
async def get_all_users(request: Request):
    # get parameter from request
    user_role = utils.get_request_attribute(request, 'r')
    user_id = utils.get_request_attribute(request, 'id')

    if user_role == platform_data_definitions.UserRole.STUDENT.value:
        data = user_course_dao.get_user_courses_by_user_id(user_id)
    elif user_role == platform_data_definitions.UserRole.TEACHER.value:
        data = user_course_dao.get_user_courses_by_teacher_id(user_id)
    elif user_role == platform_data_definitions.UserRole.ADMIN.value:
        data = user_course_dao.get_all_user_courses()
    else:
        data = []

    print(data)
    return templates.TemplateResponse("student_course_list.html",
                                      {"request": request, "data": utils.convert_dataframe_to_dict(data)})


@api.get("/add", status_code=200, response_class=HTMLResponse)
async def show_add_user_page(request: Request):
    data_dict = {}
    data_dict['status_message'] = ''
    data_dict['error_message'] = ''
    student_list = user_dao.get_all_users_by_user_type('student')
    data_dict['student_list'] = utils.convert_dataframe_to_dict(student_list)

    data_dict['user_id'] = utils.get_request_attribute(request, 'user_id', '')
    data_dict['year_course_reln_id'] = utils.get_request_attribute(request, 'year_course_reln_id', '')

    courses_by_year = course_year_dao.get_course_data_by_year(academic_year='2023-24')
    courses_by_year['course_desc'] = ('[' + courses_by_year['academic_year'] + ']' + ' ' +
                                      '[' + courses_by_year['subject'] + ']' + ' ' +
                                      courses_by_year['course_name'] + ' by ' +
                                      courses_by_year['teacher_name'])

    data_dict['courses_by_year'] = utils.convert_dataframe_to_dict(courses_by_year)

    print(data_dict)

    return templates.TemplateResponse("student_course_add.html",
                                      {"request": request,
                                       "data_dict": data_dict
                                       })


@api.post("/add", status_code=200, response_class=HTMLResponse)
async def save_user_course_data(request: Request, user_id: str = Form(...),
                         year_course_reln_id: str = Form(...)):
    data_dict = {}
    data_dict['status_message'] = ''
    data_dict['error_message'] = ''
    data_dict['user_id'] = user_id
    data_dict['year_course_reln_id'] = year_course_reln_id

    # check if user is already enrolled in the course
    df = user_course_dao.get_user_course_data_by_user_id_and_year_course_reln_id(user_id, year_course_reln_id)
    if len(df) > 0:
        data_dict['error_message'] = 'User is already enrolled in the course'
    else:
        # user is not enrolled in the course
        user_course_dao.insert_user_course(user_id, year_course_reln_id)
        data_dict['status_message'] = 'User is enrolled in the course'

    return templates.TemplateResponse("student_course_add.html",
                                      {"request": request,
                                       "data_dict": data_dict
                                       })
