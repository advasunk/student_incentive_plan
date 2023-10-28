from fastapi import APIRouter, Request, Form
from starlette.responses import HTMLResponse

from __init__ import templates
from auth import session_manager
from common import platform_data_definitions
from dao import task_dao, course_year_dao
from utils import utils

api = APIRouter(tags=['course api'], prefix="/task")


@api.get("", status_code=200, response_class=HTMLResponse)
async def get_all_tasks_by_teacher(request: Request):
    # get all courses from database
    user_id = session_manager.get_session_data_attrib(request, 'user_id')
    data = task_dao.get_all_tasks_by_course_teacher(user_id)
    return templates.TemplateResponse("course_task_list.html",
                                      {"request": request, "data": utils.convert_dataframe_to_dict(data)})

@api.get("/all", status_code=200, response_class=HTMLResponse)
async def get_all_tasks(request: Request):
    # get all courses from database
    data = task_dao.get_all_tasks_by_course()
    return templates.TemplateResponse("course_task_list.html",
                                      {"request": request, "data": utils.convert_dataframe_to_dict(data)})


@api.get("/add", status_code=200, response_class=HTMLResponse)
async def show_add_task_page(request: Request):
    data_dict = {}
    data_dict['status_message'] = ''
    data_dict['error_message'] = ''

    data_dict['task_name'] = 'name'
    data_dict['task_type'] = 'type'
    data_dict['task_description'] = 'desc'
    data_dict['task_due_date'] = '10/23/2023'
    data_dict['task_score'] = '100'

    data_dict['academic_year_list'] = platform_data_definitions.academic_year_list
    course_list = course_year_dao.get_course_data_by_year(academic_year='2023-24')
    data_dict['course_list'] = utils.convert_dataframe_to_dict(course_list)

    print(data_dict)

    return templates.TemplateResponse("course_task_add.html",
                                      {"request": request,
                                       "data_dict": data_dict
                                       })


@api.post("/", status_code=200, response_class=HTMLResponse)
async def save_task_data(request: Request, academic_year: str = Form(...),
                         year_course_reln_id: str = Form(...),
                         task_name: str = Form(...),
                         task_type: str = Form(...),
                         task_description: str = Form(...),
                         task_due_date: str = Form(...),
                         task_score: str = Form(...)):
    ret_sts = task_dao.insert_task(year_course_reln_id, task_name, task_type, task_description,
                                   task_due_date, task_score)

    data_dict = {}
    data_dict['status_message'] = ''
    data_dict['error_message'] = ''
    data_dict['academic_year_list'] = platform_data_definitions.academic_year_list
    data_dict['academic_year'] = academic_year
    data_dict['task_name'] = task_name
    data_dict['task_type'] = task_type
    data_dict['task_description'] = task_description
    data_dict['task_due_date'] = task_due_date
    data_dict['task_score'] = task_score
    course_list = course_year_dao.get_course_data_by_year(academic_year='2023-24')
    data_dict['course_list'] = utils.convert_dataframe_to_dict(course_list)

    if ret_sts:
        data_dict['error_message'] = 'Task ({}) could not be added to the course'.format(task_name)
    else:
        data_dict['status_message'] = 'Task is added successfully to the course'

    return templates.TemplateResponse("course_task_add.html",
                                      {"request": request,
                                       "data_dict": data_dict
                                       })
